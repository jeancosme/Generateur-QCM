#!/usr/bin/env python3
"""
Script pour convertir des fichiers Excel en CSV pour la base de questions
"""

import pandas as pd
import sys
from pathlib import Path

def excel_to_csv(excel_file, output_csv=None):
    """Convertit un fichier Excel en CSV compatible"""
    
    if not output_csv:
        output_csv = Path(excel_file).stem + "_converted.csv"
    
    # Colonnes attendues (ordre important)
    expected_columns = [
        'uid', 'level', 'topic', 'subtopic', 'skill', 'competence',
        'format', 'difficulty', 'time_s', 'stem_tex', 'answer_tex', 
        'distractors_tex', 'explanation_tex', 'figure_url', 'source',
        'author', 'date_created', 'date_modified', 'tags', 'keywords',
        'curriculum', 'status', 'language', 'review_count', 'success_rate'
    ]
    
    try:
        # Lire le fichier Excel
        df = pd.read_excel(excel_file)
        
        # Vérifier et ajouter les colonnes manquantes
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""  # Valeur par défaut
        
        # Réorganiser dans l'ordre attendu
        df = df[expected_columns]
        
        # Nettoyage des données
        df = df.fillna("")  # Remplacer NaN par chaînes vides
        
        # Générer des UIDs automatiques si manquants
        if df['uid'].str.strip().eq('').any():
            level_prefix = df['level'].iloc[0] if not df['level'].iloc[0] == '' else 'Q'
            topic_prefix = df['topic'].iloc[0][:3].upper() if not df['topic'].iloc[0] == '' else 'GEN'
            
            for i, row in df.iterrows():
                if row['uid'].strip() == '':
                    df.at[i, 'uid'] = f"{level_prefix}_{topic_prefix}_{i+1:03d}"
        
        # Sauvegarder en CSV
        df.to_csv(output_csv, index=False, encoding='utf-8')
        
        print(f"✅ Conversion réussie: {excel_file} → {output_csv}")
        print(f"📊 {len(df)} questions converties")
        
        return output_csv
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion: {e}")
        return None

def create_excel_template(filename="template_questions.xlsx"):
    """Crée un template Excel pour faciliter la saisie"""
    
    columns = [
        'uid', 'level', 'topic', 'subtopic', 'skill', 'format',
        'difficulty', 'time_s', 'stem_tex', 'answer_tex', 'distractors_tex',
        'explanation_tex', 'tags', 'status', 'language'
    ]
    
    # Données d'exemple
    sample_data = [
        ['Q6001', '6e', 'fractions', 'simplification', 'calculer', 'court', 1, 15, 
         'Simplifier : $\\frac{6}{9}$', '$\\frac{2}{3}$', '$\\frac{3}{2}$|$1$|$\\frac{1}{3}$',
         'On divise numérateur et dénominateur par 3', 'flash;fractions', 'validé', 'fr'],
        ['Q6002', '6e', 'decimaux', 'addition', 'calculer', 'court', 1, 20,
         'Calcule : $12,5 + 7,3$', '$19,8$', '$19,3$|$20,8$|$12,73$',
         'Addition de décimaux : aligner les virgules', 'flash;decimaux', 'validé', 'fr'],
    ]
    
    df = pd.DataFrame(sample_data, columns=columns)
    
    # Créer le fichier Excel avec formatage
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Questions', index=False)
        
        # Ajouter une feuille d'aide
        help_data = [
            ['Colonne', 'Description', 'Exemple'],
            ['uid', 'Identifiant unique (auto si vide)', 'Q6001'],
            ['level', 'Niveau scolaire', '6e, 5e, 4e, 3e'],
            ['topic', 'Thème principal', 'fractions, equations'],
            ['subtopic', 'Sous-thème', 'simplification, addition'],
            ['skill', 'Compétence', 'calculer, modéliser'],
            ['format', 'Type de question', 'court, QCM, vrai_faux'],
            ['difficulty', 'Difficulté (1-5)', '1=facile, 5=difficile'],
            ['time_s', 'Temps estimé (secondes)', '15, 30, 60'],
            ['stem_tex', 'Énoncé (LaTeX autorisé)', 'Calcule : $2^3$'],
            ['answer_tex', 'Réponse correcte', '$8$'],
            ['distractors_tex', 'Réponses fausses (séparées par |)', '$6$|$9$|$4$'],
            ['explanation_tex', 'Explication (optionnel)', 'Règle de calcul...'],
            ['tags', 'Mots-clés (séparés par ;)', 'flash;puissances;calcul'],
            ['status', 'Statut de validation', 'validé, brouillon, à_revoir'],
            ['language', 'Langue', 'fr, en'],
        ]
        
        help_df = pd.DataFrame(help_data[1:], columns=help_data[0])
        help_df.to_excel(writer, sheet_name='Aide', index=False)
    
    print(f"✅ Template Excel créé: {filename}")
    print("📝 Remplissez la feuille 'Questions', consultez 'Aide' pour les formats")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python excel_converter.py template          # Créer un template")
        print("  python excel_converter.py fichier.xlsx     # Convertir en CSV")
    elif sys.argv[1] == "template":
        create_excel_template()
    else:
        excel_to_csv(sys.argv[1])