"""
Script utilitaire pour exécuter le notebook depuis le terminal.
Se place automatiquement dans le bon répertoire.
Filtre les messages de démarrage de la JVM (WARN, incubator, etc.)
"""
import json, os, sys, io, re, threading

# Se placer dans le répertoire du script (project final/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# ── Filtrage des logs JVM sur stderr ──
# Les messages parasites arrivent sur stderr avant que Spark ne démarre.
# On les intercepte et on ne laisse passer que les vraies erreurs.
NOISE_PATTERNS = [
    "WARN", "WARNING", "INFO",
    "incubator", "log4j", "JAVA_TOOL_OPTIONS",
    "Setting default log level",
    "adjust logging level",
    "NativeCodeLoader",
    "SparkUI",
    "ConsoleProgressBar",
]

original_stderr = sys.stderr

class FilteredStderr(io.TextIOBase):
    """Redirige stderr en filtrant les lignes de log parasites."""
    def write(self, text):
        for pattern in NOISE_PATTERNS:
            if pattern in text:
                return len(text)  # Avaler la ligne silencieusement
        return original_stderr.write(text)
    def flush(self):
        original_stderr.flush()

sys.stderr = FilteredStderr()

# ── Exécution du notebook ──
NOTEBOOK = "DE2_Project_Notebook_EN.ipynb"
print(f"Exécution du notebook : {NOTEBOOK}")
print(f"Répertoire de travail : {os.getcwd()}")

with open(NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

global_env = {}
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        print(f"\n--- Cellule {i} ---")
        try:
            exec(source, global_env)
        except Exception as e:
            print(f"ERREUR dans la cellule {i}: {e}")
            raise

print("\n=== Notebook exécuté avec succès. ===")
