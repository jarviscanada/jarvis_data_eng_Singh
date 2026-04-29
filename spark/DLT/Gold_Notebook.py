import dlt
from pyspark.sql import functions as F
from pyspark.sql.window import Window


# =========================
# Gold Layer
# =========================
# Gold tables are dashboard-ready KPI tables.
# Bronze and Silver are streaming tables.
# Gold remains materialized views because it performs BI aggregations,
# window calculations, and latest snapshot logic.


# ---------------------------------------------------------
# Gold Table 1: Price Trend Analysis
# KPI:
# - 7-day price change
# - 30-day price change
# - 90-day price change
# - 7/30/90-day percentage change
# Dashboard use:
# - Stock price performance trend
# - Compare short-term vs medium-term movement
# ---------------------------------------------------------

@dlt.table(
    name="gold_price_trend_analysis",
    comment="Dashboard-ready KPI table for 7, 30, and 90 day stock price trend analysis."
)
def gold_price_trend_analysis():

    prices_df = dlt.read("silver_daily_stock_prices")

    w = Window.partitionBy("symbol").orderBy("trade_date")

    return (
        prices_df
        .withColumn("close_price_7d_ago", F.lag("close_price", 7).over(w))
        .withColumn("close_price_30d_ago", F.lag("close_price", 30).over(w))
        .withColumn("close_price_90d_ago", F.lag("close_price", 90).over(w))

        .withColumn(
            "price_change_7d",
            F.round(F.col("close_price") - F.col("close_price_7d_ago"), 2)
        )
        .withColumn(
            "price_change_30d",
            F.round(F.col("close_price") - F.col("close_price_30d_ago"), 2)
        )
        .withColumn(
            "price_change_90d",
            F.round(F.col("close_price") - F.col("close_price_90d_ago"), 2)
        )

        .withColumn(
            "price_change_pct_7d",
            F.round(
                F.when(
                    F.col("close_price_7d_ago").isNotNull() & (F.col("close_price_7d_ago") != 0),
                    (F.col("price_change_7d") / F.col("close_price_7d_ago")) * 100
                ),
                2
            )
        )
        .withColumn(
            "price_change_pct_30d",
            F.round(
                F.when(
                    F.col("close_price_30d_ago").isNotNull() & (F.col("close_price_30d_ago") != 0),
                    (F.col("price_change_30d") / F.col("close_price_30d_ago")) * 100
                ),
                2
            )
        )
        .withColumn(
            "price_change_pct_90d",
            F.round(
                F.when(
                    F.col("close_price_90d_ago").isNotNull() & (F.col("close_price_90d_ago") != 0),
                    (F.col("price_change_90d") / F.col("close_price_90d_ago")) * 100
                ),
                2
            )
        )

        .select(
            "symbol",
            "trade_date",
            "close_price",
            "close_price_7d_ago",
            "close_price_30d_ago",
            "close_price_90d_ago",
            "price_change_7d",
            "price_change_30d",
            "price_change_90d",
            "price_change_pct_7d",
            "price_change_pct_30d",
            "price_change_pct_90d"
        )
    )


# ---------------------------------------------------------
# Gold Table 2: Volume Trend Analysis
# KPI:
# - 7-day average volume
# - 30-day average volume
# - 90-day average volume
# - current volume vs moving averages
# Dashboard use:
# - Detect unusual trading activity
# - Compare current volume against historical volume trend
# ---------------------------------------------------------

@dlt.table(
    name="gold_volume_trend_analysis",
    comment="Dashboard-ready KPI table for 7, 30, and 90 day stock volume trend analysis."
)
def gold_volume_trend_analysis():

    prices_df = dlt.read("silver_daily_stock_prices")

    w_7 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-6, 0)
    w_30 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-29, 0)
    w_90 = Window.partitionBy("symbol").orderBy("trade_date").rowsBetween(-89, 0)

    return (
        prices_df
        .withColumn("avg_volume_7d", F.round(F.avg("volume").over(w_7), 0))
        .withColumn("avg_volume_30d", F.round(F.avg("volume").over(w_30), 0))
        .withColumn("avg_volume_90d", F.round(F.avg("volume").over(w_90), 0))

        .withColumn(
            "volume_vs_7d_avg",
            F.round(F.col("volume") - F.col("avg_volume_7d"), 0)
        )
        .withColumn(
            "volume_vs_30d_avg",
            F.round(F.col("volume") - F.col("avg_volume_30d"), 0)
        )
        .withColumn(
            "volume_vs_90d_avg",
            F.round(F.col("volume") - F.col("avg_volume_90d"), 0)
        )

        .withColumn(
            "volume_vs_7d_avg_pct",
            F.round(
                F.when(
                    F.col("avg_volume_7d").isNotNull() & (F.col("avg_volume_7d") != 0),
                    (F.col("volume_vs_7d_avg") / F.col("avg_volume_7d")) * 100
                ),
                2
            )
        )
        .withColumn(
            "volume_vs_30d_avg_pct",
            F.round(
                F.when(
                    F.col("avg_volume_30d").isNotNull() & (F.col("avg_volume_30d") != 0),
                    (F.col("volume_vs_30d_avg") / F.col("avg_volume_30d")) * 100
                ),
                2
            )
        )
        .withColumn(
            "volume_vs_90d_avg_pct",
            F.round(
                F.when(
                    F.col("avg_volume_90d").isNotNull() & (F.col("avg_volume_90d") != 0),
                    (F.col("volume_vs_90d_avg") / F.col("avg_volume_90d")) * 100
                ),
                2
            )
        )

        .select(
            "symbol",
            "trade_date",
            "volume",
            "avg_volume_7d",
            "avg_volume_30d",
            "avg_volume_90d",
            "volume_vs_7d_avg",
            "volume_vs_30d_avg",
            "volume_vs_90d_avg",
            "volume_vs_7d_avg_pct",
            "volume_vs_30d_avg_pct",
            "volume_vs_90d_avg_pct"
        )
    )


# ---------------------------------------------------------
# Gold Table 3: Latest Stock Snapshot
# KPI:
# - latest close price
# - latest quote price
# - previous close
# - quote change
# - quote change %
# - company sector / industry / market cap
# Dashboard use:
# - Main stock summary dashboard
# - Latest stock overview card/table
# ---------------------------------------------------------

@dlt.table(
    name="gold_latest_stock_snapshot",
    comment="Dashboard-ready latest stock snapshot combining quote, company info, and most recent daily price."
)
def gold_latest_stock_snapshot():

    prices_df = dlt.read("silver_daily_stock_prices")
    quotes_df = dlt.read("silver_stock_quotes")
    company_df = dlt.read("silver_company_info")

    latest_price_date_df = (
        prices_df
        .groupBy("symbol")
        .agg(F.max("trade_date").alias("latest_price_date"))
    )

    latest_prices_df = (
        prices_df.alias("p")
        .join(
            latest_price_date_df.alias("m"),
            (F.col("p.symbol") == F.col("m.symbol")) &
            (F.col("p.trade_date") == F.col("m.latest_price_date")),
            "inner"
        )
        .select(
            F.col("p.symbol").alias("symbol"),
            F.col("p.trade_date").alias("latest_price_date"),
            F.col("p.open_price").alias("open_price"),
            F.col("p.high_price").alias("high_price"),
            F.col("p.low_price").alias("low_price"),
            F.col("p.close_price").alias("close_price"),
            F.col("p.volume").alias("daily_volume")
        )
    )

    return (
        latest_prices_df.alias("lp")
        .join(
            quotes_df.alias("q"),
            F.col("lp.symbol") == F.col("q.symbol"),
            "left"
        )
        .join(
            company_df.alias("c"),
            F.col("lp.symbol") == F.col("c.symbol"),
            "left"
        )
        .select(
            F.col("lp.symbol").alias("symbol"),
            F.col("c.company_name").alias("company_name"),
            F.col("c.exchange").alias("exchange"),
            F.col("c.sector").alias("sector"),
            F.col("c.industry").alias("industry"),
            F.col("c.country").alias("country"),
            F.col("c.currency").alias("currency"),

            F.col("lp.latest_price_date").alias("latest_price_date"),
            F.col("lp.open_price").alias("open_price"),
            F.col("lp.high_price").alias("high_price"),
            F.col("lp.low_price").alias("low_price"),
            F.col("lp.close_price").alias("close_price"),
            F.col("lp.daily_volume").alias("daily_volume"),

            F.col("q.price").alias("quote_price"),
            F.col("q.previous_close").alias("previous_close"),
            F.col("q.change").alias("quote_change"),
            F.col("q.change_percent").alias("quote_change_percent"),
            F.col("q.latest_trading_day").alias("quote_latest_trading_day"),

            F.col("c.market_capitalization").alias("market_capitalization"),
            F.col("c.pe_ratio").alias("pe_ratio"),
            F.col("c.eps").alias("eps"),
            F.col("c.revenue_ttm").alias("revenue_ttm"),
            F.col("c.profit_margin").alias("profit_margin"),
            F.col("c.analyst_target_price").alias("analyst_target_price"),
            F.col("c.beta").alias("beta"),
            F.col("c.week_52_high").alias("week_52_high"),
            F.col("c.week_52_low").alias("week_52_low"),
            F.col("c.moving_avg_50_day").alias("moving_avg_50_day"),
            F.col("c.moving_avg_200_day").alias("moving_avg_200_day")
        )
    )