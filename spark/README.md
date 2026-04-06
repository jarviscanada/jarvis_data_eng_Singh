# Retail Data Analytics Using Zeppelin and Databricks
![Retail Analytics Architecture](./assets/arch.png)

## Introduction

This project demonstrates how retail transaction data can be analyzed using distributed big data platforms such as **Apache Zeppelin (Hadoop ecosystem)** and **Databricks (PySpark environment)**. The objective of this project is to extract business insights from raw retail transaction datasets and implement customer analytics workflows using Spark-based processing environments.

The dataset contains transactional retail records including:

- Invoice Number
- Stock Code
- Product Description
- Quantity
- Invoice Date
- Unit Price
- Customer ID
- Country

Using this dataset, multiple business KPIs were generated along with customer segmentation analytics using **RFM modeling**.

This project was implemented using two different analytics platforms:

1. Apache Zeppelin on Hadoop (GCP Dataproc)
2. Databricks using PySpark DataFrame API

Technologies used:

- PostgreSQL (data warehouse)
- Hadoop / Hive Metastore
- Apache Zeppelin
- Databricks
- PySpark DataFrame API
- Spark SQL
- JDBC ingestion
- Git & GitHub version control

---

# Databricks and Hadoop Implementation

## Dataset and Analytics Work

Retail transaction data was loaded from PostgreSQL into Databricks using JDBC. The dataset was cleaned and transformed using PySpark DataFrame APIs before performing KPI analytics and customer segmentation.

Analytics implemented:

- Data cleaning and preprocessing
- Monthly sales trend analysis
- Month-over-month growth
- Monthly active customers
- New vs returning customers
- Monthly placed vs cancelled orders
- Invoice value distribution
- RFM customer segmentation

Databricks notebook:

[Retail Data Analytics with PySpark Notebook](./notebook/Retail%20Data%20Analytics%20with%20PySpark.ipynb)

---

## Databricks Architecture

<p align="center">
  <img src="./assets/arch.png" alt="Retail Analytics Architecture" width="900">
</p> 
