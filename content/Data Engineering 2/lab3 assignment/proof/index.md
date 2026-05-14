---
title: "lab3 assignment - Preuves"
date: 2026-05-14
tags:
  - proof
  - de2
  - assignment
draft: false
---

# lab3 assignment - Preuves

Captures et plans d'execution generes lors du lab.

## Captures d'ecran

### jobSpark

![jobSpark](./jobSpark.png)

### metric1

![metric1](./metric1.png)

## Plans et logs

### plan_after.txt

```text
== Physical Plan ==
InMemoryTableScan (1)
   +- InMemoryRelation (2)
         +- Coalesce (8)
            +- InMemoryTableScan (3)
                  +- InMemoryRelation (4)
                        +- * Project (7)
                           +- * Project (6)
                              +- * Scan ExistingRDD (5)


(1) InMemoryTableScan
Output [2]: [true_cluster#2, features#71]
Arguments: [true_cluster#2, features#71]

(2) InMemoryRelation
Arguments: [true_cluster#2, features#71], StorageLevel(disk, memory, deserialized, 1 replicas)

(3) InMemoryTableScan
Output [2]: [true_cluster#2, features#71]
Arguments: [true_cluster#2, features#71]

(4) InMemoryRelation
Arguments: [true_cluster#2, features#71], StorageLevel(disk, memory, deserialized, 1 replicas)

(5) Scan ExistingRDD [codegen id : 1]
Output [3]: [x#0, y#1, true_cluster#2]
Arguments: [x#0, y#1, true_cluster#2], MapPartitionsRDD[4] at applySchemaToPythonRDD at NativeMethodAccessorImpl.java:0, ExistingRDD, UnknownPartitioning(0)

(6) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(struct(x, x#0, y, y#1)) AS features_raw#18]
Input [3]: [x#0, y#1, true_cluster#2]

(7) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(features_raw#18) AS features#71]
Input [2]: [true_cluster#2, features_raw#18]

(8) Coalesce
Input [2]: [true_cluster#2, features#71]
Arguments: 4



```

### plan_before.txt

```text
== Physical Plan ==
AdaptiveSparkPlan (16)
+- == Final Plan ==
   ResultQueryStage (15)
   +- TableCacheQueryStage (14), Statistics(sizeInBytes=156.3 KiB, rowCount=2.00E+3)
      +- InMemoryTableScan (1)
            +- InMemoryRelation (2)
                  +- AdaptiveSparkPlan (13)
                  +- == Final Plan ==
                     ResultQueryStage (11)
                     +- ShuffleQueryStage (10), Statistics(sizeInBytes=187.5 KiB, rowCount=2.00E+3)
                        +- Exchange (9)
                           +- TableCacheQueryStage (8), Statistics(sizeInBytes=156.3 KiB, rowCount=2.00E+3)
                              +- InMemoryTableScan (3)
                                    +- InMemoryRelation (4)
                                          +- * Project (7)
                                             +- * Project (6)
                                                +- * Scan ExistingRDD (5)
                  +- == Initial Plan ==
                     Exchange (12)
                     +- InMemoryTableScan (3)
                           +- InMemoryRelation (4)
                                 +- * Project (7)
                                    +- * Project (6)
                                       +- * Scan ExistingRDD (5)
+- == Initial Plan ==
   InMemoryTableScan (1)
      +- InMemoryRelation (2)
            +- AdaptiveSparkPlan (13)
            +- == Final Plan ==
               ResultQueryStage (11)
               +- ShuffleQueryStage (10), Statistics(sizeInBytes=187.5 KiB, rowCount=2.00E+3)
                  +- Exchange (9)
                     +- TableCacheQueryStage (8), Statistics(sizeInBytes=156.3 KiB, rowCount=2.00E+3)
                        +- InMemoryTableScan (3)
                              +- InMemoryRelation (4)
                                    +- * Project (7)
                                       +- * Project (6)
                                          +- * Scan ExistingRDD (5)
            +- == Initial Plan ==
               Exchange (12)
               +- InMemoryTableScan (3)
                     +- InMemoryRelation (4)
                           +- * Project (7)
                              +- * Project (6)
                                 +- * Scan ExistingRDD (5)


(1) InMemoryTableScan
Output [2]: [true_cluster#2, features#71]
Arguments: [true_cluster#2, features#71]

(2) InMemoryRelation
Arguments: [true_cluster#2, features#71], StorageLevel(disk, memory, deserialized, 1 replicas)

(3) InMemoryTableScan
Output [2]: [true_cluster#2, features#71]
Arguments: [true_cluster#2, features#71]

(4) InMemoryRelation
Arguments: [true_cluster#2, features#71], StorageLevel(disk, memory, deserialized, 1 replicas)

(5) Scan ExistingRDD [codegen id : 1]
Output [3]: [x#0, y#1, true_cluster#2]
Arguments: [x#0, y#1, true_cluster#2], MapPartitionsRDD[4] at applySchemaToPythonRDD at NativeMethodAccessorImpl.java:0, ExistingRDD, UnknownPartitioning(0)

(6) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(struct(x, x#0, y, y#1)) AS features_raw#18]
Input [3]: [x#0, y#1, true_cluster#2]

(7) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(features_raw#18) AS features#71]
Input [2]: [true_cluster#2, features_raw#18]

(8) TableCacheQueryStage
Output [2]: [true_cluster#2, features#71]
Arguments: 0

(9) Exchange
Input [2]: [true_cluster#2, features#71]
Arguments: RoundRobinPartitioning(64), REPARTITION_BY_NUM, [plan_id=1445]

(10) ShuffleQueryStage
Output [2]: [true_cluster#2, features#71]
Arguments: 1

(11) ResultQueryStage
Output [2]: [true_cluster#2, features#71]
Arguments: 2

(12) Exchange
Input [2]: [true_cluster#2, features#71]
Arguments: RoundRobinPartitioning(64), REPARTITION_BY_NUM, [plan_id=1419]

(13) AdaptiveSparkPlan
Output [2]: [true_cluster#2, features#71]
Arguments: isFinalPlan=true

(14) TableCacheQueryStage
Output [2]: [true_cluster#2, features#71]
Arguments: 0

(15) ResultQueryStage
Output [2]: [true_cluster#2, features#71]
Arguments: 1

(16) AdaptiveSparkPlan
Output [2]: [true_cluster#2, features#71]
Arguments: isFinalPlan=true



```

### plan_iteration.txt

```text
== Physical Plan ==
* Project (6)
+- InMemoryTableScan (1)
      +- InMemoryRelation (2)
            +- * Project (5)
               +- * Project (4)
                  +- * Scan ExistingRDD (3)


(1) InMemoryTableScan
Output [2]: [features#71, true_cluster#2]
Arguments: [features#71, true_cluster#2]

(2) InMemoryRelation
Arguments: [true_cluster#2, features#71], StorageLevel(disk, memory, deserialized, 1 replicas)

(3) Scan ExistingRDD [codegen id : 1]
Output [3]: [x#0, y#1, true_cluster#2]
Arguments: [x#0, y#1, true_cluster#2], MapPartitionsRDD[4] at applySchemaToPythonRDD at NativeMethodAccessorImpl.java:0, ExistingRDD, UnknownPartitioning(0)

(4) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(struct(x, x#0, y, y#1)) AS features_raw#18]
Input [3]: [x#0, y#1, true_cluster#2]

(5) Project [codegen id : 1]
Output [2]: [true_cluster#2, UDF(features_raw#18) AS features#71]
Input [2]: [true_cluster#2, features_raw#18]

(6) Project [codegen id : 1]
Output [3]: [true_cluster#2, features#71, UDF(features#71) AS prediction#4100]
Input [2]: [features#71, true_cluster#2]



```

