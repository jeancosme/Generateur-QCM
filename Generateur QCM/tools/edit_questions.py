import pandas as pd
import argparse
from datetime import datetime
import os
import shutil

class QuestionEditor:
    def __init__(self, csv_path="data/master_questions.csv"):
        self.csv_path = csv_path
        self.df = None
        self.modified = False
        self.load_data()
    
    def load_data(self):
        """Charger le fichier CSV"""
        try:
            self.df = pd.read_csv(self.csv_path, encoding='utf-8')
            print(f"✓ Chargé {len(self.df)} questions depuis {self.csv_path}")
        except Exception as e:
            print(f"✗ Erreur lors du chargement : {e}")
            self.df = None
    
    def create_backup(self):
        """Créer un backup avant modification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, f"master_questions_backup_{timestamp}.csv")
        shutil.copy2(self.csv_path, backup_path)
        print(f"✓ Backup créé : {backup_path}")
        return backup_path
    
    def save_data(self):
        """Sauvegarder les modifications"""
        if not self.modified:
            print("Aucune modification à sauvegarder.")
            return
        
        # Créer un backup
        self.create_backup()
        
        # Sauvegarder
        try:
            self.df.to_csv(self.csv_path, index=False, encoding='utf-8')
            print(f"✓ Fichier sauvegardé : {self.csv_path}")
            self.modified = False
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde : {e}")
    
    def search_question(self, search_term):
        """Rechercher des questions"""
        if self.df is None:
            return pd.DataFrame()
        
        mask = (
            self.df['uid'].astype(str).str.contains(search_term, case=False, na=False) |
            self.df['stem_tex'].astype(str).str.contains(search_term, case=False, na=False) |
            self.df['answer_tex'].astype(str).str.contains(search_term, case=False, na=False)
        )
        
        return self.df[mask]
    
    def display_question(self, uid):
        """Afficher une question par UID"""
        if self.df is None:
            return None
        
        question = self.df[self.df['uid'] == uid]
        
        if question.empty:
            print(f"✗ Question '{uid}' introuvable.")
            return None
        
        q = question.iloc[0]
        print("\n" + "="*80)
        print(f"UID: {q['uid']}")
        print(f"Niveau: {q.get('level', 'N/A')} | Thème: {q.get('topic', 'N/A')} | Difficulté: {q.get('difficulty', 'N/A')}")
        print("-"*80)
        print(f"Question: {q['stem_tex']}")
        print(f"\n✓ Réponse correcte: {q['answer_tex']}")
        
        if pd.notna(q.get('distractors_tex')):
            distractors = q['distractors_tex'].split('|')
            for i, d in enumerate(distractors, 1):
                print(f"✗ Distracteur {i}: {d}")
        
        print("="*80 + "\n")
        return q
    
    def delete_question(self, uid):
        """Supprimer une question"""
        if self.df is None:
            return False
        
        # Afficher la question avant suppression
        question = self.display_question(uid)
        if question is None:
            return False
        
        # Confirmation
        confirm = input(f"⚠️  Confirmer la suppression de '{uid}' ? (oui/non): ").strip().lower()
        
        if confirm in ['oui', 'o', 'yes', 'y']:
            self.df = self.df[self.df['uid'] != uid]
            self.modified = True
            print(f"✓ Question '{uid}' supprimée.")
            return True
        else:
            print("Suppression annulée.")
            return False
    
    def delete_multiple_questions(self, uids_list):
        """Supprimer plusieurs questions"""
        if self.df is None:
            return False
        
        # Filtrer les UIDs valides
        valid_uids = []
        invalid_uids = []
        
        for uid in uids_list:
            uid = uid.strip()
            if uid in self.df['uid'].values:
                valid_uids.append(uid)
            else:
                invalid_uids.append(uid)
        
        if invalid_uids:
            print(f"\n⚠️  UIDs introuvables : {', '.join(invalid_uids)}")
        
        if not valid_uids:
            print("✗ Aucune question valide à supprimer.")
            return False
        
        # Afficher les questions à supprimer
        print(f"\n{'='*80}")
        print(f"SUPPRESSION MULTIPLE - {len(valid_uids)} question(s)")
        print(f"{'='*80}\n")
        
        for uid in valid_uids:
            question = self.df[self.df['uid'] == uid].iloc[0]
            print(f"• {uid} - {question.get('level', 'N/A')} - {question.get('topic', 'N/A')}")
            print(f"  {str(question['stem_tex'])[:70]}...")
        
        # Confirmation globale
        print(f"\n{'='*80}")
        confirm = input(f"⚠️  Confirmer la suppression de ces {len(valid_uids)} questions ? (oui/non): ").strip().lower()
        
        if confirm in ['oui', 'o', 'yes', 'y']:
            self.df = self.df[~self.df['uid'].isin(valid_uids)]
            self.modified = True
            print(f"\n✓ {len(valid_uids)} question(s) supprimée(s).")
            return True
        else:
            print("\nSuppression annulée.")
            return False
    
    def add_question(self, interactive=True):
        """Ajouter une nouvelle question"""
        if self.df is None:
            return False
        
        print("\n" + "="*80)
        print("AJOUT D'UNE NOUVELLE QUESTION")
        print("="*80)
        
        new_question = {}
        
        # UID
        if interactive:
            uid = input("UID (ex: Q_5e_fractions_001): ").strip()
        else:
            return False
        
        if uid in self.df['uid'].values:
            print(f"✗ L'UID '{uid}' existe déjà.")
            return False
        
        new_question['uid'] = uid
        
        # Informations de base
        new_question['level'] = input("Niveau (5e/4e/3e): ").strip()
        new_question['topic'] = input("Thème: ").strip()
        new_question['subtopic'] = input("Sous-thème (optionnel): ").strip() or None
        new_question['difficulty'] = input("Difficulté (1-5): ").strip()
        
        # Question et réponses
        print("\n📝 Contenu (utilisez \\frac{a}{b} pour les fractions):")
        new_question['stem_tex'] = input("Question: ").strip()
        new_question['answer_tex'] = input("Réponse correcte: ").strip()
        
        # Distracteurs
        distractors = []
        for i in range(1, 4):
            d = input(f"Distracteur {i} (Enter pour terminer): ").strip()
            if not d:
                break
            distractors.append(d)
        
        new_question['distractors_tex'] = '|'.join(distractors) if distractors else None
        
        # Métadonnées optionnelles
        new_question['skill'] = input("Compétence (optionnel): ").strip() or None
        new_question['time_s'] = input("Temps en secondes (optionnel): ").strip() or None
        new_question['source'] = input("Source (optionnel): ").strip() or None
        
        # Compléter avec les colonnes manquantes
        for col in self.df.columns:
            if col not in new_question:
                new_question[col] = None
        
        # Ajouter au DataFrame
        new_row = pd.DataFrame([new_question])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.modified = True
        
        print(f"\n✓ Question '{uid}' ajoutée avec succès!")
        return True
    
    def modify_question(self, uid):
        """Modifier une question existante"""
        if self.df is None:
            return False
        
        # Afficher la question
        question = self.display_question(uid)
        if question is None:
            return False
        
        idx = self.df[self.df['uid'] == uid].index[0]
        
        print("Entrez les nouvelles valeurs (Enter pour garder l'actuelle):\n")
        
        # Champs modifiables
        fields = {
            'level': 'Niveau',
            'topic': 'Thème',
            'subtopic': 'Sous-thème',
            'difficulty': 'Difficulté',
            'stem_tex': 'Question',
            'answer_tex': 'Réponse correcte',
            'skill': 'Compétence',
            'time_s': 'Temps (s)'
        }
        
        modified_fields = []
        
        for field, label in fields.items():
            current_value = self.df.at[idx, field]
            new_value = input(f"{label} [{current_value}]: ").strip()
            
            if new_value:
                self.df.at[idx, field] = new_value
                modified_fields.append(field)
        
        # Distracteurs (traitement spécial)
        current_distractors = str(self.df.at[idx, 'distractors_tex']).split('|') if pd.notna(self.df.at[idx, 'distractors_tex']) else []
        
        print(f"\nDistracteurs actuels: {len(current_distractors)}")
        for i, d in enumerate(current_distractors, 1):
            print(f"  {i}. {d}")
        
        modify_distractors = input("\nModifier les distracteurs ? (oui/non): ").strip().lower()
        
        if modify_distractors in ['oui', 'o', 'yes', 'y']:
            new_distractors = []
            for i in range(1, 4):
                d = input(f"Distracteur {i} (Enter pour terminer): ").strip()
                if not d:
                    break
                new_distractors.append(d)
            
            if new_distractors:
                self.df.at[idx, 'distractors_tex'] = '|'.join(new_distractors)
                modified_fields.append('distractors_tex')
        
        if modified_fields:
            self.modified = True
            print(f"\n✓ Question '{uid}' modifiée ({len(modified_fields)} champs).")
            return True
        else:
            print("\nAucune modification effectuée.")
            return False
    
    def list_questions(self, level=None, topic=None, limit=20):
        """Lister les questions avec filtres"""
        if self.df is None:
            return
        
        filtered = self.df.copy()
        
        if level:
            filtered = filtered[filtered['level'] == level]
        
        if topic:
            filtered = filtered[filtered['topic'].str.contains(topic, case=False, na=False)]
        
        print(f"\n{'UID':<30} {'Niveau':<8} {'Thème':<20} {'Difficulté':<10}")
        print("-"*80)
        
        for _, row in filtered.head(limit).iterrows():
            uid = str(row['uid'])[:28]
            level = str(row.get('level', 'N/A'))[:6]
            topic = str(row.get('topic', 'N/A'))[:18]
            difficulty = str(row.get('difficulty', 'N/A'))[:8]
            
            print(f"{uid:<30} {level:<8} {topic:<20} {difficulty:<10}")
        
        if len(filtered) > limit:
            print(f"\n... et {len(filtered) - limit} autres questions")
        
        print(f"\nTotal: {len(filtered)} questions\n")


def interactive_mode():
    """Mode interactif"""
    editor = QuestionEditor()
    
    if editor.df is None:
        print("Impossible de charger les données.")
        return
    
    print("\n" + "="*80)
    print("ÉDITEUR DE QUESTIONS - MODE INTERACTIF")
    print("="*80)
    
    while True:
        print("\n📋 Menu:")
        print("  1. Lister les questions")
        print("  2. Rechercher une question")
        print("  3. Afficher une question")
        print("  4. Ajouter une question")
        print("  5. Modifier une question")
        print("  6. Supprimer une question")
        print("  7. Supprimer plusieurs questions (liste)")
        print("  8. Sauvegarder et quitter")
        print("  9. Quitter sans sauvegarder")
        
        choice = input("\nChoix: ").strip()
        
        if choice == '1':
            level = input("Filtrer par niveau (Enter pour tous): ").strip() or None
            topic = input("Filtrer par thème (Enter pour tous): ").strip() or None
            editor.list_questions(level=level, topic=topic)
        
        elif choice == '2':
            search_term = input("Rechercher: ").strip()
            results = editor.search_question(search_term)
            print(f"\n{len(results)} résultat(s) trouvé(s):")
            for _, row in results.iterrows():
                print(f"  - {row['uid']}: {str(row['stem_tex'])[:60]}...")
        
        elif choice == '3':
            uid = input("UID de la question: ").strip()
            editor.display_question(uid)
        
        elif choice == '4':
            editor.add_question()
        
        elif choice == '5':
            uid = input("UID de la question à modifier: ").strip()
            editor.modify_question(uid)
        
        elif choice == '6':
            uid = input("UID de la question à supprimer: ").strip()
            editor.delete_question(uid)
        
        elif choice == '7':
            print("\n" + "="*80)
            print("SUPPRESSION MULTIPLE")
            print("="*80)
            print("Entrez les UIDs séparés par des virgules ou espaces")
            print("Ou depuis un fichier (une ligne par UID)")
            print("\nExemples:")
            print("  - FON3E001, FON3E002, FON3E003")
            print("  - FON3E001 FON3E002 FON3E003")
            print("  - @liste_uids.txt (pour charger depuis un fichier)")
            print("-"*80)
            
            uids_input = input("\nUIDs à supprimer: ").strip()
            
            if uids_input.startswith('@'):
                # Charger depuis un fichier
                file_path = uids_input[1:].strip()
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        uids_list = [line.strip() for line in f if line.strip()]
                    print(f"✓ {len(uids_list)} UIDs chargés depuis {file_path}")
                except Exception as e:
                    print(f"✗ Erreur lors de la lecture du fichier : {e}")
                    continue
            else:
                # Parser la liste (séparée par virgules ou espaces)
                if ',' in uids_input:
                    uids_list = [uid.strip() for uid in uids_input.split(',')]
                else:
                    uids_list = uids_input.split()
            
            if uids_list:
                editor.delete_multiple_questions(uids_list)
            else:
                print("✗ Aucun UID fourni.")
        
        elif choice == '8':
            if editor.modified:
                editor.save_data()
            print("\n✓ Au revoir!")
            break
        
        elif choice == '9':
            if editor.modified:
                confirm = input("⚠️  Des modifications non sauvegardées seront perdues. Confirmer ? (oui/non): ").strip().lower()
                if confirm not in ['oui', 'o', 'yes', 'y']:
                    continue
            print("\n✓ Au revoir!")
            break


def main():
    parser = argparse.ArgumentParser(description="Éditeur de questions")
    parser.add_argument("--csv", default="data/master_questions.csv", help="Fichier CSV")
    parser.add_argument("--delete", help="Supprimer une question par UID")
    parser.add_argument("--delete-multiple", help="Supprimer plusieurs questions (UIDs séparés par des virgules)")
    parser.add_argument("--delete-file", help="Supprimer les questions listées dans un fichier")
    parser.add_argument("--show", help="Afficher une question par UID")
    parser.add_argument("--list", action="store_true", help="Lister les questions")
    parser.add_argument("--level", help="Filtrer par niveau")
    parser.add_argument("--topic", help="Filtrer par thème")
    parser.add_argument("--interactive", "-i", action="store_true", help="Mode interactif")
    
    args = parser.parse_args()
    
    # Mode interactif explicite ou aucune action spécifiée
    if args.interactive:
        interactive_mode()
        return
    
    # Si aucune action spécifiée (sauf --csv), mode interactif par défaut
    has_action = args.delete or args.delete_multiple or args.delete_file or args.show or args.list
    if not has_action:
        interactive_mode()
        return
    
    editor = QuestionEditor(args.csv)
    
    if args.show:
        editor.display_question(args.show)
    
    elif args.delete:
        if editor.delete_question(args.delete):
            editor.save_data()
    
    elif args.delete_multiple:
        uids_list = [uid.strip() for uid in args.delete_multiple.split(',')]
        if editor.delete_multiple_questions(uids_list):
            editor.save_data()
    
    elif args.delete_file:
        try:
            with open(args.delete_file, 'r', encoding='utf-8') as f:
                uids_list = [line.strip() for line in f if line.strip()]
            print(f"✓ {len(uids_list)} UIDs chargés depuis {args.delete_file}")
            if editor.delete_multiple_questions(uids_list):
                editor.save_data()
        except Exception as e:
            print(f"✗ Erreur lors de la lecture du fichier : {e}")
    
    elif args.list:
        editor.list_questions(level=args.level, topic=args.topic)


if __name__ == "__main__":
    main()
