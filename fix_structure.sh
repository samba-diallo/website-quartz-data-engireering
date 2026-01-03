#!/bin/bash

# COMMANDES POUR CORRIGER LA STRUCTURE DU PROJET QUARTZ
# Exécute ces commandes une par une

cd /home/sable/Documents/website

echo "=========================================="
echo "ETAPE 1 : Créer la structure static/"
echo "=========================================="

# Créer les dossiers manquants dans static/
mkdir -p static/labs/lab1/images
mkdir -p static/labs/lab1/outputs
mkdir -p static/labs/lab2/images
mkdir -p static/labs/lab2/outputs
mkdir -p static/labs/lab3/images
mkdir -p static/labs/lab3/outputs
mkdir -p static/project/images
mkdir -p static/project/outputs

echo "Dossiers créés dans static/"
tree static/ 2>/dev/null || find static -type d

echo ""
echo "=========================================="
echo "ETAPE 2 : Copier les images de Lab 1"
echo "=========================================="

cp public/static/labs/lab1/images/metrics.png static/labs/lab1/images/
cp public/static/labs/lab1/images/screenshot_lab1_extra.png static/labs/lab1/images/
cp public/static/labs/lab1/images/Spark_job.png static/labs/lab1/images/

echo "Images Lab 1 copiées"
ls -la static/labs/lab1/images/

echo ""
echo "=========================================="
echo "ETAPE 3 : Copier les fichiers .txt Lab 1"
echo "=========================================="

# Lab 1 n'a pas de fichiers txt actuellement, mais créer le dossier
echo "Lab 1 n'a pas de fichiers .txt"

echo ""
echo "=========================================="
echo "ETAPE 4 : Copier les images de Lab 2"
echo "=========================================="

cp public/static/labs/lab2/images/details\ metrics.png static/labs/lab2/images/
cp public/static/labs/lab2/images/details_sql_query.png static/labs/lab2/images/
cp public/static/labs/lab2/images/details_stage.png static/labs/lab2/images/
cp public/static/labs/lab2/images/metrics.png static/labs/lab2/images/
cp public/static/labs/lab2/images/spark_sql.png static/labs/lab2/images/
cp "public/static/labs/lab2/images/spark_ui_jobs_overview.png.png" static/labs/lab2/images/spark_ui_jobs_overview.png
cp "public/static/labs/lab2/images/spark_ui_stages_overview.png.png" static/labs/lab2/images/spark_ui_stages_overview.png

echo "Images Lab 2 copiées"
ls -la static/labs/lab2/images/

echo ""
echo "=========================================="
echo "ETAPE 5 : Copier les fichiers .txt Lab 2"
echo "=========================================="

cp public/static/labs/lab2/outputs/plan_fact_join.txt static/labs/lab2/outputs/
cp public/static/labs/lab2/outputs/plan_ingest.txt static/labs/lab2/outputs/

echo "Fichiers Lab 2 copiés"
ls -la static/labs/lab2/outputs/

echo ""
echo "=========================================="
echo "ETAPE 6 : Copier les images de Lab 3"
echo "=========================================="

cp public/static/labs/lab3/images/assignment3_esiee_57_1.png static/labs/lab3/images/
cp public/static/labs/lab3/images/assignment3_esiee_66_1.png static/labs/lab3/images/
cp public/static/labs/lab3/images/DE1_Lab3_screen_add_queries_metrics.png static/labs/lab3/images/
cp public/static/labs/lab3/images/details_job9.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job9.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job9_tasks.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job10.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job10_task.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job11_Spark.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job11_task.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job12_25.png static/labs/lab3/images/
cp public/static/labs/lab3/images/job12_Spark.png static/labs/lab3/images/
cp public/static/labs/lab3/images/lab3_queries_metrics_spark.png static/labs/lab3/images/

echo "Images Lab 3 copiées"
ls -la static/labs/lab3/images/

echo ""
echo "=========================================="
echo "ETAPE 7 : Copier les fichiers .txt Lab 3"
echo "=========================================="

cp public/static/labs/lab3/outputs/plan_broadcast.txt static/labs/lab3/outputs/
cp public/static/labs/lab3/outputs/plan_column.txt static/labs/lab3/outputs/
cp public/static/labs/lab3/outputs/plan_row.txt static/labs/lab3/outputs/

echo "Fichiers Lab 3 copiés"
ls -la static/labs/lab3/outputs/

echo ""
echo "=========================================="
echo "ETAPE 8 : Copier les images du Projet"
echo "=========================================="

cp public/static/project/images/metrics7.png static/project/images/
cp public/static/project/images/metrics_8.png static/project/images/
cp public/static/project/images/metrics_9.png static/project/images/
cp public/static/project/images/metrics_10.png static/project/images/
cp public/static/project/images/metrics_11.png static/project/images/
cp public/static/project/images/metrics_13.png static/project/images/
cp public/static/project/images/metrics_15.png static/project/images/
cp public/static/project/images/metrics12.png static/project/images/
cp public/static/project/images/Sparkjob.png static/project/images/

echo "Images du Projet copiées"
ls -la static/project/images/

echo ""
echo "=========================================="
echo "ETAPE 9 : Copier les fichiers .txt du Projet"
echo "=========================================="

cp public/static/project/outputs/baseline_q1_plan.txt static/project/outputs/
cp public/static/project/outputs/baseline_q2_plan.txt static/project/outputs/
cp public/static/project/outputs/baseline_q3_plan.txt static/project/outputs/
cp public/static/project/outputs/optimized_q1_plan.txt static/project/outputs/
cp public/static/project/outputs/optimized_q2_plan.txt static/project/outputs/
cp public/static/project/outputs/optimized_q3_plan.txt static/project/outputs/

echo "Fichiers du Projet copiés"
ls -la static/project/outputs/

echo ""
echo "=========================================="
echo "ETAPE 10 : Créer les fichiers Markdown"
echo "=========================================="

# Créer Labs - Data Engineering.md
cat > content/"Labs - Data Engineering.md" << 'EOF'
---
title: "Labs - Data Engineering"
publish: true
---

# Labs - Data Engineering

## Lab 1

### Travail Pratique - Lab 1

<iframe
src="/static/labs/lab1/assignment1_esiee.html"
width="100%"
height="900"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="Assignment 1 - ESIEE">
</iframe>

### Notebook - DE1_Lab1_Notebook_EN

<iframe
src="/static/labs/lab1/DE1_Lab1_Notebook_EN.html"
width="100%"
height="1100"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="DE1 Lab 1 Notebook">
</iframe>

### Visualisations et Métriques - Lab 1

![Metrics Lab 1](/static/labs/lab1/images/metrics.png)

![Screenshot Lab 1 Extra](/static/labs/lab1/images/screenshot_lab1_extra.png)

![Spark Job Lab 1](/static/labs/lab1/images/Spark_job.png)

---

## Lab 2

### Travail Pratique - Lab 2

<iframe
src="/static/labs/lab2/assignment2_esiee.html"
width="100%"
height="900"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="Assignment 2 - ESIEE">
</iframe>

### Notebook - DE1_Lab2_Notebook_EN

<iframe
src="/static/labs/lab2/DE1_Lab2_Notebook_EN.html"
width="100%"
height="1100"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="DE1 Lab 2 Notebook">
</iframe>

### Visualisations et Métriques - Lab 2

![Details Metrics Lab 2](/static/labs/lab2/images/details%20metrics.png)

![Metrics Lab 2](/static/labs/lab2/images/metrics.png)

![Details SQL Query Lab 2](/static/labs/lab2/images/details_sql_query.png)

![Details Stage Lab 2](/static/labs/lab2/images/details_stage.png)

![Spark SQL Lab 2](/static/labs/lab2/images/spark_sql.png)

![Spark UI Jobs Overview](/static/labs/lab2/images/spark_ui_jobs_overview.png)

![Spark UI Stages Overview](/static/labs/lab2/images/spark_ui_stages_overview.png)

### Plans d'Exécution - Lab 2

- [Plan Fact Join](/static/labs/lab2/outputs/plan_fact_join.txt)
- [Plan Ingest](/static/labs/lab2/outputs/plan_ingest.txt)

---

## Lab 3

### Travail Pratique - Lab 3

<iframe
src="/static/labs/lab3/assignment3_esiee.html"
width="100%"
height="900"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="Assignment 3 - ESIEE">
</iframe>

### Notebook - DE1_Lab3_Notebook_EN

<iframe
src="/static/labs/lab3/DE1_Lab3_Notebook_EN.html"
width="100%"
height="1100"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="DE1 Lab 3 Notebook">
</iframe>

### Visualisations et Résultats - Lab 3

![Assignment Result 1](/static/labs/lab3/images/assignment3_esiee_57_1.png)

![Assignment Result 2](/static/labs/lab3/images/assignment3_esiee_66_1.png)

![Lab 3 Queries Metrics Spark](/static/labs/lab3/images/lab3_queries_metrics_spark.png)

![Screen Add Queries Metrics](/static/labs/lab3/images/DE1_Lab3_screen_add_queries_metrics.png)

### Détails des Jobs - Lab 3

![Job 9](/static/labs/lab3/images/job9.png)

![Job 9 Details](/static/labs/lab3/images/details_job9.png)

![Job 9 Tasks](/static/labs/lab3/images/job9_tasks.png)

![Job 10](/static/labs/lab3/images/job10.png)

![Job 10 Tasks](/static/labs/lab3/images/job10_task.png)

![Job 11 Spark](/static/labs/lab3/images/job11_Spark.png)

![Job 11 Tasks](/static/labs/lab3/images/job11_task.png)

![Job 12 Metrics](/static/labs/lab3/images/job12_25.png)

![Job 12 Spark](/static/labs/lab3/images/job12_Spark.png)

### Plans d'Exécution - Lab 3

- [Plan Broadcast](/static/labs/lab3/outputs/plan_broadcast.txt)
- [Plan Column](/static/labs/lab3/outputs/plan_column.txt)
- [Plan Row](/static/labs/lab3/outputs/plan_row.txt)
EOF

echo "Fichier Labs - Data Engineering.md créé"

echo ""
echo "=========================================="
echo "ETAPE 11 : Créer le fichier Project.md"
echo "=========================================="

cat > content/Project.md << 'EOF'
---
title: "Project - Data Engineering"
publish: true
---

# Project - Data Engineering

## Travail Pratique - Project

<iframe
src="/static/project/project_esiee.html"
width="100%"
height="900"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="Project - ESIEE">
</iframe>

## Notebook - DE1_Project_Notebook_EN

<iframe
src="/static/project/DE1_Project_Notebook_EN.html"
width="100%"
height="1100"
loading="lazy"
style="border: 1px solid #ccc; border-radius: 12px;"
title="DE1 Project Notebook">
</iframe>

## Métriques et Visualisations

### Performance Metrics

![Metrics 7](/static/project/images/metrics7.png)

![Metrics 8](/static/project/images/metrics_8.png)

![Metrics 9](/static/project/images/metrics_9.png)

![Metrics 10](/static/project/images/metrics_10.png)

![Metrics 11](/static/project/images/metrics_11.png)

![Metrics 12](/static/project/images/metrics12.png)

![Metrics 13](/static/project/images/metrics_13.png)

![Metrics 15](/static/project/images/metrics_15.png)

### Spark Job Architecture

![Spark Job](/static/project/images/Sparkjob.png)

## Plans de Requêtes

### Baseline Plans

- [Plan Physique Q1 (Baseline)](/static/project/outputs/baseline_q1_plan.txt)
- [Plan Physique Q2 (Baseline)](/static/project/outputs/baseline_q2_plan.txt)
- [Plan Physique Q3 (Baseline)](/static/project/outputs/baseline_q3_plan.txt)

### Optimized Plans

- [Plan Optimisé Q1](/static/project/outputs/optimized_q1_plan.txt)
- [Plan Optimisé Q2](/static/project/outputs/optimized_q2_plan.txt)
- [Plan Optimisé Q3](/static/project/outputs/optimized_q3_plan.txt)
EOF

echo "Fichier Project.md créé"
ls -la content/

echo ""
echo "=========================================="
echo "ETAPE 12 : Vérifier la structure static/"
echo "=========================================="

echo "Structure complète de static/ :"
tree static/ 2>/dev/null || find static -type f

echo ""
echo "=========================================="
echo "ETAPE 13 : Build et test local"
echo "=========================================="

echo "Prêt pour le build ! Exécute :"
echo "npm run build"
echo "npm run docs"
echo ""
echo "Puis visite http://localhost:8080/Labs---Data-Engineering/ et http://localhost:8080/Project---Data-Engineering/"