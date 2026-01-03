# 📝 Guide d'utilisation - Éditeur de Questions

## Étape 1 : Révision des questions (HTML)

### Générer la page de révision
```bash
python tools/review_questions.py
```

### Ouvrir automatiquement dans le navigateur
```bash
python tools/review_questions.py --open
```

### Fonctionnalités de la page HTML
- 🔍 **Recherche en temps réel** dans toutes les questions
- 🎯 **Filtres** par niveau, thème, et difficulté
- ✅ **Réponses correctes** en vert
- ✗ **Distracteurs** en gris
- 📐 **Fractions LaTeX** correctement affichées
- 📊 **Compteur** de questions affichées

---

## Étape 2 : Édition des questions

### Mode interactif (recommandé)
```bash
python tools/edit_questions.py -i
```

**Menu disponible :**
1. **Lister les questions** - Voir toutes les questions avec filtres
2. **Rechercher** - Trouver une question par mot-clé
3. **Afficher** - Voir les détails d'une question
4. **Ajouter** - Créer une nouvelle question
5. **Modifier** - Éditer une question existante
6. **Supprimer** - Retirer une question
7. **Sauvegarder et quitter** - Enregistrer les modifications
8. **Quitter sans sauvegarder** - Annuler les changements

### Commandes en ligne de commande

#### Afficher une question
```bash
python tools/edit_questions.py --show Q_5e_fractions_001
```

#### Supprimer une question
```bash
python tools/edit_questions.py --delete Q_5e_fractions_001
```

#### Lister les questions par niveau
```bash
python tools/edit_questions.py --list --level 5e
```

#### Lister les questions par thème
```bash
python tools/edit_questions.py --list --topic fractions
```

---

## 🛡️ Sécurité

### Backups automatiques
À chaque modification, un **backup automatique** est créé dans :
```
data/backups/master_questions_backup_YYYYMMDD_HHMMSS.csv
```

### Restaurer un backup
Si vous voulez annuler des modifications :
```bash
copy data\backups\master_questions_backup_20251022_233000.csv data\master_questions.csv
```

---

## 💡 Conseils d'utilisation

### Workflow recommandé
1. **Réviser** avec `review_questions.py` pour voir toutes les questions
2. **Noter** les UIDs des questions à modifier/supprimer
3. **Éditer** avec `edit_questions.py -i` en mode interactif
4. **Régénérer** la page de révision pour vérifier

### Format des fractions
Utilisez toujours le format LaTeX pour les fractions :
- ✅ `\frac{3}{8}` 
- ✗ `3/8`

### Nommage des UIDs
Format recommandé : `Q_[niveau]_[thème]_[numéro]`
- Exemple : `Q_5e_fractions_001`
- Évitez les espaces et caractères spéciaux

### Distracteurs
- Minimum 1 distracteur
- Maximum 3 distracteurs recommandé
- Séparés par `|` dans le CSV

---

## 🔧 Dépannage

### Problème : Les fractions ne s'affichent pas
- Vérifiez que vous utilisez `\frac{a}{b}` et non `a/b`
- Assurez-vous que MathJax charge correctement (connexion internet requise)

### Problème : Question non trouvée
- Vérifiez l'UID exact (sensible à la casse)
- Utilisez la recherche pour retrouver la question

### Problème : Modifications perdues
- Toujours choisir "Sauvegarder et quitter" (option 7)
- Vérifiez qu'un backup a été créé dans `data/backups/`

---

## 📋 Exemples pratiques

### Exemple 1 : Ajouter une question sur les fractions
```
Mode interactif > Choix: 4

UID: Q_5e_fractions_061
Niveau: 5e
Thème: fractions
Sous-thème: addition
Difficulté: 2
Question: Calculer $\frac{1}{2} + \frac{1}{3}$
Réponse correcte: $\frac{5}{6}$
Distracteur 1: $\frac{2}{5}$
Distracteur 2: $\frac{3}{6}$
Distracteur 3: (Enter)
```

### Exemple 2 : Supprimer une question en erreur
```bash
python tools/edit_questions.py --delete Q_5e_erreur_001
```

### Exemple 3 : Rechercher toutes les questions sur Pythagore
```
Mode interactif > Choix: 2
Rechercher: pythagore
```

---

## 🚀 Raccourcis utiles

### Générer HTML et éditer ensuite
```bash
python tools/review_questions.py --open
python tools/edit_questions.py -i
```

### Vérifier une modification
```bash
python tools/edit_questions.py --show Q_5e_fractions_001
```

### Lister par difficulté (dans le CSV directement)
```bash
python tools/edit_questions.py --list
```
