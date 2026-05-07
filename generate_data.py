import openpyxl, json

# ─── Calendario completo J1-J42 extraído de Marca.com ──────────────────────
# Cada tupla: (local, visitante) con nombres internos
FIXTURES = [
  # J1
  [('Burgos','Cultural Leonesa'),('Valladolid','Ceuta'),('Racing','Castellón'),
   ('Málaga','Eibar'),('Granada','Deportivo'),('Real Sociedad B','Real Zaragoza'),
   ('Cádiz','Mirandés'),('Huesca','Leganés'),('Las Palmas','Andorra'),
   ('Sporting','Córdoba'),('Almería','Albacete')],
  # J2
  [('Eibar','Granada'),('Castellón','Valladolid'),('Leganés','Cádiz'),
   ('Mirandés','Huesca'),('Ceuta','Sporting'),('Real Zaragoza','Andorra'),
   ('Deportivo','Burgos'),('Cultural Leonesa','Almería'),('Málaga','Real Sociedad B'),
   ('Albacete','Racing'),('Córdoba','Las Palmas')],
  # J3
  [('Real Sociedad B','Almería'),('Sporting','Cultural Leonesa'),('Racing','Ceuta'),
   ('Valladolid','Córdoba'),('Castellón','Real Zaragoza'),('Cádiz','Albacete'),
   ('Andorra','Burgos'),('Las Palmas','Málaga'),('Granada','Mirandés'),
   ('Huesca','Eibar'),('Leganés','Deportivo')],
  # J4
  [('Albacete','Mirandés'),('Córdoba','Castellón'),('Deportivo','Sporting'),
   ('Real Zaragoza','Valladolid'),('Málaga','Granada'),('Ceuta','Huesca'),
   ('Burgos','Las Palmas'),('Real Sociedad B','Cádiz'),('Almería','Racing'),
   ('Cultural Leonesa','Leganés'),('Eibar','Andorra')],
  # J5
  [('Las Palmas','Real Sociedad B'),('Cádiz','Eibar'),('Mirandés','Deportivo'),
   ('Huesca','Málaga'),('Valladolid','Almería'),('Andorra','Córdoba'),
   ('Racing','Cultural Leonesa'),('Castellón','Ceuta'),('Sporting','Burgos'),
   ('Granada','Leganés'),('Real Zaragoza','Albacete')],
  # J6
  [('Deportivo','Huesca'),('Cultural Leonesa','Castellón'),('Andorra','Mirandés'),
   ('Leganés','Las Palmas'),('Almería','Sporting'),('Ceuta','Real Zaragoza'),
   ('Albacete','Valladolid'),('Eibar','Real Sociedad B'),('Málaga','Cádiz'),
   ('Córdoba','Racing'),('Burgos','Granada')],
  # J7
  [('Mirandés','Real Zaragoza'),('Eibar','Deportivo'),('Racing','Andorra'),
   ('Las Palmas','Almería'),('Real Sociedad B','Córdoba'),('Burgos','Málaga'),
   ('Cádiz','Ceuta'),('Valladolid','Cultural Leonesa'),('Sporting','Albacete'),
   ('Huesca','Granada'),('Leganés','Castellón')],
  # J8
  [('Ceuta','Eibar'),('Deportivo','Almería'),('Andorra','Leganés'),
   ('Huesca','Burgos'),('Granada','Real Sociedad B'),('Real Zaragoza','Córdoba'),
   ('Castellón','Sporting'),('Racing','Málaga'),('Valladolid','Mirandés'),
   ('Las Palmas','Cádiz'),('Cultural Leonesa','Albacete')],
  # J9
  [('Granada','Las Palmas'),('Mirandés','Leganés'),('Almería','Real Zaragoza'),
   ('Real Sociedad B','Andorra'),('Albacete','Ceuta'),('Eibar','Castellón'),
   ('Sporting','Racing'),('Burgos','Valladolid'),('Cádiz','Huesca'),
   ('Málaga','Deportivo'),('Córdoba','Cultural Leonesa')],
  # J10
  [('Andorra','Granada'),('Ceuta','Mirandés'),('Real Zaragoza','Cultural Leonesa'),
   ('Leganés','Málaga'),('Castellón','Albacete'),('Valladolid','Sporting'),
   ('Córdoba','Almería'),('Racing','Deportivo'),('Las Palmas','Eibar'),
   ('Cádiz','Burgos'),('Real Sociedad B','Huesca')],
  # J11
  [('Huesca','Las Palmas'),('Cultural Leonesa','Ceuta'),('Albacete','Córdoba'),
   ('Eibar','Leganés'),('Burgos','Real Sociedad B'),('Granada','Cádiz'),
   ('Mirandés','Racing'),('Málaga','Andorra'),('Almería','Castellón'),
   ('Sporting','Real Zaragoza'),('Deportivo','Valladolid')],
  # J12
  [('Racing','Real Sociedad B'),('Cultural Leonesa','Mirandés'),('Albacete','Huesca'),
   ('Leganés','Burgos'),('Almería','Eibar'),('Andorra','Cádiz'),
   ('Córdoba','Ceuta'),('Sporting','Las Palmas'),('Castellón','Málaga'),
   ('Real Zaragoza','Deportivo'),('Valladolid','Granada')],
  # J13
  [('Mirandés','Sporting'),('Real Sociedad B','Leganés'),('Eibar','Albacete'),
   ('Huesca','Andorra'),('Deportivo','Cultural Leonesa'),('Málaga','Córdoba'),
   ('Las Palmas','Racing'),('Granada','Real Zaragoza'),('Cádiz','Valladolid'),
   ('Burgos','Castellón'),('Ceuta','Almería')],
  # J14
  [('Valladolid','Las Palmas'),('Albacete','Andorra'),('Castellón','Real Sociedad B'),
   ('Racing','Granada'),('Ceuta','Leganés'),('Almería','Cádiz'),
   ('Sporting','Eibar'),('Córdoba','Deportivo'),('Mirandés','Burgos'),
   ('Real Zaragoza','Huesca'),('Cultural Leonesa','Málaga')],
  # J15
  [('Las Palmas','Albacete'),('Andorra','Castellón'),('Eibar','Real Zaragoza'),
   ('Leganés','Almería'),('Granada','Córdoba'),('Deportivo','Ceuta'),
   ('Cádiz','Cultural Leonesa'),('Huesca','Sporting'),('Burgos','Racing'),
   ('Málaga','Mirandés'),('Real Sociedad B','Valladolid')],
  # J16
  [('Sporting','Andorra'),('Ceuta','Burgos'),('Cultural Leonesa','Granada'),
   ('Albacete','Deportivo'),('Almería','Huesca'),('Valladolid','Málaga'),
   ('Real Zaragoza','Leganés'),('Racing','Eibar'),('Córdoba','Cádiz'),
   ('Mirandés','Real Sociedad B'),('Castellón','Las Palmas')],
  # J17
  [('Andorra','Almería'),('Huesca','Valladolid'),('Real Sociedad B','Sporting'),
   ('Cádiz','Racing'),('Leganés','Córdoba'),('Deportivo','Castellón'),
   ('Eibar','Cultural Leonesa'),('Granada','Ceuta'),('Burgos','Albacete'),
   ('Las Palmas','Mirandés'),('Málaga','Real Zaragoza')],
  # J18
  [('Cultural Leonesa','Huesca'),('Córdoba','Eibar'),('Valladolid','Andorra'),
   ('Sporting','Granada'),('Racing','Leganés'),('Deportivo','Real Sociedad B'),
   ('Real Zaragoza','Cádiz'),('Albacete','Málaga'),('Almería','Burgos'),
   ('Ceuta','Las Palmas'),('Castellón','Mirandés')],
  # J19
  [('Eibar','Valladolid'),('Andorra','Deportivo'),('Huesca','Racing'),
   ('Leganés','Sporting'),('Las Palmas','Cultural Leonesa'),('Málaga','Almería'),
   ('Mirandés','Córdoba'),('Real Sociedad B','Ceuta'),('Burgos','Real Zaragoza'),
   ('Granada','Albacete'),('Cádiz','Castellón')],
  # J20
  [('Eibar','Mirandés'),('Cultural Leonesa','Real Sociedad B'),('Almería','Granada'),
   ('Castellón','Huesca'),('Valladolid','Racing'),('Córdoba','Burgos'),
   ('Sporting','Málaga'),('Ceuta','Andorra'),('Albacete','Leganés'),
   ('Real Zaragoza','Las Palmas'),('Deportivo','Cádiz')],
  # J21
  [('Cádiz','Sporting'),('Mirandés','Almería'),('Real Sociedad B','Albacete'),
   ('Burgos','Eibar'),('Andorra','Cultural Leonesa'),('Las Palmas','Deportivo'),
   ('Racing','Real Zaragoza'),('Leganés','Valladolid'),('Granada','Castellón'),
   ('Málaga','Ceuta'),('Huesca','Córdoba')],
  # J22
  [('Castellón','Leganés'),('Ceuta','Valladolid'),('Cultural Leonesa','Sporting'),
   ('Real Zaragoza','Real Sociedad B'),('Almería','Deportivo'),('Mirandés','Andorra'),
   ('Racing','Las Palmas'),('Albacete','Cádiz'),('Burgos','Huesca'),
   ('Córdoba','Málaga'),('Granada','Eibar')],
  # J23
  [('Málaga','Burgos'),('Valladolid','Albacete'),('Leganés','Real Sociedad B'),
   ('Las Palmas','Córdoba'),('Sporting','Mirandés'),('Cádiz','Granada'),
   ('Andorra','Huesca'),('Eibar','Almería'),('Real Zaragoza','Castellón'),
   ('Deportivo','Racing'),('Ceuta','Cultural Leonesa')],
  # J24
  [('Real Sociedad B','Las Palmas'),('Albacete','Real Zaragoza'),('Burgos','Leganés'),
   ('Cultural Leonesa','Deportivo'),('Córdoba','Valladolid'),('Almería','Ceuta'),
   ('Eibar','Sporting'),('Castellón','Andorra'),('Huesca','Cádiz'),
   ('Granada','Racing'),('Mirandés','Málaga')],
  # J25
  [('Leganés','Granada'),('Andorra','Real Sociedad B'),('Las Palmas','Burgos'),
   ('Real Zaragoza','Eibar'),('Valladolid','Castellón'),('Cádiz','Almería'),
   ('Deportivo','Albacete'),('Sporting','Huesca'),('Málaga','Cultural Leonesa'),
   ('Racing','Mirandés'),('Ceuta','Córdoba')],
  # J26
  [('Almería','Andorra'),('Córdoba','Leganés'),('Burgos','Cádiz'),
   ('Cultural Leonesa','Real Zaragoza'),('Granada','Valladolid'),('Mirandés','Las Palmas'),
   ('Eibar','Racing'),('Huesca','Ceuta'),('Albacete','Sporting'),
   ('Castellón','Deportivo'),('Real Sociedad B','Málaga')],
  # J27
  [('Ceuta','Granada'),('Leganés','Cultural Leonesa'),('Deportivo','Eibar'),
   ('Huesca','Mirandés'),('Almería','Córdoba'),('Las Palmas','Castellón'),
   ('Sporting','Valladolid'),('Andorra','Real Zaragoza'),('Racing','Burgos'),
   ('Málaga','Albacete'),('Cádiz','Real Sociedad B')],
  # J28
  [('Albacete','Almería'),('Real Zaragoza','Burgos'),('Granada','Málaga'),
   ('Valladolid','Huesca'),('Castellón','Racing'),('Real Sociedad B','Deportivo'),
   ('Mirandés','Ceuta'),('Cultural Leonesa','Las Palmas'),('Eibar','Cádiz'),
   ('Sporting','Leganés'),('Córdoba','Andorra')],
  # J29
  [('Cádiz','Real Zaragoza'),('Huesca','Albacete'),('Real Sociedad B','Castellón'),
   ('Burgos','Mirandés'),('Málaga','Valladolid'),('Las Palmas','Ceuta'),
   ('Andorra','Sporting'),('Leganés','Eibar'),('Racing','Córdoba'),
   ('Deportivo','Granada'),('Almería','Cultural Leonesa')],
  # J30
  [('Mirandés','Cádiz'),('Cultural Leonesa','Racing'),('Valladolid','Leganés'),
   ('Real Zaragoza','Almería'),('Ceuta','Deportivo'),('Córdoba','Real Sociedad B'),
   ('Granada','Andorra'),('Eibar','Burgos'),('Málaga','Huesca'),
   ('Sporting','Castellón'),('Albacete','Las Palmas')],
  # J31
  [('Huesca','Almería'),('Leganés','Ceuta'),('Andorra','Eibar'),
   ('Racing','Albacete'),('Cádiz','Málaga'),('Deportivo','Real Zaragoza'),
   ('Burgos','Córdoba'),('Mirandés','Valladolid'),('Real Sociedad B','Granada'),
   ('Las Palmas','Sporting'),('Castellón','Cultural Leonesa')],
  # J32
  [('Córdoba','Mirandés'),('Ceuta','Cádiz'),('Granada','Huesca'),
   ('Valladolid','Burgos'),('Málaga','Leganés'),('Albacete','Castellón'),
   ('Sporting','Deportivo'),('Eibar','Las Palmas'),('Cultural Leonesa','Andorra'),
   ('Real Zaragoza','Racing'),('Almería','Real Sociedad B')],
  # J33
  [('Mirandés','Albacete'),('Deportivo','Córdoba'),('Valladolid','Cádiz'),
   ('Andorra','Málaga'),('Burgos','Ceuta'),('Huesca','Cultural Leonesa'),
   ('Racing','Sporting'),('Las Palmas','Granada'),('Castellón','Almería'),
   ('Real Sociedad B','Eibar'),('Leganés','Real Zaragoza')],
  # J34
  [('Cádiz','Córdoba'),('Albacete','Burgos'),('Cultural Leonesa','Valladolid'),
   ('Deportivo','Málaga'),('Eibar','Ceuta'),('Andorra','Racing'),
   ('Almería','Leganés'),('Las Palmas','Huesca'),('Real Zaragoza','Mirandés'),
   ('Castellón','Granada'),('Sporting','Real Sociedad B')],
  # J35
  [('Ceuta','Real Sociedad B'),('Burgos','Sporting'),('Leganés','Albacete'),
   ('Málaga','Las Palmas'),('Córdoba','Real Zaragoza'),('Granada','Cultural Leonesa'),
   ('Huesca','Deportivo'),('Cádiz','Andorra'),('Mirandés','Castellón'),
   ('Racing','Almería'),('Valladolid','Eibar')],
  # J36
  [('Real Sociedad B','Racing'),('Las Palmas','Leganés'),('Real Zaragoza','Ceuta'),
   ('Castellón','Burgos'),('Cultural Leonesa','Córdoba'),('Andorra','Valladolid'),
   ('Sporting','Cádiz'),('Albacete','Granada'),('Eibar','Huesca'),
   ('Almería','Málaga'),('Deportivo','Mirandés')],
  # J37
  [('Albacete','Eibar'),('Valladolid','Real Sociedad B'),('Burgos','Deportivo'),
   ('Málaga','Castellón'),('Córdoba','Sporting'),('Granada','Almería'),
   ('Mirandés','Cultural Leonesa'),('Huesca','Real Zaragoza'),('Leganés','Andorra'),
   ('Ceuta','Racing'),('Cádiz','Las Palmas')],
  # J38
  [('Andorra','Albacete'),('Deportivo','Leganés'),('Real Zaragoza','Granada'),
   ('Cultural Leonesa','Cádiz'),('Castellón','Córdoba'),('Eibar','Málaga'),
   ('Racing','Huesca'),('Sporting','Ceuta'),('Real Sociedad B','Burgos'),
   ('Las Palmas','Valladolid'),('Almería','Mirandés')],
  # J39
  [('Cádiz','Deportivo'),('Ceuta','Castellón'),('Albacete','Cultural Leonesa'),
   ('Burgos','Almería'),('Valladolid','Real Zaragoza'),('Málaga','Sporting'),
   ('Andorra','Las Palmas'),('Leganés','Racing'),('Córdoba','Granada'),
   ('Mirandés','Eibar'),('Huesca','Real Sociedad B')],
  # J40
  [('Castellón','Cádiz'),('Córdoba','Albacete'),('Real Sociedad B','Mirandés'),
   ('Ceuta','Málaga'),('Cultural Leonesa','Eibar'),('Almería','Las Palmas'),
   ('Granada','Burgos'),('Racing','Valladolid'),('Deportivo','Andorra'),
   ('Real Zaragoza','Sporting'),('Leganés','Huesca')],
  # J41
  [('Albacete','Real Sociedad B'),('Cultural Leonesa','Burgos'),('Cádiz','Leganés'),
   ('Eibar','Córdoba'),('Andorra','Ceuta'),('Huesca','Castellón'),
   ('Las Palmas','Real Zaragoza'),('Mirandés','Granada'),('Málaga','Racing'),
   ('Valladolid','Deportivo'),('Sporting','Almería')],
  # J42
  [('Almería','Valladolid'),('Burgos','Andorra'),('Castellón','Eibar'),
   ('Ceuta','Albacete'),('Córdoba','Huesca'),('Deportivo','Las Palmas'),
   ('Granada','Sporting'),('Leganés','Mirandés'),('Racing','Cádiz'),
   ('Real Sociedad B','Cultural Leonesa'),('Real Zaragoza','Málaga')],
]

wb = openpyxl.load_workbook('LIGA HYPER 25_26__.xlsx', data_only=True)
ws = wb['Hoja1']

teams_raw = []
for row in ws.iter_rows(min_row=3, max_row=31, values_only=True):
    if row[0] is None:
        continue
    name = row[0]
    results = []
    for i in range(1, 43):
        r = row[i]
        if r in ('V', 'E', 'D'):
            results.append(r)
    if name and results:
        situacion = str(row[50]).strip() if row[50] is not None else ''
        quedan = int(row[51]) if row[51] is not None else 0
        teams_raw.append({'name': name, 'results': results,
                          'situacion': situacion, 'quedan': quedan})

n_rounds = max(len(t['results']) for t in teams_raw)
round_standings = []
for j in range(1, n_rounds + 1):
    snap = []
    for t in teams_raw:
        res = t['results'][:j]
        pts = res.count('V') * 3 + res.count('E')
        snap.append({
            'name': t['name'],
            'pts': pts,
            'wins': res.count('V'),
            'draws': res.count('E'),
            'losses': res.count('D'),
            'played': j
        })
    snap.sort(key=lambda x: (-x['pts'], -x['wins']))
    for pos, t in enumerate(snap, 1):
        t['pos'] = pos
    round_standings.append(snap)

positions_by_team = {t['name']: [] for t in teams_raw}
points_by_team = {t['name']: [] for t in teams_raw}
for snap in round_standings:
    for t in snap:
        positions_by_team[t['name']].append(t['pos'])
        points_by_team[t['name']].append(t['pts'])

final = round_standings[-1]

# Greedy opponent inference: match V→D pairs and E→E pairs per round
# ─── Construir opponents_by_team desde el calendario oficial Marca ──────────
teams_set = {t['name'] for t in teams_raw}
opponents_by_team = {t['name']: [None] * 42 for t in teams_raw}
for r_idx, round_fixtures in enumerate(FIXTURES):
    for home, away in round_fixtures:
        if home in teams_set:
            opponents_by_team[home][r_idx] = away
        if away in teams_set:
            opponents_by_team[away][r_idx] = home

data = {
    'teams': [t['name'] for t in teams_raw],
    'total_rounds': n_rounds,
    'total_season_rounds': 42,
    'results_by_team': {t['name']: t['results'] for t in teams_raw},
    'positions_by_team': positions_by_team,
    'points_by_team': points_by_team,
    'final_standings': final,
    'situacion_by_team': {t['name']: t['situacion'] for t in teams_raw},
    'quedan_by_team': {t['name']: t['quedan'] for t in teams_raw},
    'opponents_by_team': opponents_by_team,
}

with open('liga_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('JSON generado OK')
print('Jornadas:', n_rounds, '- Equipos:', len(teams_raw))
for t in final[:5]:
    print(t['pos'], t['name'], t['pts'], 'pts')

# ─── Guardar en BD ─────────────────────────────────────────────────────────
try:
    import db
    db.save_liga_data(data, '25_26')
except Exception as e:
    print(f'  ⚠ DB write failed: {e}')
