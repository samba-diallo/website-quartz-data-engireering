---
title: "Backend - models.py"
publish: true
---

# Backend - models.py

Modèles SQLAlchemy pour User et FileUpload (42 lignes).

## Code Source

```python
# Imports pour la définition du modèle de base de données
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from datetime import datetime
from database import Base

# Modèle représentant un fichier uploadé dans la base de données
class UploadedFile(Base):
    __tablename__ = "uploaded_files"  # Nom de la table dans PostgreSQL
    
    # Clé primaire auto-incrémentée
    id = Column(Integer, primary_key=True, index=True)
    
    # Nom original du fichier uploadé par l'utilisateur
    filename = Column(String, index=True)
    
    # Nom du fichier stocké sur le serveur (avec timestamp pour unicité)
    stored_filename = Column(String, unique=True)
    
    # Chemin complet vers le fichier sur le système de fichiers
    file_path = Column(String)
    
    # Taille du fichier en octets
    file_size = Column(BigInteger)
    
    # Type d'utilisateur (metier, partenaire, particulier)
    user_type = Column(String, index=True)
    
    # Nom de l'utilisateur qui a uploadé le fichier
    user_name = Column(String)
    
    # Nombre de lignes dans le fichier CSV/Excel
    rows_count = Column(Integer, default=0)
    
    # Nombre de colonnes dans le fichier CSV/Excel
    columns_count = Column(Integer, default=0)
    
    # Date et heure de l'upload
    upload_date = Column(DateTime, default=datetime.now)
    
    # Représentation textuelle de l'objet pour le débogage
    def __repr__(self):
        return f"<UploadedFile(id={self.id}, filename={self.filename})>"
```

## Télécharger

[Télécharger models.py](/static/devops/projet-final/backend/models.py)
