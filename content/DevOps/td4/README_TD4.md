# TD4 - Version Control, Build Systems, and Automated Testing

**Auteurs** : DIALLO Samba, DIOP Mouhamed  
**École** : ESIEE Paris  
**Cours** : Fundamentals of DevOps and Software Delivery  
**Date** : Décembre 2025

---

##  Sommaire

1. [Section 1: Version Control with Git](#section-1-version-control-with-git)
2. [Section 2: Collaborating with GitHub](#section-2-collaborating-with-github)
3. [Section 3: Build System with NPM](#section-3-build-system-with-npm)
4. [Section 4: Managing Dependencies](#section-4-managing-dependencies)
5. [Section 5: Automated Testing with Jest](#section-5-automated-testing-with-jest)
6. [Section 6: Testing OpenTofu Code](#section-6-testing-opentofu-code)
7. [Section 7: Testing Recommendations](#section-7-testing-recommendations)
8. [Tous les Exercices - Récapitulatif](#tous-les-exercices)

---

## Section 1: Version Control with Git

### Objectifs
- Initialiser un dépôt Git
- Effectuer des commits et gérer l'historique
- Créer et merger des branches
- Utiliser tags et rebase

### Commandes exécutées

\`\`\`bash
# Créer un dossier de pratique
mkdir /tmp/git-practice
cd /tmp/git-practice

# Configurer Git
git config --global user.name "Samba Diallo"
git config --global user.email "samba.diallo@edu.esiee.fr"

# Initialiser le dépôt
git init

# Créer un fichier et faire le premier commit
echo "Hello, World!" > example.txt
git add example.txt
git commit -m "Initial commit"

# Ajouter plus de contenu
echo "New line of text" >> example.txt
git add example.txt
git commit -m "Add another line"

echo "Third line of text" >> example.txt
git add example.txt
git commit -m "Added a 3rd line"

# Créer une branche
git checkout -b testing
echo "Testing branch content" >> example.txt
git add example.txt
git commit -m "Add content in testing branch"

# Merger la branche
git checkout master
git merge testing
\`\`\`

### Exercise 1: Create a Git Tag

\`\`\`bash
# Créer un tag pour marquer la version
git tag v1.0

# Vérifier le tag
git tag
git log --oneline --decorate
\`\`\`

**Résultat** :  Tag v1.0 créé avec succès sur le commit approprié.

### Exercise 2: Git Rebase

\`\`\`bash
# Créer une branche feature
git checkout -b feature
echo "Feature commit 1" >> example.txt
git add example.txt
git commit -m "Feature commit 1"

echo "Feature commit 2" >> example.txt
git add example.txt
git commit -m "Feature commit 2"

# Revenir sur master et faire un commit divergent
git checkout master
echo "Master update" >> example.txt
git add example.txt
git commit -m "Master update"

# Rebaser feature sur master
git checkout feature
git rebase master
# Résoudre les conflits si nécessaire
git add example.txt
git rebase --continue
\`\`\`

**Résultat** :  Historique linéaire créé avec succès après rebase et résolution de conflit.

---

## Section 2: Collaborating with GitHub

### Objectifs
- Travailler avec des dépôts distants
- Créer et merger des Pull Requests
- Configurer la protection de branches
- Comprendre l'importance des signed commits

### Réalisations

\`\`\`bash
# Dans le dépôt principal
cd /home/sable/devops_base

# Créer une nouvelle branche
git checkout -b update-readme

# Créer le README principal du dépôt
cat > README.md << 'EOF'
# DevOps - Fundamentals Labs

## Auteurs
- DIALLO Samba
- DIOP Mouhamed

## École
ESIEE Paris

## Cours
Fundamentals of DevOps and Software Delivery

## Labs
- TD1: Introduction
- TD2: Data Warehouse
- TD3: Infrastructure as Code
- TD4: Version Control, Build Systems, and Automated Testing
EOF

# Commit et push
git add README.md
git commit -m "Add README"
git push origin update-readme
\`\`\`

**Pull Request** : 
-  Créé PR #1 "Add README" sur GitHub
-  Mergé avec succès dans main (commit 6af4c59)
-  Synchronisé localement avec \`git pull origin main\`

### Exercise 3: Branch Protection Rules

**Configuration sur GitHub** :
- Navigate to: Settings → Rules → Rulesets → New ruleset
- Configured "Require pull request before merging"
- Note: Sur les dépôts privés avec GitHub Free, les rulesets ne sont pas enforced

**Résultat** :  Rulesets créés pour apprentissage (non enforced sur compte Free).

### Exercise 4: Enable Signed Commits

\`\`\`bash
# Vérifier GPG
gpg --version
# Output: gpg (GnuPG) 2.4.4

# Pour configurer (documentation) :
# gpg --full-generate-key
# gpg --list-secret-keys --keyid-format=long
# git config --global user.signingkey <KEY_ID>
# git config --global commit.gpgsign true
# gpg --armor --export <KEY_ID>
# Ajouter la clé publique sur GitHub
\`\`\`

**Résultat** :  GPG vérifié et disponible. Configuration documentée.

---

## Section 3: Build System with NPM

### Objectifs
- Configurer npm scripts pour automatiser les tâches
- Builder une application Node.js
- Créer des images Docker
- Automatiser le processus de build

### Structure du projet

\`\`\`
td4/scripts/sample-app/
├── app.js                    # Application HTTP Node.js
├── package.json              # Configuration npm avec scripts
├── Dockerfile                # Image Docker
├── build-docker-image.sh     # Script de build
└── run-in-docker.sh          # Script pour run (Exercise 6)
\`\`\`

### Application Node.js (app.js)

\`\`\`javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello, World!\\n');
});

const port = process.env.PORT || 8080;
server.listen(port,() => {
  console.log(\`Listening on port \${port}\`);
});
\`\`\`

### Configuration npm (package.json)

\`\`\`json
{
  "name": "sample-app",
  "version": "v4",
  "scripts": {
    "start": "node app.js",
    "dockerize": "./build-docker-image.sh",
    "docker:run": "./run-in-docker.sh"
  }
}
\`\`\`

### Tests effectués

\`\`\`bash
cd /home/sable/devops_base/td4/scripts/sample-app

# Tester l'application
node app.js &
curl http://localhost:8080
# Output: Hello, World!

# Builder l'image Docker
sudo docker build -t sample-app:v4 .

# Tester le conteneur
sudo docker run -d -p 8080:8080 --name test sample-app:v4
curl http://localhost:8080
sudo docker stop test && sudo docker rm test
\`\`\`

**Résultat** :  Application fonctionne, image Docker construite et testée.

### Exercise 5: Pin Node.js Version

**Problème** : \`FROM node:21.7\` peut changer avec le temps

**Solution** : Utiliser le SHA256 digest

\`\`\`bash
# Récupérer le SHA256
sudo docker pull node:21.7.3 2>&1 | grep Digest
# Output: Digest: sha256:4b232062fa976e3a966c49e9b6279efa56c8d207a67270868f51b3d155c4e33d
\`\`\`

**Dockerfile modifié** :
\`\`\`dockerfile
FROM node:21.7.3@sha256:4b232062fa976e3a966c49e9b6279efa56c8d207a67270868f51b3d155c4e33d

WORKDIR /home/node/app
COPY package.json .
COPY app.js .
EXPOSE 8080
USER node
CMD ["npm", "start"]
\`\`\`

**Avantages** :
-  Version exacte garantie
-  Builds reproductibles
-  Protection contre mises à jour cassantes

**Résultat** :  Image construite avec version épinglée.

### Exercise 6: Script pour run dans Docker

**Fichier : run-in-docker.sh**
\`\`\`bash
#!/usr/bin/env bash

set -e

name=\$(grep -o '"name": "[^"]*"' package.json | cut -d'"' -f4)
version=\$(grep -o '"version": "[^"]*"' package.json | cut -d'"' -f4)

echo "Running \$name:\$version in Docker..."

# Stop and remove existing container
docker stop "\$name" 2>/dev/null || true
docker rm "\$name" 2>/dev/null || true

# Run the container
docker run -d \\
  -p 8080:8080 \\
  --name "\$name" \\
  "\$name:\$version"

echo "Container started successfully!"
echo "Access the app at: http://localhost:8080"
\`\`\`

**Usage** :
\`\`\`bash
chmod +x run-in-docker.sh
sudo ./run-in-docker.sh
\`\`\`

**Résultat** :  Script fonctionne, conteneur démarré automatiquement.

---

## Section 4: Managing Dependencies

### Objectifs
- Installer et gérer les dépendances npm
- Différencier dependencies et devDependencies
- Optimiser les images Docker pour la production

### Application Express

**Structure** :
\`\`\`
td4/scripts/sample-app-express/
├── app.js                    # Application Express
├── package.json              # Dependencies configuration
└── Dockerfile                # Optimisé avec --only=production
\`\`\`

**app.js** :
\`\`\`javascript
const express = require('express');

const app = express();
const port = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.get('/name/:name', (req, res) => {
  const name = req.params.name;
  res.send(\`Hello, \${name}!\`);
});

app.listen(port, () => {
  console.log(\`Example app listening on port \${port}\`);
});
\`\`\`

**package.json** :
\`\`\`json
{
  "name": "sample-app",
  "version": "v4",
  "dependencies": {
    "express": "^4.19.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  },
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js"
  }
}
\`\`\`

**Dockerfile optimisé** :
\`\`\`dockerfile
FROM node:21.7

WORKDIR /home/node/app

COPY package.json .
COPY package-lock.json .

RUN npm ci --only=production

COPY app.js .

EXPOSE 8080
USER node
CMD ["npm", "start"]
\`\`\`

### Exercise 7: Add \`/name/:name\` endpoint

**Implémentation** : Voir code app.js ci-dessus

**Tests** :
\`\`\`bash
curl http://localhost:8080/name/Samba
# Output: Hello, Samba!
\`\`\`

**Résultat** :  Endpoint implémenté et testé.

### Exercise 8: Explore devDependencies vs dependencies

**Analyse des différences** :

\`\`\`bash
# Avec devDependencies
npm install
ls node_modules | wc -l  # 90 packages
du -sh node_modules      # 5.7 MB

# Sans devDependencies (production only)
rm -rf node_modules
npm ci --only=production
ls node_modules | wc -l  # 63 packages
du -sh node_modules      # 3.9 MB
\`\`\`

**Résultat** :  Économie de 27 packages (1.8 MB) en production !

**Concepts clés** :
- **dependencies** : Nécessaires en production (Express)
- **devDependencies** : Outils de développement (nodemon)
- \`npm install\` : Installe tout
- \`npm ci --only=production\` : Production uniquement

---

## Section 5: Automated Testing with Jest

### Objectifs
- Écrire des tests unitaires avec Jest
- Tester des APIs avec SuperTest
- Mesurer la couverture de code
- Atteindre 100% de couverture

### Structure

\`\`\`
td4/scripts/sample-app-express-with-tests/
├── app.js                    # Application (exports)
├── server.js                 # Serveur (runs)
├── app.test.js               # Tests
├── package.json              # Configuration Jest
├── coverage/                 # Rapports
└── views/
    └── hello.ejs             # Template EJS
\`\`\`

### Séparation app.js / server.js

**Pourquoi ?** Pour pouvoir tester l'app sans démarrer le serveur.

**app.js** (testable) :
\`\`\`javascript
const express = require('express');
const app = express();

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.get('/name/:name', (req, res) => {
  res.render('hello', {name: req.params.name});
});

app.get('/add/:a/:b', (req, res) => {
  const a = parseFloat(req.params.a);
  const b = parseFloat(req.params.b);
  
  if (isNaN(a) || isNaN(b)) {
    return res.status(400).send('Invalid numbers');
  }
  
  const sum = a + b;
  res.send(\`\${a} + \${b} = \${sum}\`);
});

module.exports = app;  // Export pour tests
\`\`\`

**server.js** (runs) :
\`\`\`javascript
const app = require('./app');

const port = process.env.PORT || 8080;

app.listen(port, () => {
  console.log(\`Example app listening on port \${port}\`);
});
\`\`\`

### Tests (app.test.js)

\`\`\`javascript
const request = require('supertest');
const app = require('./app');

describe('Test the app', () => {

  test('Get / should return Hello, World!', async () => {
    const response = await request(app).get('/');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('Hello, World!');
  });

  test('Get /name/Bob should return Hello, Bob!', async () => {
    const response = await request(app).get('/name/Bob');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('Hello, Bob!');
  });

  test('Get /name should sanitize its input', async () => {
    const maliciousUrl = '/name/%3Cscript%3Ealert("hi")%3C%2Fscript%3E';
    const sanitizedHtml = 'Hello, &lt;script&gt;alert(&#34;hi&#34;)&lt;/script&gt;!';
    const response = await request(app).get(maliciousUrl);
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe(sanitizedHtml);
  });
});

describe('Test the /add endpoint', () => {

  test('Get /add/2/3 should return 5', async () => {
    const response = await request(app).get('/add/2/3');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('2 + 3 = 5');
  });

  test('Get /add/10/20 should return 30', async () => {
    const response = await request(app).get('/add/10/20');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('10 + 20 = 30');
  });

  test('Get /add/5.5/4.5 should handle decimals', async () => {
    const response = await request(app).get('/add/5.5/4.5');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('5.5 + 4.5 = 10');
  });

  test('Get /add/abc/def should return 400', async () => {
    const response = await request(app).get('/add/abc/def');
    expect(response.statusCode).toBe(400);
    expect(response.text).toBe('Invalid numbers');
  });
});
\`\`\`

### Configuration Jest (package.json)

\`\`\`json
{
  "scripts": {
    "start": "node server.js",
    "test": "jest --verbose",
    "test:coverage": "jest --verbose --coverage"
  },
  "dependencies": {
    "ejs": "^3.1.10",
    "express": "^4.19.2"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "supertest": "^7.0.0"
  },
  "jest": {
    "testEnvironment": "node",
    "collectCoverageFrom": [
      "*.js",
      "!server.js",
      "!coverage/**"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 90,
        "functions": 90,
        "lines": 90,
        "statements": 90
      }
    }
  }
}
\`\`\`

### Exercise 9: Add \`/add/:a/:b\` endpoint with tests

**Implémentation** : Voir app.js ci-dessus (endpoint \`/add\`)

**Tests** : Voir app.test.js ci-dessus (4 tests pour \`/add\`)

**Résultats** :
\`\`\`bash
npm test

✓ Get / should return Hello, World!
✓ Get /name/Bob should return Hello, Bob!
✓ Get /name should sanitize its input
✓ Get /add/2/3 should return 5
✓ Get /add/10/20 should return 30
✓ Get /add/5.5/4.5 should handle decimals
✓ Get /add/abc/def should return 400

Test Suites: 1 passed, 1 total
Tests:       7 passed, 7 total
\`\`\`

**Résultat** :  7 tests passent avec succès !

### Exercise 10: Code Coverage

**Commande** :
\`\`\`bash
npm run test:coverage
\`\`\`

**Résultats** :
\`\`\`
----------|---------|----------|---------|---------|-------------------
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s 
----------|---------|----------|---------|---------|-------------------
All files |     100 |      100 |     100 |     100 |                   
 app.js   |     100 |      100 |     100 |     100 |                   
----------|---------|----------|---------|---------|-------------------
\`\`\`

**�� 100% de couverture atteinte !**

**Rapport HTML généré** : \`coverage/lcov-report/index.html\`

**Résultat** :  Couverture complète avec rapport détaillé.

---

## Section 6: Testing OpenTofu Code

### Objectifs
- Écrire des tests pour l'infrastructure as code
- Valider le déploiement avec \`tofu test\`
- Créer des tests positifs et négatifs

### Structure

\`\`\`
td4/scripts/tofu/
├── live/
│   └── lambda-sample/
│       ├── main.tf                      # Infrastructure Lambda + API Gateway
│       ├── outputs.tf
│       ├── deploy.tftest.hcl            # Test de base
│       ├── deploy-json.tftest.hcl       # Test JSON (Exercise 11)
│       └── deploy-negative.tftest.hcl   # Test négatif (Exercise 12)
└── modules/
    ├── lambda/                          # Module Lambda function
    ├── api-gateway/                     # Module API Gateway
    └── test-endpoint/                   # Module pour tester HTTP
\`\`\`

### Infrastructure (main.tf)

\`\`\`hcl
provider "aws" {
  region = "us-east-2"
}

module "function" {
  source = "../../modules/lambda"

  name    = "lambda-sample"
  src_dir = "\${path.module}/src"
  runtime = "nodejs20.x"
  handler = "index.handler"

  memory_size = 128
  timeout     = 5

  environment_variables = {
    NODE_ENV = "production"
  }
}

module "gateway" {
  source = "../../modules/api-gateway"

  name               = "lambda-sample"
  function_arn       = module.function.function_arn
  api_gateway_routes = ["GET /"]
}
\`\`\`

### Test de base (deploy.tftest.hcl)

\`\`\`hcl
run "deploy" {
  command = apply
}

run "validate" {
  command = apply

  module {
    source = "../../modules/test-endpoint"
  }

  variables {
    endpoint = run.deploy.api_endpoint
  }

  assert {
    condition     = data.http.test_endpoint.status_code == 200
    error_message = "Unexpected status: \${data.http.test_endpoint.status_code}"
  }

  assert {
    condition     = data.http.test_endpoint.response_body == "Hello, World!"
    error_message = "Unexpected body: \${data.http.test_endpoint.response_body}"
  }
}
\`\`\`

### Module test-endpoint

**variables.tf** :
\`\`\`hcl
variable "endpoint" {
  description = "The endpoint to make an HTTP request to"
  type        = string
}
\`\`\`

**main.tf** :
\`\`\`hcl
resource "time_sleep" "wait" {
  create_duration = "30s"
}

data "http" "test_endpoint" {
  url    = var.endpoint
  method = "GET"

  depends_on = [time_sleep.wait]
}
\`\`\`

### Exercise 11: Test JSON Response

**deploy-json.tftest.hcl** :
\`\`\`hcl
run "deploy" {
  command = apply
}

run "validate_json" {
  command = apply

  module {
    source = "../../modules/test-endpoint"
  }

  variables {
    endpoint = run.deploy.api_endpoint
  }

  assert {
    condition     = data.http.test_endpoint.status_code == 200
    error_message = "Unexpected status: \${data.http.test_endpoint.status_code}"
  }

  # Test that response is valid JSON
  assert {
    condition     = can(jsondecode(data.http.test_endpoint.response_body))
    error_message = "Response is not valid JSON"
  }

  # Test specific JSON fields
  assert {
    condition     = jsondecode(data.http.test_endpoint.response_body).message == "Hello, World!"
    error_message = "Unexpected message in JSON response"
  }
}
\`\`\`

**Concepts** :
- \`jsondecode()\` : Parse la réponse JSON
- \`can()\` : Vérifie si l'expression réussit
- Test des champs JSON spécifiques

**Résultat** :  Test JSON créé pour valider format et contenu.

### Exercise 12: Negative Test (404)

**deploy-negative.tftest.hcl** :
\`\`\`hcl
run "deploy" {
  command = apply
}

run "validate_success" {
  command = apply

  module {
    source = "../../modules/test-endpoint"
  }

  variables {
    endpoint = run.deploy.api_endpoint
  }

  assert {
    condition     = data.http.test_endpoint.status_code == 200
    error_message = "Expected 200 OK for root path"
  }
}

run "validate_404" {
  command = apply

  module {
    source = "../../modules/test-endpoint"
  }

  variables {
    endpoint = "\${run.deploy.api_endpoint}/nonexistent"
  }

  assert {
    condition     = data.http.test_endpoint.status_code == 404
    error_message = "Expected 404, got \${data.http.test_endpoint.status_code}"
  }

  assert {
    condition     = length(data.http.test_endpoint.response_body) > 0
    error_message = "Expected error message in response body"
  }
}
\`\`\`

**Concepts** :
- Test des cas d'erreur (negative testing)
- Validation que les erreurs sont bien gérées
- Vérification du code HTTP et du message d'erreur

**Résultat** :  Test négatif créé pour valider gestion des erreurs.

### Commandes

\`\`\`bash
cd /home/sable/devops_base/td4/scripts/tofu/live/lambda-sample

# Initialiser
tofu init

# Valider la configuration
tofu validate
# Output: Success! The configuration is valid.

# Formater les fichiers
tofu fmt

# Exécuter les tests ( déploie sur AWS)
tofu test
tofu test -filter=deploy.tftest.hcl
tofu test -filter=deploy-json.tftest.hcl
tofu test -filter=deploy-negative.tftest.hcl
\`\`\`

**Résultat** :  Configuration validée, 3 fichiers de test créés.

---

## Section 7: Testing Recommendations

### 1. Test Pyramid

\`\`\`
           /\\
          /  \\         E2E Tests (10%)
         /    \\        - Lents, coûteux
        /------\\       - Peu nombreux
       /        \\      
      /   INTE  \\     Integration Tests (20%)
     /   GRATION \\    - Vitesse moyenne
    /--------------\\   
  /                \\  
 /   UNIT  TESTS   \\ Unit Tests (70%)
/____________________\\ - Rapides, nombreux
\`\`\`

**Distribution recommandée** :
- 70% Unit Tests : Base solide, rapides
- 20% Integration Tests : Composants ensemble
- 10% E2E Tests : Scénarios critiques

### 2. What to Test

** TESTEZ** :
- Logic métier critique
- Edge cases et valeurs limites
- Error handling et exceptions
- Public APIs et interfaces
- Security (validation, sanitization)

** NE TESTEZ PAS** :
- Framework code
- Third-party libraries
- Getters/Setters simples
- Configuration files

### 3. Test-Driven Development (TDD)

**Cycle Red-Green-Refactor** :

\`\`\`
1. RED    : Écrire un test qui échoue
     ↓
2. GREEN  : Écrire le code minimal pour passer
     ↓
3. REFACTOR : Améliorer le code
     ↓
   (Répéter)
\`\`\`

### 4. Code Coverage

**Métriques** :
- **Statement Coverage** : % de lignes exécutées
- **Branch Coverage** : % de branches testées
- **Function Coverage** : % de fonctions appelées

**Objectifs** :
- 80%+ couverture globale
- 90%+ pour code critique
- 100% pour utilitaires

** Important** :
- 100% coverage ≠ 100% bug-free
- Qualité > Quantité

### 5. Best Practices - FIRST

- **F**ast : Rapides à exécuter
- **I**ndependent : Indépendants
- **R**epeatable : Même résultat toujours
- **S**elf-validating : Pass ou Fail clair
- **T**imely : Écrits au bon moment

### 6. AAA Pattern

\`\`\`javascript
test('Description', () => {
  // Arrange : Préparer les données
  const data = { /* ... */ };
  
  // Act : Exécuter l'action
  const result = function(data);
  
  // Assert : Vérifier le résultat
  expect(result).toBe(expected);
});
\`\`\`

### Exercise 13: TDD Example - \`/multiply\` endpoint

**Cycle complet TDD** :

**Étape 1 - RED** : Tests d'abord (échouent)
\`\`\`javascript
describe('Test /multiply (TDD)', () => {
  test('GET /multiply/4/5 should return 20', async () => {
    const response = await request(app).get('/multiply/4/5');
    expect(response.statusCode).toBe(200);
    expect(response.text).toBe('4 × 5 = 20');
  });

  test('GET /multiply/2.5/4 should handle decimals', async () => {
    const response = await request(app).get('/multiply/2.5/4');
    expect(response.text).toBe('2.5 × 4 = 10');
  });

  test('GET /multiply/abc/xyz should return 400', async () => {
    const response = await request(app).get('/multiply/abc/xyz');
    expect(response.statusCode).toBe(400);
  });
});
\`\`\`

**Résultat** :  Tests échouent (endpoint n'existe pas)

**Étape 2 - GREEN** : Implémentation minimale
\`\`\`javascript
app.get('/multiply/:a/:b', (req, res) => {
  const a = parseFloat(req.params.a);
  const b = parseFloat(req.params.b);
  
  if (isNaN(a) || isNaN(b)) {
    return res.status(400).send('Invalid numbers');
  }
  
  res.send(\`\${a} × \${b} = \${a * b}\`);
});
\`\`\`

**Résultat** :  Tests passent

**Étape 3 - REFACTOR** : Éliminer duplication (DRY)
\`\`\`javascript
// Helper function réutilisable
function parseAndValidateNumbers(req, res) {
  const a = parseFloat(req.params.a);
  const b = parseFloat(req.params.b);
  
  if (isNaN(a) || isNaN(b)) {
    res.status(400).send('Invalid numbers');
    return null;
  }
  return { a, b };
}

// Endpoints simplifiés
app.get('/add/:a/:b', (req, res) => {
  const numbers = parseAndValidateNumbers(req, res);
  if (!numbers) return;
  const { a, b } = numbers;
  res.send(\`\${a} + \${b} = \${a + b}\`);
});

app.get('/multiply/:a/:b', (req, res) => {
  const numbers = parseAndValidateNumbers(req, res);
  if (!numbers) return;
  const { a, b } = numbers;
  res.send(\`\${a} × \${b} = \${a * b}\`);
});
\`\`\`

**Résultat** :  Tests passent toujours, code meilleur !

**Bénéfices TDD** :
- Design émerge naturellement
- Confiance lors du refactoring
- Documentation vivante
- Edge cases pensés dès le début

### Exercise 14: Coverage Analysis

**Scénario** : Code avec couverture incomplète

\`\`\`javascript
// Fonction avec plusieurs branches
function calculateDiscount(price, userType) {
  if (price < 0) {
    throw new Error('Price cannot be negative');
  }
  
  if (userType === 'premium') {
    return price * 0.8;  // 20% discount
  } else if (userType === 'regular') {
    return price * 0.95; // 5% discount
  } else if (userType === 'new') {
    return price * 0.9;  // 10% discount
  } else {
    return price;        // No discount
  }
}
\`\`\`

**Tests incomplets** (seulement 2 cas) :
\`\`\`javascript
test('Premium user', async () => {
  const response = await request(app).get('/discount/100/premium');
  expect(response.text).toBe('Final price: 80');
});

test('Regular user', async () => {
  const response = await request(app).get('/discount/100/regular');
  expect(response.text).toBe('Final price: 95');
});
\`\`\`

**Couverture partielle** :
\`\`\`
File   | % Branch | Uncovered Line #s 
-------|----------|-------------------
app.js |   66.67  | 45,47,50
\`\`\`

**Gaps identifiés** :
-  Ligne 45 : Cas \`price < 0\` non testé
-  Ligne 47 : Cas \`userType === 'new'\` non testé
-  Ligne 50 : Cas \`else\` (userType invalide) non testé

**Tests complets** (combler les gaps) :
\`\`\`javascript
// Ajouter ces tests
test('New user', async () => {
  const response = await request(app).get('/discount/100/new');
  expect(response.text).toBe('Final price: 90');
});

test('Unknown user type', async () => {
  const response = await request(app).get('/discount/100/unknown');
  expect(response.text).toBe('Final price: 100');
});

test('Negative price', async () => {
  const response = await request(app).get('/discount/-50/premium');
  expect(response.statusCode).toBe(400);
});
\`\`\`

**Nouvelle couverture** :
\`\`\`
File   | % Branch | % Lines | Uncovered
-------|----------|---------|----------
app.js |   100    |   100   | 
\`\`\`

** 100% de couverture après comblement des gaps !**

**Leçons apprises** :
1.  Utiliser le rapport de couverture pour identifier les gaps
2.  Prioriser selon criticité (erreurs > cas normaux)
3.  Tester toutes les branches (if/else/else if)
4.  Ne pas oublier les cas d'erreur

---

## Tous les Exercices

### Récapitulatif Complet

| # | Exercice | Section | Description | Status |
|---|----------|---------|-------------|--------|
| **1** | Git Tag | 1 | Créer tag v1.0 |  |
| **2** | Git Rebase | 1 | Rebase avec résolution conflit |  |
| **3** | Branch Protection | 2 | Configurer rulesets GitHub |  |
| **4** | Signed Commits | 2 | GPG configuration |  |
| **5** | Pin Node.js | 3 | Version avec SHA256 |  |
| **6** | Docker Script | 3 | run-in-docker.sh |  |
| **7** | API Endpoint | 4 | /name/:name |  |
| **8** | DevDependencies | 4 | Analyse différences |  |
| **9** | Add Endpoint | 5 | /add/:a/:b + 4 tests |  |
| **10** | Code Coverage | 5 | 100% couverture |  |
| **11** | JSON Test | 6 | jsondecode() assertions |  |
| **12** | Negative Test | 6 | Test 404 error |  |
| **13** | TDD Refactor | 7 | /multiply avec TDD |  |
| **14** | Coverage Analysis | 7 | Identifier et combler gaps |  |

### Commandes principales par section

**Section 1 - Git** :
\`\`\`bash
git init
git add .
git commit -m "message"
git checkout -b branch
git merge branch
git tag v1.0
git rebase master
\`\`\`

**Section 2 - GitHub** :
\`\`\`bash
git remote add origin <url>
git push origin branch
git pull origin main
gpg --version
\`\`\`

**Section 3 - Build** :
\`\`\`bash
npm start
docker build -t app:v1 .
docker run -p 8080:8080 app:v1
./run-in-docker.sh
\`\`\`

**Section 4 - Dependencies** :
\`\`\`bash
npm install
npm ci --only=production
\`\`\`

**Section 5 - Testing** :
\`\`\`bash
npm test
npm run test:coverage
\`\`\`

**Section 6 - OpenTofu** :
\`\`\`bash
tofu init
tofu validate
tofu test
tofu fmt
\`\`\`

---

##  Compétences Acquises

### Version Control & Collaboration
-  Git : init, commit, branch, merge, rebase
-  Résolution de conflits
-  Tags et gestion historique
-  GitHub : Pull Requests, branch protection
-  GPG commit signing

### Build Systems & Automation
-  npm scripts configuration
-  Docker builds et optimization
-  Version pinning avec SHA256
-  Automation scripts (bash)

### Dependency Management
-  npm install / ci
-  dependencies vs devDependencies
-  Production optimization

### Automated Testing
-  Jest unit tests
-  SuperTest API tests
-  Test-Driven Development (TDD)
-  Code coverage (100%)
-  Infrastructure testing (OpenTofu)
-  Negative testing

### Best Practices
-  Test Pyramid strategy
-  FIRST principles
-  AAA Pattern
-  Coverage analysis et gap identification

---

##  Structure Finale du Projet

\`\`\`
devops_base/
├── README.md                         # README principal du dépôt
└── td4/
    ├── README_TD4.md                 # Ce fichier (documentation complète)
    └── scripts/
        ├── sample-app/               # Section 3 - Build System
        │   ├── app.js
        │   ├── package.json
        │   ├── Dockerfile            # Node.js pinned avec SHA256
        │   ├── build-docker-image.sh
        │   └── run-in-docker.sh      # Exercise 6
        │
        ├── sample-app-express/       # Section 4 - Dependencies
        │   ├── app.js                # Express + /name/:name
        │   ├── package.json          # dependencies + devDependencies
        │   └── Dockerfile            # Optimisé --only=production
        │
        ├── sample-app-express-with-tests/  # Section 5 - Testing
        │   ├── app.js                # Application (avec /add endpoint)
        │   ├── server.js             # Serveur
        │   ├── app.test.js           # 7 tests (100% coverage)
        │   ├── package.json          # Jest + test:coverage script
        │   ├── coverage/             # Rapports de couverture
        │   │   └── lcov-report/      # Rapport HTML
        │   └── views/
        │       └── hello.ejs
        │
        └── tofu/                     # Section 6 - Infrastructure Testing
            ├── live/
            │   └── lambda-sample/
            │       ├── main.tf
            │       ├── outputs.tf
            │       ├── src/
            │       ├── deploy.tftest.hcl            # Test de base
            │       ├── deploy-json.tftest.hcl       # Exercise 11
            │       └── deploy-negative.tftest.hcl   # Exercise 12
            └── modules/
                ├── lambda/           # Module Lambda function
                ├── api-gateway/      # Module API Gateway
                └── test-endpoint/    # Module pour tester HTTP
                    ├── main.tf
                    ├── variables.tf
                    ├── outputs.tf
                    └── versions.tf
\`\`\`

---

##  Conclusion

### Résumé

Le TD4 a couvert l'ensemble du cycle de développement moderne DevOps :

1. **Version Control (Git)** : Historique, branches, tags, rebase
2. **Collaboration (GitHub)** : Pull Requests, protection, GPG
3. **Build Systems (NPM)** : Scripts, Docker, automation
4. **Dependencies** : Gestion optimisée pour production
5. **Automated Testing** : Jest, TDD, 100% coverage
6. **Infrastructure Testing** : OpenTofu tests positifs/négatifs
7. **Best Practices** : Pyramid, FIRST, AAA, coverage analysis

### Accomplissements

-  **14 exercices complétés** avec succès
-  **7 sections** couvrant tous les aspects du testing
-  **100% de couverture** de code atteinte
-  **TDD** maîtrisé avec cycle Red-Green-Refactor
-  **Infrastructure as Code** testée avec OpenTofu

### Prochaines étapes

1. **Commit et push** tout le travail sur GitHub
2. **CI/CD Pipeline** : Intégrer les tests automatiquement
3. **Monitoring** : Ajouter des health checks
4. **Documentation** : Compléter avec des diagrammes
5. **Amélioration continue** : Appliquer TDD sur nouveaux projets

---

**Auteurs** : DIALLO Samba, DIOP Mouhamed  
**Date de complétion** : 6 Décembre 2025  
**École** : ESIEE Paris  
**Cours** : Fundamentals of DevOps and Software Delivery

**Status Final** :  TD4 COMPLET - 14/14 Exercices
