---
title: Projet Final DE2 - GitHub Archive
date: 2026-05-16
description: Vue d'ensemble du projet final Data Engineering 2
---

# Projet Final DE2 : Pipeline Data-Intensive sur GitHub Archive

> ## 🔗 Démo en ligne
> **▶️ Dashboard temps réel : https://de2-dashboard-e2e.pages.dev/**
>
> Application **Next.js** déployée qui consomme l'API analytics (FastAPI) du pipeline. Aperçus dans la [[proof/|galerie de preuves]].

Bienvenue sur la documentation de mon projet final pour le cours de Data Engineering 2.
Ce projet implémente une architecture Medallion complète avec du Streaming, du Traitement de Graphes (PageRank) et une préparation de données pour le Fine-Tuning LLM.

Le projet a deux faces :

- Le **rapport noté** ([[Rapport_Projet]]) décrit le pipeline Spark + Medallion + streaming fichier + PageRank + LLM-readiness — c'est la version évaluée par le cours.
- L'**extension Plateforme E2E** ([[E2E_Plateforme|Plateforme E2E]]) ajoute Kafka, Airflow, un backend FastAPI et un dashboard Next.js temps réel par-dessus le pipeline noté. Tout est orchestré via Docker Compose et déployable en production.

## Sommaire de la documentation

1. [[Rapport_Projet|Rapport Final (Architecture, Batch, Streaming, Graphe)]] — la version notée
2. [[E2E_Plateforme|Plateforme E2E (extension v2)]] — Kafka + Airflow + FastAPI + Next.js dashboard
3. [[Data_Card|Data Card (Qualité des données pour l'IA)]]
4. [[Usage_IA|Déclaration d'utilisation de l'IA]]
5. [[DE2_Project_Notebook_EN|Code Source du Notebook (PySpark)]]
6. [[proof/|Preuves d'exécution (dashboard, Spark UI, PageRank)]]

Toutes les preuves d'exécution (captures du dashboard, Spark UI, plans d'exécution) sont rassemblées dans la **[[proof/|galerie de preuves]]**, et également intégrées dans le rapport et la page Plateforme.
