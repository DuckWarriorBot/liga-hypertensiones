"""
fetch_scores.py
Descarga resultados SP2 desde football-data.co.uk.
Enfoque: 418 filas → 38 grupos de 11 (una jornada c/u, orden cronológico).
  HomeTeam → venue='H'  |  AwayTeam → venue='A'
Cobertura: 836/836 (100%).  Coherencia V/E/D: ~99%.
"""
import json, csv, urllib.request
from io import StringIO

# ─── Mapeo football-data → nombres internos ────────────────────────────────
FD_MAP = {
    'Albacete':         'Albacete',
    'Almería':          'Almería',
    'Almeria':          'Almería',
    'Andorra':          'Andorra',
    'Burgos':           'Burgos',
    'Cádiz':            'Cádiz',
    'Cadiz':            'Cádiz',
    'Castellón':        'Castellón',
    'Castellon':        'Castellón',
    'Ceuta':            'Ceuta',
    'Córdoba':          'Córdoba',
    'Cordoba':          'Córdoba',
    'Cultural Leonesa': 'Cultural Leonesa',
    'Eibar':            'Eibar',
    'Granada':          'Granada',
    'Huesca':           'Huesca',
    'La Coruna':        'Deportivo',
    'Las Palmas':       'Las Palmas',
    'Leganés':          'Leganés',
    'Leganes':          'Leganés',
    'Málaga':           'Málaga',
    'Malaga':           'Málaga',
    'Mirandés':         'Mirandés',
    'Mirandes':         'Mirandés',
    'Santander':        'Racing',
    'Sociedad B':       'Real Sociedad B',
    'Sp Gijon':         'Sporting',
    'Valladolid':       'Valladolid',
    'Zaragoza':         'Real Zaragoza',
}

# ─── Descargar CSV ──────────────────────────────────────────────────────────
URL = 'https://www.football-data.co.uk/mmz4281/2526/SP2.csv'
print(f'Descargando {URL} ...')
req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=20) as resp:
    raw = resp.read().decode('utf-8', errors='replace')

rows = [r for r in csv.DictReader(StringIO(raw))
        if r.get('FTHG', '').strip() and r.get('FTAG', '').strip()]
print(f'  {len(rows)} partidos con marcador')

# ─── Cargar equipos ─────────────────────────────────────────────────────────
with open('liga_data.json', encoding='utf-8') as f:
    liga = json.load(f)
teams       = liga['teams']
results_map = liga['results_by_team']
opps_map    = liga.get('opponents_by_team', {})

# ─── Asignar marcadores cruzando por nombre de equipos ──────────────────────
# Usamos opponents_by_team para encontrar el índice exacto de cada partido,
# evitando desalineaciones por partidos aplazados en el CSV cronológico.
# used_idx[team] = set de índices ya asignados, para evitar sobreescrituras
# cuando dos partidos del mismo par tienen el mismo resultado.
scores_by_team = {t: {} for t in teams}
venue_by_team  = {t: {} for t in teams}
used_idx       = {t: set() for t in teams}
assigned = 0
unmapped = set()
unmatched = []

for row in rows:
    h_fd = row.get('HomeTeam', '').strip()
    a_fd = row.get('AwayTeam', '').strip()
    hg   = int(row['FTHG'])
    ag   = int(row['FTAG'])

    h_int = FD_MAP.get(h_fd)
    a_int = FD_MAP.get(a_fd)

    if not h_int:
        unmapped.add(h_fd)
    if not a_int:
        unmapped.add(a_fd)
    if not h_int or not a_int:
        continue

    h_opps  = opps_map.get(h_int, [])
    h_res   = results_map.get(h_int, [])
    exp_res = 'V' if hg > ag else ('E' if hg == ag else 'D')

    # 1º: opp + resultado correcto + índice no usado aún
    idx = next(
        (i for i, o in enumerate(h_opps)
         if o == a_int and i < len(h_res) and h_res[i] == exp_res
         and i not in used_idx[h_int]),
        None
    )
    # 2º fallback: cualquier índice con ese rival no usado aún
    if idx is None:
        idx = next(
            (i for i, o in enumerate(h_opps)
             if o == a_int and i not in used_idx[h_int]),
            None
        )

    if idx is None:
        unmatched.append((h_int, a_int))
        continue

    scores_by_team[h_int][idx] = f'{hg}-{ag}'
    venue_by_team[h_int][idx]  = 'H'
    scores_by_team[a_int][idx] = f'{ag}-{hg}'
    venue_by_team[a_int][idx]  = 'A'
    used_idx[h_int].add(idx)
    used_idx[a_int].add(idx)
    assigned += 2

if unmapped:
    print(f'  Sin mapeo FD_MAP: {unmapped}')
if unmatched:
    print(f'  Sin índice en opponents_by_team ({len(unmatched)}): {unmatched[:5]}')
print(f'  Asignaciones: {assigned} / {len(rows) * 2}')

# ─── Verificación coherencia V/E/D ──────────────────────────────────────────
ok = ko = 0
for team in teams:
    res_list = results_map.get(team, [])
    for r_str, score in scores_by_team[team].items():
        r = r_str if isinstance(r_str, int) else int(r_str)
        if r >= len(res_list):
            continue
        vned = res_list[r]
        sc, cc = map(int, score.split('-'))
        if   vned == 'V' and sc > cc:  ok += 1
        elif vned == 'E' and sc == cc: ok += 1
        elif vned == 'D' and sc < cc:  ok += 1
        else:                          ko += 1
pct = ok / (ok + ko) * 100 if (ok + ko) else 0
print(f'  Coherencia V/E/D: {ok}/{ok+ko} ({pct:.1f}%)')

# ─── Guardar ────────────────────────────────────────────────────────────────
out = {'scores_by_team': scores_by_team, 'venue_by_team': venue_by_team}
with open('scores_data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False)
print('scores_data.json guardado OK')

# ─── Guardar en BD ──────────────────────────────────────────────────────────
try:
    import db
    db.save_scores_data(out, '25_26')
except Exception as e:
    print(f'  ⚠ DB write failed: {e}')

# ─── Verificación rápida J1-J5 ──────────────────────────────────────────────
print('\nVerificacion J1-J5:')
for t in ['Racing', 'Almería', 'Deportivo', 'Sporting']:
    parts = []
    for i in range(5):
        sc = scores_by_team[t].get(i, '?')
        vn = venue_by_team[t].get(i, '?')
        parts.append(f'J{i+1}:{sc}({vn})')
    print(f'  {t:<18} {" | ".join(parts)}')
