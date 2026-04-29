import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    MapType
)


# =========================
# Silver Layer
# =========================
# Bronze now has:
# _raw_json
# _source_file
# _source_modification_time
# _source_file_size
# _ingest_timestamp
# symbol


# ---------------------------------------------------------
# Schema: Daily Stock Prices JSON
# ---------------------------------------------------------

daily_price_schema = StructType([
    StructField("1. open", StringType(), True),
    StructField("2. high", StringType(), True),
    StructField("3. low", StringType(), True),
    StructField("4. close", StringType(), True),
    StructField("5. volume", StringType(), True)
])

daily_stock_schema = StructType([
    StructField("Meta Data", MapType(StringType(), StringType()), True),
    StructField(
        "Time Series (Daily)",
        MapType(StringType(), daily_price_schema),
        True
    )
])


@dlt.table(
    name="silver_daily_stock_prices",
    comment="Cleaned and flattened daily stock price data parsed from raw Bronze JSON."
)
@dlt.expect_or_drop("valid_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_trade_date", "trade_date IS NOT NULL")
@dlt.expect_or_drop("valid_close_price", "close_price IS NOT NULL AND close_price > 0")
@dlt.expect_or_drop("valid_volume", "volume IS NOT NULL AND volume >= 0")
def silver_daily_stock_prices():

    bronze_df = dlt.read_stream("bronze_daily_stock_raw")

    parsed_df = (
        bronze_df
        .withColumn(
            "parsed_json",
            F.from_json(F.col("_raw_json"), daily_stock_schema)
        )
        .select(
            F.col("symbol"),
            F.col("_source_file"),
            F.col("_ingest_timestamp"),
            F.explode(
                F.col("parsed_json").getField("Time Series (Daily)")
            ).alias("trade_date_raw", "price_data")
        )
    )

    return (
        parsed_df
        .select(
            F.col("symbol"),
            F.to_date(F.col("trade_date_raw")).alias("trade_date"),
            F.col("price_data").getField("1. open").cast("double").alias("open_price"),
            F.col("price_data").getField("2. high").cast("double").alias("high_price"),
            F.col("price_data").getField("3. low").cast("double").alias("low_price"),
            F.col("price_data").getField("4. close").cast("double").alias("close_price"),
            F.col("price_data").getField("5. volume").cast("long").alias("volume"),
            F.col("_source_file"),
            F.col("_ingest_timestamp"),
            F.current_timestamp().alias("silver_processed_ts")
        )
        .dropDuplicates(["symbol", "trade_date"])
    )


# ---------------------------------------------------------
# Schema: Latest Quote JSON
# ---------------------------------------------------------

quote_schema = StructType([
    StructField(
        "Global Quote",
        StructType([
            StructField("01. symbol", StringType(), True),
            StructField("02. open", StringType(), True),
            StructField("03. high", StringType(), True),
            StructField("04. low", StringType(), True),
            StructField("05. price", StringType(), True),
            StructField("06. volume", StringType(), True),
            StructField("07. latest trading day", StringType(), True),
            StructField("08. previous close", StringType(), True),
            StructField("09. change", StringType(), True),
            StructField("10. change percent", StringType(), True)
        ]),
        True
    )
])


@dlt.table(
    name="silver_stock_quotes",
    comment="Cleaned latest quote snapshot data parsed from raw Bronze JSON."
)
@dlt.expect_or_drop("valid_quote_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_quote_price", "price IS NOT NULL AND price > 0")
@dlt.expect_or_drop("valid_latest_trading_day", "latest_trading_day IS NOT NULL")
def silver_stock_quotes():

    bronze_df = dlt.read_stream("bronze_quote_raw")

    parsed_df = (
        bronze_df
        .withColumn(
            "parsed_json",
            F.from_json(F.col("_raw_json"), quote_schema)
        )
        .withColumn(
            "quote",
            F.col("parsed_json").getField("Global Quote")
        )
    )

    return (
        parsed_df
        .select(
            F.coalesce(
                F.col("quote").getField("01. symbol"),
                F.col("symbol")
            ).alias("symbol"),
            F.col("quote").getField("05. price").cast("double").alias("price"),
            F.col("quote").getField("06. volume").cast("long").alias("volume"),
            F.to_date(
                F.col("quote").getField("07. latest trading day")
            ).alias("latest_trading_day"),
            F.col("quote").getField("08. previous close").cast("double").alias("previous_close"),
            F.col("quote").getField("09. change").cast("double").alias("change"),
            F.regexp_replace(
                F.col("quote").getField("10. change percent"),
                "%",
                ""
            ).cast("double").alias("change_percent"),
            F.col("_source_file"),
            F.col("_ingest_timestamp"),
            F.current_timestamp().alias("silver_processed_ts")
        )
        .dropDuplicates(["symbol", "latest_trading_day"])
    )


# ---------------------------------------------------------
# Schema: Company Overview JSON
# ---------------------------------------------------------

company_schema = StructType([
    StructField("Symbol", StringType(), True),
    StructField("AssetType", StringType(), True),
    StructField("Name", StringType(), True),
    StructField("Description", StringType(), True),
    StructField("Exchange", StringType(), True),
    StructField("Currency", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("Sector", StringType(), True),
    StructField("Industry", StringType(), True),
    StructField("MarketCapitalization", StringType(), True),
    StructField("PERatio", StringType(), True),
    StructField("PEGRatio", StringType(), True),
    StructField("EPS", StringType(), True),
    StructField("RevenueTTM", StringType(), True),
    StructField("ProfitMargin", StringType(), True),
    StructField("AnalystTargetPrice", StringType(), True),
    StructField("Beta", StringType(), True),
    StructField("52WeekHigh", StringType(), True),
    StructField("52WeekLow", StringType(), True),
    StructField("50DayMovingAverage", StringType(), True),
    StructField("200DayMovingAverage", StringType(), True)
])


@dlt.table(
    name="silver_company_info",
    comment="Cleaned company overview data parsed from raw Bronze JSON."
)
@dlt.expect_or_drop("valid_company_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_company_name", "company_name IS NOT NULL")
def silver_company_info():

    bronze_df = dlt.read_stream("bronze_company_info_raw")

    parsed_df = (
        bronze_df
        .withColumn(
            "company",
            F.from_json(F.col("_raw_json"), company_schema)
        )
    )

    return (
        parsed_df
        .select(
            F.coalesce(
                F.col("company").getField("Symbol"),
                F.col("symbol")
            ).alias("symbol"),
            F.col("company").getField("Name").alias("company_name"),
            F.col("company").getField("Exchange").alias("exchange"),
            F.col("company").getField("Sector").alias("sector"),
            F.col("company").getField("Industry").alias("industry"),
            F.col("company").getField("MarketCapitalization").cast("double").alias("market_capitalization"),
            F.col("company").getField("Country").alias("country"),
            F.col("company").getField("Currency").alias("currency"),
            F.col("company").getField("PERatio").cast("double").alias("pe_ratio"),
            F.col("company").getField("EPS").cast("double").alias("eps"),
            F.col("company").getField("RevenueTTM").cast("double").alias("revenue_ttm"),
            F.col("company").getField("ProfitMargin").cast("double").alias("profit_margin"),
            F.col("company").getField("AnalystTargetPrice").cast("double").alias("analyst_target_price"),
            F.col("company").getField("Beta").cast("double").alias("beta"),
            F.col("company").getField("52WeekHigh").cast("double").alias("week_52_high"),
            F.col("company").getField("52WeekLow").cast("double").alias("week_52_low"),
            F.col("company").getField("50DayMovingAverage").cast("double").alias("moving_avg_50_day"),
            F.col("company").getField("200DayMovingAverage").cast("double").alias("moving_avg_200_day"),
            F.col("_source_file"),
            F.col("_ingest_timestamp"),
            F.current_timestamp().alias("silver_processed_ts")
        )
        .dropDuplicates(["symbol"])
    )