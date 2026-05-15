from fastapi import FastAPI, HTTPException
import duckdb
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GitHub Archive Analytics API", description="API lisant les données Gold via DuckDB")

# Configuration CORS pour autoriser le frontend (Next.js) à faire des requêtes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En développement on autorise tout
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemins relatifs vers les données Parquet (on suppose qu'on lance depuis le dossier backend/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD_PATH = os.path.join(BASE_DIR, "outputs", "project", "gold")

# Initialisation de la connexion DuckDB (base de données en mémoire)
con = duckdb.connect(database=':memory:', read_only=False)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API GitHub Archive Analytics", "status": "online"}

@app.get("/api/health")
def health_check():
    """Vérifie si les fichiers Parquet sont accessibles par DuckDB"""
    repo_activity_path = os.path.join(GOLD_PATH, "repo_activity", "*.parquet")
    try:
        # On vérifie juste qu'on peut lire la table
        count = con.execute(f"SELECT COUNT(*) FROM '{repo_activity_path}'").fetchone()[0]
        return {"status": "ok", "gold_records_found": count}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/api/analytics/top-repos")
def get_top_repos(limit: int = 10):
    """Récupère les dépôts avec le plus d'activité globale"""
    repo_activity_path = os.path.join(GOLD_PATH, "repo_activity", "*.parquet")
    try:
        query = f"""
            SELECT repo_name, SUM(event_count) as total_events
            FROM '{repo_activity_path}'
            GROUP BY repo_name
            ORDER BY total_events DESC
            LIMIT {limit}
        """
        # Exécution de la requête et conversion en liste de dictionnaires
        results = con.execute(query).fetchdf().to_dict(orient="records")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
