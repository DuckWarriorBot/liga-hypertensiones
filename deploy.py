#!/usr/bin/env python3
"""
deploy.py — Pipeline completo + copia al hosting IONOS.

Ejecuta:
  1. fetch_all.py         (calendario + resultados de Marca)
  2. fetch_scores.py      (marcadores de football-data.co.uk)
  3. fetch_predictions_history.py
  4. build.py             (genera index.html)
  5. Copia los archivos al hosting IONOS

Uso:
  python deploy.py            → pipeline completo + deploy
  python deploy.py --only-deploy → solo copia (sin re-fetchear)
"""

import sys, os, shutil, subprocess, datetime
from pathlib import Path

# ── Configuración ─────────────────────────────────────────────────────────────
SRC  = Path(__file__).parent
DEST = Path(r'f:\HOSTING\clickandbuilds\Hypertensiones')

# Archivos a copiar al hosting
DEPLOY_FILES = [
    'index.html',
    'version.json',
    'liga_data.json',
    'scores_data.json',
    'predictions.json',
    'predictions_history.json',
]

# Pipeline de scripts a ejecutar (en orden)
PIPELINE = [
    'fetch_all.py',           # calendario + resultados V/E/D (Marca.com)
    'fetch_flashscore.py',    # marcadores y fixtures en tiempo real (Flashscore)
    'fetch_predictions_history.py',
    'build.py',               # genera index.html + version.json
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def ts():
    return datetime.datetime.now().strftime('%H:%M:%S')

def run_script(script):
    path = SRC / script
    if not path.exists():
        print(f'[{ts()}]  ⚠  {script} no encontrado, omitiendo')
        return True
    print(f'[{ts()}]  ▶  {script}...', end=' ', flush=True)
    r = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(SRC),
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if r.returncode != 0:
        print(f'✗')
        print(r.stderr[-600:])
        return False
    print(f'✓')
    return True

def do_deploy():
    if not DEST.exists():
        print(f'[{ts()}]  ✗  Carpeta destino no encontrada: {DEST}')
        print('         Comprueba que la unidad FTP de IONOS está montada.')
        return False

    print(f'[{ts()}]  Copiando al hosting...')
    ok = True
    for fname in DEPLOY_FILES:
        src_f = SRC / fname
        dst_f = DEST / fname
        if not src_f.exists():
            print(f'         ⚠  {fname} no encontrado, omitido')
            continue
        try:
            shutil.copy2(src_f, dst_f)
            size = src_f.stat().st_size
            print(f'         ✓  {fname}  ({size//1024} KB)')
        except Exception as e:
            print(f'         ✗  {fname}: {e}')
            ok = False
    return ok

# ── Main ──────────────────────────────────────────────────────────────────────
only_deploy = '--only-deploy' in sys.argv

print(f'[{ts()}] ══ DEPLOY Liga Hypertensiones ══')

if not only_deploy:
    print(f'[{ts()}] Pipeline de datos...')
    for script in PIPELINE:
        if not run_script(script):
            print(f'[{ts()}] ✗ Pipeline abortado en {script}')
            sys.exit(1)
    print(f'[{ts()}] ✓ Pipeline completado')

print(f'[{ts()}] Desplegando al hosting IONOS...')
if do_deploy():
    print(f'[{ts()}] ✓ Deploy completado → {DEST}')
else:
    print(f'[{ts()}] ✗ Deploy con errores')
    sys.exit(1)
