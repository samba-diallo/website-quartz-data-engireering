import duckdb
import os

# Chemins vers les données Parquet (support local et Docker)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_OUTPUTS = os.environ.get("PARQUET_BASE_PATH", os.path.join(BASE_DIR, "outputs", "project"))
GOLD_PATH = os.path.join(PROJECT_OUTPUTS, "gold")
STREAMING_PATH = os.path.join(PROJECT_OUTPUTS, "streaming")

# Initialisation de la connexion DuckDB (base de données en mémoire pour lire directement du Parquet)
# On utilise read_only=False pour pouvoir créer des vues si nécessaire
con = duckdb.connect(database=':memory:', read_only=False)

def get_db():
    """Retourne la connexion DuckDB"""
    return con

def query_to_dict(query: str) -> list[dict]:
    """Exécute une requête et retourne les résultats sous forme de liste de dictionnaires"""
    try:
        # fetchdf() convertit le résultat en Pandas DataFrame, puis on le transforme en liste de dicts
        return con.execute(query).fetchdf().to_dict(orient="records")
    except Exception as e:
        raise Exception(f"Erreur DuckDB : {str(e)}")
