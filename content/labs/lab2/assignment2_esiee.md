# Assignment 2: Data Engineering with PySpark
> Students : DIALLO Samba & DIOP Mouhamed
---

## Overview
This assignment focuses on building a data engineering pipeline using PySpark to process and analyze e-commerce operational data from SQLite.

## Objectives
- Set up PySpark environment
- Load and explore data from SQLite database
- Perform data transformations
- Analyze sales and customer behavior patterns
- Export processed data

## Part 1: Environment Setup

```python
# Install required packages
!pip install pyspark pandas numpy matplotlib seaborn
```

*We install all necessary packages for data processing (PySpark, pandas), numerical computing (numpy), and visualization (matplotlib, seaborn).*

```python
# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("Libraries imported successfully")
```

*Import all required libraries for distributed computing (PySpark), data manipulation (pandas), and visualization (matplotlib/seaborn).*

```python
# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Assignment2_DataEngineering") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("Spark session created successfully")
print(f"Spark version: {spark.version}")
```

*Initialize SparkSession with 4GB driver memory for processing the e-commerce dataset. This is the entry point for all Spark operations.*

## Part 2: Data Loading and Exploration

```python
# Create SQLite database from SQL dump
import sqlite3
import os

# Path to SQL file
sql_file = "/home/sable/Badr TAJINI/lab2-practice/lab2_operational_dump.sql"
db_file = "/home/sable/Badr TAJINI/lab2-practice/operational.db"

# Remove old database if exists
if os.path.exists(db_file):
    os.remove(db_file)

# Create database and load data
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Read and execute SQL file
with open(sql_file, 'r') as f:
    sql_script = f.read()
    cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Database created and data loaded successfully")
```

*Create SQLite database from the SQL dump file. This approach ensures clean data loading by recreating the database from scratch.*

```python
# Load data from SQLite database using pandas then convert to Spark
print("Loading data from database...")

# Connect to SQLite
db_path = "/home/sable/Badr TAJINI/lab2-practice/operational.db"
conn_read = sqlite3.connect(db_path)

# Load tables into pandas DataFrames first
customers_pd = pd.read_sql_query("SELECT * FROM customers", conn_read)
orders_pd = pd.read_sql_query("SELECT * FROM orders", conn_read)
order_items_pd = pd.read_sql_query("SELECT * FROM order_items", conn_read)
products_pd = pd.read_sql_query("SELECT * FROM products", conn_read)
brands_pd = pd.read_sql_query("SELECT * FROM brands", conn_read)
categories_pd = pd.read_sql_query("SELECT * FROM categories", conn_read)

conn_read.close()

# Convert pandas DataFrames to Spark DataFrames
customers_df = spark.createDataFrame(customers_pd)
orders_df = spark.createDataFrame(orders_pd)
order_items_df = spark.createDataFrame(order_items_pd)
products_df = spark.createDataFrame(products_pd)
brands_df = spark.createDataFrame(brands_pd)
categories_df = spark.createDataFrame(categories_pd)

print("Data loaded successfully")
print(f"Customers: {customers_df.count()}")
print(f"Orders: {orders_df.count()}")
print(f"Order items: {order_items_df.count()}")
```

*Load data from SQLite using pandas as an intermediary (since direct JDBC requires additional drivers). This approach efficiently loads all 6 tables: customers (24), orders (220), order_items (638), products (60), brands (8), and categories (9).*

```python
# Display sample data from each table
print("Sample customers:")
customers_df.show(5)

print("\nSample orders:")
orders_df.show(5)

print("\nSample products:")
products_df.show(5)
```

*Inspect sample records from each table to understand data structure and content.*

```python
# Display schemas
print("Customers schema:")
customers_df.printSchema()

print("\nOrders schema:")
orders_df.printSchema()

print("\nProducts schema:")
products_df.printSchema()
```

*Print schemas to understand data types and column structures for each table.*

```python
# Basic statistics
print("Customers statistics:")
customers_df.describe().show()

print("\nOrders statistics:")
orders_df.describe().show()
```

*Generate basic statistical summaries (count, mean, stddev, min, max) for numerical columns to understand data distribution.*

## Part 3: Data Quality Checks

```python
# Check for null values in each table
print("Checking for null values in customers:")
customers_df.select([count(when(col(c).isNull(), c)).alias(c) for c in customers_df.columns]).show()

print("\nChecking for null values in orders:")
orders_df.select([count(when(col(c).isNull(), c)).alias(c) for c in orders_df.columns]).show()

print("\nChecking for null values in products:")
products_df.select([count(when(col(c).isNull(), c)).alias(c) for c in products_df.columns]).show()
```

*Perform data quality checks by counting null values in each column. This ensures data completeness before analysis.*

```python
# Check for duplicate records
print("Checking for duplicates in customers...")
total = customers_df.count()
distinct = customers_df.distinct().count()
print(f"Customers - Total: {total}, Distinct: {distinct}, Duplicates: {total - distinct}")

print("\nChecking for duplicates in orders...")
total = orders_df.count()
distinct = orders_df.distinct().count()
print(f"Orders - Total: {total}, Distinct: {distinct}, Duplicates: {total - distinct}")
```

*Identify duplicate records by comparing total count vs distinct count. No duplicates found in our dataset.*

## Part 4: Data Transformations

```python
# Create a complete sales dataset by joining tables
print("Creating complete sales dataset...")
sales_df = order_items_df \
    .join(orders_df, "order_id") \
    .join(customers_df, "customer_id") \
    .join(products_df, "product_id") \
    .join(brands_df, "brand_id") \
    .join(categories_df, "category_id")

print("Sales dataset created")
print(f"Total sales records: {sales_df.count()}")
sales_df.show(5)
```

*Create a denormalized sales dataset by joining all 6 tables. This creates a complete view with 638 sales records containing all relevant customer, product, brand, and category information.*

```python
# Add calculated columns
print("Adding calculated columns...")
sales_df = sales_df.withColumn("total_price", col("quantity") * col("unit_price")) \
    .withColumn("order_month", month(col("order_date"))) \
    .withColumn("order_year", year(col("order_date")))

print("Calculated columns added")
sales_df.select("order_id", "product_name", "quantity", "unit_price", "total_price").show(5)
```

*Add derived columns for analysis: total_price (line item total), order_month, and order_year for temporal analysis.*

## Part 5: Data Analysis

```python
# Customer analysis
print("Analyzing customer behavior...")
customer_stats = sales_df.groupBy("customer_id", "name").agg(
    count("order_id").alias("total_orders"),
    sum("total_price").alias("total_spent"),
    avg("total_price").alias("avg_order_value"),
    count_distinct("product_id").alias("unique_products")
).orderBy(col("total_spent").desc())

print("Top 10 customers by spending:")
customer_stats.show(10)
```

*Analyze customer purchasing behavior by aggregating total orders, spending, average order value, and product variety. Sorted by total spending to identify top customers.*

```python
# Product analysis
print("Analyzing product performance...")
product_stats = sales_df.groupBy("product_id", "product_name").agg(
    sum("quantity").alias("total_quantity_sold"),
    sum("total_price").alias("total_revenue"),
    count("order_id").alias("number_of_orders")
).orderBy(col("total_revenue").desc())

print("Top products by revenue:")
product_stats.show(10)
```

*Identify top-performing products by analyzing quantity sold, revenue generated, and order frequency.*

```python
# Brand analysis
print("Analyzing brand performance...")
brand_stats = sales_df.groupBy("brand_id", "brand_name").agg(
    sum("total_price").alias("total_revenue"),
    count("order_id").alias("number_of_orders"),
    count_distinct("customer_id").alias("unique_customers")
).orderBy(col("total_revenue").desc())

print("Brand statistics:")
brand_stats.show()
```

*Evaluate brand performance across revenue, order volume, and customer reach to understand brand popularity.*

```python
# Category analysis
print("Analyzing category performance...")
category_stats = sales_df.groupBy("category_id", "category_name").agg(
    sum("total_price").alias("total_revenue"),
    count("order_id").alias("number_of_orders"),
    avg("total_price").alias("avg_order_value")
).orderBy(col("total_revenue").desc())

print("Category statistics:")
category_stats.show()
```

*Analyze product categories to identify which categories drive the most revenue and have the highest average order values.*

```python
# Monthly sales trend
print("Analyzing monthly sales trend...")
monthly_stats = sales_df.groupBy("order_year", "order_month").agg(
    sum("total_price").alias("total_revenue"),
    count("order_id").alias("number_of_orders")
).orderBy("order_year", "order_month")

print("Monthly sales:")
monthly_stats.show()
```

*Track sales trends over time by aggregating monthly revenue and order counts to identify seasonality patterns.*

## Part 6: Advanced Analytics

```python
# Customer segmentation by spending
print("Customer segmentation by spending...")
customer_segments = customer_stats.withColumn(
    "segment",
    when(col("total_spent") >= 1000, "High Value")
    .when((col("total_spent") >= 500) & (col("total_spent") < 1000), "Medium Value")
    .otherwise("Low Value")
)

print("Customer segments:")
customer_segments.groupBy("segment").count().orderBy("segment").show()
```

*Segment customers into High/Medium/Low value groups based on total spending thresholds. This helps identify customer tiers for targeted marketing.*

```python
# Average basket size per customer
print("Calculating average basket size...")
basket_analysis = sales_df.groupBy("order_id").agg(
    sum("quantity").alias("items_per_order"),
    sum("total_price").alias("order_value")
)

basket_stats = basket_analysis.agg(
    avg("items_per_order").alias("avg_items_per_order"),
    avg("order_value").alias("avg_order_value")
).collect()[0]

print(f"Average items per order: {basket_stats['avg_items_per_order']:.2f}")
print(f"Average order value: ${basket_stats['avg_order_value']:.2f}")
```

*Calculate basket metrics to understand typical purchase size and order value, useful for cross-selling strategies.*

## Part 7: Data Visualization

```python
# Convert to Pandas for visualization
print("Preparing data for visualization...")
monthly_pd = monthly_stats.toPandas()
product_pd = product_stats.limit(10).toPandas()
category_pd = category_stats.toPandas()

print("Data converted to Pandas")
```

*Convert Spark DataFrames to pandas for compatibility with matplotlib/seaborn visualization libraries.*

```python
# Monthly revenue trend
plt.figure(figsize=(12, 6))
monthly_pd['month_label'] = monthly_pd['order_year'].astype(str) + '-' + monthly_pd['order_month'].astype(str).str.zfill(2)
plt.plot(range(len(monthly_pd)), monthly_pd['total_revenue'], marker='o', linewidth=2)
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.grid(True, alpha=0.3)
plt.xticks(range(len(monthly_pd)), monthly_pd['month_label'], rotation=45)
plt.tight_layout()
plt.show()

print("Monthly revenue plot created")
```

*Visualize monthly revenue trends over time to identify growth patterns and seasonal variations.*

```python
# Top products by revenue
plt.figure(figsize=(12, 6))
plt.barh(product_pd['product_name'], product_pd['total_revenue'])
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Product')
plt.tight_layout()
plt.show()

print("Product revenue plot created")
```

*Create horizontal bar chart showing top 10 products by revenue for easy comparison.*

```python
# Category revenue distribution
plt.figure(figsize=(10, 10))
plt.pie(category_pd['total_revenue'], labels=category_pd['category_name'], autopct='%1.1f%%', startangle=90)
plt.title('Category Revenue Distribution')
plt.axis('equal')
plt.tight_layout()
plt.show()

print("Category distribution plot created")
```

*Pie chart showing revenue distribution across categories to visualize market share of each category.*

## Part 8: Data Export

```python
# Export processed data
print("Exporting processed data...")

# Export customer statistics
customer_stats.write.mode("overwrite").parquet("output/customer_statistics")
print("Customer statistics exported")

# Export product statistics
product_stats.write.mode("overwrite").csv("output/product_statistics", header=True)
print("Product statistics exported")

# Export sales data
sales_df.write.mode("overwrite").parquet("output/sales_data")
print("Sales data exported")
```

*Export processed analytics to parquet (efficient columnar format) and CSV (human-readable) for downstream use.*

## Part 9: Summary and Conclusions

```python
# Generate summary report
print("=" * 50)
print("ASSIGNMENT 2 SUMMARY REPORT")
print("=" * 50)

total_customers = customers_df.count()
total_orders = orders_df.count()
total_revenue = sales_df.agg(sum("total_price")).collect()[0][0]

print(f"\nData Overview:")
print(f"Total Customers: {total_customers}")
print(f"Total Orders: {total_orders}")
print(f"Total Revenue: ${total_revenue:.2f}")

print(f"\nKey Metrics:")
print(f"Average orders per customer: {total_orders / total_customers:.2f}")
print(f"Average revenue per order: ${total_revenue / total_orders:.2f}")

top_customer = customer_stats.first()
print(f"\nTop customer: {top_customer['name']} (${top_customer['total_spent']:.2f})")

top_product = product_stats.first()
print(f"Top product: {top_product['product_name']} (${top_product['total_revenue']:.2f})")

print("\nProcessing completed successfully!")
print("=" * 50)
```

*Generate comprehensive summary report with key business metrics: total customers, orders, revenue, averages, and top performers.*

```python
# Stop Spark session
spark.stop()
print("Spark session stopped")
```

*Properly shut down Spark session to release resources.*
