import csv
import sys

def generate_saison(master_csv, topic, subtopic, out_prefix="saison"):
    import subprocess
    # Charger les questions
    with open(master_csv, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        questions = [row for row in reader if row['topic'] == topic and row['subtopic'] == subtopic]
    # Trier par difficulté croissante
    questions.sort(key=lambda q: int(q['difficulty']))
    n = len(questions)
    if n < 7:
        print("Pas assez de questions pour une saison !")
        return
    # Répartition progressive
    entrainements = [[] for _ in range(6)]
    for i, q in enumerate(questions[:-1]):  # garder la dernière pour l'éval
        entrainements[i % 6].append(q)
    evaluation = [questions[-1]]  # la plus difficile ou la dernière
    # Sauvegarde et export PDF
    for i, entr in enumerate(entrainements, 1):
        csv_path = f"{out_prefix}_entrainement_{i}.csv"
        with open(csv_path, "w", encoding="utf-8", newline='') as out:
            writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(entr)
        # Export PDF
        pdf_title = f"Saison - Entraînement {i} ({topic} / {subtopic})"
        tex_cmd = [sys.executable, "exporter.py", "--csv", csv_path, "--format", "tex", "--standalone", "--title", pdf_title, "--out", f"exports/tex/{out_prefix}_entrainement_{i}.tex"]
        subprocess.run(tex_cmd)
        # Compiler en PDF
        tex_file = f"exports/tex/{out_prefix}_entrainement_{i}.tex"
        subprocess.run(["pdflatex", "-output-directory", "exports/tex", tex_file])
    # Evaluation
    eval_csv = f"{out_prefix}_evaluation.csv"
    with open(eval_csv, "w", encoding="utf-8", newline='') as out:
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(evaluation)
    pdf_title = f"Saison - Évaluation ({topic} / {subtopic})"
    tex_cmd = [sys.executable, "exporter.py", "--csv", eval_csv, "--format", "tex", "--standalone", "--title", pdf_title, "--out", f"exports/tex/{out_prefix}_evaluation.tex"]
    subprocess.run(tex_cmd)
    tex_file = f"exports/tex/{out_prefix}_evaluation.tex"
    subprocess.run(["pdflatex", "-output-directory", "exports/tex", tex_file])
    print("Saison générée ! Les PDF sont dans exports/tex/")

# Usage : python generate_saison.py master_questions.csv arithmetique decomposition
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_saison.py <master_csv> <topic> <subtopic>")
    else:
        generate_saison(sys.argv[1], sys.argv[2], sys.argv[3])
