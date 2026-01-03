@echo off
REM Scripts rapides pour generer des fiches par niveau

REM Fiche 5e - Nombres relatifs
echo Generating 5e worksheet...
python generate_flash.py --level 5e --topic nombres_relatifs --n 4 --title "Questions Flash 5e - Relatifs" --compile --clean
echo Done: 5e worksheet created
echo.