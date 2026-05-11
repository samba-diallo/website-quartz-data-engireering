---
title: "lab1 assignment - Preuves"
date: 2026-05-11
tags:
  - proof
  - de2
  - assignment
draft: false
---

# lab1 assignment - Preuves

Captures et plans d'execution generes lors du lab.

## Plans et logs

### plan_baseline.txt

```text
PLAN DE REQUÊTE DE BASE
================================================================================
== Physical Plan ==
* ColumnarToRow (2)
+- Scan parquet  (1)


(1) Scan parquet 
Output [6]: [window_start#77, window_end#78, team_id#79, event_count#80L, total_gold#81, total_kills#82L]
Batched: true
Location: MetadataLogFileIndex [/home/sable/Documents/E4FD/S4/Data Engineering/Data Engineering 2/lab1 assignment/outputs/lab1/stream_sink_baseline]
ReadSchema: struct<window_start:timestamp,window_end:timestamp,team_id:string,event_count:bigint,total_gold:double,total_kills:bigint>

(2) ColumnarToRow [codegen id : 1]
Input [6]: [window_start#77, window_end#78, team_id#79, event_count#80L, total_gold#81, total_kills#82L]



```

### plan_optimized.txt

```text
PLAN DE REQUÊTE OPTIMISÉE (avec repartitionnement)
================================================================================
== Physical Plan ==
* ColumnarToRow (2)
+- Scan parquet  (1)


(1) Scan parquet 
Output [6]: [window_start#310, window_end#311, team_id#312, event_count#313L, total_gold#314, total_kills#315L]
Batched: true
Location: MetadataLogFileIndex [/home/sable/Documents/E4FD/S4/Data Engineering/Data Engineering 2/lab1 assignment/outputs/lab1/stream_sink_optimized]
ReadSchema: struct<window_start:timestamp,window_end:timestamp,team_id:string,event_count:bigint,total_gold:double,total_kills:bigint>

(2) ColumnarToRow [codegen id : 1]
Input [6]: [window_start#310, window_end#311, team_id#312, event_count#313L, total_gold#314, total_kills#315L]



```

