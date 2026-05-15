from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation des routeurs
from routers import analytics, streaming, pagerank

app = FastAPI(
    title="GitHub Archive Analytics API", 
    description="API lisant les données du pipeline Spark via DuckDB",
    version="1.0.0"
)

# Configuration CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(analytics.router)
app.include_router(streaming.router)
app.include_router(pagerank.router)

@app.on_event("startup")
def preload_cache():
    """Pré-charge les requêtes analytiques lourdes au démarrage pour éviter les deadlocks de concurrence DuckDB"""
    try:
        from routers.analytics import fetch_top_repos_cached, fetch_event_types_cached
        from routers.pagerank import fetch_pagerank_cached
        print("Pre-loading DuckDB cache...")
        fetch_top_repos_cached(10)
        fetch_event_types_cached()
        fetch_pagerank_cached(10)
        print("Cache loaded successfully.")
    except Exception as e:
        print(f"Erreur lors du pré-chargement du cache : {e}")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bienvenue sur l'API GitHub Archive Analytics", 
        "status": "online",
        "endpoints": [
            "/api/analytics/top-repos",
            "/api/analytics/event-types",
            "/api/streaming/events",
            "/api/graph/pagerank"
        ]
    }
