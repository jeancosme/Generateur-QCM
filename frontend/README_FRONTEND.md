# Générateur de QCM - Frontend

Interface web React pour le générateur de questionnaires mathématiques.

## 🚀 Démarrage rapide

### Prérequis

- Node.js 18+ et npm
- Backend API démarré sur http://localhost:8000

### Installation

```bash
cd frontend
npm install
```

### Lancement en mode développement

```bash
npm run dev
```

L'application sera accessible sur http://localhost:5173

### Build pour la production

```bash
npm run build
npm run preview
```

## 📁 Structure du projet

```
frontend/
├── src/
│   ├── components/          # Composants React
│   │   ├── Header.jsx      # En-tête de l'application
│   │   ├── LevelSelector.jsx    # Sélection du niveau scolaire
│   │   ├── ThemeSelector.jsx    # Sélection des thèmes
│   │   ├── ConfigPanel.jsx      # Configuration du QCM
│   │   ├── QuestionPreview.jsx  # Prévisualisation des questions
│   │   └── ResultPanel.jsx      # Résultats et téléchargement
│   ├── services/
│   │   └── api.js          # Service API
│   ├── App.jsx             # Composant principal
│   ├── App.css             # Styles de l'app
│   ├── main.jsx            # Point d'entrée
│   └── index.css           # Styles globaux
├── public/                  # Fichiers statiques
├── package.json
└── vite.config.js
```

## 🎯 Fonctionnalités

### ✅ Implémenté

- **Sélection du niveau** : 6e, 5e, 4e, 3e
- **Sélection des thèmes** : Sélection multiple avec filtrage par niveau
- **Configuration** : Nombre de questions, difficulté, format de sortie
- **Prévisualisation** : Aperçu des questions disponibles
- **Génération** : Création du QCM via l'API
- **Téléchargement** : PDF et HTML
- **Interface responsive** : Adaptée mobile et desktop

## 🎨 Technologies

- **React 19** : Framework UI
- **Vite** : Build tool
- **CSS natif** : Styling moderne sans framework
- **Fetch API** : Communication avec le backend

## 🔧 Configuration

### URL de l'API

Par défaut, le frontend se connecte à `http://localhost:8000`.

Pour changer l'URL de l'API, modifiez la constante dans [src/services/api.js](src/services/api.js):

```javascript
const API_BASE_URL = 'http://votre-api-url:port';
```

## 📱 Responsive Design

L'interface s'adapte automatiquement aux différentes tailles d'écran :

- **Desktop** : Affichage en colonnes, grilles optimisées
- **Tablet** : Adaptation des grilles
- **Mobile** : Vue empilée, boutons pleine largeur

## 🎯 Workflow utilisateur

1. **Sélectionner un niveau** (6e, 5e, 4e, 3e)
2. **Choisir un ou plusieurs thèmes** (trigonométrie, probabilités, etc.)
3. **Prévisualiser** les questions disponibles
4. **Configurer** le nombre de questions et les options
5. **Générer** le QCM
6. **Télécharger** le fichier PDF ou HTML

## 🐛 Débogage

### Problèmes courants

**Le frontend ne se connecte pas à l'API**
- Vérifiez que le backend est démarré sur le port 8000
- Vérifiez la console du navigateur pour les erreurs CORS

**Les styles ne s'affichent pas correctement**
- Videz le cache du navigateur
- Redémarrez le serveur de développement

**Erreur lors de la génération**
- Vérifiez que les thèmes sélectionnés contiennent des questions
- Consultez la console pour les détails de l'erreur

## 📝 Scripts disponibles

- `npm run dev` : Lance le serveur de développement
- `npm run build` : Build de production
- `npm run preview` : Prévisualiser le build
- `npm run lint` : Vérifier le code avec ESLint

## 🔗 Liens utiles

- Documentation API : http://localhost:8000/docs
- Repository GitHub : https://github.com/jeancosme/Generateur-QCM

## 📄 Licence

Projet éducatif - © 2026
