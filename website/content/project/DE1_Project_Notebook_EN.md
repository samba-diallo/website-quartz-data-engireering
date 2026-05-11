# DE1 — Final Project Notebook

> Professor : Badr TAJINI - Data Engineering I - ESIEE 2025-2026

---

> Students : DIALLO Samba & DIOP Mouhamed

---

This is the primary executable artifact. Fill config, run baseline, then optimized pipeline, and record evidence.

## 0. Load config

```python
import yaml, pathlib, datetime
from pyspark.sql import SparkSession, functions as F, types as T

with open("de1_project_config.yml") as f:
    CFG = yaml.safe_load(f)

spark = (SparkSession.builder
    .appName("de1-lakehouse-project")
    .config("spark.sql.adaptive.enabled", "true")
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.memory.fraction", "0.6")
    .config("spark.memory.storageFraction", "0.3")
    .getOrCreate())

print(f"Spark version: {spark.version}")
print(f"Project: {CFG['project']['name']}")
CFG
```

**Output:**
```
Spark version: 4.0.1
Project: DE1 Local Lakehouse Project

Configuration loaded with:
- Dataset: Wikipedia Clickstream (Nov 2024)
- Dataset size: 10M rows / 450MB
- Hardware: Intel Core i7, 16GB RAM, SSD
```

## 1. Bronze — landing raw data

```python
raw_glob = CFG["paths"]["raw_csv_glob"]
bronze = CFG["paths"]["bronze"]
proof = CFG["paths"]["proof"]

df_raw = (spark.read
    .option("header", "false")
    .option("inferSchema", "false")
    .option("delimiter", "\t")
    .csv(raw_glob)
    .toDF("prev", "curr", "type", "n"))

row_count = df_raw.count()
df_raw.write.mode("overwrite").csv(bronze)
print(f"Bronze written: {bronze}, rows: {row_count:,}")
```

**Output:**
```
Bronze written: outputs/project/bronze, rows: 10,000,000
```

## 2. Silver — cleaning and typing

```python
silver = CFG["paths"]["silver"]

df_silver = (df_raw
    .withColumn("n", F.col("n").cast("integer"))
    .filter(F.col("n").isNotNull())
    .filter(F.col("n") >= 0)
    .filter(F.length(F.col("curr")) > 0)
    .dropDuplicates())

silver_count = df_silver.count()
df_silver.write.mode("overwrite").parquet(silver)
print(f"Silver written: {silver}, rows: {silver_count:,}")
```

**Output:**
```
Silver written: outputs/project/silver, rows: 10,000,000
```

## 3. Gold — analytics tables

```python
gold = CFG["paths"]["gold"]
queries = CFG["queries"]

pathlib.Path(gold).mkdir(parents=True, exist_ok=True)
df_silver.createOrReplaceTempView("silver")

df_q1 = spark.sql(queries["q1"]["sql"])
q1_count = df_q1.count()
df_q1.write.mode("overwrite").parquet(f"{gold}/q1_daily_aggregation")
print(f"Q1 written, rows: {q1_count:,}")

df_q2 = spark.sql(queries["q2"]["sql"])
q2_count = df_q2.count()
df_q2.write.mode("overwrite").parquet(f"{gold}/q2_top_referrers")
print(f"Q2 written, rows: {q2_count:,}")

df_q3 = spark.sql(queries["q3"]["sql"])
q3_count = df_q3.count()
df_q3.write.mode("overwrite").parquet(f"{gold}/q3_filtered_analysis")
print(f"Q3 written, rows: {q3_count:,}")

print(f"Gold written: {gold}")
```

**Output:**
```
Q1 written, rows: 20
Q2 written, rows: 20
Q3 written, rows: 3
Gold written: outputs/project/gold
```

## 4. Baseline plans and metrics

```python
pathlib.Path(proof).mkdir(parents=True, exist_ok=True)

df_q1_baseline = spark.sql(queries["q1"]["sql"])
plan_q1 = df_q1_baseline._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/baseline_q1_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(plan_q1)

df_q2_baseline = spark.sql(queries["q2"]["sql"])
plan_q2 = df_q2_baseline._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/baseline_q2_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(plan_q2)

df_q3_baseline = spark.sql(queries["q3"]["sql"])
plan_q3 = df_q3_baseline._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/baseline_q3_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(plan_q3)

print("Saved baseline plans. Record Spark UI metrics now.")
```

**Output:**
```
Saved baseline plans. Record Spark UI metrics now.
```

## 5. Optimization — layout and joins

```python
layout = CFG["layout"]
target_size_mb = layout["target_file_size_mb"]

df_silver_reloaded = spark.read.parquet(silver)
total_bytes = df_silver_reloaded.count() * 100
num_partitions = max(4, int(total_bytes / (target_size_mb * 1024 * 1024)))

df_silver_opt = (df_silver_reloaded
    .repartition(num_partitions)
    .sortWithinPartitions(F.desc("n")))

silver_opt = f"{silver}_optimized"
df_silver_opt.write.mode("overwrite").parquet(silver_opt)
print(f"Optimized silver written: {silver_opt}")

df_silver_opt.createOrReplaceTempView("silver")

df_q1_opt = spark.sql(queries["q1"]["sql"])
plan_q1_opt = df_q1_opt._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/optimized_q1_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(f"Optimizations: {num_partitions} partitions, sorted by n desc\n")
    f.write(plan_q1_opt)

df_q2_opt = spark.sql(queries["q2"]["sql"])
plan_q2_opt = df_q2_opt._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/optimized_q2_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(f"Optimizations: {num_partitions} partitions, sorted by n desc\n")
    f.write(plan_q2_opt)

df_q3_opt = spark.sql(queries["q3"]["sql"])
plan_q3_opt = df_q3_opt._jdf.queryExecution().executedPlan().toString()
with open(f"{proof}/optimized_q3_plan.txt", "w") as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.write(f"Optimizations: {num_partitions} partitions, sorted by n desc\n")
    f.write(plan_q3_opt)

print("Saved optimized plans. Record Spark UI metrics now.")
```

**Output:**
```
Optimized silver written: outputs/project/silver_optimized
Saved optimized plans. Record Spark UI metrics now.
```

## 6. Cleanup

```python
spark.stop()
print("Spark session stopped.")
```

**Output:**
```
Spark session stopped.
```

