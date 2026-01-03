#!/bin/bash

# Script de déploiement automatique
# Usage: ./deploy.sh [dev|prod]

set -e  # Arrêter en cas d'erreur

ENV=${1:-dev}

echo "🚀 Déploiement en mode: $ENV"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p data/questions data/backups exports/pdf exports/html

# Vérifier le fichier .env
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé, copie depuis .env.example"
    cp .env.example .env
    echo "⚠️  N'oubliez pas de modifier les variables dans .env"
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Build et démarrage
if [ "$ENV" = "prod" ]; then
    echo "🏗️  Build en mode production..."
    docker-compose build --no-cache
    echo "▶️  Démarrage en arrière-plan..."
    docker-compose up -d
else
    echo "🏗️  Build en mode développement..."
    docker-compose up --build -d
fi

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérifier la santé des services
echo "🏥 Vérification de la santé des services..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend API est opérationnel"
else
    echo "❌ Backend API ne répond pas"
    docker-compose logs backend
    exit 1
fi

if curl -f http://localhost &> /dev/null; then
    echo "✅ Frontend est opérationnel"
else
    echo "❌ Frontend ne répond pas"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "✅ Déploiement réussi!"
echo ""
echo "📱 Accès à l'application:"
echo "   Frontend: http://localhost"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""
echo "📊 Commandes utiles:"
echo "   Logs: docker-compose logs -f"
echo "   Stop: docker-compose down"
echo "   Restart: docker-compose restart"
echo ""
