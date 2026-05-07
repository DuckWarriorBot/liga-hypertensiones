#!/usr/bin/env python3
"""
server.py — Servidor web local con actualización automática de datos.

Lógica de actualización:
  - Cada 6 horas en días normales
  - En días de partido: cada 1 minuto desde la 1ª hora de partido
    hasta 2 horas después del último partido
  - Fuera del rango horario de partido pero en día de partido: espera
    hasta la 1ª hora de partido (sin malgastar peticiones)

Uso:
  python server.py          → http://localhost:8080
  python server.py 9000     → http://localhost:9000

Pipeline de actualización:
  fetch_all.py  →  fetch_predictions_history.py  →  build.py
"""

import os, sys, json, threading, time, subprocess, datetime, socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR         = Path(__file__).parent
PORT             = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
NORMAL_INTERVAL  = 6 * 3600   # segundos entre actualizaciones en días normales
LIVE_INTERVAL    = 60          # segundos durante partidos en curso
MATCH_END_BUFFER = 2 * 3600   # 2h de buffer tras el último kick-off para seguir en vivo

# Estado compartido (protegido por lock)
_state_lock   = threading.Lock()
_last_updated = None   # ISO string
_is_live      = False
_next_update  = None   # ISO string


# ── Lectura de datos ──────────────────────────────────────────────────────────

def _load_match_days():
    """Lee {DD/MM: [HH:MM, ...]} de liga_data.json."""
    try:
        data = json.loads((BASE_DIR / 'liga_data.json').read_text(encoding='utf-8'))
        return data.get('match_days', {})
    except Exception:
        return {}


def _get_today_kicks():
    """Devuelve lista de datetime.time con horarios de partido de hoy."""
    today = datetime.datetime.now().strftime('%d/%m')
    md = _load_match_days()
    kicks = []
    for t_str in md.get(today, []):
        try:
            h, m = map(int, t_str.split(':'))
            kicks.append(datetime.time(h, m))
        except ValueError:
            pass
    return sorted(kicks)


def _in_live_window():
    """True si ahora mismo hay partido en curso (dentro de kick-off + 2h)."""
    now   = datetime.datetime.now()
    kicks = _get_today_kicks()
    if not kicks:
        today = now.strftime('%d/%m')
        # Hay partidos hoy pero sin hora conocida → asumir en vivo todo el día
        return today in _load_match_days()
    for kick in kicks:
        ko = now.replace(hour=kick.hour, minute=kick.minute, second=0, microsecond=0)
        if ko <= now <= ko + datetime.timedelta(seconds=MATCH_END_BUFFER):
            return True
    return False


def _seconds_until_next_kickoff():
    """Segundos hasta el próximo kick-off de hoy (o None si no hay más hoy)."""
    now   = datetime.datetime.now()
    kicks = _get_today_kicks()
    for kick in kicks:
        ko = now.replace(hour=kick.hour, minute=kick.minute, second=0, microsecond=0)
        if ko > now:
            return max(0, (ko - now).total_seconds())
    return None


# ── Pipeline de actualización ─────────────────────────────────────────────────

def run_refresh():
    """Ejecuta el pipeline completo: fetch_all → predictions → build."""
    global _last_updated
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] Actualizando datos...', flush=True)

    # Pipeline: estructura (Marca) → scores+fixtures en vivo (Flashscore) → predicciones → HTML
    scripts = [
        'fetch_all.py',           # calendario, resultados V/E/D, estructura
        'fetch_flashscore.py',    # marcadores y fixtures desde Flashscore (más rápido)
        'fetch_predictions_history.py',
        'build.py',
    ]
    for script in scripts:
        path = BASE_DIR / script
        if not path.exists():
            print(f'  ⚠  {script} no encontrado, omitiendo', flush=True)
            continue
        r = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(BASE_DIR),
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        if r.returncode != 0:
            print(f'  ✗  {script} error:\n{r.stderr[-400:]}', flush=True)
        else:
            print(f'  ✓  {script}', flush=True)

    with _state_lock:
        _last_updated = datetime.datetime.now().isoformat(timespec='seconds')
    print(f'[{datetime.datetime.now():%H:%M:%S}] ✓ Listo', flush=True)


# ── Scheduler ─────────────────────────────────────────────────────────────────

def scheduler_loop():
    global _is_live, _next_update

    # Primera actualización inmediata al arrancar
    run_refresh()

    while True:
        now       = datetime.datetime.now()
        today_str = now.strftime('%d/%m')
        md        = _load_match_days()

        if today_str in md:
            if _in_live_window():
                sleep = LIVE_INTERVAL
                live  = True
            else:
                secs_to_next = _seconds_until_next_kickoff()
                if secs_to_next is not None:
                    # Dormir hasta justo antes del primer partido
                    sleep = max(60, secs_to_next - 30)
                else:
                    # Todos los partidos de hoy terminaron → 6h
                    sleep = NORMAL_INTERVAL
                live = False
        else:
            sleep = NORMAL_INTERVAL
            live  = False

        with _state_lock:
            _is_live = live
            _next_update = (now + datetime.timedelta(seconds=sleep)).isoformat(timespec='seconds')

        label = f'{sleep}s' if sleep < 120 else f'{sleep//60}m'
        print(f'[{now:%H:%M:%S}] Próxima actualización en {label} '
              f'{"🔴 EN VIVO" if live else ""}', flush=True)

        time.sleep(sleep)
        run_refresh()


# ── Servidor HTTP ─────────────────────────────────────────────────────────────

class Handler(SimpleHTTPRequestHandler):
    """Sirve los archivos del proyecto + endpoint /api/status."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        if self.path == '/api/status':
            with _state_lock:
                body = json.dumps({
                    'last_updated': _last_updated,
                    'is_live':      _is_live,
                    'next_update':  _next_update,
                }).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
        else:
            # Cachear JSON con no-cache para que el browser siempre tome el fresco
            if self.path in ('/liga_data.json', '/scores_data.json',
                             '/predictions_history.json'):
                self.send_response(200)
                ctype = 'application/json; charset=utf-8'
                fpath = BASE_DIR / self.path.lstrip('/')
                try:
                    data = fpath.read_bytes()
                    self.send_header('Content-Type', ctype)
                    self.send_header('Content-Length', str(len(data)))
                    self.send_header('Cache-Control', 'no-store')
                    self.end_headers()
                    self.wfile.write(data)
                except FileNotFoundError:
                    self.send_error(404)
            else:
                super().do_GET()

    def log_message(self, fmt, *args):
        # Silenciar logs de peticiones estáticas frecuentes
        if any(x in (args[0] if args else '') for x in
               ('liga_data.json', 'scores_data.json', 'predictions_history.json',
                'api/status')):
            return
        super().log_message(fmt, *args)


# ── Entrypoint ────────────────────────────────────────────────────────────────

def _find_free_port(preferred):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', preferred))
            return preferred
    except OSError:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]


if __name__ == '__main__':
    os.chdir(BASE_DIR)

    port = _find_free_port(PORT)
    if port != PORT:
        print(f'  ⚠  Puerto {PORT} ocupado, usando {port}')

    # Scheduler en hilo daemon
    t = threading.Thread(target=scheduler_loop, daemon=True, name='scheduler')
    t.start()

    server = HTTPServer(('', port), Handler)
    url    = f'http://localhost:{port}'
    print('=' * 50)
    print(f'  HYPERTENSIONES — Servidor local')
    print(f'  {url}')
    print(f'  Normal:  cada {NORMAL_INTERVAL//3600}h')
    print(f'  En vivo: cada {LIVE_INTERVAL}s (días de partido)')
    print('=' * 50)
    print('Ctrl+C para parar\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
