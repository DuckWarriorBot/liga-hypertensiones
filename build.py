"""
build.py  –  Liga Hyper 25/26  WebApp Builder
Genera index.html con todos los datos embebidos.
Uso: python build.py
"""
import json, os, datetime

with open('liga_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

BUILD_TS = datetime.datetime.now().isoformat(timespec='seconds')

TEAM_COLORS = {
    'Racing':           '#006633',  # verde Racing Santander
    'Almería':          '#CC0000',  # rojo UD Almería
    'Deportivo':        '#1C4E97',  # azul Deportivo de La Coruña
    'Las Palmas':       '#F5C500',  # amarillo UD Las Palmas
    'Castellón':        '#000000',  # negro CD Castellón
    'Málaga':           '#38BDF8',  # celeste Málaga CF
    'Burgos':           '#000000',  # negro Burgos CF
    'Eibar':            '#003366',  # azul marino SD Eibar
    'Córdoba':          '#2B7A2B',  # verde Córdoba CF
    'Andorra':          '#1C3C8C',  # azul FC Andorra
    'Ceuta':            '#000000',  # negro AD Ceuta
    'Sporting':         '#CC0000',  # rojo Sporting de Gijón
    'Albacete':         '#000000',  # negro Albacete BP
    'Granada':          '#CC0000',  # rojo Granada CF
    'Valladolid':       '#6A0DAD',  # violeta Real Valladolid
    'Leganés':          '#003087',  # azul CD Leganés
    'Real Sociedad B':  '#0057A8',  # azul Real Sociedad
    'Cádiz':            '#F5C500',  # amarillo Cádiz CF
    'Mirandés':         '#CC0000',  # rojo CD Mirandés
    'Huesca':           '#003087',  # azul SD Huesca
    'Real Zaragoza':    '#003087',  # azul Real Zaragoza
    'Cultural Leonesa': '#CC0000',  # rojo Cultural Leonesa
    # ── Equipos de temporadas históricas ──────────────────────────────────
    'Levante':            '#0033A0',  # azul marino Levante UD
    'Cartagena':          '#CC0000',  # rojo FC Cartagena
    'Elche':              '#00843D',  # verde Elche CF
    'Eldense':            '#CC0000',  # rojo UD Eldense
    'Espanyol':           '#003DA5',  # azul RCD Espanyol
    'Tenerife':           '#003087',  # azul CD Tenerife
    'Girona':             '#9B1C31',  # granate Girona FC
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

# Escudos oficiales de BeSoccer CDN (cdn.resfu.com)
TEAM_BADGES = {
    'Racing':           'https://cdn.resfu.com/img_data/equipos/2052.png',
    'Almería':          'https://cdn.resfu.com/img_data/equipos/183.png',
    'Deportivo':            'https://cdn.resfu.com/img_data/equipos/901.png',
    'Las Palmas':       'https://cdn.resfu.com/img_data/equipos/2563.png',
    'Castellón':        'https://cdn.resfu.com/img_data/equipos/673.png',
    'Málaga':           'https://cdn.resfu.com/img_data/equipos/1617.png',
    'Burgos':           'https://cdn.resfu.com/img_data/equipos/565.png',
    'Eibar':            'https://cdn.resfu.com/img_data/equipos/7663.png',
    'Córdoba':          'https://cdn.resfu.com/img_data/equipos/831.png',
    'Andorra':          'https://cdn.resfu.com/img_data/equipos/9501.png',
    'Ceuta':            'https://cdn.resfu.com/img_data/equipos/665.png',
    'Sporting':         'https://cdn.resfu.com/img_data/equipos/2125.png',
    'Albacete':         'https://cdn.resfu.com/img_data/equipos/140.png',
    'Granada':          'https://cdn.resfu.com/img_data/equipos/4235.png',
    'Valladolid':       'https://cdn.resfu.com/img_data/equipos/2654.png',
    'Leganés':          'https://cdn.resfu.com/img_data/equipos/1535.png',
    'Real Sociedad B':  'https://cdn.resfu.com/img_data/equipos/2121.png',
    'Cádiz':            'https://cdn.resfu.com/img_data/equipos/603.png',
    'Mirandés':         'https://cdn.resfu.com/img_data/equipos/1699.png',
    'Huesca':           'https://cdn.resfu.com/img_data/equipos/1339.png',
    'Real Zaragoza':    'https://cdn.resfu.com/img_data/equipos/2136.png',
    'Cultural Leonesa': 'https://cdn.resfu.com/img_data/equipos/877.png',
    # ── Equipos de temporadas históricas (BeSoccer CDN) ──────────────────
    'Levante':            'https://cdn.resfu.com/img_data/equipos/1547.png',
    'Cartagena':          'https://cdn.resfu.com/img_data/equipos/643.png',
    'Elche':              'https://cdn.resfu.com/img_data/equipos/975.png',
    'Eldense':            'https://cdn.resfu.com/img_data/equipos/977.png',
    'Espanyol':           'https://cdn.resfu.com/img_data/equipos/998.png',
    'Tenerife':           'https://cdn.resfu.com/img_data/equipos/2477.png',
    'Girona':             'https://cdn.resfu.com/img_data/equipos/1236.png',
    'Mallorca':           'https://cdn.resfu.com/img_data/equipos/1623.png',
    'Real Oviedo':        'https://cdn.resfu.com/img_data/equipos/2115.png',
    'Alavés':             'https://cdn.resfu.com/img_data/equipos/137.png',
    'Rayo Vallecano':     'https://cdn.resfu.com/img_data/equipos/2080.png',
    'Lugo':               'https://cdn.resfu.com/img_data/equipos/1598.png',
    'Ponferradina':       'https://cdn.resfu.com/img_data/equipos/2301.png',
    'Alcorcón':           'https://cdn.resfu.com/img_data/equipos/64.png',
    'Amorebieta':         'https://cdn.resfu.com/img_data/equipos/213.png',
    'Ibiza':              'https://cdn.resfu.com/img_data/equipos/1352.png',
    'Fuenlabrada':        'https://cdn.resfu.com/img_data/equipos/1179.png',
    'Numancia':           'https://cdn.resfu.com/img_data/equipos/1832.png',
    'Racing Club Ferrol': 'https://cdn.resfu.com/img_data/equipos/2055.png',
    'Sabadell':           'https://cdn.resfu.com/img_data/equipos/2198.png',
    'UD Logroñés':        'https://cdn.resfu.com/img_data/equipos/1578.png',
    'Villarreal B':       'https://cdn.resfu.com/img_data/equipos/2717.png',
    'Extremadura':        'https://cdn.resfu.com/img_data/equipos/1026.png',
}

# Nota: besoccer_ids.json NO sobreescribe TEAM_BADGES — los IDs hardcodeados son correctos.
# La función fetch_besoccer_shields produce IDs incorrectos por matching posicional fallback.

# Stats GF/GC + local/visitante extraidos de la tabla oficial de Marca
TEAM_EXTRA_STATS = {
    'Racing':           {'gf':79,'gc':57,'home_pts':41,'home_pj':19,'home_pg':13,'home_pe':2,'home_pp':4,'home_gf':47,'home_gc':27,'away_pts':31,'away_pj':19,'away_pg':9,'away_pe':4,'away_pp':6,'away_gf':32,'away_gc':30},
    'Almería':          {'gf':78,'gc':58,'home_pts':44,'home_pj':19,'home_pg':14,'home_pe':2,'home_pp':3,'home_gf':50,'home_gc':28,'away_pts':26,'away_pj':19,'away_pg':7,'away_pe':5,'away_pp':7,'away_gf':28,'away_gc':30},
    'Deportivo':            {'gf':59,'gc':41,'home_pts':35,'home_pj':19,'home_pg':10,'home_pe':5,'home_pp':4,'home_gf':28,'home_gc':19,'away_pts':33,'away_pj':19,'away_pg':9,'away_pe':6,'away_pp':4,'away_gf':31,'away_gc':22},
    'Las Palmas':       {'gf':51,'gc':32,'home_pts':41,'home_pj':20,'home_pg':12,'home_pe':5,'home_pp':3,'home_gf':32,'home_gc':13,'away_pts':25,'away_pj':18,'away_pg':6,'away_pe':7,'away_pp':5,'away_gf':19,'away_gc':19},
    'Castellón':        {'gf':65,'gc':48,'home_pts':39,'home_pj':19,'home_pg':12,'home_pe':3,'home_pp':4,'home_gf':39,'home_gc':23,'away_pts':25,'away_pj':19,'away_pg':6,'away_pe':7,'away_pp':6,'away_gf':26,'away_gc':25},
    'Málaga':           {'gf':66,'gc':49,'home_pts':39,'home_pj':19,'home_pg':11,'home_pe':6,'home_pp':2,'home_gf':39,'home_gc':22,'away_pts':24,'away_pj':19,'away_pg':7,'away_pe':3,'away_pp':9,'away_gf':27,'away_gc':27},
    'Burgos':           {'gf':44,'gc':33,'home_pts':34,'home_pj':19,'home_pg':9,'home_pe':7,'home_pp':3,'home_gf':24,'home_gc':12,'away_pts':28,'away_pj':19,'away_pg':8,'away_pe':4,'away_pp':7,'away_gf':20,'away_gc':21},
    'Eibar':            {'gf':47,'gc':36,'home_pts':43,'home_pj':20,'home_pg':13,'home_pe':4,'home_pp':3,'home_gf':35,'home_gc':17,'away_pts':18,'away_pj':18,'away_pg':4,'away_pe':6,'away_pp':8,'away_gf':12,'away_gc':19},
    'Córdoba':          {'gf':54,'gc':56,'home_pts':28,'home_pj':18,'home_pg':8,'home_pe':4,'home_pp':6,'home_gf':25,'home_gc':25,'away_pts':29,'away_pj':20,'away_pg':8,'away_pe':5,'away_pp':7,'away_gf':29,'away_gc':31},
    'Andorra':          {'gf':56,'gc':48,'home_pts':27,'home_pj':19,'home_pg':7,'home_pe':6,'home_pp':6,'home_gf':26,'home_gc':22,'away_pts':28,'away_pj':19,'away_pg':8,'away_pe':4,'away_pp':7,'away_gf':30,'away_gc':26},
    'Ceuta':            {'gf':46,'gc':58,'home_pts':36,'home_pj':18,'home_pg':11,'home_pe':3,'home_pp':4,'home_gf':25,'home_gc':18,'away_pts':18,'away_pj':20,'away_pg':4,'away_pe':6,'away_pp':10,'away_gf':21,'away_gc':40},
    'Sporting':         {'gf':51,'gc':49,'home_pts':36,'home_pj':20,'home_pg':10,'home_pe':6,'home_pp':4,'home_gf':32,'home_gc':21,'away_pts':16,'away_pj':18,'away_pg':5,'away_pe':1,'away_pp':12,'away_gf':19,'away_gc':28},
    'Albacete':         {'gf':49,'gc':51,'home_pts':25,'home_pj':19,'home_pg':7,'home_pe':4,'home_pp':8,'home_gf':25,'home_gc':30,'away_pts':25,'away_pj':19,'away_pg':6,'away_pe':7,'away_pp':6,'away_gf':24,'away_gc':21},
    'Granada':          {'gf':48,'gc':49,'home_pts':26,'home_pj':19,'home_pg':6,'home_pe':8,'home_pp':5,'home_gf':27,'home_gc':22,'away_pts':22,'away_pj':19,'away_pg':6,'away_pe':4,'away_pp':9,'away_gf':21,'away_gc':27},
    'Valladolid':       {'gf':41,'gc':50,'home_pts':26,'home_pj':19,'home_pg':7,'home_pe':5,'home_pp':7,'home_gf':21,'home_gc':19,'away_pts':17,'away_pj':19,'away_pg':4,'away_pe':5,'away_pp':10,'away_gf':20,'away_gc':31},
    'Leganés':          {'gf':41,'gc':46,'home_pts':23,'home_pj':18,'home_pg':6,'home_pe':5,'home_pp':7,'home_gf':21,'home_gc':21,'away_pts':19,'away_pj':20,'away_pg':4,'away_pe':7,'away_pp':9,'away_gf':20,'away_gc':25},
    'Real Sociedad B':  {'gf':46,'gc':54,'home_pts':27,'home_pj':19,'home_pg':7,'home_pe':6,'home_pp':6,'home_gf':26,'home_gc':24,'away_pts':15,'away_pj':19,'away_pg':4,'away_pe':3,'away_pp':12,'away_gf':20,'away_gc':30},
    'Cádiz':            {'gf':36,'gc':55,'home_pts':20,'home_pj':19,'home_pg':6,'home_pe':2,'home_pp':11,'home_gf':18,'home_gc':27,'away_pts':19,'away_pj':19,'away_pg':4,'away_pe':7,'away_pp':8,'away_gf':18,'away_gc':28},
    'Mirandés':         {'gf':42,'gc':64,'home_pts':20,'home_pj':19,'home_pg':5,'home_pe':5,'home_pp':9,'home_gf':19,'home_gc':29,'away_pts':16,'away_pj':19,'away_pg':4,'away_pe':4,'away_pp':11,'away_gf':23,'away_gc':35},
    'Huesca':           {'gf':39,'gc':59,'home_pts':28,'home_pj':19,'home_pg':7,'home_pe':7,'home_pp':5,'home_gf':22,'home_gc':21,'away_pts':8,'away_pj':19,'away_pg':2,'away_pe':2,'away_pp':15,'away_gf':17,'away_gc':38},
    'Real Zaragoza':    {'gf':33,'gc':51,'home_pts':18,'home_pj':19,'home_pg':4,'home_pe':6,'home_pp':9,'home_gf':17,'home_gc':26,'away_pts':17,'away_pj':19,'away_pg':4,'away_pe':5,'away_pp':10,'away_gf':16,'away_gc':25},
    'Cultural Leonesa': {'gf':35,'gc':62,'home_pts':14,'home_pj':19,'home_pg':3,'home_pe':5,'home_pp':11,'home_gf':13,'home_gc':29,'away_pts':19,'away_pj':19,'away_pg':5,'away_pe':4,'away_pp':10,'away_gf':22,'away_gc':33},
}

# Predicciones BeSoccer: % Ascenso, Playoff, Permanencia, Descenso
TEAM_PREDICTIONS = {
    'Racing':           {'ascenso':92,'playoff':8, 'permanencia':0,  'descenso':0 },
    'Almería':          {'ascenso':66,'playoff':34,'permanencia':0,  'descenso':0 },
    'Deportivo':            {'ascenso':30,'playoff':66,'permanencia':4,  'descenso':0 },
    'Las Palmas':       {'ascenso':9, 'playoff':84,'permanencia':7,  'descenso':0 },
    'Castellón':        {'ascenso':2, 'playoff':84,'permanencia':14, 'descenso':0 },
    'Málaga':           {'ascenso':0, 'playoff':61,'permanencia':39, 'descenso':0 },
    'Burgos':           {'ascenso':1, 'playoff':43,'permanencia':56, 'descenso':0 },
    'Eibar':            {'ascenso':0, 'playoff':19,'permanencia':81, 'descenso':0 },
    'Córdoba':          {'ascenso':0, 'playoff':1, 'permanencia':99, 'descenso':0 },
    'Andorra':          {'ascenso':0, 'playoff':0, 'permanencia':100,'descenso':0 },
    'Ceuta':            {'ascenso':0, 'playoff':0, 'permanencia':100,'descenso':0 },
    'Sporting':         {'ascenso':0, 'playoff':0, 'permanencia':100,'descenso':0 },
    'Albacete':         {'ascenso':0, 'playoff':0, 'permanencia':100,'descenso':0 },
    'Granada':          {'ascenso':0, 'playoff':0, 'permanencia':100,'descenso':0 },
    'Valladolid':       {'ascenso':0, 'playoff':0, 'permanencia':98, 'descenso':2 },
    'Leganés':          {'ascenso':0, 'playoff':0, 'permanencia':94, 'descenso':6 },
    'Real Sociedad B':  {'ascenso':0, 'playoff':0, 'permanencia':99, 'descenso':1 },
    'Cádiz':            {'ascenso':0, 'playoff':0, 'permanencia':45, 'descenso':55},
    'Mirandés':         {'ascenso':0, 'playoff':0, 'permanencia':38, 'descenso':62},
    'Huesca':           {'ascenso':0, 'playoff':0, 'permanencia':21, 'descenso':79},
    'Real Zaragoza':    {'ascenso':0, 'playoff':0, 'permanencia':5,  'descenso':95},
    'Cultural Leonesa': {'ascenso':0, 'playoff':0, 'permanencia':1,  'descenso':99},
}

# Mapa de nombres BeSoccer → nombres internos (Excel)
BESOCCER_NAME_MAP = {
    'Racing': 'Racing', 'Almería': 'Almería', 'RC Deportivo': 'Deportivo',
    'UD Las Palmas': 'Las Palmas', 'CD Castellón': 'Castellón',
    'Málaga': 'Málaga', 'Burgos CF': 'Burgos', 'Eibar': 'Eibar',
    'Córdoba CF': 'Córdoba', 'FC Andorra': 'Andorra', 'AD Ceuta FC': 'Ceuta',
    'Real Sporting': 'Sporting', 'Albacete': 'Albacete', 'Granada': 'Granada',
    'Real Valladolid': 'Valladolid', 'Leganés': 'Leganés',
    'Real Sociedad B': 'Real Sociedad B', 'Cádiz': 'Cádiz',
    'Huesca': 'Huesca', 'Mirandés': 'Mirandés', 'Real Zaragoza': 'Real Zaragoza',
    'Cultural Leonesa': 'Cultural Leonesa',
}

# Color primario de la camiseta de cada club (para fondos del tema oscuro)
TEAM_KIT = {
    'Racing':           '#22c55e',  # verde (medias icónicas) sobre blanco
    'Almería':          '#dc2626',  # rojas y blancas → rojo
    'Deportivo':            '#1d4ed8',  # azul y blanco → azul
    'Las Palmas':       '#f59e0b',  # amarillo
    'Castellón':        '#6b7280',  # blanco y negro → gris
    'Málaga':           '#38bdf8',  # celeste y blanco → celeste
    'Burgos':           '#94a3b8',  # blanco → plateado neutro
    'Eibar':            '#4338ca',  # azul y granate → índigo
    'Córdoba':          '#16a34a',  # verde y blanco → verde
    'Andorra':          '#2563eb',  # azul + amarillo + rojo → azul
    'Ceuta':            '#94a3b8',  # blanco → neutro
    'Sporting':         '#dc2626',  # rojo y blanco → rojo
    'Albacete':         '#94a3b8',  # blanco → neutro
    'Granada':          '#dc2626',  # rojo y blanco horizontal → rojo
    'Valladolid':       '#7c3aed',  # violeta y blanco → violeta
    'Leganés':          '#1d4ed8',  # azul y blanco → azul
    'Real Sociedad B':  '#1d4ed8',  # azul y blanco → azul
    'Cádiz':            '#f59e0b',  # amarillo
    'Mirandés':         '#dc2626',  # rojo
    'Huesca':           '#4338ca',  # azul y granate → índigo
    'Real Zaragoza':    '#1d4ed8',  # blanco y azul → azul
    'Cultural Leonesa': '#94a3b8',  # blanco → neutro
    # ── Temporadas históricas ──────────────────────────────────────────────
    'Levante':            '#1d4ed8',  # azul marino
    'Cartagena':          '#dc2626',  # rojo
    'Elche':              '#16a34a',  # verde
    'Eldense':            '#dc2626',  # rojo
    'Espanyol':           '#1d4ed8',  # azul
    'Tenerife':           '#1d4ed8',  # azul
    'Girona':             '#dc2626',  # granate
    'Mallorca':           '#dc2626',  # rojo
    'Real Oviedo':        '#1d4ed8',  # azul
    'Alavés':             '#1d4ed8',  # azul
    'Rayo Vallecano':     '#dc2626',  # rojo
    'Lugo':               '#dc2626',  # rojo
    'Ponferradina':       '#dc2626',  # rojo
    'Alcorcón':           '#f97316',  # naranja
    'Amorebieta':         '#dc2626',  # rojo
    'Ibiza':              '#1d4ed8',  # azul
    'Fuenlabrada':        '#16a34a',  # verde
    'Numancia':           '#dc2626',  # rojo
    'Racing Club Ferrol': '#dc2626',  # rojo
    'Sabadell':           '#1d4ed8',  # azul
    'UD Logroñés':        '#dc2626',  # rojo
    'Villarreal B':       '#f59e0b',  # amarillo
    'Extremadura':        '#dc2626',  # rojo
}

# Kit 2 colores: primary = borde + brillo (glow), secondary = fondo del escudo
TEAM_KIT_FULL = {
    # Equipo              primary (borde+glow)  secondary (fondo)
    'Racing':           {'primary': '#FFFFFF', 'secondary': '#006633'},  # blanco / verde
    'Almería':          {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Deportivo':        {'primary': '#1C4E97', 'secondary': '#FFFFFF'},  # azul / blanco
    'Las Palmas':       {'primary': '#F5C500', 'secondary': '#003087'},  # amarillo / azul
    'Castellón':        {'primary': '#000000', 'secondary': '#FFFFFF'},  # negro / blanco
    'Málaga':           {'primary': '#38BDF8', 'secondary': '#FFFFFF'},  # celeste / blanco
    'Burgos':           {'primary': '#000000', 'secondary': '#FFFFFF'},  # negro / blanco
    'Eibar':            {'primary': '#003366', 'secondary': '#8B0000'},  # azul marino / granate
    'Córdoba':          {'primary': '#2B7A2B', 'secondary': '#FFFFFF'},  # verde / blanco
    'Andorra':          {'primary': '#1C3C8C', 'secondary': '#F5C500'},  # azul / amarillo
    'Ceuta':            {'primary': '#000000', 'secondary': '#FFFFFF'},  # negro / blanco
    'Sporting':         {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Albacete':         {'primary': '#FFFFFF', 'secondary': '#000000'},  # blanco / negro
    'Granada':          {'primary': '#FFFFFF', 'secondary': '#CC0000'},  # blanco / rojo
    'Valladolid':       {'primary': '#6A0DAD', 'secondary': '#FFFFFF'},  # violeta / blanco
    'Leganés':          {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'Real Sociedad B':  {'primary': '#0057A8', 'secondary': '#FFFFFF'},  # azul / blanco
    'Cádiz':            {'primary': '#F5C500', 'secondary': '#003087'},  # amarillo / azul
    'Mirandés':         {'primary': '#CC0000', 'secondary': '#000000'},  # rojo / negro
    'Huesca':           {'primary': '#003087', 'secondary': '#8B1A1A'},  # azul / granate
    'Real Zaragoza':    {'primary': '#FFFFFF', 'secondary': '#003087'},  # blanco / azul
    'Cultural Leonesa': {'primary': '#FFFFFF', 'secondary': '#CC0000'},  # blanco / rojo
    # ── Temporadas históricas ──────────────────────────────────────────────
    'Levante':            {'primary': '#0033A0', 'secondary': '#CC0000'},  # azul / rojo
    'Cartagena':          {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Elche':              {'primary': '#00843D', 'secondary': '#FFFFFF'},  # verde / blanco
    'Eldense':            {'primary': '#CC0000', 'secondary': '#000000'},  # rojo / negro
    'Espanyol':           {'primary': '#003DA5', 'secondary': '#FFFFFF'},  # azul / blanco
    'Tenerife':           {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'Girona':             {'primary': '#9B1C31', 'secondary': '#FFFFFF'},  # granate / blanco
    'Mallorca':           {'primary': '#CC0000', 'secondary': '#000000'},  # rojo / negro
    'Real Oviedo':        {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'Alavés':             {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'Rayo Vallecano':     {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Lugo':               {'primary': '#CC0000', 'secondary': '#000000'},  # rojo / negro
    'Ponferradina':       {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Alcorcón':           {'primary': '#FF6600', 'secondary': '#000000'},  # naranja / negro
    'Amorebieta':         {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Ibiza':              {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'Fuenlabrada':        {'primary': '#009B3A', 'secondary': '#FFFFFF'},  # verde / blanco
    'Numancia':           {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Racing Club Ferrol': {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Sabadell':           {'primary': '#003087', 'secondary': '#FFFFFF'},  # azul / blanco
    'UD Logroñés':        {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
    'Villarreal B':       {'primary': '#F5C500', 'secondary': '#003087'},  # amarillo / azul
    'Extremadura':        {'primary': '#CC0000', 'secondary': '#FFFFFF'},  # rojo / blanco
}

# Cargar predicciones reales de BeSoccer (generadas por fetch_predictions.py)
_pred_path = os.path.join(os.path.dirname(__file__) or '.', 'predictions.json')
if os.path.exists(_pred_path):
    with open(_pred_path, 'r', encoding='utf-8') as _f:
        TEAM_PREDICTIONS = json.load(_f)
        print(f"[build] Cargando predicciones reales de {_pred_path}")
else:
    print("[build] AVISO: predictions.json no encontrado, usando datos hardcoded")

# Cargar assets adicionales de equipos históricos (generados por fetch_team_assets.py)
_assets_path = os.path.join(os.path.dirname(__file__) or '.', 'team_assets.json')
if os.path.exists(_assets_path):
    with open(_assets_path, 'r', encoding='utf-8') as _f:
        _team_assets = json.load(_f)
    _ext_badges = _team_assets.get('badges', {})
    _ext_colors = _team_assets.get('colors', {})
    # Solo añadir equipos que no estén ya hardcodeados en build.py
    for _n, _v in _ext_badges.items():
        if _n not in TEAM_BADGES:
            TEAM_BADGES[_n] = _v
    for _n, _v in _ext_colors.items():
        if _n not in TEAM_COLORS:
            TEAM_COLORS[_n] = _v
    print(f"[build] team_assets.json cargado: {len(_ext_badges)} badges, {len(_ext_colors)} colores")
else:
    print("[build] INFO: team_assets.json no encontrado — usando assets hardcodeados")

colors_js = json.dumps(TEAM_COLORS)
badges_js = json.dumps(TEAM_BADGES)
predictions_js = json.dumps(TEAM_PREDICTIONS)
besoccer_map_js = json.dumps(BESOCCER_NAME_MAP)
kit_js = json.dumps(TEAM_KIT)
kit_full_js = json.dumps(TEAM_KIT_FULL)
data_js = json.dumps(data, ensure_ascii=False)
total_rounds = data['total_rounds']

# Datos históricos de temporadas anteriores
_history_path = os.path.join(os.path.dirname(__file__), 'history_data.json')
if os.path.exists(_history_path):
    with open(_history_path, 'r', encoding='utf-8') as _f:
        _history_raw = json.load(_f)
    # Embeber todos los datos necesarios para switchSeason completo
    _history_lite = {'seasons': {}}
    _HIST_KEYS = ['label','total_rounds','total_season_rounds','teams','final_standings',
                  'results_by_team','scores_by_team','opponents_by_team','venue_by_team',
                  'playoff']
    for _label, _sdata in _history_raw.get('seasons', {}).items():
        _history_lite['seasons'][_label] = {k: _sdata[k] for k in _HIST_KEYS if k in _sdata}
    history_js = json.dumps(_history_lite, ensure_ascii=False)
    # Opciones HTML para el selector de temporada (ordenadas más reciente primero)
    _hist_labels_sorted = sorted(_history_lite['seasons'].keys(), reverse=True)
    season_options_html = '\n'.join(
        f'<option value="{_lbl}">{_lbl}</option>'
        for _lbl in _hist_labels_sorted
    )
    print(f"[build] Historial cargado: {_hist_labels_sorted}")
else:
    history_js = '{"seasons":{}}'
    season_options_html = ''
    print("[build] AVISO: history_data.json no encontrado")

# Marcadores históricos (generados por fetch_scores.py)
_scores_path = os.path.join(os.path.dirname(__file__), 'scores_data.json')
if os.path.exists(_scores_path):
    with open(_scores_path, 'r', encoding='utf-8') as _f:
        _scores_raw = json.load(_f)
    scores_js = json.dumps(_scores_raw, ensure_ascii=False)
    # Recalcular TEAM_EXTRA_STATS dinámicamente desde scores_data.json
    _sc_map = _scores_raw.get('scores_by_team', {})
    _vn_map = _scores_raw.get('venue_by_team', {})
    _computed = {}
    for _t in data['teams']:
        _sc = _sc_map.get(_t, {})
        _vn = _vn_map.get(_t, {})
        _gf=_gc=_hp=_hpj=_hpg=_hpe=_hpp=_hgf=_hgc=_ap=_apj=_apg=_ape=_app=_agf=_agc=0
        for _k, _s in _sc.items():
            try: _tg, _og = map(int, _s.split('-'))
            except: continue
            _gf+=_tg; _gc+=_og
            _ven = _vn.get(str(_k), '')
            if _ven == 'H':
                _hpj+=1; _hgf+=_tg; _hgc+=_og
                if _tg>_og: _hpg+=1; _hp+=3
                elif _tg==_og: _hpe+=1; _hp+=1
                else: _hpp+=1
            elif _ven == 'A':
                _apj+=1; _agf+=_tg; _agc+=_og
                if _tg>_og: _apg+=1; _ap+=3
                elif _tg==_og: _ape+=1; _ap+=1
                else: _app+=1
        _computed[_t] = {
            'gf':_gf,'gc':_gc,
            'home_pts':_hp,'home_pj':_hpj,'home_pg':_hpg,'home_pe':_hpe,'home_pp':_hpp,'home_gf':_hgf,'home_gc':_hgc,
            'away_pts':_ap,'away_pj':_apj,'away_pg':_apg,'away_pe':_ape,'away_pp':_app,'away_gf':_agf,'away_gc':_agc,
        }
    if _computed:
        TEAM_EXTRA_STATS = _computed
        print(f'[build] TEAM_EXTRA_STATS recalculado dinámicamente ({len(_computed)} equipos)')
else:
    scores_js = '{"scores_by_team":{}}'
    print('  ⚠ scores_data.json no encontrado – ejecuta fetch_all.py')
extra_js = json.dumps(TEAM_EXTRA_STATS)

# Predicciones históricas jornada a jornada (generadas por fetch_predictions_history.py)
_preds_hist_path = os.path.join(os.path.dirname(__file__), 'predictions_history.json')
if os.path.exists(_preds_hist_path):
    with open(_preds_hist_path, 'r', encoding='utf-8') as _f:
        pred_hist_js = json.dumps(json.load(_f), ensure_ascii=False)
else:
    pred_hist_js = '{}'
    print('  ⚠ predictions_history.json no encontrado – ejecuta fetch_predictions_history.py')

# Estadísticas avanzadas de partidos (generadas por fetch_as.py desde AS.com / Opta)
_as_stats_path = os.path.join(os.path.dirname(__file__), 'as_stats.json')
if os.path.exists(_as_stats_path):
    with open(_as_stats_path, 'r', encoding='utf-8') as _f:
        _as_raw = json.load(_f)
    as_stats_js = json.dumps(_as_raw, ensure_ascii=False)
    print(f"[build] as_stats.json cargado: {len(_as_raw)} partidos")
else:
    as_stats_js = '[]'
    print('[build] INFO: as_stats.json no encontrado — ejecuta fetch_as.py')

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚡ Liga Hypertensiones 25/26</title>
<link rel="icon" type="image/png" href="logo.png">
<link rel="apple-touch-icon" href="logo.png">
<link rel="preconnect" href="https://cdn.resfu.com" crossorigin>
<link rel="dns-prefetch" href="https://cdn.resfu.com">
<meta name="description" content="Clasificación, estadísticas y análisis de la Liga Hypertensiones 25/26">
<meta property="og:title" content="⚡ Liga Hypertensiones 25/26">
<meta property="og:description" content="Clasificación, estadísticas y análisis de la Liga Hypertensiones 25/26">
<meta property="og:image" content="https://hypertensiones.alejandrobeltran.es/logo.png">
<meta property="og:url" content="https://hypertensiones.alejandrobeltran.es/">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://hypertensiones.alejandrobeltran.es/logo.png">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
/* ===== RESET & BASE ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg:        #0a0a0a;
  --bg2:       #141414;
  --card:      #1e1e1e;
  --card2:     #2a2a2a;
  --border:    #3d3d3d;
  --accent:    #e0e0e0;
  --accent2:   #999999;
  --text:      #f0f0f0;
  --muted:     #9a9a9a;
  --win:       #22c55e;
  --draw:      #f59e0b;
  --loss:      #ef4444;
  --gold:      #fbbf24;
  --silver:    #b0b0b0;
  --bronze:    #8a6a3a;
  --zone1:     rgba(34,197,94,.15);
  --zone2:     rgba(250,204,21,.10);
  --zone3:     rgba(239,68,68,.13);
  --radius:    10px;
  --shadow:    0 4px 24px rgba(0,0,0,.7);
}}
html {{ scroll-behavior: smooth; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 14px;
  min-height: 100vh;
}}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg2); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

/* ===== TOPBAR ===== */
header {{
  background: linear-gradient(135deg, #0a0a0a 0%, #1e1e1e 100%);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow);
}}
.header-inner {{
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}}
.header-top {{
  display: flex;
  align-items: center;
  gap: 0px;
  padding: 0 24px;
  height: 130px;
}}
.logo {{
  flex-shrink: 0;
  display: flex;
  align-items: center;
  margin: 0 16px 0 0;
}}
.logo img {{
  padding-top: 0;
  width: 250px;
  height: auto;
  filter: drop-shadow(0 0 12px rgba(57,255,20,.7));
  pointer-events: none;
}}
header h1 {{
  display: none;
}}
.header-meta {{
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  padding-left: 20px;
  border-left: 1px solid var(--border);
}}
.rounds-badge {{
  flex-shrink: 0;
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  color: var(--muted);
  white-space: nowrap;
}}
/* ===== SEASON SELECTOR ===== */
.season-select-wrap {{
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 7px;
  margin-left: 8px;
}}
.season-select-wrap label {{
  font-size: 10px;
  color: var(--muted);
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: .05em;
}}
.season-select {{
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  cursor: pointer;
  outline: none;
  transition: border-color .2s;
  min-width: 90px;
}}
.season-select:focus, .season-select:hover {{
  border-color: var(--accent);
}}
/* ===== NEXT-MATCH (inline en header-meta) ===== */
#nextMatchBanner {{
  display: none;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--muted);
}}
.nm-dot {{
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #39ff14;
  flex-shrink: 0;
  animation: nmPulse 2s ease-in-out infinite;
}}
@keyframes nmPulse {{
  0%,100% {{ opacity:1; transform:scale(1); }}
  50% {{ opacity:.35; transform:scale(.65); }}
}}
.nm-label {{
  color: #39ff14;
  font-weight: 700;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  flex-shrink: 0;
}}
.nm-teams {{
  font-weight: 600;
  color: var(--text);
  flex-shrink: 0;
}}
.nm-sep {{ color: var(--border); flex-shrink: 0; }}
.nm-countdown {{
  font-weight: 700;
  color: #39ff14;
  font-variant-numeric: tabular-nums;
  letter-spacing: .5px;
  flex-shrink: 0;
}}

/* ===== TABS ===== */
nav {{
  background: rgba(0,0,0,.3);
  border-top: 1px solid var(--border);
  display: flex;
  gap: 2px;
  padding: 0 16px;
  overflow-x: auto;
  scrollbar-width: none;
}}
nav::-webkit-scrollbar {{ display: none; }}
nav button {{
  background: none;
  border: none;
  color: var(--muted);
  padding: 14px 20px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  border-bottom: 2px solid transparent;
  transition: all .2s;
  display: flex;
  align-items: center;
  gap: 6px;
}}
nav button:hover {{ color: var(--text); background: rgba(255,255,255,.04); }}
nav button.active {{ color: var(--accent); border-bottom-color: var(--accent); }}

/* ===== HAMBURGER BUTTON ===== */
.hamburger-btn {{
  display: none;
  background: none;
  border: 1px solid var(--border);
  color: var(--text);
  width: 38px; height: 38px;
  border-radius: 8px;
  cursor: pointer;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 0;
  flex-shrink: 0;
  transition: border-color .2s;
}}
.hamburger-btn:hover {{ border-color: var(--accent); }}
.hamburger-btn span {{
  display: block;
  width: 18px; height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: all .25s;
}}
.hamburger-btn.open span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.hamburger-btn.open span:nth-child(2) {{ opacity: 0; transform: scaleX(0); }}
.hamburger-btn.open span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

/* ===== MOBILE RESPONSIVE ===== */
@media (max-width: 889px) {{
  .hamburger-btn {{ display: flex; position: absolute; top: 12px; right: 16px; }}
  header {{ position: sticky; }}
  .header-top {{
    flex-direction: column;
    align-items: center;
    height: auto;
    padding: 12px 16px 0;
    position: relative;
    gap: 0;
  }}
  .logo {{
    margin: 0;
    justify-content: center;
    height: 100px;
  }}
  .logo img {{
    width: 280px;
    padding-top: 0;
    align-items: center;
  }}
  .header-meta {{
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--border);
    padding-left: 0;
    padding-top: 10px;
    padding-bottom: 2px;
    align-items: center;
    text-align: center;
  }}
  #nextMatchBanner {{ justify-content: center; flex-wrap: wrap; gap: 5px; }}
  .status-bar {{ justify-content: center; }}
  .rounds-badge {{ display: none; }}
  nav {{
    display: none;
    flex-direction: column;
    padding: 4px 0;
    border-top: 1px solid var(--border);
  }}
  nav.nav-open {{ display: flex; }}
  nav button {{
    padding: 13px 20px;
    border-bottom: none;
    border-left: 3px solid transparent;
    justify-content: flex-start;
  }}
  nav button.active {{
    border-bottom-color: transparent;
    border-left-color: var(--accent);
    background: rgba(0,212,255,.05);
  }}
  main {{ padding: 0 7px 0 10px; }}
  /* Forma label: salto de línea antes de los botones de forma */
  .forma-label {{ flex-basis: 100%; margin-left: 0 !important; }}
  /* Análisis: scatter + rankings en columna, ancho completo */
  .analisis-top-grid {{ grid-template-columns: 1fr; }}

  /* ===== TABLA CLASIFICACIÓN MOBILE ===== */
  /* Full-bleed: el wrapper sobresale del padding del card */
  .standings-wrapper {{
    margin: 0 -20px;
    padding-bottom: 4px;
    -webkit-overflow-scrolling: touch;
  }}
  /* Sticky columnas 1 (#) y 2 (Equipo) */
  .standings-table th:nth-child(1),
  .standings-table td:nth-child(1) {{
    position: sticky;
    left: 0;
    z-index: 2;
    background: var(--card2);
  }}
  .standings-table td:nth-child(1) {{ background: var(--card); }}
  .standings-table th:nth-child(2),
  .standings-table td:nth-child(2) {{
    position: sticky;
    left: 35px;
    z-index: 2;
    background: var(--card2);
    box-shadow: 2px 0 6px rgba(0,0,0,.4);
    min-width: 110px;
  }}
  .standings-table td:nth-child(2) {{
    background: var(--card);
    box-shadow: 2px 0 6px rgba(0,0,0,.4);
  }}
  /* Reducir fuente y padding en móvil SOLO en clasificación */
  #standingsTable {{ font-size: 12px; }}
  #standingsTable th, #standingsTable td {{ padding: 8px 9px; }}
  #standingsTable th:nth-child(1), #standingsTable td:nth-child(1) {{ padding-left: 10px; }}
  /* Ajuste columna Puntos en móvil */
  #standingsTable th:nth-child(11) {{ min-width: 120px; }}

  /* ===== H2H MATRIX MOBILE ===== */
  /* Full-bleed */
  #h2hGrid > div:last-child {{ margin: 0 -20px; }}
  /* Celdas más pequeñas */
  .h2h-matrix {{ font-size: 7px !important; }}
  .h2h-matrix td, .h2h-matrix th {{
    width: 18px !important;
    min-width: 18px !important;
    height: 16px !important;
  }}
  .h2h-matrix thead tr th:first-child {{
    min-width: 70px !important;
    font-size: 8px !important;
  }}
  .h2h-matrix tbody tr td:first-child {{
    font-size: 8px !important;
    padding-right: 4px !important;
    min-width: 70px;
    max-width: 70px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}
  .h2h-matrix thead tr th:not(:first-child) img {{
    width: 14px !important;
    height: 14px !important;
  }}
}}

/* ===== MAIN CONTENT ===== */
main {{ padding: 24px; max-width: 1400px; margin: 0 auto; }}
.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; animation: fadeIn .25s ease; }}
@keyframes fadeIn {{ from {{ opacity:0; transform: translateY(8px); }} to {{ opacity:1; transform: translateY(0); }} }}

/* ===== CARDS ===== */
.card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
}}
.card-title {{
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.card-legend {{
  margin-top: 14px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  font-size: 10px;
  color: var(--muted);
  line-height: 1.7;
  opacity: .75;
}}
.card-legend b {{ color: var(--text); opacity: .6; font-weight: 600; }}

/* Grid análisis superior: scatter + rankings */
.analisis-top-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: start;
}}
/* Los hijos del grid nunca se salen del contenedor */
.analisis-top-grid > *,
.analisis-bottom-grid > * {{
  min-width: 0;
  max-width: 100%;
}}

/* Grid análisis inferior: radar + consistencia 50/50 */
.analisis-bottom-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: start;
}}

/* Breakpoint 1100px: grids análisis en columna */
@media (max-width: 1100px) {{
  .analisis-top-grid,
  .analisis-bottom-grid {{ grid-template-columns: 1fr; }}
}}

/* Layout interno del radar: lista equipo izquierda + chart derecha */
.radar-layout {{
  display: flex;
  gap: 14px;
  align-items: flex-start;
}}
.radar-team-list {{
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 120px;
  max-width: 140px;
  max-height: 360px;
  overflow-y: auto;
  flex-shrink: 0;
  scrollbar-width: thin;
  scrollbar-color: var(--border) transparent;
}}
.radar-team-list .radar-team-btn {{
  justify-content: flex-start;
  width: 100%;
  border-radius: 6px;
  padding: 4px 8px;
}}
@media (max-width: 889px) {{
  .radar-layout {{ flex-direction: column; }}
  .radar-team-list {{ flex-direction: row; flex-wrap: wrap; max-width: 100%; max-height: none; min-width: 0; }}
}}

/* ===== RADAR TEAM SELECTOR ===== */
.radar-team-btn {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--card2);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  cursor: pointer;
  transition: all .15s;
  white-space: nowrap;
}}
.radar-team-btn:hover {{ border-color: var(--accent); color: var(--text); }}
.radar-team-btn.active {{ color: #0a0a0a; border-color: transparent; }}


.standings-wrapper {{
  overflow-x: auto;
}}
.standings-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}}
.standings-table th {{
  background: var(--card2);
  color: var(--muted);
  font-weight: 600;
  padding: 10px 12px;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-bottom: 1px solid var(--border);
  user-select: none;
  transition: background .2s;
}}
.standings-table th:hover {{ background: #3d3d3d; color: var(--text); }}
.standings-table th:first-child {{ text-align: left; padding-left: 16px; }}
.standings-table th:nth-child(2) {{ text-align: left; }}
.standings-table td {{
  padding: 9px 12px;
  text-align: center;
  border-bottom: 1px solid rgba(45,63,95,.4);
  vertical-align: middle;
}}
.standings-table td:first-child {{ text-align: left; padding-left: 16px; }}
.standings-table td:nth-child(2) {{ text-align: left; min-width: 140px; }}
.standings-table tr:hover td {{ background: rgba(255,255,255,.03); }}

/* Zone colors */
.zone-promotion td:first-child {{ border-left: 3px solid #22c55e; }}
.zone-playoff td:first-child {{ border-left: 3px solid #fbbf24; }}
.zone-relegation td:first-child {{ border-left: 3px solid #ef4444; }}
.zone-promotion {{ background: var(--zone1); }}
.zone-playoff {{ background: var(--zone2); }}
.zone-relegation {{ background: var(--zone3); }}
/* Posición matemáticamente asegurada (anula el borde de zona) */
tr.secured-promotion td:first-child  {{ border-left: 5px solid #4ade80 !important; box-shadow: inset 4px 0 14px rgba(74,222,128,.18); }}
tr.secured-playoff td:first-child    {{ border-left: 5px solid #fbbf24 !important; box-shadow: inset 4px 0 14px rgba(251,191,36,.18); }}
tr.secured-permanence td:first-child {{ border-left: 5px solid #94a3b8 !important; }}
tr.secured-relegation td:first-child {{ border-left: 5px solid #ef4444 !important; box-shadow: inset 4px 0 14px rgba(239,68,68,.18); }}

/* Position badge */
.pos-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  font-weight: 700;
  font-size: 12px;
}}
.pos-1 {{ background: var(--gold); color: #000; }}
.pos-2 {{ background: var(--silver); color: #000; }}
.pos-3 {{ background: var(--bronze); color: #fff; }}
.pos-default {{ background: var(--card2); color: var(--muted); }}

/* Team crest */
.team-cell {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.team-crest {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  overflow: hidden;
}}
.team-crest img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}}
.team-name-text {{
  font-weight: 500;
}}

/* Points bar */
.pts-bar-cell {{
  display: flex;
  align-items: center;
  gap: 8px;
}}
.pts-value {{
  font-weight: 700;
  font-size: 15px;
  color: var(--accent);
  min-width: 28px;
  text-align: right;
}}
.pts-bar {{
  flex: 1;
  height: 10px;
  background: var(--card2);
  border-radius: 5px;
  min-width: 60px;
}}
.pts-fill {{
  height: 100%;
  border-radius: 5px;
  transition: width .6s ease;
}}

/* Form dots */
.form-cell {{ display: flex; gap: 3px; justify-content: center; }}
.form-dot {{
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 700;
  color: #fff;
}}
.form-V {{ background: var(--win); }}
.form-E {{ background: var(--draw); color: #000; }}
.form-D {{ background: var(--loss); }}

/* ===== CHART SECTION ===== */
.chart-controls {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}}
.chart-controls button {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all .2s;
}}
.chart-controls button:hover,
.chart-controls button.active {{
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(255,255,255,.05);
}}
.chart-container {{
  position: relative;
  width: 100%;
  height: 480px;
  margin-top: 8px;
}}
.chart-tabs {{
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}}
.chart-tab {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 8px 18px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all .2s;
}}
.chart-tab.active {{
  background: var(--accent);
  color: #000;
  font-weight: 700;
  border-color: var(--accent);
}}
/* Select rankings */
#rankingSelect {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
  margin-bottom: 10px;
  width: 100%;
  appearance: auto;
}}
#rankingSelect:focus {{ outline: none; border-color: var(--accent); }}
#rankingSelect option {{ background: var(--card2); color: var(--text); }}
.team-selector {{
  max-height: 160px;
  overflow-y: auto;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 10px;
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 16px;
}}
.team-check-badge {{
  cursor: pointer;
  border-radius: 6px;
  padding: 4px;
  border: 2px solid transparent;
  transition: border-color .15s, background .15s;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}}
.team-check-badge:hover {{ background: rgba(255,255,255,.08); }}
.team-check-badge.badge-sel {{ border-color: var(--accent); background: rgba(255,255,255,.06); }}
.team-check-badge input {{ display:none; }}
.team-check-badge img {{ width:32px; height:32px; object-fit:contain; display:block; }}
#analisisTeamSelector {{ overflow:hidden; justify-content:center; }}
#analisisTeamSelector .team-check-badge {{ padding:2px; border-radius:5px; }}
#analisisTeamSelector .team-check-badge img {{ width:22px; height:22px; }}
.team-color-dot {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}}

/* ===== RESULTS SECTION ===== */
.round-selector {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}}
.round-selector label {{ color: var(--muted); font-size: 13px; }}
.round-input {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  width: 80px;
  text-align: center;
}}
.round-btn {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--text);
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all .2s;
}}
.round-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
.round-btn:disabled {{ opacity: 0.3; cursor: not-allowed; }}

.hist-sort-btn {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  transition: all .2s;
}}
.hist-sort-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
.hist-sort-btn.active {{ background: rgba(0,212,255,.12); border-color: var(--accent); color: var(--accent); }}

.results-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}}
.result-card {{
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all .2s;
}}
.result-card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
.result-badge-V {{ background: rgba(34,197,94,.15); border-left: 3px solid var(--win); }}
.result-badge-E {{ background: rgba(245,158,11,.1); border-left: 3px solid var(--draw); }}
.result-badge-D {{ background: rgba(239,68,68,.1); border-left: 3px solid var(--loss); }}
@keyframes neon-pulse-V {{ 0%,100% {{ box-shadow: 0 0 6px 2px rgba(34,197,94,.4); border-color: rgba(34,197,94,.5); }} 50% {{ box-shadow: 0 0 18px 6px rgba(34,197,94,.9); border-color: #22c55e; }} }}
@keyframes neon-pulse-E {{ 0%,100% {{ box-shadow: 0 0 6px 2px rgba(251,191,36,.4); border-color: rgba(251,191,36,.5); }} 50% {{ box-shadow: 0 0 18px 6px rgba(251,191,36,.9); border-color: #fbbf24; }} }}
@keyframes neon-pulse-D {{ 0%,100% {{ box-shadow: 0 0 6px 2px rgba(239,68,68,.4); border-color: rgba(239,68,68,.5); }} 50% {{ box-shadow: 0 0 18px 6px rgba(239,68,68,.9); border-color: #ef4444; }} }}
.live-V {{ border: 2px solid #22c55e !important; animation: neon-pulse-V 1.2s ease-in-out infinite; }}
.live-E {{ border: 2px solid #fbbf24 !important; animation: neon-pulse-E 1.2s ease-in-out infinite; }}
.live-D {{ border: 2px solid #ef4444 !important; animation: neon-pulse-D 1.2s ease-in-out infinite; }}
.result-letter {{
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}}
.result-letter-V {{ background: var(--win); color: #fff; }}
.result-letter-E {{ background: var(--draw); color: #000; }}
.result-letter-D {{ background: var(--loss); color: #fff; }}
.result-team {{ font-weight: 500; font-size: 13px; }}
.result-detail {{ font-size: 11px; color: var(--muted); }}

/* Full history grid */
.history-grid-wrapper {{ overflow-x: auto; margin-top: 12px; }}
.history-table {{ border-collapse: collapse; font-size: 11px; }}
.history-table th {{
  background: var(--card2);
  padding: 6px 8px;
  color: var(--muted);
  text-align: center;
  border: 1px solid var(--border);
  white-space: nowrap;
  font-weight: 600;
  position: sticky;
  top: 0;
}}
.history-table th:first-child {{
  text-align: left;
  min-width: 130px;
  position: sticky;
  left: 0;
  z-index: 2;
  background: var(--card2);
}}
.history-table td {{
  padding: 5px 7px;
  text-align: center;
  border: 1px solid rgba(45,63,95,.3);
}}
.history-table td:first-child {{
  text-align: left;
  background: var(--card);
  position: sticky;
  left: 0;
  font-weight: 500;
}}
.cell-V {{ background: rgba(34,197,94,.22); border: 1px solid rgba(34,197,94,.55) !important; box-shadow: inset 0 0 6px rgba(34,197,94,.28); }}
.cell-E {{ background: rgba(245,158,11,.18); border: 1px solid rgba(245,158,11,.5) !important; box-shadow: inset 0 0 6px rgba(245,158,11,.25); }}
.cell-D {{ background: rgba(239,68,68,.18); border: 1px solid rgba(239,68,68,.5) !important; box-shadow: inset 0 0 6px rgba(239,68,68,.25); }}
.cell-empty {{ background: rgba(255,255,255,.02); color: var(--muted); }}
.cell-V img, .cell-E img, .cell-D img {{ width:18px;height:18px;object-fit:contain;vertical-align:middle;display:block;margin:auto; }}
.cell-future {{ background: rgba(255,255,255,.02); cursor: default; opacity:.5; }}
.cell-future img {{ width:14px;height:14px;object-fit:contain;display:block;margin:auto;opacity:.35; }}

/* ===== HEARTBEAT LIVE GLOW ===== */
@keyframes beatGreen {{
  0%,100% {{ filter: drop-shadow(0 0 2px rgba(34,197,94,.3)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
  50% {{ filter: drop-shadow(0 0 12px rgba(34,197,94,.9)) drop-shadow(0 0 5px rgba(34,197,94,.6)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
}}
@keyframes beatYellow {{
  0%,100% {{ filter: drop-shadow(0 0 2px rgba(245,158,11,.3)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
  50% {{ filter: drop-shadow(0 0 12px rgba(245,158,11,.9)) drop-shadow(0 0 5px rgba(245,158,11,.6)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
}}
@keyframes beatRed {{
  0%,100% {{ filter: drop-shadow(0 0 2px rgba(239,68,68,.3)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
  50% {{ filter: drop-shadow(0 0 12px rgba(239,68,68,.9)) drop-shadow(0 0 5px rgba(239,68,68,.6)) drop-shadow(0 0 1px rgba(0,0,0,.7)); }}
}}
.team-crest.crest-live-win img  {{ animation: beatGreen  1.3s ease-in-out infinite; }}
.team-crest.crest-live-draw img {{ animation: beatYellow 1.3s ease-in-out infinite; }}
.team-crest.crest-live-lose img {{ animation: beatRed    1.3s ease-in-out infinite; }}

/* ===== LIVE MATCH BAR ===== */
.live-bar {{
  background: var(--card2);
  border-bottom: 1px solid var(--border);
  padding: 5px 16px;
  display: none;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  font-size: 12px;
}}
.live-bar.has-live {{ display: flex; }}
/* H2H cross-highlight */
.h2h-matrix td, .h2h-matrix th {{ transition: opacity 0.1s; }}
.h2h-matrix.h2h-hov td:not(.h2h-cross),
.h2h-matrix.h2h-hov th:not(.h2h-cross) {{ opacity: 0.12; }}
.live-match-pill {{
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}}
.live-score-pill {{
  background: rgba(239,68,68,.15);
  color: var(--loss);
  border-radius: 4px;
  padding: 1px 5px;
  font-weight: 700;
  font-size: 12px;
  min-width: 32px;
  text-align: center;
}}

/* ===== STANDINGS ROUND NAV ===== */
.standings-round-nav {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0 14px;
  flex-wrap: wrap;
}}
.standings-round-nav label {{ color: var(--muted); font-size: 12px; }}
.standings-round-nav .round-btn {{ width:28px; height:28px; font-size:14px; }}
.standings-round-nav .round-label {{
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  min-width: 120px;
  text-align: center;
}}
.standings-round-nav .btn-latest {{
  font-size: 11px;
  padding: 4px 10px;
  background: rgba(0,212,255,.1);
  border: 1px solid rgba(0,212,255,.3);
  color: var(--accent);
  border-radius: 6px;
  cursor: pointer;
}}
.standings-round-nav .btn-latest:hover {{ background: rgba(0,212,255,.18); }}
.pred-mini-bar {{
  display: flex;
  width: 72px;
  height: 3px;
  border-radius: 2px;
  overflow: hidden;
  margin-top: 3px;
}}
.live-dot-indicator {{
  display: inline-block;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 1s infinite;
  margin-right: 3px;
  vertical-align: middle;
}}

/* ===== LIVE SECTION ===== */
.live-header {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}}
.live-badge {{
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(239,68,68,.15);
  border: 1px solid rgba(239,68,68,.4);
  color: #ef4444;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}}
.live-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 1.5s infinite;
}}
@keyframes pulse {{ 0%,100% {{ opacity:1; transform:scale(1); }} 50% {{ opacity:.5; transform:scale(1.3); }} }}
.live-matches-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}}
.live-match-card {{
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  position: relative;
}}
.live-match-card.is-live {{
  border-color: rgba(239,68,68,.5);
  box-shadow: 0 0 16px rgba(239,68,68,.15);
}}
.live-match-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}}
.live-round-label {{
  font-size: 11px;
  color: var(--muted);
  background: var(--card);
  padding: 2px 8px;
  border-radius: 4px;
}}
.live-status-badge {{
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}}
.status-live {{ background: rgba(239,68,68,.2); color: #ef4444; }}
.status-finished {{ background: rgba(34,197,94,.15); color: var(--win); }}
.live-match-body {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}}
.live-team {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}}
.live-team.away {{ flex-direction: row-reverse; text-align: right; }}
.live-team-name {{ font-weight: 600; font-size: 13px; }}
.live-score {{
  font-size: 22px;
  font-weight: 700;
  color: var(--accent);
  text-align: center;
  min-width: 60px;
  background: var(--card);
  padding: 6px 12px;
  border-radius: 8px;
  letter-spacing: 2px;
}}
.live-actions {{
  display: flex;
  gap: 8px;
  margin-top: 12px;
}}
.btn {{
  padding: 7px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all .2s;
}}
.btn-primary {{ background: var(--accent); color: #000; }}
.btn-primary:hover {{ background: #00b8d9; transform: translateY(-1px); }}
.btn-danger {{ background: rgba(239,68,68,.15); color: #ef4444; border: 1px solid rgba(239,68,68,.4); }}
.btn-danger:hover {{ background: rgba(239,68,68,.25); }}
.btn-secondary {{ background: var(--card2); color: var(--text); border: 1px solid var(--border); }}
.btn-secondary:hover {{ border-color: var(--accent); color: var(--accent); }}

/* Add match form */
.add-match-form {{
  background: var(--card2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 24px;
}}
.form-row {{
  display: grid;
  grid-template-columns: 1fr auto 1fr auto auto auto;
  gap: 12px;
  align-items: end;
  flex-wrap: wrap;
}}
.form-group {{ display: flex; flex-direction: column; gap: 4px; }}
.form-group label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .5px; }}
.form-select, .form-input {{
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  transition: border-color .2s;
}}
.form-select:focus, .form-input:focus {{ border-color: var(--accent); }}
.score-sep {{ font-size: 20px; font-weight: 700; color: var(--muted); padding-bottom: 8px; align-self: end; }}
.score-input {{ width: 56px; text-align: center; }}

/* ===== TEAMS SECTION ===== */
.teams-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}}
.team-card {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform .2s, box-shadow .2s;
  cursor: pointer;
}}
.team-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 32px rgba(0,0,0,.5);
}}
.team-card-header {{
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  position: relative;
}}
.team-crest-large {{
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  overflow: hidden;
  border: 3px solid var(--crest-primary, rgba(255,255,255,.2));
  position: relative;
  box-shadow: 0 0 16px var(--crest-primary, rgba(255,255,255,.1))44;
}}
.team-crest-large img {{ width:100%; height:100%; object-fit:contain; border-radius:50%; }}

.team-card-name {{ font-weight: 700; font-size: 15px; text-align: center; }}
.team-card-body {{ padding: 0 16px 16px; }}
.team-stats-row {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-top: 4px;
}}
.team-stat {{
  background: var(--card2);
  border-radius: 6px;
  padding: 8px 4px;
  text-align: center;
}}
.team-stat-val {{ font-size: 18px; font-weight: 700; }}
.team-stat-lbl {{ font-size: 10px; color: var(--muted); }}
.team-form-mini {{ display: flex; gap: 3px; justify-content: center; margin-top: 10px; }}
.team-pos-badge {{
  position: absolute;
  top: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--card2);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
}}
.team-pos-top {{ background: var(--gold); color: #000; border-color: var(--gold); }}


/* ===== MODAL ===== */
.modal-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.7);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s;
}}
.modal-overlay.open {{ opacity: 1; pointer-events: all; }}
.modal {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow);
  transform: scale(.96);
  transition: transform .2s;
}}
.modal-overlay.open .modal {{ transform: scale(1); }}
.modal-title {{ font-size: 17px; font-weight: 700; margin-bottom: 20px; }}
.modal-close {{
  float: right;
  background: none;
  border: none;
  color: var(--muted);
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
}}

/* ===== ZONE LEGEND ===== */
.zone-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}}
.zone-item {{ display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); }}
.zone-dot {{ width: 10px; height: 10px; border-radius: 2px; }}

/* ===== GRID 2 col ===== */
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
@media (max-width: 768px) {{ .grid-2 {{ grid-template-columns: 1fr; }} .form-row {{ grid-template-columns: 1fr 1fr; }} }}

/* ===== UTILITY ===== */
.mt-20 {{ margin-top: 20px; }}
.gap-section {{ display: flex; flex-direction: column; gap: 20px; }}

/* ===== H2H ===== */
#h2hGrid table {{ border-collapse: collapse; }}
#h2hGrid td {{ border: 1px solid #0a0a0a; }}
/* Primera columna sticky en la matriz H2H */
.h2h-matrix thead tr th:first-child,
.h2h-matrix tbody tr td:first-child {{
  position: sticky;
  left: 0;
  z-index: 3;
  background: var(--card);
  box-shadow: 2px 0 6px rgba(0,0,0,.5);
}}

/* ===== STATUS BAR (inline en header-meta) ===== */
.status-bar {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  color: var(--muted);
  flex-wrap: wrap;
}}
.status-text {{ display: flex; align-items: center; gap: 8px; }}
.pulse-dot {{
  display: inline-block;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #ef4444;
  animation: pulse 1.2s infinite;
  flex-shrink: 0;
}}
@keyframes pulse {{ 0%,100%{{ opacity:1; transform:scale(1); }} 50%{{ opacity:.4; transform:scale(.8); }} }}
.refresh-btn {{
  background: none;
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 3px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  white-space: nowrap;
  transition: color .15s, border-color .15s;
}}
.refresh-btn:hover {{ color: var(--text); border-color: var(--accent); }}

/* ===== PREDICCIONES ===== */
.pred-row {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 0;
  border-bottom: 1px solid var(--border);
}}
.pred-row:last-child {{ border-bottom: none; }}
.pred-team {{
  display: flex;
  align-items: center;
  gap: 7px;
  flex: 0 0 200px;
  min-width: 0;
}}
.pred-team-name {{
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.pred-bars {{
  flex: 1;
  display: flex;
  height: 22px;
  border-radius: 4px;
  overflow: hidden;
  min-width: 0;
}}
.pred-seg {{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  transition: flex .4s;
  overflow: hidden;
  white-space: nowrap;
}}
.pred-pos {{
  text-align: right;
  font-size: 12px;
  color: var(--muted);
  flex-shrink: 0;
  width: 28px;
}}
.pred-legend {{
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 18px;
  font-size: 12px;
  color: var(--muted);
}}
.pred-legend-item {{ display: flex; align-items: center; gap: 6px; }}
.pred-legend-dot {{ width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }}
.zone-badge-sm {{
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}}
@media (max-width: 600px) {{
  .pred-team {{ flex: 0 0 140px; }}
  .pred-team-name {{ font-size: 11px; }}
}}
/* ===== SITUACION BADGE ===== */
.situ-badge {{
  display: inline-block;
  padding: 2px 7px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: .3px;
}}
.situ-ascenso   {{ background: rgba(34,197,94,.2);  color: #4ade80; }}
.situ-playoff   {{ background: rgba(251,191,36,.18); color: #fbbf24; }}
.situ-salvacion {{ background: rgba(239,68,68,.2);  color: #f87171; }}
.situ-permanencia {{ background: rgba(100,116,139,.2); color: #94a3b8; }}
.quedan-badge {{
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  white-space: nowrap;
}}
.quedan-asegurado {{
  font-size: 11px;
  font-weight: 700;
  color: #4ade80;
  background: rgba(34,197,94,.15);
  border: 1px solid rgba(34,197,94,.35);
  border-radius: 10px;
  padding: 2px 8px;
  white-space: nowrap;
}}
.quedan-ascenso {{
  font-size: 11px;
  font-weight: 700;
  color: #fbbf24;
  background: rgba(251,191,36,.12);
  border: 1px solid rgba(251,191,36,.35);
  border-radius: 10px;
  padding: 2px 8px;
  white-space: nowrap;
}}
/* Kit-color row tinting */
.standings-table tbody tr {{ transition: background .15s; }}
.standings-table tbody tr:hover {{ filter: brightness(1.1); }}
/* ===== FORM MODE BUTTONS ===== */
.btn-form {{
  background: var(--card2);
  border: 1px solid var(--border);
  color: var(--muted);
  border-radius: 6px;
  padding: 3px 9px;
  font-size: 11px;
  cursor: pointer;
  transition: all .2s;
  white-space: nowrap;
}}
.btn-form.active {{ background: var(--accent); color: #000; border-color: var(--accent); font-weight: 700; }}

/* ===== CREST GLOW ===== */
.team-crest img {{
  filter: drop-shadow(0 0 5px var(--crest-glow, rgba(255,255,255,.15)))
          drop-shadow(0 0 1px rgba(0,0,0,.7));
}}

/* ===== PLAYOFF BRACKET ===== */
.playoff-bracket {{
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  align-items: start;
  margin-bottom: 24px;
}}
.playoff-column {{ display: flex; flex-direction: column; gap: 16px; }}
.playoff-connector {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 20px;
  gap: 8px;
  color: var(--muted);
  font-size: 22px;
}}
.playoff-tie {{
  background: var(--card2);
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,.08);
}}
.playoff-tie-header {{
  padding: 6px 12px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .6px;
  color: var(--muted);
  background: rgba(255,255,255,.03);
  border-bottom: 1px solid rgba(255,255,255,.06);
}}
.playoff-match {{
  display: flex;
  align-items: center;
  padding: 8px 12px;
  gap: 8px;
  border-bottom: 1px solid rgba(255,255,255,.05);
  font-size: 13px;
}}
.playoff-match:last-child {{ border-bottom: none; }}
.playoff-team {{
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}}
.playoff-team.winner {{ color: var(--text); font-weight: 700; }}
.playoff-agg.decided {{ color: var(--text); }}
.playoff-team.loser {{ opacity: .5; }}
.playoff-team span {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.playoff-score {{
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  font-size: 14px;
  min-width: 36px;
  text-align: center;
  color: var(--accent);
}}
.playoff-agg {{
  text-align: center;
  padding: 5px 12px;
  font-size: 11px;
  font-weight: 700;
  color: var(--muted);
  background: rgba(255,255,255,.03);
  border-top: 1px solid rgba(255,255,255,.06);
}}
.playoff-agg.decided {{ color: var(--win); }}
.playoff-final-box {{
  background: linear-gradient(135deg,rgba(250,204,21,.08),rgba(250,204,21,.03));
  border: 1px solid rgba(250,204,21,.25);
  border-radius: 10px;
  overflow: hidden;
}}
.playoff-winner-banner {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  background: linear-gradient(135deg,rgba(250,204,21,.15),rgba(250,204,21,.05));
  border-top: 1px solid rgba(250,204,21,.2);
  font-size: 15px;
  font-weight: 700;
  color: #facc15;
}}
.playoff-pending {{
  text-align: center;
  padding: 24px 12px;
  color: var(--muted);
  font-size: 13px;
}}
@media (max-width: 640px) {{
  .playoff-bracket {{ grid-template-columns: 1fr; }}
  .playoff-connector {{ flex-direction: row; font-size: 14px; padding-top: 0; }}
}}

/* ── Historia ───────────────────────────────────────────── */
.historia-season-selector {{
  display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px;
}}
.historia-season-btn {{
  background: var(--card2); border: 1px solid rgba(255,255,255,.1);
  border-radius: 8px; padding: 6px 14px; font-size: 13px; cursor: pointer;
  color: var(--text); transition: background .15s, border-color .15s;
}}
.historia-season-btn.active, .historia-season-btn:hover {{
  background: var(--accent); color: #000; border-color: var(--accent);
}}
.historia-table {{
  width: 100%; border-collapse: collapse; font-size: 13px;
}}
.historia-table th {{
  background: var(--card2); color: var(--muted); font-weight: 600;
  padding: 7px 8px; text-align: center; font-size: 11px; text-transform: uppercase;
  letter-spacing: .4px; border-bottom: 1px solid rgba(255,255,255,.07);
}}
.historia-table th:nth-child(2) {{ text-align: left; }}
.historia-table td {{
  padding: 6px 8px; text-align: center;
  border-bottom: 1px solid rgba(255,255,255,.04);
}}
.historia-table td:nth-child(2) {{ text-align: left; }}
.historia-table tr:hover td {{ background: rgba(255,255,255,.03); }}
.historia-pos-badge {{
  display: inline-block; width: 22px; height: 22px; border-radius: 50%;
  font-size: 11px; font-weight: 700; line-height: 22px; text-align: center;
}}
.pos-1  {{ background: #d4af37; color: #000; }}
.pos-2  {{ background: #a8a9ad; color: #000; }}
.pos-3  {{ background: #cd7f32; color: #000; }}
.pos-asc {{ background: rgba(34,197,94,.25); color: var(--win); }}
.pos-play {{ background: rgba(250,204,21,.18); color: #facc15; }}
.pos-rel {{ background: rgba(239,68,68,.2); color: var(--loss); }}
.historia-team-row {{
  display: flex; gap: 6px; align-items: center;
}}
.historia-team-row img {{ width: 18px; height: 18px; object-fit: contain; }}
.historia-pts-bar-wrap {{ width: 70px; }}
.historia-pts-bar {{
  height: 6px; border-radius: 3px; background: var(--accent); opacity: .7;
}}
/* Sección de evolución de equipo */
.historia-team-select {{
  background: var(--card2); border: 1px solid rgba(255,255,255,.15);
  border-radius: 8px; padding: 6px 12px; color: var(--text); font-size: 13px;
  width: 100%; max-width: 260px; margin-bottom: 16px;
}}
.historia-evo-grid {{
  display: grid; gap: 6px;
}}
.historia-evo-row {{
  display: grid; grid-template-columns: 70px 1fr 40px 40px 40px 40px 40px;
  align-items: center; gap: 8px; padding: 6px 10px;
  background: var(--card2); border-radius: 8px; font-size: 12px;
}}
.historia-evo-row.current-season {{
  border-left: 3px solid var(--accent);
}}
</style>
</head>
<body>

<!-- HEADER UNIFICADO (sticky) -->
<header>
  <div class="header-inner">
  <div class="header-top">
    <button class="hamburger-btn" id="hamburgerBtn" onclick="toggleNav()" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <div class="logo">
      <img src="logo.png" alt="Liga Hypertensiones" width="250" height="88" fetchpriority="high" />
    </div>
    <h1>Liga Hypertensiones 25/26</h1>
    <div class="header-meta">
      <div id="nextMatchBanner">
        <span class="nm-dot"></span>
        <span class="nm-label">Próximo choque</span>
        <span class="nm-teams" id="nmTeams"></span>
        <span class="nm-sep">·</span>
        <span class="nm-countdown" id="nmCountdown"></span>
      </div>
      <div class="status-bar">
        <div class="status-text" id="statusText">
          <span style="color:var(--muted);font-size:11px">⟳ Iniciando actualización automática...</span>
        </div>
        <button class="refresh-btn" onclick="fetchAndUpdate()" title="Actualizar datos ahora">⟳ Actualizar</button>
      </div>
    </div>
    <div class="rounds-badge" id="roundsBadge">Jornada {total_rounds} / 42</div>
    <div class="season-select-wrap">
      <label for="seasonSelect">Temporada</label>
      <select class="season-select" id="seasonSelect" onchange="switchSeason(this.value)">
        <option value="_actual_">25/26 ★</option>
        {season_options_html}
      </select>
    </div>
  </div>
  <nav id="mainNav">
    <button class="active" data-tab="clasificacion" onclick="switchTab('clasificacion')">🏆 Clasificación</button>
    <button data-tab="evolucion" onclick="switchTab('evolucion')">📈 Evolución</button>
    <button data-tab="resultados" onclick="switchTab('resultados')">📋 Resultados</button>
    <button data-tab="predicciones" onclick="switchTab('predicciones')">🔮 Predicciones</button>
    <button data-tab="equipos" onclick="switchTab('equipos')">👕 Equipos</button>
    <button data-tab="playoff" onclick="switchTab('playoff')">🏆 Playoff</button>
    <button data-tab="analisis" onclick="switchTab('analisis')">📊 Análisis</button>
  </nav>
  </div>
</header>

<!-- LIVE MATCH BAR -->
<div class="live-bar" id="liveBar"></div>

<main>

<!-- ============================== TAB 1: CLASIFICACIÓN ============================== -->
<div class="tab-panel active" id="tab-clasificacion">
  <!-- Navegador de jornadas -->
  <div class="standings-round-nav">
    <button class="round-btn" onclick="changeStandingsRound(-1)" id="btnStandPrev">‹</button>
    <span class="round-label" id="standingsRoundLabel">J{total_rounds} / {total_rounds}</span>
    <button class="round-btn" onclick="changeStandingsRound(1)" id="btnStandNext">›</button>
    <button class="btn-latest" onclick="changeStandingsRound(999)">Última jornada →</button>
    <span class="forma-label" style="margin-left:12px;color:var(--muted);font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px">Forma:</span>
    <button class="btn-form active" id="fmtAll" onclick="setFormMode(0)">General</button>
    <button class="btn-form" id="fmt5" onclick="setFormMode(5)">Últ.5</button>
    <button class="btn-form" id="fmt10" onclick="setFormMode(10)">Últ.10</button>
    <button class="btn-form" id="fmt20" onclick="setFormMode(20)">Últ.20</button>
  </div>
  <div class="zone-legend">
    <div class="zone-item"><div class="zone-dot" style="background:#22c55e"></div> Ascenso Directo (1-2)</div>
    <div class="zone-item"><div class="zone-dot" style="background:#fbbf24"></div> Playoff Ascenso (3-6)</div>
    <div class="zone-item"><div class="zone-dot" style="background:#6b7280"></div> Permanencia (7-18)</div>
    <div class="zone-item"><div class="zone-dot" style="background:#ef4444"></div> Descenso (19-22)</div>
  </div>
  <div class="card">
    <div class="standings-wrapper">
      <table class="standings-table" id="standingsTable">
        <thead>
          <tr>
            <th onclick="sortTable('pos')" title="Posición">#</th>
            <th onclick="sortTable('name')" title="Equipo">Equipo</th>
            <th onclick="sortTable('played')">PJ</th>
            <th onclick="sortTable('wins')">PG</th>
            <th onclick="sortTable('draws')">PE</th>
            <th onclick="sortTable('losses')">PP</th>
            <th onclick="sortTable('gf')" title="Goles a favor">GF</th>
            <th onclick="sortTable('gc')" title="Goles en contra">GC</th>
            <th onclick="sortTable('dif')" title="Diferencia de goles">DIF</th>
            <th onclick="sortTable('ppg')" title="Puntos por partido">PPG</th>
            <th onclick="sortTable('pts')" style="min-width:160px">Puntos</th>
            <th title="Últimas 5">Forma</th>
            <th onclick="sortTable('racha')" title="Partidos consecutivos sin perder">Racha</th>
            <th onclick="sortTable('situacion')" title="Situación en la liga" style="min-width:140px">Situación</th>
            <th onclick="sortTable('quedan')" title="Puntos que quedan por jugar">Quedan</th>
          </tr>
        </thead>
        <tbody id="standingsBody"></tbody>
      </table>
    </div>
    <div class="card-legend"><b>PJ</b> Partidos jugados &nbsp;·&nbsp; <b>PG/PE/PP</b> Ganados / Empates / Perdidos &nbsp;·&nbsp; <b>GF/GC</b> Goles a favor / en contra &nbsp;·&nbsp; <b>DIF</b> Diferencia de goles &nbsp;·&nbsp; <b>PPG</b> Puntos por partido (media) &nbsp;·&nbsp; <b>Forma</b> últimos 5 resultados (V/E/D) &nbsp;·&nbsp; <b>Racha</b> partidos consecutivos sin perder &nbsp;·&nbsp; <b>Quedan</b> puntos máximos posibles por disputar (jornadas restantes × 3)</div>
  </div>
</div>

<!-- ============================== TAB 2: EVOLUCIÓN ============================== -->
<div class="tab-panel" id="tab-evolucion">
  <div class="gap-section">
    <div class="card">
      <div class="card-title">📈 Evolución jornada a jornada</div>
      <div class="chart-tabs">
        <button class="chart-tab active" id="ctab-pos" onclick="switchChart('pos')">Posición</button>
        <button class="chart-tab" id="ctab-pts" onclick="switchChart('pts')">Puntos</button>
        <button class="chart-tab" id="ctab-ppg" onclick="switchChart('ppg')">PPG Rolling (5J)</button>
      </div>
      <div class="card-title" style="font-size:12px; color:var(--muted); margin-bottom:8px;">Seleccionar equipos:</div>
      <div class="team-selector" id="teamSelector"></div>
      <div class="chart-controls">
        <button onclick="selectTopTeams(6)" class="active">Top 6</button>
        <button onclick="selectTopTeams(10)">Top 10</button>
        <button onclick="selectAllTeams()">Todos</button>
        <button onclick="deselectAllTeams()">Ninguno</button>
      </div>
      <div class="chart-container">
        <canvas id="evolutionChart"></canvas>
      </div>
      <div class="card-legend"><b>Posición</b> lugar en la clasificación jornada a jornada &nbsp;·&nbsp; <b>Puntos</b> puntos acumulados por jornada &nbsp;·&nbsp; <b>PPG Rolling 5J</b> media de puntos por partido en las últimas 5 jornadas (mueve la ventana hacia adelante conforme avanza la temporada) &nbsp;·&nbsp; Usa los botones para filtrar los equipos que se muestran</div>
    </div>
  </div>
</div>

<!-- ============================== TAB 3: RESULTADOS ============================== -->
<div class="tab-panel" id="tab-resultados">
  <div class="gap-section">
    <div class="card">
      <div class="card-title">📋 Resultados por jornada</div>
      <div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;align-items:center;">
        <button class="hist-sort-btn active" id="rsort-clas" onclick="setResultsSort('clas')">🏆 Clasificación</button>
        <button class="hist-sort-btn" id="rsort-alfa" onclick="setResultsSort('alfa')">🔤 Alfabético</button>
      </div>
      <div class="round-selector">
        <button class="round-btn" id="btnPrevRound" onclick="changeRound(-1)">‹</button>
        <label>Jornada</label>
        <input type="number" class="round-input" id="roundInput" min="1" max="42" value="{total_rounds}" onchange="renderRoundResults()">
        <button class="round-btn" id="btnNextRound" onclick="changeRound(1)">›</button>
        <span style="color:var(--muted); font-size:12px" id="roundProgressLabel">de {total_rounds} jugadas · 42 en temporada</span>
      </div>
      <div class="results-grid" id="resultsGrid"></div>
      <div class="card-legend">Cada partido muestra: <b>equipo</b> (el de la fila) a la izquierda · <b>rival</b> a la derecha · <b>resultado</b> al centro (goles del equipo – goles del rival) · <b>condición</b> si jugó de local (🏠) o visitante (✈️) · <span style="color:#4ade80">■</span> victoria &nbsp;<span style="color:#fbbf24">■</span> empate &nbsp;<span style="color:#ef4444">■</span> derrota · navega con las flechas o escribe directamente el número de jornada</div>
    </div>
    <div class="card">
      <div class="card-title">📊 Historial completo (V/E/D por equipo)</div>
      <div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;">
        <span style="font-size:11px;color:var(--muted);align-self:center;margin-right:4px;">Ordenar:</span>
        <button class="hist-sort-btn active" id="hsort-clas" onclick="renderHistoryTable('clas')">🏆 Clasificación</button>
        <button class="hist-sort-btn" id="hsort-alfa" onclick="renderHistoryTable('alfa')">🔤 Alfabético</button>
        <button class="hist-sort-btn" id="hsort-wins" onclick="renderHistoryTable('wins')">✅ + Victorias</button>
        <button class="hist-sort-btn" id="hsort-loss" onclick="renderHistoryTable('loss')">❌ + Derrotas</button>
      </div>
      <div class="history-grid-wrapper">
        <table class="history-table" id="historyTable"></table>
      </div>
      <div class="card-legend"><b>V</b> Victoria &nbsp;·&nbsp; <b>E</b> Empate &nbsp;·&nbsp; <b>D</b> Derrota &nbsp;·&nbsp; cada columna = una jornada · el color de fondo indica el resultado · ordena por clasificación, alfabético, más victorias o más derrotas usando los botones superiores</div>
    </div>
  </div>
</div>

<!-- ============================== TAB 4: PREDICCIONES ============================== -->
<div class="tab-panel" id="tab-predicciones">
  <div class="gap-section">
    <div class="card">
      <div class="card-title">🔮 Predicciones de clasificación final</div>
      <div style="font-size:12px;color:var(--muted);margin-bottom:16px;">
        Probabilidades al cierre de temporada · Fuente: BeSoccer
      </div>
      <div class="pred-legend">
        <div class="pred-legend-item"><div class="pred-legend-dot" style="background:#22c55e"></div> Ascenso directo</div>
        <div class="pred-legend-item"><div class="pred-legend-dot" style="background:#fbbf24"></div> Playoff ascenso</div>
        <div class="pred-legend-item"><div class="pred-legend-dot" style="background:#6b7280"></div> Permanencia</div>
        <div class="pred-legend-item"><div class="pred-legend-dot" style="background:#ef4444"></div> Descenso</div>
      </div>
      <div id="predictionsTable"></div>
      <div class="card-legend">Probabilidades estimadas de clasificación final al cierre de temporada &nbsp;·&nbsp; <b>Ascenso directo</b> puestos 1-2 &nbsp;·&nbsp; <b>Playoff</b> puestos 3-6 &nbsp;·&nbsp; <b>Permanencia</b> puestos 7-18 &nbsp;·&nbsp; <b>Descenso</b> puestos 19-22 &nbsp;·&nbsp; Fuente: BeSoccer · se actualiza tras cada jornada</div>
    </div>
    <div class="card mt-20">
      <div class="card-title">📊 Pronósticos históricos por equipo</div>
      <div style="font-size:12px;color:var(--muted);margin-bottom:14px;">
        Probabilidades de clasificación final jornada a jornada · barras apiladas + línea de posición/puntos
      </div>
      <div class="team-selector" id="predHistSelector" style="margin-bottom:14px;max-height:none;"></div>
      <div class="chart-tabs" style="margin-bottom:14px;">
        <button class="chart-tab active" id="phcTab-pos" onclick="switchPredHistMode('pos')">📍 Posición</button>
        <button class="chart-tab" id="phcTab-pts" onclick="switchPredHistMode('pts')">📊 Puntos</button>
      </div>
      <div class="chart-container" style="height:380px;">
        <canvas id="predHistCanvas"></canvas>
      </div>
      <div class="card-legend">Evolución de las probabilidades de cada zona clasificatoria jornada a jornada &nbsp;·&nbsp; <b>Barras apiladas</b> % estimado en cada zona (Ascenso / Playoff / Permanencia / Descenso) &nbsp;·&nbsp; <b>Línea</b> posición real o puntos reales según el modo seleccionado &nbsp;·&nbsp; Selecciona un equipo con los botones superiores</div>
    </div>
  </div>
</div>

<!-- ============================== TAB 5: EQUIPOS ============================== -->
<div class="tab-panel" id="tab-equipos">
  <div class="teams-grid" id="teamsGrid"></div>
</div>

<!-- ============================== TAB 6: ANÁLISIS ============================== -->
<div class="tab-panel" id="tab-analisis">
  <div class="gap-section">
    <!-- Selector de equipos análisis -->
    <div class="card" style="padding:14px 20px">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px">
        <div style="font-size:12px;font-weight:700;color:var(--text)">🎯 Filtrar equipos <span style="color:var(--muted);font-weight:400;font-size:11px">· selecciona para destacar sus datos en todos los gráficos · sin selección = todos visibles</span></div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">
          <button class="hist-sort-btn" onclick="analisisSelectTop(6)">Top 6</button>
          <button class="hist-sort-btn" onclick="analisisSelectTop(10)">Top 10</button>
          <button class="hist-sort-btn" onclick="analisisSelectAll()">Todos</button>
          <button class="hist-sort-btn" onclick="analisisSelectNone()">Ninguno</button>
        </div>
      </div>
      <div class="team-selector" id="analisisTeamSelector" style="max-height:100px;margin-bottom:0"></div>
    </div>
    <div class="analisis-top-grid">
      <div class="card">
        <div class="card-title">⚡ Ataque vs Defensa</div>
        <div style="font-size:11px;color:var(--muted);margin-bottom:8px">GF (eje X) · GC (eje Y) · líneas = media liga</div>
        <div class="chart-container" style="height:320px"><canvas id="scatterChart"></canvas></div>
        <div class="card-legend"><b>Eje X</b> Goles a favor (GF) · <b>Eje Y</b> Goles en contra (GC, mayor = peor) · Líneas = media de la liga · <b>🔥 Coladero</b> (arriba-izq) mucho gol a favor pero también encajan muchos · <b>Sólidos 📊</b> (arriba-dcha) buen ataque y buena defensa · <b>🛡 Robustos</b> (abajo-izq) poco gol pero también encajan poco · <b>Killers ⚡</b> (abajo-dcha) marcan mucho y no encajan: el ideal</div>
      </div>
      <div class="card">
        <div class="card-title">🏅 Rankings</div>
        <select id="rankingSelect" onchange="switchRanking(this.value)">
          <option value="off">⚽ Ataque</option>
          <option value="def">🛡 Defensa</option>
          <option value="dif">↕ Dif. Goles</option>
          <option value="ppg">📊 PPG</option>
          <option value="forma">🔥 Forma</option>
          <option value="racha">⚡ Racha</option>
          <option value="home">🏠 Local</option>
          <option value="away">✈️ Visitante</option>
          <option value="gfpj">🎯 GF/PJ</option>
          <option value="gcpj">🔒 GC/PJ</option>
          <option value="xpts">📐 xPts</option>
        </select>
        <div id="rankingList" style="max-height:290px;overflow-y:auto"></div>
        <div class="card-legend"><b>Ataque</b> GF por partido &nbsp;·&nbsp; <b>Defensa</b> GC por partido (menos = mejor) &nbsp;·&nbsp; <b>PPG</b> puntos por partido (media general) &nbsp;·&nbsp; <b>Local/Visitante</b> PPG jugando en casa / fuera &nbsp;·&nbsp; <b>xPts</b> puntos pitagóricos = GF²÷(GF²+GC²)×PJ×3 · Ordenado de más infrapuntuado (mala suerte, barra verde) a más sobrepuntuado (con suerte, barra roja) · <b>xPts &gt; Pts reales</b> → merece más puntos de los que tiene · <b>xPts &lt; Pts reales</b> → ha tenido suerte, puede bajar</div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">🔢 Escenarios Matemáticos</div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:12px">Máx. = si gana todo · Con E = si empata todo · Puntos restantes por disputar</div>
      <div class="standings-wrapper">
        <table class="standings-table" id="scenariosTable">
          <thead><tr>
            <th>#</th>
            <th>Equipo</th>
            <th title="Puntos actuales">Pts</th>
            <th title="Jornadas restantes">Rest.</th>
            <th title="Puntos máximos posibles si gana todo" style="color:#4ade80">Máx.</th>
            <th title="Puntos si empata todo lo que queda" style="color:#fbbf24">Con E</th>
            <th title="¿Puede alcanzar el ascenso directo?">Ascenso</th>
            <th title="¿Puede alcanzar el playoff?">Playoff</th>
            <th title="¿Puede salvarse matemáticamente? (sus puntos máximos ≥ puntos del 18º)">Salvación</th>
            <th title="¿Puede aún descender matemáticamente? (el 18º puede alcanzarle con sus puntos máximos)">Descenso</th>
          </tr></thead>
          <tbody id="scenariosBody"></tbody>
        </table>
      </div>
      <div class="card-legend"><b>Máx.</b> puntos actuales + (jornadas restantes × 3) &nbsp;·&nbsp; <b>Con E</b> puntos si empata todos los partidos que quedan &nbsp;·&nbsp; <b>Ascenso ✓</b> Máx. ≥ puntos del 2º &nbsp;·&nbsp; <b>Playoff ✓</b> Máx. ≥ puntos del 6º &nbsp;·&nbsp; <b>Salvación ✓</b> Máx. ≥ puntos actuales del 18º (aún puede salvarse) &nbsp;·&nbsp; <b>Descenso ✓ rojo</b> el 18º puede alcanzarle ganando todo (aún en peligro matemático) · ✗ gris = ya imposible</div>
    </div>
    <!-- Local vs Visitante -->
    <div class="card">
      <div class="card-title">🏠✈️ Rendimiento Local vs Visitante</div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:12px">Puntos obtenidos como local y como visitante · ordenados por total de puntos</div>
      <div class="chart-container" style="height:480px"><canvas id="localVisitanteChart"></canvas></div>
      <div class="card-legend"><b>Pts Local/Visitante</b> suma de puntos obtenidos jugando en casa / a domicilio &nbsp;·&nbsp; <b>GF Local/Visitante</b> goles marcados en casa / fuera &nbsp;·&nbsp; Calculado sobre todos los partidos jugados de la temporada · Los equipos aparecen ordenados por puntos totales (mayor arriba)</div>
    </div>

    <!-- Estadísticas Avanzadas AS.com -->
    <div class="card" id="advStatsCard">
      <div class="card-title">📊 Estadísticas Avanzadas (Opta / AS.com)</div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:10px">Promedios por partido · Ordenar por columna · Solo temporada actual</div>
      <div id="advStatsFilter" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px"></div>
      <div class="standings-wrapper" style="overflow-x:auto">
        <table class="standings-table" id="advStatsTable">
          <thead>
            <tr>
              <th style="min-width:130px;text-align:left;cursor:pointer" data-advcol="name" onclick="sortAdvStats(this)">Equipo</th>
              <th title="Posesión media %" style="cursor:pointer" data-advcol="possession" onclick="sortAdvStats(this)">Pos.%</th>
              <th title="Disparos a puerta por partido (dentro del marco)" style="cursor:pointer" data-advcol="shots_inside" onclick="sortAdvStats(this)">D.Puerta</th>
              <th title="Disparos fuera del marco por partido" style="cursor:pointer" data-advcol="shots_outside" onclick="sortAdvStats(this)">D.Fuera</th>
              <th title="Disparos bloqueados por partido" style="cursor:pointer" data-advcol="shots_blocked" onclick="sortAdvStats(this)">D.Bloq</th>
              <th title="Disparos recibidos (tiros del rival)" style="cursor:pointer" data-advcol="shots_received" onclick="sortAdvStats(this)">Recib.</th>
              <th title="Faltas cometidas por partido" style="cursor:pointer" data-advcol="fouls_committed" onclick="sortAdvStats(this)">Faltas</th>
              <th title="Tarjetas amarillas por partido" style="cursor:pointer" data-advcol="yellow_cards" onclick="sortAdvStats(this)">🟨</th>
              <th title="Tarjetas rojas por partido" style="cursor:pointer" data-advcol="red_cards" onclick="sortAdvStats(this)">🟥</th>
              <th title="Pérdidas de posesión por partido" style="cursor:pointer" data-advcol="poss_losses" onclick="sortAdvStats(this)">Pérd.</th>
              <th title="Recuperaciones de posesión por partido" style="cursor:pointer" data-advcol="poss_recoveries" onclick="sortAdvStats(this)">Recup.</th>
              <th title="Fueras de juego por partido" style="cursor:pointer" data-advcol="offsides" onclick="sortAdvStats(this)">OFJ</th>
              <th title="Partidos con estadísticas disponibles" style="cursor:pointer;color:var(--muted)" data-advcol="pj" onclick="sortAdvStats(this)">PJ</th>
            </tr>
          </thead>
          <tbody id="advStatsBody"></tbody>
        </table>
      </div>
      <div class="card-legend"><b>Pos.%</b> posesión media &nbsp;·&nbsp; <b>D.Puerta</b> disparos dentro del marco &nbsp;·&nbsp; <b>D.Fuera</b> fuera del marco &nbsp;·&nbsp; <b>D.Bloq</b> disparos bloqueados &nbsp;·&nbsp; <b>Recib.</b> disparos recibidos del rival &nbsp;·&nbsp; <b>Pérd.</b> pérdidas de posesión &nbsp;·&nbsp; <b>Recup.</b> recuperaciones de posesión &nbsp;·&nbsp; Haz clic en cualquier columna para ordenar · Fuente: AS.com / Opta</div>
    </div>

    <!-- Head-to-head matrix -->
    <div class="card">
      <div class="card-title">⚔️ Resultados directos (todos vs todos)</div>
      <div style="font-size:11px;color:var(--muted);margin-bottom:10px">Fila = equipo local · Columna = equipo visitante · marcador del partido de ida (local → visitante)</div>
      <div id="h2hGrid" style="overflow-x:auto"></div>
      <div class="card-legend"><b>Fila</b> equipo local &nbsp;·&nbsp; <b>Columna</b> equipo visitante &nbsp;·&nbsp; Cada celda muestra el marcador del partido (goles local – goles visitante) &nbsp;·&nbsp; <span style="color:#39ff14">■</span> Victoria del equipo de la fila &nbsp;·&nbsp; <span style="color:#f59e0b">■</span> Empate &nbsp;·&nbsp; <span style="color:#ef4444">■</span> Derrota del equipo de la fila &nbsp;·&nbsp; <b>Cruz de Selección</b> activa una capa de oscurecimiento fuera de la fila y columna del cursor para facilitar la lectura</div>
    </div>

    <!-- Radar por equipo y Consistencia: 50/50 -->
    <div class="analisis-bottom-grid">
      <!-- Radar por equipo -->
      <div class="card">
        <div class="card-title">🕸️ Radar por Equipo</div>
        <div style="font-size:11px;color:var(--muted);margin-bottom:12px">6 dimensiones normalizadas al 0–100 · Selecciona hasta 3 equipos</div>
        <div class="radar-layout">
          <div class="radar-team-list" id="radarTeamSelector"></div>
          <div style="flex:1;min-width:0"><canvas id="radarChart" style="width:100%;height:360px"></canvas></div>
        </div>
        <div class="card-legend"><b>Ataque</b> GF/partido · <b>Defensa</b> inv. GC/p · <b>Local/Visitante</b> PPG · <b>Consistencia</b> inv. std · <b>Momentum</b> PPG últ.5 · Todos normalizados: 100=mejor, 0=peor</div>
      </div>
      <!-- Consistencia -->
      <div class="card">
        <div class="card-title">📈 Consistencia — V/E/D por equipo</div>
        <div style="font-size:11px;color:var(--muted);margin-bottom:12px">% de victorias, empates y derrotas · ordenado por % victorias</div>
        <div class="chart-container" style="height:420px"><canvas id="consistenciaChart"></canvas></div>
      </div>
    </div>


  </div>
</div>

<!-- ============================== TAB PLAYOFF ============================== -->
<div class="tab-panel" id="tab-playoff">
  <div class="gap-section" id="playoffContent"></div>
</div>

</main>

<!-- MODAL team detail -->
<div class="modal-overlay" id="teamModal">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <div class="modal-title" id="modalTitle"></div>
    <div id="modalBody"></div>
  </div>
</div>

<!-- MODAL match stats -->
<div class="modal-overlay" id="matchModal">
  <div class="modal" style="max-width:420px">
    <button class="modal-close" onclick="closeMatchModal()">✕</button>
    <div id="matchModalBody"></div>
  </div>
</div>

<script>
// ===== DATA =====
let LIGA_DATA = {data_js};
const TEAM_COLORS = {colors_js};
const TEAM_BADGES = {badges_js};
const TEAM_EXTRA_STATS = {extra_js};
const TEAM_PREDICTIONS = {predictions_js};
const TEAM_KIT = {kit_js};
const TEAM_KIT_FULL = {kit_full_js};
const BESOCCER_NAME = {besoccer_map_js};
let SCORES_DATA = {scores_js};
const PRED_HISTORY = {pred_hist_js};
const HISTORY_DATA = {history_js};
const AS_STATS = {as_stats_js};
// Ganadores del playoff de ascenso por temporada histórica
const HIST_PLAYOFF_WINNERS = {{
  '2019/20': 'Elche',
  '2020/21': 'Rayo Vallecano',
  '2021/22': 'Girona',
  '2022/23': 'Alavés',
  '2023/24': 'Espanyol',
  '2024/25': 'Real Oviedo',
}};
const MAX_PTS = LIGA_DATA.total_rounds * 3;

// ===== STATE =====
let sortCol = 'pos', sortAsc = true;
let activeChart = 'pos';
let evolutionChart = null;
let selectedTeams = new Set();

let currentRound = LIGA_DATA.total_rounds;
let standingsRound = LIGA_DATA.total_rounds; // which jornada to show in standings
let formMode = 0; // 0 = general, N = last N jornadas
let liveState = {{}}; // name -> {{opponent, diff, homeGoals, awayGoals, isHome, minute}}

// Poblar liveState desde datos embebidos (partidos en curso)
(function() {{
  const ls = SCORES_DATA.live_scores || {{}};
  Object.entries(ls).forEach(([name, m]) => {{
    liveState[name] = {{
      opponent:  m.opponent,
      diff:      m.is_home ? (m.score_h - m.score_a) : (m.score_a - m.score_h),
      homeGoals: m.score_h,
      awayGoals: m.score_a,
      isHome:    m.is_home,
      minute:    m.minute,
    }};
  }});
}})();

// ===== DESEMPATE CARA A CARA (Reglamento 2ª División) =====
// Criterios (en orden): pts · H2H pts · H2H GD · H2H GF · GD general · GF general · nombre
function computeH2HStats(names, r) {{
  const h2h = {{}};
  names.forEach(n => h2h[n] = {{ pts: 0, gd: 0, gf: 0 }});
  const nameSet = new Set(names);
  const oppsMap = LIGA_DATA.opponents_by_team || {{}};
  const resMap  = LIGA_DATA.results_by_team   || {{}};
  const scMap   = SCORES_DATA.scores_by_team  || {{}};
  names.forEach(name => {{
    const oppArr = oppsMap[name] || [];
    const resArr = resMap[name]  || [];
    for (let i = 0; i < Math.min(r, oppArr.length); i++) {{
      const opp = oppArr[i];
      if (!nameSet.has(opp)) continue;
      const result = resArr[i];
      if (!result) continue;
      const sc = (scMap[name] || {{}})[String(i)];
      if (sc) {{
        const [gf, gc] = sc.split('-').map(Number);
        h2h[name].gf += gf;
        h2h[name].gd += (gf - gc);
      }}
      if (result === 'V') h2h[name].pts += 3;
      else if (result === 'E') h2h[name].pts += 1;
    }}
  }});
  return h2h;
}}
// Ordena in-place: pts → H2H pts → H2H GD → H2H GF → GD → GF → nombre
function applyTiebreakSort(arr, r) {{
  arr.sort((a, b) => b.pts - a.pts);
  let i = 0;
  while (i < arr.length) {{
    let j = i + 1;
    while (j < arr.length && arr[j].pts === arr[i].pts) j++;
    if (j - i > 1) {{
      const grp = arr.slice(i, j);
      const h2h = computeH2HStats(grp.map(t => t.name), r);
      grp.sort((a, b) => {{
        const ha = h2h[a.name], hb = h2h[b.name];
        if (hb.pts !== ha.pts) return hb.pts - ha.pts;
        if (hb.gd  !== ha.gd)  return hb.gd  - ha.gd;
        if (hb.gf  !== ha.gf)  return hb.gf  - ha.gf;
        if (b.dif  !== a.dif)  return b.dif  - a.dif;
        if (b.gf   !== a.gf)   return b.gf   - a.gf;
        return a.name.localeCompare(b.name, 'es');
      }});
      arr.splice(i, j - i, ...grp);
    }}
    i = j;
  }}
  return arr;
}}

// ===== COMPUTED STANDINGS =====
function computeStandingsForRound(round) {{
  const r = Math.min(round, LIGA_DATA.total_rounds);
  const isCurrent = (r === LIGA_DATA.total_rounds);
  const scMap = SCORES_DATA.scores_by_team || {{}};
  const teams = LIGA_DATA.teams.map(name => {{
    const res = (LIGA_DATA.results_by_team[name] || []).slice(0, r);
    const wins   = res.filter(x=>x==='V').length;
    const draws  = res.filter(x=>x==='E').length;
    const losses = res.filter(x=>x==='D').length;
    const pts    = wins * 3 + draws;
    // Acumular GF/GC desde los marcadores reales (scores_data.json)
    const teamScores = scMap[name] || {{}};
    let gf = 0, gc = 0;
    for (let i = 0; i < r; i++) {{
      const sc = teamScores[String(i)];
      if (sc) {{
        const [a, b] = sc.split('-').map(Number);
        gf += a; gc += b;
      }}
    }}
    // En la jornada actual siempre usamos los totales oficiales de TEAM_EXTRA_STATS
    if (isCurrent && !_historicalMode) {{
      const ex = TEAM_EXTRA_STATS[name] || {{}};
      if (ex.gf !== undefined) gf = ex.gf;
      if (ex.gc !== undefined) gc = ex.gc;
    }}
    const racha = (() => {{ let c=0; for(let i=res.length-1;i>=0;i--){{ if(res[i]==='D')break; c++; }} return c; }})();
    const played = res.length;
    return {{ name, wins, draws, losses, played, pts, gf, gc, dif: gf - gc, racha,
      ppg: played > 0 ? (pts / played).toFixed(2) : '0.00',
      quedan: (LIGA_DATA.total_season_rounds - r) * 3
    }};
  }});
  applyTiebreakSort(teams, r);
  // Situación dinámica: distancias reales a cada zona (funciona en cualquier jornada)
  const pts3  = teams[2]?.pts  ?? 0;   // 3º clasificado (referencia para asegurar ascenso)
  const pts2  = teams[1]?.pts  ?? 0;   // 2º clasificado (referencia ascenso directo)
  const pts6  = teams[5]?.pts  ?? 0;   // umbral playoff (6º)
  const pts18 = teams[17]?.pts ?? 0;   // 18º (último puesto seguro)
  const pts19 = teams[18]?.pts ?? 0;   // 19º (primer puesto en peligro)
  const quedanRnd = (LIGA_DATA.total_season_rounds - r) * 3;
  teams.forEach((t, i) => {{
    const pos = i + 1;
    t.secured = null;
    // Temporada terminada: posiciones definitivas, sin distancias imposibles
    if (quedanRnd === 0) {{
      if      (pos <= 2)  {{ t.situacion = 'ASCENSO';    t.secured = 'promotion'; }}
      else if (pos <= 6)  {{ t.situacion = 'PLAYOFF';    t.secured = 'playoff'; }}
      else if (pos <= 18) {{ t.situacion = 'PERMANENCIA'; t.secured = 'permanence'; }}
      else                {{ t.situacion = 'DESCENSO';   t.secured = 'relegation'; }}
      return;
    }}
    if (pos <= 2) {{
      // Puntos para asegurar el ascenso directo frente al 3º
      const dAsegurar = quedanRnd - (t.pts - pts3);
      if (dAsegurar <= 0) {{
        t.situacion = 'ASCENSO ASEGURADO';
        t.secured   = 'promotion';
      }} else {{
        t.situacion = `A ${{dAsegurar}} DE ASEGURAR`;
      }}
    }} else if (pos <= 6) {{
      const pts7        = teams[6]?.pts ?? 0;
      const dAscDirecto = pts2 - t.pts;            // puntos hasta el ascenso directo (2º)
      const dOver7      = t.pts - pts7;             // margen sobre el 7º
      const canReachDirecto = dAscDirecto <= quedanRnd;  // puede alcanzar el 2º
      const playoffSecured  = dOver7 > quedanRnd;        // el 7º no puede alcanzarle
      if (canReachDirecto) {{
        // Prioridad: mostrar distancia al ascenso directo mientras sea alcanzable
        t.situacion = dAscDirecto === 0 ? 'IGUALA 2º EN PTS' : `A ${{dAscDirecto}} DEL ASCENSO DIRECTO`;
        if (playoffSecured) t.secured = 'playoff';
      }} else if (playoffSecured) {{
        t.situacion = 'PLAYOFF ASEGURADO';
        t.secured   = 'playoff';
      }} else {{
        // No puede alcanzar el 2º y tampoco asegurado: en zona playoff pero sin garantizar
        t.situacion = 'EN PLAYOFF';
      }}
    }} else if (pos <= 18) {{
      const dPlay = pts6 - t.pts;             // puntos que le faltan al playoff
      const dDesc = t.pts - pts19;            // margen sobre la zona de descenso
      const canPlayoff = dPlay <= quedanRnd;  // puede alcanzar el playoff
      const safe       = dDesc > quedanRnd;   // no puede descender
      if (safe && !canPlayoff) {{
        t.situacion = 'PERMANENCIA';
        t.secured   = 'permanence';
      }} else if (canPlayoff && (safe || dPlay <= dDesc)) {{
        // Puede alcanzar playoff (dPlay ≤ quedanRnd ✔)
        t.situacion = `A ${{dPlay}} DEL PLAYOFF`;
      }} else {{
        // At risk of relegation (dDesc ≤ quedanRnd since !safe ✔)
        t.situacion = `A ${{dDesc}} DEL DESCENSO`;
      }}
    }} else {{
      const needed = pts18 - t.pts;
      if (needed > quedanRnd) {{
        t.situacion = 'DESCENSO';
        t.secured   = 'relegation';
      }} else {{
        t.situacion = `A ${{needed}} DE SALVACI\u00d3N`;
      }}
    }}
  }});
  return teams;
}}
function computeFormStandings(n) {{
  const r = Math.min(standingsRound, LIGA_DATA.total_rounds);
  const startIdx = Math.max(0, r - n);
  const scMap = SCORES_DATA.scores_by_team || {{}};
  return LIGA_DATA.teams.map(name => {{
    const allRes = (LIGA_DATA.results_by_team[name] || []).slice(0, r);
    const res = allRes.slice(-n);
    const wins   = res.filter(x=>x==='V').length;
    const draws  = res.filter(x=>x==='E').length;
    const losses = res.filter(x=>x==='D').length;
    const pts    = wins * 3 + draws;
    const teamScores = scMap[name] || {{}};
    let gf = 0, gc = 0;
    for (let i = startIdx; i < r; i++) {{
      const sc = teamScores[String(i)];
      if (sc) {{ const [a,b]=sc.split('-').map(Number); gf+=a; gc+=b; }}
    }}
    const racha = (() => {{ let c=0; for(let i=allRes.length-1;i>=0;i--){{ if(allRes[i]==='D')break; c++; }} return c; }})();
    const played = res.length;
    return {{ name, wins, draws, losses, played, pts, gf, gc, dif: gf-gc, racha,
      ppg: played > 0 ? (pts/played).toFixed(2) : '0.00',
      quedan: (LIGA_DATA.total_season_rounds - r) * 3,
      situacion: ''
    }};
  }}).sort((a,b) => b.pts - a.pts || b.wins - a.wins || b.dif - a.dif)
    .map((t, i) => ({{...t, pos: i+1,
      situacion: i<2?'ASCENSO':i<6?'PLAYOFF':i<18?'PERMANENCIA':'DESCENSO'
    }}));
}}
function computeStandings() {{
  if (formMode > 0) return computeFormStandings(formMode);
  return computeStandingsForRound(standingsRound).map((t,i)=>({{...t, pos:i+1}}));
}}

// ===== TAB SWITCHING =====
function switchTab(name) {{
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  document.querySelector(`[data-tab="${{name}}"]`).classList.add('active');
  // Cerrar menú hamburguesa al cambiar de tab en móvil
  const nav = document.getElementById('mainNav');
  const btn = document.getElementById('hamburgerBtn');
  if (nav) nav.classList.remove('nav-open');
  if (btn) btn.classList.remove('open');
  if (name === 'evolucion' && !evolutionChart) initEvolutionChart();
  if (name === 'resultados') renderRoundResults();
  if (name === 'predicciones') renderPredictions();
  if (name === 'analisis') initAnalysisTab();
  if (name === 'playoff') renderPlayoff();
}}

function toggleNav() {{
  const nav = document.getElementById('mainNav');
  const btn = document.getElementById('hamburgerBtn');
  nav.classList.toggle('nav-open');
  btn.classList.toggle('open');
}}

// ===== HELPERS =====
function getInitials(name) {{
  return name.split(' ').map(w=>w[0]).join('').toUpperCase().slice(0,3);
}}
function getColor(name) {{ return TEAM_COLORS[name] || '#6b7280'; }}
function readable(hex) {{
  if (!hex || hex.length < 7) return '#f0f0f0';
  const r=parseInt(hex.slice(1,3),16), g=parseInt(hex.slice(3,5),16), b=parseInt(hex.slice(5,7),16);
  return (r*299+g*587+b*114)/1000 < 20 ? '#f0f0f0' : hex;
}}
function crestHTML(name, size=28) {{
  const kit     = TEAM_KIT_FULL[name] || {{}};
  const primary   = kit.primary   || getColor(name);
  const secondary = kit.secondary || '#1a2236';
  const src   = TEAM_BADGES[name];
  const ls = liveState[name];
  const liveClass = ls ? (ls.diff > 0 ? 'crest-live-win' : ls.diff < 0 ? 'crest-live-lose' : 'crest-live-draw') : '';
  const bg = `linear-gradient(135deg, ${{secondary}} 0%, ${{primary}}44 100%)`;
  if (src) return `<div class="team-crest ${{liveClass}}" style="width:${{size}}px;height:${{size}}px;padding:2px;border:2px solid ${{primary}};background:${{bg}};border-radius:50%;--crest-glow:${{primary}}bb"><img src="${{src}}" alt="${{name}}" style="width:100%;height:100%;object-fit:contain;border-radius:50%;" onerror="this.parentElement.innerHTML='${{getInitials(name)}}'"></div>`;
  return `<div class="team-crest ${{liveClass}}" style="width:${{size}}px;height:${{size}}px;background:${{bg}};border:2px solid ${{primary}};border-radius:50%;font-size:${{Math.floor(size*0.38)}}px">${{getInitials(name)}}</div>`;
}}
function formHTML(results, last=5) {{
  const recent = results.slice(-last);
  return '<div class="form-cell">' + recent.map(r => `<div class="form-dot form-${{r}}">${{r}}</div>`).join('') + '</div>';
}}
function rachaHTML(results) {{
  let c = 0;
  for (let i = results.length - 1; i >= 0; i--) {{ if (results[i] === 'D') break; c++; }}
  if (c === 0) return '<span style="color:var(--loss);font-weight:700;font-size:13px">0</span>';
  const col = c >= 10 ? '#fbbf24' : c >= 6 ? 'var(--win)' : c >= 3 ? '#34d399' : 'var(--text)';
  const fire = c >= 10 ? ' 🔥' : c >= 6 ? ' ✦' : '';
  return `<span style="font-weight:700;font-size:13px;color:${{col}}" title="${{c}} partido${{c===1?'':'s'}} sin perder">${{c}}${{fire}}</span>`;
}}
function getZoneClass(pos) {{
  if (pos <= 2) return 'zone-promotion';
  if (pos <= 6) return 'zone-playoff';
  if (pos <= 18) return '';
  return 'zone-relegation';
}}
function posBadge(pos) {{
  const cls = pos===1?'pos-1':pos===2?'pos-2':'pos-default';
  return `<span class="pos-badge ${{cls}}">${{pos}}</span>`;
}}

function situacionHTML(txt, pos) {{
  if (!txt) return '<span class="situ-badge situ-permanencia">–</span>';
  const t = txt.toUpperCase();
  let cls;
  // Clasificar por contenido del texto (más preciso que solo la posición)
  if (t === 'ASCENSO' || t.includes('ASCENSO ASEGURADO') || t.includes('ASEGURAR'))
    cls = 'situ-ascenso';
  else if (t.includes('ASCENSO DIRECTO') || t.includes('IGUALA 2'))
    cls = 'situ-playoff'; // en zona playoff pero aspira al directo
  else if (t.includes('PLAYOFF ASEGURADO') || t === 'PLAYOFF' || t === 'EN PLAYOFF')
    cls = 'situ-playoff';
  else if (t.includes('DEL PLAYOFF'))
    cls = 'situ-permanencia';
  else if (t.includes('PERMANENCIA'))
    cls = 'situ-permanencia';
  else if (t.includes('DESCENSO') && !t.includes('DEL DESCENSO'))
    cls = 'situ-salvacion'; // matem. descendido
  else if (t.includes('DEL DESCENSO') || t.includes('SALVACI'))
    cls = 'situ-salvacion';
  else if (pos !== undefined)
    cls = pos <= 2 ? 'situ-ascenso' : pos <= 6 ? 'situ-playoff' : pos <= 18 ? 'situ-permanencia' : 'situ-salvacion';
  else
    cls = 'situ-permanencia';
  return `<span class="situ-badge ${{cls}}">${{txt}}</span>`;
}}

// ===== STANDINGS =====
let standingsData = [];

function predMiniBar(name) {{
  const pred = TEAM_PREDICTIONS[name] || {{ascenso:0,playoff:0,permanencia:100,descenso:0}};
  const segs = [
    [pred.ascenso,    '#22c55e'],
    [pred.playoff,    '#fbbf24'],
    [pred.permanencia,'#6b7280'],
    [pred.descenso,   '#ef4444'],
  ].filter(([v])=>v>0).map(([v,c])=>`<div style="flex:${{v}};background:${{c}};height:100%"></div>`).join('');
  return `<div class="pred-mini-bar">${{segs}}</div>`;
}}

function liveScoreCell(name) {{
  const ls = liveState[name];
  if (!ls) return '';
  const col = ls.diff > 0 ? '#4ade80' : ls.diff < 0 ? '#f87171' : '#fbbf24';
  const score = ls.isHome ? `${{ls.homeGoals}}-${{ls.awayGoals}}` : `${{ls.awayGoals}}-${{ls.homeGoals}}`;
  return `<span class="live-score-pill" style="background:${{col}}22;color:${{col}};margin-left:4px"><span class="live-dot-indicator"></span>${{score}}</span>`;
}}

function changeStandingsRound(delta) {{
  if (delta === 999) standingsRound = LIGA_DATA.total_rounds;
  else standingsRound = Math.max(1, Math.min(LIGA_DATA.total_rounds, standingsRound + delta));
  sortCol = 'pos'; sortAsc = true;
  renderStandings();
}}

function renderStandings() {{
  standingsData = computeStandings().map((t,i)=>({{...t, pos:i+1}}));
  const lbl = document.getElementById('standingsRoundLabel');
  if (lbl) lbl.textContent = `J${{standingsRound}} / ${{LIGA_DATA.total_rounds}}`;
  const note = document.getElementById('standingsRoundNote');
  if (note) note.textContent = '';
  const prev = document.getElementById('btnStandPrev');
  const next = document.getElementById('btnStandNext');
  if (prev) prev.disabled = standingsRound <= 1;
  if (next) next.disabled = standingsRound >= LIGA_DATA.total_rounds;
  drawStandingsTable();
}}
function drawStandingsTable() {{
  const tbody = document.getElementById('standingsBody');
  const maxPts = Math.max(...standingsData.map(t=>t.pts));
  const isCurrent = (standingsRound >= LIGA_DATA.total_rounds);
  const pts3 = standingsData[2]?.pts ?? 0;  // puntos del 3er clasificado
  tbody.innerHTML = standingsData.map(t => {{
    const zone        = getZoneClass(t.pos);
    const securedCls  = t.secured ? 'secured-' + t.secured : '';
    const results = LIGA_DATA.results_by_team[t.name] || [];
    // Momentum: PPG últimas 5J vs PPG global
    const recent5 = results.slice(Math.max(0, standingsRound-5), standingsRound);
    const pts5 = recent5.filter(x=>x==='V').length*3 + recent5.filter(x=>x==='E').length;
    const ppg5 = recent5.length>0 ? pts5/recent5.length : 0;
    const ppgAll = parseFloat(t.ppg);
    const mDiff = ppg5 - ppgAll;
    const mArrow = recent5.length < 3 ? '' :
      mDiff > 0.25  ? '<span style="color:#4ade80;font-size:11px;margin-left:3px" title="Tendencia ascendente (PPG\u00fab5J=' + ppg5.toFixed(2) + ')">▲</span>' :
      mDiff < -0.25 ? '<span style="color:#f87171;font-size:11px;margin-left:3px" title="Tendencia descendente (PPG\u00fab5J=' + ppg5.toFixed(2) + ')">▼</span>' :
                      '<span style="color:#94a3b8;font-size:11px;margin-left:3px" title="Tendencia estable (PPG\u00fab5J=' + ppg5.toFixed(2) + ')">▬</span>';
    const pct = maxPts > 0 ? (t.pts/maxPts*100).toFixed(1) : 0;
    const color = getColor(t.name);
    const kit = TEAM_KIT[t.name] || color;
    const kf = TEAM_KIT_FULL[t.name] || {{}};
    const kPrimary   = kf.primary   || color;
    const kSecondary = kf.secondary || '#1a2236';
    const liveSc = liveScoreCell(t.name);

    // Columna "Quedan": puntos por disputar para todos los equipos
    const quedanCell = `<span class="quedan-badge">${{t.quedan}} pts</span>`;

    return `
    <tr class="${{zone}} ${{securedCls}}" style="background:linear-gradient(90deg,${{kit}}18 0%,transparent 120px)">
      <td>${{posBadge(t.pos)}}</td>
      <td>
        <div class="team-cell">
          ${{crestHTML(t.name)}}
          <div style="display:flex;flex-direction:column;gap:1px;min-width:0">
            <span class="team-name-text">${{t.name}}</span>${{mArrow}}
            ${{isCurrent ? predMiniBar(t.name) : ''}}
          </div>
        </div>
      </td>
      <td>${{t.played}}${{liveSc}}</td>
      <td style="color:var(--win)">${{t.wins}}</td>
      <td style="color:var(--draw)">${{t.draws}}</td>
      <td style="color:var(--loss)">${{t.losses}}</td>
      <td>${{t.gf}}</td>
      <td>${{t.gc}}</td>
      <td style="color:${{t.dif>0?'var(--win)':t.dif<0?'var(--loss)':'var(--muted)'}};font-weight:600">${{(t.dif>0?'+':'')+t.dif}}</td>
      <td style="color:${{parseFloat(t.ppg)>=2.0?'#4ade80':parseFloat(t.ppg)>=1.5?'#fbbf24':parseFloat(t.ppg)<1.0?'#f87171':'var(--text)'}};font-weight:600">${{t.ppg}}</td>
      <td>
        <div class="pts-bar-cell">
          <span class="pts-value">${{t.pts}}</span>
          <div class="pts-bar"><div class="pts-fill" style="width:${{pct}}%;background:linear-gradient(180deg,${{kPrimary}} 50%,${{kSecondary}} 50%);box-shadow:0 0 0 1.5px ${{kPrimary}};box-sizing:border-box"></div></div>
        </div>
      </td>
      <td>${{formHTML(results.slice(0, standingsRound))}}</td>
      <td>${{rachaHTML(results.slice(0, standingsRound))}}</td>
      <td>${{situacionHTML(t.situacion, t.pos)}}</td>
      <td>${{quedanCell}}</td>
    </tr>`;
  }}).join('');
}}
function sortTable(col) {{
  if (sortCol === col) sortAsc = !sortAsc;
  else {{ sortCol = col; sortAsc = col === 'pos' || col === 'name'; }}
  standingsData.sort((a,b) => {{
    let va = a[col], vb = b[col];
    if (typeof va === 'string') va = va.toLowerCase();
    if (typeof vb === 'string') vb = vb.toLowerCase();
    return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
  }});
  drawStandingsTable();
}}

// ===== EVOLUTION CHART =====
function initEvolutionChart() {{
  const top6 = LIGA_DATA.final_standings.slice(0,6).map(t=>t.name);
  top6.forEach(n => selectedTeams.add(n));
  buildTeamSelector();
  buildChart();
}}
function buildTeamSelector() {{
  const el = document.getElementById('teamSelector');
  el.innerHTML = LIGA_DATA.teams.map(name => {{
    const color = getColor(name);
    const badge = TEAM_BADGES[name];
    const sel = selectedTeams.has(name) ? 'badge-sel' : '';
    const opacity = selectedTeams.has(name) ? '1' : '0.35';
    const imgTag = badge
      ? `<img src="${{badge}}" alt="${{name}}" style="opacity:${{opacity}};filter:drop-shadow(0 0 4px ${{color}}99) drop-shadow(0 0 1px rgba(0,0,0,.7))">`
      : `<div style="width:32px;height:32px;border-radius:50%;background:${{color}};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;opacity:${{opacity}};">${{getInitials(name)}}</div>`;
    return `<label class="team-check-badge ${{sel}}" title="${{name}}">
      <input type="checkbox" value="${{name}}" ${{selectedTeams.has(name)?'checked':''}} onchange="toggleTeam('${{name}}',this.checked)">
      ${{imgTag}}
    </label>`;
  }}).join('');
}}
function toggleTeam(name, checked) {{
  if (checked) selectedTeams.add(name); else selectedTeams.delete(name);
  buildTeamSelector(); buildChart();
}}
function selectTopTeams(n) {{
  selectedTeams.clear();
  LIGA_DATA.final_standings.slice(0,n).forEach(t=>selectedTeams.add(t.name));
  buildTeamSelector(); buildChart();
}}
function selectAllTeams() {{
  LIGA_DATA.teams.forEach(n=>selectedTeams.add(n));
  buildTeamSelector(); buildChart();
}}
function deselectAllTeams() {{
  selectedTeams.clear();
  buildTeamSelector(); buildChart();
}}
function switchChart(type) {{
  activeChart = type;
  document.querySelectorAll('.chart-tab').forEach(b=>b.classList.remove('active'));
  document.getElementById('ctab-'+type).classList.add('active');
  buildChart();
}}

// Plugin: fondo de zonas para la gráfica de posición
const zoneBackgroundPlugin = {{
  id: 'zoneBackground',
  beforeDatasetsDraw(chart) {{
    if (activeChart !== 'pos') return;
    const {{ ctx, chartArea, scales: {{ y }} }} = chart;
    if (!chartArea) return;
    const {{ top, bottom, left, right }} = chartArea;
    const n = LIGA_DATA.teams.length;
    const zones = [
      {{ from: 0.5,  to: 2.5,     color: 'rgba(34,197,94,.13)',   label: 'ASCENSO',     lcolor: '#22c55e' }},
      {{ from: 2.5,  to: 6.5,     color: 'rgba(251,191,36,.10)',  label: 'PLAYOFF',     lcolor: '#fbbf24' }},
      {{ from: 6.5,  to: 18.5,    color: 'rgba(100,116,139,.05)', label: 'PERMANENCIA', lcolor: '#8b9ab0' }},
      {{ from: 18.5, to: n + 0.5, color: 'rgba(239,68,68,.13)',   label: 'DESCENSO',    lcolor: '#ef4444' }},
    ];
    ctx.save();
    ctx.beginPath();
    ctx.rect(left, top, right - left, bottom - top);
    ctx.clip();
    zones.forEach(({{ from, to, color, label, lcolor }}) => {{
      const yT = y.getPixelForValue(from);
      const yB = y.getPixelForValue(to);
      ctx.fillStyle = color;
      ctx.fillRect(left, yT, right - left, yB - yT);
      const midY = (yT + yB) / 2;
      ctx.font = 'bold 9px Segoe UI, system-ui, sans-serif';
      ctx.fillStyle = lcolor + 'aa';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.fillText(label, right - 6, midY);
    }});
    ctx.setLineDash([4, 4]);
    ctx.lineWidth = 0.8;
    [{{ pos: 2.5,  col: 'rgba(34,197,94,.45)'  }},
     {{ pos: 6.5,  col: 'rgba(251,191,36,.40)' }},
     {{ pos: 18.5, col: 'rgba(239,68,68,.40)'  }}].forEach(({{ pos, col }}) => {{
      const yp = y.getPixelForValue(pos);
      ctx.strokeStyle = col;
      ctx.beginPath(); ctx.moveTo(left, yp); ctx.lineTo(right, yp); ctx.stroke();
    }});
    ctx.restore();
  }}
}};

// Plugin: líneas de referencia horizontales para la gráfica de Puntos
const referenceLinesPlugin = {{
  id: 'referenceLines',
  afterDatasetsDraw(chart) {{
    if (activeChart !== 'pts') return;
    const {{ ctx, chartArea, scales: {{ y }} }} = chart;
    if (!chartArea) return;
    const {{ left, right }} = chartArea;
    const standings = computeStandings();
    const pts2nd  = standings[1]?.pts  ?? 0;
    const pts19th = standings[18]?.pts ?? 0;
    const lines = [
      {{ pts: 50,     color: '#94a3b8', dash: [6,4], label: '50 pts' }},
      {{ pts: pts2nd, color: '#22c55e', dash: [8,4], label: `2º · ${{pts2nd}} pts` }},
      {{ pts: pts19th,color: '#ef4444', dash: [8,4], label: `19º · ${{pts19th}} pts` }},
    ];
    ctx.save();
    lines.forEach(({{ pts, color, dash, label }}) => {{
      if (pts <= 0) return;
      const yp = y.getPixelForValue(pts);
      if (yp < chartArea.top || yp > chartArea.bottom) return;
      ctx.beginPath();
      ctx.setLineDash(dash);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.moveTo(left, yp);
      ctx.lineTo(right - 90, yp);
      ctx.stroke();
      // etiqueta a la derecha
      ctx.setLineDash([]);
      ctx.font = 'bold 9px Segoe UI, system-ui, sans-serif';
      ctx.fillStyle = color;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(label, right - 86, yp);
    }});
    ctx.restore();
  }}
}};

function buildChart() {{
  const labels = Array.from({{length: LIGA_DATA.total_rounds}}, (_,i)=>'J'+(i+1));
  const datasets = [];
  selectedTeams.forEach(name => {{
    const color = getColor(name);
    const kf = TEAM_KIT_FULL[name] || {{}};
    const kPri = kf.primary   || color;
    const kSec = kf.secondary || '#1a2236';
    let dataArr;
    if (activeChart === 'pos') {{
      dataArr = LIGA_DATA.positions_by_team[name];
    }} else if (activeChart === 'pts') {{
      dataArr = LIGA_DATA.points_by_team[name];
    }} else {{
      // Rolling 5-jornada PPG
      const results = LIGA_DATA.results_by_team[name] || [];
      const ptsArr = results.map(r => r==='V'?3:r==='E'?1:0);
      const W = 5;
      dataArr = ptsArr.map((_,i) => {{
        if (i < W - 1) return null;
        const slice = ptsArr.slice(i - W + 1, i + 1);
        return parseFloat((slice.reduce((a,b)=>a+b,0) / W).toFixed(2));
      }});
    }}
    // Línea inferior gruesa (secondary) = "borde", oculta de leyenda y tooltip
    datasets.push({{
      label: '\x00' + name,
      data: dataArr,
      borderColor: kSec,
      backgroundColor: 'transparent',
      borderWidth: 5,
      pointRadius: 0,
      pointHoverRadius: 0,
      tension: 0.3,
      fill: false,
      order: 2
    }});
    // Línea superior más fina (primary) = color principal, visible en leyenda
    datasets.push({{
      label: name,
      data: dataArr,
      borderColor: kPri,
      backgroundColor: kPri + '18',
      borderWidth: 3,
      pointRadius: 0,
      pointHoverRadius: 5,
      tension: 0.3,
      fill: false,
      order: 1
    }});
  }});
  if (evolutionChart) evolutionChart.destroy();
  const ctx = document.getElementById('evolutionChart').getContext('2d');
  evolutionChart = new Chart(ctx, {{
    type: 'line',
    data: {{ labels, datasets }},
    plugins: [zoneBackgroundPlugin, referenceLinesPlugin],
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{
          display: true,
          position: 'bottom',
          labels: {{
            color: '#94a3b8', boxWidth: 12, font: {{size: 11}},
            filter: item => !item.text.startsWith('\x00')
          }}
        }},
        tooltip: {{
          callbacks: {{
            label: ctx => ctx.dataset.label.startsWith('\x00') ? null : ` ${{ctx.dataset.label}}: ${{activeChart==='pos'?'#':''}}${{ctx.parsed.y}}${{activeChart==='pts'?' pts':activeChart==='ppg'?' ppg':'º'}}`
          }}
        }}
      }},
      scales: {{
        x: {{
          grid: {{ color: '#2d3f5f44' }},
          ticks: {{ color: '#94a3b8', maxTicksLimit: 20 }}
        }},
        y: {{
          reverse: activeChart === 'pos',
          grid: {{ color: '#2d3f5f44' }},
          ticks: {{ color: '#94a3b8', stepSize: activeChart==='pos'?1:activeChart==='ppg'?0.5:5 }},
          min: activeChart === 'pos' ? 1 : 0,
          max: activeChart === 'pos' ? LIGA_DATA.teams.length : activeChart === 'ppg' ? 3 : undefined
        }}
      }}
    }}
  }});
}}

// ===== RESULTS =====
function renderRoundResults() {{
  const j = parseInt(document.getElementById('roundInput').value);
  currentRound = Math.max(1, Math.min(42, j));
  document.getElementById('roundInput').value = currentRound;
  document.getElementById('btnPrevRound').disabled = currentRound <= 1;
  document.getElementById('btnNextRound').disabled = currentRound >= 42;
  const played = currentRound <= LIGA_DATA.total_rounds;
  const idx = currentRound - 1;
  const grid = document.getElementById('resultsGrid');
  const oppsMap = LIGA_DATA.opponents_by_team || {{}};
  // Ordenar equipos según modo
  let teamList = [...LIGA_DATA.teams]; // por defecto alfabético
  if (resultsSortMode === 'clas') {{
    const standingsMap = {{}};
    computeStandingsForRound(Math.min(currentRound, LIGA_DATA.total_rounds)).forEach((t,i) => {{ standingsMap[t.name] = i; }});
    teamList.sort((a,b) => (standingsMap[a]??99) - (standingsMap[b]??99));
  }}
  // Índice global de fixtures por "home|away" → {{date, time}}
  // Usamos opponents_by_team como fuente de verdad para el rival;
  // fixtures solo aporta fecha/hora/local (buscando por nombres de equipos).
  const allFix = {{}}; // "homeTeam|awayTeam" → {{date, time}}
  if (LIGA_DATA.fixtures) {{
    LIGA_DATA.fixtures.forEach(f => {{
      allFix[f.home + '|' + f.away] = {{ date: f.date, time: f.time }};
    }});
  }}
  grid.innerHTML = teamList.map(name => {{
    if (!played) {{
      // Rival correcto desde opponents_by_team; fecha/hora desde allFix
      const opp2 = oppsMap[name]?.[idx];
      let fx = null;
      if (opp2) {{
        // ¿juega en casa o fuera?
        const keyHome = name + '|' + opp2;
        const keyAway = opp2 + '|' + name;
        if (allFix[keyHome]) {{
          fx = {{ opp: opp2, isHome: true,  ...allFix[keyHome] }};
        }} else if (allFix[keyAway]) {{
          fx = {{ opp: opp2, isHome: false, ...allFix[keyAway] }};
        }} else {{
          // rival conocido pero sin fecha aún
          fx = {{ opp: opp2, isHome: null, date: '', time: '' }};
        }}
      }}
      if (fx) {{
        const oppCrestF = crestHTML(fx.opp, 22);
        const venueLabel = fx.isHome === true ? 'Casa' : fx.isHome === false ? 'Fuera' : '';
        const venueFCol  = 'var(--muted)';
        return `<div class="result-card" style="opacity:.8;border-style:dashed">
          <div class="team-cell" style="gap:8px">
            <div style="flex-shrink:0">${{crestHTML(name)}}</div>
            <div>
              <div class="result-team">${{name}}</div>
              <div class="result-detail" style="display:flex;align-items:center;gap:4px">${{oppCrestF}}<span>${{fx.opp}}</span></div>
              <div style="display:flex;align-items:center;gap:5px;margin-top:3px;">
                <span style="font-size:10px;font-weight:700;color:var(--text)">${{fx.date}} ${{fx.time}}</span>
                <span style="font-size:9px;color:${{venueFCol}};background:rgba(255,255,255,.05);border-radius:4px;padding:1px 5px;">${{venueLabel}}</span>
              </div>
            </div>
          </div>
        </div>`;
      }}
      return `<div class="result-card" style="opacity:.35">
        <div style="width:26px;height:26px;border-radius:50%;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:13px;color:var(--muted);font-weight:700">?</div>
        <div><div class="result-team">${{name}}</div><div class="result-detail" style="color:var(--muted)">J${{currentRound}} · Sin jugar</div></div>
      </div>`;
    }}
    const res = LIGA_DATA.results_by_team[name];
    const r = res && res[idx];
    if (!r) return `<div class="result-card" style="opacity:.4"><div><div class="result-team">${{name}}</div><div class="result-detail">Sin resultado</div></div></div>`;
    const lbl = r==='V'?'Victoria':r==='E'?'Empate':'Derrota';
    const opp = oppsMap[name]?.[idx];
    const oppCrest = opp ? crestHTML(opp, 22) : '';
    const scMap2    = SCORES_DATA.scores_by_team || SCORES_DATA;
    const venueMap2 = SCORES_DATA.venue_by_team  || {{}};
    const rawScore  = (scMap2[name]||{{}})[String(idx)];
    let venue2      = (venueMap2[name]||{{}})[String(idx)];
    // Corregir venue usando AS_STATS (fuente más fiable que scores_data)
    if (opp && AS_STATS.length) {{
      const _asFix = AS_STATS.find(s => s.jornada === currentRound &&
        ((s.home === name && s.away === opp) || (s.home === opp && s.away === name)));
      if (_asFix) venue2 = _asFix.home === name ? 'H' : 'A';
    }}
    let displayScore = rawScore;
    if (rawScore && venue2==='A') {{
      const p = rawScore.split('-');
      if (p.length===2) displayScore = p[1]+'-'+p[0];
    }}
    const venueTxt = venue2==='H' ? 'Casa' : venue2==='A' ? 'Fuera' : '';
    const scoreBadge = displayScore
      ? `<span style="font-size:13px;font-weight:800;letter-spacing:1px;color:var(--text);background:rgba(255,255,255,.07);border-radius:6px;padding:1px 7px;">${{displayScore}}</span>`
      : '';
    const venueTag = venueTxt
      ? `<span style="font-size:9px;color:var(--muted);background:rgba(255,255,255,.05);border-radius:4px;padding:1px 5px;">${{venueTxt}}</span>`
      : '';
    const dotColor = r==='V'?'#22c55e':r==='E'?'#fbbf24':'#ef4444';
    const liveEntry = typeof liveState !== 'undefined' && liveState[name];
    const liveClass = liveEntry ? ` live-${{r}}` : '';
    const _mh = venue2==='H' ? name : (opp||'');
    const _ma = venue2==='A' ? name : (opp||'');
    const _ca = (opp&&venue2) ? ` data-home="${{_mh}}" data-away="${{_ma}}" data-jornada="${{currentRound}}" onclick="openMatchStatsModal(this.dataset.home,this.dataset.away,+this.dataset.jornada)" title="Ver estadísticas del partido" style="cursor:pointer"` : '';
    return `<div class="result-card result-badge-${{r}}${{liveClass}}"${{_ca}}>
      <div class="team-cell" style="gap:8px">
        <div style="position:relative;flex-shrink:0">
          ${{crestHTML(name)}}
          <span style="position:absolute;bottom:-3px;right:-3px;width:14px;height:14px;border-radius:50%;background:${{dotColor}};border:1.5px solid var(--card);display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#000;line-height:1">${{r}}</span>
        </div>
        <div>
          <div class="result-team">${{name}}</div>
          <div class="result-detail" style="display:flex;align-items:center;gap:4px">${{lbl}}${{opp?` · ${{oppCrest}}<span>${{opp}}</span>`:''}} </div>
          <div style="display:flex;align-items:center;gap:5px;margin-top:3px;">${{scoreBadge}}${{venueTag}}</div>
        </div>
      </div>
    </div>`;
  }}).join('');
  renderHistoryTable();
}}
let resultsSortMode = 'clas'; // 'clas' | 'alfa'
function setResultsSort(mode) {{
  resultsSortMode = mode;
  document.querySelectorAll('[id^="rsort-"]').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('rsort-'+mode);
  if (btn) btn.classList.add('active');
  renderRoundResults();
}}
function changeRound(delta) {{
  document.getElementById('roundInput').value = currentRound + delta;
  renderRoundResults();
}}
function renderHistoryTable(sortBy) {{
  // Actualizar botones activos
  if (sortBy) {{
    document.querySelectorAll('.hist-sort-btn').forEach(b => b.classList.remove('active'));
    const btn = document.getElementById('hsort-'+sortBy);
    if (btn) btn.classList.add('active');
  }} else {{
    sortBy = 'clas';
  }}
  const tbl = document.getElementById('historyTable');
  const totalSeason = 42;
  const playedRounds = LIGA_DATA.total_rounds;
  const rounds = totalSeason;
  // Soporte para ambos formatos de scores_data.json
  const scMap    = SCORES_DATA.scores_by_team  || SCORES_DATA;
  const venueMap = SCORES_DATA.venue_by_team   || {{}};
  const hdrs = '<tr><th style="position:sticky;left:0;z-index:2;background:var(--card)">Equipo</th>' +
    Array.from({{length:rounds}},(_,i) => {{
      const isFut = i >= playedRounds;
      return `<th style="${{isFut ? 'opacity:.4;' : ''}}">${{isFut ? '<span style="font-size:9px;opacity:.7">J'+(i+1)+'</span>' : 'J'+(i+1)}}</th>`;
    }}).join('') + '</tr>';
  const oppsMap = LIGA_DATA.opponents_by_team || {{}};
  // Ordenar equipos según criterio
  const stdMap = {{}};
  computeStandings().forEach((t,i) => {{ stdMap[t.name] = i+1; }});
  const sortedTeams = [...LIGA_DATA.teams].sort((a,b) => {{
    if (sortBy==='alfa') return a.localeCompare(b,'es');
    if (sortBy==='wins') {{
      const wA = (LIGA_DATA.results_by_team[a]||[]).filter(r=>r==='V').length;
      const wB = (LIGA_DATA.results_by_team[b]||[]).filter(r=>r==='V').length;
      return wB - wA;
    }}
    if (sortBy==='loss') {{
      const lA = (LIGA_DATA.results_by_team[a]||[]).filter(r=>r==='D').length;
      const lB = (LIGA_DATA.results_by_team[b]||[]).filter(r=>r==='D').length;
      return lB - lA;
    }}
    // 'clas' por defecto
    return (stdMap[a]||99) - (stdMap[b]||99);
  }});
  const rows = sortedTeams.map(name => {{
    const res = LIGA_DATA.results_by_team[name] || [];
    const opps = oppsMap[name] || [];
    const teamScores = scMap[name]   || {{}};
    const teamVenues = venueMap[name] || {{}};
    const cells = Array.from({{length:rounds}},(_,i)=>{{
      if (i >= playedRounds) {{
        const oppF  = opps[i];
        if (oppF) {{
          const badgeF = TEAM_BADGES[oppF];
          const innerF = badgeF
            ? `<img src="${{badgeF}}" alt="${{oppF}}" width="14" height="14" style="opacity:.4;filter:grayscale(.3)" onerror="this.style.display='none'">`
            : `<span style="font-size:8px;color:var(--muted);opacity:.6">${{oppF.substring(0,3).toUpperCase()}}</span>`;
          return `<td class="cell-future" title="J${{i+1}} \u00b7 vs ${{oppF}}">${{innerF}}</td>`;
        }}
        return `<td class="cell-future" title="J${{i+1}} \u00b7 Sin jugar"><span style="font-size:9px;color:var(--muted)">\u2013</span></td>`;
      }}
      const r = res[i];
      if (!r) return '<td class="cell-empty">\u00b7</td>';
      const opp    = opps[i];
      const score  = teamScores[String(i)];
      const venue  = teamVenues[String(i)];
      const lbl      = r==='V'?'Victoria':r==='E'?'Empate':'Derrota';
      const venueTxt = venue==='H' ? 'Casa' : venue==='A' ? 'Fuera' : '';
      // El marcador se guarda como equipo-rival; si es visitante, invertirlo a local-visitante
      let displayScore = score;
      if (score && venue==='A') {{
        const p = score.split('-');
        if (p.length===2) displayScore = p[1]+'-'+p[0];
      }}
      const scoreTxt = displayScore ? ` ${{displayScore}}` : '';
      const oppTxt   = opp ? ` | vs ${{opp}}` : '';
      const tip      = venueTxt
        ? `${{lbl}}${{scoreTxt}} | ${{venueTxt}}${{oppTxt}}`
        : `${{lbl}}${{scoreTxt}}${{oppTxt}}`;
      const badge  = opp ? TEAM_BADGES[opp] : null;
      const inner  = badge
        ? `<img src="${{badge}}" alt="${{opp}}" width="18" height="18" onerror="this.style.display='none'">`
        : `<span style="font-size:10px;font-weight:700">${{r}}</span>`;
      return `<td class="cell-${{r}}" title="${{tip}}">${{inner}}</td>`;
    }}).join('');
    return `<tr><td style="position:sticky;left:0;background:var(--card);z-index:1;font-size:11px;padding:3px 8px;white-space:nowrap">${{name}}</td>${{cells}}</tr>`;
  }}).join('');
  tbl.innerHTML = '<thead>' + hdrs + '</thead><tbody>' + rows + '</tbody>';
}}

// ===== PREDICCIONES DINÁMICAS =====
// Calcula porcentajes según posición actual y jornadas restantes (sin datos externos)
function computePredForTeam(pos, quedanPts, totalPts) {{
  const progress = Math.min(1, 1 - quedanPts / totalPts);
  // Base por posición
  let base;
  if      (pos === 1) base = {{ascenso:78, playoff:16, permanencia: 5, descenso: 1}};
  else if (pos === 2) base = {{ascenso:58, playoff:28, permanencia:12, descenso: 2}};
  else if (pos === 3) base = {{ascenso:22, playoff:56, permanencia:20, descenso: 2}};
  else if (pos === 4) base = {{ascenso:12, playoff:62, permanencia:24, descenso: 2}};
  else if (pos <= 6)  base = {{ascenso: 5, playoff:58, permanencia:35, descenso: 2}};
  else if (pos <= 9)  base = {{ascenso: 1, playoff:20, permanencia:75, descenso: 4}};
  else if (pos <= 13) base = {{ascenso: 0, playoff: 8, permanencia:83, descenso: 9}};
  else if (pos <= 15) base = {{ascenso: 0, playoff: 2, permanencia:76, descenso:22}};
  else if (pos <= 17) base = {{ascenso: 0, playoff: 1, permanencia:62, descenso:37}};
  else if (pos === 18)base = {{ascenso: 0, playoff: 0, permanencia:48, descenso:52}};
  else if (pos === 19)base = {{ascenso: 0, playoff: 0, permanencia:30, descenso:70}};
  else if (pos === 20)base = {{ascenso: 0, playoff: 0, permanencia:18, descenso:82}};
  else                base = {{ascenso: 0, playoff: 0, permanencia: 9, descenso:91}};
  // Amplificar certeza con el avance de temporada
  const amp = progress * 0.55;
  const dominant = Object.keys(base).reduce((a,b) => base[a]>base[b]?a:b);
  for (const k of Object.keys(base)) {{
    if (k === dominant) base[k] = Math.min(100, Math.round(base[k] + (100-base[k])*amp));
    else                base[k] = Math.max(0,   Math.round(base[k] * (1-amp)));
  }}
  // Normalizar a 100
  let total = Object.values(base).reduce((a,b)=>a+b,0);
  if (total !== 100) base[dominant] += (100-total);
  return base;
}}

function renderPredictions() {{
  const standings = computeStandings().map((t,i) => ({{...t, pos: i+1}}));
  const el = document.getElementById('predictionsTable');
  if (!el) return;
  const zoneColor = (pos) => pos<=2?'#22c55e':pos<=6?'#fbbf24':pos<=18?'#6b7280':'#ef4444';
  el.innerHTML = standings.map(t => {{
    const pred = TEAM_PREDICTIONS[t.name] || {{ascenso:0,playoff:0,permanencia:100,descenso:0}};
    const zc = zoneColor(t.pos);
    const seg = (val, color, textColor) => val > 0
      ? `<div class="pred-seg" style="flex:${{val}};background:${{color}};color:${{textColor}}">${{val>=6?val+'%':''}}</div>`
      : '';
    return `<div class="pred-row">
      <div class="pred-team">
        <div class="zone-badge-sm" style="background:${{zc}}"></div>
        ${{crestHTML(t.name, 24)}}
        <span class="pred-team-name">${{t.name}}</span>
      </div>
      <div class="pred-bars">
        ${{seg(pred.ascenso,   '#22c55e', '#000')}}
        ${{seg(pred.playoff,   '#fbbf24', '#000')}}
        ${{seg(pred.permanencia,'#6b7280', '#fff')}}
        ${{seg(pred.descenso,  '#ef4444', '#fff')}}
      </div>
      <div class="pred-pos">#${{t.pos}}</div>
    </div>`;
  }}).join('');
  // Init histórico en primera carga
  if (!predHistTeam) predHistTeam = LIGA_DATA.teams[0];
  initPredHistSelector();
  buildPredHistChart();
}}

// ===== PREDICCIONES HISTÓRICAS =====
let predHistChart = null;
let predHistTeam  = '';
let predHistMode  = 'pos';

function initPredHistSelector() {{
  const el = document.getElementById('predHistSelector');
  if (!el) return;
  el.innerHTML = LIGA_DATA.teams.map(name => {{
    const badge = TEAM_BADGES[name];
    const color = getColor(name);
    const sel   = name === predHistTeam;
    const opacity = sel ? '1' : '0.35';
    const img = badge
      ? `<img src="${{badge}}" alt="${{name}}" style="width:32px;height:32px;object-fit:contain;opacity:${{opacity}};filter:drop-shadow(0 0 4px ${{color}}88)">`
      : `<div style="width:32px;height:32px;border-radius:50%;background:${{color}};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;opacity:${{opacity}}">${{getInitials(name)}}</div>`;
    return `<div class="team-check-badge ${{sel?'badge-sel':''}}" onclick="selectPredHistTeam('${{name}}')" title="${{name}}" style="cursor:pointer">${{img}}</div>`;
  }}).join('');
}}

function selectPredHistTeam(name) {{
  predHistTeam = name;
  initPredHistSelector();
  buildPredHistChart();
}}

function switchPredHistMode(mode) {{
  predHistMode = mode;
  document.querySelectorAll('[id^="phcTab-"]').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('phcTab-' + mode);
  if (btn) btn.classList.add('active');
  buildPredHistChart();
}}

function buildPredHistChart() {{
  const teamHist = PRED_HISTORY[predHistTeam] || {{}};
  const rounds   = LIGA_DATA.total_season_rounds;
  const labels   = Array.from({{length: rounds}}, (_, i) => 'J' + (i + 1));
  const asc = [], play = [], perm = [], desc = [], lineData = [];
  const posArr = LIGA_DATA.positions_by_team[predHistTeam] || [];
  const ptsArr = LIGA_DATA.points_by_team[predHistTeam]    || [];
  for (let i = 0; i < rounds; i++) {{
    const p = teamHist[String(i)];
    // Jornadas sin datos (futuras) se muestran vacías
    desc.push(p ? (p.descenso    || 0) : null);
    perm.push(p ? (p.permanencia || 0) : null);
    play.push(p ? (p.playoff     || 0) : null);
    asc.push( p ? (p.ascenso     || 0) : null);
    lineData.push(predHistMode === 'pos' ? (posArr[i] ?? null) : (ptsArr[i] ?? null));
  }}
  if (predHistChart) predHistChart.destroy();
  const canvas = document.getElementById('predHistCanvas');
  if (!canvas) return;
  const isPos = predHistMode === 'pos';
  const n = LIGA_DATA.teams.length;
  const teamColor = getColor(predHistTeam);
  predHistChart = new Chart(canvas.getContext('2d'), {{
    data: {{
      labels,
      datasets: [
        {{ type:'bar',  label:'Descenso',    data:desc, backgroundColor:'rgba(239,68,68,.70)',   stack:'pred', barPercentage:1, categoryPercentage:1, order:2 }},
        {{ type:'bar',  label:'Permanencia', data:perm, backgroundColor:'rgba(100,116,139,.55)', stack:'pred', barPercentage:1, categoryPercentage:1, order:2 }},
        {{ type:'bar',  label:'Playoff',     data:play, backgroundColor:'rgba(251,191,36,.72)',  stack:'pred', barPercentage:1, categoryPercentage:1, order:2 }},
        {{ type:'bar',  label:'Ascenso',     data:asc,  backgroundColor:'rgba(34,197,94,.72)',   stack:'pred', barPercentage:1, categoryPercentage:1, order:2 }},
        {{ type:'line', label: isPos ? 'Posición' : 'Puntos',
           data: lineData, yAxisID:'y2',
           borderColor: teamColor,
           backgroundColor: teamColor + '22',
           borderWidth: 2.5,
           pointRadius: 2,
           pointBackgroundColor: teamColor,
           tension: 0.3,
           fill: false,
           order: 1
        }}
      ]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ display: true, position: 'top',
          labels: {{ color: '#94a3b8', boxWidth: 12, font: {{size: 11}} }}
        }},
        tooltip: {{
          callbacks: {{
            label: c => c.dataset.type === 'bar'
              ? ` ${{c.dataset.label}}: ${{c.parsed.y}}%`
              : ` ${{c.dataset.label}}: ${{isPos ? '#' : ''}}${{c.parsed.y}}${{isPos ? 'º' : ' pts'}}`
          }}
        }}
      }},
      scales: {{
        x: {{ stacked: true, grid: {{ display: false }},
              ticks: {{ color: '#94a3b8', maxTicksLimit: 20 }} }},
        y: {{ stacked: true, min: 0, max: 100, display: false }},
        y2: {{
          type: 'linear', position: 'left',
          reverse: isPos,
          min: isPos ? 1 : 0,
          max: isPos ? n : undefined,
          grid: {{ color: '#2d3f5f44' }},
          ticks: {{ color: '#94a3b8', stepSize: isPos ? 2 : 10 }},
          title: {{ display: true, text: isPos ? 'Posición' : 'Puntos',
                    color: '#94a3b8', font: {{size: 10}} }}
        }}
      }}
    }}
  }});
}}

// ===== FORM MODE =====
function setFormMode(n) {{
  formMode = n;
  document.querySelectorAll('.btn-form').forEach(b => b.classList.remove('active'));
  const id = n === 0 ? 'fmtAll' : 'fmt' + n;
  const btn = document.getElementById(id);
  if (btn) btn.classList.add('active');
  sortCol = 'pos'; sortAsc = true;
  renderStandings();
}}

// ===== ANÁLISIS TAB =====
let scatterChart = null;
let localVisitanteChart = null;
let radarChart = null;
let consistenciaChart = null;
let bumpChart = null;
let _radarSelected = [];
let _scatterBadgeImgs = {{}};
let rankingMode = 'off';

// ===== HISTORIA =====
var _historiaActiveSeason = null;

function renderHistoria() {{
  const el = document.getElementById('historiaContent');
  if (!el) return;
  const seasons = HISTORY_DATA.seasons || {{}};
  const labels = Object.keys(seasons).sort().reverse(); // más reciente primero

  if (!labels.length) {{
    el.innerHTML = '<div class="card"><div class="playoff-pending">📜 No hay datos de temporadas anteriores todavía. Ejecuta fetch_history.py para importarlos.</div></div>';
    return;
  }}

  if (!_historiaActiveSeason || !seasons[_historiaActiveSeason]) {{
    _historiaActiveSeason = labels[0];
  }}

  // ── Selector de temporada ───────────────────────────────────────────────
  var html = '<div class="card">';
  html += '<div class="card-title">📜 Temporadas Anteriores</div>';
  html += '<div class="historia-season-selector">';
  for (var i = 0; i < labels.length; i++) {{
    var lbl = labels[i];
    var ac  = lbl === _historiaActiveSeason ? ' active' : '';
    html += '<button class="historia-season-btn' + ac + '" data-season="' + lbl + '">' + lbl + '</button>';
  }}
  html += '</div>';

  // ── Tabla de clasificación ──────────────────────────────────────────────
  var sd = seasons[_historiaActiveSeason];
  var st = sd.final_standings || [];
  var maxPts = st.length ? st[0].pts : 1;

  html += '<div style="overflow-x:auto;">';
  html += '<table class="historia-table">';
  html += '<thead><tr>';
  html += '<th>#</th><th>Equipo</th><th>PJ</th><th>PG</th><th>PE</th><th>PP</th>';
  html += '<th>GF</th><th>GC</th><th>DIF</th><th>Pts</th><th></th>';
  html += '</tr></thead><tbody>';

  for (var j = 0; j < st.length; j++) {{
    var t   = st[j];
    var pos = j + 1;
    var n   = st.length;
    // Color de posición
    var posCls = pos <= 2 ? 'pos-asc' : pos <= 6 ? 'pos-play' : pos >= n - 3 ? 'pos-rel' : '';
    if (pos === 1) posCls = 'pos-1';
    if (pos === 2) posCls = 'pos-2';
    if (pos === 3) posCls = 'pos-3';

    var badge = TEAM_BADGES[t.name] || '';
    var crest = badge
      ? '<img src="' + badge + '" alt="' + t.name + '" style="width:18px;height:18px;object-fit:contain;">'
      : '';
    var dv = t.gd || (t.gf - t.gc) || 0;
    var dvStr = dv > 0 ? '+' + dv : String(dv);
    var dvColor = dv > 0 ? 'var(--win)' : dv < 0 ? 'var(--loss)' : 'var(--muted)';
    var barW = Math.round((t.pts / maxPts) * 100);

    html += '<tr>';
    html += '<td><span class="historia-pos-badge ' + posCls + '">' + pos + '</span></td>';
    html += '<td><div class="historia-team-row">' + crest + '<span>' + t.name + '</span></div></td>';
    html += '<td>' + (t.played || 0) + '</td>';
    html += '<td style="color:var(--win)">' + (t.wins || 0) + '</td>';
    html += '<td style="color:var(--draw)">' + (t.draws || 0) + '</td>';
    html += '<td style="color:var(--loss)">' + (t.losses || 0) + '</td>';
    html += '<td>' + (t.gf || 0) + '</td>';
    html += '<td>' + (t.gc || 0) + '</td>';
    html += '<td style="color:' + dvColor + '">' + dvStr + '</td>';
    html += '<td style="font-weight:700;color:var(--accent)">' + t.pts + '</td>';
    html += '<td><div class="historia-pts-bar-wrap"><div class="historia-pts-bar" style="width:' + barW + '%"></div></div></td>';
    html += '</tr>';
  }}
  html += '</tbody></table></div>';
  html += '</div>'; // .card

  // ── Evolución de equipos actuales a lo largo de las temporadas ──────────
  var currentTeams = LIGA_DATA.teams || [];
  // Solo mostrar equipos que aparezcan en al menos una temporada histórica
  var histTeams = [];
  for (var k = 0; k < currentTeams.length; k++) {{
    var tn = currentTeams[k];
    var appearsInHistory = false;
    for (var li = 0; li < labels.length; li++) {{
      var lst = (seasons[labels[li]].final_standings || []);
      for (var si = 0; si < lst.length; si++) {{
        if (lst[si].name === tn) {{ appearsInHistory = true; break; }}
      }}
      if (appearsInHistory) break;
    }}
    if (appearsInHistory) histTeams.push(tn);
  }}

  if (histTeams.length > 0) {{
    html += '<div class="card" style="margin-top:16px;">';
    html += '<div class="card-title" style="margin-bottom:12px">📊 Evolución por temporada</div>';
    html += '<div style="font-size:11px;color:var(--muted);margin-bottom:12px">Posición final de cada equipo en cada temporada histórica disponible.</div>';
    html += '<div style="overflow-x:auto;">';
    html += '<table class="historia-table">';
    html += '<thead><tr><th>Equipo</th>';
    for (var li = 0; li < labels.length; li++) html += '<th>' + labels[li] + '</th>';
    html += '<th>Actual</th></tr></thead><tbody>';

    for (var k = 0; k < histTeams.length; k++) {{
      var tn = histTeams[k];
      var badge2 = TEAM_BADGES[tn] || '';
      var crest2 = badge2
        ? '<img src="' + badge2 + '" alt="' + tn + '" style="width:16px;height:16px;object-fit:contain;">'
        : '';
      html += '<tr><td><div class="historia-team-row">' + crest2 + '<span>' + tn + '</span></div></td>';

      for (var li = 0; li < labels.length; li++) {{
        var lst = (seasons[labels[li]].final_standings || []);
        var found = null;
        for (var si = 0; si < lst.length; si++) {{
          if (lst[si].name === tn) {{ found = si + 1; break; }}
        }}
        if (found === null) {{
          html += '<td style="color:var(--muted);font-size:10px">—</td>';
        }} else {{
          var pc = found <= 2 ? 'pos-asc' : found <= 6 ? 'pos-play' : found >= lst.length - 3 ? 'pos-rel' : '';
          if (found === 1) pc = 'pos-1';
          if (found === 2) pc = 'pos-2';
          if (found === 3) pc = 'pos-3';
          html += '<td><span class="historia-pos-badge ' + pc + '">' + found + '</span></td>';
        }}
      }}

      // Posición actual en temporada en curso
      var curStandings = computeStandings();
      var curPos = null;
      for (var ci = 0; ci < curStandings.length; ci++) {{
        if (curStandings[ci].name === tn) {{ curPos = ci + 1; break; }}
      }}
      if (curPos === null) {{
        html += '<td style="color:var(--muted);font-size:10px">—</td>';
      }} else {{
        var cpc = curPos <= 2 ? 'pos-asc' : curPos <= 6 ? 'pos-play' : curPos >= curStandings.length - 3 ? 'pos-rel' : '';
        if (curPos === 1) cpc = 'pos-1';
        if (curPos === 2) cpc = 'pos-2';
        if (curPos === 3) cpc = 'pos-3';
        html += '<td style="font-weight:700"><span class="historia-pos-badge ' + cpc + '">' + curPos + '</span></td>';
      }}
      html += '</tr>';
    }}
    html += '</tbody></table></div></div>';
  }}

  el.innerHTML = html;
  el.querySelectorAll('.historia-season-btn').forEach(function(btn) {{
    btn.addEventListener('click', function() {{
      _historiaActiveSeason = this.getAttribute('data-season');
      renderHistoria();
    }});
  }});
}}

// ===== PLAYOFF BRACKET =====
function renderPlayoff() {{
  const el = document.getElementById('playoffContent');
  if (!el) return;
  const po = LIGA_DATA.playoff;

  // ── Helpers compartidos ────────────────────────────────────────────────────
  function crest(name, sz) {{
    sz = sz || 20;
    const bd = TEAM_BADGES[name] || '';
    if (!bd) return '<span style="font-size:10px;opacity:.5">' + (name||'?').substring(0,3).toUpperCase() + '</span>';
    return '<img src="' + bd + '" alt="' + name + '" style="width:' + sz + 'px;height:' + sz + 'px;object-fit:contain;flex-shrink:0;">';
  }}

  function tieHTML(tie, label) {{
    var legs = tie.matches;
    var winner = tie.winner;
    var agg    = tie.agg;
    var html = '<div class="playoff-tie">';
    html += '<div class="playoff-tie-header">' + label + '</div>';
    for (var i = 0; i < legs.length; i++) {{
      var m = legs[i];
      var legNum = m.leg || (i + 1);
      var legLbl = legNum === 1 ? 'IDA' : 'VUELTA';
      var homeW = winner && m.home === winner;
      var awayW = winner && m.away === winner;
      var homeCls = homeW ? 'winner' : (winner && !homeW ? 'loser' : '');
      var awayCls = awayW ? 'winner' : (winner && !awayW ? 'loser' : '');
      var scoreDisp = m.played ? ('<strong>' + (m.score || '') + '</strong>') : (m.home ? '<span style="opacity:.4;font-size:11px">por jugar</span>' : '<span style="opacity:.3;font-size:11px">\u2013</span>');
      var dateLbl = m.date ? '<span style="font-size:10px;color:var(--muted);margin-left:4px">(' + m.date + ')</span>' : '';
      html += '<div class="playoff-match">';
      html += '<span style="font-size:9px;font-weight:700;color:var(--muted);letter-spacing:.5px;min-width:36px;margin-right:4px">' + legLbl + '</span>';
      html += '<div class="playoff-team ' + homeCls + '">' + crest(m.home, 18) + '<span>' + (m.home || '?') + '</span>' + dateLbl + '</div>';
      html += '<div class="playoff-score">' + scoreDisp + '</div>';
      html += '<div class="playoff-team ' + awayCls + '" style="justify-content:flex-end;text-align:right">' + crest(m.away, 18) + '<span>' + (m.away || '?') + '</span></div>';
      html += '</div>';
    }}
    if (agg) {{
      var aggWinner = winner || '';
      html += '<div class="playoff-agg decided" style="margin-top:6px;padding:6px 10px;border-radius:6px;background:rgba(255,255,255,.05);display:flex;align-items:center;gap:8px;">';
      html += '<span style="font-size:11px;color:var(--muted)">Global:</span>';
      html += '<span style="font-weight:800;font-size:15px;color:var(--text)">' + agg + '</span>';
      if (aggWinner) html += '<span style="font-size:11px;color:var(--muted)">\u00b7 Pasa:</span><strong style="font-size:12px;color:var(--text)">' + aggWinner + '</strong>';
      html += '</div>';
    }} else {{
      html += '<div class="playoff-agg">Eliminatoria a doble partido</div>';
    }}
    html += '</div>';
    return html;
  }}

  if (!po) {{
    if (_historicalMode) {{
      // Sin datos de playoff — solo mostrar clasificación
      var st = LIGA_DATA.final_standings || [];
      var html2 = '<div class="card"><div class="card-title">🏆 Ascenso Directo</div>';
      st.slice(0,2).forEach(function(t,i) {{
        var bd = TEAM_BADGES[t.name]||'';
        var cr = bd?'<img src="'+bd+'" alt="'+t.name+'" style="width:24px;height:24px;object-fit:contain;">':'<span style="font-size:10px;color:var(--muted)">'+t.name.substring(0,3).toUpperCase()+'</span>';
        html2+='<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)"><span style="width:22px;text-align:center;font-size:12px;font-weight:700;color:var(--muted)">'+(i+1)+'</span>'+cr+'<span style="flex:1;font-weight:600">'+t.name+'</span><span style="font-size:11px;color:var(--muted)">'+t.pts+' pts</span><span style="font-size:10px;padding:2px 8px;border-radius:10px;background:var(--win);color:#0a0a0a;font-weight:700;margin-left:6px">ASCENSO DIRECTO</span></div>';
      }});
      html2 += '</div>';
      el.innerHTML = html2;
      return;
    }}
    el.innerHTML = '<div class="card"><div class="playoff-pending">🏆 El playoff de ascenso comenzará al finalizar la jornada 42.</div></div>';
    return;
  }}

  var html = '';

  // ── Modo histórico: ascenso directo + ganador del playoff + bracket ────────
  if (_historicalMode) {{
    var st = LIGA_DATA.final_standings || [];
    var currentLabel = LIGA_DATA.label || '';

    // Bloque ascenso directo
    html += '<div class="card" style="margin-bottom:16px;">';
    html += '<div class="card-title">🏆 Ascenso Directo</div>';
    st.slice(0,2).forEach(function(t,i) {{
      var bd = TEAM_BADGES[t.name]||'';
      var cr = bd?'<img src="'+bd+'" alt="'+t.name+'" style="width:24px;height:24px;object-fit:contain;">':'<span style="font-size:10px;color:var(--muted)">'+t.name.substring(0,3).toUpperCase()+'</span>';
      html+='<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)"><span style="width:22px;text-align:center;font-size:12px;font-weight:700;color:var(--muted)">'+(i+1)+'</span>'+cr+'<span style="flex:1;font-weight:600">'+t.name+'</span><span style="font-size:11px;color:var(--muted)">'+t.pts+' pts</span><span style="font-size:10px;padding:2px 8px;border-radius:10px;background:var(--win);color:#0a0a0a;font-weight:700;margin-left:6px">ASCENSO DIRECTO</span></div>';
    }});
    html += '</div>';

    // Banner ganador del playoff
    var playoffWinner = (po.final && po.final.winner) || HIST_PLAYOFF_WINNERS[currentLabel] || null;
    if (playoffWinner) {{
      var pwBd = TEAM_BADGES[playoffWinner] || '';
      var pwCrest = pwBd ? '<img src="' + pwBd + '" alt="' + playoffWinner + '" style="width:44px;height:44px;object-fit:contain;flex-shrink:0;">'
                         : '<span style="font-size:18px;font-weight:700;color:var(--muted)">' + playoffWinner.substring(0,3).toUpperCase() + '</span>';
      var pwKf = TEAM_KIT_FULL[playoffWinner] || {{}};
      var pwColor = pwKf.primary || getColor(playoffWinner) || '#f5c500';
      html += '<div class="card" style="margin-bottom:16px;background:linear-gradient(135deg,' + pwColor + '22,' + pwColor + '44);border:2px solid ' + pwColor + '88;">';
      html += '<div class="card-title" style="color:' + pwColor + '">\U0001f389 Ganador del Playoff \u00b7 Ascendido</div>';
      html += '<div style="display:flex;align-items:center;gap:14px;padding:8px 0;">';
      html += '<div style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;">' + pwCrest + '</div>';
      html += '<div><div style="font-size:20px;font-weight:800;color:var(--text)">' + playoffWinner + '</div>';
      html += '<div style="font-size:11px;color:var(--muted);margin-top:2px">Ascenso vía playoff \u00b7 ' + currentLabel + '</div></div>';
      html += '</div></div>';
    }}

    // Bracket completo igual que temporada actual
    html += '<div class="card" style="margin-bottom:16px;">';
    html += '<div class="card-title">\u26a1 Playoff de Ascenso</div>';
    html += '<div style="font-size:12px;color:var(--muted);margin-bottom:12px">3\u00ba-6\u00ba \u00b7 4\u00ba-5\u00ba \u00b7 Final \u00b7 Doble partido \u00b7 Pasa el mejor global</div>';

    var sf1h = po.semis[0], sf2h = po.semis[1], finh = po.final;
    function sfLabelH(sf) {{
      var h = sf.team_high || '?', l = sf.team_low || '?';
      return crest(h,16) + ' <span>' + h + '</span><span style="color:var(--muted);margin:0 6px">vs</span>' + crest(l,16) + ' <span>' + l + '</span>';
    }}
    var finHh = finh.matches[0] ? finh.matches[0].home : (sf1h.winner || '?');
    var finAh = finh.matches[0] ? finh.matches[0].away : (sf2h.winner || '?');

    html += '<div class="playoff-bracket">';
    html += '<div class="playoff-column">';
    html += '<div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Semifinales</div>';
    html += tieHTML(sf1h, sfLabelH(sf1h));
    html += '<div style="height:8px"></div>';
    html += tieHTML(sf2h, sfLabelH(sf2h));
    html += '</div>';
    html += '<div class="playoff-connector"><span>\u2192</span><span style="font-size:11px;color:var(--muted)">Ganadores</span><span>\u2192</span></div>';
    html += '<div class="playoff-column">';
    html += '<div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Final</div>';
    html += '<div class="playoff-final-box">';
    html += tieHTML(finh, crest(finHh,16) + ' <span>' + finHh + '</span><span style="color:var(--muted);margin:0 6px">vs</span>' + crest(finAh,16) + ' <span>' + finAh + '</span>');
    html += '</div></div>';
    html += '</div>'; // .playoff-bracket
    html += '</div>'; // .card

    el.innerHTML = html;
    return;
  }}

  var html = '';

  // ── Título ─────────────────────────────────────────────────────────────────
  html += '<div class="card" style="margin-bottom:16px;">';
  html += '<div class="card-title">🏆 Playoff de Ascenso</div>';
  html += '<div style="font-size:12px;color:var(--muted);margin-bottom:12px">3\u00ba-6\u00ba \u00b7 4\u00ba-5\u00ba \u00b7 Final \u00b7 Doble partido \u00b7 Pasa el mejor global</div>';

  // \u2500\u2500 Bracket \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
  // En temporada actual: aviso si las plazas todavia no estan decididas matematicamente
  var _provisional = false;
  if (!_historicalMode) {{
    const _st   = LIGA_DATA.final_standings || [];
    const _rem  = (LIGA_DATA.total_season_rounds||42) - (LIGA_DATA.total_rounds||0);
    const _pts6 = _st[5] ? _st[5].pts : 0;
    const _pts7 = _st[6] ? _st[6].pts : 0;
    _provisional = _rem > 0 && (_pts7 + _rem * 3 >= _pts6);
    if (_provisional) {{
      html += '<div style="margin-bottom:12px;background:rgba(250,204,21,.08);border:1px solid rgba(250,204,21,.3);border-radius:8px;padding:10px 14px;display:flex;align-items:center;gap:8px;">';
      html += '<span style="font-size:16px">\u23f3</span>';
      html += '<span style="font-size:12px;color:var(--muted)">Posiciones <strong style="color:#facc15">provisionales</strong> \u2014 quedan <strong style="color:#facc15">' + _rem + '</strong> jornada' + (_rem===1?'':'s') + ' \u00b7 Los equipos pueden cambiar</span>';
      html += '</div>';
    }}
  }}
  var sf1 = po.semis[0];
  var sf2 = po.semis[1];
  var fin = po.final;

  // Etiqueta dinámica de la semifinal
  function sfLabel(sf) {{
    var h = sf.team_high || '?', l = sf.team_low || '?';
    var prov = _provisional ? ' <span style="font-size:9px;color:#facc15;font-weight:700;opacity:.85">(provisional)</span>' : '';
    return crest(h,16) + ' <span>' + h + prov + '</span><span style="color:var(--muted);margin:0 6px">vs</span>' + crest(l,16) + ' <span>' + l + prov + '</span>';
  }}

  html += '<div class="playoff-bracket">';

  // Columna izquierda: semifinales
  html += '<div class="playoff-column">';
  html += '<div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Semifinales</div>';
  html += tieHTML(sf1, sfLabel(sf1));
  html += '<div style="height:8px"></div>';
  html += tieHTML(sf2, sfLabel(sf2));
  html += '</div>';

  // Conector central
  html += '<div class="playoff-connector"><span>\u2192</span><span style="font-size:11px;color:var(--muted)">Ganadores</span><span>\u2192</span></div>';

  // Columna derecha: final
  var finH = fin.matches[0]?.home || sf1.winner || '?';
  var finA = fin.matches[0]?.away || sf2.winner || '?';
  html += '<div class="playoff-column">';
  html += '<div style="font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Final</div>';
  html += '<div class="playoff-final-box">';
  html += tieHTML(fin, crest(finH,16) + ' <span>' + finH + '</span><span style="color:var(--muted);margin:0 6px">vs</span>' + crest(finA,16) + ' <span>' + finA + '</span>');
  // Banner ganador — usa ganador scrapeado o fallback HIST_PLAYOFF_WINNERS
  var resolvedWinner = fin.winner;
  if (!resolvedWinner && _historicalMode) {{
    var _curLabel = LIGA_DATA.label || '';
    resolvedWinner = HIST_PLAYOFF_WINNERS[_curLabel] || null;
  }}
  if (resolvedWinner) {{
    var winLabel = _historicalMode ? 'Ascendido a Primera' : 'Asciende a Primera';
    html += '<div class="playoff-winner-banner">' + crest(resolvedWinner, 28) + '\U0001f389 ' + resolvedWinner + ' \u00b7 ' + winLabel + '</div>';
  }}
  html += '</div>';
  html += '</div>';

  html += '</div>'; // .playoff-bracket
  html += '</div>'; // .card

  el.innerHTML = html;
}}

// ===== ANÁLISIS: SELECTOR DE EQUIPOS =====
let analisisFilter = new Set(); // vacío = todos visibles

function buildAnalisisSelector() {{
  const el = document.getElementById('analisisTeamSelector');
  if (!el) return;
  const teams = computeStandings().map(t => t.name);
  el.innerHTML = teams.map(name => {{
    const color = getColor(name);
    const badge = TEAM_BADGES[name];
    const sel = analisisFilter.has(name) ? 'badge-sel' : '';
    const opacity = (analisisFilter.size === 0 || analisisFilter.has(name)) ? '1' : '0.35';
    const imgTag = badge
      ? `<img src="${{badge}}" alt="${{name}}" style="opacity:${{opacity}};filter:drop-shadow(0 0 4px ${{color}}99)">`
      : `<div style="width:32px;height:32px;border-radius:50%;background:${{color}};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;opacity:${{opacity}}">${{getInitials(name)}}</div>`;
    return `<label class="team-check-badge ${{sel}}" title="${{name}}">
      <input type="checkbox" value="${{name}}" ${{analisisFilter.has(name)?'checked':''}} onchange="toggleAnalisisTeam('${{name.replace(/'/g,"\\'")}}',this.checked)">
      ${{imgTag}}
    </label>`;
  }}).join('');
}}

function toggleAnalisisTeam(name, checked) {{
  if (checked) analisisFilter.add(name); else analisisFilter.delete(name);
  buildAnalisisSelector();
  applyAnalisisFilter();
}}
function analisisSelectTop(n) {{
  analisisFilter.clear();
  computeStandings().slice(0,n).forEach(t => analisisFilter.add(t.name));
  buildAnalisisSelector(); applyAnalisisFilter();
}}
function analisisSelectAll() {{
  analisisFilter.clear();
  buildAnalisisSelector(); applyAnalisisFilter();
}}
function analisisSelectNone() {{
  analisisFilter.clear();
  buildAnalisisSelector(); applyAnalisisFilter();
}}

function applyAnalisisFilter() {{
  const sel = analisisFilter;
  const none = sel.size === 0; // sin selección: todos al 100%

  // Dimear datasets en charts Chart.js
  // Para scatter: activos con escudo, inactivos como círculo oscuro pequeño
  if (scatterChart) {{
    scatterChart.data.datasets.forEach(ds => {{
      const name = ds.label;
      const active = none || sel.has(name);
      const img = _scatterBadgeImgs[name];
      if (active) {{
        ds.pointStyle      = img || 'circle';
        ds.pointRadius      = img ? 14 : 8;
        ds.pointHoverRadius = img ? 17 : 11;
        ds.backgroundColor  = img ? 'transparent' : getColor(name) + 'cc';
        ds.borderColor      = img ? 'transparent' : getColor(name);
      }} else {{
        ds.pointStyle      = 'circle';
        ds.pointRadius      = 4;
        ds.pointHoverRadius = 5;
        ds.backgroundColor  = getColor(name) + '22';
        ds.borderColor      = getColor(name) + '35';
      }}
    }});
    scatterChart.update('none');
  }}

  // Para local/visitante (bar chart con labels = equipos, 4 datasets fijos)
  if (localVisitanteChart) {{
    const lvLabels = localVisitanteChart.data.labels || [];
    const lvBaseColors = ['#39FF14','#00F5FF','#FF00FF','#FFE000'];
    const lvBaseBg     = ['#39FF1455','#00F5FF55','#FF00FF33','#FFE00033'];
    localVisitanteChart.data.datasets.forEach((ds, di) => {{
      const baseC  = lvBaseColors[di] || '#888';
      const baseBg = lvBaseBg[di] || '#88888844';
      ds.backgroundColor = lvLabels.map(name => (none || sel.has(name)) ? baseBg : baseBg.replace(/[\da-f]{{2}}\)$/i,'0a)'));
      ds.borderColor     = lvLabels.map(name => (none || sel.has(name)) ? baseC : baseC + '25');
    }});
    localVisitanteChart.update('none');
  }}

  // Dimear filas en tablas (rankings, escenarios, advStats)
  function dimTableRows(tableId) {{
    const tbody = document.querySelector(`#${{tableId}} tbody`) || document.getElementById(tableId);
    if (!tbody) return;
    tbody.querySelectorAll('tr').forEach(row => {{
      const nameCell = row.querySelector('.team-name-text');
      if (!nameCell) return;
      const name = nameCell.textContent.trim();
      row.style.opacity = (none || sel.has(name)) ? '' : '0.2';
    }});
  }}
  dimTableRows('standingsTable');
  dimTableRows('scenariosTable');
  dimTableRows('advStatsTable');
  ['rankingList'].forEach(id => {{
    const el = document.getElementById(id);
    if (!el) return;
    el.querySelectorAll('[data-team]').forEach(row => {{
      const name = row.getAttribute('data-team');
      row.style.opacity = (none || sel.has(name)) ? '' : '0.2';
    }});
  }});

  // Consistencia chart: opacidad de barras
  if (consistenciaChart) {{
    const baseColors = ['rgba(34,197,94,0.85)','rgba(245,158,11,0.85)','rgba(239,68,68,0.85)'];
    const dimColors  = ['rgba(34,197,94,0.12)','rgba(245,158,11,0.12)','rgba(239,68,68,0.12)'];
    consistenciaChart.data.datasets.forEach((ds, di) => {{
      ds.backgroundColor = consistenciaChart.data.labels.map(name => {{
        const active = none || sel.has(name);
        return active ? baseColors[di] : dimColors[di];
      }});
    }});
    consistenciaChart.update('none');
  }}

  // Radar: cuando hay selección, actualizar _radarSelected con los seleccionados (si caben ≤3)
  if (!none && sel.size > 0 && sel.size <= 3) {{
    _radarSelected = [...sel];
    buildRadarSelector();
    buildRadarChart();
  }}
}}

function initAnalysisTab() {{
  buildAnalisisSelector();
  // Siempre inicializar radar con top 3
  _radarSelected = computeStandings().slice(0, 3).map(t => t.name);
  buildScatterChart();
  renderRanking(rankingMode);
  renderScenarios();
  buildLocalVisitanteChart();
  if (!document.getElementById('h2hGrid').hasChildNodes()) renderH2H();
  buildAdvStatsTable();
  buildRadarSelector();
  buildRadarChart();
  buildConsistenciaChart();
}}

// ===== ADVANCED STATS (AS.com / Opta) =====
(function() {{
  // Calcular promedios por equipo a partir de AS_STATS[]
  function computeTeamAdvStats() {{
    const acc = {{}};
    const FIELDS = ['possession','shots_inside','shots_outside','shots_blocked',
                    'shots_received','fouls_committed','yellow_cards','red_cards',
                    'poss_losses','poss_recoveries','offsides'];
    const HOME_FIELDS = FIELDS.map(f => f + '_home');
    const AWAY_FIELDS = FIELDS.map(f => f + '_away');
    for (const m of AS_STATS) {{
      for (let i = 0; i < FIELDS.length; i++) {{
        const key = FIELDS[i];
        if (m.home) {{
          if (!acc[m.home]) acc[m.home] = {{ pj: 0 }};
          const v = m[HOME_FIELDS[i]];
          if (v !== undefined && v !== null) {{
            acc[m.home][key] = (acc[m.home][key] || 0) + v;
            acc[m.home]['_n_' + key] = (acc[m.home]['_n_' + key] || 0) + 1;
          }}
        }}
        if (m.away) {{
          if (!acc[m.away]) acc[m.away] = {{ pj: 0 }};
          const v = m[AWAY_FIELDS[i]];
          if (v !== undefined && v !== null) {{
            acc[m.away][key] = (acc[m.away][key] || 0) + v;
            acc[m.away]['_n_' + key] = (acc[m.away]['_n_' + key] || 0) + 1;
          }}
        }}
      }}
      if (m.home) acc[m.home].pj = (acc[m.home].pj || 0) + 1;
      if (m.away) acc[m.away].pj = (acc[m.away].pj || 0) + 1;
    }}
    // Calcular medias
    const result = [];
    for (const [name, d] of Object.entries(acc)) {{
      const row = {{ name, pj: d.pj }};
      for (const key of FIELDS) {{
        const n = d['_n_' + key] || 0;
        row[key] = n > 0 ? d[key] / n : null;
      }}
      result.push(row);
    }}
    return result;
  }}

  let _advData = null;
  let _advSortCol = 'shots_inside';
  let _advSortAsc = false;

  window.buildAdvStatsTable = function() {{
    if (_historicalMode) {{
      const card = document.getElementById('advStatsCard');
      if (card) card.style.display = 'none';
      return;
    }}
    const card = document.getElementById('advStatsCard');
    if (card) card.style.display = '';
    _advData = computeTeamAdvStats();
    renderAdvStats();
  }};

  window.sortAdvStats = function(th) {{
    const col = th.getAttribute('data-advcol');
    if (_advSortCol === col) {{ _advSortAsc = !_advSortAsc; }}
    else {{ _advSortCol = col; _advSortAsc = col === 'name'; }}
    renderAdvStats();
    // Actualizar indicador visual
    document.querySelectorAll('#advStatsTable th').forEach(h => {{
      h.style.color = '';
    }});
    th.style.color = 'var(--gold)';
  }};

  function renderAdvStats() {{
    if (!_advData) return;
    const tbody = document.getElementById('advStatsBody');
    if (!tbody) return;

    const data = [..._advData].sort((a, b) => {{
      const va = a[_advSortCol] ?? (_advSortAsc ? Infinity : -Infinity);
      const vb = b[_advSortCol] ?? (_advSortAsc ? Infinity : -Infinity);
      if (typeof va === 'string') return _advSortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
      return _advSortAsc ? va - vb : vb - va;
    }});

    // Calcular min/max de cada campo para heat coloring
    const FIELDS = ['possession','shots_inside','shots_outside','shots_blocked',
                    'shots_received','fouls_committed','yellow_cards','red_cards',
                    'poss_losses','poss_recoveries','offsides'];
    const minMax = {{}};
    for (const f of FIELDS) {{
      const vals = _advData.map(r => r[f]).filter(v => v !== null);
      minMax[f] = {{ min: Math.min(...vals), max: Math.max(...vals) }};
    }}

    // Campos donde mayor es mejor (verde arriba)
    const HIGHER_IS_BETTER = new Set(['possession','shots_inside','shots_outside','shots_blocked','poss_recoveries']);
    // Campos donde menor es mejor (verde abajo)
    // shots_received, fouls_committed, yellow_cards, red_cards, poss_losses, offsides

    function heatColor(field, value) {{
      if (value === null) return '';
      const {{ min, max }} = minMax[field];
      if (max === min) return '';
      const norm = (value - min) / (max - min); // 0=min, 1=max
      const isGoodHigh = HIGHER_IS_BETTER.has(field);
      // goodRatio: 1 = verde (mejor), 0 = rojo (peor)
      const goodRatio = isGoodHigh ? norm : 1 - norm;
      if (goodRatio > 0.66) return 'rgba(34,197,94,0.18)';
      if (goodRatio < 0.33) return 'rgba(239,68,68,0.18)';
      return '';
    }}

    function fmt(v, dec) {{
      if (v === null || v === undefined) return '<span style="color:var(--muted)">—</span>';
      return v.toFixed(dec ?? 1);
    }}

    tbody.innerHTML = data.map(row => {{
      const color = getColor(row.name);
      const cells = [
        ['possession',      fmt(row.possession, 1)],
        ['shots_inside',    fmt(row.shots_inside, 1)],
        ['shots_outside',   fmt(row.shots_outside, 1)],
        ['shots_blocked',   fmt(row.shots_blocked, 1)],
        ['shots_received',  fmt(row.shots_received, 1)],
        ['fouls_committed', fmt(row.fouls_committed, 1)],
        ['yellow_cards',    fmt(row.yellow_cards, 2)],
        ['red_cards',       fmt(row.red_cards, 2)],
        ['poss_losses',     fmt(row.poss_losses, 0)],
        ['poss_recoveries', fmt(row.poss_recoveries, 1)],
        ['offsides',        fmt(row.offsides, 1)],
      ];
      const tdCells = cells.map(([f, v]) => {{
        const bg = heatColor(f, row[f]);
        const style = bg ? ` style="background:${{bg}}"` : '';
        return `<td${{style}}>${{v}}</td>`;
      }}).join('');

      return `<tr style="background:linear-gradient(90deg,${{color}}18 0%,transparent 130px)">
        <td><div class="team-cell">${{crestHTML(row.name,22)}}<span class="team-name-text">${{row.name}}</span></div></td>
        ${{tdCells}}
        <td style="color:var(--muted);font-size:11px">${{row.pj}}</td>
      </tr>`;
    }}).join('');
  }}
}})();


// ===== RADAR CHART =====
function buildRadarSelector() {{
  const container = document.getElementById('radarTeamSelector');
  if (!container) return;
  const teams = computeStandings().map(t => t.name);
  // Default: top 3
  if (_radarSelected.length === 0) _radarSelected = teams.slice(0, 3);
  container.innerHTML = teams.map(name => {{
    const color = getColor(name);
    const active = _radarSelected.includes(name);
    const badge = TEAM_BADGES[name] ? `<img src="${{TEAM_BADGES[name]}}" style="width:14px;height:14px;object-fit:contain">` : '';
    return `<button class="radar-team-btn${{active?' active':''}}" style="${{active?`background:${{color}};`:''}}" onclick="toggleRadarTeam('${{name.replace(/'/g,"\\'")}}')">
      ${{badge}}<span>${{name}}</span>
    </button>`;
  }}).join('');
}}

function toggleRadarTeam(name) {{
  if (_radarSelected.includes(name)) {{
    if (_radarSelected.length === 1) return; // mínimo 1
    _radarSelected = _radarSelected.filter(n => n !== name);
  }} else {{
    if (_radarSelected.length >= 3) _radarSelected.shift(); // máximo 3, descarta el más viejo
    _radarSelected.push(name);
  }}
  buildRadarSelector();
  buildRadarChart();
}}

function computeRadarStats() {{
  const standings = computeStandings();
  const all = standings.map(t => {{
    const hw = computeHomeAwayStats(t.name);
    // Momentum: PPG últimas 5 jornadas
    const res = LIGA_DATA.results_by_team[t.name] || [];
    const last5 = res.slice(-5);
    const momPts = last5.reduce((s, r) => s + (r==='V'?3:r==='E'?1:0), 0);
    const momPpg = last5.length > 0 ? momPts / last5.length : 0;
    // Consistencia: desviación estándar de puntos por partido
    const pts_arr = res.map(r => r==='V'?3:r==='E'?1:0);
    const mean = pts_arr.length > 0 ? pts_arr.reduce((s,v)=>s+v,0)/pts_arr.length : 0;
    const variance = pts_arr.length > 1 ? pts_arr.reduce((s,v)=>s+(v-mean)**2,0)/(pts_arr.length-1) : 0;
    const stddev = Math.sqrt(variance);
    return {{
      name: t.name,
      attack: t.played > 0 ? t.gf / t.played : 0,
      defense: t.played > 0 ? t.gc / t.played : 0,   // menor = mejor
      home_ppg: hw.home_played > 0 ? hw.home_pts / hw.home_played : 0,
      away_ppg: hw.away_played > 0 ? hw.away_pts / hw.away_played : 0,
      consistency: stddev,  // menor = mejor
      momentum: momPpg,
    }};
  }});
  // Normalizar 0-100
  function norm(arr, invert) {{
    const vals = arr.filter(v => v !== null && !isNaN(v));
    const mn = Math.min(...vals), mx = Math.max(...vals);
    return arr.map(v => {{
      if (mn === mx) return 50;
      const n = (v - mn) / (mx - mn) * 100;
      return invert ? 100 - n : n;
    }});
  }}
  const attack_n      = norm(all.map(t => t.attack),      false);
  const defense_n     = norm(all.map(t => t.defense),     true);  // menos GC = mejor
  const home_n        = norm(all.map(t => t.home_ppg),    false);
  const away_n        = norm(all.map(t => t.away_ppg),    false);
  const consist_n     = norm(all.map(t => t.consistency), true);  // menor std = mejor
  const momentum_n    = norm(all.map(t => t.momentum),    false);
  return all.map((t, i) => ({{
    name: t.name,
    values: [attack_n[i], defense_n[i], home_n[i], away_n[i], consist_n[i], momentum_n[i]],
    raw: t,
  }}));
}}

function buildRadarChart() {{
  const ctx = document.getElementById('radarChart');
  if (!ctx) return;
  if (radarChart) radarChart.destroy();
  const allStats = computeRadarStats();
  const labels = ['Ataque', 'Defensa', 'Local', 'Visitante', 'Consistencia', 'Momentum'];
  const datasets = _radarSelected.map(name => {{
    const s = allStats.find(t => t.name === name);
    if (!s) return null;
    const color = getColor(name);
    return {{
      label: name,
      data: s.values,
      backgroundColor: color + '33',
      borderColor: color,
      borderWidth: 2,
      pointBackgroundColor: color,
      pointRadius: 4,
      pointHoverRadius: 6,
    }};
  }}).filter(Boolean);
  radarChart = new Chart(ctx.getContext('2d'), {{
    type: 'radar',
    data: {{ labels, datasets }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      scales: {{
        r: {{
          min: 0, max: 100,
          ticks: {{ stepSize: 25, color: '#94a3b8', font: {{size: 9}}, backdropColor: 'transparent' }},
          grid: {{ color: 'rgba(148,163,184,.2)' }},
          angleLines: {{ color: 'rgba(148,163,184,.2)' }},
          pointLabels: {{ color: '#f0f0f0', font: {{size: 12, weight: 'bold'}} }},
        }}
      }},
      plugins: {{
        legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', boxWidth: 12, font: {{size: 11}} }} }},
        tooltip: {{
          callbacks: {{
            label: function(c) {{
              const s = computeRadarStats().find(t => t.name === c.dataset.label);
              if (!s) return `${{c.dataset.label}}: ${{c.parsed.r.toFixed(0)}}`;
              const rawLabels = ['GF/p', 'GC/p', 'PPG casa', 'PPG fuera', 'StdDev', 'PPG ult5'];
              const rawVals = [
                s.raw.attack.toFixed(2), s.raw.defense.toFixed(2),
                s.raw.home_ppg.toFixed(2), s.raw.away_ppg.toFixed(2),
                s.raw.consistency.toFixed(2), s.raw.momentum.toFixed(2),
              ];
              return `${{c.dataset.label}} · ${{c.label}}: ${{c.parsed.r.toFixed(0)}} (${{rawLabels[c.dataIndex]}}=${{rawVals[c.dataIndex]}})`;
            }}
          }}
        }}
      }}
    }}
  }});
}}

// ===== CONSISTENCIA CHART =====
function buildConsistenciaChart() {{
  const ctx = document.getElementById('consistenciaChart');
  if (!ctx) return;
  if (consistenciaChart) consistenciaChart.destroy();
  const standings = computeStandings();
  // Ordenar por % victorias desc
  const data = standings.map(t => {{
    const res = LIGA_DATA.results_by_team[t.name] || [];
    const pj = res.length || 1;
    const wins   = res.filter(r=>r==='V').length;
    const draws  = res.filter(r=>r==='E').length;
    const losses = res.filter(r=>r==='D').length;
    return {{ name: t.name, pct_v: wins/pj*100, pct_e: draws/pj*100, pct_d: losses/pj*100, wins, draws, losses, pj: res.length }};
  }}).sort((a,b) => b.pct_v - a.pct_v);

  consistenciaChart = new Chart(ctx.getContext('2d'), {{
    type: 'bar',
    data: {{
      labels: data.map(d => d.name),
      datasets: [
        {{
          label: '% Victorias',
          data: data.map(d => +d.pct_v.toFixed(1)),
          backgroundColor: 'rgba(34,197,94,0.85)',
          borderColor: '#22c55e',
          borderWidth: 1,
        }},
        {{
          label: '% Empates',
          data: data.map(d => +d.pct_e.toFixed(1)),
          backgroundColor: 'rgba(245,158,11,0.85)',
          borderColor: '#f59e0b',
          borderWidth: 1,
        }},
        {{
          label: '% Derrotas',
          data: data.map(d => +d.pct_d.toFixed(1)),
          backgroundColor: 'rgba(239,68,68,0.85)',
          borderColor: '#ef4444',
          borderWidth: 1,
        }},
      ]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {{
        legend: {{ position: 'top', labels: {{ color: '#94a3b8', boxWidth: 12, font: {{size: 11}} }} }},
        tooltip: {{
          callbacks: {{
            label: c => {{
              const d = data[c.dataIndex];
              if (c.datasetIndex === 0) return ` Victorias: ${{d.wins}} (${{d.pct_v.toFixed(1)}}%)`;
              if (c.datasetIndex === 1) return ` Empates: ${{d.draws}} (${{d.pct_e.toFixed(1)}}%)`;
              return ` Derrotas: ${{d.losses}} (${{d.pct_d.toFixed(1)}}%)`;
            }},
            title: items => `${{items[0].label}} · ${{data[items[0].dataIndex].pj}} partidos`
          }}
        }}
      }},
      scales: {{
        x: {{
          stacked: true,
          max: 100,
          grid: {{ color: '#2d3f5f44' }},
          ticks: {{ color: '#94a3b8', font: {{size: 10}}, callback: v => v+'%' }},
          title: {{ display: true, text: '% partidos', color: '#64748b', font: {{size: 10}} }}
        }},
        y: {{ stacked: true, grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{size: 10}} }} }}
      }}
    }}
  }});
}}

// ===== BUMP CHART =====
function buildBumpChart() {{
  const ctx = document.getElementById('bumpChart');
  if (!ctx) return;
  if (bumpChart) bumpChart.destroy();
  const totalRounds = LIGA_DATA.total_rounds;
  const teams = LIGA_DATA.teams;
  // Calcular posición de cada equipo en cada jornada
  const posMatrix = {{}};  // posMatrix[team][round] = position
  for (let r = 1; r <= totalRounds; r++) {{
    const standings = computeStandingsForRound(r);
    standings.forEach((t, i) => {{
      if (!posMatrix[t.name]) posMatrix[t.name] = [];
      posMatrix[t.name][r] = i + 1;
    }});
  }}
  const labels = Array.from({{length: totalRounds}}, (_, i) => `J${{i+1}}`);
  const datasets = teams.map(name => {{
    const color = getColor(name);
    return {{
      label: name,
      data: Array.from({{length: totalRounds}}, (_, i) => posMatrix[name]?.[i+1] ?? null),
      borderColor: color,
      backgroundColor: color + '22',
      borderWidth: 1.5,
      pointRadius: 2,
      pointHoverRadius: 5,
      tension: 0.3,
      fill: false,
      spanGaps: false,
    }};
  }});
  bumpChart = new Chart(ctx.getContext('2d'), {{
    type: 'line',
    data: {{ labels, datasets }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          mode: 'index',
          intersect: false,
          callbacks: {{
            title: items => `${{items[0].label}}`,
            label: c => c.parsed.y !== null ? ` ${{c.dataset.label}}: ${{c.parsed.y}}º` : null,
            afterBody: items => {{
              // Ordenar por posición
              return items
                .filter(i => i.parsed.y !== null)
                .sort((a,b) => a.parsed.y - b.parsed.y)
                .slice(0, 5)
                .map(i => `  ${{i.parsed.y}}º ${{i.dataset.label}}`);
            }}
          }},
          filter: item => item.parsed.y !== null,
        }}
      }},
      scales: {{
        x: {{
          grid: {{ color: '#1e2d40' }},
          ticks: {{ color: '#64748b', font: {{size: 9}}, maxRotation: 0 }}
        }},
        y: {{
          reverse: true,
          min: 1,
          max: teams.length,
          grid: {{ color: '#1e2d4066' }},
          ticks: {{
            color: '#94a3b8',
            font: {{size: 10}},
            stepSize: 1,
            callback: v => `${{v}}º`
          }},
          title: {{ display: true, text: 'Posición', color: '#64748b', font: {{size: 10}} }}
        }}
      }},
      interaction: {{ mode: 'nearest', intersect: false, axis: 'x' }},
      animation: {{ duration: 600 }},
    }}
  }});
}}


function buildScatterChart() {{
  const standings = computeStandings();
  if (scatterChart) scatterChart.destroy();
  const ctx = document.getElementById('scatterChart');
  if (!ctx) return;
  const avgGF = standings.reduce((s,t)=>s+t.gf,0) / standings.length;
  const avgGC = standings.reduce((s,t)=>s+t.gc,0) / standings.length;
  const quadrantPlugin = {{
    id: 'quadrantLines',
    afterDraw(chart) {{
      const {{ ctx: c, chartArea, scales: {{ x, y }} }} = chart;
      if (!chartArea) return;
      const xMid = x.getPixelForValue(avgGF);
      const yMid = y.getPixelForValue(avgGC);
      c.save();
      c.setLineDash([5,5]);
      c.strokeStyle = 'rgba(148,163,184,.3)';
      c.lineWidth = 1;
      c.beginPath(); c.moveTo(xMid, chartArea.top); c.lineTo(xMid, chartArea.bottom); c.stroke();
      c.beginPath(); c.moveTo(chartArea.left, yMid); c.lineTo(chartArea.right, yMid); c.stroke();
      // Quadrant labels
      c.setLineDash([]);
      c.font = 'bold 9px Segoe UI,system-ui,sans-serif';
      c.fillStyle = 'rgba(148,163,184,.45)';
      c.textAlign = 'left';  c.fillText('Coladero', chartArea.left+4, chartArea.top+12);
      c.textAlign = 'right'; c.fillText('S\u00f3lidos', chartArea.right-4, chartArea.top+12);
      c.textAlign = 'left';  c.fillText('Robustos', chartArea.left+4, chartArea.bottom-4);
      c.textAlign = 'right'; c.fillText('Killers', chartArea.right-4, chartArea.bottom-4);
      c.restore();
    }}
  }};
  // Pre-carga escudos como Image para usarlos como pointStyle
  standings.forEach(t => {{
    if (TEAM_BADGES[t.name] && !_scatterBadgeImgs[t.name]) {{
      const img = new Image(28, 28);
      img.src = TEAM_BADGES[t.name];
      _scatterBadgeImgs[t.name] = img;
    }}
  }});
  const badgeImgs = _scatterBadgeImgs;
  scatterChart = new Chart(ctx.getContext('2d'), {{
    type: 'scatter',
    data: {{
      datasets: standings.map(t => {{
        const img = badgeImgs[t.name];
        return {{
          label: t.name,
          data: [{{ x: t.gf, y: t.gc }}],
          backgroundColor: 'transparent',
          borderColor: 'transparent',
          borderWidth: 0,
          pointStyle: img || 'circle',
          pointRadius: img ? 14 : 8,
          pointHoverRadius: img ? 17 : 11,
        }};
      }})
    }},
    plugins: [quadrantPlugin],
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          callbacks: {{
            label: c => ` ${{c.dataset.label}}: GF ${{c.parsed.x}} · GC ${{c.parsed.y}} · DIF ${{c.parsed.x-c.parsed.y>=0?'+':''}}${{c.parsed.x-c.parsed.y}}`
          }}
        }}
      }},
      scales: {{
        x: {{ title:{{ display:true, text:'Goles a favor (GF)', color:'#94a3b8' }}, grid:{{ color:'#2d3f5f44' }}, ticks:{{ color:'#94a3b8' }} }},
        y: {{ title:{{ display:true, text:'Goles en contra (GC)', color:'#94a3b8' }}, grid:{{ color:'#2d3f5f44' }}, ticks:{{ color:'#94a3b8' }} }}
      }}
    }}
  }});
}}

function switchRanking(mode) {{
  rankingMode = mode;
  const sel = document.getElementById('rankingSelect');
  if (sel) sel.value = mode;
  renderRanking(mode);
}}

function renderRanking(mode) {{
  const standings = computeStandings();
  const xPtsCalc = t => {{ const d = t.gf*t.gf + t.gc*t.gc || 1; return t.gf*t.gf/d*t.played*3; }};
  // Forma: pts últimas 5 jornadas
  const getForma = name => {{
    const res = (LIGA_DATA.results_by_team[name] || []).slice(-5);
    return res.reduce((s,r) => s + (r==='V'?3:r==='E'?1:0), 0);
  }};
  // Racha: victorias/invicto consecutivas desde el final
  const getRacha = name => {{
    const res = (LIGA_DATA.results_by_team[name] || []);
    let streak = 0;
    for (let i = res.length-1; i>=0; i--) {{
      if (res[i] === 'V') streak++;
      else break;
    }}
    if (streak > 0) return {{ v: streak, lbl: `${{streak}}V seguidas` }};
    // Si no victorias, contar invicto
    let inv = 0;
    for (let i = res.length-1; i>=0; i--) {{
      if (res[i] !== 'D') inv++;
      else break;
    }}
    if (inv > 1) return {{ v: inv * 0.4, lbl: `${{inv}} sin perder` }};
    // Contar derrotas consecutivas
    let losses = 0;
    for (let i = res.length-1; i>=0; i--) {{
      if (res[i] === 'D') losses++;
      else break;
    }}
    return {{ v: -losses, lbl: losses > 0 ? `${{losses}} derrotas seguidas` : 'Sin datos' }};
  }};
  let sorted;
  if      (mode === 'off')   sorted = [...standings].sort((a,b)=>b.gf-a.gf||a.gc-b.gc);
  else if (mode === 'def')   sorted = [...standings].sort((a,b)=>a.gc-b.gc||b.gf-a.gf);
  else if (mode === 'dif')   sorted = [...standings].sort((a,b)=>(b.gf-b.gc)-(a.gf-a.gc));
  else if (mode === 'ppg')   sorted = [...standings].sort((a,b)=>parseFloat(b.ppg)-parseFloat(a.ppg));
  else if (mode === 'forma') sorted = [...standings].sort((a,b)=>getForma(b.name)-getForma(a.name));
  else if (mode === 'racha') sorted = [...standings].sort((a,b)=>getRacha(b.name).v-getRacha(a.name).v);
  else if (mode === 'home')  sorted = [...standings].sort((a,b)=>(TEAM_EXTRA_STATS[b.name]?.home_pts||0)-(TEAM_EXTRA_STATS[a.name]?.home_pts||0));
  else if (mode === 'away')  sorted = [...standings].sort((a,b)=>(TEAM_EXTRA_STATS[b.name]?.away_pts||0)-(TEAM_EXTRA_STATS[a.name]?.away_pts||0));
  else if (mode === 'gfpj')  sorted = [...standings].sort((a,b)=>(b.played?b.gf/b.played:0)-(a.played?a.gf/a.played:0));
  else if (mode === 'gcpj')  sorted = [...standings].sort((a,b)=>(a.played?a.gc/a.played:99)-(b.played?b.gc/b.played:99));
  else                       sorted = [...standings].sort((a,b)=>(xPtsCalc(a)-a.pts)-(xPtsCalc(b)-b.pts));
  const getVal = t => {{
    const ex = TEAM_EXTRA_STATS[t.name]||{{}};
    const pj = t.played || 1;
    if (mode==='off')   return {{ v: t.gf,              lbl: `${{t.gf}} GF`  }};
    if (mode==='def')   return {{ v: t.gc,              lbl: `${{t.gc}} GC`  }};
    if (mode==='dif')   {{ const d=t.gf-t.gc; return {{ v: d+50, lbl: `${{d>=0?'+':''}}${{d}} dif` }}; }}
    if (mode==='ppg')   return {{ v: parseFloat(t.ppg), lbl: `${{t.ppg}} pts/pj`   }};
    if (mode==='forma') {{ const f=getForma(t.name); const res5=(LIGA_DATA.results_by_team[t.name]||[]).slice(-5); const icons=res5.map(r=>r==='V'?'<span style="color:#4ade80">V</span>':r==='E'?'<span style="color:#fbbf24">E</span>':'<span style="color:#f87171">D</span>').join(''); return {{ v: f, lbl: `${{f}}pts · ${{icons}}` }}; }}
    if (mode==='racha') {{ const r=getRacha(t.name); return {{ v: r.v, lbl: r.lbl }}; }}
    if (mode==='home')  return {{ v: ex.home_pts||0,    lbl: `${{ex.home_pts||0}}pts · ${{ex.home_pg||0}}V${{ex.home_pe||0}}E${{ex.home_pp||0}}D` }};
    if (mode==='away')  return {{ v: ex.away_pts||0,    lbl: `${{ex.away_pts||0}}pts · ${{ex.away_pg||0}}V${{ex.away_pe||0}}E${{ex.away_pp||0}}D` }};
    if (mode==='gfpj')  {{ const v=(t.gf/pj); return {{ v, lbl: `${{v.toFixed(2)}} GF/pj` }}; }}
    if (mode==='gcpj')  {{ const v=(t.gc/pj); return {{ v, lbl: `${{v.toFixed(2)}} GC/pj` }}; }}
    const xp = xPtsCalc(t); const luck = xp - t.pts;
    return {{ v: Math.abs(luck), lbl: `${{xp.toFixed(1)}} xPts (${{luck>=0?'\u2212':'+'}}${{Math.abs(luck).toFixed(1)}} ${{luck>=0?'con suerte':'mala suerte'}})`, luck }};
  }};
  const maxV = Math.max(...sorted.map(t=>Math.abs(getVal(t).v)), 1);
  const el = document.getElementById('rankingList');
  if (!el) return;
  el.innerHTML = sorted.map((t,i) => {{
    const valObj = getVal(t);
    const {{ v, lbl }} = valObj;
    const bar = (Math.abs(v)/maxV*100).toFixed(1);
    const color = getColor(t.name);
    const kf2 = TEAM_KIT_FULL[t.name] || {{}};
    const kfPri = kf2.primary   || color;
    const kfSec = kf2.secondary || '#1a2236';
    let barStyle;
    if (mode === 'xpts') {{
      const luck = valObj.luck ?? 0;
      barStyle = luck >= 0
        ? `background:linear-gradient(90deg,#22c55e,#4ade80);width:${{bar}}%`
        : `background:linear-gradient(90deg,#ef4444,#f87171);width:${{bar}}%`;
    }} else if (mode === 'forma') {{
      const f = getForma(t.name);
      const c = f>=12?'#4ade80':f>=9?'#a3e635':f>=6?'#fbbf24':f>=3?'#fb923c':'#f87171';
      barStyle = `background:${{c}};width:${{bar}}%`;
    }} else if (mode === 'racha') {{
      barStyle = v >= 0
        ? `background:linear-gradient(90deg,#22c55e,#4ade80);width:${{bar}}%`
        : `background:linear-gradient(90deg,#ef4444,#f87171);width:${{bar}}%`;
    }} else if (mode === 'dif') {{
      const d = t.gf - t.gc;
      barStyle = d >= 0
        ? `background:linear-gradient(90deg,#3b82f6,#60a5fa);width:${{bar}}%`
        : `background:linear-gradient(90deg,#ef4444,#f87171);width:${{bar}}%`;
    }} else {{
      barStyle = `background:linear-gradient(180deg,${{kfPri}} 50%,${{kfSec}} 50%);box-shadow:0 0 0 1.5px ${{kfPri}};box-sizing:border-box;width:${{bar}}%`;
    }}
    return `<div data-team="${{t.name}}" style="display:flex;align-items:center;gap:8px;padding:5px 2px;border-bottom:1px solid var(--border)">
      <span style="width:18px;text-align:right;font-size:11px;color:var(--muted)">${{i+1}}</span>
      ${{crestHTML(t.name,22)}}
      <div style="flex:1;min-width:0">
        <div style="font-size:11px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${{t.name}}</div>
        <div style="height:6px;border-radius:3px;background:var(--border);margin-top:3px">
          <div style="height:100%;border-radius:2px;${{barStyle}}"></div>
        </div>
      </div>
      <span style="font-size:12px;font-weight:700;color:#f0f0f0;white-space:nowrap;flex-shrink:0">${{lbl}}</span>
    </div>`;
  }}).join('');
}}

function renderScenarios() {{
  const standings = computeStandings();
  const rndLeft = LIGA_DATA.total_season_rounds - standingsRound;
  const quedanPts = rndLeft * 3;
  const pts2  = standings[1]?.pts  ?? 0;
  const pts6  = standings[5]?.pts  ?? 0;
  const pts18 = standings[17]?.pts ?? 0;
  const tbody = document.getElementById('scenariosBody');
  if (!tbody) return;
  tbody.innerHTML = standings.map(t => {{
    let maxPts, empPts, canAscend, canPlayoff, canSave, canDescend;
    if (rndLeft === 0) {{
      // Temporada finalizada: usar posición definitiva, no cálculo
      maxPts = empPts = t.pts;
      canAscend  = t.pos <= 2;
      canPlayoff = t.pos <= 6;
      canSave    = t.pos <= 18;
      canDescend = t.pos > 18;
    }} else {{
      maxPts     = t.pts + quedanPts;
      empPts     = t.pts + rndLeft;
      canAscend  = maxPts >= pts2;
      canPlayoff = maxPts >= pts6;
      canSave    = maxPts >= pts18;
      canDescend = pts18 + quedanPts >= t.pts;
    }}
    const zone  = getZoneClass(t.pos);
    const color = getColor(t.name);
    return `<tr class="${{zone}}" style="background:linear-gradient(90deg,${{color}}18 0%,transparent 120px)">
      <td>${{posBadge(t.pos)}}</td>
      <td><div class="team-cell">${{crestHTML(t.name,22)}}<span class="team-name-text">${{t.name}}</span></div></td>
      <td style="font-weight:700;color:var(--accent)">${{t.pts}}</td>
      <td style="color:var(--muted)">${{rndLeft > 0 ? rndLeft + 'J' : '—'}}</td>
      <td style="color:#4ade80;font-weight:700">${{maxPts}}</td>
      <td style="color:#fbbf24;font-weight:600">${{empPts}}</td>
      <td style="font-size:11px">${{canAscend?'<span style="color:#4ade80;font-weight:700">✓</span>':'<span style="color:#475569">✗</span>'}}</td>
      <td style="font-size:11px">${{canPlayoff?'<span style="color:#fbbf24;font-weight:700">✓</span>':'<span style="color:#475569">✗</span>'}}</td>
      <td style="font-size:11px">${{canSave?'<span style="color:#4ade80;font-weight:700">✓</span>':'<span style="color:#ef4444;font-weight:700">✗</span>'}}</td>
      <td style="font-size:11px">${{canDescend?'<span style="color:#f87171;font-weight:700">✓</span>':'<span style="color:#475569">✗</span>'}}</td>
    </tr>`;
  }}).join('');
}}

// ===== LOCAL VS VISITANTE CHART =====
function computeHomeAwayStats(name) {{
  // Primero: usar TEAM_EXTRA_STATS si está disponible (solo temporada actual)
  const ex = TEAM_EXTRA_STATS[name];
  if (ex && ex.home_pts !== undefined && !_historicalMode) return ex;
  // Calcular desde resultados + marcadores (modo histórico o equipo sin stats)
  const res    = LIGA_DATA.results_by_team[name] || [];
  const scMap  = SCORES_DATA.scores_by_team || {{}};
  const venMap = SCORES_DATA.venue_by_team  || {{}};
  const scTeam  = scMap[name]  || {{}};
  const venTeam = venMap[name] || {{}};
  const nr = Math.min(res.length, LIGA_DATA.total_rounds);
  let home_pts=0, home_pj=0, home_pg=0, home_pe=0, home_pp=0, home_gf=0, home_gc=0;
  let away_pts=0, away_pj=0, away_pg=0, away_pe=0, away_pp=0, away_gf=0, away_gc=0;
  for (let i=0; i<nr; i++) {{
    const r = res[i]; if (!r) continue;
    const ven = venTeam[String(i)] || '';
    const sc  = scTeam[String(i)]  || '';
    let gf=0, gc=0;
    if (sc) {{ const p=sc.split('-'); gf=parseInt(p[0]||0); gc=parseInt(p[1]||0); }}
    if (ven === 'H') {{
      home_pj++; home_gf+=gf; home_gc+=gc;
      if (r==='V') {{ home_pg++; home_pts+=3; }} else if (r==='E') {{ home_pe++; home_pts+=1; }} else home_pp++;
    }} else if (ven === 'A') {{
      away_pj++; away_gf+=gf; away_gc+=gc;
      if (r==='V') {{ away_pg++; away_pts+=3; }} else if (r==='E') {{ away_pe++; away_pts+=1; }} else away_pp++;
    }}
  }}
  return {{ home_pts, home_pj, home_pg, home_pe, home_pp, home_gf, home_gc,
            away_pts, away_pj, away_pg, away_pe, away_pp, away_gf, away_gc }};
}}

function buildLocalVisitanteChart() {{
  const ctx = document.getElementById('localVisitanteChart');
  if (!ctx) return;
  if (localVisitanteChart) localVisitanteChart.destroy();
  const standings = computeStandings().sort((a,b)=>b.pts-a.pts);
  const labels    = standings.map(t => t.name);
  const homePts   = standings.map(t => computeHomeAwayStats(t.name).home_pts||0);
  const awayPts   = standings.map(t => computeHomeAwayStats(t.name).away_pts||0);
  const homeGF    = standings.map(t => computeHomeAwayStats(t.name).home_gf||0);
  const awayGF    = standings.map(t => computeHomeAwayStats(t.name).away_gf||0);
  const _glowPlugin = {{
    id: 'glowBars',
    beforeDatasetDraw(chart, args) {{
      const col = chart.data.datasets[args.index].borderColor;
      chart.ctx.save();
      chart.ctx.shadowColor = col;
      chart.ctx.shadowBlur = 18;
    }},
    afterDatasetDraw(chart) {{ chart.ctx.restore(); }}
  }};
  localVisitanteChart = new Chart(ctx.getContext('2d'), {{
    type: 'bar',
    data: {{
      labels,
      datasets: [
        {{ label: '🏠 Pts Local',    data: homePts, backgroundColor: '#39FF1455', borderColor: '#39FF14', borderWidth: 2 }},
        {{ label: '✈️ Pts Visitante', data: awayPts, backgroundColor: '#00F5FF55', borderColor: '#00F5FF', borderWidth: 2 }},
        {{ label: '🏠 GF Local',     data: homeGF,  backgroundColor: '#FF00FF33', borderColor: '#FF00FF', borderWidth: 2 }},
        {{ label: '✈️ GF Visitante',  data: awayGF,  backgroundColor: '#FFE00033', borderColor: '#FFE000', borderWidth: 2 }},
      ]
    }},
    plugins: [_glowPlugin],
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {{
        legend: {{ position: 'top', labels: {{ color: '#94a3b8', boxWidth: 12, font: {{size:11}} }} }},
        tooltip: {{ callbacks: {{ label: c => ` ${{c.dataset.label}}: ${{c.parsed.x}}` }} }}
      }},
      scales: {{
        x: {{ grid: {{ color: '#2d3f5f44' }}, ticks: {{ color: '#94a3b8' }} }},
        y: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{size:10}} }} }}
      }}
    }}
  }});
}}

// ===== HEAD-TO-HEAD MATRIX =====
function renderH2H() {{
  const el = document.getElementById('h2hGrid');
  if (!el) return;
  const teams = (LIGA_DATA.final_standings || LIGA_DATA.teams.map(n=>({{name:n}}))).map(t=>t.name);
  // ── Calcular h2h dinámicamente desde datos disponibles ──
  const resMap = LIGA_DATA.results_by_team   || {{}};
  const oppMap = LIGA_DATA.opponents_by_team  || {{}};
  const scMap  = SCORES_DATA.scores_by_team  || {{}};
  const venMap = SCORES_DATA.venue_by_team   || {{}};
  const h2h = {{}};
  for (const team of teams) {{
    const res = resMap[team] || [];
    const opp = oppMap[team] || [];
    const sc  = scMap[team]  || {{}};
    const ven = venMap[team] || {{}};
    for (let i = 0; i < res.length; i++) {{
      const opponent = opp[i];
      const venue    = ven[String(i)];
      if (!opponent || venue !== 'H') continue;
      const result = res[i];
      const score  = sc[String(i)] || '-';
      if (!h2h[team]) h2h[team] = {{}};
      h2h[team][opponent] = {{ res: result, score }};
    }}
  }}
  const abbr  = n => n.split(' ').map(w=>w[0]).join('').toUpperCase().slice(0,3);
  const bg    = r => r==='V'?'rgba(57,255,20,.70)':r==='E'?'rgba(245,158,11,.70)':r==='D'?'rgba(239,68,68,.70)':'var(--card2)';
  const tc    = r => r==='V'?'#0a0a0a':r==='E'?'#0a0a0a':r==='D'?'#fff':'var(--muted)';
  const crossEnabled = () => localStorage.getItem('h2h_cross') !== '0';
  let html = '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:8px">';
  html += '<div style="font-size:10px;color:var(--muted)">Fila = local · Columna = visitante &nbsp;|&nbsp; <span style="color:#39ff14">■</span> Victoria &nbsp;<span style="color:#f59e0b">■</span> Empate &nbsp;<span style="color:#ef4444">■</span> Derrota</div>';
  html += '<label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-size:10px;color:var(--muted);user-select:none"><input type="checkbox" id="h2hCrossToggle" style="accent-color:#39ff14;width:13px;height:13px;cursor:pointer"> Cruz de Selecci\u00f3n</label>';
  html += '</div>';
  html += '<div style="overflow-x:auto;display:flex;justify-content:center"><table class="h2h-matrix" style="border-collapse:collapse;font-size:8px;min-width:max-content"><thead><tr>';
  html += '<th style="min-width:95px;text-align:right;padding-right:6px;font-size:9px;color:var(--muted);white-space:nowrap">Local \\ Visitante</th>';
  teams.forEach((t, ci) => {{
    const badgeUrl = TEAM_BADGES[t];
    const inner = badgeUrl ? `<img src="${{badgeUrl}}" alt="${{t}}" style="width:18px;height:18px;object-fit:contain" onerror="this.outerHTML='${{abbr(t)}}'">` : abbr(t);
    html += `<th data-c="${{ci}}" style="width:26px;min-width:26px;font-size:8px;color:var(--muted);padding:2px 1px;text-align:center;vertical-align:bottom" title="${{t}}">${{inner}}</th>`;
  }});
  html += '</tr></thead><tbody>';
  teams.forEach((home, ri) => {{
    html += `<tr><td data-r="${{ri}}" style="font-size:9px;color:var(--muted);padding-right:8px;white-space:nowrap;text-align:right;padding-top:2px;padding-bottom:2px">${{home}}</td>`;
    teams.forEach((away, ci) => {{
      if (home === away) {{
        html += `<td data-r="${{ri}}" data-c="${{ci}}" style="background:var(--border);width:24px;min-width:24px;height:20px"></td>`;
      }} else {{
        const cell = (h2h[home] || {{}})[away];
        const r    = cell?.res || '?';
        const s    = cell?.score || '-';
        const disp = (s !== '-' && s !== '?') ? s : '';
        html += `<td data-r="${{ri}}" data-c="${{ci}}" style="background:${{bg(r)}};color:${{tc(r)}};width:24px;min-width:24px;height:20px;text-align:center;font-weight:700;font-size:8px" title="${{home}} vs ${{away}}: ${{s}}">${{disp}}</td>`;
      }}
    }});
    html += '</tr>';
  }});
  html += '</tbody></table></div>';
  el.innerHTML = html;
  // Inicializar checkbox con el estado guardado
  const chk = el.querySelector('#h2hCrossToggle');
  if (chk) {{
    chk.checked = crossEnabled();
    chk.addEventListener('change', function() {{
      localStorage.setItem('h2h_cross', this.checked ? '1' : '0');
      tbl && tbl.classList.toggle('h2h-cross-off', !this.checked);
    }});
  }}
  // Cruz de fila+columna al hacer hover
  const tbl = el.querySelector('.h2h-matrix');
  if (tbl) {{
    if (!crossEnabled()) tbl.classList.add('h2h-cross-off');
    tbl.addEventListener('mouseover', function(e) {{
      if (tbl.classList.contains('h2h-cross-off')) return;
      const cell = e.target.closest('[data-r],[data-c]');
      if (!cell) return;
      tbl.querySelectorAll('.h2h-cross').forEach(x => x.classList.remove('h2h-cross'));
      tbl.classList.add('h2h-hov');
      const r = cell.dataset.r, c = cell.dataset.c;
      if (r !== undefined) tbl.querySelectorAll(`[data-r="${{r}}"]`).forEach(x => x.classList.add('h2h-cross'));
      if (c !== undefined) tbl.querySelectorAll(`[data-c="${{c}}"]`).forEach(x => x.classList.add('h2h-cross'));
    }});
    tbl.addEventListener('mouseleave', function() {{
      tbl.classList.remove('h2h-hov');
      tbl.querySelectorAll('.h2h-cross').forEach(x => x.classList.remove('h2h-cross'));
    }});
  }}
}}

// ===== AUTO-UPDATE =====
let autoUpdateTimer = null;
let lastUpdateTime = null;
let isFetching = false;

function isMatchTime() {{
  const now  = new Date();
  const dd   = String(now.getDate()).padStart(2,'0');
  const mm   = String(now.getMonth()+1).padStart(2,'0');
  const today = `${{dd}}/${{mm}}`;
  const md = LIGA_DATA.match_days || {{}};
  if (!(today in md)) return false;
  const times = md[today];
  if (!times || !times.length) return true;  // fecha sin hora → asumir partido
  for (const t of times) {{
    const [h, m] = t.split(':').map(Number);
    const ko = new Date(now); ko.setHours(h, m, 0, 0);
    if (ko <= now && now <= new Date(ko.getTime() + 2*3600*1000)) return true;
  }}
  return false;
}}

function getUpdateInterval() {{
  return isMatchTime() ? 60000 : 6 * 3600 * 1000;
}}

function updateLiveBar() {{
  const bar = document.getElementById('liveBar');
  if (!bar) return;
  const entries = Object.entries(liveState);
  if (!entries.length) {{ bar.classList.remove('has-live'); bar.innerHTML = ''; return; }}
  bar.classList.add('has-live');
  bar.innerHTML = '<span style="font-size:11px;font-weight:700;color:var(--muted);margin-right:4px">🔴 EN VIVO</span>' +
    entries.map(([name, ls]) => {{
      const score = ls.isHome ? `${{ls.homeGoals}}-${{ls.awayGoals}}` : `${{ls.awayGoals}}-${{ls.homeGoals}}`;
      const vs = ls.isHome ? ls.opponent : ls.opponent;
      const col = ls.diff > 0 ? '#4ade80' : ls.diff < 0 ? '#f87171' : '#fbbf24';
      return `<div class="live-match-pill">
        ${{crestHTML(name,18)}} <span>${{name}}</span>
        <span class="live-score-pill" style="background:${{col}}22;color:${{col}}">${{score}}</span>
        ${{crestHTML(vs,18)}} <span>${{vs}}</span>
      </div>`;
    }}).join('');
}}

function parseLiveScores(html) {{
  /* Try to extract live match data from BeSoccer HTML.
     They embed live match info in a section like '.live' or '.status-live'.
     This is best-effort – if DOM structure differs, liveState stays empty. */
  try {{
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    // BeSoccer shows live rows with data-status="live" or a score column
    const liveRows = doc.querySelectorAll('tr[data-status="live"], .match-live');
    liveRows.forEach(row => {{
      const teams = row.querySelectorAll('.team-name');
      const scores = row.querySelectorAll('.score, .marcador');
      if (teams.length < 2 || scores.length < 1) return;
      const homeBS = teams[0].textContent.trim();
      const awayBS = teams[1].textContent.trim();
      const sc = scores[0].textContent.trim().split('-');
      if (sc.length < 2) return;
      const hG = parseInt(sc[0]) || 0;
      const aG = parseInt(sc[1]) || 0;
      const homeName = BESOCCER_NAME[homeBS];
      const awayName = BESOCCER_NAME[awayBS];
      if (homeName) liveState[homeName] = {{ opponent: awayName||awayBS, diff: hG-aG, homeGoals: hG, awayGoals: aG, isHome: true }};
      if (awayName) liveState[awayName] = {{ opponent: homeName||homeBS, diff: aG-hG, homeGoals: hG, awayGoals: aG, isHome: false }};
    }});
  }} catch(e) {{}}
}}

function updateStatusBar() {{
  const el = document.getElementById('statusText');
  if (!el) return;
  const t = lastUpdateTime
    ? lastUpdateTime.toLocaleTimeString('es', {{hour:'2-digit',minute:'2-digit',second:'2-digit'}})
    : 'nunca';
  const interval = isMatchTime() ? '1 min' : '1 hora';
  const dot = isMatchTime()
    ? '<span class="pulse-dot"></span>'
    : '<span style="color:#6b7280">●</span> ';
  el.innerHTML = `${{dot}} Última actualización: <strong>${{t}}</strong> &nbsp;·&nbsp; Próxima en: <strong>${{interval}}</strong>`;
}}

function scheduleUpdate() {{
  if (autoUpdateTimer) clearTimeout(autoUpdateTimer);
  autoUpdateTimer = setTimeout(fetchAndUpdate, getUpdateInterval());
}}

async function fetchAndUpdate() {{
  if (isFetching) return;
  isFetching = true;
  const el = document.getElementById('statusText');
  if (el) el.innerHTML = '<span style="color:var(--muted)">&#8635; Actualizando datos...</span>';
  try {{
    // Servidor local: fetch JSON frescos
    const [ligaResp, scoresResp] = await Promise.all([
      fetch('/liga_data.json',   {{ cache: 'no-store' }}),
      fetch('/scores_data.json', {{ cache: 'no-store' }}),
    ]);
    if (ligaResp.ok && scoresResp.ok) {{
      const newLiga   = await ligaResp.json();
      const newScores = await scoresResp.json();
      LIGA_DATA   = newLiga;
      SCORES_DATA = newScores;
      // Actualizar liveState desde live_scores del JSON fresco
      liveState = {{}};
      const freshLive = newScores.live_scores || {{}};
      Object.entries(freshLive).forEach(([name, m]) => {{
        liveState[name] = {{
          opponent:  m.opponent,
          diff:      m.is_home ? (m.score_h - m.score_a) : (m.score_a - m.score_h),
          homeGoals: m.score_h,
          awayGoals: m.score_a,
          isHome:    m.is_home,
          minute:    m.minute,
        }};
      }});
    }} else {{
      throw new Error('local-json-' + ligaResp.status);
    }}
  }} catch(e) {{
    // Fallback: BeSoccer via proxy (sin servidor local)
    try {{
      const proxy  = 'https://api.allorigins.win/raw?url=';
      const target = encodeURIComponent('https://es.besoccer.com/competicion/clasificacion/segunda');
      const ctrl   = new AbortController();
      const tid    = setTimeout(() => ctrl.abort(), 15000);
      const resp   = await fetch(proxy + target, {{ signal: ctrl.signal }});
      clearTimeout(tid);
      if (resp.ok) {{
        const html   = await resp.text();
        const parsed = parseBeSoccerStandings(html);
        if (parsed && parsed.length >= 10) {{
          parsed.forEach(item => {{
            const name  = BESOCCER_NAME[item.bsName];
            if (!name) return;
            const entry = LIGA_DATA.final_standings.find(t => t.name === name);
            if (entry) {{ entry.pts=item.pts; entry.wins=item.wins;
              entry.draws=item.draws; entry.losses=item.losses; entry.played=item.played; }}\
          }});
          LIGA_DATA.final_standings.sort((a,b) => b.pts-a.pts || b.wins-a.wins);
        }}
        liveState = {{}};
        parseLiveScores(html);
      }}
    }} catch(e2) {{ console.warn('Fallback BeSoccer error:', e2.message); }}
    if (!lastUpdateTime) lastUpdateTime = new Date();
  }} finally {{
    updateLiveBar();
    updateNextMatchBanner();
    renderStandings();
    renderTeams();
    renderPredictions();
    lastUpdateTime = new Date();
    isFetching = false;
    updateStatusBar();
    scheduleUpdate();
  }}
}}

function parseBeSoccerStandings(html) {{
  try {{
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const rows = doc.querySelectorAll('#tab_total0 tr.row-body');
    if (!rows.length) return null;
    return Array.from(rows).map(row => {{
      const cells = row.querySelectorAll('td');
      const bsName = row.querySelector('.team-name')?.textContent?.trim();
      if (!bsName || cells.length < 8) return null;
      const n = (i) => parseInt(cells[i]?.textContent?.trim()) || 0;
      return {{ bsName, pts:n(3), played:n(4), wins:n(5), draws:n(6), losses:n(7) }};
    }}).filter(Boolean);
  }} catch(e) {{
    return null;
  }}
}}
function renderTeams() {{
  const standings = computeStandings().map((t,i)=>({{...t,pos:i+1}}));
  const grid = document.getElementById('teamsGrid');
  grid.innerHTML = standings.map(t => {{
    const color = getColor(t.name);
    const kit = TEAM_KIT_FULL[t.name] || {{}};
    const primary   = kit.primary   || color;
    const secondary = kit.secondary || '#1e1e1e';
    const bgGrad = `linear-gradient(135deg,${{secondary}} 0%,${{primary}}44 100%)`;
    const headerGrad = `linear-gradient(135deg,${{primary}}18 0%,${{secondary}}30 100%)`;
    const results = LIGA_DATA.results_by_team[t.name] || [];
    const posClass = t.pos <= 3 ? 'team-pos-top' : '';
    return `<div class="team-card" onclick="openTeamModal('${{t.name}}')">
      <div class="team-card-header" style="background:${{headerGrad}}">
        <div class="team-pos-badge ${{posClass}}">${{t.pos}}</div>
        <div class="team-crest-large" style="background:${{bgGrad}};--crest-primary:${{primary}}">
          ${{TEAM_BADGES[t.name] ? `<img src="${{TEAM_BADGES[t.name]}}" alt="${{t.name}}" style="width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 6px ${{primary}}cc);" onerror="this.outerHTML=getInitials('${{t.name}}')">` : getInitials(t.name)}}
        </div>
        <div class="team-card-name">${{t.name}}</div>
      </div>
      <div class="team-card-body">
        <div class="team-stats-row">
          <div class="team-stat"><div class="team-stat-val" style="color:var(--accent)">${{t.pts}}</div><div class="team-stat-lbl">Pts</div></div>
          <div class="team-stat"><div class="team-stat-val" style="color:var(--win)">${{t.wins}}</div><div class="team-stat-lbl">PG</div></div>
          <div class="team-stat"><div class="team-stat-val" style="color:var(--draw)">${{t.draws}}</div><div class="team-stat-lbl">PE</div></div>
          <div class="team-stat"><div class="team-stat-val" style="color:var(--loss)">${{t.losses}}</div><div class="team-stat-lbl">PP</div></div>
        </div>
        <div class="team-form-mini">${{formHTML(results)}}</div>
      </div>
    </div>`;
  }}).join('');
}}

// ===== TEAM MODAL: helper para círculos de historial =====
function buildHistoryDots(name, results) {{
  var oppArr = (LIGA_DATA.opponents_by_team || {{}})[name] || [];
  var scMap  = SCORES_DATA.scores_by_team || SCORES_DATA;
  var venMap = SCORES_DATA.venue_by_team  || {{}};
  var scArr  = scMap[name]  || {{}};
  var venArr = venMap[name] || {{}};
  var total  = LIGA_DATA.total_season_rounds || 42;
  var played = LIGA_DATA.total_rounds || 0;
  var html   = '';
  for (var row = 0; row < Math.ceil(total / 21); row++) {{
    html += '<div style="display:flex;gap:2px;margin-bottom:2px;">';
    for (var col = 0; col < 21; col++) {{
      var i = row * 21 + col;
      if (i >= total) {{ html += '<div style="width:18px;height:18px;"></div>'; continue; }}
      var opp   = oppArr[i] || '';
      var badge = opp ? (TEAM_BADGES[opp] || '') : '';
      var esc   = opp.replace(/"/g, '&quot;');
      if (i >= played) {{
        var inner = badge
          ? '<img src="' + badge + '" alt="' + esc + '" style="width:14px;height:14px;object-fit:contain;display:block;margin:auto;opacity:.4;">'
          : '<span style="font-size:7px;color:var(--muted);">' + (opp ? opp.substring(0,3).toUpperCase() : '\u2013') + '</span>';
        html += '<div title="J' + (i+1) + (opp ? ' \u00b7 vs ' + esc : '') + '" class="cell-future" style="width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;">' + inner + '</div>';
        continue;
      }}
      var r = results[i];
      if (!r) {{ html += '<div style="width:18px;height:18px;border-radius:3px;background:rgba(255,255,255,.03);"></div>'; continue; }}
      var score = scArr[String(i)] || '';
      var venue = venArr[String(i)] || '';
      var lbl   = r === 'V' ? 'Victoria' : r === 'E' ? 'Empate' : 'Derrota';
      var vTxt  = venue === 'H' ? ' (Casa)' : venue === 'A' ? ' (Fuera)' : '';
      var tip   = 'J' + (i+1) + ': ' + lbl + (score ? ' ' + score : '') + (opp ? ' \u00b7 vs ' + esc : '') + vTxt;
      var inner = badge
        ? '<img src="' + badge + '" alt="' + esc + '" style="width:14px;height:14px;object-fit:contain;display:block;margin:auto;">'
        : '<span style="font-size:9px;font-weight:700;">' + r + '</span>';
      html += '<div title="' + tip + '" class="cell-' + r + '" style="width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;cursor:default;">' + inner + '</div>';
    }}
    html += '</div>';
  }}

  // ── Playoff dots (J43-J46) ────────────────────────────────────────────────
  var po = LIGA_DATA.playoff;
  if (po) {{
    // Recopilar los partidos del playoff en los que participa este equipo, en orden cronológico
    var poMatches = [];
    var allTies = (po.semis || []).concat(po.final ? [po.final] : []);
    for (var t = 0; t < allTies.length; t++) {{
      var tie = allTies[t];
      var legs = tie.matches || [];
      for (var l = 0; l < legs.length; l++) {{
        var m = legs[l];
        if (m.home === name || m.away === name) {{
          poMatches.push(m);
        }}
      }}
    }}
    if (poMatches.length > 0) {{
      // Separador visual
      html += '<div style="display:flex;align-items:center;gap:6px;margin:6px 0 4px;">'
            + '<div style="height:1px;flex:1;background:rgba(250,204,21,.25);"></div>'
            + '<span style="font-size:9px;color:#facc15;font-weight:700;text-transform:uppercase;letter-spacing:.5px">Playoff</span>'
            + '<div style="height:1px;flex:1;background:rgba(250,204,21,.25);"></div>'
            + '</div>';
      html += '<div style="display:flex;gap:2px;">';
      for (var k = 0; k < poMatches.length; k++) {{
        var pm   = poMatches[k];
        var opp2 = pm.home === name ? pm.away : pm.home;
        var badge2 = opp2 ? (TEAM_BADGES[opp2] || '') : '';
        var esc2 = opp2.replace(/"/g, '&quot;');
        var isHome = pm.home === name;
        var venueTxt = isHome ? ' (Casa)' : ' (Fuera)';
        if (!pm.played) {{
          // Partido pendiente
          var inner2 = badge2
            ? '<img src="' + badge2 + '" alt="' + esc2 + '" style="width:14px;height:14px;object-fit:contain;display:block;margin:auto;opacity:.4;">'
            : '<span style="font-size:7px;color:#facc15;opacity:.5">' + (opp2 ? opp2.substring(0,3).toUpperCase() : '?') + '</span>';
          html += '<div title="' + pm.label + ' vs ' + esc2 + venueTxt + '" style="width:18px;height:18px;border-radius:3px;border:1px solid rgba(250,204,21,.3);display:flex;align-items:center;justify-content:center;">' + inner2 + '</div>';
        }} else {{
          // Partido jugado — determinar resultado para este equipo
          var parts2 = (pm.score || '0-0').split('-');
          var hg2 = parseInt(parts2[0]) || 0;
          var ag2 = parseInt(parts2[1]) || 0;
          var teamGf = isHome ? hg2 : ag2;
          var teamGc = isHome ? ag2 : hg2;
          var res2 = teamGf > teamGc ? 'V' : teamGf < teamGc ? 'D' : 'E';
          var lbl2 = res2 === 'V' ? 'Victoria' : res2 === 'E' ? 'Empate' : 'Derrota';
          var sc2 = teamGf + '-' + teamGc;
          var tip2 = pm.label + ': ' + lbl2 + ' ' + sc2 + ' vs ' + esc2 + venueTxt;
          var inner2 = badge2
            ? '<img src="' + badge2 + '" alt="' + esc2 + '" style="width:14px;height:14px;object-fit:contain;display:block;margin:auto;">'
            : '<span style="font-size:9px;font-weight:700;">' + res2 + '</span>';
          html += '<div title="' + tip2 + '" class="cell-' + res2 + '" style="width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;cursor:default;">' + inner2 + '</div>';
        }}
      }}
      html += '</div>';
    }}
  }}

  return html;
}}

// ===== TEAM MODAL =====
function openTeamModal(name) {{
  const standings = computeStandings().map((t,i)=>({{...t,pos:i+1}}));
  const t = standings.find(s=>s.name===name);
  const results = LIGA_DATA.results_by_team[name] || [];
  const color = getColor(name);
  const posHistory = LIGA_DATA.positions_by_team[name] || [];
  const trend = posHistory.length >= 2 ? posHistory[posHistory.length-1] - posHistory[posHistory.length-2] : 0;
  const trendIcon = trend < 0 ? '▲' : trend > 0 ? '▼' : '→';
  const trendColor = trend < 0 ? 'var(--win)' : trend > 0 ? 'var(--loss)' : 'var(--muted)';

  document.getElementById('modalTitle').innerHTML = `
    <div style="display:flex;align-items:center;gap:12px;">
      ${{crestHTML(name,42)}}
      <div>
        ${{name}}
        <div style="font-size:12px;color:var(--muted);font-weight:400;margin-top:2px">Posición actual: <strong style="color:var(--accent)">#${{t.pos}}</strong> <span style="color:${{trendColor}}">${{trendIcon}}</span></div>
      </div>
    </div>`;
  document.getElementById('modalBody').innerHTML = `
    <div class="team-stats-row" style="grid-template-columns:repeat(4,1fr);margin-bottom:10px;">
      <div class="team-stat"><div class="team-stat-val" style="color:var(--accent)">${{t.pts}}</div><div class="team-stat-lbl">Pts</div></div>
      <div class="team-stat"><div class="team-stat-val" style="color:var(--win)">${{t.wins}}</div><div class="team-stat-lbl">PG</div></div>
      <div class="team-stat"><div class="team-stat-val" style="color:var(--draw)">${{t.draws}}</div><div class="team-stat-lbl">PE</div></div>
      <div class="team-stat"><div class="team-stat-val" style="color:var(--loss)">${{t.losses}}</div><div class="team-stat-lbl">PP</div></div>
    </div>
    ${{(()=>{{const ex=TEAM_EXTRA_STATS[name]||{{}};const dv=(ex.gf||0)-(ex.gc||0);const dc=dv>0?'var(--win)':dv<0?'var(--loss)':'var(--muted)';
    return `<div class="team-stats-row" style="grid-template-columns:repeat(3,1fr);margin-bottom:${{ex.home_pts!==undefined?'8px':'16px'}};">
      <div class="team-stat"><div class="team-stat-val">${{ex.gf||'–'}}</div><div class="team-stat-lbl">GF</div></div>
      <div class="team-stat"><div class="team-stat-val">${{ex.gc||'–'}}</div><div class="team-stat-lbl">GC</div></div>
      <div class="team-stat"><div class="team-stat-val" style="color:${{dc}}">${{dv>0?'+':''}}${{dv||'–'}}</div><div class="team-stat-lbl">DIF</div></div>
    </div>
    ${{ex.home_pts!==undefined?`<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">
      <div style="background:var(--card2);border-radius:8px;padding:10px;">
        <div style="font-size:11px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px">🏠 Local</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;font-size:12px;text-align:center">
          <div><div style="font-weight:700;color:var(--accent)">${{ex.home_pts}}</div><div style="font-size:10px;color:var(--muted)">Pts</div></div>
          <div><div style="font-weight:700;color:var(--win)">${{ex.home_pg}}</div><div style="font-size:10px;color:var(--muted)">PG</div></div>
          <div><div style="font-weight:700;color:var(--draw)">${{ex.home_pe}}</div><div style="font-size:10px;color:var(--muted)">PE</div></div>
          <div><div style="font-weight:700;color:var(--loss)">${{ex.home_pp}}</div><div style="font-size:10px;color:var(--muted)">PP</div></div>
          <div><div style="font-weight:700">${{ex.home_gf}}</div><div style="font-size:10px;color:var(--muted)">GF</div></div>
          <div><div style="font-weight:700">${{ex.home_gc}}</div><div style="font-size:10px;color:var(--muted)">GC</div></div>
        </div>
      </div>
      <div style="background:var(--card2);border-radius:8px;padding:10px;">
        <div style="font-size:11px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px">✈️ Visitante</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px;font-size:12px;text-align:center">
          <div><div style="font-weight:700;color:var(--accent)">${{ex.away_pts}}</div><div style="font-size:10px;color:var(--muted)">Pts</div></div>
          <div><div style="font-weight:700;color:var(--win)">${{ex.away_pg}}</div><div style="font-size:10px;color:var(--muted)">PG</div></div>
          <div><div style="font-weight:700;color:var(--draw)">${{ex.away_pe}}</div><div style="font-size:10px;color:var(--muted)">PE</div></div>
          <div><div style="font-weight:700;color:var(--loss)">${{ex.away_pp}}</div><div style="font-size:10px;color:var(--muted)">PP</div></div>
          <div><div style="font-weight:700">${{ex.away_gf}}</div><div style="font-size:10px;color:var(--muted)">GF</div></div>
          <div><div style="font-weight:700">${{ex.away_gc}}</div><div style="font-size:10px;color:var(--muted)">GC</div></div>
        </div>
      </div>
    </div>`:''}}`;}})()}}
    <div style="font-size:12px;color:var(--muted);margin-bottom:6px;display:flex;align-items:center;gap:10px;">
      <span>Evolución de posición</span>
      <span style="font-size:10px;color:var(--muted)">fondo = pronóstico BeSoccer</span>
    </div>
    <canvas id="miniChart" height="120" style="margin-bottom:14px"></canvas>
    <div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:12px 14px;margin-bottom:14px;overflow:hidden;">
      <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;">Historial completo</div>
      <div id="historyDots"></div>
    </div>`;
  document.getElementById('teamModal').classList.add('open');
  // Estadísticas avanzadas AS.com — añadir al final del modal
  const _asSection = buildTeamAsStatsModal(name);
  if (_asSection) {{
    const _div = document.createElement('div');
    _div.innerHTML = _asSection;
    document.getElementById('modalBody').appendChild(_div);
  }}
  // Rellenar círculos de historial (función separada para no romper el template literal)
  document.getElementById('historyDots').innerHTML = buildHistoryDots(name, results);
  // mini chart: barras de predicción + línea de posición
  setTimeout(()=>{{
    const ctx = document.getElementById('miniChart').getContext('2d');
    const teamHist = PRED_HISTORY[name] || {{}};
    const rounds   = LIGA_DATA.total_season_rounds;
    const posArr   = LIGA_DATA.positions_by_team[name] || [];
    const asc = [], play = [], perm = [], desc = [];
    for (let i = 0; i < rounds; i++) {{
      const p = teamHist[String(i)];
      desc.push(p ? (p.descenso    || 0) : null);
      perm.push(p ? (p.permanencia || 0) : null);
      play.push(p ? (p.playoff     || 0) : null);
      asc.push( p ? (p.ascenso     || 0) : null);
    }}
    new Chart(ctx,{{
      data:{{
        labels: Array.from({{length: rounds}}, (_,i)=>'J'+(i+1)),
        datasets:[
          {{ type:'bar',  label:'Descenso',    data:desc, backgroundColor:'rgba(239,68,68,.65)',   stack:'p', barPercentage:1, categoryPercentage:1, order:2 }},
          {{ type:'bar',  label:'Permanencia', data:perm, backgroundColor:'rgba(100,116,139,.50)', stack:'p', barPercentage:1, categoryPercentage:1, order:2 }},
          {{ type:'bar',  label:'Playoff',     data:play, backgroundColor:'rgba(251,191,36,.68)',  stack:'p', barPercentage:1, categoryPercentage:1, order:2 }},
          {{ type:'bar',  label:'Ascenso',     data:asc,  backgroundColor:'rgba(34,197,94,.68)',   stack:'p', barPercentage:1, categoryPercentage:1, order:2 }},
          {{ type:'line', label:'Posición', data:posArr, yAxisID:'y2',
             borderColor:color, backgroundColor:color+'30',
             borderWidth:2, pointRadius:1.5, pointBackgroundColor:color,
             tension:.3, fill:false, order:1 }}
        ]
      }},
      options:{{
        responsive:true,
        plugins:{{ legend:{{ display:false }} }},
        scales:{{
          x:{{ stacked:true, ticks:{{color:'#64748b',maxTicksLimit:10}}, grid:{{display:false}} }},
          y:{{ stacked:true, min:0, max:100, display:false }},
          y2:{{ type:'linear', position:'left', reverse:true, min:1,
                max:LIGA_DATA.teams.length,
                ticks:{{color:'#64748b',stepSize:2}},
                grid:{{color:'#2d3f5f44'}} }}
        }}
      }}
    }});
  }},50);
}}
function buildTeamAsStatsModal(name) {{
  if (_historicalMode) return null;
  // Filtrar partidos del equipo
  const matches = AS_STATS.filter(m => m.home === name || m.away === name);
  if (!matches.length) return null;

  const FIELDS = ['possession','shots_inside','shots_outside','shots_blocked',
                  'shots_received','fouls_committed','yellow_cards','red_cards',
                  'poss_recoveries','poss_losses','offsides'];
  const LABELS_MAP = {{
    possession:'Posesión%', shots_inside:'D.Puerta', shots_outside:'D.Fuera',
    shots_blocked:'D.Bloq', shots_received:'Recibidos', fouls_committed:'Faltas',
    yellow_cards:'Amarillas', red_cards:'Rojas',
    poss_recoveries:'Recup.', poss_losses:'Pérd.', offsides:'OFJ'
  }};

  // Calcular promedios
  const avgs = {{}};
  for (const f of FIELDS) {{
    const vals = matches.map(m => {{
      const side = m.home === name ? 'home' : 'away';
      return m[f + '_' + side];
    }}).filter(v => v !== null && v !== undefined);
    avgs[f] = vals.length ? vals.reduce((s,v)=>s+v,0)/vals.length : null;
  }}

  // Mostrar todos los partidos (orden desc)
  const last10 = matches.slice().reverse();

  function fmtv(v, dec) {{ return v === null ? '—' : v.toFixed(dec ?? 1); }}

  const avgCells = FIELDS.map(f => `
    <div style="text-align:center;">
      <div style="font-weight:700;font-size:13px;color:var(--accent)">${{fmtv(avgs[f], f==='possession'||f==='shots_inside'||f==='shots_outside'||f==='poss_recoveries'||f==='poss_losses'?1:2)}}</div>
      <div style="font-size:10px;color:var(--muted)">${{LABELS_MAP[f]}}</div>
    </div>`).join('');

  const tableRows = last10.map(m => {{
    const isHome = m.home === name;
    const side   = isHome ? 'home' : 'away';
    const opp    = isHome ? m.away : m.home;
    const venue  = isHome ? 'C' : 'F';
    const res    = (LIGA_DATA.results_by_team[name] || [])[m.jornada - 1];
    const resClass = res === 'V' ? 'cell-V' : res === 'E' ? 'cell-E' : res === 'D' ? 'cell-D' : '';
    const oppBadge = TEAM_BADGES[opp] || '';
    const oppEsc   = opp.replace(/"/g, '&quot;');
    const badgeInner = oppBadge
      ? `<img src="${{oppBadge}}" alt="${{oppEsc}}" style="width:18px;height:18px;object-fit:contain;display:block;margin:auto;">`
      : `<span style="font-size:8px;font-weight:700">${{opp.substring(0,3).toUpperCase()}}</span>`;
    const posv   = m['possession_' + side];
    const si     = m['shots_inside_' + side];
    const so     = m['shots_outside_' + side];
    const rec    = m['shots_received_' + side];
    const yc     = m['yellow_cards_' + side];
    const rc     = m['red_cards_' + side];
    return `<tr>
      <td style="font-size:10px;color:var(--muted);width:12px">${{m.jornada}}</td>
      <td style="font-size:10px;color:var(--muted);width:14px;text-align:center">${{venue}}</td>
      <td><div class="${{resClass}}" style="width:24px;height:24px;border-radius:4px;display:flex;align-items:center;justify-content:center;" title="${{oppEsc}}">${{badgeInner}}</div></td>
      <td style="font-size:11px;text-align:center">${{posv !== null && posv !== undefined ? posv.toFixed(1)+'%' : '—'}}</td>
      <td style="font-size:11px;text-align:center;color:#4ade80">${{si !== null && si !== undefined ? si : '—'}}</td>
      <td style="font-size:11px;text-align:center">${{so !== null && so !== undefined ? so : '—'}}</td>
      <td style="font-size:11px;text-align:center;color:#f87171">${{rec !== null && rec !== undefined ? rec : '—'}}</td>
      <td style="font-size:11px;text-align:center;color:#fbbf24">${{yc !== null && yc !== undefined ? yc : '—'}}</td>
      <td style="font-size:11px;text-align:center;color:#ef4444">${{rc !== null && rc !== undefined ? rc : '—'}}</td>
    </tr>`;
  }}).join('');

  return `
  <div style="margin:14px 0;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:12px;">
    <div style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;">📊 Estadísticas Avanzadas <span style="font-weight:400;font-size:10px">(media ${{matches.length}} partidos · Opta/AS.com)</span></div>
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:12px;">
      ${{avgCells}}
    </div>
    <div style="font-size:10px;color:var(--muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:.04em">Todos los partidos (${{last10.length}})</div>
    <div style="max-height:260px;overflow-y:auto;overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:11px;">
        <thead><tr style="color:var(--muted);font-size:10px;">
          <th style="text-align:left;padding:3px 4px">J</th>
          <th style="padding:3px 4px"></th>
          <th style="text-align:left;padding:3px 4px">Rival</th>
          <th title="Posesión" style="padding:3px 4px">Pos.</th>
          <th title="Disparos a puerta" style="padding:3px 4px;color:#4ade80">D.P</th>
          <th title="Disparos fuera" style="padding:3px 4px">D.F</th>
          <th title="Disparos recibidos" style="padding:3px 4px;color:#f87171">Rec.</th>
          <th title="Tarjetas amarillas" style="padding:3px 4px;color:#fbbf24">🟨</th>
          <th title="Tarjetas rojas" style="padding:3px 4px;color:#ef4444">🟥</th>
        </tr></thead>
        <tbody>${{tableRows}}</tbody>
      </table>
    </div>
  </div>`;
}}

function closeModal() {{ document.getElementById('teamModal').classList.remove('open'); }}
document.getElementById('teamModal').addEventListener('click', e => {{ if(e.target===e.currentTarget) closeModal(); }});

// ===== MATCH STATS MODAL =====
function openMatchStatsModal(home, away, jornada) {{
  const modal = document.getElementById('matchModal');
  const body  = document.getElementById('matchModalBody');
  const m = AS_STATS.find(s => s.home === home && s.away === away && s.jornada === jornada);
  const scMap = SCORES_DATA.scores_by_team || SCORES_DATA;
  const scoreRaw = (scMap[home]||{{}})[String(jornada-1)];

  // ── Selección de colores diferenciados ─────────────────────────────
  function hexToRgb(hex) {{
    const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
    return [r,g,b];
  }}
  function colorDist(h1,h2) {{
    if (!h1||!h2) return 999;
    try {{
      const [r1,g1,b1]=hexToRgb(h1), [r2,g2,b2]=hexToRgb(h2);
      return Math.sqrt((r1-r2)**2+(g1-g2)**2+(b1-b2)**2);
    }} catch(e) {{ return 999; }}
  }}
  // Paleta de alternativas
  const ALT_COLORS = ['#f59e0b','#60a5fa','#a78bfa','#34d399','#fb923c','#f472b6','#38bdf8','#facc15'];
  let hc = (TEAM_COLORS[home] && TEAM_COLORS[home] !== '#cccccc') ? TEAM_COLORS[home] : '#f59e0b';
  let ac = (TEAM_COLORS[away] && TEAM_COLORS[away] !== '#cccccc') ? TEAM_COLORS[away] : '#60a5fa';
  // Si los colores son muy similares (distancia < 80), elegir alternativa para visitante
  if (colorDist(hc, ac) < 80) {{
    const alt = ALT_COLORS.find(c => colorDist(hc, c) >= 80 && colorDist(ac, c) >= 80)
             || ALT_COLORS.find(c => colorDist(hc, c) >= 60)
             || '#60a5fa';
    ac = alt;
  }}
  // Garantizar legibilidad sobre fondo oscuro: si luminancia < 0.18 → blanco
  function luminance(hex) {{
    try {{
      const [r,g,b] = hexToRgb(hex).map(v => {{
        v /= 255;
        return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4);
      }});
      return 0.2126*r + 0.7152*g + 0.0722*b;
    }} catch(e) {{ return 1; }}
  }}
  function readable(c) {{ return luminance(c) < 0.18 ? '#ffffff' : c; }}
  const hcT = readable(hc);   // color de texto local  (puede ser blanco)
  const acT = readable(ac);   // color de texto visitante
  const headerHTML = `<div style="margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.08)">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:8px">
      <div style="text-align:center;flex:1;min-width:0">
        ${{crestHTML(home,40)}}
        <div style="font-size:11px;margin-top:5px;font-weight:600;word-break:break-word">${{home}}</div>
      </div>
      <div style="text-align:center;flex-shrink:0">
        <div style="font-size:24px;font-weight:900;letter-spacing:3px;color:var(--text)">${{scoreRaw||'—'}}</div>
        <div style="font-size:10px;color:var(--muted);margin-top:3px">J${{jornada}} · Opta/AS.com</div>
      </div>
      <div style="text-align:center;flex:1;min-width:0">
        ${{crestHTML(away,40)}}
        <div style="font-size:11px;margin-top:5px;font-weight:600;word-break:break-word">${{away}}</div>
      </div>
    </div>
  </div>`;
  if (!m) {{
    body.innerHTML = headerHTML + `<div style="text-align:center;padding:16px;color:var(--muted);font-size:12px">Sin estadísticas Opta disponibles</div>`;
    modal.classList.add('open'); return;
  }}
  const STATS = [
    {{ key:'shots_inside',    label:'Disparos a puerta'   }},
    {{ key:'shots_outside',   label:'Disparos fuera'      }},
    {{ key:'shots_blocked',   label:'Disparos bloqueados' }},
    {{ key:'shots_received',  label:'Disparos recibidos'  }},
    {{ key:'fouls_committed', label:'Faltas cometidas'    }},
    {{ key:'fouls_received',  label:'Faltas recibidas'    }},
    {{ key:'yellow_cards',    label:'Tarjetas amarillas'  }},
    {{ key:'red_cards',       label:'Tarjetas rojas'      }},
    {{ key:'poss_recoveries', label:'Recuperaciones'      }},
    {{ key:'poss_losses',     label:'Pérdidas de balón'   }},
    {{ key:'offsides',        label:'Fueras de juego'     }},
  ];
  function statRow(s) {{
    const hv = m[s.key+'_home'], av = m[s.key+'_away'];
    if (hv===null||hv===undefined||av===null||av===undefined) return '';
    const total = (hv+av)||1;
    const hPct = (hv/total*100).toFixed(1);
    const aPct = (100-parseFloat(hPct)).toFixed(1);
    return `<div style="margin:5px 0">
      <div style="display:flex;justify-content:space-between;align-items:baseline;font-size:12px">
        <span style="font-weight:700;min-width:30px;color:#fff">${{hv}}</span>
        <span style="font-size:10px;color:var(--muted);flex:1;text-align:center">${{s.label}}</span>
        <span style="font-weight:700;min-width:30px;text-align:right;color:#fff">${{av}}</span>
      </div>
      <div style="display:flex;height:3px;border-radius:2px;overflow:hidden;margin-top:2px">
        <div style="width:${{hPct}}%;background:${{hc}};opacity:.85"></div>
        <div style="width:${{aPct}}%;background:${{ac}};opacity:.7"></div>
      </div>
    </div>`;
  }}
  const ph = m.possession_home, pa = m.possession_away;
  const possHTML = (ph!=null&&pa!=null) ? `<div style="margin:8px 0 10px;padding:8px;background:rgba(255,255,255,.04);border-radius:6px">
    <div style="display:flex;justify-content:space-between;align-items:baseline;font-size:13px;margin-bottom:5px">
      <span style="font-weight:800;color:#fff">${{ph.toFixed(1)}}%</span>
      <span style="font-size:10px;color:var(--muted)">Posesión</span>
      <span style="font-weight:800;color:#fff">${{pa.toFixed(1)}}%</span>
    </div>
    <div style="display:flex;height:6px;border-radius:3px;overflow:hidden">
      <div style="width:${{ph}}%;background:${{hc}}"></div>
      <div style="width:${{pa}}%;background:${{ac}}"></div>
    </div>
  </div>` : '';
  body.innerHTML = headerHTML + possHTML + STATS.map(statRow).filter(Boolean).join('');
  modal.classList.add('open');
}}
function closeMatchModal() {{ document.getElementById('matchModal').classList.remove('open'); }}
document.getElementById('matchModal').addEventListener('click', e => {{ if(e.target===e.currentTarget) closeMatchModal(); }});

// ===== NEXT MATCH COUNTDOWN =====
function getNextFixture() {{
  const now = new Date();
  let best = null;
  let bestDt = null;
  for (const f of (LIGA_DATA.fixtures || [])) {{
    if (!f.date || !f.time) continue;
    const parts = f.date.split('/');
    const tparts = f.time.split(':');
    if (parts.length < 2 || tparts.length < 2) continue;
    const dd = parseInt(parts[0], 10);
    const mm = parseInt(parts[1], 10);
    const hh = parseInt(tparts[0], 10);
    const mi = parseInt(tparts[1], 10);
    // Temporada 25/26: meses ≥ 8 → 2025, meses ≤ 7 → 2026
    const yr = mm >= 8 ? 2025 : 2026;
    const dt = new Date(yr, mm - 1, dd, hh, mi, 0);
    if (dt > now && (!bestDt || dt < bestDt)) {{
      best = f;
      bestDt = dt;
    }}
  }}
  return {{ fixture: best, dt: bestDt }};
}}

function updateNextMatchBanner() {{
  const banner = document.getElementById('nextMatchBanner');
  const teamsEl = document.getElementById('nmTeams');
  const cdEl = document.getElementById('nmCountdown');
  if (!banner || !teamsEl || !cdEl) return;
  const {{ fixture: f, dt: matchDt }} = getNextFixture();
  if (!f || !matchDt) {{ banner.style.display = 'none'; return; }}
  const now = new Date();
  const diff = matchDt - now;
  if (diff <= 0) {{ banner.style.display = 'none'; return; }}
  const totalH = Math.floor(diff / 3600000);
  const mins   = Math.floor((diff % 3600000) / 60000);
  const secs   = Math.floor((diff % 60000) / 1000);
  const days   = Math.floor(totalH / 24);
  const hours  = totalH % 24;
  let timeStr;
  if (days >= 2) {{
    timeStr = days + 'd ' + hours + 'h ' + mins + 'm';
  }} else if (totalH >= 1) {{
    timeStr = totalH + 'h ' + String(mins).padStart(2,'0') + 'm ' + String(secs).padStart(2,'0') + 's';
  }} else {{
    timeStr = mins + 'm ' + String(secs).padStart(2,'0') + 's';
  }}
  teamsEl.textContent = f.home + ' vs ' + f.away;
  cdEl.textContent = '\u23f1 ' + timeStr;
  banner.style.display = 'flex';
}}

// ===== SEASON SWITCHER =====
const _ORIG_LIGA_DATA   = JSON.parse(JSON.stringify(LIGA_DATA));
const _ORIG_SCORES_DATA = JSON.parse(JSON.stringify(SCORES_DATA));
let _historicalMode = false;

function _buildHistPositions(teams, results_by_team, nr) {{
  const points_by_team   = {{}};
  const positions_by_team = {{}};
  for (const t of teams) {{
    points_by_team[t] = [];
    const res = results_by_team[t] || [];
    for (let r = 0; r < nr; r++) {{
      const prev = r > 0 ? points_by_team[t][r-1] : 0;
      const v = res[r];
      points_by_team[t].push(prev + (v==='V'?3:v==='E'?1:0));
    }}
  }}
  for (let r = 0; r < nr; r++) {{
    const sorted = [...teams].sort((a,b) =>
      (points_by_team[b][r]||0) - (points_by_team[a][r]||0));
    sorted.forEach((t,i) => {{
      if (!positions_by_team[t]) positions_by_team[t] = [];
      positions_by_team[t].push(i+1);
    }});
  }}
  return {{ points_by_team, positions_by_team }};
}}

function switchSeason(label) {{
  if (label === '_actual_') {{
    Object.keys(LIGA_DATA).forEach(k => delete LIGA_DATA[k]);
    Object.assign(LIGA_DATA, _ORIG_LIGA_DATA);
    Object.keys(SCORES_DATA).forEach(k => delete SCORES_DATA[k]);
    Object.assign(SCORES_DATA, _ORIG_SCORES_DATA);
    _historicalMode = false;
  }} else {{
    const hs = HISTORY_DATA.seasons[label];
    if (!hs) return;
    const nr = hs.total_rounds || hs.total_season_rounds || 42;
    const {{ points_by_team, positions_by_team }} = _buildHistPositions(hs.teams, hs.results_by_team, nr);
    const newLiga = {{
      label:               label,
      playoff:             hs.playoff || null,
      teams:               hs.teams,
      total_rounds:        nr,
      total_season_rounds: nr,
      last_updated:        label,
      results_by_team:     hs.results_by_team,
      opponents_by_team:   hs.opponents_by_team,
      final_standings:     hs.final_standings,
      positions_by_team,
      points_by_team,
      situacion_by_team:   {{}},
      quedan_by_team:      {{}},
      fixtures:            [],
      match_days:          {{}},
      h2h_data:            {{}},
    }};
    Object.keys(LIGA_DATA).forEach(k => delete LIGA_DATA[k]);
    Object.assign(LIGA_DATA, newLiga);
    Object.keys(SCORES_DATA).forEach(k => delete SCORES_DATA[k]);
    SCORES_DATA.scores_by_team = hs.scores_by_team;
    SCORES_DATA.venue_by_team  = hs.venue_by_team;
    // Cargar badges de equipos históricos que no estén ya en TEAM_BADGES
    if (hs.team_badges) {{
      Object.entries(hs.team_badges).forEach(([name, url]) => {{
        if (url && !TEAM_BADGES[name]) TEAM_BADGES[name] = url;
      }});
    }}
    _historicalMode = true;
  }}

  // Reset state
  currentRound   = LIGA_DATA.total_rounds;
  standingsRound = LIGA_DATA.total_rounds;
  formMode       = 0;
  selectedTeams  = new Set();
  if (evolutionChart) {{ evolutionChart.destroy(); evolutionChart = null; }}

  // Mostrar/ocultar tabs no disponibles en modo histórico
  const hiddenInHistory = ['predicciones'];
  hiddenInHistory.forEach(tab => {{
    const btn = document.querySelector('[data-tab="' + tab + '"]');
    if (btn) btn.style.display = _historicalMode ? 'none' : '';
  }});

  // Si la tab activa quedó oculta, ir a clasificacion
  const activePanel = document.querySelector('.tab-panel.active');
  const activeTabName = activePanel ? activePanel.id.replace('tab-','') : 'clasificacion';
  if (_historicalMode && hiddenInHistory.includes(activeTabName)) {{
    switchTab('clasificacion');
  }} else {{
    // Re-renderizar tab activa
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
    const panelEl = document.getElementById('tab-' + activeTabName);
    const btnEl   = document.querySelector('[data-tab="' + activeTabName + '"]');
    if (panelEl) panelEl.classList.add('active');
    if (btnEl)   btnEl.classList.add('active');
    if (activeTabName === 'evolucion') initEvolutionChart();
    else if (activeTabName === 'resultados') renderRoundResults();
    else if (activeTabName === 'analisis') initAnalysisTab();
    else if (activeTabName === 'equipos') renderTeams();
    else if (activeTabName === 'playoff') renderPlayoff();
    else renderStandings();
  }}
  // Actualizar roundsBadge y roundInput max
  const rb = document.getElementById('roundsBadge');
  if (rb) rb.textContent = 'Jornada ' + LIGA_DATA.total_rounds + ' / ' + LIGA_DATA.total_season_rounds;
  const ri = document.getElementById('roundInput');
  if (ri) {{ ri.max = LIGA_DATA.total_season_rounds; ri.value = LIGA_DATA.total_rounds; }}

  // Ocultar elementos irrelevantes en modo histórico
  const liveBar = document.getElementById('liveBar');
  if (liveBar) liveBar.style.display = _historicalMode ? 'none' : '';
  const nmBanner = document.getElementById('nextMatchBanner');
  if (nmBanner) nmBanner.style.display = _historicalMode ? 'none' : '';
  const statusBar = document.querySelector('.status-bar');
  if (statusBar) statusBar.style.display = _historicalMode ? 'none' : '';
}}

// ===== INIT =====
function init() {{
  renderStandings();
  renderRoundResults();
  renderTeams();
  renderPredictions();
  updateStatusBar();
  updateNextMatchBanner();
  setInterval(updateNextMatchBanner, 1000);
  scheduleUpdate();
  // Fetch inmediato solo en servidor local; en GitHub Pages/file:// los datos ya
  // van embebidos en el HTML y el fetch remoto solo genera warnings innecesarios
  if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {{
    fetchAndUpdate();
  }}
}}
init();
</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</body>
</html>"""

# Inyectar JS de auto-reload justo antes de </body>
auto_reload_js = f"""
<script>
(function(){{
  var BUILD_TS = '{BUILD_TS}';
  function checkVersion(){{
    fetch('version.json?_=' + Date.now())
      .then(function(r){{ return r.json(); }})
      .then(function(d){{
        if (d.ts && d.ts !== BUILD_TS) {{
          console.log('[auto-reload] nueva version:', d.ts);
          location.reload(true);
        }}
      }})
      .catch(function(){{}});
  }}
  // Comprobar cada 5 minutos
  setInterval(checkVersion, 5 * 60 * 1000);
  // Y tambien al volver a la pestaña tras tenerla en segundo plano
  document.addEventListener('visibilitychange', function(){{
    if (!document.hidden) checkVersion();
  }});
}})();
</script>
"""
html = html.replace('</body>', auto_reload_js + '</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Generar version.json (lo lee el JS de auto-reload para detectar actualizaciones)
with open('version.json', 'w', encoding='utf-8') as f:
    json.dump({'ts': BUILD_TS, 'jornada': data['total_rounds']}, f)

print('index.html generado correctamente.')
print(f'  Equipos: {len(data["teams"])}')
print(f'  Jornadas: {data["total_rounds"]}')
print(f'  Build timestamp: {BUILD_TS}')
print('  Abre index.html en cualquier navegador.')
