import pandas as pd
import argparse
from datetime import datetime
import os

def generate_review_html(csv_path, output_path=None):
    """Génère une page HTML interactive pour réviser les questions"""
    
    # Lire le fichier CSV
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"Chargé {len(df)} questions depuis {csv_path}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None
    
    # Générer le nom de fichier de sortie si non spécifié
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("./exports/html", exist_ok=True)
        output_path = f"./exports/html/review_{timestamp}.html"
    
    # Générer le HTML
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Révision Questions - {os.path.basename(csv_path)}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        
        .stats {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .filters {{
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .filter-group label {{
            font-size: 13px;
            font-weight: 600;
            color: #555;
        }}
        
        .filter-group select, .filter-group input {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            background: white;
        }}
        
        .question-card {{
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            background: white;
            transition: all 0.3s ease;
        }}
        
        .question-card:hover {{
            border-color: #3498db;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.15);
        }}
        
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .question-id {{
            font-weight: bold;
            font-size: 18px;
            color: #2c3e50;
        }}
        
        .question-meta {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 600;
            display: inline-block;
        }}
        
        .badge-level {{
            background: #3498db;
            color: white;
        }}
        
        .badge-topic {{
            background: #9b59b6;
            color: white;
        }}
        
        .badge-difficulty {{
            background: #e74c3c;
            color: white;
        }}
        
        .badge-difficulty-1 {{ background: #2ecc71; }}
        .badge-difficulty-2 {{ background: #f39c12; }}
        .badge-difficulty-3 {{ background: #e67e22; }}
        .badge-difficulty-4 {{ background: #e74c3c; }}
        .badge-difficulty-5 {{ background: #c0392b; }}
        
        .question-stem {{
            font-size: 18px;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            border-radius: 5px;
        }}
        
        .answers {{
            margin-top: 20px;
        }}
        
        .answer-item {{
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 6px;
            font-size: 16px;
        }}
        
        .answer-correct {{
            background: #d4edda;
            border: 2px solid #28a745;
            color: #155724;
            font-weight: 600;
        }}
        
        .answer-incorrect {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            color: #6c757d;
        }}
        
        .answer-label {{
            display: inline-block;
            width: 30px;
            font-weight: bold;
        }}
        
        .question-details {{
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
            font-size: 13px;
            color: #7f8c8d;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        
        .detail-item {{
            display: flex;
            gap: 5px;
        }}
        
        .detail-label {{
            font-weight: 600;
        }}
        
        .search-box {{
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #3498db;
        }}
        
        .hidden {{
            display: none !important;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 Révision des Questions</h1>
        <p style="color: #7f8c8d; margin-bottom: 20px;">Fichier : {os.path.basename(csv_path)} | Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
        
        <div class="stats">
            <div class="stat-item">
                <span class="stat-label">Total Questions</span>
                <span class="stat-value" id="total-count">{len(df)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Affichées</span>
                <span class="stat-value" id="visible-count">{len(df)}</span>
            </div>
        </div>
        
        <input type="text" class="search-box" id="search-box" placeholder="🔍 Rechercher dans les questions...">
        
        <div class="filters">
            <div class="filter-group">
                <label>Niveau</label>
                <select id="filter-level">
                    <option value="">Tous</option>
"""
    
    # Ajouter les options de niveau
    if 'level' in df.columns:
        for level in sorted(df['level'].dropna().unique()):
            html += f'                    <option value="{level}">{level}</option>\n'
    
    html += """                </select>
            </div>
            <div class="filter-group">
                <label>Thème</label>
                <select id="filter-topic">
                    <option value="">Tous</option>
"""
    
    # Ajouter les options de thème
    if 'topic' in df.columns:
        for topic in sorted(df['topic'].dropna().unique()):
            html += f'                    <option value="{topic}">{topic}</option>\n'
    
    html += """                </select>
            </div>
            <div class="filter-group">
                <label>Difficulté</label>
                <select id="filter-difficulty">
                    <option value="">Toutes</option>
                    <option value="1">1 - Facile</option>
                    <option value="2">2 - Moyen</option>
                    <option value="3">3 - Difficile</option>
                    <option value="4">4 - Très difficile</option>
                    <option value="5">5 - Expert</option>
                </select>
            </div>
        </div>
        
        <div id="questions-container">
"""
    
    # Générer les cartes de questions
    for idx, row in df.iterrows():
        uid = row.get('uid', f'Q{idx+1}')
        level = row.get('level', 'N/A')
        topic = row.get('topic', 'N/A')
        subtopic = row.get('subtopic', '')
        difficulty = row.get('difficulty', 'N/A')
        stem = str(row.get('stem_tex', '')).replace('\\', '\\\\')
        answer = str(row.get('answer_tex', '')).replace('\\', '\\\\')
        distractors = str(row.get('distractors_tex', '')).split('|') if pd.notna(row.get('distractors_tex')) else []
        
        html += f"""
        <div class="question-card" 
             data-level="{level}" 
             data-topic="{topic}" 
             data-difficulty="{difficulty}"
             data-search-text="{stem.lower()} {answer.lower()} {' '.join([d.lower() for d in distractors])}">
            <div class="question-header">
                <div class="question-id">{uid}</div>
                <div class="question-meta">
                    <span class="badge badge-level">{level}</span>
                    <span class="badge badge-topic">{topic}</span>
                    <span class="badge badge-difficulty badge-difficulty-{difficulty}">Difficulté {difficulty}</span>
                </div>
            </div>
            
            <div class="question-stem">
                {stem}
            </div>
            
            <div class="answers">
                <div class="answer-item answer-correct">
                    <span class="answer-label">✓</span> {answer}
                </div>
"""
        
        for i, distractor in enumerate(distractors):
            if distractor.strip():
                html += f"""                <div class="answer-item answer-incorrect">
                    <span class="answer-label">✗</span> {distractor.strip()}
                </div>
"""
        
        html += """            </div>
            
            <div class="question-details">
"""
        
        if pd.notna(row.get('subtopic')):
            html += f'                <div class="detail-item"><span class="detail-label">Sous-thème :</span> {row["subtopic"]}</div>\n'
        if pd.notna(row.get('skill')):
            html += f'                <div class="detail-item"><span class="detail-label">Compétence :</span> {row["skill"]}</div>\n'
        if pd.notna(row.get('time_s')):
            html += f'                <div class="detail-item"><span class="detail-label">Temps :</span> {row["time_s"]}s</div>\n'
        
        html += """            </div>
        </div>
"""
    
    html += """        </div>
        
        <div id="no-results" class="no-results hidden">
            Aucune question ne correspond aux critères sélectionnés.
        </div>
    </div>
    
    <script>
        // Filtrage et recherche
        const searchBox = document.getElementById('search-box');
        const filterLevel = document.getElementById('filter-level');
        const filterTopic = document.getElementById('filter-topic');
        const filterDifficulty = document.getElementById('filter-difficulty');
        const questions = document.querySelectorAll('.question-card');
        const noResults = document.getElementById('no-results');
        const visibleCount = document.getElementById('visible-count');
        
        function filterQuestions() {
            const searchTerm = searchBox.value.toLowerCase();
            const level = filterLevel.value;
            const topic = filterTopic.value;
            const difficulty = filterDifficulty.value;
            
            let visibleQuestions = 0;
            
            questions.forEach(card => {
                const cardLevel = card.dataset.level;
                const cardTopic = card.dataset.topic;
                const cardDifficulty = card.dataset.difficulty;
                const searchText = card.dataset.searchText;
                
                const matchesSearch = searchText.includes(searchTerm);
                const matchesLevel = !level || cardLevel === level;
                const matchesTopic = !topic || cardTopic === topic;
                const matchesDifficulty = !difficulty || cardDifficulty === difficulty;
                
                if (matchesSearch && matchesLevel && matchesTopic && matchesDifficulty) {
                    card.classList.remove('hidden');
                    visibleQuestions++;
                } else {
                    card.classList.add('hidden');
                }
            });
            
            visibleCount.textContent = visibleQuestions;
            
            if (visibleQuestions === 0) {
                noResults.classList.remove('hidden');
            } else {
                noResults.classList.add('hidden');
            }
        }
        
        searchBox.addEventListener('input', filterQuestions);
        filterLevel.addEventListener('change', filterQuestions);
        filterTopic.addEventListener('change', filterQuestions);
        filterDifficulty.addEventListener('change', filterQuestions);
        
        // Configuration MathJax pour les fractions LaTeX
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }
        };
    </script>
</body>
</html>
"""
    
    # Sauvegarder le fichier HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Fichier de révision généré : {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Générer une page HTML de révision pour les questions")
    parser.add_argument("--csv", default="data/master_questions.csv", help="Fichier CSV à réviser")
    parser.add_argument("--out", help="Fichier HTML de sortie (optionnel)")
    parser.add_argument("--open", action="store_true", help="Ouvrir automatiquement dans le navigateur")
    
    args = parser.parse_args()
    
    output_path = generate_review_html(args.csv, args.out)
    
    if output_path and args.open:
        import os
        os.startfile(output_path)
        print(f"📂 Ouverture dans le navigateur...")


if __name__ == "__main__":
    main()
