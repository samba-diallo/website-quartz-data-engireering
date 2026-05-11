---
title: "Configuration Nginx - EcoData Platform"
publish: true
---

# Configuration Nginx - EcoData Platform

## Vue d'ensemble

Cette configuration Nginx configure un reverse proxy pour :
- **Backend FastAPI** : API disponible à `/api/` et `/docs`
- **Frontend Streamlit** : Application Web à la racine `/`
- **WebSockets** : Support WebSocket pour Streamlit

## Architecture

```
┌─────────────────┐
│    Nginx        │
│  (Port 80)      │
└────────┬────────┘
         │
    ┌────┴─────────────────┐
    │                      │
    v                      v
┌─────────────┐      ┌────────────┐
│  FastAPI    │      │ Streamlit  │
│  (8000)     │      │  (8501)    │
└─────────────┘      └────────────┘
```

## Configuration complète

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    # Upstream pour le backend FastAPI
    upstream backend {
        server backend:8000;
    }

    # Upstream pour le frontend Streamlit
    upstream frontend {
        server frontend:8501;
    }

    # Redirection HTTP vers HTTPS (optionnel)
    server {
        listen 80;
        server_name _;
        
        # API Backend
        location /api/ {
            proxy_pass http://backend/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Documentation API
        location /docs {
            proxy_pass http://backend/docs;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /openapi.json {
            proxy_pass http://backend/openapi.json;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Frontend Streamlit (racine)
        location / {
            proxy_pass http://frontend/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Streamlit WebSocket
        location /_stcore/ {
            proxy_pass http://frontend/_stcore/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }
    }
}
```

## Points clés de la configuration

### Upstreams
| Upstream | Cible | Port | Usage |
|----------|-------|------|-------|
| `backend` | backend | 8000 | API FastAPI |
| `frontend` | frontend | 8501 | Application Streamlit |

### Routes principales

| Path | Destination | Description |
|------|-------------|-------------|
| `/api/` | FastAPI Backend | Endpoints API |
| `/docs` | FastAPI Backend | Documentation Swagger |
| `/openapi.json` | FastAPI Backend | Schéma OpenAPI |
| `/` | Streamlit Frontend | Application Web |
| `/_stcore/` | Streamlit Frontend | WebSocket Streamlit |
| `/health` | Local | Health Check |

### Configurations importantes

- **`client_max_body_size 100M`** : Permet les uploads jusqu'à 100MB
- **`keepalive_timeout 65`** : Timeout des connexions persistantes
- **Headers de proxy** : Transmission des informations client (IP réelle, protocole, etc.)
- **WebSocket Support** : Configuration Upgrade et Connection pour les WebSockets

## Utilisation en Docker Compose

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend
    networks:
      - app-network

  backend:
    image: ecodata-backend:latest
    expose:
      - "8000"
    networks:
      - app-network

  frontend:
    image: ecodata-frontend:latest
    expose:
      - "8501"
    networks:
      - app-network

networks:
  app-network:
```

## Tests de la configuration

### Vérifier la syntaxe
```bash
nginx -t -c /etc/nginx/nginx.conf
```

### Endpoints disponibles
- API: `http://localhost/api/`
- Documentation: `http://localhost/docs`
- Application: `http://localhost/`
- Health: `http://localhost/health`
