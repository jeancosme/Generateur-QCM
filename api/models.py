"""
Modèles de données pour l'API
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Question(BaseModel):
    """Modèle de question"""
    uid: str = Field(..., description="Identifiant unique")
    level: str = Field(..., description="Niveau (3e, 4e, 5e, 6e)")
    topic: str = Field(..., description="Thème principal")
    subtopic: str = Field(..., description="Sous-thème")
    skill: str = Field(..., description="Compétence visée")
    format: str = Field(..., description="Format de question (court, QCM)")
    difficulty: int = Field(..., ge=1, le=5, description="Difficulté (1-5)")
    time_s: int = Field(..., description="Temps estimé en secondes")
    stem_tex: str = Field(..., description="Énoncé en LaTeX")
    answer_tex: str = Field(..., description="Réponse correcte en LaTeX")
    distractors_tex: str = Field(..., description="Distracteurs (séparés par ;)")
    figure_url: str = Field(default="", description="URL de la figure")
    tags: str = Field(default="", description="Tags (séparés par ,)")
    status: str = Field(default="draft", description="Statut (draft, validé, archivé)")
    language: str = Field(default="fr", description="Langue")
    
    class Config:
        json_schema_extra = {
            "example": {
                "uid": "3e_thales_001",
                "level": "3e",
                "topic": "thales",
                "subtopic": "calcul_longueur",
                "skill": "calculer",
                "format": "court",
                "difficulty": 3,
                "time_s": 60,
                "stem_tex": "Dans le triangle ABC, (DE) est parallèle à (BC). Calculer DE.",
                "answer_tex": "4,5",
                "distractors_tex": "3,5;5,5;6",
                "figure_url": "",
                "tags": "géométrie,théorème",
                "status": "validé",
                "language": "fr"
            }
        }


class QuestionFilter(BaseModel):
    """Filtres pour la recherche de questions"""
    level: Optional[List[str]] = None
    topic: Optional[List[str]] = None
    subtopic: Optional[List[str]] = None
    skill: Optional[List[str]] = None
    max_difficulty: Optional[int] = None
    status: Optional[List[str]] = None
    language: Optional[str] = None


class GenerateRequest(BaseModel):
    """Requête de génération de PDF"""
    title: str = Field(default="Questions Flash", description="Titre du document")
    n: int = Field(default=5, ge=1, le=20, description="Nombre de questions")
    filters: QuestionFilter = Field(default_factory=QuestionFilter, description="Filtres de sélection")
    mode: str = Field(default="qfqcm", description="Mode (qfqcm, qflibre, modeqcm, modelibre)")
    seed: int = Field(default=42, description="Graine aléatoire")
    with_answers: bool = Field(default=True, description="Inclure les réponses")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Évaluation Théorème de Thalès",
                "n": 5,
                "filters": {
                    "level": ["3e"],
                    "topic": ["thales"],
                    "max_difficulty": 3
                },
                "mode": "qfqcm",
                "seed": 42,
                "with_answers": True
            }
        }


class Statistics(BaseModel):
    """Statistiques sur la base de questions"""
    total_questions: int
    by_level: dict
    by_topic: dict
    by_difficulty: dict
    by_status: dict
