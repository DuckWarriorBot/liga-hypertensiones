#!/usr/bin/env python3
"""
fetch_playoff.py — Actualiza los resultados del playoff de ascenso desde Flashscore.

Busca en la página de LaLiga Hypermotion los partidos etiquetados como
"Semifinales" y "Final" (aparecen tras las 42 jornadas regulares) y rellena
los campos `score`, `played`, `date` y `winner`/`agg` en liga_data['playoff'].

También calcula automáticamente:
  - El ganador de cada semifinal por marcador agregado
  - Los equipos de la final cuando ambas semifinales están completas

Requiere: pip install playwright && python -m playwright install chromium
"""

import json, re, unicodedata
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

if __import__('sys').stdout.__class__.__name__ != 'NoneType':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(__file__).parent
LIGA_F   = BASE_DIR / 'liga_data.json'

RESULTS_URL  = 'https://www.flashscore.es/futbol/espana/laliga-hypermotion/resultados/'

# Mismo mapeo que fetch_flashscore.py
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
    'Granada CF': 'Granada', 'Granada': 'Granada',
    'SD Huesca': 'Huesca', 'Huesca': 'Huesca',
    'RC Deportivo': 'Deportivo', 'RC Deportivo de La Coruña': 'Deportivo',
    'Deportivo de La Coruña': 'Deportivo', 'Deportivo': 'Deportivo',
    'UD Las Palmas': 'Las Palmas', 'Las Palmas': 'Las Palmas',
    'CD Leganés': 'Leganés', 'Leganés': 'Leganés', 'Leganes': 'Leganés',
    'CD Mirandés': 'Mirandés', 'Mirandés': 'Mirandés', 'Mirandes': 'Mirandés',
    'Málaga CF': 'Málaga', 'Málaga': 'Málaga', 'Malaga': 'Málaga',
    'Racing de Santander': 'Racing', 'Racing Santander': 'Racing',
    'R. Racing Club': 'Racing', 'R.Racing Club': 'Racing', 'Racing': 'Racing',
    'Real Sociedad B': 'Real Sociedad B', 'Soc. B': 'Real Sociedad B',
    'Real Zaragoza': 'Real Zaragoza', 'Zaragoza': 'Real Zaragoza',
    'Real Sporting': 'Sporting', 'Sporting de Gijón': 'Sporting',
    'Sp. Gijón': 'Sporting', 'Sporting': 'Sporting',
    'Real Valladolid CF': 'Valladolid', 'Real Valladolid': 'Valladolid',
    'Valladolid': 'Valladolid',
}


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
    return None


def parse_fs_date(raw):
    m = re.search(r'(\d{2})\.(\d{2})\.', raw)
    return f"{m.group(1)}/{m.group(2)}" if m else None


def _make_page(pw):
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
    return browser, ctx.new_page()


def dismiss_cookies(page):
    for sel in [
        'button#onetrust-accept-btn-handler',
        '#didomi-notice-agree-button',
        'button.fc-cta-consent',
        'button[aria-label*="Accept"]',
        'button[aria-label*="Aceptar"]',
    ]:
        try:
            page.click(sel, timeout=3000)
            page.wait_for_timeout(400)
            return
        except (PWTimeout, Exception):
            pass


def scrape_playoff_matches(page):
    """
    Lee la página de resultados de Flashscore y extrae los partidos etiquetados
    como 'Semifinales' o 'Final' (rondas > 42 en el DOM).
    Devuelve lista de dicts: {home, away, score, date, round_label}
    """
    page.goto(RESULTS_URL, wait_until='domcontentloaded', timeout=25000)
    page.wait_for_timeout(3000)
    dismiss_cookies(page)
    page.wait_for_timeout(1000)

    # Expandir todos los resultados disponibles pulsando "Mostrar más partidos"
    for _ in range(3):
        try:
            page.click('a.event__more, button.event__more', timeout=2000)
            page.wait_for_timeout(1000)
        except (PWTimeout, Exception):
            break

    raw = page.evaluate(r"""
    () => {
      const rows = [];
      // Flashscore usa event__round--static para las rondas de playoff
      const sel = '.event__round--static, .event__round--round, .event__match';
      document.querySelectorAll(sel).forEach(el => {
        const cls = el.className || '';
        if (cls.includes('event__round--static') || cls.includes('event__round--round')) {
          const txt = el.innerText ? el.innerText.trim() : '';
          if (txt) rows.push({ type: 'round', text: txt });
        } else if (cls.includes('event__match')) {
          const home = el.querySelector('.event__homeParticipant, .event__participant--home');
          const away = el.querySelector('.event__awayParticipant, .event__participant--away');
          const parts = el.querySelectorAll('.event__participant');
          const homeName = home ? home.innerText.trim() : (parts[0] ? parts[0].innerText.trim() : '');
          const awayName = away ? away.innerText.trim() : (parts[1] ? parts[1].innerText.trim() : '');
          const sh = el.querySelector('.event__score--home');
          const sa = el.querySelector('.event__score--away');
          const tm = el.querySelector('.event__time');
          rows.push({
            type: 'match',
            home: homeName, away: awayName,
            scoreH: sh ? sh.innerText.trim() : '',
            scoreA: sa ? sa.innerText.trim() : '',
            timeRaw: tm ? tm.innerText.trim() : '',
          });
        }
      });
      return rows;
    }
    """)

    playoff_matches = []
    current_label = None
    in_playoff = False

    for row in raw:
        if row['type'] == 'round':
            txt = row['text'].strip()
            txt_low = txt.lower()
            # 'FINAL' y 'SEMIFINALES' indican rondas de playoff
            if txt_low in ('final', 'semifinales', 'semifinals', 'semifinal'):
                in_playoff = True
                current_label = txt
            elif re.match(r'jornada\s+\d+|round\s+\d+', txt_low):
                # Vuelta a jornada regular — salir del bloque playoff
                in_playoff = False
                current_label = None
            # Cualquier otro round label desconocido dentro del playoff: mantener estado
            continue

        if not in_playoff:
            continue

        home_int = map_team(row['home'])
        away_int = map_team(row['away'])
        if not home_int or not away_int:
            continue

        score_h = score_a = None
        if row['scoreH'] and row['scoreA']:
            try:
                score_h = int(row['scoreH'])
                score_a = int(row['scoreA'])
            except ValueError:
                pass

        playoff_matches.append({
            'home': home_int,
            'away': away_int,
            'score': f'{score_h}-{score_a}' if score_h is not None else None,
            'played': score_h is not None,
            'date': parse_fs_date(row['timeRaw']),
            'round_label': current_label,
        })

    return playoff_matches


def _match_key(a, b):
    """Clave normalizada para un par de equipos (sin importar orden)."""
    return tuple(sorted([a, b]))


def update_playoff_data(liga, matches):
    """
    Rellena liga['playoff'] con los resultados obtenidos de Flashscore.
    Preserva los emparejamientos ya calculados en fetch_all.py.
    """
    playoff = liga.get('playoff')
    if not playoff:
        print('  ⚠  liga_data.json no tiene campo "playoff". Ejecuta fetch_all.py primero.')
        return False

    if not matches:
        print('  ℹ  Sin partidos de playoff encontrados en Flashscore todavía.')
        return False

    # Indexar partidos scrapeados por par de equipos
    scraped_by_key = {}
    for m in matches:
        k = _match_key(m['home'], m['away'])
        scraped_by_key.setdefault(k, []).append(m)

    changed = False

    # ── Actualizar semifinales ─────────────────────────────────────────────────
    for sf in playoff['semis']:
        for match in sf['matches']:
            if match['played']:
                continue  # ya tenemos el resultado, no sobreescribir
            k = _match_key(match['home'], match['away'])
            candidates = scraped_by_key.get(k, [])
            if not candidates:
                continue
            # Tomar el primero cuyo home coincida exactamente
            hit = next((c for c in candidates if c['home'] == match['home']), candidates[0])
            if hit['played']:
                match['score']  = hit['score']
                match['played'] = True
                match['date']   = hit['date']
                print(f"  ✓  SF {sf['id']} leg {match['leg']}: {match['home']} {match['score']} {match['away']}")
                changed = True

        # Calcular agregado y ganador de cada semifinal
        played_legs = [m for m in sf['matches'] if m['played']]
        if len(played_legs) == 2:
            agg_high = agg_low = 0
            for m in played_legs:
                hg, ag = map(int, m['score'].split('-'))
                if m['home'] == sf['team_high']:
                    agg_high += hg; agg_low += ag
                else:
                    agg_high += ag; agg_low += hg
            sf['agg'] = f'{agg_high}-{agg_low}'
            if agg_high > agg_low:
                sf['winner'] = sf['team_high']
            elif agg_low > agg_high:
                sf['winner'] = sf['team_low']
            else:
                # Empate en el agregado: clasifica el equipo de mayor posición (team_high)
                sf['winner'] = sf['team_high']
            print(f"  ✓  {sf['id']} ganador: {sf['winner']} (agg {sf['agg']})")
            changed = True

    # ── Rellenar final cuando ambas semifinales tienen ganador ─────────────────
    final = playoff['final']
    winners = [sf.get('winner') for sf in playoff['semis']]
    if all(winners) and not final['matches'][0]['home']:
        # SF1 ganador juega de local en la ida de la final
        final['matches'][0]['home']  = winners[0]
        final['matches'][0]['away']  = winners[1]
        final['matches'][1]['home']  = winners[1]
        final['matches'][1]['away']  = winners[0]
        print(f'  ✓  Final: {winners[0]} vs {winners[1]}')
        changed = True

    # ── Actualizar partidos de la final ────────────────────────────────────────
    for match in final['matches']:
        if not match['home'] or match['played']:
            continue
        k = _match_key(match['home'], match['away'])
        candidates = scraped_by_key.get(k, [])
        if not candidates:
            continue
        hit = next((c for c in candidates if c['home'] == match['home']), candidates[0])
        if hit['played']:
            match['score']  = hit['score']
            match['played'] = True
            match['date']   = hit['date']
            print(f"  ✓  Final leg {match['leg']}: {match['home']} {match['score']} {match['away']}")
            changed = True

    # Calcular ganador de la final
    played_final = [m for m in final['matches'] if m['played']]
    if len(played_final) == 2 and not final['winner']:
        t1 = final['matches'][0]['home']
        t2 = final['matches'][0]['away']
        agg1 = agg2 = 0
        for m in played_final:
            hg, ag = map(int, m['score'].split('-'))
            if m['home'] == t1:
                agg1 += hg; agg2 += ag
            else:
                agg1 += ag; agg2 += hg
        final['agg'] = f'{agg1}-{agg2}'
        final['winner'] = t1 if agg1 >= agg2 else t2  # local gana en empate
        print(f'  ✓  Campeón playoff: {final["winner"]} (agg {final["agg"]})')
        changed = True

    return changed


def main():
    print('=== fetch_playoff.py ===')

    if not LIGA_F.exists():
        print('✗  liga_data.json no encontrado. Ejecuta fetch_all.py primero.')
        return

    with open(LIGA_F, encoding='utf-8') as f:
        liga = json.load(f)

    if not liga.get('playoff'):
        print('ℹ  No hay campo "playoff" en liga_data.json — sin playoff configurado aún.')
        return

    print(f'  Buscando resultados de playoff en Flashscore...')
    try:
        with sync_playwright() as pw:
            browser, page = _make_page(pw)
            try:
                matches = scrape_playoff_matches(page)
            finally:
                browser.close()
    except Exception as e:
        print(f'✗  Error Playwright: {e}')
        return

    print(f'  {len(matches)} partidos de playoff encontrados en Flashscore')

    changed = update_playoff_data(liga, matches)

    if changed:
        with open(LIGA_F, 'w', encoding='utf-8') as f:
            json.dump(liga, f, ensure_ascii=False, indent=2)
        print('✓  liga_data.json actualizado con datos de playoff')
    else:
        print('ℹ  Sin cambios nuevos en el playoff')


if __name__ == '__main__':
    main()
