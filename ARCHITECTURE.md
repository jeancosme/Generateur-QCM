# Architecture recommandée pour une grande base de questions

## Structure de dossiers proposée :
```
Generateur QCM/
├── data/
│   ├── questions/
│   │   ├── 6e/
│   │   │   ├── 6e_nombres_decimaux.csv
│   │   │   ├── 6e_fractions.csv
│   │   │   ├── 6e_geometrie.csv
│   │   │   └── 6e_proportionnalite.csv
│   │   ├── 5e/
│   │   │   ├── 5e_nombres_relatifs.csv
│   │   │   ├── 5e_fractions.csv
│   │   │   └── 5e_geometrie.csv
│   │   ├── 4e/
│   │   │   ├── 4e_equations.csv
│   │   │   ├── 4e_puissances.csv
│   │   │   ├── 4e_theoreme_pythagore.csv
│   │   │   └── 4e_statistiques.csv
│   │   └── 3e/
│   │       ├── 3e_calcul_litteral.csv
│   │       ├── 3e_fonctions.csv
│   │       ├── 3e_theoreme_thales.csv
│   │       ├── 3e_probabilites.csv
│   │       └── 3e_trigonometrie.csv
│   ├── master_questions.csv      # Fichier consolidé (optionnel)
│   └── templates/
│       ├── question_template.csv
│       └── bulk_import_template.xlsx
├── scripts/
│   ├── database_manager.py       # Gestionnaire de base
│   ├── question_validator.py     # Validation des questions
│   └── merge_csv.py             # Fusion des fichiers
├── config/
│   ├── taxonomie.json           # Classification des compétences
│   └── validation_rules.json   # Règles de validation
└── tools/
    ├── import_from_excel.py
    ├── export_to_moodle.py
    └── statistics.py
```

## Avantages de cette structure :
1. **Séparation par niveau** : Plus facile à maintenir
2. **Séparation par thème** : Permet des mises à jour ciblées
3. **Modularité** : Ajout/suppression facile de thèmes
4. **Évolutivité** : Structure scalable pour des milliers de questions
5. **Collaboration** : Plusieurs personnes peuvent travailler sur différents fichiers