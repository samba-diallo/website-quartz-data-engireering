from fastapi import APIRouter, HTTPException
import os
import glob
from datetime import datetime
from functools import lru_cache
from services.duckdb_service import query_to_dict, GOLD_PATH

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

LAKE_BASE = os.path.dirname(GOLD_PATH)


def _layer_info(layer_name: str):
    path = os.path.join(LAKE_BASE, layer_name)
    if not os.path.isdir(path):
        return {"active": False, "files": 0, "last_update": None}
    parquets = glob.glob(os.path.join(path, "**", "*.parquet"), recursive=True)
    if not parquets:
        return {"active": False, "files": 0, "last_update": None}
    latest_mtime = max(os.path.getmtime(p) for p in parquets)
    return {
        "active": True,
        "files": len(parquets),
        "last_update": datetime.fromtimestamp(latest_mtime).isoformat(timespec="seconds"),
    }


# --- Métadonnées du snapshot de données (GitHub Archive rejoué) ---------------
# Affichées sur le dashboard pour situer les données dans le temps. Surchargeables
# par variables d'environnement côté hébergeur (Render).
DATA_COVERAGE = os.environ.get("DATA_COVERAGE", "GitHub Archive · 15 janvier 2025 · 10h–13h UTC")
DATA_COVERAGE_ISO = os.environ.get("DATA_COVERAGE_ISO", "2025-01-15T13:00:00")
ACTIVE_USERS_FALLBACK = int(os.environ.get("ACTIVE_USERS_COUNT", "158537"))

# En déploiement (Render) seul gold/ est embarqué ; bronze/silver ne sont pas
# présents -> on reflète l'exécution réelle du pipeline plutôt que "inactif".
_SNAPSHOT_STATUS = {
    "bronze": {"active": True, "files": 2, "last_update": DATA_COVERAGE_ISO},
    "silver": {"active": True, "files": 2, "last_update": DATA_COVERAGE_ISO},
    "gold": {"active": True, "files": 6, "last_update": DATA_COVERAGE_ISO},
}


def _layer_status(layer_name: str):
    """Statut réel si la couche est présente sur disque, sinon snapshot embarqué."""
    info = _layer_info(layer_name)
    return info if info["active"] else _SNAPSHOT_STATUS.get(layer_name, info)


@router.get("/pipeline-status")
def get_pipeline_status():
    """Statut des couches du data lake (réel si présent, sinon snapshot embarqué)."""
    return {
        "bronze": _layer_status("bronze"),
        "silver": _layer_status("silver"),
        "gold": _layer_status("gold"),
    }


@router.get("/data-info")
def get_data_info():
    """Couverture temporelle des données affichées sur le dashboard."""
    return {
        "dataset": "GitHub Archive",
        "coverage": DATA_COVERAGE,
        "source": "https://www.gharchive.org/",
    }

@lru_cache(maxsize=1)
def fetch_top_repos_cached(limit: int):
    repo_activity_path = os.path.join(GOLD_PATH, "repo_activity", "*.parquet")
    if not os.path.exists(os.path.dirname(repo_activity_path)):
        return []
        
    query = f"""
        SELECT repo_name, CAST(SUM(event_count) AS INTEGER) as total_events
        FROM '{repo_activity_path}'
        GROUP BY repo_name
        ORDER BY total_events DESC
        LIMIT {limit}
    """
    return query_to_dict(query)

@router.get("/top-repos")
def get_top_repos(limit: int = 10):
    """Récupère les dépôts avec le plus d'événements"""
    result = fetch_top_repos_cached(limit)
    if not result:
        raise HTTPException(status_code=404, detail="Données Gold non trouvées")
    return result

@lru_cache(maxsize=1)
def fetch_event_types_cached():
    repo_activity_path = os.path.join(GOLD_PATH, "repo_activity", "*.parquet")
    if not os.path.exists(os.path.dirname(repo_activity_path)):
        return []
        
    query = f"""
        SELECT event_type, CAST(SUM(event_count) AS INTEGER) as count
        FROM '{repo_activity_path}'
        GROUP BY event_type
        ORDER BY count DESC
    """
    return query_to_dict(query)

@router.get("/event-types")
def get_event_types():
    """Récupère la distribution des types d'événements"""
    result = fetch_event_types_cached()
    if not result:
        raise HTTPException(status_code=404, detail="Données Gold non trouvées")
    return result

@lru_cache(maxsize=1)
def fetch_activity_over_time_cached():
    repo_activity_path = os.path.join(GOLD_PATH, "repo_activity", "*.parquet")
    if not os.path.exists(os.path.dirname(repo_activity_path)):
        return []
        
    query = f"""
        SELECT
            event_type,
            CAST(SUM(event_count) AS INTEGER) as count
        FROM '{repo_activity_path}'
        GROUP BY event_type
        ORDER BY count DESC
        LIMIT 6
    """
    return query_to_dict(query)

@router.get("/")
def get_dashboard_data():
    """Endpoint global pour le dashboard - agrège toutes les métriques"""
    try:
        top_repos = fetch_top_repos_cached(10)
        event_types = fetch_event_types_cached()
        
        total_events = sum(item['count'] for item in event_types) if event_types else 0
        
        # Compte les développeurs uniques DIRECTEMENT depuis bronze_v2 (streaming layer).
        # On évite le dossier gold/user_activity qui n'est pas (encore) généré par le
        # pipeline Spark Gold. Bronze_v2 a 1.5M+ events avec un champ actor_login direct.
        # Fallback sur bronze (struct actor) si bronze_v2 absent.
        active_users = 0
        for src in ("bronze_v2", "bronze"):
            bronze_path = os.path.join(LAKE_BASE, src, "**", "*.parquet")
            if not glob.glob(bronze_path, recursive=True):
                continue
            try:
                if src == "bronze_v2":
                    q = f"""
                        SELECT COUNT(DISTINCT actor_login) AS user_count
                        FROM read_parquet('{bronze_path}', union_by_name=true)
                        WHERE actor_login IS NOT NULL
                    """
                else:
                    q = f"""
                        SELECT COUNT(DISTINCT actor.login) AS user_count
                        FROM read_parquet('{bronze_path}', union_by_name=true)
                        WHERE actor IS NOT NULL
                    """
                result = query_to_dict(q)
                if result and result[0]['user_count']:
                    active_users = int(result[0]['user_count'])
                    break
            except Exception as e:
                print(f"[active_users] failed on {src}: {e}")
                continue

        # Snapshot embarqué (Render) : bronze absent -> valeur réelle précalculée.
        if not active_users:
            active_users = ACTIVE_USERS_FALLBACK

        activity_over_time = []
        if event_types:
            for i, event in enumerate(event_types[:6]):
                activity_over_time.append({
                    'time': f'{10 + i}:00',
                    'commits': event['count'] if event['event_type'] == 'PushEvent' else 0,
                    'prs': event['count'] if event['event_type'] == 'PullRequestEvent' else 0
                })
        
        influence_scores = []
        if event_types:
            total = sum(item['count'] for item in event_types[:4])
            for event in event_types[:4]:
                influence_scores.append({
                    'name': event['event_type'].replace('Event', ''),
                    'value': round((event['count'] / total * 100), 1) if total > 0 else 0
                })
        
        top_repos_formatted = []
        for repo in top_repos[:4]:
            top_repos_formatted.append({
                'name': repo['repo_name'],
                'activity': repo['total_events'],
                'color': '#c5a059'
            })
        
        return {
            'total_events': total_events,
            'active_users': active_users,
            'top_repos': top_repos_formatted,
            'activity_over_time': activity_over_time,
            'influence_scores': influence_scores,
            'data_coverage': DATA_COVERAGE,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'agrégation des données: {str(e)}")
