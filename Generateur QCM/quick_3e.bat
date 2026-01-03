@echo off
REM Scripts rapides pour generer des fiches par niveau

echo Choisissez le mode:
echo [1] Mode QCM (choix A,B,C,D)
echo [2] Mode libre (reponse directe)
set /p mode_choice="Votre choix (1-2): "

if "%mode_choice%"=="1" (
    set mode=modeqcm
    set mode_name=QCM
) else (
    set mode=modelibre  
    set mode_name=Libre
)

REM Fiche 3e - Thales, Pythagore, Probabilites, Calcul litteral
echo Generating 3e worksheet %mode_name%...
python generate_flash.py --level 3e --topic thales pythagore probabilites calcul_litteral statistiques --n 5 --title "Questions Flash 3e - %mode_name%" --mode %mode% --compile --clean
echo Done: 3e worksheet created
echo.