"""
API Backend pour le Générateur de QCM
FastAPI application principale
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import os
import sys
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules existants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Question, QuestionFilter
from api.services import QuestionService, GeneratorService


class SimpleGenerateRequest(BaseModel):
    """Modèle simplifié pour la génération depuis le frontend"""
    level: Optional[str] = None
    themes: Optional[List[str]] = None
    n_questions: int = 5
    difficulty: Optional[str] = None
    output_format: str = "pdf"
    include_answers: bool = True

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
async def generate_pdf(request: SimpleGenerateRequest):
    """
    Générer un PDF de questions flash
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        import tempfile
        
        # Récupérer les questions
        filters = QuestionFilter(
            level=[request.level] if request.level else None,
            topic=request.themes,
        )
        questions = question_service.get_questions(filters, request.n_questions, 0)
        
        # Créer un fichier PDF temporaire
        pdf_filename = f"qcm_{request.level or '3e'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exports", "pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        # Générer le PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # Titre
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2*cm, height - 2*cm, f"QCM - {request.level or '3e'}")
        
        if request.themes:
            c.setFont("Helvetica", 12)
            c.drawString(2*cm, height - 2.8*cm, f"Thèmes: {', '.join(request.themes)}")
        
        # Questions
        y_position = height - 4*cm
        c.setFont("Helvetica", 11)
        
        for i, q in enumerate(questions[:request.n_questions], 1):
            if y_position < 3*cm:  # Nouvelle page si nécessaire
                c.showPage()
                y_position = height - 2*cm
                c.setFont("Helvetica", 11)
            
            # Numéro et énoncé
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2*cm, y_position, f"Question {i}:")
            y_position -= 0.6*cm
            
            c.setFont("Helvetica", 10)
            # Simplifier le LaTeX pour le PDF (retirer les $)
            enonce_simple = q.stem_tex.replace("$", "")
            c.drawString(2.5*cm, y_position, enonce_simple[:80])
            
            y_position -= 0.5*cm
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(2.5*cm, y_position, f"[{q.topic} - Difficulte: {q.difficulty}]")
            
            y_position -= 1*cm
        
        c.save()
        
        # Retourner le fichier PDF
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=pdf_filename,
            headers={"Content-Disposition": f"attachment; filename={pdf_filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")


@app.post("/generate")
async def generate_pdf_noprefix(request: SimpleGenerateRequest):
    """Génération sans préfixe /api"""
    return await generate_pdf(request)


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


@app.get("/themes")
async def get_themes_legacy(level: Optional[str] = None):
    """Alias pour compatibilité frontend - récupérer les thèmes"""
    return question_service.get_unique_values("topic", level=level)


@app.get("/api/themes")
async def get_themes_api(level: Optional[str] = None):
    """Endpoint API pour récupérer les thèmes"""
    return question_service.get_unique_values("topic", level=level)


@app.get("/levels")
async def get_levels_legacy():
    """Alias pour compatibilité frontend - récupérer les niveaux"""
    return question_service.get_unique_values("level")


@app.get("/api/taxonomy")
async def get_taxonomy_api():
    """Récupérer la taxonomie complète"""
    try:
        taxonomy_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config", "taxonomie.json"
        )
        if os.path.exists(taxonomy_path):
            import json
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Fallback: construire la taxonomie depuis les données
        return {
            "levels": question_service.get_unique_values("level"),
            "topics": question_service.get_unique_values("topic"),
            "subtopics": question_service.get_unique_values("subtopic")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur taxonomie: {str(e)}")


@app.get("/questions/search")
async def search_questions(
    level: Optional[str] = Query(None),
    themes: Optional[List[str]] = Query(None),
    difficulty: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Recherche de questions avec filtres simplifiés"""
    filters = QuestionFilter(
        level=[level] if level else None,
        topic=themes,
        max_difficulty=difficulty
    )
    questions = question_service.get_questions(filters, limit, skip)
    
    # Formater les questions pour le frontend
    formatted_questions = []
    for q in questions:
        q_dict = {
            "uid": q.uid,
            "level": q.level,
            "theme": q.topic,  # Mapper topic -> theme
            "enonce": q.stem_tex,  # Mapper stem_tex -> enonce
            "difficulty": q.difficulty,
            "format": q.format,
            "subtopic": q.subtopic,
            "skill": q.skill,
            "time_s": q.time_s,
            "status": q.status
        }
        formatted_questions.append(q_dict)
    
    return {"questions": formatted_questions, "total": len(formatted_questions)}


@app.get("/api/questions/search")
async def search_questions_api(
    level: Optional[str] = Query(None),
    themes: Optional[List[str]] = Query(None),
    difficulty: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """Recherche de questions avec filtres simplifiés (via API)"""
    return await search_questions(level, themes, difficulty, skip, limit)


@app.get("/download/pdf/{filename}")
async def download_pdf(filename: str):
    """Télécharger un fichier PDF généré"""
    pdf_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "exports", "pdf", filename
    )
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Fichier PDF non trouvé")
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)


@app.get("/download/html/{filename}")
async def download_html(filename: str):
    """Télécharger un fichier HTML généré"""
    html_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "exports", "html", filename
    )
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Fichier HTML non trouvé")
    return FileResponse(html_path, media_type="text/html", filename=filename)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
