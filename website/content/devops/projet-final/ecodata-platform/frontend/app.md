---
title: "Frontend - app.py"
publish: true
---

# Frontend - app.py

Application Streamlit complète pour l'interface utilisateur (489 lignes).

## Code Source

```python
# Imports nécessaires pour l'interface Streamlit
import streamlit as st # Framework pour créer l'interface web
import requests # Pour communiquer avec l'API backend
import pandas as pd # Pour manipuler et afficher les données tabulaires
from datetime import datetime
import os

# URL de l'API backend FastAPI
# Utilise la variable d'environnement API_URL si disponible (pour Docker), sinon localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configuration de la page Streamlit
st.set_page_config(
 page_title="EcoData Platform", # Titre de l'onglet du navigateur
 page_icon="🌍", # Icône de l'onglet
 layout="wide", # Utilise toute la largeur de l'écran
 initial_sidebar_state="expanded"
)

# CSS personnalisé pour une ambiance écologique
st.markdown("""
 <style>
 .main {
 background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
 }
 .stApp {
 background: linear-gradient(to bottom, #e3f2fd, #f1f8e9);
 }
 h1 {
 color: #2e7d32;
 text-align: center;
 font-size: 3em;
 margin-bottom: 0;
 }
 .subtitle {
 text-align: center;
 color: #558b2f;
 font-size: 1.3em;
 font-style: italic;
 margin-bottom: 30px;
 }
 .quote {
 background: linear-gradient(120deg, #a5d6a7, #81c784);
 padding: 20px;
 border-radius: 10px;
 margin: 20px 0;
 border-left: 5px solid #2e7d32;
 color: #1b5e20;
 font-size: 1.1em;
 box-shadow: 0 4px 6px rgba(0,0,0,0.1);
 }
 .stButton>button {
 background-color: #4caf50;
 color: white;
 border-radius: 8px;
 }
 .stButton>button:hover {
 background-color: #45a049;
 }
 </style>
""", unsafe_allow_html=True)

# En-tête avec image de fond et titre
st.markdown("""
 <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); 
 border-radius: 15px; margin-bottom: 30px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
 <h1 style='color: white; margin: 0; font-size: 3.5em;'>🌍 EcoData Platform</h1>
 <p style='color: #e8f5e9; font-size: 1.5em; margin-top: 10px; font-style: italic;'>
 "Agir aujourd'hui pour préserver demain"
 </p>
 <p style='color: white; font-size: 1.1em; margin-top: 5px;'>
 Plateforme collaborative de collecte de données pour le calcul du bilan carbone
 </p>
 </div>
""", unsafe_allow_html=True)

# Menu de navigation dans la barre latérale
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
st.sidebar.markdown("### 🌱 Navigation")
menu = st.sidebar.selectbox(
 "Choisissez une section :",
 ["🏠 Accueil", "📤 Déposer des Données", " Tableau de Bord", "📂 Mes Fichiers", " Analyses"],
 label_visibility="collapsed"
)

# ============================================
# PAGE ACCUEIL
# ============================================
if menu == "🏠 Accueil":
 # Message de bienvenue
 st.markdown("""
 <div class='quote'>
 <h2 style='color: #1b5e20; text-align: center;'>🌿 Bienvenue sur EcoData Platform</h2>
 <p style='text-align: center; font-size: 1.2em;'>
 Ensemble, mesurons notre impact pour mieux le réduire !
 </p>
 </div>
 """, unsafe_allow_html=True)
 
 # Description de la plateforme
 col1, col2 = st.columns(2)
 
 with col1:
 st.markdown("""
 ### Notre Mission
 
 Faciliter la collecte et l'analyse des données environnementales pour :
 
 - 🌱 **Calculer** votre empreinte carbone
 - **Visualiser** vos émissions de CO₂
 - **Identifier** les axes d'amélioration
 - 🌍 **Agir** pour un avenir durable
 
 > *"Chaque donnée partagée est un pas vers un avenir plus vert"*
 """)
 
 with col2:
 st.markdown("""
 ### 🤝 Comment ça marche ?
 
 1. **📤 Déposez vos données** : Fichiers CSV ou Excel
 2. ** Nous analysons** : Calcul automatique des indicateurs
 3. ** Consultez les résultats** : Tableaux de bord interactifs
 4. ** Passez à l'action** : Recommandations personnalisées
 
 > *"Mesurer pour mieux agir, agir pour mieux préserver"*
 """)
 
 # Statistiques en temps réel
 st.markdown("---")
 st.markdown("### Impact de la Communauté")
 
 try:
 response = requests.get(f"{API_URL}/api/stats")
 if response.status_code == 200:
 stats = response.json()
 
 col1, col2, col3, col4 = st.columns(4)
 
 with col1:
 st.metric(
 label="🌍 Fichiers analysés",
 value=stats['total_files'],
 help="Nombre total de fichiers déposés"
 )
 
 with col2:
 st.metric(
 label=" Données collectées",
 value=f"{stats['total_size_mb']} MB",
 help="Volume total de données traitées"
 )
 
 with col3:
 files_by_type = stats.get('files_by_type', {})
 st.metric(
 label="👥 Contributeurs actifs",
 value=len(files_by_type),
 help="Nombre de types d'utilisateurs"
 )
 
 with col4:
 st.metric(
 label="🌱 Impact positif",
 value="En cours",
 help="CO₂ évité grâce à nos actions"
 )
 except:
 st.info(" Connectez-vous pour voir les statistiques en temps réel")
 
 # Call to action
 st.markdown("---")
 st.markdown("""
 <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #81c784, #66bb6a); 
 border-radius: 15px; margin-top: 30px;'>
 <h2 style='color: white;'> Prêt à contribuer ?</h2>
 <p style='color: white; font-size: 1.2em;'>
 Déposez vos premières données et découvrez votre impact environnemental !
 </p>
 </div>
 """, unsafe_allow_html=True)

# ============================================
# PAGE 1: UPLOAD DE FICHIERS
# ============================================
elif menu == "📤 Déposer des Données":
 st.markdown("""
 <div class='quote'>
 <h3>🌱 Partagez vos données, construisons ensemble un avenir durable</h3>
 <p><em>"Chaque fichier déposé nous rapproche d'une planète plus verte"</em></p>
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 ### 📋 Instructions
 Déposez vos fichiers de données (CSV ou Excel) contenant vos émissions, consommations ou activités.
 Nous les analyserons pour calculer votre empreinte carbone.
 """)
 
 st.header("📤 Téléversement de fichiers")
 
 # Formulaire pour saisir les informations de l'utilisateur
 col1, col2 = st.columns(2)
 
 with col1:
 # Sélection du type d'utilisateur
 user_type = st.selectbox(
 "Type d'utilisateur",
 ["metier", "partenaire", "particulier"]
 )
 
 with col2:
 # Saisie du nom de l'utilisateur
 user_name = st.text_input("Nom", "")
 
 # Widget pour sélectionner un fichier à uploader
 uploaded_file = st.file_uploader(
 "Choisir un fichier CSV ou Excel",
 type=['csv', 'xlsx', 'xls']
 )
 
 # Si un fichier a été sélectionné
 if uploaded_file is not None:
 st.info(f"Fichier sélectionné: {uploaded_file.name}")
 
 # Afficher un aperçu du contenu du fichier
 try:
 # Lire le fichier selon son extension
 if uploaded_file.name.endswith('.csv'):
 df_preview = pd.read_csv(uploaded_file)
 else:
 df_preview = pd.read_excel(uploaded_file)
 
 # Afficher les 10 premières lignes
 st.write("Aperçu des données:")
 st.dataframe(df_preview.head(10))
 st.write(f"Nombre de lignes: {len(df_preview)}")
 st.write(f"Nombre de colonnes: {len(df_preview.columns)}")
 
 # Repositionner le curseur au début du fichier pour l'upload
 uploaded_file.seek(0)
 except Exception as e:
 st.error(f"Erreur lors de la lecture du fichier: {str(e)}")
 
 # Bouton pour envoyer le fichier à l'API
 if st.button("Téléverser"):
 if not user_name:
 st.error("Veuillez entrer votre nom")
 else:
 try:
 # Préparer les données pour la requête POST
 files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
 data = {"user_type": user_type, "user_name": user_name}
 
 # Envoyer le fichier à l'API backend
 response = requests.post(
 f"{API_URL}/api/upload",
 files=files,
 data=data
 )
 
 # Afficher le résultat de l'upload
 if response.status_code == 200:
 result = response.json()
 st.success(f" {result['message']}")
 st.json(result)
 else:
 st.error(f"Erreur: {response.text}")
 except Exception as e:
 st.error(f"Erreur de connexion: {str(e)}")


# ============================================
# PAGE 2: DASHBOARD
# ============================================
elif menu == " Tableau de Bord":
 st.markdown("""
 <div class='quote'>
 <h3> Visualisez votre impact environnemental en temps réel</h3>
 <p><em>"Voir pour comprendre, comprendre pour agir"</em></p>
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 ### 🌍 Vue d'ensemble
 Découvrez les statistiques globales et suivez l'évolution de votre empreinte carbone.
 """)
 
 st.header(" Tableau de Bord")
 
 # Récupérer les statistiques globales depuis l'API
 try:
 response = requests.get(f"{API_URL}/api/stats")
 if response.status_code == 200:
 stats = response.json()
 
 # Afficher les métriques principales en 3 colonnes
 col1, col2, col3 = st.columns(3)
 
 with col1:
 st.metric("Total Fichiers", stats['total_files'])
 
 with col2:
 st.metric("Taille Totale", f"{stats['total_size_mb']} MB")
 
 with col3:
 files_by_type = stats.get('files_by_type', {})
 st.metric("Types d'utilisateurs", len(files_by_type))
 
 # Afficher un graphique de répartition par type d'utilisateur
 if files_by_type:
 st.subheader("Répartition par type d'utilisateur")
 df_types = pd.DataFrame(
 list(files_by_type.items()),
 columns=['Type', 'Nombre']
 )
 st.bar_chart(df_types.set_index('Type'))
 except Exception as e:
 st.error(f"Erreur de connexion à l'API: {str(e)}")


# ============================================
# PAGE 3: GESTION DES FICHIERS
# ============================================
elif menu == "📂 Mes Fichiers":
 st.markdown("""
 <div class='quote'>
 <h3>📂 Gérez vos contributions à la transition écologique</h3>
 <p><em>"Organisez vos données, optimisez votre impact"</em></p>
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 ### 🗂️ Vos données
 Consultez, filtrez et gérez l'ensemble de vos fichiers déposés sur la plateforme.
 """)
 
 st.header("📂 Gestion des fichiers")
 
 # Filtre pour afficher les fichiers par type d'utilisateur
 user_type_filter = st.selectbox(
 "Filtrer par type d'utilisateur",
 ["Tous", "metier", "partenaire", "particulier"]
 )
 
 # Récupérer la liste des fichiers depuis l'API
 try:
 params = {}
 if user_type_filter != "Tous":
 params['user_type'] = user_type_filter
 
 response = requests.get(f"{API_URL}/api/files", params=params)
 
 if response.status_code == 200:
 files = response.json()
 
 if files:
 # Créer un DataFrame pandas pour afficher les données
 df = pd.DataFrame(files)
 
 # Formater la date
 df['upload_date'] = pd.to_datetime(df['upload_date']).dt.strftime('%Y-%m-%d %H:%M')
 
 # Convertir la taille en MB
 df['file_size_mb'] = (df['file_size'] / (1024 * 1024)).round(2)
 
 # Sélectionner les colonnes à afficher
 display_df = df[[
 'id', 'filename', 'user_type', 'user_name',
 'rows_count', 'file_size_mb', 'upload_date'
 ]]
 
 # Renommer les colonnes pour l'affichage
 display_df.columns = [
 'ID', 'Fichier', 'Type', 'Utilisateur',
 'Lignes', 'Taille (MB)', 'Date'
 ]
 
 # Afficher le tableau
 st.dataframe(display_df, use_container_width=True)
 
 # Section pour supprimer un fichier
 st.subheader("Actions")
 file_id_to_delete = st.number_input(
 "ID du fichier à supprimer",
 min_value=1,
 step=1
 )
 
 if st.button("Supprimer"):
 # Envoyer une requête DELETE à l'API
 delete_response = requests.delete(
 f"{API_URL}/api/files/{file_id_to_delete}"
 )
 if delete_response.status_code == 200:
 st.success("Fichier supprimé avec succès")
 st.rerun() # Recharger la page
 else:
 st.error("Erreur lors de la suppression")
 else:
 st.info("Aucun fichier trouvé")
 except Exception as e:
 st.error(f"Erreur de connexion: {str(e)}")


# ============================================
# PAGE 4: STATISTIQUES DÉTAILLÉES
# ============================================
elif menu == " Analyses":
 st.markdown("""
 <div class='quote'>
 <h3> Analyses approfondies pour un impact mesurable</h3>
 <p><em>"Des données précises pour des décisions éclairées"</em></p>
 </div>
 """, unsafe_allow_html=True)
 
 st.markdown("""
 ### 🔬 Analyses détaillées
 Explorez en profondeur les tendances, évolutions et performances environnementales.
 """)
 
 st.header(" Statistiques détaillées")
 
 # Récupérer tous les fichiers pour créer des statistiques détaillées
 try:
 response = requests.get(f"{API_URL}/api/files")
 
 if response.status_code == 200:
 files = response.json()
 
 if files:
 df = pd.DataFrame(files)
 df['upload_date'] = pd.to_datetime(df['upload_date'])
 
 # Graphique 1: Évolution des uploads dans le temps
 st.subheader("Évolution des uploads")
 df['date'] = df['upload_date'].dt.date
 uploads_by_date = df.groupby('date').size()
 st.line_chart(uploads_by_date)
 
 # Graphique 2: Distribution par type d'utilisateur
 st.subheader("Distribution par type d'utilisateur")
 user_type_counts = df['user_type'].value_counts()
 st.bar_chart(user_type_counts)
 
 # Tableau: Top 10 des fichiers les plus volumineux
 st.subheader("Top 10 fichiers les plus volumineux")
 top_files = df.nlargest(10, 'file_size')[
 ['filename', 'user_name', 'file_size', 'rows_count']
 ]
 # Convertir la taille en MB
 top_files['file_size_mb'] = (top_files['file_size'] / (1024 * 1024)).round(2)
 st.dataframe(top_files[['filename', 'user_name', 'file_size_mb', 'rows_count']])
 else:
 st.info("Aucune donnée disponible")
 except Exception as e:
 st.error(f"Erreur: {str(e)}")

# ============================================
# PIED DE PAGE DE LA BARRE LATÉRALE
# ============================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
 <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #a5d6a7, #81c784); 
 border-radius: 10px; margin-top: 20px;'>
 <h3 style='color: #1b5e20; margin: 0;'>🌍 EcoData Platform</h3>
 <p style='color: #2e7d32; margin: 5px 0;'><strong>Version 1.0.0</strong></p>
 <p style='color: #1b5e20; font-size: 0.9em; font-style: italic;'>
 "Ensemble pour une planète durable"
 </p>
 <p style='color: #2e7d32; margin-top: 10px; font-size: 0.8em;'>
 © 2025 ESIEE Paris<br>
 🌱 Chaque donnée compte
 </p>
 </div>
""", unsafe_allow_html=True)

# Citation écologique aléatoire
import random
quotes = [
 "🌿 La nature ne fait rien en vain",
 "🌍 Soyez le changement que vous voulez voir",
 "♻️ Réduire, réutiliser, recycler",
 "🌱 Chaque geste compte pour notre planète",
 "💚 Protégeons notre maison commune",
 "🌊 L'eau, l'air, la terre : notre héritage"
]
st.sidebar.info(random.choice(quotes))

```

## Télécharger

[Télécharger app.py](/static/devops/projet-final/frontend/app.py)
