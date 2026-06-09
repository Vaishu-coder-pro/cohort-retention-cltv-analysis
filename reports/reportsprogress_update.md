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