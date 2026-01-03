#!/usr/bin/env python3
"""
Gestionnaire de base de données pour Questions Flash
Gère la fusion, validation et maintenance d'une grande base de questions
"""

import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path
import glob

class QuestionDatabase:
    def __init__(self, data_folder="data"):
        self.data_folder = Path(data_folder)
        self.questions_folder = self.data_folder / "questions"
        self.master_file = self.data_folder / "master_questions.csv"
        
    def create_structure(self):
        """Crée la structure de dossiers recommandée"""
        levels = ["6e", "5e", "4e", "3e"]
        
        for level in levels:
            level_dir = self.questions_folder / level
            level_dir.mkdir(parents=True, exist_ok=True)
            
        (self.data_folder / "templates").mkdir(exist_ok=True)
        Path("config").mkdir(exist_ok=True)
        Path("scripts").mkdir(exist_ok=True)
        Path("tools").mkdir(exist_ok=True)
        
        print("✅ Structure de dossiers créée")
    
    def merge_all_csv(self):
        """Fusionne tous les fichiers CSV en un fichier maître"""
        all_files = glob.glob(str(self.questions_folder / "*" / "*.csv"))
        
        if not all_files:
            print("❌ Aucun fichier CSV trouvé dans les sous-dossiers")
            return None
            
        dataframes = []
        for file in all_files:
            try:
                df = pd.read_csv(file, encoding='utf-8')
                df['source_file'] = os.path.basename(file)
                dataframes.append(df)
                print(f"✅ Chargé: {file} ({len(df)} questions)")
            except Exception as e:
                print(f"❌ Erreur avec {file}: {e}")
        
        if dataframes:
            master_df = pd.concat(dataframes, ignore_index=True)
            master_df.to_csv(self.master_file, index=False, encoding='utf-8')
            print(f"✅ Fichier maître créé: {len(master_df)} questions totales")
            return master_df
        
        return None
    
    def validate_questions(self, df=None):
        """Valide la cohérence des questions"""
        if df is None:
            if not self.master_file.exists():
                print("❌ Fichier maître introuvable. Lancez d'abord merge_all_csv()")
                return False
            df = pd.read_csv(self.master_file, encoding='utf-8')
        
        errors = []
        
        # Vérifications de base
        required_cols = ['uid', 'level', 'topic', 'stem_tex', 'answer_tex']
        for col in required_cols:
            if col not in df.columns:
                errors.append(f"Colonne manquante: {col}")
        
        # Vérifier les UIDs uniques
        duplicates = df[df.duplicated(subset=['uid'], keep=False)]
        if not duplicates.empty:
            errors.append(f"UIDs dupliqués: {list(duplicates['uid'].values)}")
        
        # Vérifier les niveaux valides
        valid_levels = ['6e', '5e', '4e', '3e', '2nde', '1ere', 'Term']
        invalid_levels = df[~df['level'].isin(valid_levels)]
        if not invalid_levels.empty:
            errors.append(f"Niveaux invalides: {list(invalid_levels['level'].unique())}")
        
        # Vérifier les difficultés
        if 'difficulty' in df.columns:
            invalid_diff = df[(df['difficulty'] < 1) | (df['difficulty'] > 5)]
            if not invalid_diff.empty:
                errors.append(f"Difficultés invalides (doit être 1-5): {len(invalid_diff)} questions")
        
        if errors:
            print("❌ Erreurs de validation:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("✅ Validation réussie")
            return True
    
    def get_statistics(self):
        """Affiche des statistiques sur la base"""
        if not self.master_file.exists():
            print("❌ Fichier maître introuvable")
            return
            
        df = pd.read_csv(self.master_file, encoding='utf-8')
        
        print("📊 STATISTIQUES DE LA BASE DE QUESTIONS")
        print("="*50)
        print(f"Total questions: {len(df)}")
        print(f"Niveaux: {', '.join(df['level'].value_counts().index.tolist())}")
        
        print("\n🎯 Répartition par niveau:")
        for level, count in df['level'].value_counts().items():
            print(f"  {level}: {count} questions")
        
        if 'topic' in df.columns:
            print(f"\n📚 Thèmes: {df['topic'].nunique()} différents")
            top_topics = df['topic'].value_counts().head(10)
            print("  Top 10 thèmes:")
            for topic, count in top_topics.items():
                print(f"    {topic}: {count}")
        
        if 'difficulty' in df.columns:
            print(f"\n⭐ Difficultés moyennes:")
            diff_stats = df.groupby('level')['difficulty'].mean()
            for level, avg_diff in diff_stats.items():
                print(f"  {level}: {avg_diff:.1f}/5")
        
        if 'status' in df.columns:
            print(f"\n✅ Statuts:")
            for status, count in df['status'].value_counts().items():
                print(f"  {status}: {count}")
    
    def export_by_criteria(self, level=None, topic=None, difficulty_max=None, n=None):
        """Exporte un sous-ensemble selon des critères"""
        if not self.master_file.exists():
            print("❌ Fichier maître introuvable")
            return None
            
        df = pd.read_csv(self.master_file, encoding='utf-8')
        
        # Filtrage
        filtered = df.copy()
        if level:
            filtered = filtered[filtered['level'].isin(level if isinstance(level, list) else [level])]
        if topic:
            filtered = filtered[filtered['topic'].isin(topic if isinstance(topic, list) else [topic])]
        if difficulty_max:
            filtered = filtered[filtered['difficulty'] <= difficulty_max]
        if n:
            filtered = filtered.sample(min(n, len(filtered)))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"export_filtered_{timestamp}.csv"
        filtered.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✅ Export créé: {output_file} ({len(filtered)} questions)")
        return output_file

def main():
    """Interface en ligne de commande"""
    db = QuestionDatabase()
    
    print("🗄️  GESTIONNAIRE DE BASE DE QUESTIONS")
    print("="*40)
    
    while True:
        print("\nOptions disponibles:")
        print("1. Créer structure de dossiers")
        print("2. Fusionner tous les CSV")
        print("3. Valider les questions")
        print("4. Afficher statistiques")
        print("5. Export par critères")
        print("0. Quitter")
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == "1":
            db.create_structure()
        elif choice == "2":
            db.merge_all_csv()
        elif choice == "3":
            db.validate_questions()
        elif choice == "4":
            db.get_statistics()
        elif choice == "5":
            level = input("Niveau(x) (ex: 3e,4e): ").strip()
            topic = input("Thème(s) (ex: pythagore,thales): ").strip()
            difficulty = input("Difficulté max (1-5): ").strip()
            n = input("Nombre max de questions: ").strip()
            
            level = level.split(",") if level else None
            topic = topic.split(",") if topic else None
            difficulty = int(difficulty) if difficulty.isdigit() else None
            n = int(n) if n.isdigit() else None
            
            db.export_by_criteria(level, topic, difficulty, n)
        elif choice == "0":
            break
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()