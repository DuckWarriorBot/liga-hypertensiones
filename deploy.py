#!/usr/bin/env python3
"""
deploy.py — Pipeline completo + copia al hosting IONOS.

Ejecuta:
  1. fetch_all.py         (calendario + resultados de Marca)
  2. fetch_flashscore.py  (marcadores en tiempo real)
  3. fetch_predictions_history.py
  4. build.py             (genera index.html)
  5. Copia los archivos al hosting IONOS:
       - Primero intenta copia directa a unidad WebDAV (F:)
       - Si no está montada, usa SFTP (paramiko)

Uso:
  python deploy.py            → pipeline completo + deploy
  python deploy.py --only-deploy → solo copia (sin re-fetchear)
  python deploy.py --sftp     → forzar SFTP aunque esté la unidad WebDAV
"""

import sys, os, shutil, subprocess, datetime
from pathlib import Path

# ── Configuración ─────────────────────────────────────────────────────────────
SRC  = Path(__file__).parent
DEST = Path(r'f:\HOSTING\clickandbuilds\Hypertensiones')

# Credenciales SFTP (fallback cuando F: no está montada)
SFTP_HOST = 'home559128403.1and1-data.host'
SFTP_PORT = 22
SFTP_USER = 'acc147683744'
# La contraseña se lee desde variable de entorno IONOS_SFTP_PASS
# (nunca hardcodeada). Configúrala con:
#   $env:IONOS_SFTP_PASS = 'tu_contraseña'
SFTP_REMOTE_DIR = '/'   # Ajusta si es necesario (ej: '/hypertensiones.alejandrobeltran.es/')

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

def do_deploy_webdav():
    """Copia directa a unidad WebDAV montada en F:"""
    if not DEST.exists():
        return None  # No disponible
    print(f'[{ts()}]  Copiando via WebDAV → {DEST}')
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

def do_deploy_sftp():
    """Upload via SFTP usando paramiko (fallback cuando F: no está montada)."""
    try:
        import paramiko
    except ImportError:
        print(f'[{ts()}]  ⚠  paramiko no instalado. Ejecuta: pip install paramiko')
        return False

    password = os.environ.get('IONOS_SFTP_PASS', '')
    if not password:
        print(f'[{ts()}]  ✗  Variable IONOS_SFTP_PASS no definida.')
        print('         Ejecuta: $env:IONOS_SFTP_PASS = "tu_contraseña"')
        return False

    print(f'[{ts()}]  Conectando via SFTP → {SFTP_HOST}:{SFTP_PORT}')
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USER, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Determinar directorio remoto
        remote_dir = SFTP_REMOTE_DIR
        try:
            sftp.chdir(remote_dir)
        except IOError:
            print(f'         ⚠  Ruta remota "{remote_dir}" no encontrada, usando directorio actual')
            sftp.chdir('.')

        ok = True
        for fname in DEPLOY_FILES:
            src_f = SRC / fname
            if not src_f.exists():
                print(f'         ⚠  {fname} no encontrado, omitido')
                continue
            try:
                sftp.put(str(src_f), fname)
                size = src_f.stat().st_size
                print(f'         ✓  {fname}  ({size//1024} KB)')
            except Exception as e:
                print(f'         ✗  {fname}: {e}')
                ok = False

        sftp.close()
        transport.close()
        return ok
    except Exception as e:
        print(f'[{ts()}]  ✗  Error SFTP: {e}')
        return False

def do_deploy():
    force_sftp = '--sftp' in sys.argv
    if not force_sftp:
        result = do_deploy_webdav()
        if result is not None:
            return result
        print(f'[{ts()}]  ⚠  Unidad WebDAV no disponible ({DEST}). Usando SFTP...')
    return do_deploy_sftp()

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
    print(f'[{ts()}] ✓ Deploy completado')
else:
    print(f'[{ts()}] ✗ Deploy con errores')
    sys.exit(1)
