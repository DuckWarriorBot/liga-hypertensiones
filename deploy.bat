@echo off
title Liga Hypertensiones - Deploy
echo.
echo  === Deploy Liga Hypertensiones ===
echo.
python "C:\Users\Alejandro\Desktop\HYPERTENSIONES\deploy.py"
echo.
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Deploy completado correctamente.
) else (
    echo  [ERROR] El deploy ha fallado. Revisa el output anterior.
)
echo.
pause
