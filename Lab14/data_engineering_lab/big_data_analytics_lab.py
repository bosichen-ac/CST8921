import os

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, StringType, DoubleType
)

# ── Cross-platform output paths ──────────────────────────────
BASE_DIR       = os.path.join(os.getcwd(), "output")
PARTITIONED    = os.path.join(BASE_DIR, "transactions_by_region")
NONPARTITIONED = os.path.join(BASE_DIR, "transactions_non_partitioned")
SEGMENTS_PATH  = os.path.join(BASE_DIR, "customer_segments")
ANOMALIES_PATH = os.path.join(BASE_DIR, "anomaly_results")

# ── Spark Session ────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("Big_Data_Analytics_Lab") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
print("Spark session started successfully.")
print(f"Spark version: {spark.version}")


# ============================================================
# SETUP
# ============================================================
transactions = [
    (1,  "T001", "Alice",   "North", "Electronics", 899.99, 2, "2024-01-05 10:30:00", "credit_card"),
    (2,  "T002", "Bob",     "South", "Clothing",     45.00, 3, "2024-01-06 11:00:00", "cash"),
    (3,  "T003", "Charlie", "East",  "Electronics", 199.50, 1, "2024-01-06 14:20:00", "debit_card"),
    (4,  "T004", "Alice",   "North", "Food",          12.50, 5, "2024-01-07 09:15:00", "cash"),
    (5,  "T005", "David",   "West",  "Electronics", 450.00, 1, "2024-01-08 16:45:00", "credit_card"),
    (6,  "T006", "Eve",     "South", "Food",          22.00, 4, "2024-01-08 18:00:00", "credit_card"),
    (7,  "T007", "Frank",   "North", "Clothing",      75.00, 2, "2024-01-09 13:30:00", "debit_card"),
    (8,  "T008", "Grace",   "East",  "Food",          33.00, 3, "2024-01-10 10:00:00", "cash"),
    (9,  "T009", "Heidi",   "West",  "Electronics", 600.00, 1, "2024-02-01 12:00:00", "credit_card"),
    (10, "T010", "Ivan",    "South", "Clothing",     110.00, 2, "2024-02-02 15:30:00", "debit_card"),
    (11, "T011", "Alice",   "North", "Electronics", 250.00, 1, "2024-02-03 09:00:00", "credit_card"),
    (12, "T012", "Bob",     "South", "Food",          18.00, 6, "2024-02-04 17:00:00", "cash"),
    (13, "T013", "Charlie", "East",  "Clothing",      95.00, 1, "2024-02-05 11:45:00", "credit_card"),
    (14, "T014", "David",   "West",  "Food",           8.50, 2, "2024-02-06 08:30:00", "debit_card"),
    (15, "T015", "Eve",     "South", "Electronics", 320.00, 1, "2024-02-07 14:00:00", "credit_card"),
    (16, "T016", "Frank",   "North", "Food",          55.00, 3, "2024-03-01 10:15:00", "cash"),
    (17, "T017", "Grace",   "East",  "Electronics", 780.00, 2, "2024-03-02 16:00:00", "credit_card"),
    (18, "T018", "Heidi",   "West",  "Clothing",     200.00, 1, "2024-03-03 12:30:00", "debit_card"),
    (19, "T019", "Ivan",    "South", "Food",          40.00, 5, "2024-03-04 09:45:00", "cash"),
    (20, "T020", "Alice",   "North", "Electronics", 999.99, 1, "2024-03-05 11:00:00", "credit_card"),
]

schema = StructType([
    StructField("id",             IntegerType(), True),
    StructField("transaction_id", StringType(),  True),
    StructField("customer",       StringType(),  True),
    StructField("region",         StringType(),  True),
    StructField("category",       StringType(),  True),
    StructField("unit_price",     DoubleType(),  True),
    StructField("quantity",       IntegerType(), True),
    StructField("timestamp",      StringType(),  True),
    StructField("payment_method", StringType(),  True),
])

raw_df = spark.createDataFrame(transactions, schema)

enriched_df = raw_df \
    .withColumn("revenue", F.round(F.col("unit_price") * F.col("quantity"), 2)) \
    .withColumn("event_time", F.to_timestamp(F.col("timestamp"), "yyyy-MM-dd HH:mm:ss")) \
    .cache()

print("=" * 65)
print("SETUP: SOURCE DATA WITH DERIVED COLUMNS")
print("=" * 65)
print(f"Row count: {enriched_df.count()}")
enriched_df.orderBy("id").show(20, truncate=False)
enriched_df.printSchema()


# ============================================================
# PART 1 — DESCRIPTIVE ANALYTICS
# ============================================================
print("=" * 65)
print("PART 1: DESCRIPTIVE ANALYTICS")
print("=" * 65)

print("\nSummary statistics:")
enriched_df.select("unit_price", "quantity", "revenue").describe().show()

print("Revenue and units sold by category:")
category_summary = enriched_df.groupBy("category").agg(
    F.round(F.sum("revenue"), 2).alias("total_revenue"),
    F.round(F.avg("revenue"), 2).alias("avg_revenue"),
    F.count("*").alias("transaction_count"),
    F.sum("quantity").alias("units_sold")
).orderBy(F.desc("total_revenue"))
category_summary.show()

print("Revenue and units sold by region:")
region_summary = enriched_df.groupBy("region").agg(
    F.round(F.sum("revenue"), 2).alias("total_revenue"),
    F.round(F.avg("revenue"), 2).alias("avg_revenue"),
    F.count("*").alias("transaction_count"),
    F.sum("quantity").alias("units_sold")
).orderBy(F.desc("total_revenue"))
region_summary.show()


# ============================================================
# PART 2 — DIAGNOSTIC ANALYTICS
# ============================================================
print("=" * 65)
print("PART 2: DIAGNOSTIC ANALYTICS — Why did it happen?")
print("=" * 65)

print("\nRegion x Category revenue pivot:")
region_category_pivot = enriched_df.groupBy("region") \
    .pivot("category", ["Electronics", "Clothing", "Food"]) \
    .agg(F.round(F.sum("revenue"), 2)) \
    .orderBy("region")
region_category_pivot.show()

top_region = region_summary.first()["region"]
print(f"Transactions in the top-revenue region ({top_region}):")
enriched_df.filter(F.col("region") == top_region) \
    .select("transaction_id", "customer", "category", "revenue") \
    .orderBy(F.desc("revenue")) \
    .show()

print("Monthly revenue trend:")
monthly_trend = enriched_df \
    .withColumn("month", F.date_format(F.col("event_time"), "yyyy-MM")) \
    .groupBy("month") \
    .agg(F.round(F.sum("revenue"), 2).alias("total_revenue")) \
    .orderBy("month")
monthly_trend.show()

print("Average revenue by payment method:")
enriched_df.groupBy("payment_method").agg(
    F.round(F.avg("revenue"), 2).alias("avg_revenue"),
    F.count("*").alias("transaction_count")
).orderBy(F.desc("avg_revenue")).show()


# ============================================================
# PART 3 — WINDOW FUNCTIONS
# ============================================================
print("=" * 65)
print("PART 3: WINDOW FUNCTIONS — Rankings and running totals")
print("=" * 65)

revenue_window = Window.partitionBy("region").orderBy(F.desc("revenue"))
ranked_df = enriched_df.withColumn("revenue_rank", F.rank().over(revenue_window))

print("\nTop 2 transactions by revenue within each region:")
ranked_df.filter(F.col("revenue_rank") <= 2) \
    .select("region", "revenue_rank", "transaction_id", "customer", "revenue") \
    .orderBy("region", "revenue_rank") \
    .show()

running_window = Window.partitionBy("region") \
    .orderBy("event_time") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

print("Running revenue total within each region:")
running_df = enriched_df.withColumn(
    "running_revenue",
    F.round(F.sum("revenue").over(running_window), 2)
)
running_df.select(
    "region", "event_time", "transaction_id", "revenue", "running_revenue"
).orderBy("region", "event_time").show(20, truncate=False)

quartile_window = Window.orderBy(F.desc("revenue"), "transaction_id")
print("Revenue quartiles (tier 1 = highest):")
enriched_df.withColumn("revenue_tier", F.ntile(4).over(quartile_window)) \
    .select("transaction_id", "customer", "revenue", "revenue_tier") \
    .orderBy("revenue_tier", F.desc("revenue")) \
    .show(20)

previous_window = Window.partitionBy("customer").orderBy("event_time")
print("Previous purchase revenue for each customer:")
enriched_df.withColumn("prev_revenue", F.lag("revenue").over(previous_window)) \
    .select("customer", "event_time", "transaction_id", "revenue", "prev_revenue") \
    .orderBy("customer", "event_time") \
    .show(20, truncate=False)


# ============================================================
# PART 4 — FEATURE ENGINEERING AND RFM
# ============================================================
print("=" * 65)
print("PART 4: FEATURE ENGINEERING — Preparing for prediction")
print("=" * 65)

mean_revenue = enriched_df.agg(F.avg("revenue")).first()[0]

featured_df = enriched_df \
    .withColumn("hour", F.hour("event_time")) \
    .withColumn("day", F.dayofmonth("event_time")) \
    .withColumn("day_of_week", F.dayofweek("event_time")) \
    .withColumn("month", F.month("event_time")) \
    .withColumn("is_weekend", F.when(F.col("day_of_week").isin(1, 7), 1).otherwise(0)) \
    .withColumn("is_high_value", F.when(F.col("revenue") > mean_revenue, 1).otherwise(0)) \
    .withColumn("high_quantity", F.when(F.col("quantity") > 3, 1).otherwise(0)) \
    .cache()

print(f"\nMean revenue used for is_high_value: {mean_revenue:.2f}")
print("Transaction-level engineered features:")
featured_df.select(
    "transaction_id", "customer", "revenue", "hour", "day",
    "day_of_week", "month", "is_weekend", "is_high_value", "high_quantity"
).orderBy("transaction_id").show(20)

reference_date = enriched_df.select(
    F.date_add(F.max("event_time"), 1).alias("reference_date")
).first()["reference_date"]

rfm_df = enriched_df.groupBy("customer").agg(
    F.datediff(F.lit(reference_date), F.max("event_time")).alias("recency_days"),
    F.count("*").alias("frequency"),
    F.round(F.sum("revenue"), 2).alias("monetary")
)

recency_window   = Window.orderBy(F.asc("recency_days"), "customer")
frequency_window = Window.orderBy(F.asc("frequency"), "customer")
monetary_window  = Window.orderBy(F.asc("monetary"), "customer")

rfm_df = rfm_df \
    .withColumn("R", 5 - F.ntile(4).over(recency_window)) \
    .withColumn("F", F.ntile(4).over(frequency_window)) \
    .withColumn("M", F.ntile(4).over(monetary_window)) \
    .withColumn("rfm_sum", F.col("R") + F.col("F") + F.col("M")) \
    .withColumn(
        "rfm_cell",
        F.concat(F.lit("R"), F.col("R"), F.lit("F"), F.col("F"), F.lit("M"), F.col("M"))
    ) \
    .cache()

print(f"RFM reference date: {reference_date}")
print("Customer-level RFM scores:")
rfm_df.orderBy(F.desc("rfm_sum"), "customer").show(truncate=False)


# ============================================================
# PART 5 — CUSTOMER SEGMENTATION
# ============================================================
print("=" * 65)
print("PART 5: CUSTOMER SEGMENTATION — Champions to At Risk")
print("=" * 65)

segmented_df = rfm_df \
    .withColumn("fm", (F.col("F") + F.col("M")) / 2) \
    .withColumn(
        "segment",
        F.when((F.col("R") >= 4) & (F.col("fm") >= 4), "Champions")
         .when(F.col("fm") >= 3, "Loyal")
         .when((F.col("R") >= 3) & (F.col("fm") >= 2), "Potential Loyalist")
         .when(F.col("R") >= 3, "New / Promising")
         .when((F.col("R") <= 2) & (F.col("fm") >= 3), "At Risk")
         .when((F.col("R") <= 2) & (F.col("fm") < 3), "Hibernating / Lost")
         .otherwise("Needs Attention")
    ) \
    .cache()

print("\nCustomer segments:")
segmented_df.orderBy("segment", F.desc("rfm_sum")).show(truncate=False)

print("Segment sizes:")
segmented_df.groupBy("segment").count() \
    .orderBy(F.desc("count"), "segment") \
    .show(truncate=False)


# ============================================================
# PART 6 — ANOMALY DETECTION
# ============================================================
print("=" * 65)
print("PART 6: ANOMALY DETECTION — Finding outliers with z-scores")
print("=" * 65)

THRESHOLD = 2.0

global_stats = enriched_df.agg(
    F.avg("revenue").alias("global_mean"),
    F.stddev_samp("revenue").alias("global_stddev")
)

global_anomaly_df = enriched_df.crossJoin(F.broadcast(global_stats)) \
    .withColumn(
        "global_z",
        (F.col("revenue") - F.col("global_mean")) / F.col("global_stddev")
    ) \
    .withColumn("is_global_anomaly", F.abs(F.col("global_z")) > THRESHOLD)

stats = global_stats.first()
print(
    f"\nGlobal mean: {stats['global_mean']:.2f}; "
    f"sample standard deviation: {stats['global_stddev']:.2f}; "
    f"threshold: {THRESHOLD} sigma"
)
print("Transactions flagged by the global baseline:")
global_anomaly_df.filter(F.col("is_global_anomaly")) \
    .select(
        "transaction_id", "customer", "category", "revenue",
        F.round("global_z", 3).alias("global_z")
    ) \
    .orderBy(F.desc("global_z")) \
    .show()

category_window = Window.partitionBy("category")
anomaly_df = global_anomaly_df \
    .withColumn("category_mean", F.avg("revenue").over(category_window)) \
    .withColumn("category_stddev", F.stddev_samp("revenue").over(category_window)) \
    .withColumn(
        "category_z",
        (F.col("revenue") - F.col("category_mean")) / F.col("category_stddev")
    ) \
    .withColumn("is_category_anomaly", F.abs(F.col("category_z")) > THRESHOLD) \
    .cache()

print("Transactions flagged by the per-category baseline:")
anomaly_df.filter(F.col("is_category_anomaly")) \
    .select(
        "transaction_id", "customer", "category", "revenue",
        F.round("category_z", 3).alias("category_z")
    ) \
    .orderBy("category", F.desc("category_z")) \
    .show()


# ============================================================
# PART 7 — DATA ENGINEERING / PARQUET OUTPUT
# ============================================================
print("=" * 65)
print("PART 7: DATA ENGINEERING — Parquet output for downstream use")
print("=" * 65)

print("\nWriting transaction data partitioned by region...")
featured_df.write \
    .mode("overwrite") \
    .partitionBy("region") \
    .parquet(PARTITIONED)

print("Writing a non-partitioned control copy...")
featured_df.write \
    .mode("overwrite") \
    .parquet(NONPARTITIONED)

segmented_df.write.mode("overwrite").parquet(SEGMENTS_PATH)
anomaly_df.write.mode("overwrite").parquet(ANOMALIES_PATH)

read_back_df = spark.read.parquet(PARTITIONED)
original_count = featured_df.count()
read_back_count = read_back_df.count()

print(f"Partitioned output path: {PARTITIONED}")
print("Partition folders: region=East, region=North, region=South, region=West")
print(f"Original row count : {original_count}")
print(f"Read-back row count: {read_back_count}")

if original_count == read_back_count:
    print("Parquet row counts match.")
else:
    print("Parquet row counts differ — investigate!")

print("\nRead-back schema:")
read_back_df.printSchema()

print("=" * 65)
print("LAB 14 COMPLETE — All required Parts 0-7 finished.")
print("=" * 65)

spark.stop()
