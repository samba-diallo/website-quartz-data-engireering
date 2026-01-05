---
title: "TD4 - Application Node.js Simple"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Node.js et NPM - Application Exemple

Ce dossier contient:

* **`app.js`**: Une application Node.js "Hello, World" qui écoute sur le port 8080.
* **`package.json`**: Configuration de build NPM pour l'application Node.js.
* **`Dockerfile`**: Instructions pour packager l'application Node.js comme image Docker.

## Structure du Projet

```
sample-app/
├── app.js                  # Application Node.js simple
├── package.json            # Dépendances et scripts NPM
├── Dockerfile              # Configuration Docker
├── build-docker-image.sh   # Script de construction d'image
└── run-in-docker.sh        # Script d'exécution Docker
```

## Fichiers Téléchargeables

- [app.js](/static/devops/td4/scripts/sample-app/app.js)
- [package.json](/static/devops/td4/scripts/sample-app/package.json)
- [Dockerfile](/static/devops/td4/scripts/sample-app/Dockerfile)
- [build-docker-image.sh](/static/devops/td4/scripts/sample-app/build-docker-image.sh)
- [run-in-docker.sh](/static/devops/td4/scripts/sample-app/run-in-docker.sh)

## Utilisation Locale

### Installation des dépendances
```bash
npm install
```

### Exécution de l'application
```bash
node app.js
```

L'application sera disponible sur http://localhost:8080

## Utilisation avec Docker

### Construction de l'image
```bash
chmod +x build-docker-image.sh
./build-docker-image.sh
```

Ou manuellement:
```bash
docker build -t sample-app:latest .
```

### Exécution du conteneur
```bash
chmod +x run-in-docker.sh
./run-in-docker.sh
```

Ou manuellement:
```bash
docker run -d -p 8080:8080 --name sample-app sample-app:latest
```

### Test de l'application
```bash
curl http://localhost:8080
```

## Détails Techniques

### app.js
Application Node.js minimale utilisant le module HTTP natif. Répond "Hello, World!" à toutes les requêtes sur le port 8080.

### package.json
Définit les métadonnées du projet et les dépendances NPM (aucune dépendance externe dans cette version simple).

### Dockerfile
Image multi-stage pour optimiser la taille:
- Base: Node.js officielle
- Copie des fichiers sources
- Installation des dépendances
- Exposition du port 8080
- Commande de démarrage

## Concepts Clés

1. **Application Node.js**: Serveur HTTP simple sans framework
2. **Conteneurisation**: Empaquetage de l'application avec ses dépendances
3. **Port Mapping**: Exposition du port 8080 du conteneur vers l'hôte
4. **Scripts Shell**: Automatisation des tâches Docker courantes

## Évolution

Cette application de base sert de fondation pour:
- **sample-app-express**: Version avec Express.js
- **sample-app-express-with-tests**: Version avec tests Jest
- Déploiements dans des environnements de production
