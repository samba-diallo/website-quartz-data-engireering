from fastapi import APIRouter, HTTPException
import os
from services.duckdb_service import query_to_dict, STREAMING_PATH

router = APIRouter(prefix="/api/streaming", tags=["Streaming"])

@router.get("/events")
def get_streaming_events(limit: int = 50):
    """Récupère les événements du Structured Streaming"""
    streaming_path = os.path.join(STREAMING_PATH, "*.parquet")
    
    if not os.path.exists(os.path.dirname(streaming_path)):
        raise HTTPException(status_code=404, detail="Données Streaming non trouvées.")
        
    # On gère le format 'window' complexe de Spark Streaming
    query = f"""
        SELECT 
            window.start as window_start, 
            window."end" as window_end, 
            event_type, 
            event_count
        FROM '{streaming_path}'
        ORDER BY window_start DESC, event_count DESC
        LIMIT {limit}
    """
    return query_to_dict(query)
