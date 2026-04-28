import dlt
from pyspark.sql import functions as F


# =========================
# Silver Layer
# =========================

@dlt.table(
    name="silver_daily_stock_prices",
    comment="Cleaned and flattened daily stock price data"
)
@dlt.expect_or_drop("valid_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_trade_date", "trade_date IS NOT NULL")
@dlt.expect_or_drop("valid_close_price", "close_price IS NOT NULL AND close_price > 0")
@dlt.expect_or_drop("valid_volume", "volume IS NOT NULL AND volume >= 0")
def silver_daily_stock_prices():
    bronze_df = dlt.read("bronze_daily_stock_raw")

    date_cols = [
        field.name
        for field in bronze_df.schema["Time Series (Daily)"].dataType.fields
    ]

    stack_expr = "stack({}, {}) as (trade_date, price_data)".format(
        len(date_cols),
        ", ".join([
            f"'{date_col}', `Time Series (Daily)`.`{date_col}`"
            for date_col in date_cols
        ])
    )

    return (
        bronze_df
        .select(
            F.col("`Meta Data`.`2. Symbol`").alias("symbol"),
            F.expr(stack_expr)
        )
        .select(
            F.col("symbol"),
            F.to_date("trade_date").alias("trade_date"),
            F.col("price_data.`1. open`").cast("double").alias("open_price"),
            F.col("price_data.`2. high`").cast("double").alias("high_price"),
            F.col("price_data.`3. low`").cast("double").alias("low_price"),
            F.col("price_data.`4. close`").cast("double").alias("close_price"),
            F.col("price_data.`5. volume`").cast("long").alias("volume"),
            F.current_timestamp().alias("silver_processed_ts")
        )
        .dropDuplicates(["symbol", "trade_date"])
    )


@dlt.table(
    name="silver_stock_quotes",
    comment="Cleaned latest quote snapshot data"
)
@dlt.expect_or_drop("valid_quote_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_quote_price", "price IS NOT NULL AND price > 0")
@dlt.expect_or_drop("valid_latest_trading_day", "latest_trading_day IS NOT NULL")
def silver_stock_quotes():
    bronze_df = dlt.read("bronze_quote_raw")

    return (
        bronze_df
        .select(
            F.col("`Global Quote`.`01. symbol`").alias("symbol"),
            F.col("`Global Quote`.`05. price`").cast("double").alias("price"),
            F.col("`Global Quote`.`06. volume`").cast("long").alias("volume"),
            F.to_date(F.col("`Global Quote`.`07. latest trading day`")).alias("latest_trading_day"),
            F.col("`Global Quote`.`08. previous close`").cast("double").alias("previous_close"),
            F.col("`Global Quote`.`09. change`").cast("double").alias("change"),
            F.regexp_replace(
                F.col("`Global Quote`.`10. change percent`"),
                "%",
                ""
            ).cast("double").alias("change_percent"),
            F.current_timestamp().alias("silver_processed_ts")
        )
    )


@dlt.table(
    name="silver_company_info",
    comment="Cleaned company overview data"
)
@dlt.expect_or_drop("valid_company_symbol", "symbol IS NOT NULL")
@dlt.expect_or_drop("valid_company_name", "company_name IS NOT NULL")
def silver_company_info():
    bronze_df = dlt.read("bronze_company_info_raw")

    return (
        bronze_df
        .select(
            F.col("Symbol").alias("symbol"),
            F.col("Name").alias("company_name"),
            F.col("Exchange").alias("exchange"),
            F.col("Sector").alias("sector"),
            F.col("Industry").alias("industry"),
            F.col("MarketCapitalization").cast("double").alias("market_capitalization"),
            F.col("Country").alias("country"),
            F.col("Currency").alias("currency"),
            F.current_timestamp().alias("silver_processed_ts")
        )
    )