# Imports nécessaires pour l'API FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from datetime import datetime
import pandas as pd

# Import des modules locaux
from database import get_db, engine
import models
import schemas

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="EcoData Platform API",
    description="API for carbon footprint data collection and management",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les headers
)

# Dossier pour stocker les fichiers uploadés
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Route racine - Page d'accueil de l'API
@app.get("/")
def read_root():
    return {
        "message": "Welcome to EcoData Platform API",
        "version": "1.0.0",
        "status": "active"
    }

# Route de vérification de santé de l'API
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Route pour uploader un fichier CSV ou Excel
@app.post("/api/upload", response_model=schemas.FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),  # Fichier à uploader
    user_type: str = "metier",     # Type d'utilisateur (metier, partenaire, particulier)
    user_name: str = "anonymous",  # Nom de l'utilisateur
    db: Session = Depends(get_db)  # Session de base de données
):
    # Vérification de l'extension du fichier
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are allowed"
        )
    
    # Création d'un nom de fichier sécurisé avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{user_type}_{user_name}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # Sauvegarde du fichier sur le disque
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Récupération de la taille du fichier
    file_size = os.path.getsize(file_path)
    
    # Lecture du fichier pour obtenir le nombre de lignes et colonnes
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        rows_count = len(df)
        columns_count = len(df.columns)
    except Exception as e:
        rows_count = 0
        columns_count = 0
    
    # Enregistrement des métadonnées dans la base de données
    db_file = models.UploadedFile(
        filename=file.filename,
        stored_filename=safe_filename,
        file_path=file_path,
        file_size=file_size,
        user_type=user_type,
        user_name=user_name,
        rows_count=rows_count,
        columns_count=columns_count
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "message": "File uploaded successfully",
        "upload_date": db_file.upload_date,
        "file_size": file_size,
        "rows_count": rows_count
    }

# Route pour lister tous les fichiers uploadés avec filtres optionnels
@app.get("/api/files", response_model=List[schemas.FileInfo])
def list_files(
    user_type: str = None,  # Filtre par type d'utilisateur (optionnel)
    skip: int = 0,          # Nombre d'éléments à sauter (pagination)
    limit: int = 100,       # Nombre maximum d'éléments à retourner
    db: Session = Depends(get_db)
):
    query = db.query(models.UploadedFile)
    
    # Application du filtre par type d'utilisateur si fourni
    if user_type:
        query = query.filter(models.UploadedFile.user_type == user_type)
    
    # Récupération des fichiers avec pagination, triés par date décroissante
    files = query.order_by(models.UploadedFile.upload_date.desc()).offset(skip).limit(limit).all()
    return files

# Route pour obtenir les informations d'un fichier spécifique
@app.get("/api/files/{file_id}", response_model=schemas.FileInfo)
def get_file_info(file_id: int, db: Session = Depends(get_db)):
    # Recherche du fichier dans la base de données
    file = db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

# Route pour supprimer un fichier
@app.delete("/api/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    # Recherche du fichier dans la base de données
    file = db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Suppression du fichier physique si il existe
    if os.path.exists(file.file_path):
        os.remove(file.file_path)
    
    # Suppression de l'entrée dans la base de données
    db.delete(file)
    db.commit()
    
    return {"message": "File deleted successfully"}

# Route pour obtenir les statistiques globales
@app.get("/api/stats")
def get_statistics(db: Session = Depends(get_db)):
    # Nombre total de fichiers
    total_files = db.query(models.UploadedFile).count()
    
    # Répartition des fichiers par type d'utilisateur
    files_by_type = db.query(
        models.UploadedFile.user_type,
        db.func.count(models.UploadedFile.id)
    ).group_by(models.UploadedFile.user_type).all()
    
    # Taille totale occupée par tous les fichiers
    total_size = db.query(
        db.func.sum(models.UploadedFile.file_size)
    ).scalar() or 0
    
    return {
        "total_files": total_files,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "files_by_type": {user_type: count for user_type, count in files_by_type}
    }

# Point d'entrée pour lancer le serveur en mode développement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
