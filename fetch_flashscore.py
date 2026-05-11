#!/usr/bin/env python3
"""
fetch_flashscore.py — Actualiza datos desde Flashscore (LaLiga Hypermotion).

Scrapes:
  /resultados/ → scores_data.json   (marcadores gol-gol, todas las jornadas disponibles)
  /partidos/   → liga_data.json     (fixtures: fecha/hora de jornadas futuras + match_days)

Requiere: pip install playwright && python -m playwright install chromium
"""

import json, re, sys, unicodedata, time as _time, ast as _ast
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR     = Path(__file__).parent
LIGA_F       = BASE_DIR / 'liga_data.json'
SCORES_F     = BASE_DIR / 'scores_data.json'

# ── Calendario canónico H/A extraído de generate_data.py (fuente de verdad) ──
# _CANONICAL_HOME[(home, away, idx)] = True  → home ES el local real en esa jornada
_CANONICAL_HOME: dict = {}
try:
    _gd_src = (BASE_DIR / 'generate_data.py').read_text(encoding='utf-8')
    _m = re.search(r'FIXTURES\s*=\s*(\[.+?\])\s*\n[a-zA-Z#]', _gd_src, re.DOTALL)
    if _m:
        _FIXTURES_RAW = _ast.literal_eval(_m.group(1))
        for _jidx, _matches in enumerate(_FIXTURES_RAW):
            for _h, _a in _matches:
                _CANONICAL_HOME[(_h, _a, _jidx)] = True   # home es local
                _CANONICAL_HOME[(_a, _h, _jidx)] = False  # away es visitante (home invertido)
except Exception as _e:
    print(f'[flashscore] AVISO: no se pudo cargar CANONICAL_HOME: {_e}', flush=True)

# Índice 0-based por pareja directional: (home, away) -> jidx
# Fuente de verdad para el round de cada partido, sin depender de Flashscore.
_CANONICAL_IDX: dict = {(_h, _a): _jidx for (_h, _a, _jidx) in _CANONICAL_HOME.keys()}

RESULTS_URL  = 'https://www.flashscore.es/futbol/espana/laliga-hypermotion/resultados/'
FIXTURES_URL = 'https://www.flashscore.es/futbol/espana/laliga-hypermotion/partidos/'
LIVE_URL     = 'https://www.flashscore.es/futbol/espana/laliga-hypermotion/'

# ── Mapeo nombres Flashscore → nombres internos ──────────────────────────────
FS_MAP = {
    'Albacete':                    'Albacete',
    'Almería':                     'Almería',
    'Almeria':                     'Almería',
    'FC Andorra':                  'Andorra',
    'Andorra':                     'Andorra',
    'Burgos CF':                   'Burgos',
    'Burgos':                      'Burgos',
    'Cádiz':                       'Cádiz',
    'Cadiz':                       'Cádiz',
    'Cádiz CF':                    'Cádiz',
    'CD Castellón':                'Castellón',
    'Castellón':                   'Castellón',
    'Castellon':                   'Castellón',
    'AD Ceuta FC':                 'Ceuta',    'AD Ceuta':                    'Ceuta',    'Ceuta':                       'Ceuta',
    'Córdoba CF':                  'Córdoba',
    'Córdoba':                     'Córdoba',
    'Cordoba':                     'Córdoba',
    'Cultural Leonesa':            'Cultural Leonesa',
    'C. Leonesa':                  'Cultural Leonesa',
    'SD Eibar':                    'Eibar',
    'Eibar':                       'Eibar',
    'Granada CF':                  'Granada',
    'Granada':                     'Granada',
    'SD Huesca':                   'Huesca',
    'Huesca':                      'Huesca',
    'RC Deportivo':                'Deportivo',
    'RC Deportivo de La Coruña':   'Deportivo',
    'Deportivo de La Coruña':      'Deportivo',
    'Deportivo':                   'Deportivo',
    'UD Las Palmas':               'Las Palmas',
    'Las Palmas':                  'Las Palmas',
    'CD Leganés':                  'Leganés',
    'Leganés':                     'Leganés',
    'Leganes':                     'Leganés',
    'CD Mirandés':                 'Mirandés',
    'Mirandés':                    'Mirandés',
    'Mirandes':                    'Mirandés',
    'Málaga CF':                   'Málaga',
    'Málaga':                      'Málaga',
    'Malaga':                      'Málaga',
    'Racing de Santander':         'Racing',
    'Racing Santander':            'Racing',    'R. Racing Club':              'Racing',
    'R.Racing Club':               'Racing',    'Racing':                      'Racing',
    'Real Sociedad B':             'Real Sociedad B',
    'Soc. B':                      'Real Sociedad B',
    'Real Zaragoza':               'Real Zaragoza',
    'Zaragoza':                    'Real Zaragoza',
    'Real Sporting':               'Sporting',
    'Sporting de Gijón':           'Sporting',
    'Sp. Gijón':                   'Sporting',
    'Sporting':                    'Sporting',
    'Real Valladolid CF':          'Valladolid',
    'Real Valladolid':             'Valladolid',
    'Valladolid':                  'Valladolid',
}

def _norm(s):
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower().strip()

def map_team(raw):
    # Limpiar nombre: quitar líneas extra y números finales (badges de Flashscore)
    raw = raw.strip()
    raw = re.sub(r'[\n\r]+.*$', '', raw)   # quitar texto tras salto de línea
    raw = re.sub(r'\s+\d+$', '', raw).strip()  # quitar número final (ej. "Real Zaragoza 2")
    if raw in FS_MAP:
        return FS_MAP[raw]
    rn = _norm(raw)
    for k, v in FS_MAP.items():
        if _norm(k) == rn:
            return v
    return None

def find_idx(liga, home_int, away_int, exp_res=None):
    """Encuentra índice 0-based de jornada para home vs away via opponents_by_team."""
    h_opps = liga['opponents_by_team'].get(home_int, [])
    h_res  = liga['results_by_team'].get(home_int, [])
    if exp_res:
        for i, o in enumerate(h_opps):
            if o == away_int and i < len(h_res) and h_res[i] == exp_res:
                return i
    return next((i for i, o in enumerate(h_opps) if o == away_int), None)

def parse_fs_datetime(raw):
    """
    Convierte texto de Flashscore → (date_str, time_str) en hora de Madrid.
    Ej: "03.05. 20:30" → ("03/05", "20:30")
         "20:30"        → ("",      "20:30")
    Flashscore ya muestra las horas en hora local (Madrid/CEST), no en UTC.
    """
    date_str = time_str = ''
    m = re.search(r'(\d{2})\.(\d{2})\.', raw)
    if m:
        date_str = f"{m.group(1)}/{m.group(2)}"
    t = re.search(r'(\d{2}:\d{2})', raw)
    if t:
        time_str = t.group(1)
    return date_str, time_str

# ── Browser helpers ──────────────────────────────────────────────────────────

def make_page(pw):
    """Crea un contexto Playwright con UA humano y anti-bot básico."""
    browser = pw.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage',
              '--disable-blink-features=AutomationControlled'],
    )
    ctx = browser.new_context(
        user_agent=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        locale='es-ES',
        timezone_id='Europe/Madrid',
        viewport={'width': 1280, 'height': 900},
    )
    # Eliminar la firma de webdriver
    ctx.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return browser, ctx.new_page()

def dismiss_cookies(page):
    """Cierra el banner de cookies si aparece (OneTrust / Didomi)."""
    for sel in [
        'button#onetrust-accept-btn-handler',
        '#didomi-notice-agree-button',
        'button.fc-cta-consent',
        'button[aria-label*="Accept"]',
        'button[aria-label*="Aceptar"]',
    ]:
        try:
            page.click(sel, timeout=4000)
            page.wait_for_timeout(500)
            return
        except (PWTimeout, Exception):
            pass

# ── Parsing ──────────────────────────────────────────────────────────────────

def _parse_events(page, is_results):
    """
    Lee todos los eventos (resultados o partidos) de la página actual.
    Devuelve lista de dicts con keys: home, away, score_h, score_a, date, time, round_num.
    """
    events = []
    current_round = None
    not_mapped = set()

    # Los selectores que usa Flashscore (pueden variar con actualizaciones)
    ROUND_SELS = ['.event__round.event__round--round', '.event__round--round']
    MATCH_SEL  = '.event__match'

    # Intentamos el selector de round hasta que devuelva algo
    round_els = []
    for sel in ROUND_SELS:
        round_els = page.query_selector_all(sel)
        if round_els:
            break

    match_els = page.query_selector_all(MATCH_SEL)
    if not match_els:
        print('  ⚠  No se encontraron .event__match en la página', flush=True)
        return []

    # Combinamos rounds + matches en orden de aparición en el DOM
    # Playwright no preserva orden entre query_selector_all de diferentes selectores,
    # así que usamos evaluate para obtener una lista ordenada.
    raw = page.evaluate(r"""
    () => {
      const rows = [];
      const sel = '.event__round--round, .event__match';
      document.querySelectorAll(sel).forEach(el => {
        const cls = el.className || '';
        if (cls.includes('event__round--round')) {
          rows.push({ type: 'round', text: el.innerText.trim() });
        } else if (cls.includes('event__match')) {
          // Team names
          const home = el.querySelector('.event__homeParticipant, .event__participant--home');
          const away = el.querySelector('.event__awayParticipant, .event__participant--away');
          // Fallback: any .event__participant
          const parts = el.querySelectorAll('.event__participant');
          const homeName = home ? home.innerText.trim() : (parts[0] ? parts[0].innerText.trim() : '');
          const awayName = away ? away.innerText.trim() : (parts[1] ? parts[1].innerText.trim() : '');
          // Scores
          const sh = el.querySelector('.event__score--home');
          const sa = el.querySelector('.event__score--away');
          const scoreH = sh ? sh.innerText.trim() : '';
          const scoreA = sa ? sa.innerText.trim() : '';
          // Time
          const tm = el.querySelector('.event__time');
          const timeRaw = tm ? tm.innerText.trim() : '';
          rows.push({
            type: 'match',
            home: homeName, away: awayName,
            scoreH, scoreA, timeRaw,
          });
        }
      });
      return rows;
    }
    """)

    for row in raw:
        if row['type'] == 'round':
            m = re.search(r'(\d+)', row['text'])
            if m:
                current_round = int(m.group(1))
            continue

        home_raw = row['home']
        away_raw = row['away']
        if not home_raw or not away_raw:
            continue

        home_int = map_team(home_raw)
        away_int = map_team(away_raw)
        if not home_int:
            not_mapped.add(home_raw)
            continue
        if not away_int:
            not_mapped.add(away_raw)
            continue

        score_h = score_a = None
        if is_results and row['scoreH'] and row['scoreA']:
            try:
                score_h = int(row['scoreH'])
                score_a = int(row['scoreA'])
            except ValueError:
                pass

        if is_results and score_h is None:
            continue  # partido sin marcador → no fue jugado aún o está en progreso

        date_str, time_str = parse_fs_datetime(row['timeRaw'])

        events.append({
            'home':     home_int,
            'away':     away_int,
            'score_h':  score_h,
            'score_a':  score_a,
            'date':     date_str,
            'time':     time_str,
            'round_num': current_round,
        })

    if not_mapped:
        print(f'  ⚠  Equipos sin mapear: {not_mapped}', flush=True)

    return events

def scrape_live_scores(page):
    """
    Detecta partidos en curso navegando a la URL principal de la competición.
    Un partido está en vivo si su .event__time muestra minutos (ej. "35'") o "HT".
    Devuelve lista de dicts: {home, away, score_h, score_a, minute}.
    """
    print('  [live] Buscando partidos en vivo...', flush=True)
    # Navegar a la página principal de la competición (no /partidos/) donde
    # aparecen los partidos en vivo con su minuto en el marcador.
    try:
        page.goto(LIVE_URL, timeout=35000)
        dismiss_cookies(page)
        # Intentar varios selectores; si no aparece .event__match en 25s, continuar sin live
        try:
            page.wait_for_selector('.event__match', timeout=25000)
        except PWTimeout:
            pass  # puede no haber partidos → continuar, el evaluate devolverá []
        page.wait_for_timeout(1500)  # breve espera para que cargue el estado live
    except PWTimeout:
        print('  ⚠  Timeout en página live, sin partidos en vivo', flush=True)
        return []
    except Exception as _e:
        print(f'  ⚠  Error en página live ({_e}), sin partidos en vivo', flush=True)
        return []

    not_mapped = set()
    raw = page.evaluate(r"""
    () => {
      const results = [];
      document.querySelectorAll('.event__match').forEach(el => {
        // Partidos futuros: usan .event__time. Partidos en vivo: usan .event__stage
        const tm    = el.querySelector('.event__time');
        const stage = el.querySelector('.event__stage');
        const timeRaw = tm ? tm.innerText.trim()
                           : (stage ? stage.innerText.trim() : '');
        const stageRaw = stage ? stage.innerText.trim() : '';
        // En vivo: clase CSS event__match--live, o minutos "35'" / "45+2'" / "HT" / "Descanso"
        const isLiveCls = el.classList.contains('event__match--live');
        const isLiveTime = /\d+'|^HT$|^Descanso$/i.test(timeRaw) || /\d+'|^HT$|^Descanso$/i.test(stageRaw);
        if (!isLiveCls && !isLiveTime) return;
        // Usar el texto de stage si está disponible, si no el time
        const minuteText = stageRaw || timeRaw;

        const home = el.querySelector('.event__homeParticipant, .event__participant--home');
        const away = el.querySelector('.event__awayParticipant, .event__participant--away');
        const parts = el.querySelectorAll('.event__participant');
        const homeName = home ? home.innerText.trim()
                              : (parts[0] ? parts[0].innerText.trim() : '');
        const awayName = away ? away.innerText.trim()
                              : (parts[1] ? parts[1].innerText.trim() : '');

        const sh = el.querySelector('.event__score--home');
        const sa = el.querySelector('.event__score--away');
        const scoreH = sh ? sh.innerText.trim() : '';
        const scoreA = sa ? sa.innerText.trim() : '';
        if (!scoreH || !scoreA) return;

        results.push({ home: homeName, away: awayName,
                       scoreH, scoreA, minute: minuteText });
      });
      return results;
    }
    """)
    live_events = []
    for row in raw:
        home_int = map_team(row['home'])
        away_int = map_team(row['away'])
        if not home_int:
            not_mapped.add(row['home'])
            continue
        if not away_int:
            not_mapped.add(row['away'])
            continue
        try:
            score_h = int(row['scoreH'])
            score_a = int(row['scoreA'])
        except (ValueError, KeyError):
            continue
        live_events.append({
            'home': home_int, 'away': away_int,
            'score_h': score_h, 'score_a': score_a,
            'minute': row['minute'],
        })
    if not_mapped:
        print(f'  ⚠  Live: equipos sin mapear: {not_mapped}', flush=True)
    print(f'  ✓ {len(live_events)} partidos en vivo detectados', flush=True)
    return live_events


def update_live_scores(scores, live_list):
    """
    Actualiza scores['live_scores'] con los partidos en curso.
    - Si live_list tiene partidos: reemplaza con datos frescos.
    - Si live_list está vacío: marca como 'FT' los que estaban en curso
      (último marcador conocido) para que la web lo muestre mientras esperamos
      que el resultado aterrice en /resultados/. El caller (live_loop) los
      borrará cuando scores_by_team tenga el resultado final.
    """
    if live_list:
        # Hay partidos en vivo: reemplazar completamente
        scores['live_scores'] = {}
        for m in live_list:
            home, away = m['home'], m['away']
            hg, ag = m['score_h'], m['score_a']
            minute = m['minute']
            scores['live_scores'][home] = {
                'opponent': away, 'score_h': hg, 'score_a': ag,
                'minute': minute, 'is_home': True,
            }
            scores['live_scores'][away] = {
                'opponent': home, 'score_h': hg, 'score_a': ag,
                'minute': minute, 'is_home': False,
            }
    else:
        # Sin partidos en vivo: marcar los existentes como FT (último resultado conocido)
        # Solo si tenían un minuto real (no ya FT), para no sobrescribir en bucle
        for team, entry in scores.get('live_scores', {}).items():
            if entry.get('minute', '') not in ('FT', ''):
                entry['minute'] = 'FT'
    return len(live_list)


# ── Scrapers ─────────────────────────────────────────────────────────────────

def scrape_results(page):
    """Descarga todos los resultados disponibles en /resultados/."""
    print('  [1/2] Scraping resultados...', flush=True)
    try:
        page.goto(RESULTS_URL, timeout=30000)
        dismiss_cookies(page)
        page.wait_for_selector('.event__match', timeout=25000)
    except PWTimeout:
        print('  ✗ Timeout cargando resultados', flush=True)
        return []

    # Scroll para cargar más jornadas pasadas (lazy-load)
    # Sigue scrolleando hasta que no aparezcan más partidos nuevos
    prev_count = 0
    for _ in range(12):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(800)
        cur_count = page.evaluate("document.querySelectorAll('.event__match').length")
        if cur_count == prev_count:
            break
        prev_count = cur_count

    events = _parse_events(page, is_results=True)
    print(f'  ✓ {len(events)} resultados parseados', flush=True)
    return events

def scrape_fixtures(page):
    """Descarga todos los partidos futuros en /partidos/."""
    print('  [2/2] Scraping partidos futuros...', flush=True)
    try:
        page.goto(FIXTURES_URL, timeout=30000)
        dismiss_cookies(page)
        page.wait_for_selector('.event__match', timeout=25000)
    except PWTimeout:
        print('  ✗ Timeout cargando partidos', flush=True)
        return []

    # Scroll para cargar todas las jornadas restantes
    for _ in range(3):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(800)

    events = _parse_events(page, is_results=False)
    print(f'  ✓ {len(events)} fixtures parseados', flush=True)
    return events

# ── Actualizadores de datos ──────────────────────────────────────────────────

def update_scores(liga, scores, result_list, rdb=None):
    """
    Actualiza scores_data.json con los resultados scrapeados.
    Si se pasa rdb (results_db), los resultados locked no se sobreescriben.
    Retorna número de entradas actualizadas.
    """
    import results_db as _rdb_mod
    updated = 0
    # Pre-indexar fixtures por pareja para poder sincronizar rondas desde resultados
    fix_by_pair = {f'{f["home"]}|{f["away"]}': f for f in liga.get('fixtures', [])}
    for m in result_list:
        home, away = m['home'], m['away']
        hg, ag = m['score_h'], m['score_a']
        exp_res = 'V' if hg > ag else ('E' if hg == ag else 'D')

        # Determinar el índice (0-based) correcto para este resultado.
        # Flashscore /resultados/ NO muestra headers de ronda → round_num siempre None.
        # Estrategia de resolución (por orden de fiabilidad):
        #   1) Si round_num viene del DOM (alguna página futura lo incluya), usarlo directo.
        #   2) Buscar la pareja home|away en fixtures → el campo 'round' (1-based) − 1.
        #   3) Fallback: find_idx usando opponents_by_team (puede apuntar a primera vuelta).
        rn = m.get('round_num')
        idx = None
        if rn is not None:
            idx = rn  # 0-based directo
            fixture_round = rn + 1
            key = f'{home}|{away}'
            if key in fix_by_pair:
                fix_by_pair[key]['round'] = fixture_round
            else:
                new_f = {'round': fixture_round, 'home': home, 'away': away,
                         'date': m.get('date', ''), 'time': m.get('time', '')}
                liga.setdefault('fixtures', []).append(new_f)
                fix_by_pair[key] = new_f
        else:
            # Buscar en fixtures (más fiable: contiene la ronda real del calendario actual)
            key = f'{home}|{away}'
            fix = fix_by_pair.get(key)
            if fix and fix.get('round'):
                idx = fix['round'] - 1  # fixture round es 1-based → 0-based
            if idx is None:
                idx = find_idx(liga, home, away, exp_res)
            if idx is None:
                idx = find_idx(liga, home, away)
        if idx is None:
            continue

        idx_str = str(idx)

        # ── Guardia estricta: nunca sobreescribir J1-J38 con datos de flashscore ─
        # Los datos de J1-J38 provienen EXCLUSIVAMENTE de football-data.co.uk
        # (fetch_scores.py). Flashscore solo gestiona J39+ (jornadas actuales).
        total_rounds_val = liga.get('total_rounds', 38)
        if idx < total_rounds_val:
            continue  # J1-J38: siempre saltar, usar sólo football-data.co.uk

        # ── Validar home/away con calendario canónico ─────────────────────
        # Flashscore a veces invierte home y away para jornadas actuales (J39+).
        # Para J1-J38 ya están protegidas por la guardia histórica de arriba.
        if _CANONICAL_HOME:
            is_home = _CANONICAL_HOME.get((home, away, idx))
            if is_home is False:
                # home de flashscore es en realidad el visitante → invertir
                home, away = away, home
                hg, ag = ag, hg

        # ── BD persistente ────────────────────────────────────────────────
        if rdb is not None:
            locked = _rdb_mod.get_locked(rdb, home, away, idx)
            if locked:
                # Resultado ya confirmado por ambas fuentes: usar el locked
                hg_l, ag_l = map(int, locked[0].split('-'))
                hg, ag = hg_l, ag_l
            else:
                res_h = 'V' if hg > ag else ('E' if hg == ag else 'D')
                _rdb_mod.confirm_source(rdb, 'flashscore', home, away, idx,
                                        f'{hg}-{ag}', f'{ag}-{hg}', res_h)

        idx_str = str(idx)
        # Home team: score gf-ga, venue H
        scores['scores_by_team'].setdefault(home, {})[idx_str] = f'{hg}-{ag}'
        scores['venue_by_team'].setdefault(home, {})[idx_str]  = 'H'
        # Away team: score gf-ga (invertido), venue A
        scores['scores_by_team'].setdefault(away, {})[idx_str] = f'{ag}-{hg}'
        scores['venue_by_team'].setdefault(away, {})[idx_str]  = 'A'
        updated += 1

    return updated

def update_fixtures(liga, fixture_list):
    """
    Actualiza liga_data.json:
      - fixtures[]: solo DATE y TIME de partidos futuros
      - match_days: {DD/MM: [HH:MM, ...]} para el scheduler de server.py

    IMPORTANTE: round, home y away de fixtures EXISTENTES son INMUTABLES aquí.
    Su fuente de verdad es generate_data.py. Flashscore solo aporta fecha/hora.

    Retorna número de partidos actualizados.
    """
    # Índice fixtures existentes por home|away (y también away|home para matchear invertidos)
    fix_by_pair = {}
    for f in liga.get('fixtures', []):
        fix_by_pair[f'{f["home"]}|{f["away"]}'] = f

    # Índice alternativo para encontrar fixture aunque Flashscore invierta home/away
    fix_by_canonical = {}
    for f in liga.get('fixtures', []):
        h, a = f['home'], f['away']
        fix_by_canonical[f'{h}|{a}'] = f
        fix_by_canonical[f'{a}|{h}'] = f  # alias invertido apunta al mismo objeto

    match_days = liga.setdefault('match_days', {})
    updated = 0

    for m in fixture_list:
        home, away = m['home'], m['away']
        date_str, time_str = m['date'], m['time']

        # Buscar fixture existente (por orden directo o invertido de Flashscore)
        key = f'{home}|{away}'
        f = fix_by_canonical.get(key)

        if f is not None:
            # Fixture existente: SOLO actualizar fecha/hora. NUNCA round/home/away.
            if date_str:
                f['date'] = date_str
            if time_str:
                f['time'] = time_str
        else:
            # Fixture nuevo (no estaba en el calendario canónico):
            # Usar _CANONICAL_IDX para asignar round correcto si lo conocemos.
            canonical_idx = _CANONICAL_IDX.get((home, away)) or _CANONICAL_IDX.get((away, home))
            round_num = m.get('round_num')
            if canonical_idx is not None:
                fixture_round = canonical_idx + 1
            elif round_num is not None:
                fixture_round = round_num + 1
            else:
                fixture_round = 0
            new_f = {'round': fixture_round, 'home': home, 'away': away,
                     'date': date_str, 'time': time_str}
            liga.setdefault('fixtures', []).append(new_f)
            fix_by_canonical[key] = new_f

        # Actualizar match_days
        if date_str and time_str:
            md = match_days.setdefault(date_str, [])
            if time_str not in md:
                md.append(time_str)
                md.sort()

        updated += 1

    return updated

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    t0 = _time.time()
    print('[flashscore] Iniciando...', flush=True)

    liga   = json.loads(LIGA_F.read_text(encoding='utf-8'))
    scores = json.loads(SCORES_F.read_text(encoding='utf-8')) if SCORES_F.exists() else {}
    scores.setdefault('scores_by_team', {})
    scores.setdefault('venue_by_team', {})

    # ── Cargar BD de resultados persistentes ─────────────────────────────
    try:
        import results_db as _rdb_mod
        rdb = _rdb_mod.load()
    except Exception as _e:
        print(f'  ⚠ results_db no disponible: {_e}')
        rdb = None
        _rdb_mod = None

    with sync_playwright() as pw:
        browser, page = make_page(pw)
        try:
            result_list  = scrape_results(page)
            fixture_list = scrape_fixtures(page)
            live_list    = scrape_live_scores(page)   # página ya en /partidos/
        finally:
            browser.close()

    # ── Recargar scores tras el scraping (~60s) para no sobreescribir datos
    # frescos escritos por fetch_scores.py durante la ventana de scraping.
    scores = json.loads(SCORES_F.read_text(encoding='utf-8')) if SCORES_F.exists() else {}
    scores.setdefault('scores_by_team', {})
    scores.setdefault('venue_by_team', {})

    n_scores = update_scores(liga, scores, result_list, rdb)
    n_fix    = update_fixtures(liga, fixture_list)
    n_live   = update_live_scores(scores, live_list)

    print(f'  Scores actualizados/añadidos  : {n_scores}', flush=True)
    print(f'  Fixtures actualizados/añadidos: {n_fix}', flush=True)
    print(f'  Partidos en vivo              : {n_live}', flush=True)

    # ── Restaurar resultados locked + guardar BD ──────────────────────────
    if rdb is not None and _rdb_mod is not None:
        try:
            _rdb_mod.apply_locked_to_scores(rdb, scores, liga)
            _rdb_mod.save(rdb)
            locked_count = sum(1 for v in rdb['locked'].values() if v.get('locked'))
            print(f'  Resultados locked en BD       : {locked_count}', flush=True)
        except Exception as _e:
            print(f'  ⚠ results_db save error: {_e}')

    SCORES_F.write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding='utf-8')
    LIGA_F.write_text(json.dumps(liga, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'[flashscore] ✓ Completado en {_time.time()-t0:.1f}s', flush=True)

if __name__ == '__main__':
    main()
