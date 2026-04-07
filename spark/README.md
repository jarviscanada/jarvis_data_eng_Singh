
# Retail Data Analytics Using Zeppelin and Databricks

## Introduction

Retail organizations generate large volumes of transactional data through their e-commerce platforms. However, extracting meaningful business insights from this data requires scalable analytics infrastructure capable of processing large datasets efficiently.

This project demonstrates how distributed Spark environments can be used to analyze retail transaction data and generate business insights using two big-data analytics platforms:

Apache Zeppelin running on Hadoop (GCP Dataproc)
Databricks using PySpark (cloud Spark environment)

The goal of this project is to design a scalable analytics workflow that supports KPI generation, customer behaviour analysis, and segmentation using Spark-based processing pipelines.

The dataset contains retail transaction records, including:

* Invoice Number
* Product Description
* Quantity
* Invoice Date
* Unit Price
* Customer ID
* Country

Using this dataset, several business analytics workflows were implemented including:

* Monthly sales trend analysis
* Customer activity tracking
* Cancelled vs completed order comparison
* Country-level revenue insights
* Customer segmentation using the RFM model

Technologies used:

* PostgreSQL (transactional dataset source)
* Hadoop Distributed File System (HDFS)
* GCP dataproc
* Apache Zeppelin
* Databricks
* PySpark DataFrame API
* Spark SQL
* Hive Metastore
* JDBC ingestion
* Git & GitHub

### This project was implemented using two different analytics platforms:

1. Apache Zeppelin on Hadoop (GCP Dataproc)
2. Databricks using PySpark DataFrame API

### Databricks Architecture

<p align="center">
  <img src="./assets/arch.png" alt="Retail Analytics Architecture" width="900">
</p>




























[Retail Data Analytics with PySpark Notebook](./notebook/Retail%20Data%20Analytics%20with%20PySpark.ipynb)

---

### Databricks Architecture

<p align="center">
  <img src="./assets/arch.png" alt="Retail Analytics Architecture" width="900">
</p>

Workflow:

```text
PostgreSQL Retail Dataset
        |
        | JDBC Connection
        v
Databricks Notebook
        |
        v
PySpark Data Cleaning
        |
        v
KPI Analytics
        |
        v
Customer Segmentation (RFM Model)
