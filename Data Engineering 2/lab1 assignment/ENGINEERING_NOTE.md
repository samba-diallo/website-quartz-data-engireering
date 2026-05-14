# DE2 Lab 1: Streaming Pipeline - GitHub Archive Track B

## Objective
Implement and optimize a Spark streaming pipeline on GitHub Archive (Track B) with window aggregation, watermark management, and Parquet persistence with baseline vs optimized comparison.

## Architecture
**Baseline**: No repartitioning, Parquet sink baseline_sink
**Optimized**: Repartition by event_type + repo_name (4 partitions) before aggregation

## Data: GitHub Archive (real public events)
- Window: 1 hour | Watermark: 15 minutes
- Aggregations: count(*), countDistinct(actor_login), sum(public events)
- Outputs: plan_baseline.txt, plan_optimized.txt, lab1_metrics_log.csv
