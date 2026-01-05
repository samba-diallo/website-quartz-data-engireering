---
title: "Documentation Complète - Déploiement EcoData Platform"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Documentation Complète - Projet EcoData Platform

## Table des matières
1. [Introduction](#introduction)
2. [Architecture du projet](#architecture-du-projet)
3. [Prérequis système](#prérequis-système)
4. [Installation de l'environnement](#installation-de-lenvironnement)
5. [Structure du projet](#structure-du-projet)
6. [Déploiement de l'application](#déploiement-de-lapplication)
7. [Pipeline CI/CD](#pipeline-cicd)
8. [Opérations CRUD](#opérations-crud)
9. [Gestion et maintenance](#gestion-et-maintenance)
10. [Problèmes rencontrés et solutions](#problèmes-rencontrés-et-solutions)
11. [Commandes de référence](#commandes-de-référence)

---

## Introduction

### Contexte du projet
Ce projet consiste à déployer une application web complète (frontend, backend, base de données) en utilisant un pipeline CI/CD automatisé. L'objectif est de se familiariser avec les fondamentaux du DevOps moderne en privilégiant la simplicité et la mise en pratique concrète.

### Objectifs pédagogiques
- Comprendre l'intégration et la livraison continues (CI/CD)
- Maîtriser le déploiement sur Kubernetes
- Gérer une application conteneurisée avec Docker
- Implémenter des opérations CRUD dans une architecture microservices

### Technologies utilisées

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Frontend | Streamlit (Python) | Interface utilisateur web |
| Backend | FastAPI (Python) | API REST pour la logique métier |
| Base de données | PostgreSQL | Stockage persistant des données |
| Conteneurisation | Docker | Isolation des services |
| Orchestration | Kubernetes (Minikube) | Gestion des conteneurs |
| CI/CD | GitHub Actions | Automatisation du pipeline |
| Registry | GitHub Container Registry | Stockage des images Docker |

---

## Architecture du projet

### Architecture Kubernetes détaillée

```
Namespace: ecodata
│
├── Secrets
│   └── ecodata-secrets (credentials PostgreSQL)
│
├── PersistentVolumeClaim
│   └── postgres-pvc (stockage base de données)
│
├── Deployment
│   └── ecodata-postgres
│       ├── Image: postgres:15
│       ├── Port: 5432
│       ├── Volume: postgres-pvc
│       └── Secrets: ecodata-secrets
│
├── Deployments
│   ├── ecodata-backend
│   │   ├── Image: ghcr.io/samba-diallo/devops/ecodata-backend:latest
│   │   ├── Port: 8000
│   │   └── Variables d'env: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
│   │
│   └── ecodata-frontend
│       ├── Image: ghcr.io/samba-diallo/devops/ecodata-frontend:latest
│       ├── Port: 8501
│       └── Variable d'env: BACKEND_URL=http://ecodata-backend:8000
│
└── Services
    ├── ecodata-postgres (ClusterIP:5432)
    ├── ecodata-backend (ClusterIP:8000)
    └── ecodata-frontend (NodePort:8501→30255)
```

---

## Prérequis système

### Configuration minimale recommandée

| Ressource | Minimum | Recommandé |
|-----------|---------|------------|
| CPU | 2 cœurs | 4 cœurs |
| RAM | 4 GB | 8 GB |
| Disque | 20 GB libres | 30 GB libres |
| OS | Linux/macOS/Windows | Linux (Ubuntu 20.04+) |

### Logiciels requis

#### 1. Docker
```bash
# Vérifier l'installation
docker --version
# Résultat attendu: Docker version 20.x.x ou supérieur

# Installation sur Ubuntu (si nécessaire)
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. kubectl
```bash
# Vérifier l'installation
kubectl version --client
# Résultat attendu: Client Version: v1.x.x

# Installation sur Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### 3. Minikube
```bash
# Vérifier l'installation
minikube version
# Résultat attendu: minikube version: v1.x.x

# Installation sur Linux
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64
```

#### 4. Git
```bash
# Vérifier l'installation
git --version
# Résultat attendu: git version 2.x.x

# Installation sur Ubuntu (si nécessaire)
sudo apt-get install -y git
```

#### 5. Python (pour développement local)
```bash
# Vérifier l'installation
python3 --version
# Résultat attendu: Python 3.11.x

# Installation sur Ubuntu (si nécessaire)
sudo apt-get install -y python3.11 python3-pip
```

---

## Installation de l'environnement

### Étape 1: Cloner le repository

```bash
# Cloner le projet
git clone https://github.com/samba-diallo/Devops.git

# Naviguer dans le répertoire
cd Devops

# Vérifier la structure
ls -la
```

Vous devriez voir:
```
.github/
projet-final-devops/
td5/
README.md
.gitignore
```

### Étape 2: Configuration de Minikube

```bash
# Démarrer Minikube avec ressources adaptées
minikube start --cpus=4 --memory=4096 --driver=docker

# Si vous avez moins de RAM, utilisez:
minikube start --cpus=2 --memory=2048 --driver=docker

# Vérifier le statut
minikube status
```

Résultat attendu:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

```bash
# Vérifier la connexion kubectl
kubectl cluster-info

# Vérifier le node
kubectl get nodes
```

Résultat attendu:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.34.0
```

### Étape 3: Préparer l'environnement

```bash
# Naviguer vers le projet
cd projet-final-devops/ecodata-platform

# Rendre les scripts exécutables
chmod +x build-images.sh deploy-from-ghcr.sh
chmod +x k8s/deploy.sh k8s/cleanup.sh

# Vérifier que tout est en place
ls -la
```

Vous devriez voir:
```
backend/
frontend/
k8s/
build-images.sh
deploy-from-ghcr.sh
```

---

## Structure du projet

### Arborescence complète

```
Devops/
│
├── .github/
│   └── workflows/
│       └── ci-cd-ghcr.yml              # Pipeline CI/CD automatisé
│
├── projet-final-devops/
│   └── ecodata-platform/
│       │
│       ├── backend/                     # Service Backend (FastAPI)
│       │   ├── Dockerfile               # Image Docker du backend
│       │   ├── main.py                  # Point d'entrée FastAPI
│       │   ├── models.py                # Modèles SQLAlchemy (ORM)
│       │   ├── schemas.py               # Schémas Pydantic (validation)
│       │   ├── database.py              # Configuration base de données
│       │   └── requirements.txt         # Dépendances Python
│       │
│       ├── frontend/                    # Service Frontend (Streamlit)
│       │   ├── Dockerfile               # Image Docker du frontend
│       │   ├── app.py                   # Application Streamlit
│       │   └── requirements.txt         # Dépendances Python
│       │
│       ├── k8s/                         # Manifestes Kubernetes
│       │   ├── namespace.yaml           # Namespace ecodata
│       │   ├── secrets-and-pvc.yaml     # Secrets + Volume
│       │   ├── postgres-statefulset.yaml # Base de données
│       │   ├── backend-deployment.yaml  # Déploiement backend
│       │   ├── frontend-deployment.yaml # Déploiement frontend
│       │   ├── deploy.sh                # Script de déploiement
│       │   └── cleanup.sh               # Script de nettoyage
│       │
│       ├── build-images.sh              # Build images localement
│       └── deploy-from-ghcr.sh          # Déploiement depuis GHCR
│
├── td5/                                 # Travaux dirigés (non utilisé)
│
├── README.md                            # Documentation principale
└── .gitignore                           # Fichiers à ignorer
```

### Description des composants clés

#### Backend (FastAPI)

**Fichier: `backend/main.py`**
```python
# Point d'entrée de l'API REST
# Routes disponibles:
# - POST   /data/     : Créer une donnée (Create)
# - GET    /data/     : Lire toutes les données (Read)
# - GET    /data/{id} : Lire une donnée (Read)
# - PUT    /data/{id} : Modifier une donnée (Update)
# - DELETE /data/{id} : Supprimer une donnée (Delete)
```

**Fichier: `backend/models.py`**
```python
# Définit la structure de la table en base de données
# Utilise SQLAlchemy pour l'ORM (Object-Relational Mapping)
```

**Fichier: `backend/Dockerfile`**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend (Streamlit)

**Fichier: `frontend/app.py`**
```python
# Interface utilisateur web
# Permet de:
# - Visualiser les données dans un tableau
# - Ajouter de nouvelles données via un formulaire
# - Modifier des données existantes
# - Supprimer des données
# - Uploader des fichiers CSV
```

**Fichier: `frontend/Dockerfile`**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

#### Manifestes Kubernetes

**namespace.yaml**
```yaml
# Crée un espace de noms isolé pour l'application
apiVersion: v1
kind: Namespace
metadata:
  name: ecodata
```

**secrets-and-pvc.yaml**
```yaml
# Secret: stocke les credentials PostgreSQL de manière sécurisée
# PVC: réserve de l'espace disque pour les fichiers uploadés
```

**postgres-statefulset.yaml**
```yaml
# StatefulSet: garantit l'ordre de déploiement et la persistance
# Service: expose PostgreSQL en interne sur le port 5432
```

**backend-deployment.yaml**
```yaml
# Deployment: gère 2 replicas du backend pour la haute disponibilité
# Service: expose le backend en interne sur le port 8000
```

**frontend-deployment.yaml**
```yaml
# Deployment: gère 2 replicas du frontend
# Service: expose le frontend avec LoadBalancer sur le port 8501
```

---

## Déploiement de l'application

### Méthode 1: Déploiement automatique (Recommandé)

Cette méthode utilise les images pré-construites stockées dans GitHub Container Registry.

```bash
# 1. Naviguer vers le projet
cd ~/Devops/projet-final-devops/ecodata-platform

# 2. Exécuter le script de déploiement automatique
bash deploy-from-ghcr.sh
```

**Ce que fait le script:**
1. Vérifie si Minikube est démarré, sinon le lance
2. Pull les images Docker depuis GHCR
3. Charge les images dans Minikube
4. Met à jour les manifests Kubernetes avec les bonnes images
5. Applique tous les manifests (namespace, secrets, deployments, services)
6. Attend que les pods soient prêts
7. Ouvre automatiquement l'application dans votre navigateur

**Sortie attendue:**
```
[INFO] Verification de Minikube...
[OK] Minikube est actif
[INFO] Pull des images depuis GHCR...
[INFO] Chargement des images dans Minikube...
[INFO] Mise a jour des manifests Kubernetes...
[INFO] Deploiement sur Minikube...
namespace/ecodata created
secret/ecodata-secrets created
persistentvolumeclaim/ecodata-uploads-pvc created
statefulset.apps/ecodata-postgres created
service/ecodata-postgres created
deployment.apps/ecodata-backend created
service/ecodata-backend created
deployment.apps/ecodata-frontend created
service/ecodata-frontend created
[INFO] Attente que les pods soient prets (60 secondes)...
[OK] Tous les pods sont prets
[INFO] Ouverture de l'application...
```

### Méthode 2: Déploiement manuel (Pour développement)

Cette méthode construit les images localement à partir du code source.

#### Étape 1: Construire les images Docker

```bash
# Naviguer vers le projet
cd ~/Devops/projet-final-devops/ecodata-platform

# Exécuter le script de build
bash build-images.sh
```

**Ce que fait le script:**
```bash
# Build backend
docker build -t ecodata-backend:latest ./backend

# Build frontend
docker build -t ecodata-frontend:latest ./frontend

# Charge les images dans Minikube
minikube image load ecodata-backend:latest
minikube image load ecodata-frontend:latest
```

**Vérifier les images:**
```bash
# Dans Minikube
minikube image ls | grep ecodata

# Résultat attendu:
# docker.io/library/ecodata-backend:latest
# docker.io/library/ecodata-frontend:latest
```

#### Étape 2: Déployer sur Kubernetes

```bash
# Naviguer vers le dossier k8s
cd k8s

# Exécuter le script de déploiement
bash deploy.sh
```

**Ce que fait le script:**
```bash
# 1. Vérifie Minikube
# 2. Crée le namespace
kubectl apply -f namespace.yaml

# 3. Crée les secrets et PVC
kubectl apply -f secrets-and-pvc.yaml

# 4. Déploie PostgreSQL
kubectl apply -f postgres-statefulset.yaml

# 5. Attend 30 secondes pour PostgreSQL

# 6. Déploie le backend
kubectl apply -f backend-deployment.yaml

# 7. Déploie le frontend
kubectl apply -f frontend-deployment.yaml
```

#### Étape 3: Vérifier le déploiement

```bash
# Voir tous les pods
kubectl get pods -n ecodata
```

**État attendu (après 1-2 minutes):**
```
NAME                                READY   STATUS    RESTARTS   AGE
ecodata-backend-xxx                 1/1     Running   0          2m
ecodata-backend-yyy                 1/1     Running   0          2m
ecodata-frontend-aaa                1/1     Running   0          2m
ecodata-frontend-bbb                1/1     Running   0          2m
ecodata-postgres-0                  1/1     Running   0          2m
```

**Si les pods sont en `ContainerCreating`:** Attendez quelques secondes.

**Si les pods sont en `ErrImagePull` ou `ImagePullBackOff`:**
```bash
# Vérifier que les images sont bien chargées
minikube image ls | grep ecodata

# Si les images n'apparaissent pas, relancer le build
cd ..
bash build-images.sh
```

```bash
# Voir les services
kubectl get svc -n ecodata
```

**Résultat attendu:**
```
NAME               TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
ecodata-backend    ClusterIP      10.111.x.x      <none>        8000/TCP         2m
ecodata-frontend   LoadBalancer   10.103.x.x      <pending>     8501:30255/TCP   2m
ecodata-postgres   ClusterIP      10.108.x.x      <none>        5432/TCP         2m
```

**Note:** `EXTERNAL-IP` restera `<pending>` sur Minikube, c'est normal.

#### Étape 4: Accéder à l'application

```bash
# Ouvrir le frontend automatiquement
minikube service ecodata-frontend -n ecodata
```

Cette commande:
1. Crée un tunnel vers le service
2. Ouvre automatiquement votre navigateur par défaut
3. Affiche l'URL dans le terminal

**Sortie attendue:**
```
|-----------|------------------|-------------|---------------------------|
| NAMESPACE |       NAME       | TARGET PORT |            URL            |
|-----------|------------------|-------------|---------------------------|
| ecodata   | ecodata-frontend | http/8501   | http://192.168.49.2:30255 |
|-----------|------------------|-------------|---------------------------|
Opening service ecodata/ecodata-frontend in default browser...
```

**Si le navigateur ne s'ouvre pas automatiquement:**
Copiez l'URL affichée et ouvrez-la manuellement dans votre navigateur.

### Méthode 3: Déploiement depuis VS Code

#### Configuration de VS Code

1. **Installer les extensions recommandées:**
   - Docker (Microsoft)
   - Kubernetes (Microsoft)
   - YAML (Red Hat)

2. **Ouvrir le projet:**
```bash
code ~/Devops
```

3. **Ouvrir le terminal intégré:**
   - Menu: Terminal → New Terminal
   - Raccourci: `Ctrl + `` (backtick)

#### Étapes de déploiement

**Dans le terminal VS Code:**

```bash
# 1. Naviguer vers le projet
cd projet-final-devops/ecodata-platform

# 2. Déployer automatiquement
bash deploy-from-ghcr.sh

# OU pour développement local:
# bash build-images.sh
# cd k8s
# bash deploy.sh
```

**Avantages de VS Code:**
- Coloration syntaxique pour YAML
- Autocomplétion kubectl
- Visualisation graphique des pods (avec extension Kubernetes)
- Accès facile aux logs des pods
- Éditeur intégré pour modifier les manifests

#### Utiliser l'extension Kubernetes

1. Cliquer sur l'icône Kubernetes dans la barre latérale
2. Développer `Clusters → minikube → Namespaces → ecodata`
3. Voir tous les pods, services, deployments
4. Clic droit sur un pod → `Get Logs` pour voir les logs
5. Clic droit sur un service → `Forward Port` pour accéder

---

## Pipeline CI/CD

### Vue d'ensemble du workflow

Le pipeline CI/CD est automatiquement déclenché à chaque:
- Push sur la branche `main`
- Pull Request vers la branche `main`

**Fichier:** `.github/workflows/ci-cd-ghcr.yml`

### Structure du pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Déclenchement                             │
│              (push ou pull_request sur main)                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─────────────────┬──────────────────┬────────────┐
             ▼                 ▼                  ▼            ▼
      ┌──────────┐      ┌──────────┐      ┌──────────┐  ┌──────────┐
      │   Job 1  │      │   Job 2  │      │   Job 3  │  │   Job 4  │
      │  Tests   │  →   │  Build & │  →   │ Notify PR│  │  Report  │
      │          │      │   Push   │      │          │  │          │
      └──────────┘      └──────────┘      └──────────┘  └──────────┘
```

### Job 1: Tests

**Objectif:** Valider que le code compile et fonctionne.

```yaml
steps:
  - Checkout du code
  - Installation Python 3.11
  - Installation dépendances backend
  - Installation dépendances frontend
  - Exécution tests backend
  - Exécution tests frontend
```

**Commandes exécutées:**
```bash
# Backend
cd backend
pip install -r requirements.txt
python -c "import main; print('Backend OK')"

# Frontend
cd frontend
pip install -r requirements.txt
python -c "import app; print('Frontend OK')"
```

### Job 2: Build and Push

**Objectif:** Construire les images Docker et les pousser vers GHCR.

```yaml
steps:
  - Checkout du code
  - Configuration Docker Buildx
  - Login vers GHCR (avec GITHUB_TOKEN)
  - Extraction des métadonnées (tags, labels)
  - Build et push backend
  - Build et push frontend
```

**Images générées:**
```
ghcr.io/samba-diallo/devops/ecodata-backend:latest
ghcr.io/samba-diallo/devops/ecodata-backend:main-<sha>

ghcr.io/samba-diallo/devops/ecodata-frontend:latest
ghcr.io/samba-diallo/devops/ecodata-frontend:main-<sha>
```

**Note importante:** Le job ne s'exécute que sur `push` (pas sur `pull_request`).

### Job 3: Notify PR (optionnel)

**Objectif:** Commenter la Pull Request avec le statut du build.

Ce job est désactivé par défaut car nécessite des permissions additionnelles.

### Job 4: Report

**Objectif:** Générer un rapport de déploiement.

```yaml
steps:
  - Génération du rapport (texte simple)
  - Upload en tant qu'artifact
```

**Contenu du rapport:**
```
Pipeline Summary Report
======================
Tests: success
Build: success
Timestamp: 2026-01-05 21:59:00
```

**Accès au rapport:**
1. Aller sur GitHub Actions
2. Cliquer sur le workflow exécuté
3. Télécharger l'artifact `deployment-report`

### Configuration GitHub requise

#### Permissions du workflow

**Important:** Le workflow nécessite des permissions d'écriture pour pousser vers GHCR.

**Configuration:**
1. Aller sur GitHub: `https://github.com/samba-diallo/Devops`
2. Cliquer sur `Settings`
3. Dans la barre latérale: `Actions` → `General`
4. Scroller jusqu'à `Workflow permissions`
5. Sélectionner `Read and write permissions`
6. Cliquer `Save`

**Capture d'écran attendue:**
```
○ Read repository contents and packages permissions (default)
● Read and write permissions
```

#### Visibilité des packages GHCR

Par défaut, les packages GHCR sont privés. Pour les rendre publics:

1. Aller sur votre profil GitHub
2. Cliquer sur `Packages`
3. Sélectionner `ecodata-backend` et `ecodata-frontend`
4. Cliquer sur `Package settings`
5. Scroller jusqu'à `Danger Zone`
6. Cliquer sur `Change visibility` → `Public`

### Déclencher manuellement le pipeline

#### Méthode 1: Via un commit

```bash
# Faire un petit changement
echo "# Test pipeline" >> README.md

# Commit et push
git add README.md
git commit -m "Test CI/CD pipeline"
git push origin main
```

#### Méthode 2: Via une Pull Request

```bash
# Créer une nouvelle branche
git checkout -b test-feature

# Faire des modifications
echo "nouvelle feature" > feature.txt
git add feature.txt
git commit -m "Add new feature"

# Pousser la branche
git push origin test-feature

# Créer une PR sur GitHub
# Le pipeline se déclenchera automatiquement
```

### Voir l'exécution du pipeline

1. Aller sur: `https://github.com/samba-diallo/Devops/actions`
2. Vous verrez la liste des workflows exécutés
3. Cliquer sur un workflow pour voir les détails
4. Cliquer sur un job pour voir les logs

**Interface attendue:**
```
CI/CD - EcoData Platform
#2: Fix YAML syntax in workflow
by samba-diallo was started 5 minutes ago

Run details
✓ Run Tests (2m 15s)
✓ Build and Push Docker Images (45s)
✓ Generate Deployment Report (8s)

Total duration: 3m 12s
Status: Success
```

### Déboguer un workflow qui échoue

#### Voir les logs détaillés

```bash
# Méthode 1: Via l'interface GitHub
# Cliquer sur le job qui a échoué
# Les logs s'affichent avec les erreurs en rouge

# Méthode 2: Via GitHub CLI (si installé)
gh run list
gh run view <run-id>
```

#### Erreurs courantes

**1. Test failed**
```
Error: Command '...' returned non-zero exit status 1
```
Solution: Vérifier le code source, corriger l'erreur, recommiter.

**2. Permission denied lors du push vers GHCR**
```
Error: denied: permission_denied: write_package
```
Solution: Vérifier les permissions du workflow (voir section Configuration GitHub).

**3. Invalid workflow file**
```
Error: You have an error in your yaml syntax on line X
```
Solution: Valider le YAML localement:
```bash
python3 -m pip install yamllint
yamllint .github/workflows/ci-cd-ghcr.yml
```

---

## Opérations CRUD

### Interface utilisateur (Frontend)

Une fois l'application déployée et accessible, vous pouvez effectuer des opérations CRUD directement via l'interface Streamlit.

#### Accéder à l'interface

```bash
minikube service ecodata-frontend -n ecodata
```

L'URL sera quelque chose comme: `http://192.168.49.2:30255`

### Create (Créer)

**Via l'interface:**
1. Dans la section "Ajouter une nouvelle donnée"
2. Remplir les champs:
   - Nom: Ex. "Station Météo Paris"
   - Type: Ex. "Temperature"
   - Valeur: Ex. "22.5"
3. Cliquer sur "Ajouter"

**Via l'API (curl):**
```bash
# Obtenir l'URL du backend
BACKEND_URL=$(kubectl get svc ecodata-backend -n ecodata -o jsonpath='{.spec.clusterIP}')

# Créer une donnée
curl -X POST "http://$BACKEND_URL:8000/data/" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Station Météo Paris",
    "type": "Temperature",
    "valeur": "22.5"
  }'
```

**Réponse attendue:**
```json
{
  "id": 1,
  "nom": "Station Météo Paris",
  "type": "Temperature",
  "valeur": "22.5"
}
```

### Read (Lire)

**Via l'interface:**
- Les données s'affichent automatiquement dans le tableau en haut de page
- Le tableau se rafraîchit toutes les 5 secondes

**Via l'API - Lire toutes les données:**
```bash
curl -X GET "http://$BACKEND_URL:8000/data/"
```

**Réponse attendue:**
```json
[
  {
    "id": 1,
    "nom": "Station Météo Paris",
    "type": "Temperature",
    "valeur": "22.5"
  },
  {
    "id": 2,
    "nom": "Capteur Humidité Lyon",
    "type": "Humidity",
    "valeur": "65.0"
  }
]
```

**Via l'API - Lire une donnée spécifique:**
```bash
curl -X GET "http://$BACKEND_URL:8000/data/1"
```

**Réponse attendue:**
```json
{
  "id": 1,
  "nom": "Station Météo Paris",
  "type": "Temperature",
  "valeur": "22.5"
}
```

### Update (Modifier)

**Via l'interface:**
1. Dans le tableau, identifier l'ID de la donnée à modifier
2. Dans la section "Modifier une donnée"
3. Entrer l'ID de la donnée
4. Remplir les nouveaux champs
5. Cliquer sur "Modifier"

**Via l'API:**
```bash
curl -X PUT "http://$BACKEND_URL:8000/data/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Station Météo Paris Centre",
    "type": "Temperature",
    "valeur": "23.5"
  }'
```

**Réponse attendue:**
```json
{
  "id": 1,
  "nom": "Station Météo Paris Centre",
  "type": "Temperature",
  "valeur": "23.5"
}
```

### Delete (Supprimer)

**Via l'interface:**
1. Dans le tableau, identifier l'ID de la donnée à supprimer
2. Dans la section "Supprimer une donnée"
3. Entrer l'ID de la donnée
4. Cliquer sur "Supprimer"

**Via l'API:**
```bash
curl -X DELETE "http://$BACKEND_URL:8000/data/1"
```

**Réponse attendue:**
```json
{
  "message": "Données supprimées avec succès"
}
```

### Tester les opérations CRUD complètes

**Script de test complet:**
```bash
#!/bin/bash

# Obtenir l'URL du backend
BACKEND_URL=$(kubectl get svc ecodata-backend -n ecodata -o jsonpath='{.spec.clusterIP}')

echo "=== Test CREATE ==="
curl -X POST "http://$BACKEND_URL:8000/data/" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test Station","type":"Test","valeur":"100"}'

echo -e "\n\n=== Test READ ALL ==="
curl -X GET "http://$BACKEND_URL:8000/data/"

echo -e "\n\n=== Test READ ONE ==="
curl -X GET "http://$BACKEND_URL:8000/data/1"

echo -e "\n\n=== Test UPDATE ==="
curl -X PUT "http://$BACKEND_URL:8000/data/1" \
  -H "Content-Type: application/json" \
  -d '{"nom":"Updated Station","type":"Test","valeur":"200"}'

echo -e "\n\n=== Test DELETE ==="
curl -X DELETE "http://$BACKEND_URL:8000/data/1"

echo -e "\n\n=== Test READ ALL (après suppression) ==="
curl -X GET "http://$BACKEND_URL:8000/data/"
```

---

## Gestion et maintenance

### Surveillance des pods

#### Voir le statut en temps réel

```bash
# Voir tous les pods avec rafraîchissement automatique
kubectl get pods -n ecodata --watch

# Arrêter avec Ctrl+C
```

#### Voir les logs des pods

```bash
# Logs du backend (premier pod)
kubectl logs -n ecodata deployment/ecodata-backend --tail=50 --follow

# Logs du frontend
kubectl logs -n ecodata deployment/ecodata-frontend --tail=50 --follow

# Logs de PostgreSQL
kubectl logs -n ecodata ecodata-postgres-0 --tail=50 --follow

# Logs d'un pod spécifique
kubectl logs -n ecodata <nom-du-pod> --tail=100
```

#### Diagnostiquer un pod qui ne démarre pas

```bash
# Voir les détails d'un pod
kubectl describe pod -n ecodata <nom-du-pod>

# Voir les événements du namespace
kubectl get events -n ecodata --sort-by='.lastTimestamp'

# Accéder à un pod pour déboguer
kubectl exec -it -n ecodata <nom-du-pod> -- /bin/bash
```

### Mise à l'échelle

#### Augmenter le nombre de replicas

```bash
# Augmenter le backend à 3 replicas
kubectl scale deployment ecodata-backend -n ecodata --replicas=3

# Augmenter le frontend à 4 replicas
kubectl scale deployment ecodata-frontend -n ecodata --replicas=4

# Vérifier les changements
kubectl get pods -n ecodata
```

#### Revenir au nombre initial

```bash
kubectl scale deployment ecodata-backend -n ecodata --replicas=2
kubectl scale deployment ecodata-frontend -n ecodata --replicas=2
```

### Mise à jour des images

#### Après un nouveau build CI/CD

```bash
# Forcer le redéploiement avec les nouvelles images
kubectl rollout restart deployment/ecodata-backend -n ecodata
kubectl rollout restart deployment/ecodata-frontend -n ecodata

# Vérifier le statut du rollout
kubectl rollout status deployment/ecodata-backend -n ecodata
kubectl rollout status deployment/ecodata-frontend -n ecodata
```

#### Rollback en cas de problème

```bash
# Voir l'historique des déploiements
kubectl rollout history deployment/ecodata-backend -n ecodata

# Revenir à la version précédente
kubectl rollout undo deployment/ecodata-backend -n ecodata

# Revenir à une version spécifique
kubectl rollout undo deployment/ecodata-backend -n ecodata --to-revision=2
```

### Sauvegarder la base de données

#### Créer un backup

```bash
# Se connecter au pod PostgreSQL
kubectl exec -it -n ecodata ecodata-postgres-0 -- bash

# Dans le pod, créer un dump
pg_dump -U ecouser -d ecodata > /tmp/backup.sql

# Sortir du pod (Ctrl+D)

# Copier le backup localement
kubectl cp ecodata/ecodata-postgres-0:/tmp/backup.sql ./backup-$(date +%Y%m%d).sql
```

#### Restaurer un backup

```bash
# Copier le backup dans le pod
kubectl cp ./backup.sql ecodata/ecodata-postgres-0:/tmp/backup.sql

# Se connecter au pod
kubectl exec -it -n ecodata ecodata-postgres-0 -- bash

# Restaurer le backup
psql -U ecouser -d ecodata < /tmp/backup.sql

# Sortir du pod
exit
```

### Nettoyage et redéploiement

#### Supprimer complètement l'application

```bash
# Utiliser le script de nettoyage
cd ~/Devops/projet-final-devops/ecodata-platform/k8s
bash cleanup.sh

# OU manuellement:
kubectl delete namespace ecodata

# Vérifier que tout est supprimé
kubectl get all -n ecodata
```

#### Redéployer depuis zéro

```bash
# Méthode automatique
cd ~/Devops/projet-final-devops/ecodata-platform
bash deploy-from-ghcr.sh

# OU méthode manuelle
bash build-images.sh
cd k8s
bash deploy.sh
```

### Gestion des ressources Minikube

#### Voir l'utilisation des ressources

```bash
# Voir l'utilisation CPU/RAM par pod
kubectl top pods -n ecodata

# Voir l'utilisation du node
kubectl top node
```

#### Redémarrer Minikube

```bash
# Arrêter Minikube
minikube stop

# Démarrer Minikube
minikube start

# Redéployer l'application
cd ~/Devops/projet-final-devops/ecodata-platform
bash deploy-from-ghcr.sh
```

#### Supprimer et recréer le cluster

```bash
# Supprimer complètement le cluster
minikube delete

# Recréer un nouveau cluster
minikube start --cpus=4 --memory=4096 --driver=docker

# Redéployer l'application
cd ~/Devops/projet-final-devops/ecodata-platform
bash deploy-from-ghcr.sh
```

---

## Problèmes rencontrés et solutions

### Problème 1: Images Docker non trouvées

**Symptôme:**
```
Failed to pull image "ecodata-backend:latest": rpc error: code = Unknown
desc = Error response from daemon: pull access denied for ecodata-backend
```

**Cause:** Les images ne sont pas chargées dans Minikube.

**Solution:**
```bash
# Reconstruire et charger les images
cd ~/Devops/projet-final-devops/ecodata-platform
bash build-images.sh

# OU pour utiliser GHCR
bash deploy-from-ghcr.sh
```

### Problème 2: Pods en CrashLoopBackOff

**Symptôme:**
```
NAME                                READY   STATUS             RESTARTS   AGE
ecodata-backend-xxx                 0/1     CrashLoopBackOff   5          3m
```

**Cause:** Le conteneur démarre puis s'arrête immédiatement.

**Solution:**
```bash
# Voir les logs pour identifier l'erreur
kubectl logs -n ecodata <nom-du-pod>

# Causes communes:
# 1. Base de données non accessible
kubectl get pods -n ecodata | grep postgres

# 2. Variables d'environnement incorrectes
kubectl describe pod -n ecodata <nom-du-pod>

# 3. Erreur dans le code
# Vérifier les logs pour voir l'erreur Python
```

### Problème 3: Service frontend non accessible

**Symptôme:**
```
Error: unable to forward port because pod is not running
```

**Cause:** Le pod frontend n'est pas en état Running.

**Solution:**
```bash
# Vérifier l'état des pods
kubectl get pods -n ecodata

# Si le pod n'existe pas, vérifier le deployment
kubectl get deployment -n ecodata

# Si le deployment n'existe pas, redéployer
cd ~/Devops/projet-final-devops/ecodata-platform/k8s
kubectl apply -f frontend-deployment.yaml

# Si le pod est en erreur, voir les logs
kubectl logs -n ecodata deployment/ecodata-frontend
```

### Problème 4: Base de données perd les données

**Symptôme:** Les données disparaissent après un redémarrage du pod PostgreSQL.

**Cause:** Le PersistentVolume n'est pas correctement configuré.

**Solution:**
```bash
# Vérifier que le PVC est bien créé
kubectl get pvc -n ecodata

# Vérifier que le StatefulSet utilise le volume
kubectl describe statefulset ecodata-postgres -n ecodata

# Si le PVC n'existe pas, le recréer
kubectl apply -f k8s/secrets-and-pvc.yaml
```

### Problème 5: Pipeline CI/CD échoue

**Symptôme:** Le workflow GitHub Actions ne s'exécute pas ou échoue.

**Causes et solutions:**

**1. Permission denied pour GHCR:**
```
Error: denied: permission_denied: write_package
```
Solution: Activer les permissions d'écriture (voir section Pipeline CI/CD).

**2. Tests Python échouent:**
```
ModuleNotFoundError: No module named 'fastapi'
```
Solution: Vérifier que `requirements.txt` est à jour et complet.

**3. Syntaxe YAML incorrecte:**
```
Error: You have an error in your yaml syntax
```
Solution: Valider le YAML avec yamllint ou un validateur en ligne.

### Problème 6: Minikube ne démarre pas

**Symptôme:**
```
Exiting due to GUEST_DRIVER_MISMATCH: The existing "minikube" cluster was created using the "virtualbox" driver, which is incompatible with requested "docker" driver.
```

**Solution:**
```bash
# Supprimer l'ancien cluster
minikube delete

# Recréer avec le bon driver
minikube start --cpus=4 --memory=4096 --driver=docker
```

### Problème 7: Connection refused vers le backend

**Symptôme:** Le frontend ne peut pas contacter le backend.

**Cause:** Variable d'environnement `BACKEND_URL` incorrecte.

**Solution:**
```bash
# Vérifier l'URL du backend dans le frontend
kubectl describe deployment ecodata-frontend -n ecodata | grep BACKEND_URL

# L'URL doit être: http://ecodata-backend:8000

# Si incorrecte, modifier frontend-deployment.yaml
# Puis redéployer:
kubectl apply -f k8s/frontend-deployment.yaml
```

### Problème 8: Espace disque insuffisant

**Symptôme:**
```
Error: No space left on device
```

**Solution:**
```bash
# Nettoyer les images Docker inutilisées
docker system prune -a --volumes

# Dans Minikube
minikube ssh
docker system prune -a
exit

# Supprimer les anciennes images
minikube image rm <image-name>
```

---

## Commandes de référence

### Commandes Minikube essentielles

```bash
# Démarrer Minikube
minikube start --cpus=4 --memory=4096 --driver=docker

# Arrêter Minikube
minikube stop

# Supprimer le cluster
minikube delete

# Voir le statut
minikube status

# Ouvrir le dashboard Kubernetes
minikube dashboard

# Accéder à un service
minikube service <service-name> -n <namespace>

# SSH dans le node Minikube
minikube ssh

# Voir l'IP du cluster
minikube ip
```

### Commandes kubectl essentielles

```bash
# Voir tous les namespaces
kubectl get namespaces

# Voir toutes les ressources dans un namespace
kubectl get all -n ecodata

# Voir les pods
kubectl get pods -n ecodata
kubectl get pods -n ecodata -o wide

# Voir les services
kubectl get svc -n ecodata

# Voir les deployments
kubectl get deployments -n ecodata

# Voir les logs
kubectl logs -n ecodata <pod-name>
kubectl logs -n ecodata deployment/<deployment-name>

# Décrire une ressource (détails complets)
kubectl describe pod -n ecodata <pod-name>
kubectl describe service -n ecodata <service-name>

# Exécuter une commande dans un pod
kubectl exec -it -n ecodata <pod-name> -- /bin/bash

# Port-forward local
kubectl port-forward -n ecodata svc/ecodata-frontend 8501:8501

# Appliquer des manifests
kubectl apply -f <file.yaml>
kubectl apply -f <directory>/

# Supprimer des ressources
kubectl delete -f <file.yaml>
kubectl delete pod -n ecodata <pod-name>
kubectl delete namespace ecodata

# Mise à l'échelle
kubectl scale deployment <deployment-name> -n ecodata --replicas=3

# Rollout
kubectl rollout restart deployment/<deployment-name> -n ecodata
kubectl rollout status deployment/<deployment-name> -n ecodata
kubectl rollout undo deployment/<deployment-name> -n ecodata
kubectl rollout history deployment/<deployment-name> -n ecodata
```

### Commandes Docker essentielles

```bash
# Lister les images
docker images
minikube image ls

# Construire une image
docker build -t <image-name>:<tag> .

# Charger une image dans Minikube
minikube image load <image-name>:<tag>

# Supprimer une image
docker rmi <image-name>:<tag>
minikube image rm <image-name>:<tag>

# Nettoyer les ressources
docker system prune -a
docker volume prune
```

### Commandes Git essentielles

```bash
# Cloner le repository
git clone https://github.com/samba-diallo/Devops.git

# Voir le statut
git status

# Ajouter des fichiers
git add .
git add <file>

# Commiter
git commit -m "message"

# Pousser vers GitHub
git push origin main

# Créer une branche
git checkout -b <branch-name>

# Changer de branche
git checkout main

# Voir l'historique
git log --oneline
```

### Commandes de débogage

```bash
# Tester la connectivité réseau dans un pod
kubectl exec -it -n ecodata <pod-name> -- curl http://ecodata-backend:8000/

# Vérifier les DNS
kubectl exec -it -n ecodata <pod-name> -- nslookup ecodata-backend

# Voir les événements du cluster
kubectl get events -n ecodata --sort-by='.lastTimestamp'

# Voir l'utilisation des ressources
kubectl top pods -n ecodata
kubectl top node

# Inspecter un secret
kubectl get secret ecodata-secrets -n ecodata -o yaml

# Vérifier les variables d'environnement d'un pod
kubectl exec -n ecodata <pod-name> -- env
```

### Scripts de déploiement rapide

**Déploiement complet automatique:**
```bash
cd ~/Devops/projet-final-devops/ecodata-platform && bash deploy-from-ghcr.sh
```

**Rebuild et redéploiement local:**
```bash
cd ~/Devops/projet-final-devops/ecodata-platform
bash build-images.sh
cd k8s
bash deploy.sh
```

**Nettoyage complet:**
```bash
cd ~/Devops/projet-final-devops/ecodata-platform/k8s && bash cleanup.sh
```

**Accès rapide à l'application:**
```bash
minikube service ecodata-frontend -n ecodata
```

---

## Conclusion

Ce document couvre l'intégralité du processus de déploiement et de maintenance de l'application EcoData Platform. Pour toute question ou problème non documenté, vous pouvez:

1. Consulter les logs des pods avec `kubectl logs`
2. Vérifier les événements du cluster avec `kubectl get events`
3. Consulter la documentation officielle:
   - [Kubernetes Documentation](https://kubernetes.io/docs/)
   - [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
   - [Docker Documentation](https://docs.docker.com/)
   - [FastAPI Documentation](https://fastapi.tiangolo.com/)
   - [Streamlit Documentation](https://docs.streamlit.io/)

**Bonne pratique:** Toujours sauvegarder votre base de données avant une mise à jour majeure ou un redéploiement complet.
