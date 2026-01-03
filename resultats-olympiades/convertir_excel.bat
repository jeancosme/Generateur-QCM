@echo off
chcp 65001 >nul
echo ============================================================
echo 🔄 Conversion Excel vers JSON
echo ============================================================
echo.
echo Cette commande va convertir Résultats.xlsx en data.js
echo.
pause
echo.

C:\Python313\python.exe convert_excel_to_json.py

echo.
echo ============================================================
echo Conversion terminée !
echo ============================================================
echo.
pause