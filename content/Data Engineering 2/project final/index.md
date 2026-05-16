---
title: Projet Final DE2 - GitHub Archive
date: 2026-05-16
description: Vue d'ensemble du projet final Data Engineering 2
---

# Projet Final DE2 : Pipeline Data-Intensive sur GitHub Archive

Bienvenue sur la documentation de mon projet final pour le cours de Data Engineering 2.
Ce projet implémente une architecture Medallion complète avec du Streaming, du Traitement de Graphes (PageRank) et une préparation de données pour le Fine-Tuning LLM.

Le projet a deux faces :

- Le **rapport noté** ([[Rapport_Projet]]) décrit le pipeline Spark + Medallion + streaming fichier + PageRank + LLM-readiness — c'est la version évaluée par le cours.
- L'**extension Plateforme E2E** ([[Plateforme]]) ajoute Kafka, Airflow, un backend FastAPI et un dashboard Next.js temps réel par-dessus le pipeline noté. Tout est orchestré via Docker Compose et déployable en production.

## Sommaire de la documentation

1. [[Rapport_Projet|Rapport Final (Architecture, Batch, Streaming, Graphe)]] — la version notée
2. [[Plateforme|Plateforme E2E (extension v2)]] — Kafka + Airflow + FastAPI + Next.js dashboard
3. [[Data_Card|Data Card (Qualité des données pour l'IA)]]
4. [[Usage_IA|Déclaration d'utilisation de l'IA]]
5. [[DE2_Project_Notebook_EN|Code Source du Notebook (PySpark)]]

Toutes les preuves d'exécution (Spark UI, Plans d'exécution, captures du dashboard) sont intégrées dans le rapport et la page Plateforme.
