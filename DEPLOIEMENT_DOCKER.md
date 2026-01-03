# 🐳 Guide de Déploiement Docker - Générateur de QCM

## 📋 Prérequis

- **Docker** 20.10+
- **Docker Compose** 2.0+
- Au moins **2 GB de RAM** disponible
- Port **80** et **8000** libres

## 🚀 Démarrage rapide

### 1. Cloner le projet (si nécessaire)

```bash
git clone <votre-repo>
cd "Generateur QCM"
```

### 2. Construire et lancer les conteneurs

```bash
docker-compose up --build
```

L'application sera accessible sur :
- **Frontend** : http://localhost
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

### 3. Arrêter l'application

```bash
docker-compose down
```

## 📦 Architecture Docker

```
┌─────────────────────────────────────────┐
│           DOCKER COMPOSE                │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────┐   ┌──────────────┐  │
│  │   Frontend    │   │   Backend    │  │
│  │   (nginx)     │   │   (Python)   │  │
│  │   Port: 80    │   │  Port: 8000  │  │
│  └───────┬───────┘   └──────┬───────┘  │
│          │                   │          │
│          └───────┬───────────┘          │
│                  │                      │
│           qcm-network                   │
└─────────────────────────────────────────┘
         │                  │
         ↓                  ↓
    Volumes:           Volumes:
    - dist/            - data/
                       - exports/
                       - config/
```

## 🔧 Services

### Backend API (Python/FastAPI)

**Image** : Python 3.11-slim + LaTeX  
**Port** : 8000  
**Healthcheck** : `/health`  

Caractéristiques :
- Uvicorn avec 2 workers
- Support LaTeX pour génération PDF
- Volumes persistants pour données
- Utilisateur non-root pour sécurité

### Frontend (React/Nginx)

**Image** : Node 20 (build) + Nginx Alpine (production)  
**Port** : 80  
**Healthcheck** : `wget localhost/`

Caractéristiques :
- Build multi-stage optimisé
- Compression gzip
- Cache des assets
- Proxy vers l'API backend
- Headers de sécurité

## 📁 Structure des fichiers Docker

```
Generateur QCM/
├── docker-compose.yml          # Orchestration
├── api/
│   ├── Dockerfile             # Image backend
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile             # Image frontend
│   ├── nginx.conf             # Config nginx
│   └── .dockerignore
└── data/                       # Volumes persistants
    ├── questions/
    ├── backups/
    └── exports/
```

## 🎯 Commandes utiles

### Démarrage en arrière-plan

```bash
docker-compose up -d
```

### Voir les logs

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reconstruire les images

```bash
docker-compose build --no-cache
docker-compose up --build
```

### État des conteneurs

```bash
docker-compose ps
```

### Redémarrer un service

```bash
docker-compose restart backend
docker-compose restart frontend
```

### Entrer dans un conteneur

```bash
# Backend
docker exec -it qcm-backend sh

# Frontend
docker exec -it qcm-frontend sh
```

### Nettoyer tout

```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer aussi les volumes
docker-compose down -v

# Supprimer les images
docker-compose down --rmi all
```

## 🔒 Sécurité

### Mesures implémentées

✅ Utilisateurs non-root dans les conteneurs  
✅ Multi-stage builds (images légères)  
✅ Headers de sécurité nginx  
✅ Healthchecks actifs  
✅ Réseau Docker isolé  
✅ Volumes avec permissions appropriées  

### Pour la production

⚠️ À configurer en plus :

1. **HTTPS** : Ajouter un reverse proxy (Traefik, Caddy)
2. **Secrets** : Utiliser Docker secrets ou variables d'environnement
3. **Limites** : Définir memory/CPU limits
4. **Monitoring** : Ajouter Prometheus/Grafana
5. **Backups** : Automatiser les sauvegardes des volumes

## 🌍 Variables d'environnement

Créer un fichier `.env` à la racine :

```env
# API Backend
API_ENV=production
API_PORT=8000
API_WORKERS=2

# Frontend
VITE_API_URL=http://localhost:8000

# Ports publics
FRONTEND_PORT=80
BACKEND_PORT=8000
```

Puis modifier `docker-compose.yml` :

```yaml
services:
  backend:
    ports:
      - "${BACKEND_PORT}:8000"
    environment:
      - API_ENV=${API_ENV}
```

## 📊 Monitoring

### Vérifier la santé des services

```bash
# Via Docker
docker inspect qcm-backend | grep -A 10 Health
docker inspect qcm-frontend | grep -A 10 Health

# Via curl
curl http://localhost:8000/health
curl http://localhost/
```

### Logs d'erreurs

```bash
# Backend
docker-compose logs backend | grep ERROR

# Frontend (nginx)
docker exec qcm-frontend cat /var/log/nginx/error.log
```

## 🚢 Déploiement en production

### Option 1 : VPS/Serveur dédié

1. Installer Docker et Docker Compose
2. Cloner le projet
3. Configurer les variables d'environnement
4. Lancer : `docker-compose up -d`
5. Configurer un reverse proxy (Nginx/Traefik) avec SSL

### Option 2 : Docker Swarm

```bash
docker stack deploy -c docker-compose.yml qcm-stack
```

### Option 3 : Kubernetes

Créer les manifests K8s appropriés (Deployment, Service, Ingress)

## 🐛 Dépannage

### Le frontend ne peut pas joindre l'API

**Problème** : Erreur CORS ou connexion refusée

**Solutions** :
1. Vérifier que le backend est démarré : `docker-compose ps`
2. Vérifier les logs : `docker-compose logs backend`
3. Tester l'API : `curl http://localhost:8000/health`
4. Vérifier la config nginx dans `frontend/nginx.conf`

### LaTeX ne compile pas

**Problème** : Erreur lors de la génération PDF

**Solutions** :
1. Vérifier que LaTeX est installé dans le conteneur
2. Entrer dans le conteneur : `docker exec -it qcm-backend sh`
3. Tester : `pdflatex --version`

### Problèmes de permissions

**Problème** : Cannot write to volume

**Solutions** :
```bash
# Donner les bonnes permissions
sudo chown -R 1000:1000 data/ exports/

# Ou recréer les volumes
docker-compose down -v
docker-compose up
```

### Images trop volumineuses

**Problème** : Temps de build trop long

**Solutions** :
```bash
# Nettoyer les images inutilisées
docker system prune -a

# Utiliser le cache
docker-compose build
```

## 📈 Optimisations

### Build plus rapide

- Utilisez `.dockerignore` pour exclure les fichiers inutiles
- Mettez en cache les dépendances (layers Docker)
- Utilisez multi-stage builds

### Performance en production

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

## 🔗 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Configuration](https://nginx.org/en/docs/)

## ✅ Checklist de déploiement

- [ ] Docker et Docker Compose installés
- [ ] Ports 80 et 8000 disponibles
- [ ] Variables d'environnement configurées
- [ ] Volumes de données créés
- [ ] Healthchecks fonctionnels
- [ ] Logs accessibles et monitoring en place
- [ ] Backups automatisés configurés
- [ ] SSL/HTTPS configuré (production)
- [ ] Firewall configuré
- [ ] Tests de charge effectués

---

**Besoin d'aide ?** Consultez les logs avec `docker-compose logs -f`
