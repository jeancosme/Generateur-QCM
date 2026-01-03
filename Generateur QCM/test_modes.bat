@echo off
echo =====================================
echo  TEST DES NOUVEAUX MODES QCM/LIBRE
echo =====================================
echo.

echo [TEST 1] Mode QCM avec choix A, B, C, D...
C:/Python313/python.exe generate_flash.py --level 3e --n 3 --title "Test Mode QCM" --mode modeqcm --out test_qcm --compile
echo.

echo [TEST 2] Mode libre sans propositions...
C:/Python313/python.exe generate_flash.py --level 3e --n 3 --title "Test Mode Libre" --mode modelibre --out test_libre --compile
echo.

echo Tests termines !
echo Verifiez les PDFs generes dans exports/tex/
pause