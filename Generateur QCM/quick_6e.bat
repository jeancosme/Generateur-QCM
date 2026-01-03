@echo off
REM Scripts rapides pour generer des fiches par niveau

REM Fiche 6e - Fractions et geometrie de base
echo Generating 6e worksheet...
python generate_flash.py --level 6e --topic fractions geometrie --max-difficulty 2 --n 5 --title "Questions Flash 6e" --compile --clean
echo Done: 6e worksheet created
echo.