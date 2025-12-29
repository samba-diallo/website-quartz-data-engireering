---
title: Final Project – Data Engineering 1
---

# Final Project – Data Engineering 1


## Notebook : DE1_Project_Notebook_EN
<!-- Inclusion directe du notebook HTML complet -->
<article>
<h1 id="de1--final-project-notebook">DE1 — Final Project Notebook<a role="anchor" aria-hidden="true" tabindex="-1" data-no-popover="true" href="#de1--final-project-notebook" class="internal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a></h1>
<blockquote>
<p>Professor : Badr TAJINI - Data Engineering I - ESIEE 2025-2026</p>
</blockquote>
<hr/>
<blockquote>
<p>Students : DIALLO Samba & DIOP Mouhamed</p>
</blockquote>
<hr/>
<p>This is the primary executable artifact. Fill config, run baseline, then optimized pipeline, and record evidence.</p>
<h2 id="0-load-config">0. Load config<a role="anchor" aria-hidden="true" tabindex="-1" data-no-popover="true" href="#0-load-config" class="internal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a></h2>
<figure data-rehype-pretty-code-figure><pre tabindex="0" data-language="python" data-theme="github-light github-dark"><code data-language="python" data-theme="github-light github-dark" style="display:grid;"><span data-line><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">import</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> yaml, pathlib, datetime</span></span>
<span data-line><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">from</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> pyspark.sql </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">import</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> SparkSession, functions </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">as</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> F, types </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">as</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> T</span></span>
<span data-line> </span>
<span data-line><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">with</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;"> open</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"de1_project_config.yml"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">) </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">as</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> f:</span></span>
<span data-line><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">    CFG</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;"> =</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> yaml.safe_load(f)</span></span>
<span data-line> </span>
<span data-line><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">spark </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> (SparkSession.builder</span></span>
<span data-line><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    .appName(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"de1-lakehouse-project"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    .config(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"spark.sql.adaptive.enabled"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"true"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    .config(</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"spark.sql.adaptive.coalescePartitions.enabled"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">, </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">"true"</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">    .config("spark.driver.memory", "4g")</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">    .config("spark.executor.memory", "4g")</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">    .config("spark.memory.fraction", "0.6")</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">    .config("spark.memory.storageFraction", "0.3")</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">)</span></span>
<span data-line><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    .getOrCreate())</span></span>
<span data-line> </span>
<span data-line><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">print(f"Spark version: {spark.version}")</span></span>
<span data-line><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">print(f"Project: {CFG['project']['name']}")</span></span>
<span data-line><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">CFG</span></span></code></pre></figure>
<pre><code>WARNING: Using incubator modules: jdk.incubator.vector
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
25/12/20 20:51:51 WARN Utils: Your hostname, sable-ThinkPad-X1-Yoga-3rd, resolves to a loopback address: 127.0.1.1; using 10.192.33.105 instead (on interface wlp2s0)
25/12/20 20:51:51 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
25/12/20 20:51:51 WARN Utils: Your hostname, sable-ThinkPad-X1-Yoga-3rd, resolves to a loopback address: 127.0.1.1; using 10.192.33.105 instead (on interface wlp2s0)
25/12/20 20:51:51 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Using Spark's default log4j profile: org/apache/spark/log4j2-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
25/12/20 20:51:52 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
25/12/20 20:51:52 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


Spark version: 4.0.1
Project: DE1 Local Lakehouse Project





{'project': {'name': 'DE1 Local Lakehouse Project',
  'dataset': 'Wikipedia Clickstream (Nov 2024)',
  'dataset_size': '10M rows / 450MB',
  'team': 'Badr TAJINI'},
 'paths': {'raw_csv_glob': 'data/clickstream/clickstream-10M.tsv',
  'bronze': 'outputs/project/bronze',
  'silver': 'outputs/project/silver',
  'gold': 'outputs/project/gold',
  'proof': 'proof',
  'metrics_log': 'project_metrics_log.csv'},
 'slo': {'freshness_hours': 2,
  'q1_latency_p95_seconds': 4,
  'storage_ratio_max': 0.6},
 'hardware': {'cpu': 'Intel Core i7',
  'ram_gb': 16,
  'disk_type': 'SSD',
  'spark_version': '4.0.0'},
 'layout': {'partition_by': [],
  'sort_by': [],
  'target_file_size_mb': 128,
  'max_files_per_partition': 10},
 'queries': {'q1': {'description': 'Top 20 most visited pages',
   'sql': 'SELECT curr as page, \n       SUM(n) as total_clicks\nFROM silver\nGROUP BY curr\nORDER BY total_clicks DESC\nLIMIT 20\n'},
  'q2': {'description': 'Top 20 referrer pages',
   'sql': "SELECT prev as referrer, \n       SUM(n) as total_clicks\nFROM silver\nWHERE prev != 'other-empty'\nGROUP BY prev\nORDER BY total_clicks DESC\nLIMIT 20\n"},
  'q3': {'description': 'Click patterns by type (external/internal/link)',
   'sql': 'SELECT type,\n       COUNT(DISTINCT curr) as unique_pages,\n       SUM(n) as total_clicks,\n       AVG(n) as avg_clicks_per_pair\nFROM silver\nGROUP BY type\nORDER BY total_clicks DESC\n'}},
 'silver_schema': {'columns': [{'name': 'prev',
    'type': 'StringType',
    'nullable': False},
   {'name': 'curr', 'type': 'StringType', 'nullable': False},
   {'name': 'type', 'type': 'StringType', 'nullable': False},
   {'name': 'n', 'type': 'IntegerType', 'nullable': False}]},
 'data_quality': {'rules': [{'name': 'Non-null clicks',
    'check': 'n IS NOT NULL',
    'severity': 'error'},
   {'name': 'Positive clicks', 'check': 'n >= 0', 'severity': 'error'},
   {'name': 'Valid page names',
    'check': 'LENGTH(curr) > 0',
    'severity': 'error'},
   {'name': 'Valid type',
    'check': "type IN ('link', 'external', 'other')",
    'severity': 'warning'}]},
 'optimization': {'baseline': ['No partitioning',
   'No sorting',
   'Default file sizes',
   'Full table scans'],
  'optimized': ['Repartition by computed hash',
   'Sort by clicks (n) descending',
   'Target 128MB file size',
   'Enable AQE',
   'Coalesce small files']}}
</code></pre>
<h2 id="1-bronze--landing-raw-data">1. Bronze — landing raw data<a role="anchor" aria-hidden="true" tabindex="-1" data-no-popover="true" href="#1-bronze--landing-raw-data" class="internal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></a></h2>
<!-- ...le reste du contenu HTML du notebook peut être inséré ici ... -->
</article>
<!-- FIN INCLUSION NOTEBOOK HTML -->

### Images
- ![metrics_13.png](project/assets/metrics_13.png)
- ![metrics_15.png](project/assets/metrics_15.png)
- ![metrics7.png](project/assets/metrics7.png)
- ![metrics_8.png](project/assets/metrics_8.png)
- ![metrics_9.png](project/assets/metrics_9.png)
- ![Sparkjob.png](project/assets/Sparkjob.png)

### Text files
- [baseline_q1_plan.txt](project/assets/baseline_q1_plan.txt)
- [baseline_q2_plan.txt](project/assets/baseline_q2_plan.txt)
- [baseline_q3_plan.txt](project/assets/baseline_q3_plan.txt)
- [DE1_Project_Report.md](project/assets/DE1_Project_Report.md)
- [optimized_q1_plan.txt](project/assets/optimized_q1_plan.txt)
- [optimized_q2_plan.txt](project/assets/optimized_q2_plan.txt)
- [optimized_q3_plan.txt](project/assets/optimized_q3_plan.txt)
- [project_final_genai.md](project/assets/project_final_genai.md)
