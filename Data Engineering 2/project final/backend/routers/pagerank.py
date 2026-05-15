from fastapi import APIRouter, HTTPException
import os
from functools import lru_cache
from services.duckdb_service import query_to_dict, GOLD_PATH

router = APIRouter(prefix="/api/graph", tags=["PageRank"])

@lru_cache(maxsize=1)
def fetch_pagerank_cached(limit: int):
    pagerank_path = os.path.join(GOLD_PATH, "pagerank", "*.parquet")
    if not os.path.exists(os.path.dirname(pagerank_path)):
        return []
        
    query = f"""
        SELECT src as node_name, rank as influence_score
        FROM '{pagerank_path}'
        ORDER BY rank DESC
        LIMIT {limit}
    """
    return query_to_dict(query)

@router.get("/pagerank")
def get_pagerank(limit: int = 10):
    """Récupère les résultats du modèle PageRank (Noeuds les plus influents)"""
    result = fetch_pagerank_cached(limit)
    if not result:
        raise HTTPException(status_code=404, detail="Modèle PageRank non trouvé")
    return result
