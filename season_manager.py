"""
season_manager.py — Gestión de temporadas de Liga Hyper.

Comandos:
  python season_manager.py status            → lista temporadas en DB
  python season_manager.py save [year]       → guarda JSON actuales en DB
  python season_manager.py finalize [year]   → guarda + marca como finalizada
  python season_manager.py summary [year]    → muestra clasificación final
  python season_manager.py next [year]       → instrucciones para temporada siguiente

Año por defecto: 25_26
"""
import sys, json, os
import db

CURRENT_YEAR = '25_26'

# ─── Helpers ────────────────────────────────────────────────────────────────
def _next_year(year: str) -> str:
    parts = year.split('_')
    return f'{int(parts[0])+1}_{int(parts[1])+1}'

def _load_jsons():
    if not os.path.exists('liga_data.json'):
        print('❌  liga_data.json no encontrado. Ejecuta: python generate_data.py')
        sys.exit(1)
    if not os.path.exists('scores_data.json'):
        print('❌  scores_data.json no encontrado. Ejecuta: python fetch_scores.py')
        sys.exit(1)
    with open('liga_data.json',   encoding='utf-8') as f: liga   = json.load(f)
    with open('scores_data.json', encoding='utf-8') as f: scores = json.load(f)
    return liga, scores

# ─── Comandos ────────────────────────────────────────────────────────────────
def cmd_status():
    seasons = db.get_seasons()
    if not seasons:
        print('No hay temporadas registradas en liga.db.')
        return
    print(f'\n{"Año":<10} {"Jornadas":<10} {"Estado"}')
    print('─' * 35)
    for s in seasons:
        estado = '✅ Finalizada' if s['finalized'] else '⏳ En curso'
        print(f'{s["year"]:<10} J{s["total_rounds"]:<9} {estado}')
    print()

def cmd_save(year: str):
    liga, scores = _load_jsons()
    db.save_liga_data(liga, year)
    db.save_scores_data(scores, year)
    print(f'\n✅  Temporada {year} guardada en liga.db')

def cmd_finalize(year: str):
    liga, scores = _load_jsons()
    total = liga.get('total_rounds', 0)
    if total < 38:
        print(f'⚠️  Solo hay {total} jornadas. ¿Seguro que la temporada está completa?')
        resp = input('Continuar de todas formas? (s/N): ').strip().lower()
        if resp != 's':
            print('Cancelado.')
            return
    db.save_liga_data(liga, year)
    db.save_scores_data(scores, year)
    db.finalize_season(year)
    print(f'\n✅  Temporada {year} finalizada y archivada en liga.db.')
    print(f'   Ejecuta: python season_manager.py next {year}')

def cmd_summary(year: str):
    s = db.get_season_summary(year)
    if not s:
        print(f'❌  Temporada {year} no encontrada en DB.')
        return
    estado = '✅ Finalizada' if s['finalized'] else '⏳ En curso'
    print(f'\n=== Temporada {s["label"] or year} · {estado} ===')
    print(f'Jornadas disputadas: {s["total_rounds"]}  |  Equipos: {len(s["teams"])}')
    if s['final_standings']:
        print('\nClasificación final:')
        for t in s['final_standings']:
            mark = '🟢' if t['position'] <= 2 else '🟡' if t['position'] <= 6 else '🔴' if t['position'] >= 19 else '⚪'
            print(f'  {mark} #{t["position"]:<3} {t["team_name"]:<24} {t["pts"]} pts')
    print()

def cmd_next(current_year: str):
    ny = _next_year(current_year)
    ny_label = '20' + ny[:2] + '/20' + ny[3:]

    # Verificar que la actual está finalizada
    seasons = [s for s in db.get_seasons() if s['year'] == current_year]
    if seasons and not seasons[0]['finalized']:
        print(f'⚠️  La temporada {current_year} no está marcada como finalizada.')
        print(f'   Ejecuta: python season_manager.py finalize {current_year}')

    print(f"""
╔══════════════════════════════════════════════════════════╗
║      Preparar temporada {ny_label}                       ║
╚══════════════════════════════════════════════════════════╝

1. CALENDARIO (julio/agosto):
   → https://www.marca.com/futbol/segunda-division/calendario.html
   Cuando esté publicado, actualiza la lista FIXTURES[] en generate_data.py
   Reemplaza las 42 jornadas con los nuevos partidos.

2. ARCHIVO EXCEL:
   Renombra / crea:  LIGA HYPER {ny}__.xlsx
   Actualiza la ruta en generate_data.py si es necesario.

3. ESCUDOS E IDs BeSoccer:
   Puede haber equipos nuevos (ascensos/descensos).
   Actualiza TEAM_BADGES y TEAM_COLORS en build.py.

4. ARRANCAR LA TEMPORADA:
   python generate_data.py
   python fetch_scores.py
   python build.py
   → Repite esto después de cada jornada.

5. AL FINALIZAR {ny_label}:
   python season_manager.py finalize {ny}

Nota: football-data.co.uk para {ny_label} estará en:
   https://www.football-data.co.uk/mmz4281/{ny}/SP2.csv
   Actualiza URL en fetch_scores.py.
""")

# ─── Main ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    args = sys.argv[1:]
    cmd  = args[0] if args else 'status'
    year = args[1] if len(args) > 1 else CURRENT_YEAR

    if   cmd == 'status':   cmd_status()
    elif cmd == 'save':     cmd_save(year)
    elif cmd == 'finalize': cmd_finalize(year)
    elif cmd == 'summary':  cmd_summary(year)
    elif cmd == 'next':     cmd_next(year)
    else:
        print(__doc__)
