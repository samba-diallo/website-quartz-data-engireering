---
title: "Backend - schemas.py"
publish: true
---

# Backend - schemas.py

Schémas Pydantic pour validation des données (35 lignes).

## Code Source

```python
# Imports pour la validation et la sérialisation des données avec Pydantic
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schéma de réponse après l'upload d'un fichier
# Retourné par l'API pour confirmer le succès de l'upload
class FileUploadResponse(BaseModel):
    id: int               # ID du fichier dans la base de données
    filename: str         # Nom original du fichier
    message: str          # Message de confirmation
    upload_date: datetime # Date et heure de l'upload
    file_size: int        # Taille du fichier en octets
    rows_count: int       # Nombre de lignes dans le fichier
    
    # Configuration Pydantic pour permettre la conversion depuis les modèles SQLAlchemy
    class Config:
        from_attributes = True  # Permet de créer un schéma depuis un objet ORM

# Schéma complet d'information sur un fichier
# Utilisé pour lister et afficher les détails d'un fichier
class FileInfo(BaseModel):
    id: int                  # ID unique du fichier
    filename: str            # Nom original du fichier
    stored_filename: str     # Nom stocké avec timestamp
    file_size: int           # Taille en octets
    user_type: str           # Type d'utilisateur (metier, partenaire, particulier)
    user_name: str           # Nom de l'utilisateur
    rows_count: int          # Nombre de lignes
    columns_count: int       # Nombre de colonnes
    upload_date: datetime    # Date et heure de l'upload
    
    # Configuration Pydantic pour permettre la conversion depuis les modèles SQLAlchemy
    class Config:
        from_attributes = True  # Permet de créer un schéma depuis un objet ORM
```

## Télécharger

[Télécharger schemas.py](/static/devops/projet-final/backend/schemas.py)
