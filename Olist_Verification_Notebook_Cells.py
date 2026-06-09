
# %% [markdown]
# # Olist Customer Clustering Verification Notebook
# 
# This notebook verifies:
# - Data cleaning
# - Customer-level feature engineering
# - K-Means clustering
# - Elbow Method
# - Silhouette Score
# - CLTV calculation
# - ABC product analysis
# - Geographic analysis
# 
# Run all cells from top to bottom.

# %% Cell 2
import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

pd.set_option('display.max_columns', 100)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

DATA_DIR = '/mnt/data'   # change this path if running locally
RANDOM_STATE = 42

# %% Cell 3
# Load datasets
customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset(1).csv'))
orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
order_items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))
reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset(1).csv'))
sellers = pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv'))
category_translation = pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))

for name, df in {
    'customers': customers,
    'orders': orders,
    'order_items': order_items,
    'payments': payments,
    'reviews': reviews,
    'products': products,
    'sellers': sellers,
    'category_translation': category_translation
}.items():
    print(f'{name:22s}', df.shape)

# %% Cell 4
# Data cleaning
datasets = [customers, orders, order_items, payments, reviews, products, sellers, category_translation]
customers, orders, order_items, payments, reviews, products, sellers, category_translation = [
    df.drop_duplicates().copy() for df in datasets
]

date_cols = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors='coerce')

reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'], errors='coerce')
reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'], errors='coerce')
order_items['shipping_limit_date'] = pd.to_datetime(order_items['shipping_limit_date'], errors='coerce')

products = products.merge(category_translation, on='product_category_name', how='left')
products['product_category_name'] = products['product_category_name'].fillna('unknown')
products['product_category_name_english'] = products['product_category_name_english'].fillna('unknown')

for col in ['product_name_lenght', 'product_description_lenght', 'product_photos_qty']:
    products[col] = products[col].fillna(0)

for col in ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']:
    products[col] = products[col].fillna(products[col].median())

order_items = order_items[(order_items['price'] >= 0) & (order_items['freight_value'] >= 0)]
payments = payments[payments['payment_value'] >= 0]

print('Cleaning complete')

# %% Cell 5
# Build order-level table without duplicating revenue
payment_agg = payments.groupby('order_id', as_index=False).agg(
    payment_value=('payment_value', 'sum'),
    payment_installments=('payment_installments', 'mean'),
    payment_methods_used=('payment_type', 'nunique'),
    primary_payment_type=('payment_type', lambda x: x.mode().iloc[0] if not x.mode().empty else 'unknown')
)

item_agg = order_items.groupby('order_id', as_index=False).agg(
    order_item_count=('order_item_id', 'count'),
    gross_item_value=('price', 'sum'),
    freight_value=('freight_value', 'sum'),
    seller_count=('seller_id', 'nunique'),
    product_count=('product_id', 'nunique')
)

review_agg = reviews.groupby('order_id', as_index=False).agg(
    review_score=('review_score', 'mean')
)

orders_enriched = (
    orders
    .merge(customers, on='customer_id', how='left')
    .merge(payment_agg, on='order_id', how='left')
    .merge(item_agg, on='order_id', how='left')
    .merge(review_agg, on='order_id', how='left')
)

orders_enriched['delivery_days'] = (
    orders_enriched['order_delivered_customer_date'] -
    orders_enriched['order_purchase_timestamp']
).dt.days

orders_enriched['delivery_delay_days'] = (
    orders_enriched['order_delivered_customer_date'] -
    orders_enriched['order_estimated_delivery_date']
).dt.days

valid_orders = orders_enriched[
    (orders_enriched['order_status'] == 'delivered') &
    (orders_enriched['order_purchase_timestamp'].notna()) &
    (orders_enriched['payment_value'].notna())
].copy()

valid_orders.shape

# %% Cell 6
# Customer-level features for K-Means
analysis_date = valid_orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

base = valid_orders.sort_values('order_purchase_timestamp')

customer_features = base.groupby('customer_unique_id').agg(
    first_purchase=('order_purchase_timestamp', 'min'),
    last_purchase=('order_purchase_timestamp', 'max'),
    frequency=('order_id', 'nunique'),
    monetary=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    avg_items_per_order=('order_item_count', 'mean'),
    avg_freight_value=('freight_value', 'mean'),
    avg_review_score=('review_score', 'mean'),
    avg_delivery_days=('delivery_days', 'mean'),
    late_delivery_rate=('delivery_delay_days', lambda x: (x > 0).mean()),
    state=('customer_state', 'first'),
    city=('customer_city', 'first')
).reset_index()

customer_features['recency_days'] = (analysis_date - customer_features['last_purchase']).dt.days
customer_features['customer_tenure_days'] = (
    customer_features['last_purchase'] - customer_features['first_purchase']
).dt.days + 1

customer_features['avg_review_score'] = customer_features['avg_review_score'].fillna(
    customer_features['avg_review_score'].median()
)

for col in ['avg_items_per_order', 'avg_freight_value', 'avg_delivery_days', 'late_delivery_rate']:
    customer_features[col] = customer_features[col].fillna(customer_features[col].median())

customer_features.head()

# %% Cell 7
# Scale clustering variables
cluster_cols = [
    'recency_days',
    'frequency',
    'monetary',
    'avg_order_value',
    'avg_review_score',
    'avg_delivery_days',
    'late_delivery_rate'
]

cluster_data = customer_features.copy()

# Cap extreme outliers to reduce distortion in distance-based clustering
for col in cluster_cols:
    cluster_data[col] = cluster_data[col].clip(
        cluster_data[col].quantile(0.01),
        cluster_data[col].quantile(0.99)
    )

scaler = StandardScaler()
X_scaled = scaler.fit_transform(cluster_data[cluster_cols])

# %% Cell 8
# Elbow Method
# Sampling is used for validation speed while keeping reproducibility.
rng = np.random.default_rng(RANDOM_STATE)
sample_idx = rng.choice(X_scaled.shape[0], size=min(10000, X_scaled.shape[0]), replace=False)
X_sample = X_scaled[sample_idx]

k_range = range(2, 11)
inertias = []

for k in k_range:
    km = MiniBatchKMeans(
        n_clusters=k,
        random_state=RANDOM_STATE,
        n_init=5,
        max_iter=100,
        batch_size=2048
    )
    km.fit(X_sample)
    inertias.append(km.inertia_)

elbow_df = pd.DataFrame({'k': list(k_range), 'inertia': inertias})
display(elbow_df)

plt.figure(figsize=(8, 5))
plt.plot(elbow_df['k'], elbow_df['inertia'], marker='o')
plt.title('Elbow Method for K-Means Customer Clustering')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia / WCSS')
plt.xticks(list(k_range))
plt.grid(True, alpha=0.3)
plt.show()

# %% Cell 9
# Silhouette Score output
silhouette_results = []

for k in k_range:
    km = MiniBatchKMeans(
        n_clusters=k,
        random_state=RANDOM_STATE,
        n_init=5,
        max_iter=100,
        batch_size=2048
    )
    labels = km.fit_predict(X_sample)
    score = silhouette_score(X_sample, labels)
    silhouette_results.append({'k': k, 'silhouette_score': score})

silhouette_df = pd.DataFrame(silhouette_results).sort_values(
    'silhouette_score', ascending=False
)

display(silhouette_df)

# %% Cell 10
# Final K-Means model
# Use the value supported by the elbow and business interpretability.
FINAL_K = 5

kmeans = MiniBatchKMeans(
    n_clusters=FINAL_K,
    random_state=RANDOM_STATE,
    n_init=10,
    max_iter=150,
    batch_size=2048
)

customer_features['cluster_id'] = kmeans.fit_predict(X_scaled)

cluster_profile = customer_features.groupby('cluster_id').agg(
    customers=('customer_unique_id', 'count'),
    recency_days=('recency_days', 'median'),
    frequency=('frequency', 'median'),
    monetary=('monetary', 'mean'),
    avg_order_value=('avg_order_value', 'mean'),
    avg_review_score=('avg_review_score', 'mean'),
    avg_delivery_days=('avg_delivery_days', 'mean'),
    late_delivery_rate=('late_delivery_rate', 'mean')
).reset_index()

cluster_profile['customer_share_pct'] = (
    cluster_profile['customers'] / cluster_profile['customers'].sum() * 100
)

display(cluster_profile.sort_values('monetary', ascending=False))

# %% Cell 11
# PCA visualization of customer clusters
pca = PCA(n_components=2, random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_scaled)

plot_df = pd.DataFrame({
    'pc1': X_pca[:, 0],
    'pc2': X_pca[:, 1],
    'cluster_id': customer_features['cluster_id'].astype(str)
})

plot_sample = plot_df.sample(n=min(10000, len(plot_df)), random_state=RANDOM_STATE)

plt.figure(figsize=(8, 6))
for cluster in sorted(plot_sample['cluster_id'].unique()):
    subset = plot_sample[plot_sample['cluster_id'] == cluster]
    plt.scatter(subset['pc1'], subset['pc2'], s=8, alpha=0.5, label=f'Cluster {cluster}')

plt.title('Customer Clusters Visualized with PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %% Cell 12
# CLTV calculation
# Historical annualized CLTV estimate:
# Estimated CLTV = Average Order Value × Annual Purchase Frequency

observation_years = max(
    (valid_orders['order_purchase_timestamp'].max() -
     valid_orders['order_purchase_timestamp'].min()).days / 365.25,
    1
)

cltv = customer_features.copy()
cltv['annual_purchase_frequency'] = cltv['frequency'] / observation_years
cltv['estimated_cltv'] = (
    cltv['avg_order_value'] * cltv['annual_purchase_frequency']
)

cltv_summary = cltv.groupby('cluster_id').agg(
    customers=('customer_unique_id', 'count'),
    avg_aov=('avg_order_value', 'mean'),
    avg_frequency=('frequency', 'mean'),
    avg_estimated_cltv=('estimated_cltv', 'mean'),
    total_historical_revenue=('monetary', 'sum')
).sort_values('avg_estimated_cltv', ascending=False)

display(cltv_summary)

# %% Cell 13
# ABC Product Analysis
product_sales = (
    order_items
    .merge(products[['product_id', 'product_category_name_english']], on='product_id', how='left')
    .merge(orders[['order_id', 'order_status']], on='order_id', how='left')
)

product_sales = product_sales[product_sales['order_status'] == 'delivered'].copy()

product_abc = product_sales.groupby(
    ['product_id', 'product_category_name_english'],
    as_index=False
).agg(
    units_sold=('order_item_id', 'count'),
    revenue=('price', 'sum'),
    freight=('freight_value', 'sum'),
    avg_price=('price', 'mean')
)

product_abc = product_abc.sort_values('revenue', ascending=False)
product_abc['revenue_share_pct'] = product_abc['revenue'] / product_abc['revenue'].sum() * 100
product_abc['cumulative_revenue_share_pct'] = product_abc['revenue_share_pct'].cumsum()

product_abc['abc_class'] = np.select(
    [
        product_abc['cumulative_revenue_share_pct'] <= 80,
        product_abc['cumulative_revenue_share_pct'] <= 95
    ],
    ['A', 'B'],
    default='C'
)

abc_summary = product_abc.groupby('abc_class').agg(
    products=('product_id', 'nunique'),
    revenue=('revenue', 'sum'),
    units_sold=('units_sold', 'sum')
).reset_index()

abc_summary['revenue_share_pct'] = (
    abc_summary['revenue'] / abc_summary['revenue'].sum() * 100
)

display(abc_summary)
display(product_abc.head(10))

# %% Cell 14
# Geographic Analysis
state_summary = valid_orders.groupby('customer_state', as_index=False).agg(
    customers=('customer_unique_id', 'nunique'),
    orders=('order_id', 'nunique'),
    revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    avg_review_score=('review_score', 'mean'),
    avg_delivery_days=('delivery_days', 'mean'),
    late_delivery_rate=('delivery_delay_days', lambda x: (x > 0).mean())
).sort_values('revenue', ascending=False)

state_summary['revenue_share_pct'] = (
    state_summary['revenue'] / state_summary['revenue'].sum() * 100
)

city_summary = valid_orders.groupby(['customer_state', 'customer_city'], as_index=False).agg(
    customers=('customer_unique_id', 'nunique'),
    orders=('order_id', 'nunique'),
    revenue=('payment_value', 'sum'),
    avg_order_value=('payment_value', 'mean'),
    avg_review_score=('review_score', 'mean'),
    avg_delivery_days=('delivery_days', 'mean')
).sort_values('revenue', ascending=False)

display(state_summary.head(10))
display(city_summary.head(10))

# %% Cell 15
# Save outputs
OUTPUT_DIR = os.path.join(DATA_DIR, 'olist_notebook_outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

customer_features.to_csv(os.path.join(OUTPUT_DIR, 'customer_clusters_verified.csv'), index=False)
cluster_profile.to_csv(os.path.join(OUTPUT_DIR, 'kmeans_cluster_profile.csv'), index=False)
elbow_df.to_csv(os.path.join(OUTPUT_DIR, 'elbow_method_inertia.csv'), index=False)
silhouette_df.to_csv(os.path.join(OUTPUT_DIR, 'silhouette_scores.csv'), index=False)
cltv_summary.to_csv(os.path.join(OUTPUT_DIR, 'cltv_summary_by_cluster.csv'))
product_abc.to_csv(os.path.join(OUTPUT_DIR, 'product_abc_analysis.csv'), index=False)
abc_summary.to_csv(os.path.join(OUTPUT_DIR, 'abc_summary.csv'), index=False)
state_summary.to_csv(os.path.join(OUTPUT_DIR, 'geographic_state_performance.csv'), index=False)
city_summary.to_csv(os.path.join(OUTPUT_DIR, 'geographic_city_performance.csv'), index=False)

print('Saved outputs to:', OUTPUT_DIR)
