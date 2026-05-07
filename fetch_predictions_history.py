"""
fetch_predictions_history.py
Genera predicciones históricas jornada a jornada para cada equipo,
basadas en el historial de posiciones de liga_data.json.

Cada jornada se calcula cuánto % de probabilidad de ascenso/playoff/
permanencia/descenso tenía el equipo según su posición en ese momento,
amplificado por el avance de la temporada (cuanto más tarde, más certeza).
"""
import json, os, random

HIST_FILE = 'predictions_history.json'

# Distribución base por posición (sobre 22 equipos)
def pos_to_base(pos):
    if   pos <= 1:  return {'ascenso': 78, 'playoff': 16, 'permanencia':  5, 'descenso':  1}
    elif pos <= 2:  return {'ascenso': 58, 'playoff': 28, 'permanencia': 12, 'descenso':  2}
    elif pos <= 3:  return {'ascenso': 22, 'playoff': 56, 'permanencia': 20, 'descenso':  2}
    elif pos <= 4:  return {'ascenso': 12, 'playoff': 62, 'permanencia': 24, 'descenso':  2}
    elif pos <= 6:  return {'ascenso':  5, 'playoff': 58, 'permanencia': 35, 'descenso':  2}
    elif pos <= 9:  return {'ascenso':  1, 'playoff': 20, 'permanencia': 75, 'descenso':  4}
    elif pos <= 13: return {'ascenso':  0, 'playoff':  8, 'permanencia': 83, 'descenso':  9}
    elif pos <= 15: return {'ascenso':  0, 'playoff':  2, 'permanencia': 76, 'descenso': 22}
    elif pos <= 17: return {'ascenso':  0, 'playoff':  1, 'permanencia': 62, 'descenso': 37}
    elif pos == 18: return {'ascenso':  0, 'playoff':  0, 'permanencia': 48, 'descenso': 52}
    elif pos == 19: return {'ascenso':  0, 'playoff':  0, 'permanencia': 30, 'descenso': 70}
    elif pos == 20: return {'ascenso':  0, 'playoff':  0, 'permanencia': 18, 'descenso': 82}
    else:           return {'ascenso':  0, 'playoff':  0, 'permanencia':  9, 'descenso': 91}

def normalize(d):
    """Fuerza que los 4 valores sumen 100."""
    total = sum(d.values())
    if total == 0:
        d['permanencia'] = 100
        return d
    result = {k: max(0, int(v * 100 / total)) for k, v in d.items()}
    diff = 100 - sum(result.values())
    dominant = max(result, key=result.get)
    result[dominant] += diff
    return result

def make_pred(pos, round_idx, total_rounds, rng, final_base=None):
    base = pos_to_base(pos)
    progress = (round_idx + 1) / total_rounds  # 0..1

    # Interpolación hacia la predicción final conforme avanza la temporada
    if final_base and progress > 0.65:
        alpha = min(1.0, (progress - 0.65) / 0.35)
        for k in base:
            base[k] = int(base[k] * (1 - alpha) + final_base.get(k, base[k]) * alpha)

    # Amplificación de certeza: la posición dominante gana peso
    amp = progress * 0.55
    dominant = max(base, key=base.get)
    for k in base:
        if k == dominant:
            base[k] = min(100, int(base[k] + (100 - base[k]) * amp))
        else:
            base[k] = max(0, int(base[k] * (1 - amp)))

    # Ruido aleatorio (decrece con el avance)
    noise = max(1, int(6 * (1 - progress)))
    for k in base:
        base[k] = max(0, base[k] + rng.randint(-noise, noise))

    return normalize(base)


if __name__ == '__main__':
    rng = random.Random(42)

    with open('liga_data.json', encoding='utf-8') as f:
        liga = json.load(f)

    teams        = liga['teams']
    total_rounds = liga['total_rounds']
    positions    = liga['positions_by_team']
    final_snap   = liga.get('final_standings', [])
    n            = len(teams)

    # Base final por equipo (desde su posición actual en la última jornada)
    final_base_map = {t['name']: pos_to_base(t.get('pos', t.get('position', 22)))
                      for t in final_snap}

    print(f'Generando predicciones para {n} equipos × {total_rounds} jornadas...')
    hist = {}
    for team in teams:
        hist[team] = {}
        pos_hist = positions.get(team, [])
        fb       = final_base_map.get(team)
        for r_idx, pos in enumerate(pos_hist):
            hist[team][str(r_idx)] = make_pred(pos, r_idx, total_rounds, rng, fb)

    # Preservar datos reales si ya existían (solo si las claves coinciden con los nombres canónicos)
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, encoding='utf-8') as f:
            existing = json.load(f)
        canonical = set(teams)
        existing_valid = all(k in canonical for k in existing.keys())
        if existing_valid:
            for team, rounds in hist.items():
                if team not in existing:
                    existing[team] = rounds
                else:
                    for r, pred in rounds.items():
                        if r not in existing[team]:
                            existing[team][r] = pred
            hist = existing
        else:
            print('  ⚠ predictions_history.json tenía nombres incorrectos – regenerando desde cero')

    with open(HIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in hist.values())
    print(f'  {HIST_FILE} guardado: {n} equipos · {total} predicciones\n')

    print('Muestra Racing (J1, J10, J20, J38):')
    for r in ['0', '9', '19', '37']:
        p = hist.get('Racing', {}).get(r)
        if p:
            print(f'  J{int(r)+1:>2}: asc={p["ascenso"]:>3}%  play={p["playoff"]:>3}%  '
                  f'perm={p["permanencia"]:>3}%  desc={p["descenso"]:>3}%')
