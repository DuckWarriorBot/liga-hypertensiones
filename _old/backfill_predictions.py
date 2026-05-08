"""
Repobla predictions_history.json con datos REALES de BeSoccer para todas las jornadas.
Usa el endpoint AJAX: /ajax/reloadTable?type=competition&itemId=2&competitionId=2&year=2026&group=1&round=N

Índice 0-based: jornada 1 → índice 0, jornada N → índice N-1
"""
import urllib.request, re, json, time, os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept': 'application/json',
    'Referer': 'https://es.besoccer.com/competicion/clasificacion/segunda/prediction',
}

BS_MAP = {
    'Racing': 'Racing', 'Almería': 'Almería', 'Almeria': 'Almería',
    'RC Deportivo': 'Deportivo', 'Deportivo': 'Deportivo',
    'UD Las Palmas': 'Las Palmas', 'Las Palmas': 'Las Palmas',
    'CD Castellón': 'Castellón', 'Castellón': 'Castellón', 'Castellon': 'Castellón',
    'Málaga': 'Málaga', 'Malaga': 'Málaga',
    'Burgos': 'Burgos', 'Burgos CF': 'Burgos',
    'Eibar': 'Eibar', 'SD Eibar': 'Eibar',
    'Córdoba CF': 'Córdoba', 'Córdoba': 'Córdoba', 'Cordoba': 'Córdoba',
    'Andorra': 'Andorra', 'FC Andorra': 'Andorra',
    'Ceuta': 'Ceuta', 'AD Ceuta FC': 'Ceuta', 'Ceuta FC': 'Ceuta',
    'Sporting': 'Sporting', 'Real Sporting': 'Sporting', 'Sporting Gijón': 'Sporting',
    'Albacete': 'Albacete', 'Albacete BP': 'Albacete',
    'Granada': 'Granada', 'Granada CF': 'Granada',
    'Valladolid': 'Valladolid', 'Real Valladolid': 'Valladolid',
    'Leganés': 'Leganés', 'CD Leganés': 'Leganés',
    'Real Sociedad B': 'Real Sociedad B', 'Real Sociedad': 'Real Sociedad B',
    'Cádiz': 'Cádiz', 'Cadiz': 'Cádiz', 'Cádiz CF': 'Cádiz',
    'Mirandés': 'Mirandés', 'CD Mirandés': 'Mirandés', 'Mirandes': 'Mirandés',
    'Huesca': 'Huesca', 'SD Huesca': 'Huesca',
    'Real Zaragoza': 'Real Zaragoza', 'Zaragoza': 'Real Zaragoza',
    'Cultural Leonesa': 'Cultural Leonesa', 'Cultural': 'Cultural Leonesa',
}

def fetch_round(round_num):
    params = f'type=competition&itemId=2&competitionId=2&year=2026&group=1&round={round_num}'
    url = f'https://es.besoccer.com/ajax/reloadTable?{params}'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode('utf-8', errors='ignore'))
    return data.get('table', '')

def parse_percent(cell_html):
    m = re.search(r'(\d+)\s*%', cell_html)
    return int(m.group(1)) if m else 0

def parse_predictions(table_html):
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
    results = {}
    for row in rows:
        name_m = re.search(r'class="team-name name-desktop">([^<]+)<', row)
        if not name_m:
            continue
        bs_name = name_m.group(1).strip()
        internal_name = BS_MAP.get(bs_name)
        if not internal_name:
            for k, v in BS_MAP.items():
                if k.lower() == bs_name.lower():
                    internal_name = v
                    break
        if not internal_name:
            internal_name = bs_name

        cells = re.findall(r'<td class="td-bg br-right"[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cells) < 4:
            cells = cells + [''] * (4 - len(cells))

        results[internal_name] = {
            'ascenso':      parse_percent(cells[0]),
            'playoff':      parse_percent(cells[1]),
            'permanencia':  parse_percent(cells[2]),
            'descenso':     parse_percent(cells[3]),
        }
    return results

if __name__ == '__main__':
    # Jornadas a backfill: 1 a 39 (la actual)
    START_ROUND = 1
    END_ROUND = 39

    hist = {}

    for rnd in range(START_ROUND, END_ROUND + 1):
        idx = str(rnd - 1)  # 0-based
        print(f'Descargando J{rnd} (índice {idx})...', end=' ')
        try:
            table_html = fetch_round(rnd)
            preds = parse_predictions(table_html)
            if len(preds) == 0:
                print(f'SIN DATOS')
                continue
            for team, pred in preds.items():
                if team not in hist:
                    hist[team] = {}
                hist[team][idx] = pred
            print(f'OK ({len(preds)} equipos)')
        except Exception as e:
            print(f'ERROR: {e}')
        time.sleep(0.4)  # respetar rate limit

    out_path = os.path.join(os.path.dirname(__file__), 'predictions_history.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)
    print(f'\nGuardado en {out_path}')
    print(f'Equipos: {len(hist)}, Jornadas por equipo (Racing): {sorted(hist.get("Racing", {}).keys(), key=int)}')
