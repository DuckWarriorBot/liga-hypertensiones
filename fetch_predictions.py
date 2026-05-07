"""
Scrapea predicciones reales de BeSoccer para La Liga Hypermotion (Segunda División).
URL: https://es.besoccer.com/competicion/clasificacion/segunda/prediction

Guarda el resultado en predictions.json con el formato:
{
  "NombreEquipo": {"ascenso": X, "playoff": X, "permanencia": X, "descenso": X},
  ...
}
"""
import urllib.request
import re
import json
import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,*/*;q=0.9',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://es.besoccer.com/',
}

# Mapa de nombres BeSoccer → nombres internos del proyecto
BS_MAP = {
    'Racing':           'Racing',
    'Almería':          'Almería',
    'Almeria':          'Almería',
    'RC Deportivo':     'Deportivo',
    'Deportivo':        'Deportivo',
    'UD Las Palmas':    'Las Palmas',
    'Las Palmas':       'Las Palmas',
    'CD Castellón':     'Castellón',
    'Castellón':        'Castellón',
    'Castellon':        'Castellón',
    'Málaga':           'Málaga',
    'Malaga':           'Málaga',
    'Burgos':           'Burgos',
    'Burgos CF':        'Burgos',
    'Eibar':            'Eibar',
    'SD Eibar':         'Eibar',
    'Córdoba CF':       'Córdoba',
    'Córdoba':          'Córdoba',
    'Cordoba':          'Córdoba',
    'Andorra':          'Andorra',
    'FC Andorra':       'Andorra',
    'Ceuta':            'Ceuta',
    'AD Ceuta FC':      'Ceuta',
    'Ceuta FC':         'Ceuta',
    'Sporting':         'Sporting',
    'Real Sporting':    'Sporting',
    'Sporting Gijón':   'Sporting',
    'Albacete':         'Albacete',
    'Albacete BP':      'Albacete',
    'Granada':          'Granada',
    'Granada CF':       'Granada',
    'Valladolid':       'Valladolid',
    'Real Valladolid':  'Valladolid',
    'Leganés':          'Leganés',
    'CD Leganés':       'Leganés',
    'Real Sociedad B':  'Real Sociedad B',
    'Real Sociedad':    'Real Sociedad B',
    'Cádiz':            'Cádiz',
    'Cadiz':            'Cádiz',
    'Cádiz CF':         'Cádiz',
    'Mirandés':         'Mirandés',
    'CD Mirandés':      'Mirandés',
    'Mirandes':         'Mirandés',
    'Huesca':           'Huesca',
    'SD Huesca':        'Huesca',
    'Real Zaragoza':    'Real Zaragoza',
    'Zaragoza':         'Real Zaragoza',
    'Cultural Leonesa': 'Cultural Leonesa',
    'Cultural':         'Cultural Leonesa',
}

URL = 'https://es.besoccer.com/competicion/clasificacion/segunda/prediction'
AJAX_URL = 'https://es.besoccer.com/ajax/reloadTable'
# Parámetros fijos del data-* del HTML de BeSoccer (Segunda División 2025/26)
AJAX_PARAMS = 'type=competition&itemId=2&competitionId=2&year=2026&group=1'


def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def fetch_round_ajax(round_num):
    """Obtiene el HTML de la tabla de predicciones para una jornada específica via AJAX."""
    url = f'{AJAX_URL}?{AJAX_PARAMS}&round={round_num}'
    req = urllib.request.Request(url, headers={**HEADERS, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8', errors='ignore'))
    return data.get('table', '')


def parse_percent(cell_html):
    """Extrae el número entero de un <td> de predicción. Devuelve 0 si vacío."""
    m = re.search(r'(\d+)\s*%', cell_html)
    return int(m.group(1)) if m else 0


def get_current_round():
    """Lee data-round del HTML principal de BeSoccer (jornada activa/próxima)."""
    html = fetch_html(URL)
    # data-round en el div classificationTables
    m = re.search(r'id="classificationTables"[^>]*data-round="(\d+)"', html)
    if m:
        return int(m.group(1))
    # Fallback: último option del dropdown de jornadas
    rounds = re.findall(r'<option[^>]+value="(\d+)"', html)
    return int(rounds[-1]) if rounds else None


def parse_predictions_html(table_html):
    """Parsea la tabla HTML de predicciones y devuelve dict {equipo: {ascenso,playoff,permanencia,descenso}}."""
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
            print(f"  [WARN] Nombre no mapeado: '{bs_name}'")
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
        print(f"  {internal_name}: ascenso={results[internal_name]['ascenso']} playoff={results[internal_name]['playoff']} permanencia={results[internal_name]['permanencia']} descenso={results[internal_name]['descenso']}")
    return results


def scrape_predictions():
    # Obtener la jornada actual de BeSoccer
    besoccer_round = get_current_round()
    print(f"  BeSoccer jornada activa: {besoccer_round}")

    # Descargar predicciones vía AJAX para esa jornada
    table_html = fetch_round_ajax(besoccer_round)
    if not table_html:
        raise ValueError("No se obtuvo tabla del endpoint AJAX")

    results = parse_predictions_html(table_html)

    return results, besoccer_round


if __name__ == '__main__':
    print("Scrapeando predicciones de BeSoccer...")
    predictions, besoccer_round = scrape_predictions()
    print(f"\nTotal equipos: {len(predictions)}")

    out_path = os.path.join(os.path.dirname(__file__), 'predictions.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
    print(f"Guardado en {out_path}")

    # Guardar snapshot en historial usando la jornada que BeSoccer tiene seleccionada
    # Índice 0-based: jornada 1 → índice 0, jornada 38 → índice 37
    if besoccer_round is not None:
        round_idx = str(besoccer_round - 1)

        hist_path = os.path.join(os.path.dirname(__file__), 'predictions_history.json')
        if os.path.exists(hist_path):
            with open(hist_path, encoding='utf-8') as f:
                hist = json.load(f)
        else:
            hist = {}

        updated = 0
        for team, pred in predictions.items():
            if team not in hist:
                hist[team] = {}
            hist[team][round_idx] = pred
            updated += 1

        with open(hist_path, 'w', encoding='utf-8') as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
        print(f"Historial actualizado: {updated} equipos → jornada {besoccer_round} (índice {round_idx})")
    else:
        print("  ⚠ No se pudo determinar la jornada de BeSoccer — historial no actualizado")
