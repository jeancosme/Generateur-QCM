import pandas as pd
import re
import glob
import os

def convert_fractions_to_latex(text):
    """Convertit les fractions au format a/b vers \frac{a}{b} en LaTeX"""
    if pd.isna(text) or text == '':
        return text
    
    # Pattern pour capturer les fractions: chiffres/chiffres (avec possibilité de décimales et nombres négatifs)
    pattern = r'(-?\d+(?:[.,]\d+)?)/(-?\d+(?:[.,]\d+)?)'
    
    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        # Normaliser virgule -> point pour LaTeX si nécessaire
        numerator = numerator.replace(',', '.')
        denominator = denominator.replace(',', '.')
        return f'\\frac{{{numerator}}}{{{denominator}}}'
    
    # Remplacer toutes les fractions trouvées
    result = re.sub(pattern, replace_fraction, str(text))
    return result

def process_fraction_files():
    """Traite tous les fichiers fractions pour convertir les notations"""
    fraction_files = glob.glob('data/questions/5e/fractions*.csv')
    
    for file_path in fraction_files:
        print(f"Traitement de {os.path.basename(file_path)}...")
        
        # Lire le fichier
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Colonnes à traiter pour les fractions
        columns_to_convert = ['stem_tex', 'answer_tex', 'distractors_tex']
        
        for col in columns_to_convert:
            if col in df.columns:
                print(f"  Conversion colonne {col}...")
                df[col] = df[col].apply(convert_fractions_to_latex)
        
        # Sauvegarder le fichier mis à jour
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"  ✓ {file_path} mis à jour")
    
    print(f"\n✅ {len(fraction_files)} fichiers fractions traités")

def test_conversion():
    """Teste la fonction de conversion sur quelques exemples"""
    test_cases = [
        "Calculer : 3/8 + 2/8",
        "5/7",
        "1/4|2/6|2/4|1/6", 
        "Calculer et simplifier : 2/6 + 1/6",
        "-5/8",
        "2,5/3,7",
        "Aucune fraction ici",
        "15/8"
    ]
    
    print("=== Test de conversion ===")
    for test in test_cases:
        converted = convert_fractions_to_latex(test)
        print(f"'{test}' → '{converted}'")

if __name__ == '__main__':
    print("--- Conversion des fractions vers LaTeX ---")
    test_conversion()
    print("\n" + "="*50 + "\n")
    process_fraction_files()