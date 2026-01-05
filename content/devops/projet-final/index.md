---
title: "index"
publish: true
---

# EcoData Platform 🌍

Plateforme de collecte de données pour le calcul du bilan carbone.

## 📋 Description

EcoData Platform est une application web full-stack permettant aux entreprises, partenaires et particuliers de déposer des fichiers CSV/Excel contenant des données pour le calcul du bilan carbone. L'équipe interne peut ensuite consulter, télécharger et gérer ces fichiers via une interface intuitive.

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│                 │      │                  │      │                 │
│   Streamlit     │─────▶│   FastAPI        │─────▶│   PostgreSQL    │
│   Frontend      │      │   Backend        │      │   Database      │
│   (Port 8501)   │      │   (Port 8000)    │      │   (Port 5432)   │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  File Storage    │
                         │  (uploads/)      │
                         └──────────────────┘
```

## 🛠️ Stack Technique

- **Backend**: Python FastAPI 0.104.1
- **Frontend**: Streamlit 1.28.2
- **Base de données**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.23
- **Containerisation**: Docker & Docker Compose
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

## 📦 Structure du Projet

```
ecodata-platform/
├── backend/
│   ├── main.py              # API REST FastAPI
│   ├── models.py            # Modèles SQLAlchemy
│   ├── database.py          # Configuration DB
│   ├── schemas.py           # Schémas Pydantic
│   ├── requirements.txt     # Dépendances backend
│   └── Dockerfile          # Image Docker backend
├── frontend/
│   ├── app.py              # Application Streamlit
│   ├── requirements.txt    # Dépendances frontend
│   └── Dockerfile          # Image Docker frontend
├── k8s/
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-statefulset.yaml
│   └── secrets-and-pvc.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # Pipeline CI/CD
├── docker-compose.yml      # Orchestration locale
└── README.md
```

## 🚀 Installation et Lancement

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optionnel)
- Kubernetes (pour déploiement en production)

### 1. Installation Locale

#### Configuration PostgreSQL

```bash
# Créer la base de données et l'utilisateur
sudo -u postgres psql
CREATE DATABASE ecodata_db;
CREATE USER ecodata_user WITH PASSWORD 'ecodata_password';
GRANT ALL PRIVILEGES ON DATABASE ecodata_db TO ecodata_user;
\q
```

#### Backend

```bash
cd ecodata-platform/backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scriptsctivate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le backend
python main.py
# ou
uvicorn main:app --reload
```

Le backend sera accessible sur `http://localhost:8000`

#### Frontend

```bash
cd ecodata-platform/frontend

# Installer les dépendances
pip install -r requirements.txt

# Lancer le frontend
streamlit run app.py
```

Le frontend sera accessible sur `http://localhost:8501`

### 2. Déploiement avec Docker Compose

```bash
cd ecodata-platform

# Construire et lancer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

Services disponibles :
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

### 3. Déploiement sur Kubernetes

```bash
cd ecodata-platform/k8s

# Créer le namespace
kubectl apply -f namespace.yaml

# Créer les secrets et PVC
kubectl apply -f secrets-and-pvc.yaml

# Déployer PostgreSQL
kubectl apply -f postgres-statefulset.yaml

# Déployer le backend
kubectl apply -f backend-deployment.yaml

# Déployer le frontend
kubectl apply -f frontend-deployment.yaml

# Vérifier les déploiements
kubectl get pods -n ecodata-platform
kubectl get services -n ecodata-platform
```

## 📡 API Endpoints

### Backend API (FastAPI)

- `GET /` - Page d'accueil de l'API
- `GET /health` - Vérification de santé
- `POST /api/upload` - Upload de fichier CSV/Excel
  - Form data: `file`, `user_type`, `user_name`
- `GET /api/files` - Liste des fichiers
  - Query params: `user_type` (optionnel), `skip`, `limit`
- `GET /api/files/{id}` - Détails d'un fichier
- `DELETE /api/files/{id}` - Supprimer un fichier
- `GET /api/stats` - Statistiques globales

Documentation interactive : `http://localhost:8000/docs`

## 🎯 Fonctionnalités

### Pour les Utilisateurs

1. **Upload de fichiers**
   - Support CSV, Excel (.xlsx, .xls)
   - Types d'utilisateurs : métier, partenaire, particulier
   - Aperçu des données avant upload
   - Métadonnées automatiques (lignes, colonnes)

2. **Dashboard**
   - Statistiques globales
   - Répartition par type d'utilisateur
   - Visualisations graphiques

3. **Gestion des fichiers**
   - Liste filtrable par type
   - Détails de chaque fichier
   - Suppression sécurisée

4. **Statistiques avancées**
   - Évolution des uploads
   - Top fichiers volumineux
   - Analyses temporelles

## 🔒 Sécurité

- Validation des types de fichiers
- Sanitisation des noms de fichiers
- Gestion sécurisée des mots de passe (secrets K8s)
- CORS configuré pour le frontend
- Isolation des containers

## 🧪 Tests

```bash
# Backend tests
cd backend
pytest tests/

# Lint
flake8 .
```

## 📝 Variables d'Environnement

### Backend

- `DATABASE_URL`: URL de connexion PostgreSQL
  - Format: `postgresql://user:password@host:port/database`

### Frontend

- `API_URL`: URL de l'API backend
  - Défaut: `http://localhost:8000`

## 🚦 CI/CD

Le pipeline GitHub Actions effectue :

1. **Tests** : Lint et tests unitaires
2. **Build** : Construction des images Docker
3. **Push** : Publication sur GitHub Container Registry
4. **Deploy** : Déploiement automatique (à configurer)

## 👥 Contributeurs

- Projet final DevOps - ESIEE Paris 2025

## 📄 Licence

© 2025 ESIEE Paris - Projet Académique

## 🆘 Support

Pour toute question ou problème :
1. Vérifier les logs : `docker-compose logs` ou `kubectl logs`
2. Consulter la documentation API : `/docs`
3. Vérifier la connexion PostgreSQL

## 🔄 Mises à jour futures

- [ ] Tests unitaires complets
- [ ] Authentication et autorisation
- [ ] Export des données
- [ ] Notifications email
- [ ] Analyses avancées de bilan carbone
- [ ] Interface d'administration

---

## Documentation Additionnelle

- [[devops/projet-final/docs/DESIGN|Architecture et Design]]
- [[devops/projet-final/docs/VISUAL_ASSETS|Assets Visuels]]

---

## Fichiers de Configuration

### Docker Compose
- [docker-compose.yml](/static/devops/projet-final/docker-compose.yml)

### Kubernetes Manifests
- [backend-deployment.yaml](/static/devops/projet-final/k8s/backend-deployment.yaml)
- [frontend-deployment.yaml](/static/devops/projet-final/k8s/frontend-deployment.yaml)
- [postgres-statefulset.yaml](/static/devops/projet-final/k8s/postgres-statefulset.yaml)
- [namespace.yaml](/static/devops/projet-final/k8s/namespace.yaml)
- [secrets-and-pvc.yaml](/static/devops/projet-final/k8s/secrets-and-pvc.yaml)

---

## Code Source

### Backend (FastAPI)
- [[devops/projet-final/backend/index|Vue d'ensemble Backend]]
- [[devops/projet-final/backend/main|main.py]] (189 lignes)
- [[devops/projet-final/backend/database|database.py]] (32 lignes)
- [[devops/projet-final/backend/models|models.py]] (42 lignes)
- [[devops/projet-final/backend/schemas|schemas.py]] (35 lignes)

### Frontend (Streamlit)
- [[devops/projet-final/frontend/index|Vue d'ensemble Frontend]]
- [[devops/projet-final/frontend/app|app.py]] (489 lignes)

**Total: 787 lignes de code Python**
