@echo off
REM Scripts rapides pour generer des fiches par niveau

REM Fiche 4e - Equations et puissances
echo Generating 4e worksheet...
python generate_flash.py --level 4e --topic equations puissances geometrie --n 5 --title "Questions Flash 4e" --compile --clean
echo Done: 4e worksheet created
echo.