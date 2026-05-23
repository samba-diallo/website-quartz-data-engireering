import duckdb
import os

# Chemins vers les données Parquet (support local et Docker)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Source des données, par ordre de priorité :
#   1) PARQUET_BASE_PATH si défini (docker-compose local : volume avec tout le lake)
#   2) le bundle Gold embarqué backend/data/project (déploiement Render sans volume)
#   3) le data lake local outputs/project (dev hors Docker)
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BUNDLED_OUTPUTS = os.path.join(_BACKEND_DIR, "data", "project")
_DEFAULT_OUTPUTS = _BUNDLED_OUTPUTS if os.path.isdir(_BUNDLED_OUTPUTS) else os.path.join(BASE_DIR, "outputs", "project")
PROJECT_OUTPUTS = os.environ.get("PARQUET_BASE_PATH", _DEFAULT_OUTPUTS)
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
