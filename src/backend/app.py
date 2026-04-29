from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request
import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

try:
    from src.algorithms import astar as astar_algorithm
except ModuleNotFoundError:
    # Suport pentru rulare directa: python src/backend/app.py
    import sys

    DIRECTOR_SRC = Path(__file__).resolve().parents[1]
    if str(DIRECTOR_SRC) not in sys.path:
        sys.path.insert(0, str(DIRECTOR_SRC))

    from algorithms import astar as astar_algorithm

try:
    import networkx as nx
    import osmnx as ox
except Exception:
    nx = None
    ox = None

DIRECTOR_BAZA = Path(__file__).resolve().parent
CALE_BAZA_DATE = DIRECTOR_BAZA / "navigatie.db"
RADACINA_PROIECT = DIRECTOR_BAZA.parent.parent
FISIER_GRAF_RUTIER = RADACINA_PROIECT / "data" / "baia_mare_drive.graphml"
LOCALITATE_IMPLICITA = "Baia Mare, Romania"
VITEZA_ESTIMATA_KMH = 35.0
TIP_RETEA_OSM = "drive_service"

app = Flask(
    __name__,
    template_folder=str(DIRECTOR_BAZA.parent / "frontend" / "templates"),
    static_folder=str(DIRECTOR_BAZA.parent / "frontend" / "static"),
)
def init_db():
    # Această linie creează fișierul navigatie.db automat în folderul tău
    conn = sqlite3.connect(str(CALE_BAZA_DATE))
    cursor = conn.cursor()
    
    # Tabel pentru istoricul rutelor găsite de A*
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS istoric_rute (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_punct TEXT,
            destinatie_punct TEXT,
            traseu_complet TEXT,
            data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute("PRAGMA table_info(istoric_rute)")
    coloane_existente = {rand[1] for rand in cursor.fetchall()}
    coloane_noi = {
        "distanta_m": "REAL",
        "durata_min": "REAL",
        "path_gps_json": "TEXT",
        "tip_ruta": "TEXT DEFAULT 'osm_drive'",
        "sursa": "TEXT DEFAULT 'click_harta'",
    }
    for nume_coloana, tip_coloana in coloane_noi.items():
        if nume_coloana not in coloane_existente:
            cursor.execute(f"ALTER TABLE istoric_rute ADD COLUMN {nume_coloana} {tip_coloana}")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_istoric_rute_data_ora ON istoric_rute(data_ora)")
    conn.commit()
    conn.close()

# Apelam functia ca sa fim siguri ca baza de date exista la pornirea aplicatiei
init_db()

# Traseul proiectat pe harta in coordonate GPS.
traseu_gps_proiectat = []


def incarca_sau_genereaza_graf_rutier() -> Optional[object]:
    """Incarca graful rutier OSM din cache sau il descarca prima data."""
    if ox is None:
        return None

    try:
        FISIER_GRAF_RUTIER.parent.mkdir(parents=True, exist_ok=True)
        if FISIER_GRAF_RUTIER.exists():
            graf_cache = ox.load_graphml(filepath=str(FISIER_GRAF_RUTIER))
            if graf_cache.graph.get("tip_retea") == TIP_RETEA_OSM:
                return graf_cache

            # Cache vechi: incercam sa il actualizam pentru acoperire mai buna pe strazi mici.
            try:
                ox.settings.use_cache = True
                graf_actualizat = ox.graph_from_place(LOCALITATE_IMPLICITA, network_type=TIP_RETEA_OSM, simplify=True)
                graf_actualizat.graph["tip_retea"] = TIP_RETEA_OSM
                ox.save_graphml(graf_actualizat, filepath=str(FISIER_GRAF_RUTIER))
                return graf_actualizat
            except Exception as eroare_refresh:
                print(f"[navigatie] Nu s-a putut actualiza cache-ul rutier, folosesc varianta existenta: {eroare_refresh}")
                return graf_cache

        ox.settings.use_cache = True
        graf_nou = ox.graph_from_place(LOCALITATE_IMPLICITA, network_type=TIP_RETEA_OSM, simplify=True)
        graf_nou.graph["tip_retea"] = TIP_RETEA_OSM
        ox.save_graphml(graf_nou, filepath=str(FISIER_GRAF_RUTIER))
        return graf_nou
    except Exception as eroare:
        print(f"[navigatie] Nu s-a putut incarca graful rutier: {eroare}")
        return None


graf_rutier = incarca_sau_genereaza_graf_rutier()
graf_adiacenta_algoritmi: Optional[Dict[Any, List[Tuple[Any, float]]]] = None
coordonate_algoritmi: Optional[Dict[Any, Tuple[float, float]]] = None


def pregateste_structuri_algoritmi() -> Tuple[Dict[Any, List[Tuple[Any, float]]], Dict[Any, Tuple[float, float]]]:
    global graf_adiacenta_algoritmi, coordonate_algoritmi

    if graf_rutier is None:
        return {}, {}

    if graf_adiacenta_algoritmi is not None and coordonate_algoritmi is not None:
        return graf_adiacenta_algoritmi, coordonate_algoritmi

    adiacenta: Dict[Any, List[Tuple[Any, float]]] = {nod: [] for nod in graf_rutier.nodes}
    muchii_minime: Dict[Tuple[Any, Any], float] = {}

    for nod_sursa, nod_tinta, date_muchie in graf_rutier.edges(data=True):
        try:
            lungime = float(date_muchie.get("length", 1.0))
        except (TypeError, ValueError):
            continue

        cheie = (nod_sursa, nod_tinta)
        if cheie not in muchii_minime or lungime < muchii_minime[cheie]:
            muchii_minime[cheie] = lungime

    for (nod_sursa, nod_tinta), lungime in muchii_minime.items():
        adiacenta[nod_sursa].append((nod_tinta, lungime))

    coordonate: Dict[Any, Tuple[float, float]] = {}
    for nod, date_nod in graf_rutier.nodes(data=True):
        try:
            coordonate[nod] = (float(date_nod["x"]), float(date_nod["y"]))
        except (KeyError, TypeError, ValueError):
            continue

    graf_adiacenta_algoritmi = adiacenta
    coordonate_algoritmi = coordonate
    return adiacenta, coordonate


def puncte_aproape_egale(punct_a: List[float], punct_b: List[float], toleranta: float = 1e-7) -> bool:
    return abs(punct_a[0] - punct_b[0]) <= toleranta and abs(punct_a[1] - punct_b[1]) <= toleranta


def extrage_date_muchie(graf: object, nod_sursa: int, nod_tinta: int) -> Dict[str, Any]:
    date_muchii = graf.get_edge_data(nod_sursa, nod_tinta, default={})
    if not date_muchii:
        return {}

    # Pentru MultiDiGraph alegem muchia cea mai scurta dintre muchiile paralele.
    if "length" in date_muchii:
        return date_muchii

    return min(
        date_muchii.values(),
        key=lambda date_muchie: float(date_muchie.get("length", float("inf"))),
    )


def construieste_ruta_gps_din_geometrie(graf: object, ruta_noduri: List[int]) -> List[List[float]]:
    ruta_gps: List[List[float]] = []

    if len(ruta_noduri) < 2:
        return ruta_gps

    for index in range(len(ruta_noduri) - 1):
        nod_sursa = ruta_noduri[index]
        nod_tinta = ruta_noduri[index + 1]

        date_muchie = extrage_date_muchie(graf, nod_sursa, nod_tinta)
        geometrie = date_muchie.get("geometry")

        if geometrie is not None and hasattr(geometrie, "coords"):
            puncte_segment = [[float(coord_y), float(coord_x)] for coord_x, coord_y in geometrie.coords]
        else:
            puncte_segment = [
                [float(graf.nodes[nod_sursa]["y"]), float(graf.nodes[nod_sursa]["x"])],
                [float(graf.nodes[nod_tinta]["y"]), float(graf.nodes[nod_tinta]["x"])],
            ]

        if not puncte_segment:
            continue

        if not ruta_gps:
            ruta_gps.extend(puncte_segment)
            continue

        if puncte_aproape_egale(ruta_gps[-1], puncte_segment[0]):
            ruta_gps.extend(puncte_segment[1:])
        else:
            ruta_gps.extend(puncte_segment)

    return ruta_gps


def centru_harta_implicit() -> List[float]:
    if graf_rutier is None:
        return [47.6568, 23.5688]

    noduri = list(graf_rutier.nodes)
    if not noduri:
        return [47.6568, 23.5688]

    primul_nod = noduri[0]
    return [float(graf_rutier.nodes[primul_nod]["y"]), float(graf_rutier.nodes[primul_nod]["x"])]


def calculeaza_ruta_osm(lat_start: float, lon_start: float, lat_final: float, lon_final: float):
    if graf_rutier is None or nx is None or ox is None:
        raise RuntimeError("Graful rutier nu este disponibil in acest moment.")

    nod_start = ox.distance.nearest_nodes(graf_rutier, X=lon_start, Y=lat_start)
    nod_final = ox.distance.nearest_nodes(graf_rutier, X=lon_final, Y=lat_final)

    graful_algoritmi, coordonate = pregateste_structuri_algoritmi()
    ruta_noduri, distanta_totala_m = astar_algorithm(
        graful_algoritmi,
        nod_start=nod_start,
        nod_scop=nod_final,
        coordonate=coordonate,
    )

    if not ruta_noduri or distanta_totala_m == float("inf"):
        raise nx.NetworkXNoPath("Nu exista ruta intre punctele selectate.")

    distanta_totala_m = float(distanta_totala_m)

    ruta_gps = construieste_ruta_gps_din_geometrie(graf_rutier, ruta_noduri)
    if len(ruta_gps) < 2:
        ruta_gps = [
            [float(graf_rutier.nodes[nod]["y"]), float(graf_rutier.nodes[nod]["x"])]
            for nod in ruta_noduri
        ]

    durata_estimata_min = (distanta_totala_m / 1000.0) / VITEZA_ESTIMATA_KMH * 60.0
    return ruta_gps, distanta_totala_m, durata_estimata_min

# 1. RUTA PRINCIPALĂ: Harta reală
@app.route("/")
def index():
    return redirect("/map")


# 2. Harta reală (OpenStreetMap + Leaflet)
@app.route("/map")
def show_map():
    return render_template(
        "map.html",
        centru_harta=centru_harta_implicit(),
        traseu_initial=[],
        serviciu_rutare_activ=graf_rutier is not None,
    )


@app.route("/calculeaza-ruta-harta", methods=["POST"])
def calculeaza_ruta_harta():
    date_cerere = request.get_json(silent=True) or {}
    punct_start = date_cerere.get("start", {})
    punct_final = date_cerere.get("end", {})

    try:
        lat_start = float(punct_start.get("lat"))
        lon_start = float(punct_start.get("lon"))
        lat_final = float(punct_final.get("lat"))
        lon_final = float(punct_final.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Coordonate GPS invalide."}), 400

    try:
        drum_gps, distanta_m, durata_min = calculeaza_ruta_osm(
            lat_start,
            lon_start,
            lat_final,
            lon_final,
        )
    except RuntimeError as eroare:
        return jsonify({
            "status": "error",
            "message": str(eroare) + " Instaleaza dependintele si porneste aplicatia cu internet pentru prima incarcare.",
        }), 503
    except nx.NetworkXNoPath:
        return jsonify({"status": "error", "message": "Nu exista ruta rutiera intre punctele selectate."}), 404
    except Exception as eroare:
        return jsonify({"status": "error", "message": f"Eroare la calculul rutei: {eroare}"}), 500

    global traseu_gps_proiectat
    traseu_gps_proiectat = drum_gps

    return jsonify({
        "status": "success",
        "path_gps": drum_gps,
        "distance_m": round(distanta_m, 2),
        "duration_min": round(durata_min, 2),
        "algorithm": "astar",
    })
@app.route('/salveaza_ruta', methods=['POST'])
def salveaza_ruta():
    date_cerere = request.get_json(silent=True) or {}
    puncte_gps = date_cerere.get('path_gps', [])
    distanta_m = date_cerere.get('distance_m')
    durata_min = date_cerere.get('duration_min')
    tip_ruta = str(date_cerere.get('tip_ruta', 'osm_astar')).strip() or 'osm_astar'

    try:
        distanta_m_val = float(distanta_m) if distanta_m is not None else None
        durata_min_val = float(durata_min) if durata_min is not None else None
    except (TypeError, ValueError):
        return jsonify({"status": "error", "mesaj": "distance_m si duration_min trebuie sa fie numere."}), 400

    if not isinstance(puncte_gps, list) or len(puncte_gps) < 2:
        return jsonify({"status": "error", "mesaj": "Ruta GPS invalida. Trimite cel putin doua puncte."}), 400

    for punct in puncte_gps:
        if not isinstance(punct, list) or len(punct) != 2:
            return jsonify({"status": "error", "mesaj": "Fiecare punct GPS trebuie sa fie [lat, lon]."}), 400
        try:
            float(punct[0])
            float(punct[1])
        except (TypeError, ValueError):
            return jsonify({"status": "error", "mesaj": "Coordonatele GPS trebuie sa fie numere reale."}), 400

    print("S-a realizat conexiunea cu baza de date!")
    conn = sqlite3.connect(str(CALE_BAZA_DATE))
    cursor = conn.cursor()
    
    start_punct = str([round(float(puncte_gps[0][0]), 6), round(float(puncte_gps[0][1]), 6)])
    destinatie_punct = str([round(float(puncte_gps[-1][0]), 6), round(float(puncte_gps[-1][1]), 6)])
    traseu_text = f"Ruta rutiera OSM ({tip_ruta}) cu {len(puncte_gps)} puncte"
    if distanta_m_val is not None:
        traseu_text += f", distanta {round(distanta_m_val, 1)} m"
    if durata_min_val is not None:
        traseu_text += f", durata estimata {round(durata_min_val, 1)} min"

    path_gps_json = json.dumps(puncte_gps, ensure_ascii=False)

    cursor.execute('''
        INSERT INTO istoric_rute (
            start_punct,
            destinatie_punct,
            traseu_complet,
            distanta_m,
            durata_min,
            path_gps_json,
            tip_ruta,
            sursa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        start_punct,
        destinatie_punct,
        traseu_text,
        distanta_m_val,
        durata_min_val,
        path_gps_json,
        tip_ruta,
        'click_harta',
    ))
    
    conn.commit()
    print("Datele au fost salvate cu succes!")
    conn.close()
    
    return jsonify({"status": "success", "mesaj": "Ruta a fost salvata!", "itinerariu": traseu_text})


@app.route('/istoric_rute', methods=['GET'])
def istoric_rute():
    limita = request.args.get('limita', default=10, type=int)
    if limita is None or limita < 1 or limita > 100:
        return jsonify({"status": "error", "mesaj": "Parametrul limita trebuie sa fie intre 1 si 100."}), 400

    conn = sqlite3.connect(str(CALE_BAZA_DATE))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT id, start_punct, destinatie_punct, traseu_complet, data_ora,
               distanta_m, durata_min, path_gps_json, tip_ruta, sursa
        FROM istoric_rute
        ORDER BY data_ora DESC, id DESC
        LIMIT ?
        ''',
        (limita,),
    )
    randuri = cursor.fetchall()
    conn.close()

    rezultate = []
    for rand in randuri:
        path_gps = []
        if rand['path_gps_json']:
            try:
                path_gps = json.loads(rand['path_gps_json'])
            except json.JSONDecodeError:
                path_gps = []

        rezultate.append({
            'id': rand['id'],
            'start_punct': rand['start_punct'],
            'destinatie_punct': rand['destinatie_punct'],
            'traseu_complet': rand['traseu_complet'],
            'data_ora': rand['data_ora'],
            'distanta_m': rand['distanta_m'],
            'durata_min': rand['durata_min'],
            'path_gps': path_gps,
            'tip_ruta': rand['tip_ruta'],
            'sursa': rand['sursa'],
        })

    return jsonify({'status': 'success', 'rute': rezultate, 'count': len(rezultate)})

if __name__ == "__main__":
    app.run(debug=True)