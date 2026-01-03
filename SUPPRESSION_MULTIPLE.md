# 🗑️ Suppression Multiple de Questions

## Nouvelle fonctionnalité ajoutée !

Vous pouvez maintenant supprimer **plusieurs questions en une seule fois** de 3 façons différentes.

---

## 🎯 Méthode 1 : Mode interactif (Option 7)

```bash
python tools/edit_questions.py -i
```

1. Choisir l'option **7. Supprimer plusieurs questions (liste)**
2. Entrer les UIDs de 3 façons possibles :

### a) Séparés par des virgules
```
UIDs à supprimer: FON3E001, FON3E002, FON3E003
```

### b) Séparés par des espaces
```
UIDs à supprimer: FON3E001 FON3E002 FON3E003
```

### c) Depuis un fichier texte
```
UIDs à supprimer: @liste_a_supprimer.txt
```

---

## 🎯 Méthode 2 : Ligne de commande avec liste

```bash
python tools/edit_questions.py --delete-multiple "FON3E001,FON3E002,FON3E003"
```

✅ Séparation par virgules obligatoire  
✅ Backup automatique avant suppression  
✅ Confirmation demandée

---

## 🎯 Méthode 3 : Depuis un fichier texte

### Créer un fichier texte (ex: `supprimer.txt`)
```
FON3E001
FON3E002
FON3E003
FON3E004
```
(Une UID par ligne)

### Exécuter la suppression
```bash
python tools/edit_questions.py --delete-file supprimer.txt
```

---

## 🛡️ Sécurité

### Avant chaque suppression :
1. ✅ **Affichage** de toutes les questions qui seront supprimées
2. ✅ **Confirmation** obligatoire (oui/non)
3. ✅ **Backup automatique** créé dans `data/backups/`
4. ✅ **Vérification** des UIDs invalides

### Exemple d'affichage avant confirmation :
```
================================================================================
SUPPRESSION MULTIPLE - 3 question(s)
================================================================================

• FON3E001 - 3e - fonctions
  D'après le graphique, l'image de 2 par la fonction f est :...
• FON3E002 - 3e - fonctions
  Quelle est la valeur de f(0) ?...
• FON3E003 - 3e - fonctions
  Pour quelle valeur de x a-t-on f(x) = 0 ?...

================================================================================
⚠️  Confirmer la suppression de ces 3 questions ? (oui/non):
```

---

## 📝 Cas d'usage pratiques

### Scénario 1 : Supprimer toutes les questions obsolètes d'un thème

```bash
# 1. Lister les questions du thème
python tools/edit_questions.py --list --topic "ancien_theme" > questions_a_supprimer.txt

# 2. Éditer le fichier pour ne garder que les UIDs (une par ligne)

# 3. Supprimer en masse
python tools/edit_questions.py --delete-file questions_a_supprimer.txt
```

### Scénario 2 : Nettoyer rapidement quelques questions en double

```bash
# Mode interactif, option 7
python tools/edit_questions.py -i
# Puis : FON3E001, FON3E002, FON3E003
```

### Scénario 3 : Supprimer depuis Excel/CSV

1. Ouvrir `data/master_questions.csv` dans Excel
2. Filtrer les questions à supprimer
3. Copier les UIDs dans un fichier texte
4. Exécuter :
```bash
python tools/edit_questions.py --delete-file uids_depuis_excel.txt
```

---

## ⚠️ UIDs invalides

Si vous entrez des UIDs qui n'existent pas :
```
⚠️  UIDs introuvables : FON3E999, OLD_Q_001
```

Les UIDs valides seront quand même traités, les invalides ignorés.

---

## 🔄 Annuler une suppression

Si vous avez confirmé par erreur :

```bash
# 1. Aller dans les backups
dir data\backups

# 2. Identifier le backup le plus récent (YYYYMMDD_HHMMSS)
# Exemple : master_questions_backup_20251022_235000.csv

# 3. Restaurer
copy data\backups\master_questions_backup_20251022_235000.csv data\master_questions.csv
```

---

## 📊 Exemples complets

### Exemple 1 : Supprimer 5 questions rapidement

```bash
python tools/edit_questions.py --delete-multiple "Q1,Q2,Q3,Q4,Q5"
```

**Sortie :**
```
✓ Chargé 340 questions depuis data/master_questions.csv

================================================================================
SUPPRESSION MULTIPLE - 5 question(s)
================================================================================

• Q1 - 5e - fractions
  Calculer : \frac{3}{8} + \frac{2}{8}...
• Q2 - 5e - fractions
  Simplifier : \frac{6}{8}...
(... etc ...)

⚠️  Confirmer la suppression de ces 5 questions ? (oui/non): oui

✓ Backup créé : data/backups/master_questions_backup_20251022_235500.csv
✓ Fichier sauvegardé : data/master_questions.csv
✓ 5 question(s) supprimée(s).
```

### Exemple 2 : Depuis un fichier

**Fichier `nettoyer_3e.txt` :**
```
FON3E001
FON3E002
PROB3E005
GEOM3E012
```

**Commande :**
```bash
python tools/edit_questions.py --delete-file nettoyer_3e.txt
```

**Sortie :**
```
✓ 4 UIDs chargés depuis nettoyer_3e.txt
✓ Chargé 340 questions depuis data/master_questions.csv

================================================================================
SUPPRESSION MULTIPLE - 4 question(s)
================================================================================
(affichage des 4 questions...)

⚠️  Confirmer la suppression de ces 4 questions ? (oui/non): oui

✓ Backup créé : data/backups/master_questions_backup_20251022_235600.csv
✓ Fichier sauvegardé : data/master_questions.csv
✓ 4 question(s) supprimée(s).
```

---

## 🎉 Résumé des options

| Méthode | Commande | Cas d'usage |
|---------|----------|-------------|
| **Mode interactif** | `python tools/edit_questions.py -i` → Option 7 | Suppression ponctuelle |
| **CLI avec liste** | `--delete-multiple "UID1,UID2,UID3"` | Script rapide |
| **Depuis fichier** | `--delete-file liste.txt` | Grande quantité |

---

## 💡 Astuces

### Pour créer rapidement un fichier de suppression :

#### Windows PowerShell :
```powershell
# Exporter tous les UIDs d'un niveau
python tools/edit_questions.py --list --level 3e | Select-String "FON3E" > a_supprimer.txt
```

#### Linux/Mac :
```bash
# Exporter tous les UIDs d'un thème
python tools/edit_questions.py --list --topic fractions | grep "FR5E" > a_supprimer.txt
```

### Vérifier avant de supprimer :

```bash
# 1. Voir le contenu du fichier
cat supprimer.txt

# 2. Compter combien seront supprimées
python -c "print(len(open('supprimer.txt').readlines()))"

# 3. Lancer la suppression
python tools/edit_questions.py --delete-file supprimer.txt
```

---

## 📞 Aide

```bash
python tools/edit_questions.py --help
```

Options disponibles :
- `--delete UID` : Supprimer une seule question
- `--delete-multiple "UID1,UID2,UID3"` : Supprimer plusieurs (virgules)
- `--delete-file fichier.txt` : Supprimer depuis un fichier
- `--list` : Lister les questions
- `--show UID` : Afficher une question
- `-i` : Mode interactif
