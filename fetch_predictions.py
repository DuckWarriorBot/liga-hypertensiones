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


def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='ignore')


def parse_percent(cell_html):
    """Extrae el número entero de un <td> de predicción. Devuelve 0 si vacío."""
    m = re.search(r'(\d+)\s*%', cell_html)
    return int(m.group(1)) if m else 0


def scrape_predictions():
    html = fetch_html(URL)

    # Localizar el bloque de predicciones
    m = re.search(r'id="tab_predictions\d+"[^>]*>(.*)', html, re.DOTALL)
    if not m:
        raise ValueError("No se encontró el bloque tab_predictions en la página")
    pred_html = m.group(1)

    # Extraer filas <tr>
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', pred_html, re.DOTALL)

    results = {}
    for row in rows:
        # Nombre completo (name-desktop)
        name_m = re.search(r'class="team-name name-desktop">([^<]+)<', row)
        if not name_m:
            continue
        bs_name = name_m.group(1).strip()
        internal_name = BS_MAP.get(bs_name)
        if not internal_name:
            # Intentar limpiar acentos manualmente
            for k, v in BS_MAP.items():
                if k.lower() == bs_name.lower():
                    internal_name = v
                    break
        if not internal_name:
            print(f"  [WARN] Nombre no mapeado: '{bs_name}'")
            internal_name = bs_name

        # Las 4 celdas de predicción (td-bg br-right) en orden: Ascenso, Playoff, Permanencia, Descenso
        cells = re.findall(r'<td class="td-bg br-right"[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cells) < 4:
            # Algunas filas tienen menos; rellenar con 0
            cells = cells + [''] * (4 - len(cells))

        ascenso    = parse_percent(cells[0])
        playoff    = parse_percent(cells[1])
        permanencia = parse_percent(cells[2])
        descenso   = parse_percent(cells[3])

        results[internal_name] = {
            'ascenso':     ascenso,
            'playoff':     playoff,
            'permanencia': permanencia,
            'descenso':    descenso,
        }
        print(f"  {internal_name}: ascenso={ascenso} playoff={playoff} permanencia={permanencia} descenso={descenso}")

    return results


if __name__ == '__main__':
    print("Scrapeando predicciones de BeSoccer...")
    predictions = scrape_predictions()
    print(f"\nTotal equipos: {len(predictions)}")

    out_path = os.path.join(os.path.dirname(__file__), 'predictions.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
    print(f"Guardado en {out_path}")

    # Guardar snapshot en historial con la jornada actual
    ld_path = os.path.join(os.path.dirname(__file__), 'liga_data.json')
    if os.path.exists(ld_path):
        with open(ld_path, encoding='utf-8') as f:
            liga = json.load(f)
        round_idx = str(liga.get('total_rounds', 1) - 1)  # 0-indexed

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
        print(f"Historial actualizado: {updated} equipos → jornada {int(round_idx)+1} (índice {round_idx})")
    else:
        print("  ⚠ liga_data.json no encontrado — historial no actualizado")
