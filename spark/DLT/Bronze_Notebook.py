import dlt

from pyspark.sql.functions import (
    col,
    current_timestamp,
    regexp_extract
)

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    TimestampType,
    LongType,
    BinaryType
)


RAW_BASE_PATH = "/Volumes/pyspark_module/stock_dlt/raw_stock_data"

DAILY_PRICES_PATH = f"{RAW_BASE_PATH}/daily_prices"
QUOTES_PATH = f"{RAW_BASE_PATH}/quotes"
COMPANY_INFO_PATH = f"{RAW_BASE_PATH}/company_info"


# ------------------------------------------------------------
# Schema required for streaming binaryFile source
# ------------------------------------------------------------

binary_file_schema = StructType([
    StructField("path", StringType(), True),
    StructField("modificationTime", TimestampType(), True),
    StructField("length", LongType(), True),
    StructField("content", BinaryType(), True)
])


# ------------------------------------------------------------
# Bronze Table 1: Raw Daily Stock Prices
# ------------------------------------------------------------

@dlt.table(
    name="bronze_daily_stock_raw",
    comment="Raw daily stock price JSON files loaded incrementally using spark.readStream."
)
def bronze_daily_stock_raw():
    return (
        spark.readStream
            .format("binaryFile")
            .schema(binary_file_schema)
            .load(DAILY_PRICES_PATH)
            .select(
                col("content").cast("string").alias("_raw_json"),
                col("path").alias("_source_file"),
                col("modificationTime").alias("_source_modification_time"),
                col("length").alias("_source_file_size"),
                current_timestamp().alias("_ingest_timestamp"),
                regexp_extract(
                    col("path"),
                    r"symbol=([^/]+)",
                    1
                ).alias("symbol")
            )
    )


# ------------------------------------------------------------
# Bronze Table 2: Raw Latest Quote
# ------------------------------------------------------------

@dlt.table(
    name="bronze_quote_raw",
    comment="Raw latest quote JSON files loaded incrementally using spark.readStream."
)
def bronze_quote_raw():
    return (
        spark.readStream
            .format("binaryFile")
            .schema(binary_file_schema)
            .load(QUOTES_PATH)
            .select(
                col("content").cast("string").alias("_raw_json"),
                col("path").alias("_source_file"),
                col("modificationTime").alias("_source_modification_time"),
                col("length").alias("_source_file_size"),
                current_timestamp().alias("_ingest_timestamp"),
                regexp_extract(
                    col("path"),
                    r"symbol=([^/]+)",
                    1
                ).alias("symbol")
            )
    )


# ------------------------------------------------------------
# Bronze Table 3: Raw Company Info
# ------------------------------------------------------------

@dlt.table(
    name="bronze_company_info_raw",
    comment="Raw company overview JSON files loaded incrementally using spark.readStream."
)
def bronze_company_info_raw():
    return (
        spark.readStream
            .format("binaryFile")
            .schema(binary_file_schema)
            .load(COMPANY_INFO_PATH)
            .select(
                col("content").cast("string").alias("_raw_json"),
                col("path").alias("_source_file"),
                col("modificationTime").alias("_source_modification_time"),
                col("length").alias("_source_file_size"),
                current_timestamp().alias("_ingest_timestamp"),
                regexp_extract(
                    col("path"),
                    r"symbol=([^/]+)",
                    1
                ).alias("symbol")
            )
    )