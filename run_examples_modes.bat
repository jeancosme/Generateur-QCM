@echo off
REM ==============================================
REM  Generateur Questions Flash - Nouveaux Modes
REM ==============================================

echo.
echo ===================================================
echo   Generateur automatique Questions Flash v2.0
echo ===================================================
echo.

echo Choisissez d'abord le MODE d'affichage:
echo.
echo [A] Mode QCM - Choix multiples A, B, C, D
echo [B] Mode Libre - Reponse directe de l'eleve
echo.
set /p mode_choice="Mode (A ou B): "

if /i "%mode_choice%"=="A" (
    set mode=modeqcm
    set mode_name=QCM
) else (
    set mode=modelibre
    set mode_name=Libre
)

echo.
echo Mode selectionne: %mode_name%
echo.

echo Choisissez maintenant le contenu:
echo.
echo [1] Questions 3e - Thales et Pythagore (%mode_name%)
echo [2] Questions 4e - Equations et Puissances (%mode_name%) 
echo [3] Questions 6e - Fractions niveau facile (%mode_name%)
echo [4] Melange tous niveaux - difficulte max 2 (%mode_name%)
echo [5] Questions 3e - Probabilites et Statistiques (%mode_name%)
echo [6] Test rapide - 1 question aleatoire (%mode_name%)
echo [0] Quitter
echo.

set /p choix="Votre choix (0-6): "

if "%choix%"=="1" goto exemple1
if "%choix%"=="2" goto exemple2  
if "%choix%"=="3" goto exemple3
if "%choix%"=="4" goto exemple4
if "%choix%"=="5" goto exemple5
if "%choix%"=="6" goto exemple6
if "%choix%"=="0" goto fin
goto invalid

:exemple1
echo.
echo ^> Generation fiche 3e - Thales et Pythagore (%mode_name%)...
python generate_flash.py --level 3e --topic thales pythagore --n 5 --title "Evaluation 3e - Geometrie (%mode_name%)" --mode %mode% --compile --open --clean
goto fin

:exemple2
echo.
echo ^> Generation fiche 4e - Equations et Puissances (%mode_name%)...
python generate_flash.py --level 4e --topic equations puissances --n 4 --title "Controle 4e - Algebre (%mode_name%)" --mode %mode% --compile --open --clean  
goto fin

:exemple3
echo.
echo ^> Generation fiche 6e - Fractions niveau facile (%mode_name%)...
python generate_flash.py --level 6e --topic fractions --max-difficulty 2 --n 3 --title "Exercices 6e - Fractions (%mode_name%)" --mode %mode% --compile --open --clean
goto fin

:exemple4
echo.
echo ^> Generation fiche multi-niveaux - difficulte moderee (%mode_name%)...
python generate_flash.py --level 3e 4e 5e --max-difficulty 2 --n 5 --title "Questions Flash - Revision (%mode_name%)" --mode %mode% --compile --open --clean
goto fin

:exemple5
echo.
echo ^> Generation fiche 3e - Probabilites et Statistiques (%mode_name%)...
python generate_flash.py --level 3e --topic probabilites statistiques --n 3 --title "Evaluation 3e - Data (%mode_name%)" --mode %mode% --compile --open --clean
goto fin

:exemple6
echo.
echo ^> Test rapide - 1 question aleatoire (%mode_name%)...
python generate_flash.py --n 1 --title "Test Flash (%mode_name%)" --mode %mode% --compile --open --clean
goto fin

:invalid
echo.
echo Choix invalide. Veuillez choisir entre 0 et 6.
echo.
pause
goto fin

:fin
echo.
echo Termine !
pause