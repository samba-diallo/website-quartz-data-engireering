import urllib.request
import os
import time
import glob

def clean_large_files(output_dir):
    """Supprime les anciens fichiers pour s'assurer que Spark repart de zéro."""
    print("Nettoyage des anciens fichiers de données existants...")
    for ext in ["*.json.gz", "*.json"]:
        for f in glob.glob(os.path.join(output_dir, ext)):
            try:
                os.remove(f)
                print(f"  - Supprimé : {os.path.basename(f)}")
            except Exception as e:
                print(f"  - Impossible de supprimer {os.path.basename(f)}")

def download_files(output_dir, year="2024", month="01", day="01", hours=4):
    """
    Télécharge plusieurs fichiers horaires et les conserve au format .json.gz
    """
    os.makedirs(output_dir, exist_ok=True)
    clean_large_files(output_dir)
    
    for hour in range(hours):
        filename = f"{year}-{month}-{day}-{hour}.json.gz"
        url = f"https://data.gharchive.org/{filename}"
        temp_path = os.path.join(output_dir, filename)

        print(f"Téléchargement de {filename} ({url}) ...", end="", flush=True)
        try:
            t0 = time.time()
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req) as response, open(temp_path, 'wb') as out_file:
                out_file.write(response.read())
            t1 = time.time()
            print(f" Fait ! en {t1-t0:.1f} s")
        except Exception as e:
            print(f" Erreur : {e}")
            
if __name__ == "__main__":
    # Toujours résoudre les chemins par rapport au répertoire du script
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(SCRIPT_DIR, "data", "archive")
    
    # On télécharge 2 fichiers horaires complets (sans échantillonnage)
    download_files(output_directory, hours=2)
    
    os.makedirs(os.path.join(SCRIPT_DIR, "data", "landing"), exist_ok=True)
    print("Dossiers d'ingestion et fichiers JSON.GZ prêts pour Spark !")

