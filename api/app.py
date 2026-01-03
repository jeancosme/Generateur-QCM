"""
API Backend pour le Générateur de QCM
FastAPI application principale
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import pandas as pd
import os
import sys
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules existants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Question, QuestionFilter, GenerateRequest
from api.services import QuestionService, GeneratorService

app = FastAPI(
    title="Générateur de QCM API",
    description="API pour générer des questionnaires mathématiques personnalisés",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
question_service = QuestionService()
generator_service = GeneratorService()

# Servir les fichiers statiques du frontend
web_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
if os.path.exists(web_path):
    app.mount("/static", StaticFiles(directory=web_path), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Servir la page d'accueil de l'application web"""
    index_path = os.path.join(web_path, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # Fallback API info
    return {
        "message": "Générateur de QCM API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "questions": "/api/questions",
            "generate": "/api/generate",
            "stats": "/api/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de santé pour Docker healthcheck"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/questions", response_model=List[Question])
async def get_questions(
    level: Optional[List[str]] = Query(None, description="Niveaux (ex: 3e, 4e, 5e)"),
    topic: Optional[List[str]] = Query(None, description="Thèmes"),
    subtopic: Optional[List[str]] = Query(None, description="Sous-thèmes"),
    skill: Optional[List[str]] = Query(None, description="Compétences"),
    max_difficulty: Optional[int] = Query(None, ge=1, le=5, description="Difficulté max (1-5)"),
    status: Optional[List[str]] = Query(None, description="Statuts"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max de résultats"),
    offset: int = Query(0, ge=0, description="Décalage pour pagination")
):
    """
    Récupérer la liste des questions avec filtres optionnels
    """
    filters = QuestionFilter(
        level=level,
        topic=topic,
        subtopic=subtopic,
        skill=skill,
        max_difficulty=max_difficulty,
        status=status
    )
    
    questions = question_service.get_questions(filters, limit, offset)
    return questions


@app.get("/api/questions/{question_id}", response_model=Question)
async def get_question(question_id: str):
    """
    Récupérer une question spécifique par son UID
    """
    question = question_service.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return question


@app.post("/api/questions", response_model=Question, status_code=201)
async def create_question(question: Question):
    """
    Créer une nouvelle question
    """
    try:
        new_question = question_service.create_question(question)
        return new_question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/api/questions/{question_id}", response_model=Question)
async def update_question(question_id: str, question: Question):
    """
    Mettre à jour une question existante
    """
    try:
        updated_question = question_service.update_question(question_id, question)
        if not updated_question:
            raise HTTPException(status_code=404, detail="Question non trouvée")
        return updated_question
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/questions/{question_id}")
async def delete_question(question_id: str):
    """
    Supprimer une question
    """
    success = question_service.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    return {"message": "Question supprimée avec succès"}


@app.post("/api/generate")
async def generate_pdf(request: GenerateRequest):
    """
    Générer un PDF de questions flash
    """
    try:
        pdf_path = generator_service.generate_pdf(request)
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="Erreur lors de la génération du PDF")
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@app.get("/api/stats")
async def get_statistics():
    """
    Récupérer des statistiques sur la base de questions
    """
    stats = question_service.get_statistics()
    return stats


@app.get("/api/levels")
async def get_levels():
    """
    Récupérer la liste des niveaux disponibles
    """
    return question_service.get_unique_values("level")


@app.get("/api/topics")
async def get_topics(level: Optional[str] = None):
    """
    Récupérer la liste des thèmes disponibles
    """
    return question_service.get_unique_values("topic", level=level)


@app.get("/api/subtopics")
async def get_subtopics(topic: Optional[str] = None):
    """
    Récupérer la liste des sous-thèmes disponibles
    """
    return question_service.get_unique_values("subtopic", topic=topic)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
