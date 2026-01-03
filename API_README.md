# API Backend - Générateur de QCM

## 🚀 Démarrage rapide

### 1. Installer les dépendances
```bash
pip install -r requirements-api.txt
```

### 2. Lancer le serveur API
```bash
python api/app.py
```

Ou avec uvicorn directement :
```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Accéder à la documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

---

## 📡 Endpoints disponibles

### Questions
- `GET /api/questions` - Liste des questions avec filtres
- `GET /api/questions/{uid}` - Récupérer une question
- `POST /api/questions` - Créer une question
- `PUT /api/questions/{uid}` - Modifier une question
- `DELETE /api/questions/{uid}` - Supprimer une question

### Génération
- `POST /api/generate` - Générer un PDF de questions flash

### Métadonnées
- `GET /api/stats` - Statistiques de la base
- `GET /api/levels` - Liste des niveaux disponibles
- `GET /api/topics` - Liste des thèmes disponibles
- `GET /api/subtopics` - Liste des sous-thèmes disponibles

---

## 🔍 Exemples d'utilisation

### Récupérer toutes les questions de 3e
```bash
curl "http://localhost:8000/api/questions?level=3e"
```

### Filtrer par niveau et thème
```bash
curl "http://localhost:8000/api/questions?level=3e&level=4e&topic=thales&topic=pythagore"
```

### Générer un PDF
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Évaluation Thalès",
    "n": 5,
    "filters": {
      "level": ["3e"],
      "topic": ["thales"],
      "max_difficulty": 3
    },
    "mode": "qfqcm"
  }' \
  --output questions.pdf
```

### Obtenir les statistiques
```bash
curl "http://localhost:8000/api/stats"
```

---

## 🏗️ Architecture

```
api/
├── __init__.py          # Package marker
├── app.py              # Application FastAPI principale
├── models.py           # Modèles Pydantic (Question, Filters, etc.)
└── services.py         # Logique métier (QuestionService, GeneratorService)
```

### Séparation des responsabilités
- **app.py** : Définition des routes et endpoints
- **models.py** : Modèles de données et validation
- **services.py** : Logique métier et interaction avec les données

---

## 🔧 Configuration

### Variables d'environnement (optionnel)
Créer un fichier `.env` :
```env
CSV_PATH=data/master_questions.csv
EXPORTS_DIR=exports/tex
HOST=0.0.0.0
PORT=8000
```

### CORS
Par défaut, CORS est configuré pour accepter toutes les origines (`*`). 
En production, modifier dans `app.py` :
```python
allow_origins=["https://votre-domaine.com"]
```

---

## 📊 Format des données

### Question JSON
```json
{
  "uid": "3e_thales_001",
  "level": "3e",
  "topic": "thales",
  "subtopic": "calcul_longueur",
  "skill": "calculer",
  "format": "court",
  "difficulty": 3,
  "time_s": 60,
  "stem_tex": "Dans le triangle ABC...",
  "answer_tex": "4,5",
  "distractors_tex": "3,5;5,5;6",
  "figure_url": "",
  "tags": "géométrie,théorème",
  "status": "validé",
  "language": "fr"
}
```

---

## 🧪 Tests

### Test manuel avec la documentation interactive
1. Aller sur http://localhost:8000/docs
2. Cliquer sur "Try it out" pour chaque endpoint
3. Tester les différents paramètres

### Test avec curl
```bash
# Santé de l'API
curl http://localhost:8000/

# Liste des questions
curl http://localhost:8000/api/questions?limit=5

# Statistiques
curl http://localhost:8000/api/stats
```

---

## 🐛 Dépannage

### Port déjà utilisé
Si le port 8000 est occupé, changer le port :
```bash
uvicorn api.app:app --port 8001
```

### Erreur de module
Vérifier que vous êtes à la racine du projet :
```bash
cd "c:\Users\Utilisateur\Desktop\NextCloud\Applications\Generateur QCM"
python api/app.py
```

### CSV non trouvé
Vérifier que `data/master_questions.csv` existe.

---

## 🚀 Prochaines étapes

1. **Frontend** : Créer une interface web (HTML/CSS/JS ou React)
2. **Base de données** : Migrer vers PostgreSQL/SQLite
3. **Authentification** : Ajouter JWT pour sécuriser l'API
4. **Cache** : Implémenter Redis pour les performances
5. **Tests** : Ajouter des tests unitaires et d'intégration
