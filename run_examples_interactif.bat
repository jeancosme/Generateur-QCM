@echo off
REM ==============================================
REM  Generateur Questions Flash - Exemples
REM ==============================================

echo.
echo ================================================
echo   Generateur automatique Questions Flash
echo ================================================
echo.

echo Choisissez un exemple:
echo.
echo [1] Questions 3e - Thales et Pythagore (5 questions)
echo [2] Questions 4e - Equations et Puissances (4 questions) 
echo [3] Questions 6e - Fractions niveau facile (3 questions)
echo [4] Melange tous niveaux - difficulte max 2 (5 questions)
echo [5] Questions 3e - Probabilites et Statistiques (3 questions)
echo [6] Test rapide - 1 question aleatoire
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
echo ^> Generation fiche 3e - Thales et Pythagore...
python generate_flash.py --level 3e --topic thales pythagore --n 5 --title "Evaluation 3e - Geometrie" --compile --open --clean
goto fin

:exemple2
echo.
echo ^> Generation fiche 4e - Equations et Puissances...
python generate_flash.py --level 4e --topic equations puissances --n 4 --title "Controle 4e - Algebre" --compile --open --clean  
goto fin

:exemple3
echo.
echo ^> Generation fiche 6e - Fractions niveau facile...
python generate_flash.py --level 6e --topic fractions --max-difficulty 2 --n 3 --title "Exercices 6e - Fractions" --compile --open --clean
goto fin

:exemple4
echo.
echo ^> Generation fiche multi-niveaux - difficulte moderee...
python generate_flash.py --level 3e 4e 5e --max-difficulty 2 --n 5 --title "Questions Flash - Revision" --compile --open --clean
goto fin

:exemple5
echo.
echo ^> Generation fiche 3e - Probabilites et Statistiques...
python generate_flash.py --level 3e --topic probabilites statistiques --n 3 --title "Evaluation 3e - Data" --compile --open --clean
goto fin

:exemple6
echo.
echo ^> Test rapide - 1 question aleatoire...
python generate_flash.py --n 1 --title "Test Flash" --compile --open --clean
goto fin

:invalid
echo.
echo Choix invalide. Veuillez choisir entre 0 et 6.
echo.
pause
goto debut

:fin
echo.
echo Termine !
pause