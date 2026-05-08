#!/usr/bin/env python3
"""
fetch_as.py — Scraper de estadísticas de partidos de LaLiga Hypermotion desde AS.com

Datos capturados por partido (equipo local / visitante):
  - Posesión %
  - Tiros: dentro del marco, fuera del marco, bloqueados, recibidos
  - Faltas cometidas y recibidas
  - Tarjetas amarillas y rojas
  - Pérdidas de posesión
  - Recuperaciones de posesión
  - Fueras de juego

Uso:
  python fetch_as.py                  # temporada actual 2025_2026
  python fetch_as.py 2024_2025        # temporada histórica
  python fetch_as.py 2025_2026 --from-jornada 10   # retomar desde jornada 10
"""

import json
import time
import sys
import re
import io
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# Forzar UTF-8 en stdout para evitar UnicodeEncodeError en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Mapeo nombres AS.com → nombres internos del sistema ──────────────────────
AS_NAME_MAP = {
    'A. D. Ceuta':   'Ceuta',
    'Burgos CF':     'Burgos',
    'Cultural':      'Cultural Leonesa',
    'R. Sociedad B': 'Real Sociedad B',
    'Real Valladolid': 'Valladolid',
}

def norm_name(n):
    return AS_NAME_MAP.get(n, n)

# ── Configuración ─────────────────────────────────────────────────────────────
SEASON          = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else "2025_2026"
BASE_URL        = "https://as.com/resultados/futbol/segunda"
OUTPUT_FILE     = Path("as_stats.json")
TOTAL_JORNADAS  = 42
DELAY_JORNADA   = 1.5    # segundos entre jornadas
DELAY_MATCH     = 2.0    # segundos entre partidos
HEADLESS        = True

# Retomar desde jornada específica
from_jornada = 1
for i, arg in enumerate(sys.argv):
    if arg == '--from-jornada' and i + 1 < len(sys.argv):
        from_jornada = int(sys.argv[i + 1])

# ── Extractor de jornada ──────────────────────────────────────────────────────

JS_GET_MATCHES = """
() => Array.from(document.querySelectorAll('li.a_sc_l_it[data-id]')).map(li => ({
    match_id:  li.getAttribute('data-id'),
    home:      li.getAttribute('data-team-home-name'),
    away:      li.getAttribute('data-team-away-name'),
    home_id:   li.getAttribute('data-team-home-id'),
    away_id:   li.getAttribute('data-team-away-id'),
}))
"""

# ── Extractor de estadísticas ─────────────────────────────────────────────────

JS_GET_STATS = r"""
() => {
    const data = {};

    // Posesión (barra dual con %)
    const bar = document.querySelector('.stat-bar-xl');
    if (bar) {
        const m = bar.textContent.match(/([\d.]+)%\s*([\d.]+)%/);
        if (m) {
            data.possession_home = parseFloat(m[1]);
            data.possession_away = parseFloat(m[2]);
        }
    }

    // Mapa de etiquetas → claves del JSON
    const STAT_MAP = {
        'Disparos recibidos':             ['shots_received_home',     'shots_received_away'],
        'Tarjetas amarillas':             ['yellow_cards_home',       'yellow_cards_away'],
        'Tarjetas rojas':                 ['red_cards_home',          'red_cards_away'],
        'Faltas recibidas':               ['fouls_received_home',     'fouls_received_away'],
        'Faltas cometidas':               ['fouls_committed_home',    'fouls_committed_away'],
        'Perdidas de posesión':           ['poss_losses_home',        'poss_losses_away'],
        'Recuperaciones de posesión':     ['poss_recoveries_home',    'poss_recoveries_away'],
        'Fueras de juego':                ['offsides_home',           'offsides_away'],
        'Disparos efectuados bloqueados': ['shots_blocked_home',      'shots_blocked_away'],
    };

    document.querySelectorAll('.stat-wr').forEach(row => {
        const label = row.querySelector('.stat-tl')?.textContent?.trim();
        if (!label || !STAT_MAP[label]) return;
        const homeVal = row.querySelector('.stat-i:not(.stat-i-aux)')?.textContent?.trim();
        const awayVal = row.querySelector('.stat-i-aux')?.textContent?.trim();
        const [hk, ak] = STAT_MAP[label];
        if (homeVal !== undefined && homeVal !== '') data[hk] = parseInt(homeVal, 10);
        if (awayVal !== undefined && awayVal !== '') data[ak] = parseInt(awayVal, 10);
    });

    // Tiros dentro/fuera del marco (.stat-shots con .stat-i-wr por fila)
    const shotsBlock = document.querySelector('.stat-shots');
    if (shotsBlock) {
        const wrRows = shotsBlock.querySelectorAll('.stat-i-wr');
        // Cada .stat-i-wr agrupa [fuera, dentro] para home (fila0) y away (fila1)
        // Los valores suelen repetirse en el DOM — usamos Set para deduplicar
        const parseRow = (wr) => {
            const unique = [...new Set(
                Array.from(wr.querySelectorAll('.stat-i, .stat-i-aux'))
                    .map(e => e.textContent.trim())
                    .filter(t => /^\d+$/.test(t))
            )].map(Number);
            return unique;
        };
        if (wrRows[0]) {
            const [outside, inside] = parseRow(wrRows[0]);
            if (outside !== undefined) data.shots_outside_home = outside;
            if (inside  !== undefined) data.shots_inside_home  = inside;
        }
        if (wrRows[1]) {
            const [outside, inside] = parseRow(wrRows[1]);
            if (outside !== undefined) data.shots_outside_away = outside;
            if (inside  !== undefined) data.shots_inside_away  = inside;
        }
    }

    // Estado del partido (Finalizado / En juego / etc.)
    const status = document.querySelector('.end-ev-status')?.textContent?.trim() || null;
    data.status = status;

    return Object.keys(data).length > 1 ? data : null;
}
"""


def get_jornada_matches(page, jornada_n):
    url = f"{BASE_URL}/{SEASON}/jornada/regular_a_{jornada_n}/"
    try:
        page.goto(url, timeout=30_000, wait_until="domcontentloaded")
        time.sleep(DELAY_JORNADA)
    except PWTimeout:
        print(f"  [!] Timeout cargando jornada {jornada_n}")
        return []
    try:
        return page.evaluate(JS_GET_MATCHES)
    except Exception as e:
        print(f"  [!] Error JS jornada {jornada_n}: {e}")
        return []


def get_match_stats(page, jornada_n, match_id):
    url = f"{BASE_URL}/{SEASON}/directo/regular_a_{jornada_n}_{match_id}/estadisticas/"
    try:
        page.goto(url, timeout=30_000, wait_until="domcontentloaded")
        time.sleep(DELAY_MATCH)
    except PWTimeout:
        print(f"  [!] Timeout stats {match_id[:8]}")
        return None
    try:
        return page.evaluate(JS_GET_STATS)
    except Exception as e:
        print(f"  [!] Error JS stats {match_id[:8]}: {e}")
        return None


def main():
    print(f"[AS] Temporada: {SEASON}  |  Jornadas: {from_jornada}–{TOTAL_JORNADAS}")

    # Cargar datos existentes
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        print(f"[AS] Datos existentes cargados: {len(all_data)} partidos")
    else:
        all_data = []

    # Índice para evitar re-scraping
    done_ids = {e['match_id'] for e in all_data}
    total_new = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS)
        ctx = browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/124.0.0.0 Safari/537.36'
            ),
            locale='es-ES',
            viewport={'width': 1280, 'height': 800},
        )
        page = ctx.new_page()
        page.set_extra_http_headers({'Accept-Language': 'es-ES,es;q=0.9'})

        for jornada_n in range(from_jornada, TOTAL_JORNADAS + 1):
            print(f"\n[J{jornada_n:02d}] Cargando jornada...")
            matches = get_jornada_matches(page, jornada_n)

            if not matches:
                print(f"  [!] Sin partidos (jornada no publicada aun?)")
                continue

            print(f"  -> {len(matches)} partidos encontrados")
            new_in_jornada = 0

            for m in matches:
                match_id = m.get('match_id', '')
                if not match_id:
                    continue
                if match_id in done_ids:
                    print(f"  ok {m['home']} vs {m['away']} (ya procesado)")
                    continue

                home = norm_name(m.get('home', '?'))
                away = norm_name(m.get('away', '?'))
                print(f"  -> {home} vs {away}  [{match_id[:10]}]", end='', flush=True)

                stats = get_match_stats(page, jornada_n, match_id)

                if stats:
                    entry = {
                        'season':   SEASON,
                        'jornada':  jornada_n,
                        'match_id': match_id,
                        'home':     home,
                        'away':     away,
                        'home_id':  m.get('home_id'),
                        'away_id':  m.get('away_id'),
                        **stats,
                    }
                    all_data.append(entry)
                    done_ids.add(match_id)
                    new_in_jornada += 1
                    total_new += 1
                    fields = [k for k in stats if k != 'status']
                    print(f"  OK ({len(fields)} campos, {stats.get('status','')})", flush=True)
                else:
                    print(f"  -- sin stats (partido no jugado?)", flush=True)

            if new_in_jornada:
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)
                print(f"  >> {new_in_jornada} nuevos guardados -> {OUTPUT_FILE}")

        browser.close()

    print(f"\n[OK] Total nuevos: {total_new}  |  Total acumulado: {len(all_data)}")
    print(f"     Guardado en: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
