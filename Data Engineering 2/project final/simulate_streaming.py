"""
simulate_streaming.py — Simule un flux temps réel pour Structured Streaming.

Ce script copie les fichiers .json.gz depuis data/archive/ vers data/landing/
un par un, avec une pause entre chaque fichier. Spark readStream (file source)
détecte chaque nouveau fichier et le traite comme un micro-batch.

Usage : lancer ce script AVANT ou EN PARALLELE de la cellule Streaming du notebook.
"""
import os
import time
import shutil
import glob

# Toujours résoudre les chemins par rapport au répertoire du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ARCHIVE_DIR = os.path.join(SCRIPT_DIR, "data", "archive")
LANDING_DIR = os.path.join(SCRIPT_DIR, "data", "landing")

# Pause entre chaque fichier déposé (en secondes)
PAUSE_SECONDS = 15


def clean_landing(landing_dir):
    """Vide le dossier landing/ pour repartir de zéro."""
    if os.path.exists(landing_dir):
        for f in glob.glob(os.path.join(landing_dir, "*")):
            os.remove(f)
        print(f"Dossier landing/ nettoyé : {landing_dir}")
    os.makedirs(landing_dir, exist_ok=True)


def simulate_stream(archive_dir, landing_dir, pause=PAUSE_SECONDS):
    """
    Copie les fichiers .json.gz un par un dans landing/.
    Spark readStream les détectera comme de nouveaux fichiers.
    """
    clean_landing(landing_dir)

    files = sorted(glob.glob(os.path.join(archive_dir, "*.json.gz")))
    if not files:
        print(f"ERREUR : aucun fichier .json.gz trouvé dans {archive_dir}")
        print("Lancez d'abord download_gh_archive.py pour télécharger les données.")
        return

    print(f"Simulation de streaming : {len(files)} fichier(s) à déposer.")
    print(f"Pause entre chaque fichier : {pause} secondes.\n")

    for i, src in enumerate(files, 1):
        filename = os.path.basename(src)
        dst = os.path.join(landing_dir, filename)
        shutil.copy2(src, dst)
        print(f"[{i}/{len(files)}] Déposé : {filename} dans landing/")

        if i < len(files):
            print(f"  Attente de {pause}s avant le prochain fichier...")
            time.sleep(pause)

    print("\nSimulation terminée. Tous les fichiers ont été déposés.")


if __name__ == "__main__":
    simulate_stream(ARCHIVE_DIR, LANDING_DIR)
