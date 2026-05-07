"""
fetch_team_assets.py
====================
Busca escudos (BeSoccer CDN) y colores para equipos que NO estén en build.py.

Guarda resultados en team_assets.json.
build.py los fusiona sobre TEAM_BADGES / TEAM_COLORS / TEAM_KIT_FULL.

Uso:
    python fetch_team_assets.py
    python fetch_team_assets.py --force   # re-buscar aunque ya estén en assets
"""
import asyncio, json, os, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

ASSETS_FILE = Path(__file__).parent / 'team_assets.json'
BUILD_FILE  = Path(__file__).parent / 'build.py'

# Alias de búsqueda para nombres que BeSoccer no encontraría directamente
SEARCH_ALIAS = {
    'Racing Club Ferrol': 'Racing Ferrol',
    'UD Logroñés':        'Logroñes',
    'Real Sociedad B':    'Real Sociedad B',
}

# Colores de fallback cuando no se puede extraer automáticamente
FALLBACK_COLORS = {
    # (clave: color primario del equipo)
    'Levante':            '#0033A0',
    'Cartagena':          '#CC0000',
    'Elche':              '#00843D',
    'Eldense':            '#CC0000',
    'Espanyol':           '#003DA5',
    'Tenerife':           '#003087',
    'Girona':             '#9B1C31',
    'Mallorca':           '#CC0000',
    'Real Oviedo':        '#003087',
    'Alavés':             '#003087',
    'Rayo Vallecano':     '#CC0000',
    'Lugo':               '#CC0000',
    'Ponferradina':       '#CC0000',
    'Alcorcón':           '#FF6600',
    'Amorebieta':         '#CC0000',
    'Ibiza':              '#003087',
    'Fuenlabrada':        '#009B3A',
    'Numancia':           '#CC0000',
    'Racing Club Ferrol': '#CC0000',
    'Sabadell':           '#003087',
    'UD Logroñés':        '#CC0000',
    'Villarreal B':       '#F5C500',
    'Extremadura':        '#CC0000',
}


def load_existing():
    if ASSETS_FILE.exists():
        return json.loads(ASSETS_FILE.read_text('utf-8'))
    return {'badges': {}, 'colors': {}}


def get_known_from_build():
    """Lee los equipos que ya tienen badge/color hardcodeado en build.py."""
    known = set()
    if not BUILD_FILE.exists():
        return known
    text = BUILD_FILE.read_text('utf-8')
    for m in re.finditer(r"'([^']+)':\s*'https://cdn\.resfu", text):
        known.add(m.group(1))
    for m in re.finditer(r"'([^']+)':\s*'#[0-9A-Fa-f]{6}'", text):
        known.add(m.group(1))
    return known


def get_history_teams():
    hist_file = Path(__file__).parent / 'history_data.json'
    current_file = Path(__file__).parent / 'liga_data.json'
    teams = set()
    if hist_file.exists():
        d = json.loads(hist_file.read_text('utf-8'))
        for s in d.get('seasons', {}).values():
            teams.update(s.get('teams', []))
    if current_file.exists():
        d = json.loads(current_file.read_text('utf-8'))
        teams.update(d.get('teams', []))
    return teams


async def fetch_besoccer_badge(page, team_name):
    """Busca en BeSoccer el escudo del equipo. Devuelve (badge_url, color) o (None, None)."""
    query = SEARCH_ALIAS.get(team_name, team_name)
    # Ir directamente a la búsqueda de equipos en BeSoccer
    url = f'https://www.besoccer.com/search?q={query}&c=team&l=es'
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
        await page.wait_for_timeout(2000)

        # Buscar links a páginas de equipo
        links = await page.query_selector_all('.team-list .team-name a, .search-result a[href*="/equipo/"], a.team-link')
        if not links:
            links = await page.query_selector_all('a[href*="/equipo/"]')

        for lnk in links[:4]:
            href = await lnk.get_attribute('href')
            if not href:
                continue
            full_url = f'https://www.besoccer.com{href}' if href.startswith('/') else href
            if '/equipo/' not in full_url:
                continue
            try:
                await page.goto(full_url, wait_until='domcontentloaded', timeout=15000)
                await page.wait_for_timeout(1000)
                # Buscar imagen del escudo en CDN resfu
                img = await page.query_selector('img[src*="cdn.resfu.com/img_data/equipos"]')
                if img:
                    src = await img.get_attribute('src')
                    if src and re.search(r'/equipos/\d+\.png', src):
                        print(f'  ✓ BeSoccer: {team_name} → {src}')
                        return src, None
            except Exception:
                continue
    except Exception as e:
        print(f'  ✗ BeSoccer error para {team_name}: {type(e).__name__}')
    return None, None


async def fetch_flashscore_badge(page, team_name):
    """Alternativa: buscar en Flashscore la URL de badge del equipo."""
    query = SEARCH_ALIAS.get(team_name, team_name)
    url = f'https://www.flashscore.es/search/?q={query}'
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(1500)
        # Flashscore usa imágenes tipo /res/image/data/{hash}.png  o img.flashscore
        imgs = await page.query_selector_all('img[src*="flashscore"], img[src*="fscdn"]')
        for img in imgs[:5]:
            src = await img.get_attribute('src')
            if src:
                print(f'  ~ Flashscore badge: {src[:60]}')
                return src, None
    except Exception as e:
        print(f'  ✗ Flashscore error para {team_name}: {type(e).__name__}')
    return None, None


async def main():
    force = '--force' in sys.argv
    existing = load_existing()
    badges = existing.get('badges', {})
    colors = existing.get('colors', {})

    known_in_build = get_known_from_build()
    all_teams = get_history_teams()

    if not all_teams:
        print('[team_assets] No se encontraron equipos en history_data.json / liga_data.json')
        return

    # Equipos que necesitamos resolver (no están en build.py ni en assets)
    missing = sorted(t for t in all_teams
                     if t not in known_in_build and (force or t not in badges))

    if not missing:
        print('[team_assets] Todos los equipos ya tienen assets.')
        return

    print(f'[team_assets] Buscando assets para {len(missing)} equipos:')
    for t in missing:
        print(f'  - {t}')

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0',
            locale='es-ES',
        )
        page = await ctx.new_page()

        for team in missing:
            print(f'\n── {team}')

            # 1. Intentar BeSoccer
            badge, color = await fetch_besoccer_badge(page, team)

            # 2. Si no hay badge, intentar Flashscore
            if not badge:
                badge, color = await fetch_flashscore_badge(page, team)

            if badge:
                badges[team] = badge
            else:
                print(f'  ⚠ Sin badge para {team}')

            # Color: fallback predefinido
            if team not in colors:
                c = FALLBACK_COLORS.get(team, '#6b7280')
                colors[team] = c
                print(f'  color: {c}')

            # Guardar progresivamente tras cada equipo
            ASSETS_FILE.write_text(
                json.dumps({'badges': badges, 'colors': colors}, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
            await asyncio.sleep(0.8)

        await browser.close()

    print(f'\n[team_assets] Guardado → {ASSETS_FILE}')
    print(f'  Escudos encontrados: {len(badges)} | Colores: {len(colors)}')
    print()
    print('Equipos SIN escudo:')
    for t in missing:
        if t not in badges:
            print(f'  - {t}')


if __name__ == '__main__':
    asyncio.run(main())


Fuentes utilizadas:
  1. BeSoccer CDN (cdn.resfu.com) — escudo via búsqueda en besoccer.com
  2. Wikipedia ES — colores primarios del equipo (infobox)

Guarda los resultados en team_assets.json.
build.py ya lo lee y lo fusiona sobre TEAM_BADGES / TEAM_COLORS.

Uso:
    python fetch_team_assets.py
"""
import asyncio, json, os, re, time
from pathlib import Path
from playwright.async_api import async_playwright

# ── Equipos ya mapeados en build.py ──────────────────────────────────────────
KNOWN_TEAMS = {
    'Racing', 'Almería', 'Deportivo', 'Las Palmas', 'Castellón', 'Málaga',
    'Burgos', 'Eibar', 'Córdoba', 'Andorra', 'Ceuta', 'Sporting', 'Albacete',
    'Granada', 'Valladolid', 'Leganés', 'Real Sociedad B', 'Cádiz', 'Mirandés',
    'Huesca', 'Real Zaragoza', 'Cultural Leonesa',
}

# ── Colores de referencia cuando no se puede leer automáticamente ────────────
FALLBACK_COLORS = {
    'Levante':            '#0033A0',  # azul marino Levante UD
    'Cartagena':          '#CC0000',  # rojo FC Cartagena
    'Elche':              '#00843D',  # verde Elche CF
    'Eldense':            '#CC0000',  # rojo UD Eldense
    'Espanyol':           '#003DA5',  # azul Espanyol
    'Tenerife':           '#003087',  # azul CD Tenerife
    'Girona':             '#CC0000',  # rojo Girona FC
    'Mallorca':           '#CC0000',  # rojo RCD Mallorca
    'Real Oviedo':        '#003087',  # azul Real Oviedo
    'Alavés':             '#003087',  # azul Deportivo Alavés
    'Rayo Vallecano':     '#CC0000',  # rojo Rayo Vallecano
    'Lugo':               '#CC0000',  # rojo CD Lugo
    'Ponferradina':       '#CC0000',  # rojo SD Ponferradina
    'Alcorcón':           '#FF6600',  # naranja AD Alcorcón
    'Amorebieta':         '#CC0000',  # rojo SD Amorebieta
    'Ibiza':              '#003087',  # azul UD Ibiza
    'Fuenlabrada':        '#009B3A',  # verde CF Fuenlabrada
    'Numancia':           '#CC0000',  # rojo CD Numancia
    'Racing Club Ferrol': '#CC0000',  # rojo Racing Club de Ferrol
    'Sabadell':           '#003087',  # azul CE Sabadell
    'UD Logroñés':        '#CC0000',  # rojo UD Logroñés
    'Villarreal B':       '#F5C500',  # amarillo Villarreal CF B
    'Extremadura':        '#CC0000',  # rojo Extremadura UD
}

# ── Alias para búsqueda en BeSoccer ─────────────────────────────────────────
SEARCH_ALIAS = {
    'Racing Club Ferrol': 'Racing Ferrol',
    'Real Sociedad B':    'Real Sociedad B',
    'Villarreal B':       'Villarreal B',
    'UD Logroñés':        'Logroñés',
}

ASSETS_FILE = Path(__file__).parent / 'team_assets.json'


def load_existing():
    if ASSETS_FILE.exists():
        return json.loads(ASSETS_FILE.read_text('utf-8'))
    return {'badges': {}, 'colors': {}}


def load_history_teams():
    hist_file = Path(__file__).parent / 'history_data.json'
    if not hist_file.exists():
        return set()
    d = json.loads(hist_file.read_text('utf-8'))
    teams = set()
    for s in d.get('seasons', {}).values():
        teams.update(s.get('teams', []))
    return teams


async def find_besoccer_badge(page, team_name):
    """Busca en BeSoccer el escudo de un equipo. Devuelve URL del badge o None."""
    query = SEARCH_ALIAS.get(team_name, team_name)
    url = f'https://www.besoccer.com/search?q={query}&c=team&l=es'
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(1500)
        # Buscar primer resultado de equipo
        # El DOM de BeSoccer tiene: .team-search .team-name + img con src de cdn.resfu
        links = await page.query_selector_all('a[href*="/team/"]')
        for lnk in links[:5]:
            href = await lnk.get_attribute('href')
            if not href:
                continue
            # Navegar al equipo para obtener su ID de escudo
            full_url = f'https://www.besoccer.com{href}' if href.startswith('/') else href
            try:
                await page.goto(full_url, wait_until='domcontentloaded', timeout=15000)
                await page.wait_for_timeout(1000)
                # Buscar img con src de cdn.resfu
                img = await page.query_selector('img[src*="cdn.resfu.com/img_data/equipos"]')
                if img:
                    src = await img.get_attribute('src')
                    if src and 'equipos' in src:
                        print(f'  ✓ BeSoccer badge para {team_name}: {src}')
                        return src
            except Exception:
                continue
    except Exception as e:
        print(f'  ✗ BeSoccer error para {team_name}: {e}')
    return None


async def find_wikipedia_badge(page, team_name):
    """Busca en Wikipedia ES el escudo del equipo via infobox."""
    query = SEARCH_ALIAS.get(team_name, team_name)
    url = f'https://es.wikipedia.org/w/index.php?search={query}&ns0=1'
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(1000)
        # En resultados de búsqueda, ir al primero
        first = await page.query_selector('.mw-search-result-heading a')
        if first:
            await first.click()
            await page.wait_for_load_state('domcontentloaded')
            await page.wait_for_timeout(800)
        # Buscar img del escudo en la infobox
        # Wikipedia usa imgs con clase ".infobox img" o dentro de ".infobox-image"
        for sel in ['.infobox-image img', '.infobox img:first-child', 'td.infobox-label ~ td img']:
            img = await page.query_selector(sel)
            if img:
                src = await img.get_attribute('src')
                if src and src.startswith('//'):
                    src = 'https:' + src
                if src and ('escudo' in src.lower() or 'logo' in src.lower() or 
                           'badge' in src.lower() or 'crest' in src.lower() or
                           'shield' in src.lower() or '_logo' in src.lower() or
                           'sports' in src.lower()):
                    print(f'  ✓ Wikipedia badge para {team_name}: {src[:60]}')
                    return src
    except Exception as e:
        print(f'  ✗ Wikipedia error para {team_name}: {e}')
    return None


async def main():
    existing = load_existing()
    badges = existing.get('badges', {})
    colors = existing.get('colors', {})

    history_teams = load_history_teams()
    missing = sorted(t for t in history_teams if t not in KNOWN_TEAMS and t not in badges)

    if not missing:
        print('[team_assets] Todos los equipos ya están mapeados.')
        return

    print(f'[team_assets] Buscando assets para {len(missing)} equipos: {missing}')

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx     = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0',
            locale='es-ES',
        )
        page = await ctx.new_page()

        for team in missing:
            print(f'\n── {team}')

            # 1. Intentar BeSoccer
            badge = await find_besoccer_badge(page, team)

            # 2. Si no, intentar Wikipedia
            if not badge:
                badge = await find_wikipedia_badge(page, team)

            if badge:
                badges[team] = badge
            else:
                print(f'  ⚠ Sin escudo para {team}')

            # Colores: fallback hardcodeado
            if team not in colors:
                c = FALLBACK_COLORS.get(team, '#6b7280')
                colors[team] = c
                print(f'  color: {c}')

            # Guardar progresivamente
            ASSETS_FILE.write_text(
                json.dumps({'badges': badges, 'colors': colors}, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            await asyncio.sleep(0.5)

        await browser.close()

    print(f'\n[team_assets] Guardado en {ASSETS_FILE}')
    print(f'  Escudos: {len(badges)} | Colores: {len(colors)}')


if __name__ == '__main__':
    asyncio.run(main())
