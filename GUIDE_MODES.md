# 🎯 NOUVEAUX MODES QCM ET LIBRE - GUIDE D'UTILISATION

## 🚀 **NOUVEAUTÉS v2.0**

Votre générateur supporte maintenant **2 modes d'affichage** :

### **📝 Mode QCM (`--mode modeqcm`)**
- Affiche **4 choix multiples A, B, C, D** 
- Les distracteurs sont mélangés automatiquement
- Parfait pour les évaluations rapides

### **✏️ Mode Libre (`--mode modelibre`)**  
- Espace vide pour que l'élève écrive sa réponse
- Aucune proposition affichée
- Idéal pour tester le raisonnement

---

## 🛠️ **UTILISATION**

### **Ligne de commande :**
```bash
# Mode QCM
python generate_flash.py --level 3e --n 4 --mode modeqcm --compile

# Mode Libre  
python generate_flash.py --level 3e --n 4 --mode modelibre --compile

# Par défaut = Mode QCM si pas spécifié
python generate_flash.py --level 3e --n 4 --compile
```

### **Scripts rapides :**
- `run_examples_modes.bat` : Menu interactif avec choix du mode
- `quick_3e.bat` : Maintenant avec choix du mode
- `test_modes.bat` : Test des deux modes

---

## 📋 **FORMATS GÉNÉRÉS**

### **Mode QCM** - Tableau avec colonnes :
| # | Énoncé | Choix | Jury |
|---|---------|--------|------|
| Q1 | Calcule : 2+3 | **A.** 5<br>**B.** 4<br>**C.** 6<br>**D.** 7 | |

### **Mode Libre** - Tableau avec colonnes :
| # | Énoncé | Réponse | Jury |
|---|---------|---------|------|
| Q1 | Calcule : 2+3 | _(vide)_ | |

---

## ⚙️ **CONFIGURATION AUTOMATIQUE**

### **Création des choix QCM :**
1. **Réponse correcte** : Tirée de `answer_tex`
2. **3 Distracteurs** : Tirés de `distractors_tex` (séparés par `|`)
3. **Mélange aléatoire** : Ordre différent pour chaque question
4. **Étiquetage** : A, B, C, D automatiques

### **Exemples dans vos données :**
```csv
stem_tex,answer_tex,distractors_tex
"Calcule : 2³","$8$","$6$|$9$|$4$"
```
→ Génère : **A.** $4$ **B.** $8$ **C.** $6$ **D.** $9$ _(ordre mélangé)_

---

## 🎯 **CAS D'USAGE RECOMMANDÉS**

### **Mode QCM** idéal pour :
- ✅ Contrôles rapides (5-10 min)
- ✅ Questions de calcul mental  
- ✅ Révisions avec correction immédiate
- ✅ Évaluations diagnostiques

### **Mode Libre** idéal pour :
- ✅ Évaluations de raisonnement
- ✅ Démonstrations courtes
- ✅ Expression écrite mathématique
- ✅ Développements de calculs

---

## 🔧 **PERSONNALISATION AVANCÉE**

### **Ajouter de meilleurs distracteurs :**
Editez vos fichiers CSV pour améliorer les choix QCM :
```csv
"Résoudre : 2x = 10","$x = 5$","$x = 20$|$x = 2$|$x = 8$"
```

### **Contrôler la difficulté :**
```bash
# Questions faciles en mode QCM
python generate_flash.py --max-difficulty 2 --mode modeqcm

# Questions difficiles en mode libre  
python generate_flash.py --max-difficulty 4 --mode modelibre
```

---

## 📊 **STATISTIQUES D'USAGE**

Les deux modes utilisent la même base de questions, vous pouvez :
- Comparer les résultats QCM vs Libre
- Adapter le mode selon le niveau des élèves  
- Utiliser le mode QCM pour diagnostiquer, puis le mode Libre pour approfondir

---

**🎉 Vos fiches sont maintenant adaptables selon vos besoins pédagogiques !**