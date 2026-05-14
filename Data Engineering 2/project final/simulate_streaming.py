import os
import time
import shutil
import glob

def simulate_streaming(archive_dir="data/archive", landing_dir="data/landing", interval_sec=10, max_files=5):
    """
    Simule un flux de données temps réel en copiant périodiquement des fichiers 
    depuis archive/ vers landing/ pour que Spark Structured Streaming puisse les lire.
    """
    print(f"--- Démarrage du Simulateur de Streaming ---")
    print(f"Dossier source : {archive_dir}")
    print(f"Dossier cible (atterrissage) : {landing_dir}")
    print(f"Intervalle : {interval_sec} secondes")
    
    os.makedirs(landing_dir, exist_ok=True)
    
    # Récupérer un fichier source (notre échantillon)
    source_files = glob.glob(os.path.join(archive_dir, "*.json.gz"))
    if not source_files:
        print(f"Erreur : Aucun fichier .json.gz trouvé dans {archive_dir}.")
        print("Veuillez d'abord lancer download_gh_archive.py !")
        return
        
    source_file = source_files[0]
    
    for i in range(1, max_files + 1):
        target_filename = f"stream_batch_{i}.json.gz"
        target_path = os.path.join(landing_dir, target_filename)
        
        print(f"[{time.strftime('%H:%M:%S')}] Simulation : Arrivée du fichier {target_filename}...")
        shutil.copy2(source_file, target_path)
        
        if i < max_files:
            print(f"Attente de {interval_sec} secondes avant le prochain lot...")
            time.sleep(interval_sec)
            
    print("--- Simulation terminée ---")

if __name__ == "__main__":
    simulate_streaming()
