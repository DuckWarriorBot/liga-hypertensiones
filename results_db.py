"""
results_db.py — Base de datos persistente de resultados confirmados.

Un resultado queda "locked" (bloqueado) cuando tanto Marca como FlashScore
lo confirman con el MISMO marcador. Un resultado locked NUNCA se sobreescribe.

Formato del fichero results_db.json:
{
  "locked": {
    "Albacete|Almería|0": {
      "marca":      {"score_h": "4-4", "score_a": "4-4", "res_h": "E"},
      "flashscore": {"score_h": "4-4", "score_a": "4-4", "res_h": "E"},
      "score_h": "4-4",
      "score_a": "4-4",
      "res_h":   "E",
      "locked":  true,
      "first_seen": "2025-09-15T22:00:00",
      "locked_at":  "2025-09-15T22:05:00"
    }
  }
}
"""

import json, datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / 'results_db.json'


def load():
    """Carga la BD de resultados. Devuelve dict con clave 'locked'."""
    if DB_PATH.exists():
        try:
            return json.loads(DB_PATH.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'locked': {}}


def save(db):
    """Guarda la BD de resultados."""
    DB_PATH.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')


def _key(home, away, r_idx):
    return f'{home}|{away}|{int(r_idx)}'


def get_locked(db, home, away, r_idx):
    """
    Devuelve (score_h, score_a, res_h) si el partido está locked.
    Devuelve None si no está locked.
    """
    entry = db['locked'].get(_key(home, away, r_idx), {})
    if entry.get('locked'):
        return entry['score_h'], entry['score_a'], entry['res_h']
    return None


def confirm_source(db, source, home, away, r_idx, score_h, score_a, res_h):
    """
    Registra la confirmación de un resultado desde 'source' ('marca' o 'flashscore').
    Si ambas fuentes coinciden, bloquea el resultado.
    Devuelve True si el resultado queda locked tras esta confirmación.
    """
    k = _key(home, away, r_idx)
    entry = db['locked'].setdefault(k, {})

    # Si ya está locked, no tocar nada
    if entry.get('locked'):
        return True

    # Registrar esta fuente
    entry[source] = {'score_h': score_h, 'score_a': score_a, 'res_h': res_h}
    if 'first_seen' not in entry:
        entry['first_seen'] = datetime.datetime.now().isoformat()

    # Intentar bloquear si ambas fuentes presentes y de acuerdo
    m  = entry.get('marca', {})
    fs = entry.get('flashscore', {})
    if m and fs and m.get('score_h') == fs.get('score_h'):
        entry['locked']    = True
        entry['score_h']   = m['score_h']
        entry['score_a']   = m['score_a']
        entry['res_h']     = m['res_h']
        entry['locked_at'] = datetime.datetime.now().isoformat()

    return entry.get('locked', False)


def apply_locked_to_scores(db, scores_full, liga_data):
    """
    Fuerza los resultados locked en scores_full y liga_data.
    scores_full puede ser el dict completo de scores_data.json
    (con top-level por equipo + 'scores_by_team' + 'venue_by_team').
    """
    res_map = liga_data.get('results_by_team', {})
    restored = 0

    for k, entry in db['locked'].items():
        if not entry.get('locked'):
            continue
        try:
            home, away, r_idx_str = k.rsplit('|', 2)
            r_idx = int(r_idx_str)
        except Exception:
            continue

        score_h = entry['score_h']   # "hg-ag" desde local
        score_a = entry['score_a']   # "ag-hg" desde visitante
        res_h   = entry['res_h']     # 'V'/'E'/'D' para local
        res_a   = 'V' if res_h == 'D' else ('D' if res_h == 'V' else 'E')
        idx_str = str(r_idx)

        # Actualizar top-level (por equipo directamente)
        scores_full.setdefault(home, {})[idx_str] = score_h
        scores_full.setdefault(away, {})[idx_str] = score_a

        # Actualizar scores_by_team si existe
        sb = scores_full.get('scores_by_team')
        if sb is not None:
            sb.setdefault(home, {})[idx_str] = score_h
            sb.setdefault(away, {})[idx_str] = score_a

        # Actualizar venue_by_team si existe
        vb = scores_full.get('venue_by_team')
        if vb is not None:
            vb.setdefault(home, {})[idx_str] = 'H'
            vb.setdefault(away, {})[idx_str] = 'A'

        # Actualizar results_by_team en liga_data
        home_res = res_map.get(home, [])
        away_res = res_map.get(away, [])
        if r_idx < len(home_res) and home_res[r_idx] != res_h:
            home_res[r_idx] = res_h
            restored += 1
        if r_idx < len(away_res) and away_res[r_idx] != res_a:
            away_res[r_idx] = res_a

    if restored:
        print(f'[results_db] {restored} resultados restaurados desde BD locked')
    return restored
