---
title: Projet Final DE2 - Preuves
date: 2026-05-24
description: Captures d'écran et plans d'exécution du projet final (dashboard, Spark UI, PageRank)
draft: false
---

# Projet Final DE2 — Preuves d'exécution

Captures du dashboard temps réel, de la Spark UI (Jobs / Executors) et du calcul PageRank, plus les plans d'exécution générés par le pipeline.

> 🔗 **Dashboard en ligne (démo live)** : **https://de2-dashboard-e2e.pages.dev/**

---

## Dashboard temps réel

### Mode sombre — « Luxe de Minuit »

![Dashboard mode sombre](./Dashboard_DarkMode_LuxeDeMinuit.png)

### Mode clair — « Aurore »

![Dashboard mode clair](./Dashboard_LightMode_Aurore.png)

---

## Spark UI — Jobs & Executors

### Jobs du pipeline (projet final)

![Spark UI - Jobs du projet final](./Jobs_Projet_final.png)

### Jobs Spark

![Spark UI - Jobs](./JObs.png)

### Executors (projet final)

![Spark UI - Executors du projet final](./Excutors_projetfinal.png)

### Executors

![Spark UI - Executors](./Executors.png)

---

## Traitement de graphe — PageRank

### Jobs Spark du calcul PageRank

![Spark UI - Jobs PageRank](./Jobs_Rankpage.png)

### Résultats PageRank

![Résultats PageRank](./Rankpage1.png)

---

## Plans d'exécution

- [Plan — agrégation Gold](./plan_gold_query.txt)
- [Plan — PageRank itératif](./plan_iterative_pagerank.txt)
