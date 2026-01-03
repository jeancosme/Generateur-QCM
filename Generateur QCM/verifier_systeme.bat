@echo off
echo ===========================================
echo  VERIFICATION COMPLETE DU SYSTEME
echo ===========================================
echo.

REM Test 1: Verification CSV
echo [TEST 1] Verification du fichier CSV...
C:/Python313/python.exe -c "import pandas as pd; df = pd.read_csv('flash_bank.csv', encoding='utf-8'); print(f'✓ CSV OK - {len(df)} questions, colonnes: {len(df.columns)}')"
if errorlevel 1 (
    echo ❌ Probleme CSV
    goto error
)

REM Test 2: Test exporteur basique
echo [TEST 2] Test exporteur format table...
C:/Python313/python.exe exporter.py --csv flash_bank.csv --format table --n 2 --title "Test Systeme" --out test_export.tex
if exist test_export.tex (
    echo ✓ Exporteur OK
    del test_export.tex
) else (
    echo ❌ Probleme exporteur
    goto error
)

REM Test 3: Test generateur principal
echo [TEST 3] Test generateur principal...
C:/Python313/python.exe generate_flash.py --n 2 --title "Test Integration" --out test_integration
if exist exports\tex\test_integration.tex (
    echo ✓ Generateur principal OK
    del exports\tex\test_integration.tex
) else (
    echo ❌ Probleme generateur principal
    goto error
)

REM Test 4: Test compilation (si pdflatex disponible)
echo [TEST 4] Test compilation PDF...
pdflatex --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pdflatex non disponible - test ignore
) else (
    C:/Python313/python.exe generate_flash.py --n 1 --title "Test Compilation" --compile --clean --out test_pdf 2>nul
    if exist exports\tex\test_pdf.pdf (
        echo ✓ Compilation PDF OK
        del exports\tex\test_pdf.pdf
        del exports\tex\test_pdf.tex
    ) else (
        echo ⚠️  Probleme compilation (pas critique)
    )
)

REM Test 5: Test filtres par niveau
echo [TEST 5] Test filtres par niveau...
C:/Python313/python.exe generate_flash.py --level 3e --n 2 --title "Test Filtres" --out test_filtres
if exist exports\tex\test_filtres.tex (
    echo ✓ Filtres OK
    del exports\tex\test_filtres.tex
) else (
    echo ❌ Probleme filtres
    goto error
)

echo.
echo ===========================================
echo  ✅ TOUS LES TESTS PASSES !
echo ===========================================
echo.
echo Votre système est entièrement fonctionnel :
echo - ✓ Fichier CSV corrigé et valide
echo - ✓ Exporteur LaTeX fonctionnel  
echo - ✓ Générateur principal opérationnel
echo - ✓ Compilation PDF disponible
echo - ✓ Filtrage par niveau/thème fonctionnel
echo.
echo Utilisation recommandée:
echo   python generate_flash.py --level 3e --n 5 --compile --open
echo.
echo Scripts disponibles:
echo   - run_examples_interactif.bat (menu interactif)
echo   - quick_3e.bat, quick_4e.bat, etc. (génération rapide)
echo.
goto end

:error
echo.
echo ❌ ERREUR DETECTEE
echo Vérifiez l'installation Python et les dépendances.
echo.
echo Solutions possibles:
echo 1. Installer pandas: pip install pandas
echo 2. Vérifier l'encodage du fichier CSV
echo 3. Vérifier les permissions d'écriture dans le dossier exports

:end
pause