# Documentation Déploiement - EcoData Platform

Etudiants : DIALLO Samba & DIOP Mouhamed

## Table des matières
1. [Presentation](#presentation)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Deploiement complet A-Z](#deploiement-complet-a-z)
6. [Choix techniques et architecture](#choix-techniques-et-architecture)
7. [Acces a l'application](#acces-a-lapplication)
8. [Commandes utiles](#commandes-utiles)
9. [Ressources et references](#ressources-et-references)
10. [Role de Claude AI](#role-de-claude-ai-dans-ce-projet)

---

## Presentation

EcoData Platform est une application web pour la gestion de donnees environnementales.

Stack technique :
- Frontend : Streamlit (Python)
- Backend : FastAPI (Python)
- Base de donnees : PostgreSQL 15
- Conteneurisation : Docker
- Reverse Proxy : Nginx
- CI/CD : GitHub Actions

---

## Architecture

```
Internet
  |
  v
Nginx (port 80 - Reverse Proxy)
  |
  +-- Frontend Streamlit (port 8501)
  |
  +-- Backend FastAPI (port 8000)
  |
  +-- PostgreSQL (port 5433)
```

Services Docker :
- ecodata-nginx : Reverse proxy centralise
- ecodata-frontend : Interface utilisateur Streamlit
- ecodata-backend : API REST FastAPI
- ecodata-postgres : Base de donnees PostgreSQL

---

## Prerequisites

Verifier les versions installes :

```bash
docker --version          # Docker 28.2+
docker-compose --version # Docker Compose 1.29+
```

Exigences systeme :
- CPU : 2 cores minimum
- RAM : 4 GB minimum
- Disque : 10 GB libres

---

## Installation

Cloner le repository :

```bash
git clone https://github.com/samba-diallo/Devops.git
cd Devops/projet-final-devops/ecodata-platform
```

Verifier les fichiers essentiels :

```bash
ls -la
# Doit contenir :
# - docker-compose.yml
# - nginx.conf
# - backend/ (avec Dockerfile)
# - frontend/ (avec Dockerfile)
```

---

## Deploiement complet (A-Z)

### Etape 1 : Preparation de l'environnement

```bash
# 1. Cloner le repository
git clone https://github.com/samba-diallo/Devops.git
cd Devops/projet-final-devops/ecodata-platform

# 2. Verifier que Docker est installe et en cours d'execution
docker --version
docker ps  # Doit afficher une liste vide ou les containers actuels

# 3. Verifier la disponibilite des ressources
df -h  # Au moins 10 GB libres
free -h  # Au moins 4 GB RAM disponibles
```

**Explication**: Ces verifications garantissent que votre systeme est pret a accueillir les 4 conteneurs Docker (Nginx, FastAPI, Streamlit, PostgreSQL).

### Etape 2 : Construction des images Docker

```bash
# Les images sont definies dans les Dockerfile de chaque service
# Le fichier docker-compose.yml les construit automatiquement

# Option 1 : Utiliser le script automatique (RECOMMANDE)
chmod +x ../../deploy-docker-compose.sh
../../deploy-docker-compose.sh

# Option 2 : Construire manuellement
docker-compose build --no-cache

# Cette commande :
# - Lit le docker-compose.yml
# - Construit l'image backend (FastAPI)
# - Construit l'image frontend (Streamlit)
# - Cree l'image Nginx a partir de l'image officielle
# - Utilise PostgreSQL officiel
```

**Explication**: La construction crée des images locales. Sans `--no-cache`, Docker reutilise les couches existantes, ce qui est plus rapide lors des rebuilds.

### Etape 3 : Demarrage des conteneurs

```bash
# Demarrer tous les services en arriere-plan (-d = detached)
docker-compose up -d

# Attendre 10-15 secondes pour que les services demarrent
sleep 15

# Verifier que tous les conteneurs sont en cours d'execution
docker-compose ps

# Expected output:
# NAME                COMMAND             SERVICE     STATUS      PORTS
# ecodata-nginx       /docker-...         nginx       Up 30s      0.0.0.0:80->80/tcp
# ecodata-backend     uvicorn main:...    backend     Up 35s      0.0.0.0:8000->8000/tcp
# ecodata-frontend    streamlit run...    frontend    Up 40s      0.0.0.0:8501->8501/tcp
# ecodata-postgres    docker-...          db          Up 45s      0.0.0.0:5433->5432/tcp
```

**Explication**: 
- `-d` = detached mode (services tournent en arriere-plan)
- Le port 80 (Nginx) est seul expose au public
- Les autres ports (8000, 8501, 5433) sont accessibles mais via Nginx

### Etape 4 : Verification du demarrage

```bash
# Verifier la sante de PostgreSQL
docker-compose exec db psql -U ecodata_user -d ecodata_db -c "SELECT version();"

# Expected output: PostgreSQL 15.15 ...

# Verifier que le backend demarre sans erreurs
docker-compose logs backend | tail -20

# Verifier que le frontend demarre sans erreurs
docker-compose logs frontend | tail -20

# Verifier que Nginx a accepte la configuration
docker-compose logs nginx | tail -10
```

**Explication**: Ces verifications detectent les erreurs de demarrage avant de router le traffic utilisateur.

### Etape 5 : Tests de connectivite

```bash
# Test 1 : Nginx reverse proxy
curl -I http://localhost/
# Expected : HTTP/1.1 200 OK

# Test 2 : API Documentation
curl -I http://localhost/docs
# Expected : HTTP/1.1 200 OK

# Test 3 : API Endpoints
curl http://localhost/api/openapi.json | head -20
# Expected : JSON OpenAPI schema

# Test 4 : Base de donnees
docker-compose exec db psql -U ecodata_user -d ecodata_db -c "SELECT COUNT(*) FROM files;"
# Expected : count = 0 (ou le nombre de fichiers existants)
```

**Explication**: Ces tests garantissent que le routing est correctement configure et que tous les services communiquent.

### Etape 6 : Acces a l'application

Ouvrir votre navigateur et aller a :

```
http://localhost/
```

Vous devriez voir :
- L'interface Streamlit (Frontend)
- Un formulaire pour uploader des fichiers CSV/Excel
- Un dashboard avec les statistiques

---

## Choix techniques

Option 1 : Script automatique (recommande)

```bash
cd ~/Devops
chmod +x deploy-docker-compose.sh
./deploy-docker-compose.sh
```

Le script va :
1. Arreter les conteneurs existants
2. Construire les images Docker
3. Demarrer tous les services
4. Afficher l'URL d'acces

Option 2 : Commande manuelle

```bash
cd projet-final-devops/ecodata-platform

# Construire et demarrer
docker-compose up -d

# Verifier l'etat
docker-compose ps

# Voir les logs
docker-compose logs -f
```

---

## Choix techniques et architecture

### Pourquoi Docker Compose et pas Kubernetes pour le developpement local ?

Docker Compose est ideal pour le developpement local car :
- **Simplifie** : Une seule commande `docker-compose up` vs plusieurs `kubectl apply -f`
- **Rapide** : Demarrage en secondes vs quelques minutes pour Kubernetes
- **Ressources** : ~1 GB vs ~3-4 GB pour Minikube/K8s
- **Debugging facile** : `docker-compose logs` vs `kubectl logs`
- **Synchronisation fichiers** : Meilleure integration avec le systeme hote

Kubernetes reste disponible en production (voir le dossier `k8s/` pour les manifests YAML).

### Pourquoi Nginx comme reverse proxy ?

**Avant (sans Nginx)** :
- Frontend : http://localhost:8501
- Backend : http://localhost:8000
- CORS complexe entre deux domaines

**Problemes** :
- Deux URLs differentes = confusing pour les utilisateurs
- Configuration CORS requise
- Architecture non professionnelle

**Solution : Nginx reverse proxy**

```
Client -> http://localhost/ (Port 80 unique)
            |
            v
         Nginx
         /   \   \
        /     \   \
    Frontend  API  Docs
    (8501)   (8000) (8000)
```

**Benefices** :
- **UNE URL unique** pour tout
- **Routage intelligent** : `/` -> Frontend, `/api/` -> Backend, `/docs` -> Swagger
- **WebSocket support** : Streamlit necessite WebSocket
- **Production-ready** : Configuration identique en production

### Pourquoi PostgreSQL 15 et pas SQLite ?

**SQLite** :
- ✓ Aucune installation
- ✗ Pas de concurrence (un seul writer)
- ✗ Limites de taille et performance
- ✗ Pas de replication

**PostgreSQL 15** :
- ✓ Multi-concurrence (lecture/ecriture simultanees)
- ✓ Robuste pour donnees importantes
- ✓ Backup/Recovery professionnel
- ✓ Identique a la production
- ✓ Persistence via volume Docker

**Decision** : PostgreSQL pour mimer l'environnement production.

### Versions specifiques choisies

```
Backend    : FastAPI 0.104.1    (async, validation native)
Frontend   : Streamlit 1.28.2   (interface simple, dashboards)
Database   : PostgreSQL 15      (robuste, moderne)
Proxy      : Nginx latest       (performant, production)
Conteneurs : Docker Compose     (orchestration simple)
```

### Architecture des volumes Docker

```
Host machine
    |
    v
docker-compose.yml (volumes: postgres_data)
    |
    v
Volume persistant "postgres_data"
    |
    v
Container PostgreSQL /var/lib/postgresql/data
```

**Pourquoi un volume nomme ?**
- **Persistence** : Donnees conservees apres `docker-compose down`
- **Backup facile** : `docker volume backup postgres_data`
- **Performance** : Meilleur qu'un bind mount pour les BD

### CI/CD avec GitHub Actions

Fichier : `.github/workflows/ci-cd-ghcr.yml`

```
Git Push vers main
        |
        v
    GitHub Actions
        |
    +---+---+
    |       |
    v       v
  Build   Push a
  Images  GHCR
    |       |
    +---+---+
        |
        v
   Images dispos dans
   GitHub Container Registry
   (deploiement facile)
```

**Workflow** :
1. Chaque push vers `main` declenche la build
2. Images Docker construites (backend + frontend)
3. Pushees vers GHCR (registre de GitHub)
4. Dispos pour deployment : `./deploy-from-ghcr.sh`

---

## Acces a l'application

L'application est accessible sur UNE SEULE URL :

```
http://localhost/
```

Endpoints disponibles :

| URL | Service | Description |
|-----|---------|-------------|
| http://localhost/ | Frontend | Interface Streamlit |
| http://localhost/docs | API Docs | Documentation Swagger |
| http://localhost/api/ | Backend | Endpoints API |

Port PostgreSQL (interne uniquement) :
- localhost:5433 (pour acces direct si necessaire)

---

## Commandes utiles

Gestion des conteneurs :

```bash
# Demarrer les services
docker-compose up -d

# Arreter les services
docker-compose down

# Voir l'etat
docker-compose ps

# Voir les logs en temps reel
docker-compose logs -f

# Logs d'un service specifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

Operations sur la base de donnees :

```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U ecodata_user -d ecodata_db

# Lister les tables
docker-compose exec db psql -U ecodata_user -d ecodata_db -c "\dt"

# Executer une requete SQL
docker-compose exec db psql -U ecodata_user -d ecodata_db -c "SELECT * FROM files;"
```

Nettoyage :

```bash
# Supprimer les conteneurs et volumes
docker-compose down -v

# Nettoyer Docker
docker system prune -a --volumes -f
```

---

## Resolution de problemes

Nginx ne demarre pas :

```bash
# Verifier la configuration
docker-compose exec nginx nginx -t

# Voir les logs
docker-compose logs nginx
```

Base de donnees non accessible :

```bash
# Verifier la sante de PostgreSQL
docker-compose ps

# Verifier les credentials
docker-compose exec db psql -U ecodata_user -d ecodata_db -c "SELECT 1"
```

Espace disque insuffisant :

```bash
# Nettoyer Docker
docker system prune -a --volumes -f

# Verifier l'espace
df -h

# Redemarrer les services
docker-compose down && docker-compose up -d
```

---

## Pipeline CI/CD

Le pipeline GitHub Actions automatise :
1. Tests du code
2. Construction des images Docker
3. Push vers GitHub Container Registry (GHCR)

Declenchement : A chaque push vers main

Workflows : .github/workflows/ci-cd-ghcr.yml

---

## Ressources et references

### Documentation officielle

**Backend (FastAPI)**
- Documentation : https://fastapi.tiangolo.com/
- API Reference : https://fastapi.tiangolo.com/api/
- Tutorial complet : https://fastapi.tiangolo.com/tutorial/
- Validation Pydantic : https://docs.pydantic.dev/

**Frontend (Streamlit)**
- Documentation : https://docs.streamlit.io/
- Composants : https://docs.streamlit.io/library/api-reference
- Gallery d'exemples : https://streamlit.io/gallery
- Streamlit Deployment : https://docs.streamlit.io/deploy

**Base de donnees (PostgreSQL)**
- Documentation : https://www.postgresql.org/docs/15/
- Tutorials : https://www.postgresql.org/docs/15/tutorial.html
- SQL Reference : https://www.postgresql.org/docs/15/sql.html

**Conteneurisation (Docker)**
- Docker Documentation : https://docs.docker.com/
- Docker Compose : https://docs.docker.com/compose/
- Best Practices : https://docs.docker.com/develop/dev-best-practices/

**Reverse Proxy (Nginx)**
- Documentation : https://nginx.org/en/docs/
- Configuration Guide : https://nginx.org/en/docs/http/ngx_http_core_module.html
- Proxy Setup : https://nginx.org/en/docs/http/ngx_http_proxy_module.html

### Repositories GitHub

**Projet principal**
- Repository : https://github.com/samba-diallo/Devops
- EcoData Platform : https://github.com/samba-diallo/Devops/tree/main/projet-final-devops/ecodata-platform

**Images et CI/CD**
- GitHub Container Registry (GHCR) : ghcr.io/samba-diallo/devops/
- CI/CD Workflow : .github/workflows/ci-cd-ghcr.yml

### Outils et references techniques

**Orchestration**
- Docker Compose : https://docs.docker.com/compose/
- Kubernetes (pour production) : https://kubernetes.io/docs/

**Debogage et logs**
- Docker Logs : `docker-compose logs -f`
- PostgreSQL Logs : `docker-compose logs db`
- Nginx Logs : `docker-compose logs nginx`

**Testing et Validation**
- Pytest (Python) : https://docs.pytest.org/
- FastAPI Testing : https://fastapi.tiangolo.com/tutorial/testing/

---

## Role de Claude AI dans ce projet

Claude a aide a plusieurs aspects techniques critiques du deploiement :

**Architecture et decisions techniques** : Claude a fourni une analyse comparative detaillee entre Docker Compose et Kubernetes pour le developpement local, expliquant pourquoi Compose est superieur en termes de complexite, ressources et vitesse de mise en place. De meme, le choix d'ajouter Nginx comme reverse proxy a ete justifie par Claude en exposant les problemes de CORS et la necessity d'une URL unique pour une meilleure experience utilisateur.

**Configuration Nginx** : Le fichier `nginx.conf` a ete genere avec une comprehension des requirements specifiques du projet (routes `/api/`, `/docs`, support WebSocket pour Streamlit, proxy headers corrects). Claude a explique chaque bloc de configuration pour clarifier le routing et la communication entre services.

**Debogage et troubleshooting** : Lors des problemes de disk space (99% full), de Docker snap corruption, et d'erreurs de demarrage Minikube, Claude a systematiquement guide vers les solutions appropriees avec des commandes diagnostiques et des explications des causes racines plutot que des solutions superficielles.

**Documentation complete** : Cette documentation a ete structuree par Claude pour couvrir le deploiement complet A-Z avec explications techniques a chaque etape, permettant a tout developpeur de reproduced l'installation sans ambiguite et de comprendre pourquoi chaque choix technique a ete fait.

**Scripts d'automatisation** : Le script `deploy-docker-compose.sh` a ete concu pour automatiser l'ensemble du processus de build et deployment avec verifications sanitaires et affichage clair du statut final.

En resume, Claude a transformation un projet Kubernetes complexe et instable en une solution Docker Compose robuste, bien documentee et facilement reproductible, tout en conservant la flexibilite de passer a Kubernetes en production.

---

## Notes importantes

- Les donnees PostgreSQL persistent dans le volume Docker
- Nginx est le point d'entree unique
- Les ports internes (8000, 8501, 5432) ne sont pas exposes directement
- Seul le port 80 (Nginx) est expose publiquement

---
