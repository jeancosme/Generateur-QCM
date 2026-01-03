@echo off
echo ===================================================
echo   GESTIONNAIRE DE BASE DE QUESTIONS - MENU RAPIDE
echo ===================================================
echo.

echo Choisissez une action:
echo.
echo [1] Fusionner tous les CSV et voir les statistiques
echo [2] Valider toute la base
echo [3] Exporter selon des criteres
echo [4] Ouvrir le gestionnaire complet
echo [5] Creer un template Excel
echo [0] Quitter
echo.

set /p choix="Votre choix (0-5): "

if "%choix%"=="1" goto stats
if "%choix%"=="2" goto validate
if "%choix%"=="3" goto export
if "%choix%"=="4" goto manager
if "%choix%"=="5" goto template
if "%choix%"=="0" goto fin
goto invalid

:stats
echo.
echo ^> Fusion des CSV et affichage des statistiques...
C:/Python313/python.exe -c "from scripts.database_manager import QuestionDatabase; db = QuestionDatabase(); db.merge_all_csv(); print(); db.get_statistics()"
goto fin

:validate
echo.
echo ^> Validation de la base de questions...
C:/Python313/python.exe -c "from scripts.database_manager import QuestionDatabase; db = QuestionDatabase(); db.validate_questions()"
goto fin

:export
echo.
set /p niveau="Niveau(x) (ex: 3e,4e) ou ENTREE pour tous: "
set /p theme="Theme(s) (ex: pythagore,thales) ou ENTREE pour tous: "
set /p difficulte="Difficulte max (1-5) ou ENTREE pour toutes: "
set /p nombre="Nombre max de questions ou ENTREE pour toutes: "

echo ^> Export en cours...
C:/Python313/python.exe -c "from scripts.database_manager import QuestionDatabase; db = QuestionDatabase(); db.export_by_criteria('%niveau%'.split(',') if '%niveau%' else None, '%theme%'.split(',') if '%theme%' else None, int('%difficulte%') if '%difficulte%'.isdigit() else None, int('%nombre%') if '%nombre%'.isdigit() else None)"
goto fin

:manager
echo.
echo ^> Lancement du gestionnaire complet...
C:/Python313/python.exe scripts/database_manager.py
goto fin

:template
echo.
echo ^> Creation d'un template Excel...
C:/Python313/python.exe tools/excel_converter.py template
goto fin

:invalid
echo.
echo Choix invalide. Veuillez choisir entre 0 et 5.
echo.
pause
goto debut

:fin
echo.
echo Termine !
pause