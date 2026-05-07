#!/usr/bin/env python3
"""
fetch_history.py — Descarga resultados de temporadas anteriores desde Flashscore
y genera history_data.json con la clasificación final calculada automáticamente.

Temporadas scrapeadas (de más reciente a más antigua):
  2024/25, 2023/24, 2022/23, 2021/22, 2020/21, 2019/20

Uso:
  python fetch_history.py
"""

import json, re, sys, unicodedata, time as _time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR   = Path(__file__).parent
HISTORY_F  = BASE_DIR / 'history_data.json'

# Temporadas a importar (slug Flashscore, label de visualización)
SEASONS = [
    ('2024-2025', '2024/25'),
    ('2023-2024', '2023/24'),
    ('2022-2023', '2022/23'),
    ('2021-2022', '2021/22'),
    ('2020-2021', '2020/21'),
    ('2019-2020', '2019/20'),
]

# ── Mapeo de nombres Flashscore → nombres internos ──────────────────────────
FS_MAP = {
    'Albacete': 'Albacete',
    'Almería': 'Almería', 'Almeria': 'Almería',
    'FC Andorra': 'Andorra', 'Andorra': 'Andorra',
    'Burgos CF': 'Burgos', 'Burgos': 'Burgos',
    'Cádiz': 'Cádiz', 'Cadiz': 'Cádiz', 'Cádiz CF': 'Cádiz',
    'CD Castellón': 'Castellón', 'Castellón': 'Castellón', 'Castellon': 'Castellón',
    'AD Ceuta FC': 'Ceuta', 'AD Ceuta': 'Ceuta', 'Ceuta': 'Ceuta',
    'Córdoba CF': 'Córdoba', 'Córdoba': 'Córdoba', 'Cordoba': 'Córdoba',
    'Cultural Leonesa': 'Cultural Leonesa', 'C. Leonesa': 'Cultural Leonesa',
    'SD Eibar': 'Eibar', 'Eibar': 'Eibar',
    'Espanyol': 'Espanyol', 'RCD Espanyol': 'Espanyol',
    'Granada CF': 'Granada', 'Granada': 'Granada',
    'SD Huesca': 'Huesca', 'Huesca': 'Huesca',
    'RC Deportivo': 'Deportivo', 'RC Deportivo de La Coruña': 'Deportivo',
    'Deportivo de La Coruña': 'Deportivo', 'Deportivo': 'Deportivo',
    'UD Las Palmas': 'Las Palmas', 'Las Palmas': 'Las Palmas',
    'CD Leganés': 'Leganés', 'Leganés': 'Leganés', 'Leganes': 'Leganés',
    'Levante UD': 'Levante', 'Levante': 'Levante',
    'CD Mirandés': 'Mirandés', 'Mirandés': 'Mirandés', 'Mirandes': 'Mirandés',
    'Málaga CF': 'Málaga', 'Málaga': 'Málaga', 'Malaga': 'Málaga',
    'Ponferradina': 'Ponferradina', 'SD Ponferradina': 'Ponferradina',
    'Racing de Santander': 'Racing', 'Racing Santander': 'Racing',
    'R. Racing Club': 'Racing', 'R.Racing Club': 'Racing', 'Racing': 'Racing',
    'Real Oviedo': 'Real Oviedo',
    'Real Sociedad B': 'Real Sociedad B', 'Soc. B': 'Real Sociedad B',
    'Real Zaragoza': 'Real Zaragoza', 'Zaragoza': 'Real Zaragoza',
    'Real Sporting': 'Sporting', 'Sporting de Gijón': 'Sporting',
    'Sp. Gijón': 'Sporting', 'Sporting': 'Sporting',
    'Real Valladolid CF': 'Valladolid', 'Real Valladolid': 'Valladolid', 'Valladolid': 'Valladolid',
    'Tenerife': 'Tenerife', 'CD Tenerife': 'Tenerife',
    'Villarreal B': 'Villarreal B',
    'Elche CF': 'Elche', 'Elche': 'Elche',
    'Alcorcón': 'Alcorcón', 'AD Alcorcón': 'Alcorcón', 'Alcorcon': 'Alcorcón',
    'Fuenlabrada': 'Fuenlabrada', 'CF Fuenlabrada': 'Fuenlabrada',
    'Girona': 'Girona', 'Girona FC': 'Girona',
    'Ibiza': 'Ibiza', 'UD Ibiza': 'Ibiza',
    'Lugo': 'Lugo', 'CD Lugo': 'Lugo',
    'Real Oviedo': 'Real Oviedo',
    'Amorebieta': 'Amorebieta', 'SD Amorebieta': 'Amorebieta',
    'Cartagena': 'Cartagena', 'FC Cartagena': 'Cartagena',
    'Rayo Vallecano': 'Rayo Vallecano',
    'UD Almería': 'Almería',
    'Deportivo Alavés': 'Alavés', 'Alavés': 'Alavés',
    'Real Betis B': 'Real Betis B', 'Betis B': 'Real Betis B',
    'Villarreal CF B': 'Villarreal B',
    'Celta B': 'Celta B', 'RC Celta B': 'Celta B',
    'FC Cartagena': 'Cartagena',
    'Hyères FC': 'Hyères',
    'Mirandés': 'Mirandés',
    'Mérida AD': 'Mérida', 'Mérida': 'Mérida',
    'Málaga': 'Málaga',
    'Tenerife': 'Tenerife',
    'Sporting de Gijón': 'Sporting',
}

# ── Helpers ─────────────────────────────────────────────────────────────────

def _norm(s):
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower().strip()

def map_team(raw):
    raw = raw.strip()
    raw = re.sub(r'[\n\r]+.*$', '', raw)
    raw = re.sub(r'\s+\d+$', '', raw).strip()
    if raw in FS_MAP:
        return FS_MAP[raw]
    rn = _norm(raw)
    for k, v in FS_MAP.items():
        if _norm(k) == rn:
            return v
    return raw  # Si no lo conocemos, devolvemos el nombre tal cual (no descartamos)

# ── JS para extraer partidos de la página de resultados ──────────────────────

JS_EXTRACT = r"""
() => {
  const rows = [];
  const sel = '.event__round--round, .event__round--static, .event__match';
  document.querySelectorAll(sel).forEach(el => {
    const cls = el.className || '';
    if (cls.includes('event__round')) {
      rows.push({ type: 'round', text: el.innerText.trim() });
    } else if (cls.includes('event__match')) {
      const home = el.querySelector('.event__homeParticipant, .event__participant--home');
      const away = el.querySelector('.event__awayParticipant, .event__participant--away');
      const parts = el.querySelectorAll('.event__participant');
      const homeName = home ? home.innerText.trim() : (parts[0] ? parts[0].innerText.trim() : '');
      const awayName = away ? away.innerText.trim() : (parts[1] ? parts[1].innerText.trim() : '');
      const sh = el.querySelector('.event__score--home');
      const sa = el.querySelector('.event__score--away');
      const scoreH = sh ? sh.innerText.trim() : '';
      const scoreA = sa ? sa.innerText.trim() : '';
      rows.push({ type: 'match', home: homeName, away: awayName, scoreH, scoreA });
    }
  });
  return rows;
}
"""

# ── Clasificación desde resultados ──────────────────────────────────────────

def compute_standings(matches):
    """
    Calcula clasificación final desde lista de partidos.
    matches: [{home, away, score_h, score_a}]
    Devuelve lista ordenada [{name, pts, played, wins, draws, losses, gf, gc, gd}]
    """
    teams = {}
    for m in matches:
        for name in (m['home'], m['away']):
            if name not in teams:
                teams[name] = {'name': name, 'pts': 0, 'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'gf': 0, 'gc': 0}
        h, a = teams[m['home']], teams[m['away']]
        hg, ag = m['score_h'], m['score_a']

        h['played'] += 1; a['played'] += 1
        h['gf'] += hg; h['gc'] += ag
        a['gf'] += ag; a['gc'] += hg

        if hg > ag:
            h['wins'] += 1; h['pts'] += 3
            a['losses'] += 1
        elif hg < ag:
            a['wins'] += 1; a['pts'] += 3
            h['losses'] += 1
        else:
            h['draws'] += 1; h['pts'] += 1
            a['draws'] += 1; a['pts'] += 1

    for t in teams.values():
        t['gd'] = t['gf'] - t['gc']

    return sorted(teams.values(), key=lambda t: (-t['pts'], -t['gd'], -t['gf'], t['name']))

# ── Scrapers ─────────────────────────────────────────────────────────────────

def scrape_season(page, year_slug, label):
    """Descarga resultados de una temporada histórica y devuelve el dict de datos."""
    url = f'https://www.flashscore.es/futbol/espana/laliga-hypermotion-{year_slug}/resultados/'
    print(f'  → {url}', flush=True)
    page.goto(url, wait_until='domcontentloaded', timeout=40000)
    page.wait_for_timeout(4000)

    # Expandir todos los resultados (Flashscore pagina ~30 partidos por bloque)
    # Una temporada completa tiene ~462 partidos → necesitamos ~15-20 clics
    for attempt in range(60):
        btn = page.query_selector(
            'button[class*="wcl-footer__button"], '
            'a.event__more--block, button.event__more, a.showMore'
        )
        if not btn:
            break
        try:
            btn.scroll_into_view_if_needed()
            btn.click()
            page.wait_for_timeout(1200)
        except Exception:
            break
    print(f'  Carga completada', flush=True)

    raw = page.evaluate(JS_EXTRACT)

    matches = []
    current_round = None
    in_playoff = False
    not_mapped = set()

    PLAYOFF_LABELS = {'final', 'semifinales', 'semifinal', 'semifinals'}

    for row in raw:
        if row['type'] == 'round':
            txt = row['text'].strip().lower()
            if txt in PLAYOFF_LABELS:
                in_playoff = True
            elif re.match(r'jornada\s+\d+|round\s+\d+', txt):
                in_playoff = False
                m = re.search(r'(\d+)', txt)
                if m:
                    current_round = int(m.group(1))
            continue
        if in_playoff:
            continue  # ignorar partidos de playoff en clasificación de liga

        home_raw, away_raw = row['home'], row['away']
        if not home_raw or not away_raw:
            continue

        home_int = map_team(home_raw)
        away_int = map_team(away_raw)

        try:
            score_h = int(row['scoreH'])
            score_a = int(row['scoreA'])
        except (ValueError, TypeError):
            continue  # Sin marcador = no jugado

        matches.append({
            'home':    home_int,
            'away':    away_int,
            'score_h': score_h,
            'score_a': score_a,
            'round':   current_round,
        })

    if not matches:
        print(f'  ⚠  {label}: sin partidos extraídos', flush=True)
        return None

    total_rounds = max((m['round'] for m in matches if m['round']), default=42)

    # ── Construir estructuras por equipo ───────────────────────────────────
    opponents_by_team  = {}  # name → list[42] (oponente por jornada 0-based)
    results_by_team    = {}  # name → list[42] (V/E/D)
    scores_by_team     = {}  # name → {str(round_idx): "gf-gc"}
    venue_by_team      = {}  # name → {str(round_idx): H/A}

    # Inicializar
    all_teams = set()
    for m in matches:
        all_teams.add(m['home'])
        all_teams.add(m['away'])
    for name in all_teams:
        opponents_by_team[name] = ['' ] * total_rounds
        results_by_team[name]   = [None] * total_rounds

    for m in matches:
        rnd = m['round']
        if not rnd or rnd < 1 or rnd > total_rounds:
            continue
        idx = rnd - 1  # 0-based

        h, a   = m['home'], m['away']
        hg, ag = m['score_h'], m['score_a']

        # Oponente
        opponents_by_team[h][idx] = a
        opponents_by_team[a][idx] = h

        # Resultado desde perspectiva de cada equipo
        if hg > ag:
            results_by_team[h][idx] = 'V'
            results_by_team[a][idx] = 'D'
        elif hg < ag:
            results_by_team[h][idx] = 'D'
            results_by_team[a][idx] = 'V'
        else:
            results_by_team[h][idx] = 'E'
            results_by_team[a][idx] = 'E'

        # Marcador desde perspectiva de cada equipo
        key = str(idx)
        if h not in scores_by_team:
            scores_by_team[h] = {}
            venue_by_team[h]  = {}
        if a not in scores_by_team:
            scores_by_team[a] = {}
            venue_by_team[a]  = {}

        scores_by_team[h][key] = f'{hg}-{ag}'
        scores_by_team[a][key] = f'{ag}-{hg}'
        venue_by_team[h][key]  = 'H'
        venue_by_team[a][key]  = 'A'

    # ── Clasificación final ───────────────────────────────────────────────
    standings = compute_standings(matches)

    print(f'  ✓ {label}: {len(matches)} partidos · {len(all_teams)} equipos · J{total_rounds}', flush=True)
    if standings:
        print(f'    1º {standings[0]["name"]} {standings[0]["pts"]}pts · '
              f'Último {standings[-1]["name"]} {standings[-1]["pts"]}pts', flush=True)

    return {
        'label':              label,
        'total_rounds':       total_rounds,
        'total_season_rounds': total_rounds,
        'teams':              sorted(all_teams),
        'final_standings':    standings,
        'opponents_by_team':  opponents_by_team,
        'results_by_team':    results_by_team,
        'scores_by_team':     scores_by_team,
        'venue_by_team':      venue_by_team,
    }

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Cargar histórico existente si hay
    if HISTORY_F.exists():
        with open(HISTORY_F, encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = {'seasons': {}}

    with sync_playwright() as pw:
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
            viewport={'width': 1280, 'height': 900},
        )
        ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        page = ctx.new_page()

        # Cerrar cookies en el primer acceso
        page.goto('https://www.flashscore.es/', wait_until='domcontentloaded', timeout=40000)
        page.wait_for_timeout(2000)
        for sel in ['button#onetrust-accept-btn-handler', '#didomi-notice-agree-button',
                    'button.fc-cta-consent', 'button[aria-label*="Aceptar"]']:
            try:
                page.click(sel, timeout=2000)
                page.wait_for_timeout(500)
                break
            except Exception:
                pass

        for year_slug, label in SEASONS:
            print(f'\n[{label}]', flush=True)
            try:
                data = scrape_season(page, year_slug, label)
                if data:
                    history['seasons'][label] = data
            except Exception as e:
                print(f'  ⚠  Error en {label}: {e}', flush=True)
            _time.sleep(1)

        browser.close()

    with open(HISTORY_F, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, separators=(',', ':'))

    print(f'\n✅  history_data.json guardado ({HISTORY_F.stat().st_size // 1024} KB)')
    print(f'   Temporadas: {list(history["seasons"].keys())}')

if __name__ == '__main__':
    main()
