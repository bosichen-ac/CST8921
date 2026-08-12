# CST8921 Lab 13: ETL vs ELT with PySpark

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 13 - ETL vs ELT with PySpark

---

## Introduction

The purpose of this lab was to implement and compare ETL and ELT data pipelines using PySpark. 

Both pipelines processed the same e-commerce order dataset, which contained data quality issues such as inconsistent capitalization, a null amount, and a cancelled order.

The ETL pipeline transformed the data before writing it to storage. In comparison, the ELT pipeline first preserved the raw data in storage and then performed transformations using Spark SQL. The lab demonstrated that the two approaches can produce the same final result while using different data-processing architectures.

## Execution results

### Raw data

![raw data](/Lab13/screenshots/0.png)

### ELT

![ELT 1](/Lab13/screenshots/1-1.png)
![ELT 2](/Lab13/screenshots/1-2.png)

### ETL

![ETL-1](/Lab13/screenshots/2-1.png)
![ETL-2](/Lab13/screenshots/2-2.png)

---

## Assessment & Discussion Questions

### Question 1: Architecture & Approach

**Both pipelines produced the same final output. What is the key architectural difference between them? (Hint: timing of transformation in the workflow.)**

In the ETL pattern, the workflow follows an "extract-transform-load" pipeline. The data is first extracted from raw data, then cleaned and transformed, and finally loaded as output files. While in the ELT pattern, the workflow follows an "extract-load-transform" pipeline. At first the data is loaded from raw data, then the raw data is loaded as output files, and then the data is cleaned and transformed, with another tramform to summary mart table at the end.

### Question 2: Data Preservation in ELT

**The ELT pipeline preserved the raw data in orders_raw. Why is this valuable when business requirements change?**

Changing business requirements means changing the data processing logic. By keeping the raw data loaded first, no matter how the data processing workflows will change in the future, the raw data is always usable for processing.

### Question 3: Flexibility & Secondary Analytics

**The ELT pipeline built a category_summary mart as a second SQL step without touching the ETL workflow. How does this demonstrate ELT's flexibility?**

In ELT, the loaded raw data can be reused for different types of processing. This allows new transformations and analytics to be added without changing the original data-loading process.

### Question 4: Scalability on Large Data

**If this dataset were 100 GB on a distributed Spark cluster, which approach would likely perform better and why? Consider network bandwidth, compute costs, and the ability to parallelize work.**

ELT.

Since ELT will load the raw data befor processing, the loaded raw data thus can be stored in the target system without requiring all transformations to be completed before loading. Then the parallel processing among different workloads can be introduced, they can all use the loaded raw data instead of waiting for the first transformation result of raw data.

### Question 5: Real-World Trade-offs

**Identify one real-world scenario where you would still prefer ETL over ELT. What constraints or requirements would drive that choice?**

Processing sensitive or regulated data.

When sensitive or regulated data must be cleaned or validated before it is stored in the target system, it's better to have only processed data saved. With ETL, the sensitive data can be validated, cleaned, or removed during the transformation stage before it is loaded into the target storage. In this situation, data quality, security, and regulatory requirements make ETL more appropriate than storing the complete raw data first.

## Conclusion

This lab demonstrated that ETL and ELT can produce equivalent transformed results while following different architectures. ETL applies quality and transformation rules before loading, which is useful when clean and compliant data must be guaranteed at the storage boundary. ELT preserves raw data first and performs transformations afterward, making it well suited to flexible analytics and modern cloud platforms with scalable storage and compute.