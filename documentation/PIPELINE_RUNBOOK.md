# Pipeline GitHub Archive Analytics — Runbook complet

Guide pas à pas pour cloner, configurer, démarrer, vérifier et arrêter le pipeline `Data Engineering 2/project final/`.

**Stack** : Kafka + Spark Structured Streaming + Airflow + FastAPI + Next.js, orchestré par Docker Compose.

---

## 1. Prérequis système

Vérifier que les outils suivants sont installés :

```bash
docker --version                 # >= 20.10
docker-compose --version         # >= 2.0  (ou `docker compose` plugin)
node --version                   # >= 22.x   (uniquement pour build local Quartz)
git --version                    # >= 2.30
```

**Ports requis libres sur la machine hôte** :

| Port | Service |
|---|---|
| 2181 | Zookeeper |
| 9092 | Kafka (broker exposé au host) |
| 8000 | Backend FastAPI |
| 3000 | Frontend Next.js |
| 8080 | Airflow Webserver |
| 8090 | Kafka UI |

Vérifier qu'aucun process ne bloque ces ports :

```bash
sudo lsof -i :2181,9092,8000,3000,8080,8090
```

**Espace disque** : ~5 GB pour les images Docker + le data lake généré.

---

## 2. Cloner le repository

```bash
git clone https://github.com/samba-diallo/website-quartz-data-engireering.git
cd "website-quartz-data-engireering/Data Engineering 2/project final"
```

---

## 3. Configurer l'environnement (`.env`)

Le `docker-compose.yml` lit ses credentials depuis un fichier `.env` local (gitignored, jamais poussé).

**Créer le `.env` depuis le template fourni** :

```bash
cp .env.example .env
```

**Contenu attendu** (édite les valeurs `<change_me>`) :

```env
# Airflow metadata Postgres
POSTGRES_USER=airflow
POSTGRES_PASSWORD=<change_me>
POSTGRES_DB=airflow

# Airflow admin web user (UI sur http://localhost:8080)
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=<change_me>
AIRFLOW_ADMIN_EMAIL=admin@example.com

# Kafka
KAFKA_BOOTSTRAP_SERVERS_INTERNAL=kafka:29092
KAFKA_TOPIC=github.raw.events

# Backend
PARQUET_BASE_PATH=/app/outputs/project

# Frontend (exposé au client — NE JAMAIS y mettre un secret)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **Important** : pour la prod, génère des mots de passe forts (`openssl rand -base64 24`). En local-dev, `admin`/`airflow` suffisent.

---

## 4. Build et démarrage

### 4.1. Build de toutes les images (~ 3-5 min la première fois)

```bash
docker-compose build
```

### 4.2. Lancer toute la stack en arrière-plan

```bash
docker-compose up -d
```

L'option `-d` (detached) rend la main au terminal. Pour suivre les logs en direct, voir la section 6.

### 4.3. Vérifier que tous les containers sont UP

```bash
docker-compose ps
```

Attendu (statut `Up`) :

```
de2_zookeeper            Up
de2_kafka                Up
de2_kafka_ui             Up
de2_kafka_init           Exited (0)   ← normal, c'est un init job one-shot
de2_producer             Exited (0)   ← normal, le producer charge puis termine
de2_spark_bronze         Up
de2_backend              Up
de2_frontend             Up
de2_airflow_db           Up
de2_airflow_init         Exited (0)   ← normal, c'est un init job one-shot
de2_airflow_webserver    Up
de2_airflow_scheduler    Up
```

Si un container est en `Restarting` ou `Exited (1)`, voir la section **Troubleshooting**.

---

## 5. Trajet de la donnée (chronologie au démarrage)

```
1. Zookeeper démarre (coordonne Kafka)
2. Kafka démarre et écoute sur 9092
3. kafka-init crée le topic "github.raw.events"
4. producer télécharge les fichiers GH Archive (.json.gz) et les
   publie dans Kafka topic
5. spark-bronze consomme le topic 24/7 et écrit les events bruts
   dans outputs/project/bronze_v2/*.parquet
6. Airflow scheduler déclenche les DAG batch :
   - DAG Silver : nettoyage et formatage des events bronze → silver
   - DAG Gold   : agrégations (repo_activity, pagerank) → gold
7. Backend FastAPI lit les parquets gold via DuckDB
8. Frontend Next.js fetch /api/analytics/ toutes les 30s
```

---

## 6. URLs de vérification

Une fois la stack démarrée, ouvre ces URLs dans le navigateur :

| URL | Quoi vérifier |
|---|---|
| http://localhost:3000 | **Dashboard Next.js** — chiffres + charts non vides |
| http://localhost:8000/docs | **Backend FastAPI Swagger** — tester `GET /api/analytics/` |
| http://localhost:8000/api/analytics/pipeline-status | **Pipeline status JSON** — bronze/silver/gold non `null` |
| http://localhost:8080 | **Airflow UI** — login avec les creds du `.env` |
| http://localhost:8090 | **Kafka UI** — voir le topic `github.raw.events` avec des messages |

---

## 7. Commandes utiles au quotidien

### 7.1. Suivre les logs d'un service

```bash
docker-compose logs -f backend           # logs backend en live
docker-compose logs -f spark-bronze      # voir le streaming Kafka → Bronze
docker-compose logs -f airflow-scheduler # voir l'orchestration Airflow
docker-compose logs --tail 50 producer   # 50 dernières lignes du producer
```

### 7.2. Redémarrer un seul service

```bash
docker-compose restart backend
```

### 7.3. Rebuild + redéploiement après modification de code

Le code Python est *baked* dans l'image (pas en volume) pour le backend / spark / airflow. Toute modif Python nécessite un rebuild.

```bash
# Backend uniquement
docker-compose build backend
docker rm -f de2_backend                 # force remove (compose stop/rm parfois capricieux)
docker-compose up -d --no-deps backend

# Vérifier que la nouvelle image est utilisée
docker inspect de2_backend --format '{{.Image}}: created {{.Created}}'
```

Le **frontend** a un volume sync (`./frontend-dashboard:/app`), donc **hot-reload Next.js** sans rebuild — sauf si tu modifies `package.json`.

### 7.4. Exécuter une commande dans un container

```bash
# Shell Bash dans le backend
docker exec -it de2_backend bash

# Inspecter le contenu du data lake depuis le backend
docker exec de2_backend ls -la /app/outputs/project/

# Lister les topics Kafka
docker exec de2_kafka kafka-topics --list --bootstrap-server kafka:29092

# Lancer un DAG Airflow manuellement
docker exec de2_airflow_scheduler airflow dags trigger gh_archive_batch
```

### 7.5. Tester un endpoint backend

```bash
curl -s http://localhost:8000/api/analytics/ | python3 -m json.tool
curl -s http://localhost:8000/api/analytics/pipeline-status | python3 -m json.tool
curl -s http://localhost:8000/api/analytics/top-repos?limit=5 | python3 -m json.tool
```

---

## 8. Troubleshooting

### 8.1. `de2_backend` en `Exited (255)`

**Cause** : crash silencieux ou arrêt manuel.
**Fix** : `docker-compose logs --tail 50 backend` pour voir l'erreur, puis `docker-compose restart backend`.

### 8.2. Frontend `Build Error: globals.css line 837`

**Cause** : cache `.next` corrompu, ou ordre des `@import` cassé dans `globals.css`.
**Fix** :
```bash
docker rm -f de2_frontend
docker run --rm -v "$(pwd)/frontend-dashboard:/app" -w /app alpine sh -c "rm -rf .next node_modules/.cache"
docker-compose up -d frontend
```
Vérifier que le fichier `globals.css` a `@import url('Google Fonts')` **AVANT** `@import "tailwindcss"`.

### 8.3. Airflow `Permission denied` sur `logs/scheduler/latest`

**Cause** : le user UID dans le container ≠ ton UID host.
**Fix** :
```bash
sudo chown -R $(id -u):$(id -g) airflow/logs/
```

### 8.4. Airflow montre `All 0 DAGs` ou DAGs en "rouge"

**Cause** : désynchronisation entre la DB Airflow et les fichiers du dossier `dags/`.
**Fix** :
```bash
docker exec de2_airflow_scheduler airflow dags reserialize
```

### 8.5. `ACTIVE DEVELOPERS = 0` dans le dashboard

**Cause** : le dossier `gold/user_activity/` n'a pas été généré par le pipeline Spark/Airflow (seul `repo_activity` existe).
**Fix** : à corriger dans le job Spark Gold. Voir TODO #1 dans `PROJET_JOURNAL.md`.

### 8.6. `Cannot create container — already in use`

**Cause** : un ancien container avec le même nom traîne.
**Fix** :
```bash
docker rm -f de2_backend          # ou le nom concerné
docker-compose up -d
```

### 8.7. Port déjà occupé

```bash
sudo lsof -i :3000                # voir qui occupe
sudo kill <PID>                   # tuer le process
# OU changer le port dans docker-compose.yml
```

### 8.8. Le producer ne charge pas de données

Le producer télécharge un fichier GH Archive (`.json.gz`) au démarrage et termine. C'est normal qu'il soit en `Exited (0)`.

Pour relancer une ingestion manuelle :
```bash
docker-compose up producer
```

### 8.9. Endpoint `/api/analytics/pipeline-status` retourne 404

**Cause** : ancienne image backend sans cet endpoint.
**Fix** : rebuild backend (cf. section 7.3).

---

## 9. Arrêt propre

### 9.1. Stopper tous les services (garde les volumes)

```bash
docker-compose down
```

Les containers sont supprimés mais les **données persistantes restent** :
- `outputs/project/bronze*/silver*/gold*/` (parquets) sur le host
- Volume Docker `airflow_db_data` (metadata Airflow)
- Volume Docker `kafka_data` (offsets, topic data)

### 9.2. Arrêt total + nettoyage des volumes Docker

> **Attention** : efface les metadata Airflow et les offsets Kafka. Les parquets sur le host (`outputs/`) restent intacts.

```bash
docker-compose down -v
```

### 9.3. Nuke complet (rebuild from scratch)

```bash
docker-compose down -v
docker system prune -af --volumes        # nettoie TOUT (autres projets compris)
rm -rf outputs/project/{bronze,silver,gold,streaming,text}*
docker-compose build --no-cache
docker-compose up -d
```

---

## 10. Vérifier la santé du pipeline (script rapide)

Tu peux coller ce bloc dans le terminal après un `docker-compose up -d` :

```bash
echo "=== Containers ===" && docker-compose ps --filter status=running --format "table {{.Name}}\t{{.Status}}"
echo "=== Backend ===" && curl -s -o /dev/null -w "  HTTP %{http_code}\n" http://localhost:8000/api/analytics/
echo "=== Frontend ===" && curl -s -o /dev/null -w "  HTTP %{http_code}\n" http://localhost:3000/
echo "=== Airflow ===" && curl -s -o /dev/null -w "  HTTP %{http_code}\n" http://localhost:8080/
echo "=== Kafka UI ===" && curl -s -o /dev/null -w "  HTTP %{http_code}\n" http://localhost:8090/
echo "=== Pipeline status ===" && curl -s http://localhost:8000/api/analytics/pipeline-status | python3 -m json.tool
```

Tout doit retourner `HTTP 200` et le JSON pipeline-status doit avoir `"active": true` pour bronze/silver/gold.

---

## 11. Pour aller plus loin

- **Architecture détaillée** : voir `Data Engineering 2/project final/PROJET_JOURNAL.md`
- **Sécurité du repo** : voir `documentation/SECURITY_AUDIT.md` (local, gitignored)
- **Site Quartz publié** : https://website-quartz-data-engireering.pages.dev/

---

*Dernière mise à jour : 16 Mai 2026.*
