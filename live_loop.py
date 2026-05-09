#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
live_loop.py -- Bucle automatico de actualizacion en vivo.

Mientras hay partidos en curso (live_scores no vacio):
  fetch_flashscore + build + deploy cada INTERVAL segundos.
Cuando todos terminan: un ciclo de cierre para registrar el resultado.
En reposo: comprueba cada 5 min si hay partido proximo.

Si hay varios partidos en directo a la vez, el bucle continua
hasta que el ULTIMO de todos termine.

Uso:
    python live_loop.py              -> monitoriza indefinidamente
    python live_loop.py --now        -> fuerza un ciclo inmediato ya
    python live_loop.py --interval 90 -> ciclo cada 90s (defecto: 60s)
"""

import sys, os, json, time, subprocess, datetime
from pathlib import Path

# -- Configuracion
BASE_DIR        = Path(__file__).parent

# Python para scripts de build (no necesitan playwright, el venv es suficiente)
_VENV_PY = BASE_DIR / '.venv' / 'Scripts' / 'python.exe'
PYTHON   = str(_VENV_PY) if _VENV_PY.exists() else sys.executable

# Python para scripts que necesitan playwright (fetch_flashscore, fetch_all, etc.)
# El venv puede no tener playwright instalado; detectar qué Python lo tiene.
def _find_playwright_python():
    """Devuelve el ejecutable Python que tiene playwright disponible."""
    candidates = [
        PYTHON,             # venv primero
        sys.executable,     # Python que corre live_loop
    ]
    # Añadir Python311 y Python313 del sistema si existen
    import shutil
    for name in ('python', 'python3', 'python3.11', 'python3.13'):
        p = shutil.which(name)
        if p and p not in candidates:
            candidates.append(p)
    for py in candidates:
        try:
            r = subprocess.run(
                [py, '-c', 'import playwright'],
                capture_output=True, timeout=10
            )
            if r.returncode == 0:
                return py
        except Exception:
            pass
    return PYTHON  # fallback al venv aunque falle

PYTHON_PLAYWRIGHT = _find_playwright_python()

SCORES_FILE     = BASE_DIR / 'scores_data.json'
LIGA_FILE       = BASE_DIR / 'liga_data.json'
INTERVAL        = 60    # segundos entre ciclos LIVE
STANDBY_MINUTES = 10    # minutos antes del partido para pasar a STANDBY
IDLE_SLEEP      = 300   # segundos en IDLE (5 min)
STANDBY_SLEEP   = 60    # segundos en STANDBY
CLOSING_EXTRA   = 1     # ciclos extra tras partido terminado (para capturar resultado)


def ts():
    return datetime.datetime.now().strftime('%H:%M:%S')


def log(msg):
    print(f'[{ts()}] {msg}', flush=True)


def env_utf8():
    """Env con PYTHONIOENCODING=utf-8 para evitar errores de codificacion en Windows."""
    e = os.environ.copy()
    e['PYTHONIOENCODING'] = 'utf-8'
    return e


def load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as ex:
        log(f'Aviso: error leyendo {path.name}: {ex}')
        return {}


def run_step(script_name):
    path = BASE_DIR / script_name
    if not path.exists():
        log(f'Aviso: {script_name} no encontrado')
        return False
    # Scripts que necesitan playwright usan PYTHON_PLAYWRIGHT
    _PLAYWRIGHT_SCRIPTS = {'fetch_flashscore.py', 'fetch_all.py', 'fetch_as.py',
                           'fetch_besoccer.py', 'fetch_scores.py', 'fetch_history.py',
                           'fetch_predictions.py', 'fetch_team_assets.py'}
    py = PYTHON_PLAYWRIGHT if script_name in _PLAYWRIGHT_SCRIPTS else PYTHON
    log(f'  > {script_name}...')
    t0 = time.time()
    r = subprocess.run(
        [py, str(path)],
        cwd=str(BASE_DIR),
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        env=env_utf8()
    )
    elapsed = time.time() - t0
    if r.returncode != 0:
        log(f'  FAIL {script_name} ({elapsed:.0f}s)')
        for line in r.stderr.strip().splitlines()[-5:]:
            print(f'       {line}', flush=True)
        return False
    log(f'  OK   {script_name} ({elapsed:.0f}s)')
    return True


def run_full_cycle():
    """fetch_flashscore + build + deploy --sftp --only-deploy"""
    log('--- fetch + build + deploy ---')
    if not run_step('fetch_flashscore.py'):
        return False
    if not run_step('build.py'):
        return False
    # Verificar que el build es correcto antes de desplegar
    index_path = BASE_DIR / 'index.html'
    REQUIRED_STRINGS = [
        'fx0raw',              # fixture lookup directo (tarjetas !r branch)
        '_fxRes',              # fixture lookup en resultado cards (fix oppsMap)
        'isCurrent = !isFut',  # highlight jornada actual en historyTable
    ]
    try:
        built = index_path.read_text(encoding='utf-8', errors='replace')
        missing = [s for s in REQUIRED_STRINGS if s not in built]
        if missing:
            log(f'  WARN build incompleto (faltan: {missing}) -- rehaciendo con venv...')
            r2 = subprocess.run(
                [PYTHON, str(BASE_DIR / 'build.py')],
                cwd=str(BASE_DIR),
                capture_output=True, text=True, encoding='utf-8', errors='replace',
                env=env_utf8()
            )
            built2 = index_path.read_text(encoding='utf-8', errors='replace')
            still_missing = [s for s in REQUIRED_STRINGS if s not in built2]
            if r2.returncode != 0 or still_missing:
                log(f'  FAIL build de respaldo falló (aún faltan: {still_missing}) — abortando deploy')
                return False
            log('  OK   build de respaldo generado correctamente')
    except Exception as e:
        log(f'  WARN no se pudo verificar index.html: {e}')
    deploy_path = BASE_DIR / 'deploy.py'
    log('  > deploy.py --sftp --only-deploy...')
    t0 = time.time()
    # Intentar primero WebDAV (F:) que es instantaneo y no requiere password
    r = subprocess.run(
        [PYTHON, str(deploy_path), '--only-deploy'],
        cwd=str(BASE_DIR),
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        env=env_utf8()
    )
    elapsed = time.time() - t0
    if r.returncode == 0:
        log(f'  OK   deploy ({elapsed:.0f}s)')
        return True
    # Fallback a SFTP si WebDAV no disponible
    log(f'  WARN WebDAV falló ({elapsed:.0f}s), intentando SFTP...')
    r2 = subprocess.run(
        [PYTHON, str(deploy_path), '--sftp', '--only-deploy'],
        cwd=str(BASE_DIR),
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        env=env_utf8()
    )
    elapsed2 = time.time() - t0
    if r2.returncode == 0:
        log(f'  OK   deploy SFTP ({elapsed2:.0f}s)')
        return True
    log(f'  FAIL deploy ({elapsed2:.0f}s)')
    for line in r2.stderr.strip().splitlines()[-5:]:
        print(f'       {line}', flush=True)
    return False


def get_live_scores():
    return load_json(SCORES_FILE).get('live_scores', {})


def get_next_fixture_dt():
    data = load_json(LIGA_FILE)
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    best, best_dt = None, None
    for f in data.get('fixtures', []):
        d, t = f.get('date', ''), f.get('time', '')
        if not d or not t:
            continue
        dp, tp = d.split('/'), t.split(':')
        if len(dp) < 2 or len(tp) < 2:
            continue
        dd, mm = int(dp[0]), int(dp[1])
        hh, mi = int(tp[0]), int(tp[1])
        yr = 2025 if mm >= 8 else 2026
        # Los tiempos en liga_data.json son hora local Madrid (CEST=+2 abr-oct, CET=+1 nov-mar)
        # Convertir a UTC para comparar con now_utc
        offset = 2 if 4 <= mm <= 10 else 1
        dt_madrid = datetime.datetime(yr, mm, dd, hh, mi)
        dt_utc = (datetime.datetime(yr, mm, dd, hh, mi, tzinfo=datetime.timezone.utc)
                  - datetime.timedelta(hours=offset))
        if dt_utc > now_utc and (best_dt is None or dt_utc < best_dt):
            best, best_dt = f, dt_utc
    return best, best_dt


def minutes_until(dt_utc):
    return (dt_utc - datetime.datetime.now(datetime.timezone.utc)).total_seconds() / 60


def main():
    force_now = '--now' in sys.argv
    interval = INTERVAL
    for i, arg in enumerate(sys.argv):
        if arg == '--interval' and i + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[i + 1])
            except ValueError:
                pass

    log('=' * 55)
    log('  live_loop.py -- Bucle de actualizacion en vivo')
    log(f'  Intervalo LIVE: {interval}s | Standby: {STANDBY_MINUTES}min antes')
    log('  Ctrl+C para detener')
    log('=' * 55)

    # was_live=True si hubo live datos (o se fuerza --now) para que el modo
    # CLOSING se dispare aunque el partido termine justo antes de arrancar
    was_live = False
    closing_cycles = 0

    if force_now:
        log('--now: ciclo inmediato forzado')
        was_live = True
        run_full_cycle()

    while True:
        live = get_live_scores()

        if live:
            # LIVE: hay uno o varios partidos en curso
            # El bucle continua hasta que live_scores quede completamente vacio
            home_teams = [k for k, v in live.items() if v.get('is_home')] or list(live.keys())
            n = len(home_teams)
            partidos = '  |  '.join(
                '{} {}-{} {} ({})'.format(
                    k,
                    live[k].get('score_h', 0),
                    live[k].get('score_a', 0),
                    live[k].get('opponent', '?'),
                    live[k].get('minute', '?')
                )
                for k in home_teams
            )
            plural = 's' if n > 1 else ''
            log(f'[LIVE] {n} partido{plural}: {partidos}')
            was_live = True
            closing_cycles = 0
            run_full_cycle()
            log(f'Proximo ciclo en {interval}s...')
            time.sleep(interval)

        elif was_live and closing_cycles < CLOSING_EXTRA:
            # CLOSING: live_scores quedo vacio => todos los partidos terminaron
            closing_cycles += 1
            log(f'[FIN] Todos terminados. Ciclo de cierre {closing_cycles}/{CLOSING_EXTRA}...')
            run_full_cycle()
            if closing_cycles >= CLOSING_EXTRA:
                log('[OK] Resultado registrado. Volviendo a IDLE.')
                was_live = False
                closing_cycles = 0

        else:
            # IDLE / STANDBY
            fixture, fix_dt = get_next_fixture_dt()
            if fixture and fix_dt:
                mins = minutes_until(fix_dt)
                home = fixture.get('home', '?')
                away = fixture.get('away', '?')
                date = fixture.get('date', '')
                time_s = fixture.get('time', '')
                if mins <= STANDBY_MINUTES:
                    log(f'[STANDBY] {home} vs {away} empieza en {mins:.0f}min -- check en {STANDBY_SLEEP}s')
                    time.sleep(STANDBY_SLEEP)
                else:
                    log(f'[IDLE] proximo: {home} vs {away} el {date} {time_s} (en {mins:.0f}min) -- check en {IDLE_SLEEP}s')
                    time.sleep(IDLE_SLEEP)
            else:
                log('[IDLE] sin proximos partidos -- check en {IDLE_SLEEP}s'.format(IDLE_SLEEP=IDLE_SLEEP))
                time.sleep(IDLE_SLEEP)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n[{ts()}] Detenido.', flush=True)
