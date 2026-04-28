# =========================
# Bronze Layer
# =========================
import dlt
from pyspark.sql import functions as F

RAW_BASE_PATH = "/Volumes/pyspark_module/stock_dlt/raw_stock_data"


@dlt.table(
    name="bronze_daily_stock_raw",
    comment="Raw daily stock price data from Alpha Vantage API",
    table_properties={"delta.columnMapping.mode": "name"}
)
def bronze_daily_stock_raw():
    return (
        spark.read
        .option("multiline", "true")
        .json(f"{RAW_BASE_PATH}/daily_prices/*/*.json")
        .withColumn("source_file", F.col("_metadata.file_path"))
        .withColumn("bronze_ingest_ts", F.current_timestamp())
    )


@dlt.table(
    name="bronze_quote_raw",
    comment="Raw latest quote data from Alpha Vantage API",
    table_properties={"delta.columnMapping.mode": "name"}
)
def bronze_quote_raw():
    return (
        spark.read
        .option("multiline", "true")
        .json(f"{RAW_BASE_PATH}/quotes/*/*.json")
        .withColumn("source_file", F.col("_metadata.file_path"))
        .withColumn("bronze_ingest_ts", F.current_timestamp())
    )


@dlt.table(
    name="bronze_company_info_raw",
    comment="Raw company overview data from Alpha Vantage API",
    table_properties={"delta.columnMapping.mode": "name"}
)
def bronze_company_info_raw():
    return (
        spark.read
        .option("multiline", "true")
        .json(f"{RAW_BASE_PATH}/company_info/*/*.json")
        .withColumn("source_file", F.col("_metadata.file_path"))
        .withColumn("bronze_ingest_ts", F.current_timestamp())
    )