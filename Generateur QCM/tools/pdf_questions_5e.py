import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

CSV_PATH = "data/master_questions.csv"
PDF_PATH = "exports/tex/questions_5e_liste.pdf"


def get_5e_questions(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8')
    df5e = df[df['level'] == '5e']
    return df5e


def build_pdf(df, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("<b>Questions niveau 5e - QCM</b>", styles['Title']))
    story.append(Spacer(1, 0.5*cm))
    
    for idx, row in df.iterrows():
        uid = row.get('uid', f'Q{idx+1}')
        stem = str(row.get('stem_tex', ''))
        answer = str(row.get('answer_tex', ''))
        distractors = str(row.get('distractors_tex', '')).split('|') if pd.notna(row.get('distractors_tex')) else []
        
        # Préparer la liste des réponses (bonne + distracteurs)
        choices = [answer] + distractors
        # Surligner la bonne réponse
        table_data = []
        for i, choice in enumerate(choices):
            if i == 0:
                table_data.append([f"<b style='color:green'>✓ {choice}</b>"])
            else:
                table_data.append([f"✗ {choice}"])
        
        story.append(Paragraph(f"<b>ID:</b> {uid}", styles['Normal']))
        story.append(Paragraph(f"<b>Question:</b> {stem}", styles['Normal']))
        story.append(Spacer(1, 0.2*cm))
        t = Table(table_data, colWidths=[16*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.lightgreen),
            ('TEXTCOLOR', (0,0), (0,0), colors.darkgreen),
            ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))
    
    doc.build(story)
    print(f"✓ PDF généré : {pdf_path}")


def main():
    df5e = get_5e_questions(CSV_PATH)
    build_pdf(df5e, PDF_PATH)

if __name__ == "__main__":
    main()
