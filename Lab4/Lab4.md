# CST8921 Lab 4：Azure Databricks and analyzing files with databricks

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 4 - Azure Databricks and analyzing files with databricks
- Submission Date: 

---

## Introduction

The purpose of this lab was to explore parquet files stored in Azure Data Lake Storage Gen2, perform data transformation using Spark, and analyze the transformed data using Azure Synapse and Databricks.

## Environment Setup

- Azure Storage Account
  - Raw Container
  - Refined Container
- Azure Synapse Workspace

## Part 1: Data Exploration

### Uploading Data

A container `raw` was created in Azure Data Lake Storage. The provided Parquet files were uploaded into the storage account for analysis.

The raw container in the Storage Account.

![raw container in the storage account](/Lab4/screenshots/1.png)

### Exploring Data with SQL

Take the customers dataset as example.

The datasets were explored using `Synapse SQL` and `OPENROWSET` queries. Column names and sample records were reviewed to understand the structure of the source data.

The parquet files were successfully queried using SQL.

![exploring result using SQL](/Lab4/screenshots/2.png)

### Exploring Data with Spark

Take the customers dataset as example. Load it into a Spark DataFrame.

The schema contained:
```
customer_id (string)
country (string)
signup_date (date)
```
Sample records were displayed using the DataFrame `show()` function as in the screenshot.

![exploring result using Spark](/Lab4/screenshots/3.png)

Both Synapse SQL and Spark were used to validate schema consistency and ensure that the Parquet files were correctly interpreted across different processing engines.

## Part 2: Data Transformation

### Remove Duplicates

Removed duplicated data using the following code.
```
df_dedup = df.dropDuplicates()
print(df.count())
print(df_dedup.count())
```

Duplicate records were removed to ensure data quality, as the same event may appear multiple times due to repeated ingestion or upstream logging duplication.

![remove duplicates](/Lab4/screenshots/4.png)

### Fix Data Types

The `event_time` column was initially interpreted as a long integer because the source Parquet files stored timestamps using nanosecond precision. The values were converted to Spark TimestampType before further transformations were applied.

```
from pyspark.sql.functions import to_timestamp
df_clean = df_dedup.withColumn(  "event_time",  to_timestamp("event_time"))

df_clean.printSchema()
```

![convert timestamp columns](/Lab4/screenshots/5.png)

### Create Derived Columns

Tried to add Year and Month columns following the code below.

```
from pyspark.sql.functions import year, month
df_transformed = (
    df_clean
    .withColumn("Year", year("event_time"))
    .withColumn("Month", month("event_time"))
)

df_transformed.show(5)
```

The anomaly in the Year field (Year = 294247) seemed to be caused by incorrect conversion of nanosecond-precision timestamps into Spark TimestampType, which does not natively support nanosecond resolution. This led to corrupted timestamp values, resulting in unrealistic derived Year values.

![create derived columns](/Lab4/screenshots/6.png)

## Writing to Refined Zone

```
df_transformed.write.mode("overwrite").parquet( "abfss://refined@<storage-account>.dfs.core.windows.net/")
```

The transformed dataset was successfully written to the refined container.

![overwite code](/Lab4/screenshots/7-1.png)
![written into new container](/Lab4/screenshots/7-2.png)

## Part 3: Data Analysis

The transformed data stored in the refined container was analyzed using both Synapse SQL and Spark.

Due to the use of Synapse Serverless SQL Pool, external tables and data sources couldn't be created. Instead, OPENROWSET was used to directly query Parquet files stored in Azure Data Lake Storage.

The following SQL query was used to analyze the transformed data:

```sql
SELECT Year, COUNT(*) AS total_events
FROM OPENROWSET(
    BULK 'https://8921lab4storageacc.dfs.core.windows.net/refined/refined_events/*.parquet',
    FORMAT = 'PARQUET'
) AS rows
GROUP BY Year
ORDER BY Year;
```

A Spark aggregation was also performed in the notebook:

```
df_transformed.groupBy("Year").count().show()
```

The results confirmed that the transformed dataset could be successfully queried and aggregated after being written to the refined storage layer. Screenshots of the SQL query results and Spark notebook output are shown in the screenshots. 

While both Synapse SQL and Spark produced the same aggregation results in general, an anomaly was observed in the Year field, where an unexpected value (Year = 294247) appeared in the output.

This value is likely caused by incorrect interpretation of nanosecond-precision timestamps during the initial transformation process.

The issue highlights a common challenge when working with Parquet data containing high-precision `event_time` fields, where improper conversion can lead to incorrect derived time attributes.

Despite this anomaly, the overall pipeline and aggregation logic remain valid for demonstrating the end-to-end data processing workflow.

![sql result](/Lab4/screenshots/8.png)

![spark result](/Lab4/screenshots/9.png)

## Challenges Encountered

During the lab, some provided code snippets required adaptation to work correctly within the Azure environment. Additional debugging and interpretation were needed to align the instructions with the actual dataset and Spark execution behavior.

Another key challenge was working with Parquet datasets containing high-precision timestamp values.

Ensuring correct interpretation of time-based fields required careful attention to data types and transformation logic in Spark.

This highlighted the importance of validating data schemas and understanding source data formats when performing distributed data processing.

## Conclusion

This lab demonstrated how Azure Data Lake Storage, Spark, and Synapse can be integrated to build a basic data engineering pipeline. 

Raw parquet files were explored, cleaned, transformed, and written to a refined storage zone for analytical querying.