import argparse
import pandas as pd
import random
from datetime import datetime
from textwrap import dedent
import os
import sys

# -----------------------------
#  Arguments
# -----------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Exporteur de questions flash depuis une banque CSV.")
    p.add_argument("--csv", default="data/master_questions.csv", help="Chemin vers la banque CSV.")
    p.add_argument("--out", default=None, help="Chemin de sortie (fichier). Par défaut: ./exports/<format>/questions_<timestamp>.<ext>")
    p.add_argument("--format", default="tex", choices=["tex", "md", "html", "table"], help="Format d'export.")
    p.add_argument("--standalone", action="store_true", help="(TEX) Générer un document complet compilable.")
    p.add_argument("--title", default="Questions flash", help="Titre du document.")
    p.add_argument("--cols", type=int, default=2, help="(TEX) Nombre de colonnes pour le format standard.")
    p.add_argument("--n", type=int, default=8, help="Nombre de questions à exporter.")
    p.add_argument("--seed", type=int, default=42, help="Graine aléatoire (pour ordre reproductible).")
    p.add_argument("--level", nargs="*", help="Niveaux à inclure (ex: 3e 4e).")
    p.add_argument("--topic", nargs="*", help="Thèmes à inclure.")
    p.add_argument("--subtopic", nargs="*", help="Sous-thèmes à inclure.")
    p.add_argument("--skill", nargs="*", help="Compétences à inclure.")
    p.add_argument("--qformat", nargs="*", help="Formats de question (ex: court QCM).")
    p.add_argument("--max-difficulty", type=int, default=None, help="Difficulté max (1-5).")
    p.add_argument("--status", nargs="*", help="Statuts à inclure (ex: validé).")
    p.add_argument("--language", default=None, help="Langue (fr/en...).")
    p.add_argument("--no-answers", action="store_true", help="Ne pas ajouter le corrigé.")
    p.add_argument("--mode", default="modeqcm", choices=["modeqcm", "modelibre", "qfqcm", "qflibre"], help="Mode d'affichage: modeqcm/qfqcm (4 choix A,B,C,D) ou modelibre/qflibre (réponse libre).")
    return p.parse_args()

# -----------------------------
#  Chargement CSV
# -----------------------------
def load_bank(path):
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp1252")
    df = df.reset_index(drop=True)
    required = ["uid","level","topic","subtopic","skill","format","difficulty","time_s","stem_tex","answer_tex","distractors_tex","figure_url","tags","status","language"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"[Erreur] Colonnes manquantes dans le CSV: {missing}", file=sys.stderr)
        sys.exit(1)
    return df


# -----------------------------
#  Sélection
# -----------------------------
def filter_bank(df, args):
    q = df.copy()
    # Nettoyage des colonnes pour filtrage robuste
    for col in ["level", "topic", "subtopic", "skill", "format", "status", "language"]:
        if col in q.columns:
            q[col] = q[col].astype(str).str.strip().str.lower()
    # Filtrage avec nettoyage des arguments
    if args.level:
        levels = [l.strip().lower() for l in args.level]
        q = q[q["level"].isin(levels)]
    if args.topic:
        topics = [t.strip().lower() for t in args.topic]
        q = q[q["topic"].isin(topics)]
    if args.subtopic:
        subtopics = [s.strip().lower() for s in args.subtopic]
        q = q[q["subtopic"].isin(subtopics)]
    if args.skill:
        skills = [s.strip().lower() for s in args.skill]
        q = q[q["skill"].isin(skills)]
    if args.qformat:
        formats = [f.strip().lower() for f in args.qformat]
        q = q[q["format"].isin(formats)]
    if args.max_difficulty is not None:
        q = q[q["difficulty"] <= args.max_difficulty]
    if args.status:
        statuses = [s.strip().lower() for s in args.status]
        q = q[q["status"].isin(statuses)]
    if args.language:
        lang = args.language.strip().lower()
        q = q[q["language"] == lang]
    q = q.sample(frac=1, random_state=args.seed).reset_index(drop=True)
    return q.head(args.n)

# -----------------------------
#  Format TEX standard
# -----------------------------
def render_tex(questions, title, cols=2, with_answers=True, standalone=False):
    header = ""
    if standalone:
        header = (
            r"\documentclass[11pt]{article}" "\n"
            r"\usepackage[utf8]{inputenc}" "\n"
            r"\usepackage[T1]{fontenc}" "\n"
            r"\usepackage[french]{babel}" "\n"
            r"\usepackage[a4paper, margin=1.6cm]{geometry}" "\n"
            r"\usepackage{amsmath, amssymb}" "\n"
            r"\usepackage{multicol}" "\n"
            r"\usepackage{graphicx}" "\n"
            r"\usepackage{hyperref}" "\n"
            r"\setlength{\parskip}{0.5em}" "\n"
            r"\setlength{\parindent}{0pt}" "\n"
            r"\begin{document}" "\n"
            r"\begin{center}" "\n"
            f"  {{\\Large {title} }}\\\\[4pt]\n"
            f"  {{\\small Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}}}\n"
            r"\end{center}" "\n"
            r"\vspace{0.5em}" "\n"
            f"\\begin{{multicols}}{{{cols}}}\n"
        )
    else:
        header = f"\\begin{{multicols}}{{{cols}}}\n"

    body = ""
    for i, row in questions.reset_index(drop=True).iterrows():
        body += f"\\textbf{{Q{i+1}.}} {row['stem_tex']} \\\n"
        if str(row["format"]).lower() == "qcm":
            answer = str(row["answer_tex"]).strip()
            choices = [answer] + str(row["distractors_tex"]).split("|")
            rng = random.Random(1000 + i)
            rng.shuffle(choices)
            body += "\\begin{itemize}\n"
            for c in choices:
                c_clean = c.strip()
                # Mettre la bonne réponse en gras
                if c_clean == answer:
                    body += f"\\item \\textbf{{{c_clean}}}\n"
                else:
                    body += f"\\item {c_clean}\n"
            body += "\\end{itemize}\n"
        body += "\\vspace{0.5em}\n"

    footer = "\\end{multicols}\n"
    if with_answers:
        footer += "\\newpage\n\\section*{Corrigé}\n"
        for i, row in questions.reset_index(drop=True).iterrows():
            footer += f"\\textbf{{Q{i+1}.}} {row['answer_tex']} \\\\\n"
        footer += "\n"

    if standalone:
        footer += "\\end{document}"

    return header + body + footer

# -----------------------------
#  Format TABLE (nouveau)
# -----------------------------
def render_table_tex(questions, title="Questions Flash", standalone=True, mode="modeqcm"):
    """Rend un tableau LaTeX 4 colonnes (#, énoncé, réponse, jury) complet"""
    
    # Normaliser les modes (alias pour compatibilité)
    if mode in ["qfqcm"]: mode = "modeqcm"
    if mode in ["qflibre"]: mode = "modelibre"
    
    header = ""
    if standalone:
        header = dedent(r"""
        \documentclass[11pt,a4paper]{article}
        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage[french]{babel}
        \usepackage[a4paper,top=0.3cm,bottom=1cm,left=1cm,right=1cm]{geometry}
        \usepackage{array,booktabs}
        \usepackage{tabularx}
        \usepackage{amsmath,amssymb}
        \usepackage{graphicx}
        \usepackage{multirow}
        \usepackage{multicol}
        \usepackage{setspace}
        
        \setlength{\parindent}{0pt}
        \setlength{\parskip}{0.3em}
        \pagestyle{empty}
        
        \begin{document}
        
        \vspace*{-0.5cm}
        
        \begin{center}
            {\LARGE \textbf{""") + title + r"""}}\\[10pt]
        \end{center}
        
        \vspace{0.2cm}
        \noindent
        {\large Date : \underline{\hspace{2cm}} \hspace{3cm} Saison : \underline{\hspace{1.1cm}} \hspace{0.5cm} Épisode : \underline{\hspace{1.1cm}} \hfill Score : \underline{\hspace{1cm}} /5}
        
        \renewcommand{\arraystretch}{1.5}
        \setlength{\tabcolsep}{6pt}
        \setlength{\arrayrulewidth}{0.5pt}
        """
    
    # Début du tableau selon le mode
    if mode == "modeqcm":
        table_start = dedent(r"""
        \begin{center}
        \begin{tabular}{|p{0.8cm}|p{7.5cm}|p{7cm}|p{0.9cm}|@{}p{0cm}@{}}
        \hline
        \textbf{\#} & \textbf{Énoncé} & \textbf{Choix} & \textbf{Jury} & \\
        \hline
        """)
    else:  # modelibre
        table_start = dedent(r"""
        \begin{center}
        \begin{tabular}{|p{0.8cm}|p{7.5cm}|p{7cm}|p{0.9cm}|@{}p{0cm}@{}}
        \hline
        \textbf{\#} & \textbf{Énoncé} & \textbf{Réponse} & \textbf{Jury} & \\
        \hline
        """)
    
    # Corps du tableau
    body = ""
    import random
    for i, row in questions.reset_index(drop=True).iterrows():
        stem = str(row["stem_tex"]).replace("\n", " ").strip()
        
        if mode == "modeqcm":
            # Mode QCM : créer 4 choix A, B, C, D
            correct_answer = str(row["answer_tex"]).replace("\n", " ").strip()
            distractors = str(row.get("distractors_tex", "")).split("|")
            
            # Nettoyer les distracteurs
            distractors = [d.strip() for d in distractors if d.strip()] 
            
            # S'assurer d'avoir exactement 3 distracteurs
            while len(distractors) < 3:
                distractors.append("...")  # Placeholder si pas assez de distracteurs
            distractors = distractors[:3]  # Prendre seulement les 3 premiers
            
            # Créer la liste des 4 choix
            choices = [correct_answer] + distractors
            
            # Mélanger les choix de façon reproductible
            rng = random.Random(1000 + i)
            rng.shuffle(choices)
            
            # Détecter si des choix contiennent des fractions
            has_fractions = any("\\frac" in str(choice) for choice in choices)
            
            # Formater les choix A, B, C, D
            choice_text = ""
            if has_fractions:
                # Format en grille 2x2 pour les fractions
                formatted_choices = []
                for j, choice in enumerate(choices):
                    letter = chr(65 + j)  # A, B, C, D
                    # Wrapper le contenu en mode math si contient des commandes LaTeX
                    if "\\frac" in choice or "\\sqrt" in choice or "\\cdot" in choice:
                        choice_formatted = f"$\\Large {choice}$"  # Police encore plus grande pour les fractions
                    else:
                        choice_formatted = choice
                    formatted_choices.append(f"\\textbf{{{letter}.}} $\\square$ {choice_formatted}")
                
                # Organiser en grille 2x2 simple (compatible tabular)
                choice_text = (f"{formatted_choices[0]} \\hspace{{1cm}} {formatted_choices[1]} \\newline "
                              f"\\rule{{0pt}}{{0.15cm}} \\newline "
                              f"{formatted_choices[2]} \\hspace{{1cm}} {formatted_choices[3]}")
            else:
                # Format linéaire standard pour les autres
                for j, choice in enumerate(choices):
                    letter = chr(65 + j)  # A, B, C, D
                    # Wrapper le contenu en mode math si contient des commandes LaTeX
                    if "\\frac" in choice or "\\sqrt" in choice or "\\cdot" in choice:
                        choice_formatted = f"$\\Large {choice}$"  # Police encore plus grande pour les fractions
                    else:
                        choice_formatted = choice
                    choice_text += f"\\textbf{{{letter}.}} $\\square$ {choice_formatted}"
                    if j < len(choices) - 1:
                        choice_text += " \\newline "
            
            # Wrapper l'énoncé en mode math si nécessaire aussi
            if "\\frac" in stem or "\\sqrt" in stem or "\\cdot" in stem:
                stem_formatted = f"$\\Large {stem}$"  # Police encore plus grande pour les fractions dans l'énoncé
            else:
                stem_formatted = stem
            
            body += f"Q{i+1} & {stem_formatted} & {choice_text} & & \\\\ \n\\hline\n"
        else:
            # Mode libre : juste un espace pour la réponse
            # Wrapper l'énoncé en mode math si nécessaire aussi
            if "\\frac" in stem or "\\sqrt" in stem or "\\cdot" in stem:
                stem_formatted = f"$\\Large {stem}$"  # Police encore plus grande pour les fractions dans l'énoncé
            else:
                stem_formatted = stem
            body += f"Q{i+1} & {stem_formatted} & & & \\\\ \n\\hline\n"
    
    # Compléter jusqu'à 5 lignes si nécessaire
    num_questions = len(questions)
    if num_questions < 5:
        for i in range(num_questions, 5):
            body += f"Q{i+1} & & & & \\\\ \n\\hline\n"
    
    # Fin du tableau
    table_end = r"\end{tabular}" + "\n" + r"\end{center}"
    
    # Footer (plus besoin de score séparé)
    footer = ""
    
    # Deuxième fiche identique
    second_copy = dedent(r"""
    
    \vspace{0.3cm}
    
    \begin{center}
        {\LARGE \textbf{""") + title + r"""}}\\[10pt]
    \end{center}
    
    \vspace{0.2cm}
    \noindent
        {\large Date : \underline{\hspace{2cm}} \hspace{3cm} Saison : \underline{\hspace{1.1cm}} \hspace{0.5cm} Épisode : \underline{\hspace{1.1cm}} \hfill Score : \underline{\hspace{1cm}} /5}
    """ + table_start + body + table_end
    
    # Assemblage final
    full_content = header + table_start + body + table_end + footer + second_copy
    
    if standalone:
        full_content += "\n\\end{document}"
    
    return full_content

# -----------------------------
#  Formats MD + HTML
# -----------------------------
def render_md(questions, title, with_answers=True):
    out = f"# {title}\n\n_Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    for i, row in questions.reset_index(drop=True).iterrows():
        out += f"**Q{i+1}.** {row['stem_tex']}\n\n"
        if str(row["format"]).lower() == "qcm":
            choices = [str(row["answer_tex"])] + str(row["distractors_tex"]).split("|")
            rng = random.Random(1000 + i)
            rng.shuffle(choices)
            for c in choices:
                out += f"- {c.strip()}\n"
            out += "\n"
    if with_answers:
        out += "\n---\n\n## Corrigé\n\n"
        for i, row in questions.reset_index(drop=True).iterrows():
            out += f"**Q{i+1}.** {row['answer_tex']}\n\n"
    return out

def render_html(questions, title, with_answers=True):
    out = f"""<!DOCTYPE html>
<html lang="fr">
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; line-height: 1.4; }}
h1 {{ margin-top: 0; }}
.q {{ margin: 0 0 16px 0; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }}
.ans {{ background: #f7f7f7; padding: 12px; border-radius: 8px; }}
</style>
<h1>{title}</h1>
<p><em>Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}</em></p>
"""
    for i, row in questions.reset_index(drop=True).iterrows():
        out += f'<div class="q"><strong>Q{i+1}.</strong> {row["stem_tex"]}'
        if str(row["format"]).lower() == "qcm":
            choices = [str(row["answer_tex"])] + str(row["distractors_tex"]).split("|")
            rng = random.Random(1000 + i)
            rng.shuffle(choices)
            out += "<ul>" + "".join([f"<li>{c.strip()}</li>" for c in choices]) + "</ul>"
        out += "</div>\n"
    if with_answers:
        out += "<hr><h2>Corrigé</h2>\n"
        out += '<div class="ans">'
        for i, row in questions.reset_index(drop=False).iterrows():
            out += f"<p><strong>Q{i+1}.</strong> {row['answer_tex']}</p>\n"
        out += "</div>\n"
    out += "</html>"
    return out

# -----------------------------
#  Gestion des sorties
# -----------------------------
def ensure_out_path(path, ext):
    if path:
        return path
    os.makedirs(f"./exports/{ext}", exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"./exports/{ext}/questions_{stamp}.{ext}"

# -----------------------------
#  Main
# -----------------------------
def main():
    args = parse_args()
    df = load_bank(args.csv)
    print("[Diagnostic] Colonnes du CSV:", list(df.columns))
    print("[Diagnostic] Premières lignes:")
    print(df.head(10))
    print("[Diagnostic] Valeurs uniques level:", df['level'].unique())
    print("[Diagnostic] Valeurs uniques topic:", df['topic'].unique())
    print("[Diagnostic] Valeurs uniques subtopic:", df['subtopic'].unique())
    print("[Diagnostic] Valeurs uniques skill:", df['skill'].unique())
    print("[Diagnostic] Valeurs uniques format:", df['format'].unique())
    sel = filter_bank(df, args)
    if sel.empty:
        print("[Info] Aucun item ne correspond aux filtres. Vérifiez l'orthographe, la casse et les espaces dans le CSV et les arguments.")
        sys.exit(2)
    with_answers = not args.no_answers

    if args.format == "tex":
        content = render_tex(sel, args.title, cols=args.cols, with_answers=with_answers, standalone=args.standalone)
        out_path = ensure_out_path(args.out, "tex")
    elif args.format == "table":
        content = render_table_tex(sel, title=args.title, standalone=args.standalone, mode=args.mode)
        out_path = ensure_out_path(args.out, "tex")
    elif args.format == "md":
        content = render_md(sel, args.title, with_answers=with_answers)
        out_path = ensure_out_path(args.out, "md")
    else:
        content = render_html(sel, args.title, with_answers=with_answers)
        out_path = ensure_out_path(args.out, "html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(out_path)

if __name__ == "__main__":
    main()
