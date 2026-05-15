from fastapi import APIRouter, HTTPException
import os
from functools import lru_cache
from services.duckdb_service import query_to_dict, GOLD_PATH

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

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
