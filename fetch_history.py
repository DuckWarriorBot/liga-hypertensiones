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
  const teamLogos = {};

  // Capturar logos (Flashscore usa background-image en .event__logo)
  document.querySelectorAll('.event__match').forEach(el => {
    const logos = el.querySelectorAll('.event__logo');
    const parts = el.querySelectorAll('.event__participant');
    logos.forEach((logo, idx) => {
      const nameEl = parts[idx];
      if (!nameEl) return;
      const name = nameEl.innerText.trim().split('\n')[0].trim();
      if (!name || teamLogos[name]) return;
      const style = window.getComputedStyle(logo);
      const bg = style.getPropertyValue('background-image');
      const m = bg.match(/url\(["']?([^"')]+)["']?\)/);
      if (m && m[1] && m[1].startsWith('http')) teamLogos[name] = m[1];
    });
  });

  // Extraer rondas y partidos (incluye event__round--static para playoff)
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
  return { rows, teamLogos };
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

# ── Construcción del playoff ────────────────────────────────────────────────

def build_playoff_structure(playoff_matches, final_standings):
    """
    Construye la estructura estándar de playoff desde los partidos scrapeados.

    playoff_matches: [{home, away, score_h, score_a, round_label}]
    final_standings: lista ordenada (0-based), el top-6 define los participantes

    Formato: 3º vs 6º (SF1), 4º vs 5º (SF2), ganadores en la Final.
    Devuelve None si no hay suficientes datos.
    """
    from collections import defaultdict

    if len(final_standings) < 6 or not playoff_matches:
        return None

    valid = [m for m in playoff_matches if m.get('home') and m.get('away')]
    if not valid:
        return None

    # Mapeo de nombres de equipos a los nombres canónicos del clasificación.
    # Buscamos en el top-10 (no solo top-6) para manejar errores de desempate.
    top10_names = [t['name'] for t in final_standings[:10]]

    def _best_match(raw):
        """Devuelve el nombre canónico más cercano en top10 para raw."""
        if raw in top10_names:
            return raw
        rn = _norm(raw)
        for k in top10_names:
            if _norm(k) == rn:
                return k
        for k in top10_names:
            kn = _norm(k)
            if rn in kn or kn in rn:
                return k
        for k in top10_names:
            if _norm(k)[:5] == rn[:5]:
                return k
        return raw  # sin match: mantener original

    # Agrupar partidos por par de equipos (nombres canónicos)
    pair_matches = defaultdict(list)
    for m in valid:
        canon_home = _best_match(m['home'])
        canon_away = _best_match(m['away'])
        m = dict(m, home=canon_home, away=canon_away)
        key = tuple(sorted([canon_home, canon_away]))
        pair_matches[key].append(m)

    # Determinar los 4 equipos del playoff directamente de los partidos scrapeados.
    # Cada equipo se cuenta según cuántos pares distintos tiene. El de mayor pos en
    # standings actúa como "high seed" de su semifinal.
    po_teams_raw = set()
    for key in pair_matches:
        po_teams_raw.update(key)

    # Ordenar por posición en clasificación (si el equipo no aparece → pos 999)
    standings_pos = {t['name']: i for i, t in enumerate(final_standings)}

    # ── Detectar bracket automáticamente ──────────────────────────────────
    # La final es el par donde AMBOS equipos aparecen en 2 llaves distintas
    # (semifinalistas que ganaron su llave). Los otros 2 pares son las semis.
    from collections import Counter
    team_pair_count = Counter()
    for key in pair_matches:
        for team in key:
            team_pair_count[team] += 1

    # Finalistas: los 2 equipos que aparecen en 2 pares
    finalists = {t for t, c in team_pair_count.items() if c >= 2}
    final_key = next((k for k in pair_matches if set(k) == finalists), None)
    semi_keys = [k for k in pair_matches if k != final_key]

    def build_tie(team_high, team_low):
        """Construye un tie (eliminatoria a doble partido) entre dos equipos."""
        key = tuple(sorted([team_high, team_low]))
        legs = list(pair_matches.get(key, []))
        # Primer partido: team_high en casa (ida); segundo: team_low en casa (vuelta)
        legs.sort(key=lambda m: 0 if m['home'] == team_high else 1)

        agg_high = agg_low = 0
        match_structs = []
        for i, m in enumerate(legs[:2]):
            if m['home'] == team_high:
                agg_high += m['score_h']; agg_low += m['score_a']
            else:
                agg_high += m['score_a']; agg_low += m['score_h']
            match_structs.append({
                'home':   m['home'],
                'away':   m['away'],
                'score':  f"{m['score_h']}-{m['score_a']}",
                'played': True,
                'date':   None,
                'leg':    i + 1,
            })

        # Rellenar si faltan partidos
        while len(match_structs) < 2:
            if not match_structs:
                match_structs.append({'home': team_high, 'away': team_low,
                                      'score': None, 'played': False, 'date': None, 'leg': 1})
            else:
                match_structs.append({'home': team_low, 'away': team_high,
                                      'score': None, 'played': False, 'date': None, 'leg': 2})

        played_count = sum(1 for ms in match_structs if ms['played'])
        winner = agg_str = None
        if played_count >= 2:
            agg_str = f'{agg_high}-{agg_low}'
            if agg_high > agg_low:
                winner = team_high
            elif agg_low > agg_high:
                winner = team_low
            else:
                winner = team_high  # empate: clasifica el equipo de mayor posición

        return {'team_high': team_high, 'team_low': team_low,
                'matches': match_structs, 'agg': agg_str, 'winner': winner}

    # Construir semis desde las llaves detectadas
    def _high_low(pair_key):
        a, b = pair_key
        return (a, b) if standings_pos.get(a, 999) < standings_pos.get(b, 999) else (b, a)

    if len(semi_keys) == 2 and final_key:
        h1, l1 = _high_low(semi_keys[0])
        h2, l2 = _high_low(semi_keys[1])
        # SF1 = la semi donde el high seed tiene menor posición (más arriba en clasificación)
        if standings_pos.get(h1, 999) <= standings_pos.get(h2, 999):
            sf1 = build_tie(h1, l1); sf1['id'] = 'sf1'
            sf2 = build_tie(h2, l2); sf2['id'] = 'sf2'
        else:
            sf1 = build_tie(h2, l2); sf1['id'] = 'sf1'
            sf2 = build_tie(h1, l1); sf2['id'] = 'sf2'
    else:
        # Fallback: usar clasificación (3vs6, 4vs5)
        po_teams_sorted = sorted(po_teams_raw, key=lambda t: standings_pos.get(t, 999))
        if len(po_teams_sorted) >= 4:
            p3, p4, p5, p6 = po_teams_sorted[:4]
        else:
            p3 = final_standings[2]['name']; p4 = final_standings[3]['name']
            p5 = final_standings[4]['name']; p6 = final_standings[5]['name']
        sf1 = build_tie(p3, p6); sf1['id'] = 'sf1'
        sf2 = build_tie(p4, p5); sf2['id'] = 'sf2'
        final_key = None

    # Construir final
    if final_key:
        fw1 = sf1.get('winner') or sf1['team_high']
        fw2 = sf2.get('winner') or sf2['team_high']
        fin = build_tie(fw1, fw2)
        fh, fl = _high_low(final_key)
        fin = build_tie(fh, fl)
    else:
        fw1 = sf1.get('winner') or ''
        fw2 = sf2.get('winner') or ''
        fin = {
            'matches': [
                {'home': fw1, 'away': fw2, 'score': None, 'played': False, 'date': None, 'leg': 1},
                {'home': fw2, 'away': fw1, 'score': None, 'played': False, 'date': None, 'leg': 2},
            ],
            'agg': None, 'winner': None,
        }

    return {'semis': [sf1, sf2], 'final': fin}


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

    result = page.evaluate(JS_EXTRACT)
    raw       = result['rows']
    raw_logos = result.get('teamLogos', {})

    # Traducir logos Flashscore: raw_name → URL, mapeando al nombre interno
    team_badges = {}
    for raw_name, url in raw_logos.items():
        mapped = map_team(raw_name)
        if mapped and url and url.startswith('http'):
            team_badges[mapped] = url

    matches          = []
    playoff_matches_raw = []
    current_round    = None
    current_playoff_label = None
    in_playoff       = False

    PLAYOFF_LABELS = {'final', 'semifinales', 'semifinal', 'semifinals'}

    for row in raw:
        if row['type'] == 'round':
            txt = row['text'].strip().lower()
            if txt in PLAYOFF_LABELS:
                in_playoff = True
                current_playoff_label = row['text'].strip()
            elif re.match(r'jornada\s+\d+|round\s+\d+', txt):
                in_playoff = False
                current_playoff_label = None
                m = re.search(r'(\d+)', txt)
                if m:
                    current_round = int(m.group(1))
            continue

        home_raw, away_raw = row['home'], row['away']
        if not home_raw or not away_raw:
            continue

        home_int = map_team(home_raw)
        away_int = map_team(away_raw)

        if in_playoff:
            # Capturar partidos de playoff (en lugar de ignorarlos)
            try:
                score_h = int(row['scoreH'])
                score_a = int(row['scoreA'])
            except (ValueError, TypeError):
                continue
            playoff_matches_raw.append({
                'home':        home_int,
                'away':        away_int,
                'score_h':     score_h,
                'score_a':     score_a,
                'round_label': current_playoff_label,
            })
            continue

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
    playoff   = build_playoff_structure(playoff_matches_raw, standings)

    print(f'  ✓ {label}: {len(matches)} partidos · {len(all_teams)} equipos · J{total_rounds}', flush=True)
    if standings:
        print(f'    1º {standings[0]["name"]} {standings[0]["pts"]}pts · '
              f'Último {standings[-1]["name"]} {standings[-1]["pts"]}pts', flush=True)
    if playoff:
        winner = playoff['final'].get('winner') or 'no determinado'
        print(f'    Playoff: {len(playoff_matches_raw)} partidos · ganador: {winner}', flush=True)
    else:
        print(f'    Playoff: {len(playoff_matches_raw)} partidos scrapeados (sin estructura)', flush=True)

    return {
        'label':               label,
        'total_rounds':        total_rounds,
        'total_season_rounds': total_rounds,
        'teams':               sorted(all_teams),
        'final_standings':     standings,
        'opponents_by_team':   opponents_by_team,
        'results_by_team':     results_by_team,
        'scores_by_team':      scores_by_team,
        'venue_by_team':       venue_by_team,
        'playoff':             playoff,
        'team_badges':         team_badges,
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
