# Introduction

London Gift Shop (LGS) is a UK-based online retailer generating high volumes of transactional data through its web platform. While the company collects extensive sales and customer data, raw transaction logs alone do not provide actionable business insight.

This project builds a containerized retail analytics environment that transforms transactional data into structured business intelligence. By implementing data wrangling, KPI reporting, customer behavior analysis, and RFM segmentation, this proof-of-concept enables LGS to transition from reactive reporting to data-driven marketing and revenue optimization.

The objective is to help LGS:

- Understand monthly revenue trends
- Identify customer growth and churn patterns
- Segment customers by value
- Design precision marketing campaigns
- Increase retention and lifetime value

Technologies Used:

- Python
- Pandas / NumPy
- Matplotlib
- PostgreSQL (Dockerized OLAP)
- SQLAlchemy
- Jupyter Notebook
- Docker (Containerized environment)
- Git & GitHub (Feature Branch Workflow)

---

# Implementation

## Project Architecture

The architecture follows a separation-of-concerns design that isolates analytics from production systems.

### Data Flow

1. LGS Web Application  
   Generates transactional order data.

2. Data Extraction  
   LGS IT team provides a sanitized SQL dump / CSV file.

3. Local Analytics Environment (Docker)
   - PostgreSQL container (Data Warehouse - OLAP)
   - Jupyter Notebook container (Analytics Layer)
   - Bridge Network enables container communication

4. Data Processing
   - Load retail data into PostgreSQL
   - Use Pandas for wrangling & feature engineering
   - Compute KPIs and segmentation

5. Business Insight Generation
   - Sales trends
   - Growth metrics
   - Customer segmentation (RFM)
   - Retention analysis

This architecture ensures:

- Secure separation from production
- Reproducibility
- Portability
- Scalability for future automation

---

## Data Analytics and Wrangling

Notebook Link:  
[Retail Data Analytics Notebook](./python_data_analytics/python_data_wrangling/retail_data_analytics_wrangling.ipynb)

### 1?? Data Preparation

- Standardized column names (snake_case)
- Converted datatypes (datetime, numeric)
- Calculated invoice-level revenue
- Identified canceled orders
- Engineered year_month features
- Aggregated transactional data

---

### 2?? Sales & Revenue Analysis

- Monthly Sales Trend
- Monthly Sales Growth (%)
- Moving Average smoothing
- Distribution of invoice amounts
- Outlier handling

? Business Value:
- Detect seasonal spikes
- Evaluate campaign effectiveness
- Monitor revenue stability

---

### 3?? Customer Behavior Analysis

- Monthly Active Users
- New vs Existing Users
- Order Placement vs Cancellation Trends

? Business Value:
- Identify growth momentum
- Measure retention quality
- Detect churn risk periods

---

### 4?? RFM (Recency, Frequency, Monetary) Analysis

RFM segmentation categorizes customers based on behavioral patterns:

Recency ? How recently a customer purchased  
Frequency ? How often a customer purchases  
Monetary ? Total spending value  

Using this model, customers are segmented into groups such as:

- Champions
- Loyal Customers
- At Risk
- Hibernating
- Potential Loyalists
- New Customers

? Marketing Impact:

High Recency + High Frequency + High Monetary  
? VIP treatment & retention programs

High Monetary but High Recency  
? Aggressive win-back campaigns

Low Frequency + Low Monetary  
? Nurture & upsell strategies

This enables targeted marketing instead of generic promotions, improving ROI and retention.

---

# How This Increases LGS Revenue

The analytics output directly supports:

1. Customer Retention Optimization  
   Identify and re-engage at-risk customers before churn.

2. Revenue Expansion  
   Upsell high-value customers through loyalty programs.

3. Marketing Budget Efficiency  
   Segment-based campaigns instead of mass discounts.

4. Growth Monitoring  
   Track monthly growth and customer acquisition trends.

5. Strategic Planning  
   Identify peak sales periods for inventory and marketing alignment.

---

# Improvements

If given additional time, I would enhance the project by:

1?? Automating ETL  
Convert notebook logic into scheduled ETL jobs using Airflow.

2?? Predictive Modeling  
Add churn prediction and customer lifetime value (CLV) forecasting.

3?? Interactive Dashboard  
Build a Streamlit or Power BI dashboard for non-technical stakeholders.

4?? CI/CD Pipeline  
Integrate automated testing and deployment workflow.

5?? Cloud Deployment  
Deploy analytics pipeline on Azure/GCP for scalability.


