
@echo off
REM Exemple Windows - Export LaTeX autonome pour 3e, 8 questions max diff 3
REM Assure-toi d'avoir Python dans le PATH (py -V) ou remplace "python" par "py"
python exporter.py --csv flash_bank.csv --format tex --standalone --title "Questions flash 3e" --level 3e --topic probabilites thales pythagore calcul_litteral --n 8 --max-difficulty 3
pause
