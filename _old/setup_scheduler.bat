@echo off
rem ═══════════════════════════════════════════════════════════════
rem  setup_scheduler.bat
rem  Crea 3 tareas programadas en el Programador de tareas Windows:
rem
rem  1. LigaHyper-Normal   → cada 6 horas (todos los días)
rem  2. LigaHyper-Partido  → cada 5 min entre 13:30 y 23:59
rem                          (activo solo en días con partido;
rem                           deploy.py sale rápido si no toca)
rem  3. LigaHyper-Boot     → al arrancar el PC (actualización inicial)
rem ═══════════════════════════════════════════════════════════════
title Setup Programador de Tareas - Liga Hypertensiones
echo.
echo  Creando tareas programadas para deploy automatico...
echo.

set PYTHON=python
set SCRIPT=C:\Users\Alejandro\Desktop\HYPERTENSIONES\deploy.py

rem ── Tarea 1: Cada 6 horas todos los días ──────────────────────
schtasks /Create /F /TN "LigaHyper-Normal" ^
  /TR "\"%PYTHON%\" \"%SCRIPT%\"" ^
  /SC DAILY ^
  /ST 07:00 ^
  /RI 360 ^
  /DU 9999:59 ^
  /RU "%USERNAME%"

if %ERRORLEVEL% EQU 0 (
    echo  [OK] LigaHyper-Normal creada ^(cada 6h^)
) else (
    echo  [ERROR] No se pudo crear LigaHyper-Normal
)

rem ── Tarea 2: Cada 5 min entre 13:30 y 23:59 (días de partido) -
schtasks /Create /F /TN "LigaHyper-Partido" ^
  /TR "\"%PYTHON%\" \"%SCRIPT%\"" ^
  /SC DAILY ^
  /ST 13:30 ^
  /RI 5 ^
  /DU 10:29 ^
  /RU "%USERNAME%"

if %ERRORLEVEL% EQU 0 (
    echo  [OK] LigaHyper-Partido creada ^(cada 5min 13:30-23:59^)
) else (
    echo  [ERROR] No se pudo crear LigaHyper-Partido
)

rem ── Tarea 3: Al arrancar el PC ────────────────────────────────
schtasks /Create /F /TN "LigaHyper-Boot" ^
  /TR "\"%PYTHON%\" \"%SCRIPT%\"" ^
  /SC ONSTART ^
  /DELAY 0001:00 ^
  /RU "%USERNAME%"

if %ERRORLEVEL% EQU 0 (
    echo  [OK] LigaHyper-Boot creada ^(al arrancar el PC^)
) else (
    echo  [ERROR] No se pudo crear LigaHyper-Boot
)

echo.
echo  Tareas creadas. Puedes verlas en:
echo    Panel de Control ^> Herramientas administrativas ^> Programador de tareas
echo.
echo  IMPORTANTE: el PC debe estar encendido para que se ejecuten.
echo  La unidad FTP de IONOS debe estar montada en F:\
echo.
pause
