# Résultats Olympiades de Mathématiques

Application web pour consulter les résultats des Olympiades de Mathématiques - Académie de Créteil.

## 🌐 Lien Web

**https://jeancosme.github.io/resultats-olympiades/**

⚠️ **Dépôt privé** : accessible uniquement aux personnes autorisées

## 🔐 Sécurité

- ✅ Dépôt GitHub **privé** (données protégées)
- ✅ Authentification par établissement (UAI + mot de passe)
- ✅ Accès limité aux personnes autorisées

## 📋 Fonctionnalités

- ✅ Authentification sécurisée par établissement (code UAI)
- 🔍 Recherche d'élève en temps réel
- 📊 Affichage des résultats individuels et d'équipe
- 📥 Export des résultats en PDF, Excel, CSV, ODS

## 🚀 Mise à jour des résultats

### 1. Convertir le fichier Excel

Placez votre fichier `Résultats.xlsx` et exécutez :
```bash
convertir_excel.bat
```

Génère :
- `data.js` : résultats
- `establishments.js` : identifiants
- `identifiants_etablissements.csv` : à transmettre aux établissements

### 2. Publier sur GitHub

```bash
git add .
git commit -m "Mise à jour des résultats"
git push
```

Tous les fichiers peuvent être publiés car le **dépôt est privé**.

## 📝 Transmettre les identifiants

Envoyez `identifiants_etablissements.csv` aux établissements (email sécurisé).

Chaque établissement utilise :
- Son code UAI
- Son mot de passe unique

---

© 2025 Olympiades de Mathématiques - Académie de Créteil
