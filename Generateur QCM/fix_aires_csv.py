#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script pour corriger les lignes d'aires dans master_questions.csv"""

# Lire tout le fichier
with open('data/master_questions.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lignes: {len(lines)}")
print(f"Ligne 402 avant (virgules={lines[401].count(',')}):")
print(lines[401][:100])

# Remplacer les lignes problématiques
# Ligne 402 (index 401)
lines[401] = 'AI3E004,3e,aires,disque,calcul,QCM,2,40,"Calculer l\'aire d\'un disque de rayon 4 cm. ($\\pi \\approx 3,14$)","50,24 cm^2","25,12 cm^2|12,56 cm^2|100,48 cm^2",,flash;aires;disque,à valider,fr,aires.csv\n'

# Ligne 417 (index 416) - AI3E017
for i, line in enumerate(lines):
    if line.startswith('AI3E017,'):
        lines[i] = 'AI3E017,3e,aires,parallelogramme,calcul,QCM,2,40,Calculer l\'aire d\'un parallélogramme de base 9 cm et hauteur 7 cm.,63 cm^2,21 cm^2|36 cm^2|49 cm^2,,flash;aires;parallelogramme,à valider,fr,aires.csv\n'
        print(f"Corrigé ligne {i+1} (AI3E017)")
        
# Ligne 418 (index 417) - AI3E018
for i, line in enumerate(lines):
    if line.startswith('AI3E018,'):
        lines[i] = 'AI3E018,3e,aires,trapeze,calcul,QCM,2,40,"Calculer l\'aire d\'un trapèze de bases 12 cm et 6 cm, hauteur 5 cm.",45 cm^2,30 cm^2|36 cm^2|60 cm^2,,flash;aires;trapeze,à valider,fr,aires.csv\n'
        print(f"Corrigé ligne {i+1} (AI3E018)")

# Ligne 419 (index 418) - AI3E019
for i, line in enumerate(lines):
    if line.startswith('AI3E019,'):
        lines[i] = 'AI3E019,3e,aires,carre,calcul,QCM,1,30,Un carré a une aire de 64 cm^2. Quelle est la longueur de son côté ?,8 cm,16 cm|32 cm|4 cm,,flash;aires;carre,à valider,fr,aires.csv\n'
        print(f"Corrigé ligne {i+1} (AI3E019)")

# Ligne 420 (index 419) - AI3E020        
for i, line in enumerate(lines):
    if line.startswith('AI3E020,'):
        lines[i] = 'AI3E020,3e,aires,rectangle,calcul,QCM,1,30,Un rectangle a une aire de 96 cm^2 et une largeur de 8 cm. Quelle est sa longueur ?,12 cm,8 cm|16 cm|24 cm,,flash;aires;rectangle,à valider,fr,aires.csv\n'
        print(f"Corrigé ligne {i+1} (AI3E020)")

print(f"\nLigne 402 après (virgules={lines[401].count(',')}):")
print(lines[401][:100])

# Écrire le fichier corrigé
with open('data/master_questions.csv', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✓ Fichier corrigé et sauvegardé!")
