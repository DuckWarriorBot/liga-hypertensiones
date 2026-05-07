#!/usr/bin/env python3
"""
fetch_all.py — Descarga todos los datos de la temporada de forma autónoma.
Sin necesidad de Excel ni archivos manuales.

Fuentes:
  1. marca.com/futbol/segunda-division/calendario.html
     → calendario completo J1-J42 (resultados + fechas futuras)
  2. football-data.co.uk/mmz4281/YYMM/SP2.csv  (opcional)
     → validación/corrección de marcadores

Genera:
  - liga_data.json   (estructura principal del sistema)
  - scores_data.json (marcadores gol-gol por equipo y jornada)

Uso:
  python fetch_all.py             # temporada actual (25_26)
  python fetch_all.py 26_27       # otra temporada
"""

import json, re, sys, os, unicodedata
import requests
from collections import defaultdict

# Forzar UTF-8 en stdout para evitar UnicodeEncodeError en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── Configuración por temporada ───────────────────────────────────────────────
SEASONS = {
    '25_26': {
        'marca_cal_url':   'https://www.marca.com/futbol/segunda-division/calendario.html',
        'marca_clas_url':  'https://www.marca.com/futbol/segunda-division/clasificacion.html',
        'num_teams': 22,
        'total_season_rounds': 42,
    },
    # Para añadir temporada 26_27 (las URLs de Marca son siempre las mismas):
    # '26_27': {
    #     'marca_cal_url':  'https://www.marca.com/futbol/segunda-division/calendario.html',
    #     'marca_clas_url': 'https://www.marca.com/futbol/segunda-division/clasificacion.html',
    #     'num_teams': 22,
    #     'total_season_rounds': 42,
    # },
}

SEASON = sys.argv[1] if len(sys.argv) > 1 else '25_26'
if SEASON not in SEASONS:
    print(f'✗ Temporada "{SEASON}" no configurada. Añádela en SEASONS.')
    sys.exit(1)

cfg    = SEASONS[SEASON]
MARCA_CAL_URL       = cfg['marca_cal_url']
MARCA_CLAS_URL      = cfg['marca_clas_url']
NUM_TEAMS           = cfg['num_teams']
MPR                 = NUM_TEAMS // 2      # partidos por jornada (11 para 22 equipos)
TOTAL_SEASON_ROUNDS = cfg['total_season_rounds']

# ── Mapeo nombres Marca.com → nombres internos del sistema ───────────────────
MARCA_MAP = {
    'FC Andorra':             'Andorra',
    'Zaragoza':               'Real Zaragoza',
    'Deportivo':              'Deportivo',
    'Deportivo de la Coruña': 'Deportivo',
    'Mirandés':               'Mirandés',
    'Leganés':                'Leganés',
    'Córdoba':                'Córdoba',
    'Castellón':              'Castellón',
    'Málaga':                 'Málaga',
    'Almería':                'Almería',
    'Cádiz':                  'Cádiz',
    'Las Palmas':             'Las Palmas',
    'Real Sociedad B':        'Real Sociedad B',
    # Nombres que ya coinciden (explícitos para claridad):
    'Racing':                 'Racing',
    'Sporting':               'Sporting',
    'Cultural Leonesa':       'Cultural Leonesa',
    'Valladolid':             'Valladolid',
    'Ceuta':                  'Ceuta',
    'Burgos':                 'Burgos',
    'Albacete':               'Albacete',
    'Granada':                'Granada',
    'Huesca':                 'Huesca',
    'Eibar':                  'Eibar',
}


def _strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def norm_marca(name):
    """Normaliza un nombre de Marca.com al nombre interno del sistema."""
    name = name.strip()
    name = re.sub(r'\s+', ' ', name)
    if name in MARCA_MAP:
        return MARCA_MAP[name]
    # Intento sin acentos
    nf = _strip_accents(name)
    for k, v in MARCA_MAP.items():
        if _strip_accents(k) == nf:
            return v
    return name  # fallback: devolver tal cual


# ── Patrones de reconocimiento ────────────────────────────────────────────────
SCORE_RE    = re.compile(r'^\d{1,2}-\d{1,2}$')
DATETIME_RE = re.compile(r'^(\d{2}/\d{2})(?:\s+(\d{2}:\d{2}))?')


def _strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s)


def _clean_cell(s):
    """Limpia HTML entities y espacios de una celda."""
    s = _strip_tags(s)
    s = re.sub(r'&[a-z]+;', '', s)
    s = re.sub(r'&#\d+;', '', s)
    return re.sub(r'\s+', ' ', s).strip()


# ── 1. Descarga Marca.com ─────────────────────────────────────────────────────
def fetch_html(url):
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    }
    print(f'  GET {url}')
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


# ── 2. Parser de calendario ───────────────────────────────────────────────────
def parse_match_cells(cells):
    """
    Dada una lista de textos de celdas, intenta extraer un partido.
    Devuelve dict o None.
    """
    if len(cells) < 3:
        return None
    home = cells[0].strip()
    mid  = cells[1].strip()
    away = cells[2].strip()
    if not home or not away or not mid:
        return None
    is_score = bool(SCORE_RE.match(mid))
    dm = DATETIME_RE.match(mid)
    is_date  = bool(dm) and not is_score
    if not (is_score or is_date):
        return None
    return {
        'home':   norm_marca(home),
        'away':   norm_marca(away),
        'score':  mid if is_score else None,
        'date':   dm.group(1) if dm else None,
        'time':   dm.group(2) if dm else None,
        'played': is_score,
    }


def parse_rounds_html(html):
    """
    Extrae jornadas del HTML de Marca.com.
    Estrategia principal: buscar <tr> con exactamente 3 <td>.
    """
    td_re = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    tr_re = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)

    all_matches = []
    for tr_m in tr_re.finditer(html):
        cells = [_clean_cell(td.group(1)) for td in td_re.finditer(tr_m.group(1))]
        m = parse_match_cells(cells)
        if m:
            all_matches.append(m)

    if len(all_matches) < MPR:
        print('  ⚠ Parse HTML insuficiente, intentando modo texto...')
        return parse_rounds_text(html)

    print(f'  {len(all_matches)} filas de partido encontradas en HTML')
    return group_into_rounds(all_matches)


def parse_rounds_text(raw):
    """Fallback: parsea el texto plano buscando filas separadas por '|'."""
    text = _strip_tags(raw)
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'&#\d+;', '', text)

    all_matches = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split('|')]
        parts = [p for p in parts if p]
        m = parse_match_cells(parts)
        if m:
            all_matches.append(m)

    print(f'  {len(all_matches)} filas de partido encontradas en texto')
    return group_into_rounds(all_matches)


def group_into_rounds(all_matches):
    """Agrupa partidos en jornadas de MPR (11) partidos cada una."""
    rounds = []
    i = 0
    while i + MPR <= len(all_matches):
        rounds.append(all_matches[i:i + MPR])
        i += MPR
    # Última jornada parcial (temporada en curso, última jornada incompleta)
    if i < len(all_matches):
        rounds.append(all_matches[i:])
    return rounds


# ── 3. Parser clasificación Marca.com ────────────────────────────────────────
def parse_clasificacion(html):
    """
    Parsea la tabla de clasificación de Marca y devuelve lista de dicts:
      {name, pts, pj, wins, draws, losses, gf, gc,
       home_pts, home_pj, home_pg, home_pe, home_pp, home_gf, home_gc,
       away_pts, away_pj, away_pg, away_pe, away_pp, away_gf, away_gc}
    """
    td_re = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    tr_re = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    rows = []
    for tr_m in tr_re.finditer(html):
        cells = [_clean_cell(td.group(1)) for td in td_re.finditer(tr_m.group(1))]
        # Formato esperado: pos | nombre | pts | pj | pg | pe | pp | gf | gc
        #                   | h_pts | h_pj | h_pg | h_pe | h_pp | h_gf | h_gc
        #                   | a_pts | a_pj | a_pg | a_pe | a_pp | a_gf | a_gc
        if len(cells) < 9:
            continue
        if not cells[0].isdigit():
            continue
        try:
            # El nombre puede estar duplicado por la estructura del HTML (ej: "Racing Santander Racing Santander")
            raw_name = cells[1].strip()
            # Quitar duplicación: si la mitad inicial == segunda mitad
            mid = len(raw_name) // 2
            if raw_name[:mid].strip() == raw_name[mid:].strip():
                raw_name = raw_name[:mid].strip()
            name = norm_marca(raw_name)
            nums = []
            for c in cells[2:]:
                c = c.strip()
                if c.lstrip('-').isdigit():
                    nums.append(int(c))
            if len(nums) < 7:
                continue
            entry = {
                'name': name,
                'pts': nums[0], 'pj': nums[1], 'wins': nums[2],
                'draws': nums[3], 'losses': nums[4], 'gf': nums[5], 'gc': nums[6],
            }
            if len(nums) >= 21:
                entry.update({
                    'home_pts': nums[7],  'home_pj': nums[8],
                    'home_pg':  nums[9],  'home_pe': nums[10], 'home_pp': nums[11],
                    'home_gf':  nums[12], 'home_gc': nums[13],
                    'away_pts': nums[14], 'away_pj': nums[15],
                    'away_pg':  nums[16], 'away_pe': nums[17], 'away_pp': nums[18],
                    'away_gf':  nums[19], 'away_gc': nums[20],
                })
            rows.append(entry)
        except (ValueError, IndexError):
            continue
    return rows


# ── 4. Computar liga_data y scores_data ──────────────────────────────────────
def compute_data(rounds, total_season_rounds=42, extra_stats=None):
    """
    A partir de las jornadas parseadas, construye todos los datos del sistema.
    Devuelve (liga_data_dict, scores_data_dict).
    """
    # Recoger todos los equipos
    teams_set = set()
    for rnd in rounds:
        for m in rnd:
            teams_set.add(m['home'])
            teams_set.add(m['away'])
    teams = sorted(teams_set)

    # Resultados y marcadores
    results_by_team = defaultdict(list)   # ['V','E','D',...]
    scores_data     = defaultdict(dict)   # {team: {str(round_idx): "gf-gc"}}

    for r_idx, rnd in enumerate(rounds):
        for m in rnd:
            if not m['played']:
                continue
            home, away = m['home'], m['away']
            hg, ag = map(int, m['score'].split('-'))

            # Resultado para cada equipo
            if hg > ag:
                results_by_team[home].append('V')
                results_by_team[away].append('D')
            elif hg == ag:
                results_by_team[home].append('E')
                results_by_team[away].append('E')
            else:
                results_by_team[home].append('D')
                results_by_team[away].append('V')

            # Marcador desde la perspectiva de cada equipo (propios primero)
            scores_data[home][str(r_idx)] = f'{hg}-{ag}'
            scores_data[away][str(r_idx)] = f'{ag}-{hg}'

    # Número de jornadas jugadas (última con al menos 1 resultado)
    rounds_played = 0
    for r_idx, rnd in enumerate(rounds):
        if any(m['played'] for m in rnd):
            rounds_played = r_idx + 1

    print(f'  Jornadas jugadas: {rounds_played} / {len(rounds)} totales')

    # ── Historial de posiciones y puntos (tras cada jornada) ──────────────────
    positions_by_team = {t: [] for t in teams}
    points_by_team    = {t: [] for t in teams}

    for r_idx in range(rounds_played):
        # ¿Jornada completamente jugada? (o al menos >80% de partidos)
        played_count = sum(1 for m in rounds[r_idx] if m['played'])
        if played_count == 0:
            break

        snap = []
        for t in teams:
            res  = results_by_team[t][:r_idx + 1]
            pts  = sum(3 if x == 'V' else 1 if x == 'E' else 0 for x in res)
            wins = res.count('V')
            gf = gc = 0
            for i2 in range(r_idx + 1):
                sc = scores_data[t].get(str(i2))
                if sc:
                    a, b = map(int, sc.split('-'))
                    gf += a; gc += b
            snap.append({'name': t, 'pts': pts, 'wins': wins, 'dif': gf - gc})

        snap.sort(key=lambda x: (-x['pts'], -x['wins'], -x['dif']))
        for pos, t in enumerate(snap, 1):
            positions_by_team[t['name']].append(pos)
            points_by_team[t['name']].append(t['pts'])

    # ── Clasificación final ────────────────────────────────────────────────────
    final_standing = []
    for t in teams:
        res    = results_by_team[t]
        pts    = sum(3 if x == 'V' else 1 if x == 'E' else 0 for x in res)
        wins   = res.count('V')
        draws  = res.count('E')
        losses = res.count('D')
        gf = gc = 0
        for sc in scores_data[t].values():
            a, b = map(int, sc.split('-'))
            gf += a; gc += b
        final_standing.append({
            'name': t, 'pts': pts, 'wins': wins, 'draws': draws,
            'losses': losses, 'played': len(res), 'gf': gf, 'gc': gc,
            'dif': gf - gc,
        })
    final_standing.sort(key=lambda x: (-x['pts'], -x['wins'], -x['dif']))
    for pos, t in enumerate(final_standing, 1):
        t['pos'] = pos

    # ── Situación y partidos que quedan ───────────────────────────────────────
    get_pts = lambda pos: final_standing[pos - 1]['pts'] if len(final_standing) >= pos else 0
    pts2  = get_pts(2)
    pts3  = get_pts(3)   # para calcular cuánto falta para ASEGURAR el ascenso (pos 1-2)
    pts6  = get_pts(6)
    pts18 = get_pts(18)
    pts19 = get_pts(19)  # primer descendido, para medir peligro real de descenso

    rounds_left       = total_season_rounds - rounds_played
    max_pts           = rounds_left * 3
    situacion_by_team = {}
    quedan_by_team    = {}

    for t in final_standing:
        quedan_by_team[t['name']] = max_pts
        pos = t['pos']
        pts = t['pts']

        if pos <= 2:
            # Zona ascenso directo.
            # "A X del ascenso" = puntos que necesita para que el 3º ya no pueda alcanzarle
            # (suponiendo que el 3º gana todos los que le quedan).
            gap = pts3 + max_pts - pts
            if gap <= 0:
                sit = 'ASCENSO ASEGURADO'
            else:
                sit = f'A {gap} DEL ASCENSO'

        elif pos <= 6:
            # Zona playoff: muestran distancia al ascenso directo (2º puesto).
            sit = f'A {pts2 - pts} DEL ASCENSO'

        elif pos == 7:
            # Justo fuera del playoff.
            sit = f'A {pts6 - pts} DEL PLAYOFF'

        elif pos <= 18:
            # Zona media: puede perseguir playoff o estar amenazado de descenso.
            d_play = pts6 - pts          # puntos que le separan del playoff
            d_desc = pts - pts19         # ventaja sobre el primer descendido

            cant_play    = d_play > max_pts   # imposible alcanzar el playoff
            cant_relegate = d_desc > max_pts  # imposible ser alcanzado por el 19º

            if cant_play and cant_relegate:
                sit = 'PERMANENCIA'
            elif cant_play:
                # Sólo peligro de descenso: mostrar distancia de seguridad sobre 19º
                sit = f'A {d_desc} DEL DESCENSO'
            elif cant_relegate:
                # Sólo persiguiendo playoff
                sit = f'A {d_play} DEL PLAYOFF'
            else:
                # Ambas opciones vivas: mostrar la referencia más cercana
                if d_play <= d_desc:
                    sit = f'A {d_play} DEL PLAYOFF'
                else:
                    sit = f'A {d_desc} DEL DESCENSO'

        else:
            # Zona descenso (pos 19-22).
            gap = pts18 - pts   # puntos por debajo de la salvación
            if gap > max_pts:
                sit = 'DESCENSO ASEGURADO'
            else:
                sit = f'A {gap} DE SALVACIÓN'

        situacion_by_team[t['name']] = sit

    # ── opponents_by_team ─────────────────────────────────────────────────────
    opponents_by_team = {t: [None] * total_season_rounds for t in teams}
    for r_idx, rnd in enumerate(rounds):
        if r_idx >= total_season_rounds:
            break
        for m in rnd:
            home, away = m['home'], m['away']
            if home in opponents_by_team:
                opponents_by_team[home][r_idx] = away
            if away in opponents_by_team:
                opponents_by_team[away][r_idx] = home

    # ── Fixtures pendientes y días de partido ─────────────────────────────────
    import datetime as _dt
    fixtures = []
    match_days = {}   # {'DD/MM': ['HH:MM', ...]}
    for r_idx, rnd in enumerate(rounds):
        for m in rnd:
            if not m['played']:
                d = m.get('date')
                t = m.get('time')
                fixtures.append({'round': r_idx, 'home': m['home'], 'away': m['away'],
                                  'date': d, 'time': t})
                if d:
                    if d not in match_days:
                        match_days[d] = []
                    if t and t not in match_days[d]:
                        match_days[d].append(t)

    # ── extra_stats de clasificacion.html → enriquece final_standings ─────────
    if extra_stats:
        for t in final_standing:
            ex = extra_stats.get(t['name'], {})
            for key in ('home_pts','home_pj','home_pg','home_pe','home_pp',
                        'home_gf','home_gc','away_pts','away_pj','away_pg',
                        'away_pe','away_pp','away_gf','away_gc'):
                if key in ex:
                    t[key] = ex[key]

    liga_data = {
        'teams':               teams,
        'total_rounds':        rounds_played,
        'total_season_rounds': total_season_rounds,
        'last_updated':        _dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'results_by_team':     dict(results_by_team),
        'positions_by_team':   positions_by_team,
        'points_by_team':      points_by_team,
        'final_standings':     final_standing,
        'situacion_by_team':   situacion_by_team,
        'quedan_by_team':      quedan_by_team,
        'opponents_by_team':   opponents_by_team,
        'fixtures':            fixtures,
        'match_days':          match_days,
    }

    return liga_data, dict(scores_data)


# ── 5. Escudos desde BeSoccer ─────────────────────────────────────────────────
BESOCCER_CLAS_URL = 'https://es.besoccer.com/competicion/clasificacion/segunda'
SHIELD_CDN_RE     = re.compile(r'cdn\.resfu\.com/img_data/equipos/(\d+)', re.IGNORECASE)
BS_NAME_BADGE_RE  = re.compile(
    r'<(?:img|source)[^>]+src="(https://cdn\.resfu\.com/img_data/equipos/\d+[^"]*)"[^>]*>',
    re.IGNORECASE,
)


def fetch_besoccer_shields(teams_internal):
    """
    Descarga la clasificación de BeSoccer y extrae {nombre_interno: URL_escudo}.
    Guarda los resultados en besoccer_ids.json para que build.py los lea.
    Solo actualiza los equipos presentes en teams_internal.
    Devuelve el dict (puede estar vacío si la página no es parseable).
    """
    try:
        print(f'  GET {BESOCCER_CLAS_URL}')
        html = fetch_html(BESOCCER_CLAS_URL)
    except Exception as e:
        print(f'  ⚠ BeSoccer no disponible: {e}')
        return {}

    # Buscar todos los JSON-LD de tipo SportsOrganization/SportsTeam
    ld_re = re.compile(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
                       re.DOTALL | re.IGNORECASE)
    shield_ids   = {}
    badge_urls   = {}

    for raw in ld_re.findall(html):
        try:
            ld = json.loads(raw.strip())
        except Exception:
            continue
        objs = ld if isinstance(ld, list) else [ld]
        for obj in objs:
            t_type = obj.get('@type', '')
            if t_type not in ('SportsTeam', 'SportsOrganization', 'Organization'):
                continue
            name  = obj.get('name', '').strip()
            image = obj.get('image', '') or obj.get('logo', '')
            if not name or not image:
                continue
            internal = norm_marca(name)
            if internal not in teams_internal:
                # intentar buscar por BS_MAP si está disponible
                continue
            m = SHIELD_CDN_RE.search(image)
            if m:
                shield_ids[internal]  = m.group(1)
                badge_urls[internal]  = f'https://cdn.resfu.com/img_data/equipos/{m.group(1)}.png'

    # Fallback: si JSON-LD no dio resultados, buscar patrón CDN en HTML bruto
    # emparejando con nombres de equipo cercanos
    if not badge_urls:
        # Buscar todas las URLs CDN en el HTML y asociarlas por posición
        all_cdns = SHIELD_CDN_RE.findall(html)
        # Extraer nombres de tabla (texto de celdas de nombre de equipo)
        name_re = re.compile(r'class="[^"]*team-name[^"]*"[^>]*>([^<]+)<', re.IGNORECASE)
        names_found = [n.strip() for n in name_re.findall(html) if n.strip()]
        for i, bs_name in enumerate(names_found):
            internal = norm_marca(bs_name)
            if internal in teams_internal and i < len(all_cdns):
                sid = all_cdns[i]
                shield_ids[internal]  = sid
                badge_urls[internal]  = f'https://cdn.resfu.com/img_data/equipos/{sid}.png'

    if badge_urls:
        ids_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'besoccer_ids.json')
        # Leer existente y hacer merge (sin borrar equipos que ya teníamos)
        existing = {}
        if os.path.exists(ids_path):
            try:
                existing = json.loads(open(ids_path, encoding='utf-8').read()).get('shield_ids', {})
            except Exception:
                pass
        existing.update(shield_ids)
        with open(ids_path, 'w', encoding='utf-8') as f:
            json.dump({'shield_ids': existing}, f, ensure_ascii=False, indent=2)
        print(f'  {len(badge_urls)} escudos actualizados en besoccer_ids.json')
    else:
        print('  ⚠ No se encontraron escudos en BeSoccer (página JS-rendered)')

    return badge_urls


# ── 6. Main ───────────────────────────────────────────────────────────────────
def main():
    print(f'=== fetch_all.py — Temporada {SEASON} ===\n')

    # Paso 1: Calendario de Marca.com
    print('[1/3] Descargando calendario de Marca.com ...')
    html_cal = fetch_html(MARCA_CAL_URL)
    rounds   = parse_rounds_html(html_cal)
    if not rounds:
        print('✗ No se pudo parsear el calendario de Marca.com')
        sys.exit(1)
    total_found = sum(len(r) for r in rounds)
    print(f'  {len(rounds)} jornadas, {total_found} partidos en total')

    expected = TOTAL_SEASON_ROUNDS * MPR
    if total_found != expected:
        print(f'  ⚠ Esperados {expected} partidos, encontrados {total_found}.')

    # Paso 2: Clasificación oficial de Marca.com (GF/GC, stats casa/fuera)
    print('\n[2/4] Descargando clasificación de Marca.com ...')
    html_clas    = fetch_html(MARCA_CLAS_URL)
    clas_rows    = parse_clasificacion(html_clas)
    extra_stats  = {r['name']: r for r in clas_rows}
    print(f'  {len(clas_rows)} equipos en tabla de clasificación')

    # Paso 3: Computar datos y guardar JSONs
    print('\n[3/4] Computando datos del sistema ...')
    liga_data, scores_data = compute_data(rounds, TOTAL_SEASON_ROUNDS, extra_stats)

    out_dir = os.path.dirname(os.path.abspath(__file__))
    liga_path   = os.path.join(out_dir, 'liga_data.json')
    scores_path = os.path.join(out_dir, 'scores_data.json')

    with open(liga_path, 'w', encoding='utf-8') as f:
        json.dump(liga_data, f, ensure_ascii=False, indent=2)
    with open(scores_path, 'w', encoding='utf-8') as f:
        json.dump(scores_data, f, ensure_ascii=False, indent=2)

    print(f'\n✓ {liga_path}')
    print(f'✓ {scores_path}')
    print(f'  Equipos:           {len(liga_data["teams"])}')
    print(f'  Jornadas jugadas:  {liga_data["total_rounds"]}')
    print(f'  Jornadas totales:  {liga_data["total_season_rounds"]}')
    print('\nClasificación actual (Top 5):')
    for t in liga_data['final_standings'][:5]:
        print(f'  {t["pos"]}. {t["name"]:25s} {t["pts"]:3d} pts  '
              f'{t["wins"]}V {t["draws"]}E {t["losses"]}D')

    # Paso 4: Escudos desde BeSoccer (actualiza besoccer_ids.json)
    print('\n[4/4] Actualizando escudos desde BeSoccer ...')
    fetch_besoccer_shields(set(liga_data['teams']))

    # Guardar en BD SQLite
    try:
        import db
        db.save_liga_data(liga_data, SEASON)
        db.save_scores_data(scores_data, SEASON)
        print('\n✓ liga.db actualizado')
    except Exception as e:
        print(f'\n  ⚠ DB write failed: {e}')


if __name__ == '__main__':
    main()
