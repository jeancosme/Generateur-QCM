@echo off
REM Script de déploiement automatique pour Windows
REM Usage: deploy.bat [dev|prod]

setlocal
set ENV=%1
if "%ENV%"=="" set ENV=dev

echo 🚀 Déploiement en mode: %ENV%

REM Vérifier que Docker est installé
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker n'est pas installé
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose n'est pas installé
    exit /b 1
)

REM Créer les répertoires nécessaires
echo 📁 Création des répertoires...
if not exist "data\questions" mkdir data\questions
if not exist "data\backups" mkdir data\backups
if not exist "exports\pdf" mkdir exports\pdf
if not exist "exports\html" mkdir exports\html

REM Vérifier le fichier .env
if not exist ".env" (
    echo ⚠️  Fichier .env non trouvé, copie depuis .env.example
    copy .env.example .env
    echo ⚠️  N'oubliez pas de modifier les variables dans .env
)

REM Arrêter les conteneurs existants
echo 🛑 Arrêt des conteneurs existants...
docker-compose down

REM Build et démarrage
if "%ENV%"=="prod" (
    echo 🏗️  Build en mode production...
    docker-compose build --no-cache
    echo ▶️  Démarrage en arrière-plan...
    docker-compose up -d
) else (
    echo 🏗️  Build en mode développement...
    docker-compose up --build -d
)

REM Attendre que les services soient prêts
echo ⏳ Attente du démarrage des services...
timeout /t 10 /nobreak >nul

REM Vérifier la santé des services
echo 🏥 Vérification de la santé des services...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend API ne répond pas
    docker-compose logs backend
    exit /b 1
) else (
    echo ✅ Backend API est opérationnel
)

curl -f http://localhost >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend ne répond pas
    docker-compose logs frontend
    exit /b 1
) else (
    echo ✅ Frontend est opérationnel
)

echo.
echo ✅ Déploiement réussi!
echo.
echo 📱 Accès à l'application:
echo    Frontend: http://localhost
echo    API: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo.
echo 📊 Commandes utiles:
echo    Logs: docker-compose logs -f
echo    Stop: docker-compose down
echo    Restart: docker-compose restart
echo.

endlocal
