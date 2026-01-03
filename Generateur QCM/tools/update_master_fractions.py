import pandas as pd
import re
import sys
import os

# Ajouter le répertoire parent au chemin pour importer depuis tools/
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from tools.convert_fractions import convert_fractions_to_latex

def update_master_fractions():
    """Met à jour les fractions dans le fichier master"""
    master_path = 'data/master_questions.csv'
    
    print(f"Lecture du master : {master_path}")
    
    try:
        # Lire le master
        df = pd.read_csv(master_path, encoding='utf-8')
        print(f"Trouvé {len(df)} questions dans le master")
        
        # Colonnes à traiter pour les fractions
        columns_to_convert = ['stem_tex', 'answer_tex', 'distractors_tex']
        
        # Compter les questions avec fractions
        original_fractions = 0
        converted_fractions = 0
        
        for col in columns_to_convert:
            if col in df.columns:
                print(f"Traitement colonne {col}...")
                
                # Avant conversion
                before = df[col].astype(str).str.contains(r'\d+/\d+', na=False).sum()
                original_fractions += before
                
                # Conversion
                df[col] = df[col].apply(convert_fractions_to_latex)
                
                # Après conversion 
                after = df[col].astype(str).str.contains(r'\\frac\{', na=False).sum()
                converted_fractions += after
                
                print(f"  {before} fractions détectées → {after} converties en LaTeX")
        
        # Créer une sauvegarde
        backup_path = f'data/backups/master_questions_fractions_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv'
        os.makedirs('data/backups', exist_ok=True)
        
        # Lire le fichier original pour la sauvegarde
        original_df = pd.read_csv(master_path, encoding='utf-8')
        original_df.to_csv(backup_path, index=False, encoding='utf-8')
        print(f"✓ Sauvegarde créée : {backup_path}")
        
        # Sauvegarder le master mis à jour
        df.to_csv(master_path, index=False, encoding='utf-8')
        print(f"✓ Master mis à jour avec {converted_fractions} fractions LaTeX")
        
        # Afficher quelques exemples de conversions
        print("\n=== Exemples de conversions ===")
        fraction_questions = df[df['topic'] == 'fractions'].head(3)
        for _, row in fraction_questions.iterrows():
            if pd.notna(row['stem_tex']) and '\\frac' in str(row['stem_tex']):
                print(f"Q{row['uid']}: {row['stem_tex']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour : {e}")
        return False

if __name__ == '__main__':
    print("--- Mise à jour des fractions dans le master ---")
    success = update_master_fractions()
    if success:
        print("\n✅ Mise à jour du master terminée avec succès !")
    else:
        print("\n❌ Échec de la mise à jour")