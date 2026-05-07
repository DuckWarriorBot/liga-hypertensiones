@echo off
title Liga Hypertensiones - Deploy
echo.
echo  === Deploy Liga Hypertensiones ===
echo.

REM Si la variable IONOS_SFTP_PASS no está definida, pedirla
if "%IONOS_SFTP_PASS%"=="" (
    set /p IONOS_SFTP_PASS="  Contrasena SFTP IONOS (Enter si WebDAV esta montada): "
)

python "C:\Users\Alejandro\Desktop\HYPERTENSIONES\deploy.py"
echo.
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Deploy completado correctamente.
) else (
    echo  [ERROR] El deploy ha fallado. Revisa el output anterior.
)
echo.
pause
