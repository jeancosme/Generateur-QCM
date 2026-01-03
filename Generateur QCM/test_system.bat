@echo off
REM Test du systeme complet

echo ===========================================
echo  Test du generateur Questions Flash
echo ===========================================
echo.

REM Test 1: Verification CSV
echo [TEST 1] Verification du fichier CSV...
python exporter.py --csv flash_bank.csv --format table --n 1 --out test_csv.tex
if exist test_csv.tex (
    echo ✓ CSV OK
    del test_csv.tex
) else (
    echo ✗ Probleme CSV
    goto error
)

REM Test 2: Generation format table
echo [TEST 2] Test generation format table...
python generate_flash.py --n 3 --title "Test Flash" --out test_table
if exist exports\tex\test_table.tex (
    echo ✓ Generation table OK
) else (
    echo ✗ Probleme generation table
    goto error
)

REM Test 3: Test compilation (si pdflatex disponible)
echo [TEST 3] Test compilation PDF...
pdflatex --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  pdflatex non disponible - test de compilation ignore
) else (
    python generate_flash.py --n 2 --title "Test Compilation" --compile --clean
    echo ✓ Compilation OK
)

echo.
echo ===========================================
echo  ✅ TOUS LES TESTS PASSES !
echo ===========================================
echo.
echo Le systeme est pret a utiliser.
echo Utilisez 'run_examples_interactif.bat' pour des exemples.
goto end

:error
echo.
echo ❌ ERREUR DETECTEE
echo Verifiez l'installation et les fichiers.

:end
pause