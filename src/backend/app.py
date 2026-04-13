from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request
import json
import sqlite3
from typing import List, Optional

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
            return ox.load_graphml(filepath=str(FISIER_GRAF_RUTIER))

        ox.settings.use_cache = True
        graf_nou = ox.graph_from_place(LOCALITATE_IMPLICITA, network_type="drive", simplify=True)
        ox.save_graphml(graf_nou, filepath=str(FISIER_GRAF_RUTIER))
        return graf_nou
    except Exception as eroare:
        print(f"[navigatie] Nu s-a putut incarca graful rutier: {eroare}")
        return None


graf_rutier = incarca_sau_genereaza_graf_rutier()


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

    ruta_noduri = nx.shortest_path(graf_rutier, nod_start, nod_final, weight="length")
    distanta_totala_m = float(nx.shortest_path_length(graf_rutier, nod_start, nod_final, weight="length"))

    ruta_gps = []
    for nod in ruta_noduri:
        ruta_gps.append([float(graf_rutier.nodes[nod]["y"]), float(graf_rutier.nodes[nod]["x"])])

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
        drum_gps, distanta_m, durata_min = calculeaza_ruta_osm(lat_start, lon_start, lat_final, lon_final)
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
    })
@app.route('/salveaza_ruta', methods=['POST'])
def salveaza_ruta():
    date_cerere = request.get_json(silent=True) or {}
    puncte_gps = date_cerere.get('path_gps', [])
    distanta_m = date_cerere.get('distance_m')
    durata_min = date_cerere.get('duration_min')

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
    traseu_text = f"Ruta rutiera OSM cu {len(puncte_gps)} puncte"
    if distanta_m is not None:
        traseu_text += f", distanta {round(float(distanta_m), 1)} m"
    if durata_min is not None:
        traseu_text += f", durata estimata {round(float(durata_min), 1)} min"

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
        float(distanta_m) if distanta_m is not None else None,
        float(durata_min) if durata_min is not None else None,
        path_gps_json,
        'osm_drive',
        'click_harta',
    ))
    
    conn.commit()
    print("Datele au fost salvate cu succes!")
    conn.close()
    
    return jsonify({"status": "success", "mesaj": "Ruta a fost salvata!", "itinerariu": traseu_text})

if __name__ == "__main__":
    app.run(debug=True)