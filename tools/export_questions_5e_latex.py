import pandas as pd
from datetime import datetime
import os
import re

CSV_PATH = "data/master_questions.csv"
LATEX_PATH = "exports/tex/questions_5e_latex.tex"
PDF_PATH = "exports/tex/questions_5e_latex.pdf"


def latex_escape(text):
    """Échappe les caractères spéciaux LaTeX et corrige les fractions"""
    if not isinstance(text, str):
        return ''
    repl = [
        ('&', '\\&'),
        ('%', '\\%'),
        ('#', '\\#'),
        ('{', '\\{'),
        ('}', '\\}'),
    ]
    for a, b in repl:
        text = text.replace(a, b)
    text = text.replace('_', '\\_')
    # Corrige les fractions mal formées: \frac\{a\}\{b\} -> \frac{a}{b}
    text = re.sub(r'\\frac\\\{([^}]*)\\\}\\\{([^}]*)\\\}', r'\\frac{\1}{\2}', text)
    return text

# Only wrap full math expressions (with at least one operator or LaTeX command), always with single $...$
def wrap_math_fragments(s):
    if not isinstance(s, str):
        return s
    def mathify(m):
        frag = m.group(0)
        frag = frag.strip('$')
        return f'${frag}$'
    # Wrap \frac{...}{...}
    s = re.sub(r'(\\frac\{[^}]+\}\{[^}]+\})', mathify, s)
    # Only wrap expressions like 3(x + 2), x(x + 3), etc. as a single math fragment
    s = re.sub(r'([a-zA-Z0-9^_]+\([^\)]+\))', mathify, s)  # e.g. 3(x + 2)
    # Do NOT wrap any sub-expressions inside parentheses
    # Do NOT wrap single numbers or variables
    s = s.replace('$$', '$')
    s = s.replace('\u001b[0m', '')
    return s


def build_latex(df, latex_path):
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\geometry{margin=2cm}
\usepackage{xcolor}
\begin{document}
\section*{Questions niveau 5e - QCM}
""")
        for idx, row in df.iterrows():
            uid = latex_escape(row.get('uid', f'Q{idx+1}'))
            stem_raw = row.get('stem_tex', '')
            stem = wrap_math_fragments(latex_escape(stem_raw))
            answer_raw = row.get('answer_tex', '')
            answer = latex_escape(answer_raw)
            distractors = str(row.get('distractors_tex', '')).split('|') if pd.notna(row.get('distractors_tex')) else []
            choices_raw = [answer_raw] + distractors

            f.write("\\noindent\\textbf{ID:} %s\\\\\n" % uid)
            f.write("\\textbf{Question:} %s\\\\" % stem)
            f.write("\\begin{itemize}\n")
            for i, choice_raw in enumerate(choices_raw):
                choice = latex_escape(choice_raw)
                # Wrap math for choices if needed
                if re.search(r'(\\frac|\^|_|[0-9]|[+\-*/=])', choice):
                    choice = f'${choice}$'
                if i == 0:
                    # correct answer: bold + blue text
                    f.write("\\item \\textbf{\\textcolor{blue}{%s}}\n" % choice)
                else:
                    f.write("\\item %s\n" % choice)
            f.write("\\end{itemize}\n")
            f.write("\\vspace{0.5cm}\n")
        f.write(r"\end{document}")
    print(f"✓ Fichier LaTeX généré : {latex_path}")


def main():
    df = pd.read_csv(CSV_PATH, encoding='utf-8')
    df5e = df[df['level'] == '5e']
    build_latex(df5e, LATEX_PATH)
    print("Compilez le fichier avec pdflatex pour obtenir le PDF.")

if __name__ == "__main__":
    main()
