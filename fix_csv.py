#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script pour corriger le fichier CSV master_questions.csv"""

import csv

input_file = "data/master_questions.csv"
output_file = "data/master_questions_fixed.csv"

# Lire et réécrire le CSV proprement
with open(input_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Réécrire avec le module csv qui gère correctement les guillemets
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    
    for i, line in enumerate(lines, 1):
        # Parser la ligne avec le module csv
        try:
            reader = csv.reader([line.strip()])
            row = next(reader)
            writer.writerow(row)
            if i % 50 == 0:
                print(f"Ligne {i} traitée OK")
        except Exception as e:
            print(f"Erreur ligne {i}: {e}")
            print(f"Contenu: {line[:100]}...")

print(f"\n✓ Fichier corrigé sauvegardé dans {output_file}")
print("Vérifiez le fichier et remplacez l'original si tout est OK.")
