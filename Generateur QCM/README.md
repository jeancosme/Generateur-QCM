
# Workflow "Questions flash" — sans figures (v1)

## 📚 Banque de questions

### Base de données
- **Fichier principal** : `data/master_questions.csv` (340 questions)
- **Organisation** : `data/questions/[niveau]/[fichier].csv`
- **Niveaux** : 5e, 4e, 3e

### 🛠️ Outils de gestion

#### 1️⃣ Révision visuelle (HTML interactif)
```bash
python tools/review_questions.py --open
```
- Interface web moderne avec recherche et filtres
- Fractions LaTeX correctement affichées
- Tri par niveau, thème, difficulté

#### 2️⃣ Édition interactive
```bash
python tools/edit_questions.py -i
```
- Ajouter/modifier/supprimer des questions
- Backups automatiques avant chaque modification
- Recherche et filtrage intégrés

📖 **Guide complet** : voir [GUIDE_EDITION.md](GUIDE_EDITION.md)

### Édition manuelle
- Vous pouvez aussi éditer directement dans Excel/LibreOffice/Google Sheets
- Colonnes clés : uid, level, topic, subtopic, skill, format, difficulty, time_s, stem_tex, answer_tex, distractors_tex, figure_url, tags, status, language

---

## 📄 Génération de flash cards (CLI)

### Utilisation rapide
```bash
```bash
python generate_flash.py --level 5e --topic fractions --mode qfqcm
```

### Script principal : `generate_flash.py`
- Sélectionne les questions selon vos critères
- Génère un PDF LaTeX avec mise en page optimisée
- Ouvre automatiquement le résultat

### Modes disponibles
- `qfqcm` : Questions Flash QCM
- `qflibre` : Questions Flash Libre
- `qcm` : QCM standard
- `libre` : Questions ouvertes

### Options principales
```bash
--level 5e          # Niveau (5e, 4e, 3e)
--topic fractions   # Thème spécifique
--n 10             # Nombre de questions
--difficulty 2     # Difficulté max (1-5)
--mode qfqcm       # Mode de génération
```

### Exemple complet
```bash
python generate_flash.py --level 5e --topic fractions --n 15 --difficulty 3 --mode qfqcm
```

---

## 📊 Formats d'export

### Exporteur : `exporter.py`

#### Format LaTeX
```bash
python exporter.py --format tex --level 3e --topic pythagore --n 8
```

#### Format Markdown
```bash
python exporter.py --format md --level 3e --n 6 --no-answers
```

#### Format HTML
```bash
python exporter.py --format html --level 4e --n 10
```

---

## 🔧 Outils de maintenance

### Normalisation de la base
```bash
python tools/normalize_master.py
```
- Harmonise les schémas CSV
- Valide l'intégrité des données
- Crée des backups automatiques

### Conversion des fractions
```bash
python tools/convert_fractions.py
```
- Convertit `3/8` en `\frac{3}{8}`
- Traite stem_tex, answer_tex, distractors_tex

---

## 🚀 Démarrage rapide

### 1. Réviser vos questions
```bash
python tools/review_questions.py --open
```

### 2. Générer des flash cards
```bash
python generate_flash.py --level 5e --topic fractions --mode qfqcm
```

### 3. Ajouter/modifier des questions
```bash
python tools/edit_questions.py -i
```

---

## 📁 Structure du projet

```
Generateur QCM/
├── data/
│   ├── master_questions.csv       # Base principale (340 questions)
│   ├── backups/                   # Sauvegardes automatiques
│   └── questions/                 # Questions par niveau
│       ├── 5e/
│       ├── 4e/
│       └── 3e/
├── tools/
│   ├── review_questions.py        # Révision HTML
│   ├── edit_questions.py          # Éditeur interactif
│   ├── normalize_master.py        # Normalisation CSV
│   └── convert_fractions.py       # Conversion LaTeX
├── exports/
│   ├── tex/                       # PDFs générés
│   └── html/                      # Pages de révision
├── generate_flash.py              # Générateur principal
├── exporter.py                    # Exporteur multi-format
└── GUIDE_EDITION.md              # Guide détaillé

```

---

## 💡 Prochaines étapes
- Ajout d'images/figures depuis votre app (colonne `figure_url`)
- Paramétrage de questions (templates + tirage de valeurs)
- Webhook/automation n8n (filtrage via paramètres d'URL, génération et dépôt dans un dossier partagé)
```

### Script principal : `generate_flash.py`
- Sélectionne les questions selon vos critères
- Génère un PDF LaTeX avec mise en page optimisée
- Ouvre automatiquement le résultat
```bash
python exporter.py --csv flash_bank.csv --format tex --standalone --title "Questions flash 3e" --level 3e --topic probabilites thales pythagore --n 8 --max-difficulty 3
```
- Autres formats :
```bash
python exporter.py --format md --level 3e --n 6 --no-answers
python exporter.py --format html --level 4e --n 10
```
- Sorties par défaut : `./exports/<format>/questions_<timestamp>.<ext>`

## 3) Compilation LaTeX (si `--standalone`)
- Compilez avec TinyTeX/MiKTeX/TeX Live :
```bash
pdflatex questions_YYYYMMDD_HHMMSS.tex
```

## 4) Intégration dans votre template
- Sans `--standalone`, l’exporteur peut produire un **corps** à `\input{...}`.
- Vous pouvez aussi copier-coller la partie questions dans votre gabarit.

## 5) Prochaines étapes
- Ajout d’images/figures depuis votre app (colonne `figure_url`), génération et inclusion automatiques.
- Paramétrage de questions (templates + tirage de valeurs).
- Webhook/automation n8n (filtrage via paramètres d’URL, génération et dépôt dans un dossier partagé).
