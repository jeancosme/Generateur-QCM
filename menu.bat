@echo off
REM Script de lancement rapide - Éditeur de Questions

echo.
echo ================================================
echo    EDITEUR DE QUESTIONS - MENU PRINCIPAL
echo ================================================
echo.
echo 1. Reviser les questions (HTML)
echo 2. Editer les questions (Mode interactif)
echo 3. Generer des flash cards
echo 4. Lister toutes les questions
echo 5. Quitter
echo.

choice /C 12345 /N /M "Votre choix : "

if errorlevel 5 goto :fin
if errorlevel 4 goto :lister
if errorlevel 3 goto :generer
if errorlevel 2 goto :editer
if errorlevel 1 goto :reviser

:reviser
echo.
echo Ouverture de la page de revision...
python tools\review_questions.py --open
goto :fin

:editer
echo.
echo Lancement de l'editeur interactif...
python tools\edit_questions.py -i
goto :fin

:generer
echo.
set /p niveau="Niveau (5e/4e/3e) : "
set /p theme="Theme (ex: fractions) : "
set /p mode="Mode (qfqcm/qflibre/qcm/libre) [qfqcm] : "
if "%mode%"=="" set mode=qfqcm

echo.
echo Generation en cours...
python generate_flash.py --level %niveau% --topic %theme% --mode %mode%
goto :fin

:lister
echo.
python tools\edit_questions.py --list
pause
goto :fin

:fin
echo.
echo Au revoir !
pause
