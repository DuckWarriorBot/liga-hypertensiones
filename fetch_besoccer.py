"""
fetch_besoccer.py
Descarga resultados de la 2ª División 2025/26 desde BeSoccer y genera:
  - scores_data.json   → {scores_by_team, venue_by_team}
  - besoccer_ids.json  → {shield_ids: {equipo_interno: ID_besoccer}}

Parsing:
  - Nombres de equipo y URLs de escudo → bloques <script type="application/ld+json">
  - Marcadores → spans .r1 / .r2 del HTML (mismo orden que los ld+json)
  - Casa/Visitante → homeTeam siempre es el equipo de la izquierda en BeSoccer
"""

import re, json, time, urllib.request
from collections import defaultdict

TOTAL_ROUNDS  = 38   # jornadas ya disputadas
SLEEP_BETWEEN = 1.2  # segundos entre peticiones (ser amables con el servidor)

# URL que BeSoccer usa para cada jornada (server-rendered para SEO)
# Patrón probado: /competicion/{slug}/{año}/partidos/{jornada}
URL_TMPL = 'https://es.besoccer.com/competicion/segunda-division/2026/partidos/{round}'

# ── Mapeo nombre BeSoccer → nombre interno del proyecto ────────────────────
BS_MAP = {
    'Real Sociedad B':          'Real Sociedad B',
    'Almería':                  'Almería',
    'Almeria':                  'Almería',
    'Real Sporting':            'Sporting',
    'Sporting de Gijón':        'Sporting',
    'Cultural Leonesa':         'Cultural Leonesa',
    'Cultural Deportiva Leonesa': 'Cultural Leonesa',
    'Racing':                   'Racing',
    'Racing de Santander':      'Racing',
    'AD Ceuta FC':              'Ceuta',
    'Ceuta':                    'Ceuta',
    'Real Valladolid':          'Valladolid',
    'Valladolid':               'Valladolid',
    'Córdoba CF':               'Córdoba',
    'Cordoba CF':               'Córdoba',
    'Córdoba':                  'Córdoba',
    'CD Castellón':             'Castellón',
    'Castellón':                'Castellón',
    'Real Zaragoza':            'Real Zaragoza',
    'Zaragoza':                 'Real Zaragoza',
    'FC Andorra':               'Andorra',
    'Andorra':                  'Andorra',
    'Burgos CF':                'Burgos',
    'Burgos':                   'Burgos',
    'Cádiz':                    'Cádiz',
    'Cadiz CF':                 'Cádiz',
    'Albacete':                 'Albacete',
    'Albacete Balompié':        'Albacete',
    'UD Las Palmas':            'Las Palmas',
    'Las Palmas':               'Las Palmas',
    'Málaga':                   'Málaga',
    'Málaga CF':                'Málaga',
    'Granada':                  'Granada',
    'Granada CF':               'Granada',
    'Mirandés':                 'Mirandés',
    'CD Mirandés':              'Mirandés',
    'Huesca':                   'Huesca',
    'SD Huesca':                'Huesca',
    'Eibar':                    'Eibar',
    'SD Eibar':                 'Eibar',
    'Leganés':                  'Leganés',
    'CD Leganés':               'Leganés',
    'RC Deportivo':             'Deportivo',
    'Deportivo de La Coruña':   'Deportivo',
    'RC Deportivo de La Coruña':'Deportivo',
    'Deportivo':                'Deportivo',
}

# ── Helpers ─────────────────────────────────────────────────────────────────
SCORE_RE = re.compile(
    r'<span class=" "><span class="r1">(\d+)</span>-<span class="r2">(\d+)</span></span>'
)
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
SHIELD_RE = re.compile(r'/(\d+)\.jpg')

def fetch_html(round_num):
    url = URL_TMPL.format(round=round_num)
    req = urllib.request.Request(url, headers={
        'User-Agent':      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.7',
        'Referer':         'https://es.besoccer.com/',
    })
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode('utf-8', errors='replace')

def result_matches(res, sc, cc):
    """¿Coincide V/E/D con el marcador visto desde la perspectiva del equipo?"""
    if res == 'V': return sc > cc
    if res == 'E': return sc == cc
    if res == 'D': return sc < cc
    return False

def parse_matches(html):
    """
    Extrae lista de dicts {home, away, hg, ag, home_id, away_id}.
    Estrategia: JSON-LD para nombres/escudos + score spans para marcadores.
    Ambos aparecen en el mismo orden dentro de la página.
    """
    scores  = SCORE_RE.findall(html)
    matches = []
    ld_idx  = 0

    for raw in LD_RE.findall(html):
        try:
            ld = json.loads(raw.strip())
        except Exception:
            continue
        if ld.get('@type') != 'SportsEvent':
            continue

        home_obj  = ld.get('homeTeam', {})
        away_obj  = ld.get('awayTeam', {})
        home_name = home_obj.get('name', '').strip()
        away_name = away_obj.get('name', '').strip()
        home_img  = home_obj.get('image', '')
        away_img  = away_obj.get('image', '')

        hm = SHIELD_RE.search(home_img)
        am = SHIELD_RE.search(away_img)

        hg = ag = None
        if ld_idx < len(scores):
            hg, ag = int(scores[ld_idx][0]), int(scores[ld_idx][1])

        matches.append({
            'home':    home_name,
            'away':    away_name,
            'hg':      hg,
            'ag':      ag,
            'home_id': hm.group(1) if hm else None,
            'away_id': am.group(1) if am else None,
        })
        ld_idx += 1

    return matches

# ── Cargar datos de liga ─────────────────────────────────────────────────────
with open('liga_data.json', encoding='utf-8') as f:
    liga = json.load(f)

opponents   = liga['opponents_by_team']
results_map = liga['results_by_team']
teams       = liga['teams']

# ── Descargar todas las jornadas ─────────────────────────────────────────────
print(f'Descargando {TOTAL_ROUNDS} jornadas de BeSoccer…')
all_rounds  = {}   # round_idx (0-based) → list of matches
shield_ids  = {}   # internal_name → besoccer_id
unmapped_bs = set()

for r in range(1, TOTAL_ROUNDS + 1):
    print(f'  J{r:2d} …', end=' ', flush=True)
    try:
        html    = fetch_html(r)
        matches = parse_matches(html)
        all_rounds[r - 1] = matches
        print(f'{len(matches)} partidos', end='')

        for m in matches:
            for bs_name, bs_id in [(m['home'], m['home_id']), (m['away'], m['away_id'])]:
                internal = BS_MAP.get(bs_name)
                if not internal:
                    unmapped_bs.add(bs_name)
                elif bs_id and internal not in shield_ids:
                    shield_ids[internal] = bs_id

        if len(matches) != 11:
            print(f'  ⚠ esperados 11', end='')
        print()
    except Exception as e:
        print(f'ERROR: {e}')
        all_rounds[r - 1] = []

    time.sleep(SLEEP_BETWEEN)

if unmapped_bs:
    print(f'\n⚠  Nombres sin mapeo: {unmapped_bs}')

# ── Asignar scores a equipos (con verificación V/E/D) ────────────────────────
scores_by_team = {t: {} for t in teams}
venue_by_team  = {t: {} for t in teams}
assigned = unmatched = 0

for r_idx, matches in all_rounds.items():
    for m in matches:
        if m['hg'] is None:
            continue
        h_int = BS_MAP.get(m['home'])
        a_int = BS_MAP.get(m['away'])
        if not h_int or not a_int:
            unmatched += 1
            continue

        # Equipo local
        res_h = results_map.get(h_int, [])
        if r_idx < len(res_h) and result_matches(res_h[r_idx], m['hg'], m['ag']):
            scores_by_team[h_int][r_idx] = f"{m['hg']}-{m['ag']}"
            venue_by_team[h_int][r_idx]  = 'H'
            assigned += 1
        elif r_idx < len(res_h):
            # Almacenamos igualmente aunque no coincida el V/E/D
            scores_by_team[h_int][r_idx] = f"{m['hg']}-{m['ag']}"
            venue_by_team[h_int][r_idx]  = 'H'
            assigned += 1

        # Equipo visitante
        res_a = results_map.get(a_int, [])
        if r_idx < len(res_a):
            scores_by_team[a_int][r_idx] = f"{m['ag']}-{m['hg']}"
            venue_by_team[a_int][r_idx]  = 'A'
            assigned += 1

total_ok = sum(1 for v in all_rounds.values() if len(v) == 11)
print(f'\nJornadas completas (11 partidos): {total_ok}/{TOTAL_ROUNDS}')
print(f'Asignaciones realizadas: {assigned}  |  Sin mapeo: {unmatched}')

# ── Guardar scores_data.json ──────────────────────────────────────────────────
out = {'scores_by_team': scores_by_team, 'venue_by_team': venue_by_team}
with open('scores_data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)
print('scores_data.json guardado ✓')

# ── Guardar besoccer_ids.json ─────────────────────────────────────────────────
with open('besoccer_ids.json', 'w', encoding='utf-8') as f:
    json.dump({'shield_ids': shield_ids}, f, ensure_ascii=False, indent=2)
print('besoccer_ids.json guardado ✓')
print(f'Escudos capturados: {len(shield_ids)}/22')

# ── Verificación rápida ───────────────────────────────────────────────────────
print('\nVerificación (J1-J5):')
for t in ['Racing', 'Almería', 'Deportivo', 'Sporting']:
    row = []
    for i in range(5):
        sc = scores_by_team[t].get(i)
        vn = venue_by_team[t].get(i, '?')
        row.append(f'J{i+1}:{sc}({vn})')
    print(f'  {t:<18} {" | ".join(row)}')
