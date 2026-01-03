#!/usr/bin/env python3
"""
Script d'intégration pour générer automatiquement des fiches Questions Flash.
Ce script combine l'exporteur avec la compilation LaTeX pour un workflow complet.
"""

import argparse
import subprocess
import os
import sys
from datetime import datetime
from exporter import main as export_main, parse_args as export_parse_args

def parse_args():
    """Parse les arguments pour le générateur de fiches flash"""
    p = argparse.ArgumentParser(
        description="Générateur automatique de fiches Questions Flash",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python generate_flash.py --level 3e --topic thales pythagore --n 5
  python generate_flash.py --level 4e 5e --max-difficulty 2 --compile
  python generate_flash.py --level 6e --topic fractions --title "Évaluation fractions 6e"
        """
    )
    
    # Arguments du générateur
    p.add_argument("--csv", default="data/master_questions.csv", help="Banque de questions CSV")
    p.add_argument("--title", default="Questions Flash", help="Titre de la fiche")
    p.add_argument("--n", type=int, default=5, help="Nombre de questions (max 5 pour format table)")
    p.add_argument("--level", nargs="*", help="Niveaux à inclure (ex: 3e 4e)")
    p.add_argument("--topic", nargs="*", help="Thèmes à inclure") 
    p.add_argument("--subtopic", nargs="*", help="Sous-thèmes à inclure")
    p.add_argument("--skill", nargs="*", help="Compétences à inclure")
    p.add_argument("--qformat", nargs="*", help="Formats de question (ex: court QCM)")
    p.add_argument("--max-difficulty", type=int, help="Difficulté max (1-5)")
    p.add_argument("--seed", type=int, default=42, help="Graine aléatoire")
    
    # Arguments de sortie
    p.add_argument("--out", help="Fichier de sortie (sans extension)")
    p.add_argument("--compile", action="store_true", help="Compiler automatiquement en PDF")
    p.add_argument("--open", action="store_true", help="Ouvrir le PDF après compilation")
    p.add_argument("--clean", action="store_true", help="Nettoyer les fichiers temporaires LaTeX")
    p.add_argument("--mode", default="modeqcm", choices=["modeqcm", "modelibre", "qfqcm", "qflibre"], help="Mode d'affichage: modeqcm/qfqcm (4 choix A,B,C,D) ou modelibre/qflibre (réponse libre)")
    
    return p.parse_args()

def generate_filename(args):
    """Génère un nom de fichier basé sur les paramètres"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construire le nom basé sur les filtres
    parts = ["questions"]
    if args.level:
        parts.append("-".join(args.level))
    if args.topic:
        parts.append("-".join(args.topic[:2]))  # Limiter à 2 thèmes max dans le nom
    
    filename = "_".join(parts) + f"_{timestamp}"
    return filename

def run_exporter(args):
    """Exécute l'exporteur avec les paramètres donnés"""
    
    # Générer le nom de fichier si pas spécifié
    if not args.out:
        filename = generate_filename(args)
        args.out = f"./exports/tex/{filename}.tex"
    else:
        # Si un nom est fourni sans répertoire, l'ajouter dans exports/tex
        if os.path.dirname(args.out) == "":
            args.out = f"./exports/tex/{args.out}"
        if not args.out.endswith('.tex'):
            args.out += ".tex"
    
    # S'assurer que le répertoire existe
    out_dir = os.path.dirname(args.out)
    if out_dir:  # Only create directory if there's actually a directory component
        os.makedirs(out_dir, exist_ok=True)
    
    # Préparer les arguments pour l'exporteur
    export_args = [
        "--csv", args.csv,
        "--format", "table",
        "--standalone",
        "--title", args.title,
        "--n", str(min(args.n, 5)),  # Limiter à 5 pour le format table
        "--seed", str(args.seed),
        "--out", args.out,
        "--mode", args.mode
    ]
    
    if args.level:
        export_args.extend(["--level"] + args.level)
    if args.topic:
        export_args.extend(["--topic"] + args.topic)
    if args.subtopic:
        export_args.extend(["--subtopic"] + args.subtopic)
    if args.skill:
        export_args.extend(["--skill"] + args.skill)
    if args.qformat:
        export_args.extend(["--qformat"] + args.qformat)
    if args.max_difficulty:
        export_args.extend(["--max-difficulty", str(args.max_difficulty)])
    
    # Simuler sys.argv pour l'exporteur
    original_argv = sys.argv
    sys.argv = ["exporter.py"] + export_args
    
    try:
        # Importer et exécuter l'exporteur
        from exporter import main as export_main
        export_main()
        print(f"✓ Fiche générée: {args.out}")
        return args.out
    except SystemExit as e:
        if e.code == 2:
            print("❌ Aucune question ne correspond aux filtres spécifiés.")
            return None
        elif e.code == 1:
            print("❌ Erreur dans le fichier CSV.")
            return None
        else:
            raise
    finally:
        sys.argv = original_argv

def compile_pdf(tex_file):
    """Compile le fichier LaTeX en PDF"""
    if not os.path.exists(tex_file):
        print(f"❌ Fichier {tex_file} introuvable")
        return None
    
    # Changer vers le répertoire du fichier LaTeX
    tex_dir = os.path.dirname(tex_file)
    tex_basename = os.path.basename(tex_file)
    original_dir = os.getcwd()
    
    try:
        os.chdir(tex_dir)
        
        # Essayer pdflatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_basename],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pdf_file = tex_basename.replace('.tex', '.pdf')
            print(f"✓ PDF compilé: {os.path.join(tex_dir, pdf_file)}")
            return os.path.join(tex_dir, pdf_file)
        else:
            print("❌ Erreur de compilation LaTeX:")
            print(result.stdout)
            print(result.stderr)
            return None
            
    except FileNotFoundError:
        print("❌ pdflatex non trouvé. Installez MiKTeX, TeX Live ou TinyTeX.")
        return None
    finally:
        os.chdir(original_dir)

def clean_latex_files(tex_file):
    """Nettoie les fichiers temporaires LaTeX"""
    base = tex_file.replace('.tex', '')
    extensions = ['.aux', '.log', '.out', '.synctex.gz']
    
    for ext in extensions:
        temp_file = base + ext
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"🗑️  Supprimé: {os.path.basename(temp_file)}")

def open_file(file_path):
    """Ouvre le fichier avec l'application par défaut"""
    if os.name == 'nt':  # Windows
        os.startfile(file_path)
    elif os.name == 'posix':  # macOS et Linux
        subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', file_path])

def main():
    args = parse_args()
    
    print("🚀 Générateur automatique de fiches Questions Flash")
    print("=" * 50)
    
    # Générer le fichier LaTeX
    tex_file = run_exporter(args)
    if not tex_file:
        sys.exit(1)
    
    # Compiler en PDF si demandé
    pdf_file = None
    if args.compile:
        print("\n📄 Compilation en PDF...")
        pdf_file = compile_pdf(tex_file)
        
        # Nettoyer les fichiers temporaires si demandé
        if args.clean and pdf_file:
            print("\n🧹 Nettoyage des fichiers temporaires...")
            clean_latex_files(tex_file)
    
    # Ouvrir le fichier si demandé
    if args.open:
        file_to_open = pdf_file if pdf_file else tex_file
        if file_to_open:
            print(f"\n📂 Ouverture de {os.path.basename(file_to_open)}...")
            open_file(file_to_open)
    
    print("\n✅ Terminé!")

if __name__ == "__main__":
    main()