# 🗄️ GUIDE D'UTILISATION - BASE DE QUESTIONS ÉLARGIE

## 🚀 DÉMARRAGE RAPIDE

### 1️⃣ **Ajout rapide de questions**
```bash
# Créer un template Excel
C:/Python313/python.exe tools/excel_converter.py template

# Remplir le fichier template_questions.xlsx
# Puis convertir en CSV
C:/Python313/python.exe tools/excel_converter.py template_questions.xlsx
```

### 2️⃣ **Organiser vos questions** 
Placez vos fichiers CSV dans :
```
data/questions/
├── 6e/   # Questions de 6e
├── 5e/   # Questions de 5e  
├── 4e/   # Questions de 4e
└── 3e/   # Questions de 3e
```

### 3️⃣ **Fusion et génération**
```bash
# Fusionner tous les CSV
gestion_base.bat   # Choix 1

# Générer une fiche
C:/Python313/python.exe generate_flash.py --level 3e --n 5 --compile --open
```

---

## 🛠️ WORKFLOWS RECOMMANDÉS

### **Workflow A : Ajout ponctuel (1-10 questions)**
1. Ouvrir `template_questions.xlsx` 
2. Ajouter vos questions
3. Sauvegarder dans `data/questions/[niveau]/`
4. Lancer `gestion_base.bat` → Choix 1 (fusion)

### **Workflow B : Ajout massif (10+ questions)**
1. Créer un nouveau template : `tools/excel_converter.py template`
2. Remplir massivement dans Excel
3. Convertir : `tools/excel_converter.py mon_fichier.xlsx` 
4. Déplacer le CSV dans le bon dossier niveau
5. Fusionner : `gestion_base.bat` → Choix 1

### **Workflow C : Maintenance de la base**
1. Validation : `gestion_base.bat` → Choix 2
2. Statistiques : `gestion_base.bat` → Choix 1
3. Export ciblé : `gestion_base.bat` → Choix 3

---

## 📋 FORMAT DES QUESTIONS

### **Colonnes essentielles :**
- `uid` : Identifiant unique (ex: Q3001)
- `level` : Niveau (6e, 5e, 4e, 3e)
- `topic` : Thème (pythagore, equations, fractions...)
- `stem_tex` : Énoncé (LaTeX autorisé)
- `answer_tex` : Réponse correcte
- `difficulty` : Difficulté 1-5

### **Colonnes enrichies (optionnelles) :**
- `explanation_tex` : Explication de la solution
- `competence` : Compétence visée (calculer, modéliser...)
- `tags` : Mots-clés séparés par `;`
- `source` : Origine de la question
- `success_rate` : Taux de réussite observé

---

## 🎯 EXEMPLES D'UTILISATION

### **Génération ciblée :**
```bash
# Fiche 3e sur Thalès et Pythagore
python generate_flash.py --level 3e --topic thales pythagore --n 4 --compile

# Questions faciles tous niveaux
python generate_flash.py --max-difficulty 2 --n 5 --title "Questions faciles" --compile

# Fiche 4e-3e équations uniquement  
python generate_flash.py --level 4e 3e --topic equations --n 3 --compile
```

### **Export pour analyse :**
```bash
# Export toutes les questions de 6e en CSV
gestion_base.bat → Choix 3 → niveau: 6e

# Export questions difficiles (niveau 4-5)
gestion_base.bat → Choix 3 → difficulte: 4
```

---

## 🔧 MAINTENANCE

### **Validation régulière :**
- Lancer `gestion_base.bat` → Choix 2 après chaque ajout
- Vérifier les UIDs uniques
- Contrôler les niveaux et difficultés

### **Sauvegarde :**
- Sauvegarder le dossier `data/` régulièrement  
- Le fichier `data/master_questions.csv` contient tout

### **Performance :**
- Avec des milliers de questions, privilégier les exports ciblés
- Séparer par niveau/thème pour une meilleure organisation

---

## 📊 STATISTIQUES ET SUIVI

Le fichier `data/master_questions.csv` permet :
- Analyse des taux de réussite par thème/niveau
- Équilibrage des difficultés
- Suivi de la couverture du programme
- Export vers d'autres plateformes (Moodle, etc.)

---

**🎉 Votre base est maintenant prête à accueillir des centaines ou milliers de questions de manière organisée !**