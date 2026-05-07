"""
db.py — Capa de persistencia SQLite para Liga Hyper.
Soporta múltiples temporadas. Un único fichero liga.db junto al proyecto.

Uso desde otros scripts:
    import db
    db.save_liga_data(data_dict, '25_26')
    db.save_scores_data(scores_dict, '25_26')
    db.finalize_season('25_26')
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'liga.db')

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS seasons (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    year          TEXT    NOT NULL UNIQUE,   -- '25_26', '26_27', ...
    label         TEXT,                      -- '2025/26'
    total_rounds  INTEGER DEFAULT 0,
    total_season_rounds INTEGER DEFAULT 42,
    finalized     INTEGER DEFAULT 0,
    created_at    TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS teams (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    name       TEXT    NOT NULL,
    UNIQUE(season_id, name),
    FOREIGN KEY(season_id) REFERENCES seasons(id)
);

CREATE TABLE IF NOT EXISTS fixtures (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    round_idx  INTEGER NOT NULL,    -- 0-based (J1=0)
    home_team  TEXT    NOT NULL,
    away_team  TEXT    NOT NULL,
    UNIQUE(season_id, round_idx, home_team),
    FOREIGN KEY(season_id) REFERENCES seasons(id)
);

CREATE TABLE IF NOT EXISTS results (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    team_name  TEXT    NOT NULL,
    round_idx  INTEGER NOT NULL,    -- 0-based
    result     TEXT,                -- V / E / D
    score      TEXT,                -- '2-1' desde perspectiva del equipo
    venue      TEXT,                -- H / A
    opponent   TEXT,
    UNIQUE(season_id, team_name, round_idx),
    FOREIGN KEY(season_id) REFERENCES seasons(id)
);

CREATE TABLE IF NOT EXISTS standings_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    round_idx  INTEGER NOT NULL,
    team_name  TEXT    NOT NULL,
    position   INTEGER,
    pts        INTEGER,
    wins       INTEGER DEFAULT 0,
    draws      INTEGER DEFAULT 0,
    losses     INTEGER DEFAULT 0,
    gf         INTEGER DEFAULT 0,
    gc         INTEGER DEFAULT 0,
    saved_at   TEXT    DEFAULT (datetime('now')),
    UNIQUE(season_id, round_idx, team_name),
    FOREIGN KEY(season_id) REFERENCES seasons(id)
);

CREATE TABLE IF NOT EXISTS team_meta (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    team_name  TEXT    NOT NULL,
    situacion  TEXT    DEFAULT '',
    quedan     INTEGER DEFAULT 0,
    updated_at TEXT    DEFAULT (datetime('now')),
    UNIQUE(season_id, team_name),
    FOREIGN KEY(season_id) REFERENCES seasons(id)
);

CREATE TABLE IF NOT EXISTS update_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id  INTEGER NOT NULL,
    source     TEXT,   -- 'excel', 'football-data', 'besoccer', 'manual'
    round_idx  INTEGER,
    records    INTEGER,
    notes      TEXT,
    logged_at  TEXT    DEFAULT (datetime('now'))
);
"""

# ─────────────────────────────────────────────────────────────────────────────
def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db():
    """Crea todas las tablas si no existen."""
    c = _conn()
    c.executescript(SCHEMA)
    c.commit()
    c.close()

def get_or_create_season(year: str, label: str = None) -> int:
    """Devuelve season_id para el año dado, creándolo si hace falta."""
    init_db()
    c = _conn()
    row = c.execute("SELECT id FROM seasons WHERE year=?", (year,)).fetchone()
    if row:
        sid = row['id']
    else:
        lbl = label or ('20' + year[:2] + '/' + '20' + year[3:])
        cur = c.execute("INSERT INTO seasons(year, label) VALUES(?,?)", (year, lbl))
        c.commit()
        sid = cur.lastrowid
        print(f'  Nueva temporada creada en DB: {year} (id={sid})')
    c.close()
    return sid

# ─────────────────────────────────────────────────────────────────────────────
def save_liga_data(data: dict, year: str):
    """
    Persiste todo el contenido de liga_data.json en la BD.
    Llamar después de generate_data.py.
    """
    init_db()
    sid = get_or_create_season(year)
    c = _conn()
    total_rounds = data['total_rounds']
    c.execute("UPDATE seasons SET total_rounds=?, total_season_rounds=? WHERE id=?",
              (total_rounds, data.get('total_season_rounds', 42), sid))

    # Equipos
    for name in data['teams']:
        c.execute("INSERT OR IGNORE INTO teams(season_id,name) VALUES(?,?)", (sid, name))

    # Fixtures (del calendario oficial)
    inserted = set()
    for team, opps in data.get('opponents_by_team', {}).items():
        for r_idx, opp in enumerate(opps):
            if opp is None:
                continue
            key = (r_idx, min(team, opp), max(team, opp))
            if key in inserted:
                continue
            inserted.add(key)
            c.execute(
                "INSERT OR IGNORE INTO fixtures(season_id,round_idx,home_team,away_team) VALUES(?,?,?,?)",
                (sid, r_idx, team, opp)
            )

    # Resultados + rivales por jornada
    results_map = data['results_by_team']
    opps_map    = data.get('opponents_by_team', {})
    for team in data['teams']:
        res_list  = results_map.get(team, [])
        opps_list = opps_map.get(team, [])
        for r_idx, result in enumerate(res_list):
            opp = opps_list[r_idx] if r_idx < len(opps_list) else None
            c.execute(
                "INSERT OR REPLACE INTO results(season_id,team_name,round_idx,result,opponent)"
                " VALUES(?,?,?,?,?)",
                (sid, team, r_idx, result, opp)
            )
        # Situación y puntos que quedan
        situacion = data.get('situacion_by_team', {}).get(team, '')
        quedan    = data.get('quedan_by_team',    {}).get(team, 0)
        c.execute(
            "INSERT OR REPLACE INTO team_meta(season_id,team_name,situacion,quedan,updated_at)"
            " VALUES(?,?,?,?,datetime('now'))",
            (sid, team, situacion, quedan)
        )

    # Historial de posiciones y puntos por jornada
    positions_map = data.get('positions_by_team', {})
    points_map    = data.get('points_by_team', {})
    for team in data['teams']:
        pos_list = positions_map.get(team, [])
        pts_list = points_map.get(team, [])
        for r_idx in range(min(len(pos_list), len(pts_list))):
            c.execute(
                "INSERT OR REPLACE INTO standings_history"
                "(season_id,round_idx,team_name,position,pts) VALUES(?,?,?,?,?)",
                (sid, r_idx, team, pos_list[r_idx], pts_list[r_idx])
            )

    c.execute(
        "INSERT INTO update_log(season_id,source,records,notes) VALUES(?,?,?,?)",
        (sid, 'excel', len(data['teams']) * total_rounds, f'J{total_rounds}')
    )
    c.commit()
    c.close()
    print(f'  DB: liga_data guardado (temporada {year}, J{total_rounds})')

# ─────────────────────────────────────────────────────────────────────────────
def save_scores_data(scores_data: dict, year: str):
    """
    Actualiza marcadores y venue en la tabla results.
    Llamar después de fetch_scores.py.
    """
    init_db()
    sid = get_or_create_season(year)
    c = _conn()
    scores_map = scores_data.get('scores_by_team', {})
    venue_map  = scores_data.get('venue_by_team',  {})
    count = 0
    for team, rounds in scores_map.items():
        for r_str, score in rounds.items():
            r_idx = int(r_str)
            venue = venue_map.get(team, {}).get(r_str, '')
            c.execute(
                "UPDATE results SET score=?, venue=?"
                " WHERE season_id=? AND team_name=? AND round_idx=?",
                (score, venue, sid, team, r_idx)
            )
            count += 1
    c.execute(
        "INSERT INTO update_log(season_id,source,records,notes) VALUES(?,?,?,?)",
        (sid, 'football-data', count, 'scores+venues')
    )
    c.commit()
    c.close()
    print(f'  DB: scores_data guardado (temporada {year}, {count} registros)')

# ─────────────────────────────────────────────────────────────────────────────
def finalize_season(year: str):
    """Marca la temporada como finalizada (todas las jornadas jugadas)."""
    init_db()
    c = _conn()
    c.execute("UPDATE seasons SET finalized=1 WHERE year=?", (year,))
    c.commit()
    c.close()
    print(f'  DB: temporada {year} marcada como finalizada.')

def get_seasons():
    """Lista todas las temporadas en la BD."""
    init_db()
    c = _conn()
    rows = c.execute("SELECT * FROM seasons ORDER BY year DESC").fetchall()
    c.close()
    return [dict(r) for r in rows]

def get_season_summary(year: str):
    """Resumen de una temporada (clasificación final + metadatos)."""
    init_db()
    c = _conn()
    sr = c.execute("SELECT * FROM seasons WHERE year=?", (year,)).fetchone()
    if not sr:
        c.close()
        return None
    sid = sr['id']
    final_idx = sr['total_rounds'] - 1
    standings = c.execute(
        """SELECT sh.team_name, sh.position, sh.pts,
                  tm.situacion, tm.quedan
           FROM standings_history sh
           LEFT JOIN team_meta tm
             ON tm.season_id=sh.season_id AND tm.team_name=sh.team_name
           WHERE sh.season_id=? AND sh.round_idx=?
           ORDER BY sh.position""",
        (sid, final_idx)
    ).fetchall()
    teams = c.execute("SELECT name FROM teams WHERE season_id=? ORDER BY name", (sid,)).fetchall()
    c.close()
    return {
        'year':          year,
        'label':         sr['label'],
        'total_rounds':  sr['total_rounds'],
        'finalized':     bool(sr['finalized']),
        'teams':         [r['name'] for r in teams],
        'final_standings': [dict(r) for r in standings],
    }

if __name__ == '__main__':
    init_db()
    print('liga.db inicializada correctamente.')
    seasons = get_seasons()
    if seasons:
        for s in seasons:
            estado = '✅ Finalizada' if s['finalized'] else '⏳ En curso'
            print(f'  {s["year"]:<10} J{s["total_rounds"]:<4} {estado}')
    else:
        print('  Sin temporadas registradas aún.')
