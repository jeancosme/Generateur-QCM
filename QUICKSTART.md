# ⚡ Commandes Rapides

## 🎯 Workflow complet

### 1. Réviser les questions
```bash
python tools/review_questions.py --open
```
→ Ouvre une page HTML interactive dans le navigateur

### 2. Éditer la base de données
```bash
python tools/edit_questions.py -i
```
→ Mode interactif pour ajouter/modifier/supprimer

### 3. Générer des flash cards
```bash
python generate_flash.py --level 5e --topic fractions --mode qfqcm
```
→ Crée un PDF et l'ouvre automatiquement

---

## 📝 Édition rapide

### Afficher une question
```bash
python tools/edit_questions.py --show Q_5e_fractions_001
```

### Supprimer une question
```bash
python tools/edit_questions.py --delete Q_5e_fractions_001
```

### Supprimer plusieurs questions
```bash
# Par liste
python tools/edit_questions.py --delete-multiple "FON3E001,FON3E002,FON3E003"

# Depuis un fichier
python tools/edit_questions.py --delete-file liste_a_supprimer.txt
```

### Lister par niveau
```bash
python tools/edit_questions.py --list --level 5e
```

### Lister par thème
```bash
python tools/edit_questions.py --list --topic fractions
```

---

## 🚀 Génération PDF

### Par niveau et thème
```bash
python generate_flash.py --level 5e --topic fractions
```

### Limiter le nombre
```bash
python generate_flash.py --level 5e --topic fractions --n 10
```

### Avec difficulté max
```bash
python generate_flash.py --level 5e --topic fractions --difficulty 3
```

### Tous les modes
```bash
# QCM Flash
python generate_flash.py --level 5e --topic fractions --mode qfqcm

# Libre Flash
python generate_flash.py --level 5e --topic fractions --mode qflibre

# QCM standard
python generate_flash.py --level 5e --topic fractions --mode qcm

# Questions ouvertes
python generate_flash.py --level 5e --topic fractions --mode libre
```

---

## 🛠️ Maintenance

### Normaliser la base
```bash
python tools/normalize_master.py
```

### Convertir les fractions en LaTeX
```bash
python tools/convert_fractions.py
```

### Mettre à jour le master avec fractions
```bash
python tools/update_master_fractions.py
```

---

## 📊 Export autres formats

### HTML simple
```bash
python exporter.py --format html --level 5e --topic fractions
```

### Markdown
```bash
python exporter.py --format md --level 5e --topic fractions
```

### LaTeX brut
```bash
python exporter.py --format tex --level 5e --topic fractions
```

---

## 🔍 Vérification

### Voir toutes les stats
```bash
python tools/edit_questions.py --list
```

### Rechercher dans le HTML
1. Ouvrir : `python tools/review_questions.py --open`
2. Utiliser la barre de recherche
3. Appliquer les filtres

---

## ⚠️ En cas de problème

### Restaurer un backup
```bash
# Lister les backups
dir data\backups

# Restaurer (remplacer YYYYMMDD_HHMMSS par la date souhaitée)
copy data\backups\master_questions_backup_YYYYMMDD_HHMMSS.csv data\master_questions.csv
```

### Vérifier l'intégrité
```bash
python tools/normalize_master.py
```

---

## 📚 Aide détaillée

### Pour chaque outil
```bash
python generate_flash.py --help
python tools/edit_questions.py --help
python tools/review_questions.py --help
python exporter.py --help
```

### Documentation complète
- Voir [README.md](README.md)
- Voir [GUIDE_EDITION.md](GUIDE_EDITION.md)
