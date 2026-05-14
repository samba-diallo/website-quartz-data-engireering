import urllib.request
import os
import time
import gzip
import glob

def clean_large_files(output_dir):
    """Supprime les fichiers json et json.gz pour s'assurer que Spark ne lit pas de vieux gros fichiers."""
    print("Nettoyage des anciens fichiers de données existants...")
    for ext in ["*.json.gz", "*.json"]:
        for f in glob.glob(os.path.join(output_dir, ext)):
            try:
                os.remove(f)
                print(f"  - Supprimé : {os.path.basename(f)}")
            except Exception as e:
                print(f"  - Impossible de supprimer {os.path.basename(f)} (Peut-être verrouillé par Spark ?)")

def download_and_extract_sample(output_dir, year="2024", month="01", day="01", hour=0, num_lines=1000):
    """
    Télécharge 1 fichier, extrait un petit échantillon et le sauvegarde en JSON NON COMPRESSÉ.
    """
    os.makedirs(output_dir, exist_ok=True)
    clean_large_files(output_dir)
    
    filename = f"{year}-{month}-{day}-{hour}.json.gz"
    # Nouveau nom de fichier SANS .gz à la fin
    sample_filename = f"sample_{num_lines}_{year}{month}{day}_{hour}.json"
    
    url = f"https://data.gharchive.org/{filename}"
    temp_path = os.path.join(output_dir, filename)
    sample_path = os.path.join(output_dir, sample_filename)

    print(f"Téléchargement du fichier temporaire : {url} ...", end="", flush=True)
    try:
        t0 = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response, open(temp_path, 'wb') as out_file:
            out_file.write(response.read())
        t1 = time.time()
        print(f" Fait ! en {t1-t0:.1f} s")
        
        print(f"Création d'un mini-échantillon NON COMPRESSÉ de {num_lines} événements...", end="", flush=True)
        # Extraire N lignes et sauvegarder en texte brut (pas de gzip pour f_out)
        with gzip.open(temp_path, 'rt', encoding='utf-8') as f_in:
            with open(sample_path, 'w', encoding='utf-8') as f_out:
                for i, line in enumerate(f_in):
                    if i >= num_lines:
                        break
                    f_out.write(line)
        print(" Fait !")
        
        # Supprimer le gros fichier temporaire
        os.remove(temp_path)
        print(f"Gros fichier temporaire supprimé. Fichier final créé : {sample_filename}")

    except Exception as e:
        print(f" Erreur : {e}")
            
if __name__ == "__main__":
    output_directory = "data/archive"
    
    # On crée un échantillon de 1000 événements décompressé
    download_and_extract_sample(output_directory, num_lines=1000)
    
    os.makedirs("data/landing", exist_ok=True)
    print("Dossiers d'ingestion et échantillon pur JSON prêts !")
