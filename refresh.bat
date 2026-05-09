@echo off
:: Refresh de emergencia: fetch_flashscore + build + deploy SFTP
:: Usar cuando la web se queda desactualizada. Doble clic o llamar desde CMD.
cd /d "%~dp0"
echo [REFRESH] %date% %time%

echo [1/3] fetch_flashscore...
C:\Users\Alejandro\AppData\Local\Programs\Python\Python311\python.exe fetch_flashscore.py
if errorlevel 1 echo WARN: fetch_flashscore fallo, continuando...

echo [2/3] build...
C:\Users\Alejandro\AppData\Local\Programs\Python\Python311\python.exe build.py
if errorlevel 1 ( echo ERROR: build fallo & pause & exit /b 1 )

echo [3/3] deploy SFTP...
C:\Users\Alejandro\AppData\Local\Programs\Python\Python311\python.exe deploy.py --sftp --only-deploy
if errorlevel 1 ( echo ERROR: deploy fallo & pause & exit /b 1 )

echo [OK] Refresh completado: %time%
timeout /t 3
