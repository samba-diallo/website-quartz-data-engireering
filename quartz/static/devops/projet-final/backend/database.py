# Imports pour la gestion de la connexion à la base de données
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Classe de base pour tous les modèles SQLAlchemy
Base = declarative_base()

# URL de connexion à PostgreSQL
# Format: postgresql://utilisateur:motdepasse@hôte:port/nom_base
# Utilise la variable d'environnement DATABASE_URL si disponible, sinon localhost
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://ecodata_user:ecodata_password@localhost:5432/ecodata_db"
)

# Création du moteur SQLAlchemy pour se connecter à PostgreSQL
engine = create_engine(DATABASE_URL)

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction de dépendance pour obtenir une session de base de données
# Utilisée par FastAPI pour injecter la connexion DB dans les routes
def get_db():
    db = SessionLocal()  # Crée une nouvelle session
    try:
        yield db  # Fournit la session à la route
    finally:
        db.close()  # Ferme la session après utilisation
