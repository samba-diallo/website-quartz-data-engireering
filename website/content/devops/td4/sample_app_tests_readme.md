---
title: "TD4 - Application Express avec Tests"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Application Node.js avec Express et Tests Jest

Application Node.js avancée utilisant Express.js avec une suite de tests complète utilisant Jest et Supertest.

## Contenu du Projet

* **`app.js`**: Application Express.js avec routes configurables
* **`server.js`**: Point d'entrée du serveur
* **`app.test.js`**: Suite de tests Jest
* **`package.json`**: Configuration NPM avec scripts de test
* **`Dockerfile`**: Image Docker multi-stage optimisée
* **`views/`**: Templates EJS pour le rendu HTML

## Structure

```
sample-app-express-with-tests/
├── app.js              # Application Express
├── server.js           # Serveur HTTP
├── app.test.js         # Tests Jest
├── package.json        # Dépendances et scripts
├── Dockerfile          # Configuration Docker
├── build-docker-image.sh   # Script de construction
├── coverage/           # Rapports de couverture de tests
└── views/              # Templates EJS
    └── index.ejs       # Template de page d'accueil
```

## Fichiers Téléchargeables

- [app.js](/static/devops/td4/scripts/sample-app-express-with-tests/app.js)
- [server.js](/static/devops/td4/scripts/sample-app-express-with-tests/server.js)
- [app.test.js](/static/devops/td4/scripts/sample-app-express-with-tests/app.test.js)
- [package.json](/static/devops/td4/scripts/sample-app-express-with-tests/package.json)
- [Dockerfile](/static/devops/td4/scripts/sample-app-express-with-tests/Dockerfile)

## Installation

```bash
npm install
```

## Développement

### Démarrer le serveur
```bash
npm start
```

L'application démarre sur http://localhost:8080

### Exécuter les tests
```bash
npm test
```

### Couverture de code
```bash
npm run test:coverage
```

Génère un rapport de couverture dans `coverage/`

### Mode Watch (développement)
```bash
npm run test:watch
```

Ré-exécute les tests automatiquement lors des modifications

## Tests Inclus

### Tests Fonctionnels
- **GET /**: Répond avec status 200 et "Hello, World!"
- **GET /health**: Endpoint de health check
- **GET /version**: Retourne la version de l'application
- **404 Handling**: Gestion des routes inconnues

### Tests de Sécurité
- Validation des headers
- Protection contre les injections
- Gestion des erreurs

### Tests de Performance
- Temps de réponse acceptable
- Gestion de charge concurrente

## Utilisation avec Docker

### Construction
```bash
chmod +x build-docker-image.sh
./build-docker-image.sh
```

Ou:
```bash
docker build -t sample-app-express-tests:latest .
```

### Exécution
```bash
docker run -d -p 8080:8080 --name app-tests sample-app-express-tests:latest
```

### Tests dans Docker
```bash
docker run --rm sample-app-express-tests:latest npm test
```

## Intégration CI/CD

Cette application est configurée pour l'intégration continue:

### GitHub Actions
```yaml
- name: Install dependencies
  run: npm ci
  
- name: Run tests
  run: npm test
  
- name: Generate coverage
  run: npm run test:coverage
  
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

### Scripts Disponibles

- `npm start`: Démarre le serveur
- `npm test`: Exécute les tests une fois
- `npm run test:watch`: Mode watch pour les tests
- `npm run test:coverage`: Génère le rapport de couverture
- `npm run lint`: Vérifie le style de code

## Dépendances Principales

### Production
- **express**: Framework web minimal et flexible
- **ejs**: Moteur de templates
- **morgan**: Logger HTTP

### Développement
- **jest**: Framework de test
- **supertest**: Tests HTTP
- **eslint**: Linter JavaScript

## Couverture de Tests

Objectif: 80% de couverture de code minimum

- Statements: 85%
- Branches: 80%
- Functions: 90%
- Lines: 85%

## Bonnes Pratiques Démontrées

1. **Séparation des Préoccupations**: app.js vs server.js
2. **Tests Unitaires**: Vérification de chaque endpoint
3. **Tests d'Intégration**: Tests end-to-end avec Supertest
4. **Couverture de Code**: Suivi de la qualité des tests
5. **CI/CD Ready**: Configuration pour pipelines automatisés
6. **Dockerfile Optimisé**: Build multi-stage pour image légère
7. **Documentation**: README complet et commentaires dans le code

## Débogage

### Logs
```bash
DEBUG=app:* npm start
```

### Tests Spécifiques
```bash
npm test -- --testNamePattern="GET /"
```

### Mode Verbose
```bash
npm test -- --verbose
```

## Évolution et Améliorations

Cette application démontre:
- Tests automatisés robustes
- Prête pour l'intégration continue
- Architecture scalable
- Bonnes pratiques DevOps

Prochaines étapes:
- Déploiement sur Kubernetes
- Monitoring avec Prometheus
- Logs centralisés avec ELK
- Stratégies de déploiement avancées (Blue/Green, Canary)
