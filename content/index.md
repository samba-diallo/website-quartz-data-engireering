---
title: "Data Engineering & DevOps – Labs & Projets"
publish: true
---

# Data Engineering & DevOps
ESIEE Paris – Année universitaire 2025–2026

Ce site web présente l'ensemble des **travaux pratiques (labs)** et **projets finaux** réalisés dans le cadre des cours **Data Engineering 1** et **DevOps**.

**Auteurs :**  
- DIALLO Samba  
- DIOP Mouhamed  

---

## Présentation du cours

Le cours *Data Engineering 1* introduit les concepts fondamentaux de l’ingénierie des données à l’aide d’outils modernes tels que **Apache Spark**, **PySpark** et **SQL**.  
L’objectif principal est de comprendre les mécanismes du traitement distribué des données, d’analyser les performances et d’appliquer des bonnes pratiques d’optimisation.

Les différents labs et le projet final couvrent notamment :
- le traitement distribué de données à grande échelle,
- la transformation et l’analyse de données,
- l’utilisation des API RDD, DataFrame et Spark SQL,
- l’étude des performances et des stratégies d’optimisation,
- la restitution des résultats sous forme de rapports et de visualisations.

---

## Présentation des labs

### Lab 1 – Introduction à PySpark
Ce premier lab est consacré à la configuration de l’environnement Spark et à la prise en main de PySpark.  
Il inclut la réalisation d’un **Word Count** sur des données textuelles en utilisant les API **RDD** et **DataFrame**.

Lien : [Accéder au Lab 1](labs/lab1)

---

### Lab 2 – Pipeline d’ingénierie des données
Ce lab porte sur la construction d’un **pipeline complet de traitement de données** avec PySpark.  
Il comprend l’ingestion, la transformation de données, l’analyse de comportements utilisateurs et l’export des résultats.

Lien : [Accéder au Lab 2](labs/lab2)

---

### Lab 3 – Analyse et performances
Ce lab propose une analyse avancée à l’aide de **Spark SQL** et des **DataFrames**.  
Différentes implémentations de calculs (jointures, agrégations) sont comparées afin d’observer et d’expliquer les impacts sur les performances.

Lien : [Accéder au Lab 3](labs/lab3)

---

## Projet final

Le projet final constitue une application complète des notions abordées tout au long du cours sur un jeu de données réel.  
Il inclut :
- l’ingénierie et la préparation des données,
- l’analyse et l’optimisation des traitements,
- la production de métriques et de visualisations,
- la rédaction d’un rapport technique détaillé.

Lien : [Accéder au projet final](project)

---

# DevOps – Infrastructure & Automatisation

Le cours **DevOps** couvre les pratiques modernes de développement et d'opérations, incluant l'automatisation, la conteneurisation, l'orchestration et le déploiement continu.

## Labs DevOps

### TD1 – Introduction au Cloud (AWS EC2)
Configuration d'instances EC2, déploiement d'applications Node.js, et automatisation avec user-data scripts.

**Technologies :** AWS EC2, Node.js, User Data Scripts  
Lien : [[devops/td1/index|Accéder au TD1]]

---

### TD2 – Infrastructure as Code (Packer & OpenTofu)
Création d'images personnalisées avec Packer et déploiement d'infrastructure avec OpenTofu (Terraform).

**Technologies :** Packer, OpenTofu/Terraform, Ansible, AWS AMI  
Lien : [[devops/td2/index|Accéder au TD2]]

---

### TD3 – Automatisation avec Ansible
Gestion de configuration et automatisation du déploiement d'applications avec Ansible.

**Technologies :** Ansible, Playbooks, Roles, AWS  
Lien : [[devops/td3/index|Accéder au TD3]]

---

### TD4 – Docker & Conteneurisation
Création d'images Docker, gestion de conteneurs et déploiement d'applications conteneurisées.

**Technologies :** Docker, Dockerfile, Docker Compose, Node.js  
Lien : [[devops/td4/index|Accéder au TD4]]

---

### TD5 – CI/CD avec GitHub Actions
Mise en place de pipelines CI/CD automatisés avec GitHub Actions.

**Technologies :** GitHub Actions, CI/CD, Docker, Tests automatisés  
Lien : [[devops/td5/index|Accéder au TD5]]

---

### TD6 – Kubernetes & Orchestration
Déploiement et gestion d'applications sur Kubernetes avec Minikube.

**Technologies :** Kubernetes, Minikube, kubectl, Pods, Services  
Lien : [[devops/td6/index|Accéder au TD6]]

---

## Projet Final DevOps – EcoData Platform

Déploiement d'une **plateforme complète** de collecte et visualisation de données environnementales avec architecture cloud-native.

**Architecture :**
- **Frontend :** Streamlit (Python) – Interface utilisateur interactive
- **Backend :** FastAPI (Python) – API REST avec opérations CRUD
- **Base de données :** PostgreSQL – Stockage persistant
- **Infrastructure :** Kubernetes (Minikube) – Orchestration de conteneurs
- **CI/CD :** GitHub Actions – Automatisation du pipeline
- **Registry :** GitHub Container Registry (GHCR) – Stockage des images Docker

**Fonctionnalités :**
- Pipeline CI/CD automatisé (test → build → push → deploy)
- Déploiement automatique avec script `deploy-from-ghcr.sh`
- Haute disponibilité avec replicas
- Persistance des données avec PersistentVolumes
- Monitoring et logs centralisés

**Documentation complète :**
- [[devops/projet-final/ecodata-platform/index|Vue d'ensemble du projet]]
- [[devops/projet-final/ecodata-platform/documentation-projet-final-deploiement|Guide de déploiement complet]]
- [[devops/projet-final/ecodata-platform/backend/index|Documentation Backend]]
- [[devops/projet-final/ecodata-platform/frontend/index|Documentation Frontend]]

---

## Navigation rapide

### Data Engineering
- [Lab 1](labs/lab1)  
- [Lab 2](labs/lab2)  
- [Lab 3](labs/lab3)  
- [Projet final](project)

### DevOps
- [[devops/td1/index|TD1 – Cloud AWS]]
- [[devops/td2/index|TD2 – IaC Packer/OpenTofu]]
- [[devops/td3/index|TD3 – Ansible]]
- [[devops/td4/index|TD4 – Docker]]
- [[devops/td5/index|TD5 – CI/CD]]
- [[devops/td6/index|TD6 – Kubernetes]]
- [[devops/projet-final/ecodata-platform/index|Projet Final – EcoData Platform]]

---

## Ressources

**Data Engineering :**  
Dépôt GitHub : https://github.com/samba-diallo/data-engineering-1

**DevOps :**  
Dépôt GitHub : https://github.com/samba-diallo/Devops

