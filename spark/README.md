# Retail Data Analytics Using Zeppelin and Databricks

## Introduction

This project demonstrates how retail transaction data can be analyzed using distributed data processing tools such as Apache Zeppelin and Databricks with PySpark. The goal of this project is to generate business insights from transactional retail datasets and implement customer analytics workflows using Hadoop-based and cloud-based notebook environments.

The dataset contains retail transaction records including:

- Invoice Number
- Stock Code
- Product Description
- Quantity
- Invoice Date
- Unit Price
- Customer ID
- Country

This project implements analytics pipelines using two different big data environments:

1. Apache Zeppelin on Hadoop (GCP Dataproc)
2. Databricks using PySpark DataFrame API

Technologies used:

- PostgreSQL
- Hadoop / Hive Metastore
- Apache Zeppelin
- Databricks
- PySpark
- JDBC ingestion
- Spark SQL
- Git & GitHub

---

## Databricks and Hadoop Implementation

### Dataset and Analytics Work

Retail transaction data was loaded from PostgreSQL using JDBC into Databricks. The dataset was cleaned and transformed using PySpark DataFrame APIs to generate business KPIs and customer segmentation insights.

Key analytics implemented:

- Data cleaning and preprocessing
- Monthly sales trend analysis
- Month-over-month growth
- Monthly active customers
- New vs returning customers
- Monthly placed vs cancelled orders
- Invoice value distribution
- RFM segmentation

Notebook:

