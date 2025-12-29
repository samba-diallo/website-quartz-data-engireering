---
title: Lab 1 – Data Engineering
---

# Lab 1 – Data Engineering




## Notebook : assignment1_esiee

# ESIEE Paris — Data Engineering I — Assignment 1
> Author : DIALLO Samba & DIOP Mouhamed

**Academic year:** 2025–2026  
**Program:** Data & Applications - Engineering - (FD)   
**Course:** Data Engineering I  

---

In this assignment, you'll make sure that you've correctly set up your local Spark environment.
You'll then complete a classic "Word Count" task on the `description` column of the `a1-brand.csv` file.

You can think of "Word Count" as the "Hello World!" of Hadoop, Spark, etc.
The task is simple: We want to count the total number of times each word occurs (in a potentially large collection of text).
Typically, we want to sort by the counts in descending order so we can examine the most frequently occurring words.

## Learning goals
- Confirm local Spark environment in JupyterLab.
- Implement word-count using **RDD** and **DataFrame** APIs.
- Produce top-10 tokens with and without stopwords.
- Record brief performance notes and environment details.

## 1. Setup

The following code snippet should "just work" to initialize Spark.
If it doesn't, consult the **helper and Lab 0 with installation and setup guide**.

```python
#import findspark, os
#os.environ["SPARK_HOME"] = "/path/to/spark-4.0.0-bin-hadoop3"
#findspark.init()
```

```python
import os
import sys
from pyspark.sql import SparkSession
import pyspark
```

```python
# Configurer JAVA_HOME
os.environ['JAVA_HOME'] = '/home/sable/miniconda3/envs/de1-env'

# Configurer SPARK_HOME correctement
os.environ['SPARK_HOME'] = '/home/sable/miniconda3/envs/de1-env/lib/python3.10/site-packages/pyspark'

# Vérifier les configurations
print(f"JAVA_HOME: {os.environ['JAVA_HOME']}")
print(f"SPARK_HOME: {os.environ['SPARK_HOME']}")
```

	JAVA_HOME: /home/sable/miniconda3/envs/de1-env
	SPARK_HOME: /home/sable/miniconda3/envs/de1-env/lib/python3.10/site-packages/pyspark

---


## Notebook : assignment1_esiee

<iframe src="./assets/assignment1_esiee.html" width="100%" height="900"></iframe>

## Notebook : DE1_Lab1_Notebook_EN

<iframe src="./assets/DE1_Lab1_Notebook_EN.html" width="100%" height="900"></iframe>
## 📊 Proof / Outputs
