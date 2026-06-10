Phase 1 Progress Update – 09/06/2026

Today I completed the data cleaning and preprocessing stage of the Olist E-Commerce dataset.

The work started by integrating multiple datasets related to customers, orders, products, sellers and payments into a single master dataset. After merging the data, I analysed the dataset structure and identified missing values, inconsistent records and date format issues.

Numerical columns were handled using suitable imputation methods, while categorical columns were filled with meaningful placeholder values. Date columns were converted into proper datetime format to support time-based analysis.

Several new features were created including delivery_days, delivery_delay and delivery_status. These features help in analysing order fulfilment performance and customer experience.

I then performed RFM (Recency, Frequency and Monetary) analysis to understand customer purchasing behaviour. Based on RFM scores, customers were segmented into groups such as Champions, Loyal Customers, At Risk and Others.

Finally, the cleaned dataset was validated, all remaining missing values were handled and the final cleaned master dataset was exported for further analysis.

Current Status:
- Data Integration Completed
- Data Cleaning Completed
- Missing Value Treatment Completed
- Feature Engineering Completed
- Delivery Analysis Completed
- RFM Segmentation Completed
- Clean Dataset Exported

Next Step:
Customer Lifetime Value (CLTV) Analysis 


Second Half Update (09.06.2026)

Today I continued working on Project 2 and completed the Cohort Retention Analysis. I created the Purchase Month, Cohort Month and Cohort Index features, then generated the retention matrix and retention rate table to analyse customer retention behaviour over time.

After completing the cohort analysis, I worked on Business Insights Analysis using the cleaned dataset. I calculated important business metrics such as total revenue, total customers, total orders and average delivery days. I also analysed revenue by product category, state-wise revenue performance, payment methods and delivery status.

The generated datasets were saved for future dashboard development and reporting. I also updated the notebooks with explanations and outputs and pushed the latest work to the GitHub repository.

Current completed modules:

* Data Cleaning and Preparation
* Feature Engineering
* RFM Analysis
* CLTV Analysis
* Cohort Retention Analysis
* Business Insights Analysis

Next, I plan to work on Product Analysis, Customer Clustering, Churn Analysis, Revenue Forecasting and Power BI dashboard development.


# Daily Progress Report – 10.06.2026

## Work Completed

### Product Analysis

Completed detailed product performance analysis using the cleaned Olist dataset.

Activities performed:

* Analysed top revenue-generating product categories.
* Identified most sold product categories.
* Calculated monthly revenue trends.
* Analysed top revenue-generating products.
* Generated product performance KPIs.
* Exported dashboard-ready datasets.

Deliverables:

* product_category_revenue.csv
* monthly_revenue.csv
* top_categories.csv

### Customer Clustering Analysis

Implemented customer segmentation using K-Means Clustering.

Activities performed:

* Created customer-level aggregation dataset.
* Engineered customer behavioural features including revenue, frequency, average order value and recency.
* Applied feature standardisation.
* Performed K-Means clustering.
* Generated customer cluster profiles.
* Analysed cluster-wise revenue contribution.
* Created customer segment distribution reports.

Deliverables:

* customer_clusters.csv
* cluster_summary.csv
* cluster_revenue.csv

### Churn Analysis

Performed customer churn and retention intelligence analysis.

Activities performed:

* Calculated customer recency.
* Created churn flags and churn rate metrics.
* Developed churn risk segmentation.
* Estimated revenue at risk.
* Created customer health scores.
* Generated customer action recommendations.
* Prepared dashboard-ready churn datasets.

Deliverables:

* customer_churn.csv
* churn_dashboard.csv
* risk_revenue.csv

### Churn Prediction Model

Developed a machine learning-based churn prediction model using Random Forest.

Activities performed:

* Prepared customer-level training dataset.
* Created churn target variable.
* Trained and evaluated the churn prediction model.
* Calculated churn probability scores.
* Generated future churn risk categories.
* Identified top future churn customers.
* Analysed feature importance.
* Exported prediction datasets for future dashboard integration.

Deliverables:

* customer_churn_predictions.csv
* future_churn_customers.csv
* feature_importance.csv
* model_performance.csv

### Documentation and Repository Updates

* Updated GitHub repository with completed notebooks and datasets.
* Added screenshots of important outputs and analysis results.
* Updated README documentation.
* Organised project folders and deliverables.
* Maintained phase-wise commit history and project tracking.

## Current Project Status

Completed Modules:

* Data Cleaning and Preparation
* Feature Engineering
* Missing Value Handling
* RFM Segmentation
* CLTV Analysis
* Cohort Retention Analysis
* Business Insights Analysis
* Product Analysis
* Customer Clustering
* Churn Analysis
* Churn Prediction Model

## Planned Work

* Revenue Forecasting
* Power BI Dashboard Development
* Streamlit Web Application
* AI Insight Generator
* Automated PDF Reporting
* Final Project Documentation
