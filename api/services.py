"""
Services métier pour l'API
"""
import pandas as pd
import os
import sys
import subprocess
from typing import List, Optional, Dict
from datetime import datetime
import shutil

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Question, QuestionFilter, GenerateRequest, Statistics


class QuestionService:
    """Service de gestion des questions"""
    
    def __init__(self, csv_path: str = "data/master_questions.csv"):
        self.csv_path = csv_path
        self.df = self._load_csv()
    
    def _load_csv(self) -> pd.DataFrame:
        """Charger le fichier CSV"""
        try:
            df = pd.read_csv(self.csv_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(self.csv_path, encoding="cp1252")
        return df.fillna("")
    
    def _save_csv(self):
        """Sauvegarder le fichier CSV avec backup"""
        # Créer un backup
        backup_dir = "data/backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"master_questions_backup_{timestamp}.csv")
        shutil.copy(self.csv_path, backup_path)
        
        # Sauvegarder
        self.df.to_csv(self.csv_path, index=False, encoding="utf-8")
    
    def _apply_filters(self, filters: QuestionFilter) -> pd.DataFrame:
        """Appliquer les filtres sur le DataFrame"""
        df = self.df.copy()
        
        # Normaliser pour filtrage
        for col in ["level", "topic", "subtopic", "skill", "status", "language"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.lower()
        
        if filters.level:
            levels = [l.strip().lower() for l in filters.level]
            df = df[df["level"].isin(levels)]
        
        if filters.topic:
            topics = [t.strip().lower() for t in filters.topic]
            df = df[df["topic"].isin(topics)]
        
        if filters.subtopic:
            subtopics = [s.strip().lower() for s in filters.subtopic]
            df = df[df["subtopic"].isin(subtopics)]
        
        if filters.skill:
            skills = [s.strip().lower() for s in filters.skill]
            df = df[df["skill"].isin(skills)]
        
        if filters.max_difficulty:
            df = df[df["difficulty"] <= filters.max_difficulty]
        
        if filters.status:
            statuses = [s.strip().lower() for s in filters.status]
            df = df[df["status"].isin(statuses)]
        
        if filters.language:
            df = df[df["language"] == filters.language.strip().lower()]
        
        return df
    
    def get_questions(self, filters: QuestionFilter, limit: int = 100, offset: int = 0) -> List[Question]:
        """Récupérer les questions avec filtres"""
        df = self._apply_filters(filters)
        df = df.iloc[offset:offset+limit]
        
        questions = []
        for _, row in df.iterrows():
            questions.append(Question(**row.to_dict()))
        
        return questions
    
    def get_question_by_id(self, uid: str) -> Optional[Question]:
        """Récupérer une question par son UID"""
        df = self.df[self.df["uid"] == uid]
        if df.empty:
            return None
        
        return Question(**df.iloc[0].to_dict())
    
    def create_question(self, question: Question) -> Question:
        """Créer une nouvelle question"""
        # Vérifier si l'UID existe déjà
        if not self.df[self.df["uid"] == question.uid].empty:
            raise ValueError(f"Une question avec l'UID {question.uid} existe déjà")
        
        # Ajouter la question
        new_row = pd.DataFrame([question.model_dump()])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self._save_csv()
        
        return question
    
    def update_question(self, uid: str, question: Question) -> Optional[Question]:
        """Mettre à jour une question"""
        idx = self.df[self.df["uid"] == uid].index
        if len(idx) == 0:
            return None
        
        # Mettre à jour
        for key, value in question.model_dump().items():
            self.df.at[idx[0], key] = value
        
        self._save_csv()
        return question
    
    def delete_question(self, uid: str) -> bool:
        """Supprimer une question"""
        initial_len = len(self.df)
        self.df = self.df[self.df["uid"] != uid]
        
        if len(self.df) < initial_len:
            self._save_csv()
            return True
        
        return False
    
    def get_statistics(self) -> Statistics:
        """Calculer les statistiques"""
        return Statistics(
            total_questions=len(self.df),
            by_level=self.df["level"].value_counts().to_dict(),
            by_topic=self.df["topic"].value_counts().to_dict(),
            by_difficulty=self.df["difficulty"].value_counts().to_dict(),
            by_status=self.df["status"].value_counts().to_dict()
        )
    
    def get_unique_values(self, column: str, **filters) -> List[str]:
        """Récupérer les valeurs uniques d'une colonne"""
        df = self.df.copy()
        
        # Appliquer les filtres additionnels
        for key, value in filters.items():
            if value and key in df.columns:
                df = df[df[key].str.lower() == value.lower()]
        
        values = df[column].dropna().unique().tolist()
        return sorted([str(v) for v in values if v])


class GeneratorService:
    """Service de génération de documents"""
    
    def __init__(self):
        self.exports_dir = "exports/tex"
        os.makedirs(self.exports_dir, exist_ok=True)
    
    def generate_pdf(self, request: GenerateRequest) -> str:
        """Générer un PDF à partir d'une requête"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Construire le nom de fichier
        filename_parts = ["questions"]
        if request.filters.level:
            filename_parts.append("-".join(request.filters.level))
        if request.filters.topic:
            filename_parts.append("-".join(request.filters.topic[:2]))
        
        filename = "_".join(filename_parts) + f"_{timestamp}"
        tex_path = os.path.join(self.exports_dir, f"{filename}.tex")
        pdf_path = os.path.join(self.exports_dir, f"{filename}.pdf")
        
        # Préparer les arguments pour generate_flash.py
        args = [
            sys.executable,
            "generate_flash.py",
            "--title", request.title,
            "--n", str(request.n),
            "--seed", str(request.seed),
            "--mode", request.mode,
            "--out", filename,
            "--compile",
        ]
        
        if request.filters.level:
            args.extend(["--level"] + request.filters.level)
        if request.filters.topic:
            args.extend(["--topic"] + request.filters.topic)
        if request.filters.subtopic:
            args.extend(["--subtopic"] + request.filters.subtopic)
        if request.filters.skill:
            args.extend(["--skill"] + request.filters.skill)
        if request.filters.max_difficulty:
            args.extend(["--max-difficulty", str(request.filters.max_difficulty)])
        if request.filters.status:
            args.extend(["--status"] + request.filters.status)
        
        # Exécuter generate_flash.py
        result = subprocess.run(args, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Erreur de génération: {result.stderr}")
        
        return pdf_path
