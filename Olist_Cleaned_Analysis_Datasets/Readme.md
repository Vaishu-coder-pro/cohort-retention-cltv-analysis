


CUSTOMER CLUSTERING &
PRODUCT PERFORMANCE ANALYSIS
Olist Brazilian E-Commerce Platform  |  2016–2018

Prepared for Data Analytics Internship  |  June 2025


EXECUTIVE SUMMARY
This report looks closely at Olist's Brazilian e-commerce dataset from September 2016 to October 2018. It covers 99,441 orders, 93,358 unique customers, and 32,951 distinct products across 72 categories. To turn the raw data into business insight, the analysis uses RFM (Recency-Frequency-Monetary) modelling, K-Means clustering, ABC inventory analysis, geographic profiling, and delivery performance benchmarking.

99,441
Total Orders
96,478 delivered (97.0%)	93,358
Unique Customers
Delivered-order base	R$15.4M
Gross Revenue
Delivered orders only	R$160
Avg Order Value
Incl. freight

4.09 / 5
Avg Review Score
92,755 scored orders	93.2%
On-Time Delivery
Median 10 days	3.0%
Repeat Purchase Rate
2,801 repeat buyers	Health & Beauty
Top Category
R$1.23M | 8,647 orders

Key Findings at a Glance
Customer Base: Most customers (97%) placed only one order, which shows that the business is still heavily driven by new customer acquisition rather than repeat purchasing. The small repeat-buyer group, only 3% of the customer base, is still very important because it generates 5.6% of total revenue.
Segmentation: The RFM analysis separates customers into eight clear segments. 'Champions' (7.0% of the base) and 'Loyal Customers' (15.2%) together contribute 32.2% of revenue. The 'Cannot Lose Them' group (9.3%) is especially important because it contains high-value customers who have not returned and should be treated as the main winback target.
K-Means Clustering: The clustering model produced five practical customer groups. One group stands out as a serious quality concern: Cluster 2, with around 13,000 customers, has an average review score of only 1.54. The main driver is late delivery, with average delivery taking 23 days compared with about -13 days of delay for the more satisfied clusters.
Product Portfolio: Health & Beauty, Watches & Gifts, and Bed, Bath & Table are the top three revenue categories. ABC analysis shows that 8,351 products, or 26% of the SKU base, produce 80% of revenue. At the same time, several freight-heavy categories are likely losing margin because shipping costs are too high relative to product prices.
Geography: São Paulo (SP) is the strongest market, generating 38.3% of revenue. The Southeast corridor (SP+RJ+MG) accounts for 63.4% of revenue overall. There is still clear room to grow in northern and central-western states, where average order values are above the national average.

1. DATASET OVERVIEW & METHODOLOGY
1.1 Data Architecture
The Olist public dataset is built from nine related tables. For this report, the tables were combined into one analytical dataset using order_id and customer_id as the main join keys. Customer behaviour modelling was limited to orders marked as 'delivered' so that revenue and delivery timelines remained reliable.

Dataset	Records	Key Fields	Role in Analysis
olist_orders	99,441	order_id, status, timestamps	Master order table; status & timeline analysis
olist_customers	99,441	customer_id, unique_id, state	Customer identity & geography
olist_order_items	112,650	order_id, product_id, price, freight	Revenue, basket size, freight cost
olist_order_payments	103,886	order_id, payment_type, installments	Payment behaviour
olist_order_reviews	104,719	order_id, review_score	Customer satisfaction
olist_products	32,951	product_id, category, dimensions	Product catalogue
olist_sellers	3,095	seller_id, state	Seller geography
product_category_name_translation	71	category (PT/EN)	Category labelling

1.2 Analytical Methodology
Data Preparation
•	Date fields were parsed and timezone-normalised across all five order timestamp columns.
•	Customers were de-duplicated with customer_unique_id instead of session-level customer_id so the analysis could follow real individuals across multiple sessions.
•	Product categories were translated from Portuguese to English, while 2,402 records with missing categories were kept and flagged as 'Unknown'.
•	Freight and item prices were aggregated at the order level before the final joins were created.
Customer Analytics
•	RFM Modelling: Recency, Frequency, and Monetary values were scored on a 1-5 quintile scale, and the combined RFM score was then used for rule-based segment assignment.
•	K-Means Clustering: The best cluster count was selected using the elbow method and silhouette score analysis from k=2 to k=7. Features were log-transformed and standardised with StandardScaler before model fitting. The best result was k=5 with a silhouette score of 0.288.
Product Analytics
•	ABC Analysis: Products were ranked by cumulative revenue contribution. Class A represents the top 80% of revenue, Class B the next 15%, and Class C the remaining 5%.
•	Categories were compared across revenue, average price, review score, and freight-to-price ratio.
•	Monthly revenue trends were reviewed to identify seasonality and the overall growth pattern.

2. CUSTOMER SEGMENTATION: RFM ANALYSIS
2.1 RFM Framework
RFM (Recency-Frequency-Monetary) is a commonly used customer segmentation method. Each customer is scored from 1 to 5 on recency, frequency, and monetary value, then those scores are combined to assign a segment. This analysis covers 93,358 unique customers with at least one delivered order.

238 days
Avg Recency
Days since last purchase	1.03 orders
Avg Frequency
Max: 15 orders	R$165
Avg Monetary
Per customer LTV	4.15 / 5
Avg Review Score
Across RFM base

2.2 Segment Profiles

Segment	Customers	% Base	Avg Recency	Avg Monetary	Total Revenue	Rev %	Avg Review
Champions	6,497	7.0%	91 days	R$312	R$2,027,031	13.1%	4.16
Loyal Customers	14,210	15.2%	153 days	R$207	R$2,942,647	19.1%	4.06
Cannot Lose Them	8,676	9.3%	395 days	R$241	R$2,089,724	13.6%	4.13
New Customers	14,984	16.1%	91 days	R$163	R$2,448,694	15.9%	4.20
At-Risk Customers	22,230	23.8%	395 days	R$167	R$3,711,040	24.1%	4.17
Potential Loyalists	14,588	15.6%	143 days	R$55	R$795,736	5.2%	4.19
Needs Attention	5,863	6.3%	220 days	R$180	R$1,052,866	6.8%	4.00
Lost / Hibernating	6,310	6.8%	397 days	R$56	R$352,035	2.3%	4.25

2.3 Segment Deep-Dives
Champions (7.0% | R$2.0M | 13.1% revenue)
Champions are the platform's strongest customer group. They purchased recently (91 days ago on average), buy more often than most customers, and have the highest average spend per customer (R$312). Although they make up only 7% of the base, they contribute a much larger share of revenue. Their 4.16 review score shows that they are generally satisfied, but not the most satisfied segment, which may mean their expectations are higher. Recommended actions include VIP loyalty programme enrollment, early access to new categories, and personalised upsell offers for complementary products.
Loyal Customers (15.2% | R$2.9M | 19.1% revenue)
Loyal Customers generate the largest revenue share and form the commercial backbone of the platform. Their average recency of 153 days shows they are still engaged, although their purchase cycle is longer. They are good candidates for targeted re-engagement campaigns and subscription-style offers. Cross-selling based on their earlier category purchases should be the main growth lever.
Cannot Lose Them (9.3% | R$2.1M | 13.6% revenue)
This is the highest-priority winback group. These 8,676 customers used to spend heavily, with an average of R$241 per customer, close to the Champions segment, but they have not purchased in about 13 months. Their past spend and long absence suggest that some may have moved to competitors. Personalised outreach, including discounts on categories they bought before, should be launched within 30 days.
At-Risk Customers (23.8% | R$3.7M | 24.1% revenue)
At-Risk Customers are the largest segment by both customer count and revenue contribution, so they represent a major churn risk. Their average recency is 395 days, but their monetary value is still mid-range, which suggests many are lapsed rather than completely lost. Automated email or push re-engagement with time-sensitive offers is recommended. Higher-spending customers inside this group should be prioritised for direct outreach.
New Customers (16.1% | R$2.4M | 15.9% revenue)
New Customers purchased recently (91 days ago on average), but their frequency is exactly 1.0, meaning they have not yet made a second purchase. The first 90 days are important: in e-commerce, converting a first-time buyer into a second-time buyer before that point can raise long-term retention probability by 2-4x. Onboarding messages with category recommendations should begin right after first delivery.

  KEY INSIGHT: The Retention Crisis
  ✓  97% of all customers make exactly one purchase—the platform is almost entirely acquisition-dependent.
  ✓  Even a 1% improvement in repeat rate would add ~930 new repeat buyers, worth approx. R$290,000 in incremental LTV.
  ✓  The 'New Customers' cohort (14,984) must be the primary retention battleground within the next 90 days.
  ✓  Champions + Loyal Customers represent only 22.2% of customers but drive 32.2% of revenue—protect them at all cost.

3. K-MEANS CUSTOMER CLUSTERING
3.1 Clustering Approach & Model Selection
K-Means clustering was run on six standardised, log-transformed behavioural features: Recency, Frequency, Monetary Value, Average Order Value, Average Review Score, and Average Delivery Days. The cluster count was chosen empirically. The silhouette score, used as the main model-selection metric, was highest at k=5 (score=0.288), with k=4 and k=6 also reviewed as secondary options.

k (Clusters)	Within-Cluster Inertia	Silhouette Score	Assessment
2	93,067	0.2405	Under-segmented; insufficient granularity
3	76,621	0.2584	Improving; three broad archetypes
4	62,545	0.2767	Good; competitive candidate
5 (OPTIMAL)	52,810	0.2881	Best silhouette; operationally interpretable
6	46,787	0.2615	Score drops; cluster fragmentation
7	42,179	0.2689	Marginal recovery; over-segmented

3.2 Cluster Profiles & Business Interpretation
The five clusters below are compared across the main business metrics. Each cluster has been given a practical business label based on the behaviour that defines it most clearly.

Cluster	Label	Count	Rev Share	Avg Recency	Avg AOV	Avg Review	Avg Del. Days	Avg Delay
0	High-Value Satisfied	27,329	55.3%	267 days	R$310	4.58	12 days	-14 days
1	Recent Low-Spend	13,889	10.2%	42 days	R$112	4.50	7 days	-12 days
2	Dissatisfied / Late Delivery	12,173	13.0%	248 days	R$163	1.54	23 days	-3 days
3	Repeat Mid-Value	2,792	5.6%	220 days	R$146	4.21	12 days	-13 days
4	Low-Spend Lapsed	36,564	15.9%	288 days	R$66	4.57	10 days	-13 days

Cluster 0 – High-Value Satisfied (27,329 customers | 55.3% revenue)
This is the platform's most commercially important cluster. Customers in this group spent an average of R$310 per order, rated their experience 4.58/5, and received orders 14 days earlier than the estimated date. Even though they are moderately lapsed (267 days), their high spend and positive sentiment suggest strong repurchase potential if the right trigger is used. This cluster overlaps strongly with the RFM Champions and Loyal Customers segments.
Cluster 1 – Recent Low-Spend (13,889 customers | 10.2% revenue)
This is the most recently active cluster, with only 42 days since the last purchase. Satisfaction is strong (4.50), and delivery is fast at 7 days on average. The low average order value (R$112) likely comes from a tilt toward lower-priced categories. This is a growth cluster: customers are active and satisfied, so targeted upsell into higher-value categories is the best monetisation lever. They are also strong candidates for subscription or bundle offers.
Cluster 2 – Dissatisfied / Late Delivery (12,173 customers | CRITICAL RISK)
This cluster is the biggest operational warning sign in the dataset. Its average review score is only 1.54/5, far below every other cluster, and the main reason is delivery performance. Average delivery time is 23 days, compared with 7-12 days for the other clusters. Average delay is only -3 days, compared with -12 to -14 days for satisfied clusters, meaning these customers received orders much closer to the promised date or genuinely late.
The link between delivery delay and review score is very clear. Orders delivered more than 5 days late average only 1.77/5, while early deliveries average 4.32. This is not mainly a product quality issue. It is a logistics problem that is lowering satisfaction, hurting brand trust, and almost certainly increasing churn.

  CRITICAL ALERT: Cluster 2 Dissatisfaction Cascade
  ⚠  12,173 customers averaging 1.54/5 review score—this cohort is driving down the platform-level NPS equivalent.
  ⚠  Root cause is logistics: 23-day average delivery vs 7-12 days for satisfied clusters.
  ⚠  Data shows: late deliveries (>5 days) score 1.77/5 vs. on-time/early at 4.12-4.32/5.
  ⚠  Priority action: Audit seller-level fulfilment times; identify which sellers and which routes are causing delays.
  ⚠  These customers require immediate service recovery outreach (apology + discount voucher) before permanent churn.

Cluster 3 – Repeat Mid-Value (2,792 customers)
This is the smallest cluster, but it matters strategically because it is the only group with meaningful repeat-order behaviour, averaging 2.11 orders. With an average order value of R$146 and a positive review score of 4.21, these are the platform's real repeat customers. Their category preferences, seller relationships, and geographic profile should be studied closely to guide the design of a wider loyalty programme.
Cluster 4 – Low-Spend Lapsed (36,564 customers | 15.9% revenue)
This is the largest cluster by customer count. These customers spent modestly (R$66 average AOV), were satisfied (4.57/5), received their orders on time (-13 days), but have not returned in 288 days. The low spend may reflect category-specific buying, such as a single low-cost item, or general price sensitivity. Reactivation campaigns should focus on value-based messages such as promotions, bundles, and free-shipping thresholds.

4. PRODUCT & CATEGORY ANALYSIS
4.1 Revenue Overview

72
Total Categories
Active in delivered orders	32,951
Total SKUs
Unique products	R$120
Avg Price per Item
Excl. freight	R$19.9
Avg Freight / Order
17% of avg item price

4.2 Top 15 Categories by Revenue

#	Category	Orders	Revenue	Avg Price	Avg Review	Rev %	Freight %
1	Health & Beauty	8,647	R$1,233,132	R$130	4.19	9.5%	14.5%
2	Watches & Gifts	5,495	R$1,166,177	R$199	4.07	8.9%	8.4%
3	Bed, Bath & Table	9,272	R$1,023,435	R$93	3.92	7.9%	19.7%
4	Sports & Leisure	7,530	R$954,853	R$113	4.17	7.3%	17.1%
5	Computers & Accessories	6,530	R$888,725	R$116	3.99	6.8%	16.2%
6	Furniture & Decor	6,307	R$711,928	R$87	3.96	5.5%	23.7%
7	Housewares	5,743	R$615,629	R$91	4.11	4.7%	23.2%
8	Cool Stuff	3,559	R$610,204	R$164	4.19	4.7%	13.4%
9	Auto	3,810	R$578,967	R$140	4.12	4.4%	15.6%
10	Toys	3,804	R$471,286	R$117	4.21	3.6%	16.1%
11	Garden Tools	3,448	R$470,495	R$110	4.08	3.6%	20.5%
12	Baby	2,809	R$400,422	R$134	4.08	3.1%	16.6%
13	Perfumery	3,086	R$390,145	R$117	4.22	3.0%	13.6%
14	Telephony	4,093	R$309,860	R$70	3.99	2.4%	22.4%
15	Office Furniture	1,254	R$268,154	R$161	3.52	2.1%	25.0%

4.3 ABC Inventory Analysis
ABC analysis groups products by their cumulative revenue contribution so the business can prioritise assortment planning, stock availability, and promotional investment. The results show a highly concentrated revenue pattern that is consistent with Pareto's 80/20 principle.

ABC Class	Product Count	% SKUs	Total Revenue	Rev %	Avg Price	Avg Review
A (Core Revenue Drivers)	8,351	25.3%	R$10,577,147	80.0%	R$328	4.11
B (Supporting Products)	11,058	33.6%	R$1,983,227	15.0%	R$122	4.11
C (Long-Tail SKUs)	12,807	38.9%	R$661,124	5.0%	R$44	4.14
Total	32,216	100%	R$13,221,498	100%	R$167	4.11

Class A products (8,351 SKUs) generate 80% of platform revenue while making up only 25% of the catalogue. Class C products (12,807 SKUs) produce just 5% of revenue, creating a lot of assortment complexity without matching commercial return. Class C should therefore be reviewed, especially SKUs that also have high freight-to-price ratios.

  ABC Strategic Implications
  ✓  Class A SKUs deserve maximum availability, premium placement, and dedicated marketing investment.
  ✓  Class C long-tail SKUs should be reviewed for profitability after freight cost—many sub-R$44 avg-price items with 25%+ freight ratios likely generate negative contribution margin.
  ✓  New product launches should be benchmarked against Class A category metrics before assortment inclusion.
  ✓  Supplier negotiations for Class A products should prioritise lead time reduction over cost alone.

4.4 Price Segmentation Analysis

Price Band	Orders	Revenue	% Revenue	Avg Price	Insight
R$0-50 (Budget)	32,494	R$1,212,249	9.2%	R$31	High volume, low value; freight often exceeds margin
R$50-100 (Entry)	28,703	R$2,432,918	18.4%	R$75	Strong order volume; core accessible segment
R$100-200 (Mid-Market)	24,137	R$3,785,031	28.6%	R$144	Highest revenue tier; sweet spot for LTV
R$200-500 (Premium)	9,335	R$2,926,502	22.1%	R$297	High value per order; lower but quality volume
R$500+ (Luxury/High Ticket)	2,992	R$2,864,799	21.7%	R$927	Small volume, massive value; 3% of orders, 22% revenue

The R$100-200 mid-market band is the clearest commercial sweet spot. It contributes the largest revenue share (28.6%) while still keeping healthy order volume and unit economics. The R$500+ high-ticket segment is also important: only 2,992 orders, or 3% of total orders, generate R$2.86M, equal to 21.7% of product revenue. This segment should receive dedicated curation, premium service standards, and focused customer success support.
4.5 Freight-to-Price Ratio Analysis
Freight cost as a share of item price is a key profitability signal. Categories with freight ratios above 25% are at high risk of negative contribution margin once platform fees and seller costs are included.

Category	Avg Item Price	Avg Freight	Freight %	Risk Level
Office Furniture	R$161	R$40.2	25.0%	HIGH
Furniture, Living Room	R$136	R$35.8	26.3%	HIGH
Kitchen/Garden Furniture	R$166	R$42.1	25.3%	HIGH
Electronics	R$57	R$16.7	29.5%	CRITICAL
Food & Drink	R$56	R$16.3	29.4%	CRITICAL
Drinks	R$60	R$15.1	25.3%	HIGH
Furniture & Decor	R$87	R$20.6	23.7%	ELEVATED
Housewares	R$91	R$21.0	23.2%	ELEVATED
Telephony	R$70	R$16.8	24.0%	ELEVATED

5. GEOGRAPHIC & PAYMENT ANALYSIS
5.1 State-Level Revenue Distribution

Rank	State	Orders	Revenue	% Revenue	Unique Cust.	Avg Order Value
1	SP (São Paulo)	40,501	R$5,067,633	38.3%	39,156	R$125
2	RJ (Rio de Janeiro)	12,350	R$1,759,651	13.3%	11,917	R$142
3	MG (Minas Gerais)	11,354	R$1,552,482	11.7%	11,001	R$137
4	RS (Rio Grande do Sul)	5,345	R$728,897	5.5%	5,168	R$136
5	PR (Paraná)	4,923	R$666,064	5.0%	4,769	R$135
6	SC (Santa Catarina)	3,546	R$507,012	3.8%	3,449	R$143
7	BA (Bahia)	3,256	R$493,584	3.7%	3,158	R$152
8	DF (Brasília)	2,080	R$296,498	2.2%	2,019	R$143
9	GO (Goiás)	1,957	R$282,837	2.1%	1,895	R$145
10	CE (Ceará)	1,279	R$219,757	1.7%	1,258	R$172
11	PA (Pará)	946	R$174,471	1.3%	922	R$184
12	MT (Mato Grosso)	886	R$152,192	1.1%	856	R$172

São Paulo's 38.3% revenue share is driven by both its population size and its closeness to many Olist sellers, most of whom are based in SP. This helps reduce freight cost and delivery time. The Southeast corridor (SP+RJ+MG) generates 63.4% of total revenue even though it represents about 42% of Brazil's population, which suggests stronger-than-average e-commerce adoption in this region.
Several lower-volume states still show strong potential. Pará (R$184 average order), Ceará (R$172), and Mato Grosso (R$172) all have above-average order values despite fewer orders. This suggests that demand exists, but supply coverage and logistics may be limiting growth. These states should be treated as priority geographic expansion opportunities.

  Geographic Expansion Opportunity
  ✓  Northern and Central-Western states (PA, MT, CE, MA) show AOVs 10-47% above SP, signalling pent-up demand.
  ✓  SP-RJ-MG concentration creates systemic risk: any logistics disruption in Southeast Brazil cascades to 63% of revenue.
  ✓  Seller recruitment campaigns targeting fulfillment centres in Bahia, Pará, and Ceará would reduce delivery times to those states and likely increase both order volume and review scores.

5.2 Payment Behaviour Analysis

Payment Type	Transaction Count	% Transactions	Total Value	Avg Installments	Profile
Credit Card	76,795	73.9%	R$12,542,084	3.51	Core payment method; instalment-driven
Boleto (Bank Slip)	19,784	19.0%	R$2,869,361	1.00	Unbanked/credit-averse segment; typically lower AOV
Voucher	5,775	5.6%	R$379,437	1.00	Promotion/loyalty redemption; strong retention signal
Debit Card	1,529	1.5%	R$217,990	1.00	Low frequency; likely cautious, lower-income segment

Credit cards dominate payments, accounting for 73.9% of transactions with an average of 3.51 installments. This reflects a key feature of Brazilian e-commerce behaviour: installment purchasing, or parcelamento, makes higher-priced products more accessible. Around 36% of credit card orders use 4 or more installments, allowing customers to buy items they may not purchase in one full payment.
Boleto accounts for 19% of payments and represents the financially underserved or credit-averse customer segment, making it an important inclusion metric. Voucher use, at 5.6%, is also a positive signal because customers who redeem vouchers have already stayed engaged enough with the brand to use a promotion, which points to good reuse potential.

Installment Count	Credit Card Orders	% of CC Orders
1 (Full payment)	25,455	33.2%
2	12,413	16.2%
3	10,461	13.6%
4	7,098	9.2%
5	5,239	6.8%
6	3,920	5.1%
8	4,268	5.6%
10	5,328	6.9%

6. DELIVERY PERFORMANCE & CUSTOMER SATISFACTION
6.1 Delivery Performance Metrics

93.2%
On-Time Delivery Rate
6.8% late deliveries	12.1 days
Avg Delivery Time
Median: 10 days	-13 days
Avg Early Arrival
Before estimated date	+10.6 days
Avg Late Arrival
When late

The platform's 93.2% on-time delivery rate looks strong at first, but it hides an important risk: the 6.8% of late orders receive review scores that are 2-3 points lower than on-time orders. The estimated delivery window appears to include a large buffer, with orders arriving 13 days early on average. This improves the on-time rate, but it may also reduce urgency inside logistics operations.
6.2 The Delivery-Satisfaction Relationship

Delivery Timing	Avg Review Score	Interpretation
>10 days early	4.32 / 5	Excellent: strong delight effect
5-10 days early	4.26 / 5	Very Good: exceeds expectations
On time (0 days)	4.12 / 5	Good: meets expectations
1-5 days late	2.99 / 5	POOR: expectations broken; serious dissatisfaction
6-10 days late	1.77 / 5	CRITICAL: experience-destroying; high churn risk
>10 days late	1.65 / 5	CRITICAL: total failure; immediate churn + negative reviews

The table shows that delivery affects satisfaction unevenly. Customers who receive orders early are only moderately more satisfied, with scores rising from 4.12 to 4.32, a 0.2-point gain. Late deliveries, however, cause a much sharper drop, from 4.12 to 1.65-2.99, a decline of 1-2.5 points. The business message is clear: preventing late delivery is 5-10x more valuable for satisfaction than making already-early deliveries even faster.
6.3 Review Score Distribution

Score	Order Count	% of Scored Orders	Cumulative %
5 (Excellent)	57,328	57.6%	57.6%
4 (Good)	19,142	19.2%	76.8%
3 (Neutral)	8,179	8.2%	85.0%
2 (Poor)	3,151	3.2%	88.2%
1 (Very Poor)	11,424	11.5%	100%

Review scores are strongly split between very good and very bad experiences. 57.6% of customers give a 5/5, while 11.5% give a 1/5, making 1/5 the second-most-common score. Scores of 2 and 3 are rare, which suggests customers usually feel the experience either worked well or failed badly. This pattern is typical when satisfaction is driven by logistics: smooth delivery feels excellent, while delivery failure creates severe disappointment.

  Operational Priority: Eliminate Late Deliveries
  ⚠  11.5% of all reviewed orders received a 1/5 score—this is the #1 brand damage vector.
  ⚠  The 6.8% late delivery rate translates to approximately 6,560 severely dissatisfied customers.
  ⚠  Cluster 2 (12,173 customers, 1.54 avg score) is the concentrated manifestation of this problem.
  ⚠  Recommended action: Seller-level SLA enforcement, fulfilment audits, and real-time delay alerting to customer service.
  ⚠  A proactive 'delay apology + 10% voucher' protocol for orders projected to be late would recover significant satisfaction.

7. BUSINESS GROWTH & TRENDS
7.1 Monthly Revenue Trajectory
Revenue grew strongly from 2017 to 2018, with revenue rising by roughly 2.5x from the early 2017 peaks to the sustained 2018 level. The dataset captures about 22 full months of operating history after the initial ramp-up in late 2016.

Period	Monthly Revenue	Monthly Orders	Avg Order Value	YoY Growth
Q1 2017 (avg)	R$235,074	1,650	R$142	Baseline
Q2 2017 (avg)	R$417,310	2,995	R$139	+77%
Q3 2017 (avg)	R$547,901	3,738	R$147	+133%
Q4 2017 (avg)	R$787,349	5,760	R$137	+235%
Q1 2018 (avg)	R$901,479	6,876	R$131	+284%
Q2 2018 (avg)	R$935,719	6,549	R$143	+124%
Q3 2018 (avg)	R$853,265	6,255	R$137	Partial data

November 2017 clearly stands out at R$987,765, which is 57% higher than the previous month. This is consistent with Black Friday and Cyber Monday promotions. The spike is useful for planning because peak-period logistics pressure is likely one of the main reasons behind late deliveries and the rise in 1-star reviews.
Growth appears to level off in H2 2018 compared with the sharp rise seen in 2017. This may reflect market maturity, stronger competition, or the natural limit of a growth model that depends mainly on customer acquisition. It reinforces the need to move from acquisition-only growth to a model that also improves retention.
7.2 Order Status Analysis

Status	Count	% Total	Business Implication
Delivered	96,478	97.0%	Core operational base; analysis foundation
Shipped	1,107	1.1%	In-transit at data snapshot; expected delivery
Canceled	625	0.6%	Lost revenue; cancel reason analysis recommended
Unavailable	609	0.6%	Seller fulfilment failure; inventory/availability issue
Invoiced	314	0.3%	Payment processed; awaiting fulfilment
Processing	301	0.3%	Pre-fulfilment stage; seller response time monitor

The 0.6% cancellation rate and 0.6% unavailability rate together equal about 1,234 failed commercial transactions. The percentage is small, but with an average order value of R$160, this still represents roughly R$197,000 in direct lost revenue. Seller-level cancellation rates should be tracked as a seller performance KPI.

8. STRATEGIC RECOMMENDATIONS
8.1 Immediate Actions (0-30 Days)

1.	Deploy Cluster 2 Service Recovery Campaign: Reach out to all 12,173 Cluster 2 customers with a personalised apology, a 15% discount voucher for the next purchase, and a clear message that service is being improved. Expected recovery is 8-12% reactivation at better satisfaction levels.
2.	Launch 'Cannot Lose Them' Winback Sequence: Start personalised outreach for 8,676 high-value lapsed customers with an average spend of R$241. Use category-specific messages based on their previous purchases. A/B test discount levels of 10%, 15%, and 20% to find the best recovery incentive.
3.	Implement Late Delivery Alert Protocol: Create real-time monitoring for orders likely to miss the estimated delivery date. If an order becomes T+1 day late, automatically send a customer update and a compensatory voucher. This turns a satisfaction-damaging event into a service-recovery opportunity.
4.	New Customer Onboarding Programme: The 14,984 New Customers, including overlap with Cluster 1, are in the critical 90-day conversion window. Run a 3-email onboarding sequence: Day 7 after delivery with category recommendations, Day 30 with an engagement offer, and Day 60 with a loyalty incentive.
8.2 Medium-Term Initiatives (30-90 Days)
5.	Seller Logistics Audit: Identify the seller groups responsible for most late deliveries. Introduce seller performance scoring with SLA thresholds. Also consider expanding logistics partnerships in northern Brazil to reduce delivery times and freight costs.
6.	Class C SKU Rationalisation: Review the profitability of all 12,807 Class C products. Remove or deprioritise SKUs with freight ratios above 25% and below-average review scores. This will simplify operations, reduce logistics complexity, and improve the platform's average quality score.
7.	High-Ticket Segment Curation (R$500+): The R$500+ price band creates 21.7% of product revenue from only 3% of orders. Invest in premium seller acquisition, white-glove packaging standards, and dedicated support queues for this segment to improve conversion and reduce returns.
8.3 Long-Term Strategic Priorities (90+ Days)
8.	Loyalty Programme Infrastructure: Build a points-based loyalty programme using the behaviour patterns of Cluster 3, the 2,792 repeat buyers. If the repeat rate increases from 3.0% to 5.0%, the extra 1,867 repeat buyers would generate around R$590,000 in additional annual LTV.
9.	Geographic Expansion into High-AOV States: Focus seller recruitment and logistics hub development on Pará (R$184 AOV), Ceará (R$172), and Mato Grosso (R$172). Shorter delivery times in these states should directly improve review scores and repeat rates.
10.	Predictive Churn Modelling: Build a real-time churn prediction model using RFM trajectory features. If a customer reaches 90 days after purchase without a second order, trigger re-engagement automatically. Use Cluster 2 delivery-delay features as early warning signals for satisfaction-driven churn before it appears in reviews.

9. CONCLUSIONS
This analysis of Olist's 2016-2018 e-commerce dataset shows a platform at an important turning point. Revenue growth and geographic reach are strong, but the business is still highly dependent on new customer acquisition, while delivery-related satisfaction issues are quietly weakening brand equity.
Five core conclusions emerge from this work:

11.	Retention is the #1 strategic lever. A 97% single-purchase rate means the business is running hard just to replace customers instead of building compounding value. The data, infrastructure, and customer relationships needed for repeat purchasing already exist. The missing piece is execution.
12.	Logistics is part of the product experience. Review scores are shaped heavily by delivery performance. Product quality and pricing improvements cannot fully make up for late deliveries. Strong fulfilment performance is therefore a requirement for sustainable growth.
13.	Portfolio concentration is efficient but fragile. Having 8,351 SKUs generate 80% of revenue is commercially useful, but it also creates supply-chain risk. Availability of Class A products should be managed as a business-critical metric.
14.	Geographic diversification can reduce systemic risk. The 63% revenue concentration in the Southeast is a strength because the infrastructure is already there, but it is also a vulnerability if that region faces disruption. Expansion in northern states supports both growth and risk reduction.
15.	Cluster 2 is the most urgent business issue. A group of 12,173 customers averaging only 1.54/5 in satisfaction can create a compounding problem through negative word of mouth and public reviews. Service recovery for this group should be treated as necessary, not optional.

Overall, the data shows a platform with strong growth momentum, solid product-market fit, and a clear set of operational problems that management can address. The priority order is straightforward: fix logistics, retain customers, and then expand geographically.

APPENDIX: TECHNICAL NOTES
A. Data Quality Notes
•	2,402 products, equal to 7.3% of SKUs, had missing category translations and were excluded from category-level revenue calculations.
•	961 orders, or 1.0%, had missing review scores and were excluded from satisfaction calculations. No imputation was applied.
•	3 payment records with the 'not_defined' payment type and R$0 total value were excluded from the payment analysis.
•	Recency was calculated using the dataset snapshot date of 2018-08-30, one day after the last recorded delivered order.
•	The geolocation table was not used in the main analysis because it contains 1.6M records. State-level analysis was instead derived directly from the customer table.
B. Clustering Technical Parameters
•	Features used: Recency (log), Frequency, Monetary (log), Average Order Value (log), Average Review Score, and Average Delivery Days.
•	Pre-processing: Log transformation was applied to Recency, Monetary, and AvgOrderValue to reduce right-skewed distributions. StandardScaler was applied to all features.
•	Missing values, mainly AvgReviewScore for unreviewed orders, were imputed with the feature median before scaling. 603 records were excluded because delivery timestamps were missing.
•	Model selection: The silhouette score was evaluated on a 20,000-record stratified sample using random seed 42. The final model was then fitted on the full 92,747-record dataset.
•	Algorithm: sklearn KMeans with n_init=5, max_iter=200, random_state=42.
C. RFM Scoring Methodology
•	Recency: Scored from 5 for most recent to 1 for least recent, using quintiles based on absolute days since the last purchase.
•	Frequency: Scored from 1 to 5 using quintiles on rank-transformed frequency with method='first' to handle the heavy concentration at frequency=1.
•	Monetary: Scored from 1 to 5 based on total delivered-order spend, including freight, using quintiles on raw values.
•	Segment assignment: Rule-based logic was applied to the individual R/F/M scores. Hierarchy: Champions > Loyal > New > Potential Loyalists > At-Risk > Cannot Lose Them > Lost/Hibernating > Needs Attention.

END OF REPORT
Olist E-Commerce Analytics  |  Customer Clustering & Product Analysis  |  Prepared for Data Analytics Internship

