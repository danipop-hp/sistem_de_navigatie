from pathlib import Path
from flask import Flask, jsonify, redirect, render_template, request, url_for
import sqlite3

DIRECTOR_BAZA = Path(__file__).resolve().parent
CALE_BAZA_DATE = DIRECTOR_BAZA / "navigatie.db"

app = Flask(
    __name__,
    template_folder=str(DIRECTOR_BAZA.parent / "frontend" / "templates"),
    static_folder=str(DIRECTOR_BAZA.parent / "frontend" / "static"),
)
def init_db():
    # Această linie creează fișierul navigatie.db automat în folderul tău
    conn = sqlite3.connect(str(CALE_BAZA_DATE))
    cursor = conn.cursor()
    
    # Tabel pentru harta orașului (Grid -> Străzi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS harta_urbana (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            row INTEGER,
            col INTEGER,
            nume_strada TEXT,
            este_drum BOOLEAN
        )
    ''')
    
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
    conn.commit()
    conn.close()

# Apelăm funcția ca să fim siguri că baza de date există la pornirea aplicației
init_db()

# Traseul proiectat din grid in coordonate GPS.
traseu_gps_proiectat = []

# Punct de referinta (coltul stanga-sus al grid-ului 5x5) in Baia Mare.
GRID_REFERENCE_LAT = 47.6568
GRID_REFERENCE_LON = 23.5688
GRID_OFFSET_DEGREES = 0.001
HARTA_ORAS = [
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0],
]


def in_grila(rand, coloana):
    return 0 <= rand < len(HARTA_ORAS) and 0 <= coloana < len(HARTA_ORAS[0])


def este_drum(rand, coloana):
    return in_grila(rand, coloana) and HARTA_ORAS[rand][coloana] == 1


def grid_la_gps(rand, coloana):
    latitudine = GRID_REFERENCE_LAT - (rand * GRID_OFFSET_DEGREES)
    longitudine = GRID_REFERENCE_LON + (coloana * GRID_OFFSET_DEGREES)
    return [latitudine, longitudine]


def gps_la_grid(latitudine, longitudine):
    rand = round((GRID_REFERENCE_LAT - latitudine) / GRID_OFFSET_DEGREES)
    coloana = round((longitudine - GRID_REFERENCE_LON) / GRID_OFFSET_DEGREES)
    return [rand, coloana]


def euristica(nod_curent, nod_final):
    return abs(nod_curent[0] - nod_final[0]) + abs(nod_curent[1] - nod_final[1])


def calculeaza_ruta_astar(punct_start, punct_final):
    directii = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    set_deschis = [punct_start]
    precedent = {}
    scor_g = {punct_start: 0}
    scor_f = {punct_start: euristica(punct_start, punct_final)}

    while set_deschis:
        nod_curent = min(set_deschis, key=lambda punct: scor_f.get(punct, float("inf")))

        if nod_curent == punct_final:
            drum = [nod_curent]
            while nod_curent in precedent:
                nod_curent = precedent[nod_curent]
                drum.append(nod_curent)
            drum.reverse()
            return drum

        set_deschis.remove(nod_curent)
        rand_curent, coloana_curenta = nod_curent

        for delta_rand, delta_coloana in directii:
            rand_vecin = rand_curent + delta_rand
            coloana_vecin = coloana_curenta + delta_coloana

            if not este_drum(rand_vecin, coloana_vecin):
                continue

            vecin = (rand_vecin, coloana_vecin)
            scor_temporar = scor_g[nod_curent] + 1
            if scor_temporar < scor_g.get(vecin, float("inf")):
                precedent[vecin] = nod_curent
                scor_g[vecin] = scor_temporar
                scor_f[vecin] = scor_temporar + euristica(vecin, punct_final)
                if vecin not in set_deschis:
                    set_deschis.append(vecin)

    return []

# 1. RUTA EXISTENTĂ: Grid-ul interactiv
@app.route("/")
def index():
    return redirect(url_for("show_map"))


@app.route("/grid")
def grid():
    return render_template("index.html")

# 2. RUTA NOUĂ: Harta reală (OpenStreetMap + Folium)
@app.route("/map")
def show_map():
    return render_template(
        "map.html",
        centru_harta=[GRID_REFERENCE_LAT, GRID_REFERENCE_LON],
        offset=GRID_OFFSET_DEGREES,
        harta_oras=HARTA_ORAS,
        traseu_initial=traseu_gps_proiectat,
    )


@app.route("/proiecteaza-harta", methods=["POST"])
def proiecteaza():
    date_cerere = request.get_json(silent=True) or {}
    traseu_grid = date_cerere.get("path", [])

    if not isinstance(traseu_grid, list) or not traseu_grid:
        return jsonify({"status": "error", "message": "Path invalid."}), 400

    coordonate_gps = []
    for punct in traseu_grid:
        if not isinstance(punct, list) or len(punct) != 2:
            return jsonify({"status": "error", "message": "Punct de grid invalid."}), 400

        x, y = punct
        if not isinstance(x, int) or not isinstance(y, int):
            return jsonify({"status": "error", "message": "Coordonatele trebuie sa fie intregi."}), 400

        latitudine_reala = GRID_REFERENCE_LAT - (x * GRID_OFFSET_DEGREES)
        longitudine_reala = GRID_REFERENCE_LON + (y * GRID_OFFSET_DEGREES)
        coordonate_gps.append([latitudine_reala, longitudine_reala])

    global traseu_gps_proiectat
    traseu_gps_proiectat = coordonate_gps
    return jsonify({"status": "success", "points": len(coordonate_gps)})


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

    start_grid = gps_la_grid(lat_start, lon_start)
    final_grid = gps_la_grid(lat_final, lon_final)

    if not in_grila(start_grid[0], start_grid[1]) or not in_grila(final_grid[0], final_grid[1]):
        return jsonify({"status": "error", "message": "Punctele sunt in afara zonei de navigatie."}), 400

    if not este_drum(start_grid[0], start_grid[1]) or not este_drum(final_grid[0], final_grid[1]):
        return jsonify({"status": "error", "message": "Selecteaza puncte pe drumuri, nu pe cladiri."}), 400

    drum_grid_tupluri = calculeaza_ruta_astar((start_grid[0], start_grid[1]), (final_grid[0], final_grid[1]))
    if not drum_grid_tupluri:
        return jsonify({"status": "error", "message": "Nu exista ruta intre punctele selectate."}), 404

    drum_grid = [[rand, coloana] for rand, coloana in drum_grid_tupluri]
    drum_gps = [grid_la_gps(rand, coloana) for rand, coloana in drum_grid_tupluri]

    global traseu_gps_proiectat
    traseu_gps_proiectat = drum_gps

    return jsonify({
        "status": "success",
        "path_grid": drum_grid,
        "path_gps": drum_gps,
    })
@app.route('/salveaza_ruta', methods=['POST'])
def salveaza_ruta():
    date_cerere = request.get_json(silent=True) or {}
    puncte = date_cerere.get('puncte') or date_cerere.get('path', [])

    if not isinstance(puncte, list) or len(puncte) < 2:
        return jsonify({"status": "error", "mesaj": "Ruta invalida. Trimite cel putin doua puncte."}), 400

    for punct in puncte:
        if not isinstance(punct, list) or len(punct) != 2:
            return jsonify({"status": "error", "mesaj": "Fiecare punct trebuie sa fie [rand, coloana]."}), 400
        if not isinstance(punct[0], int) or not isinstance(punct[1], int):
            return jsonify({"status": "error", "mesaj": "Coordonatele punctelor trebuie sa fie numere intregi."}), 400

    conn = sqlite3.connect(str(CALE_BAZA_DATE))
    cursor = conn.cursor()
    
    nume_strazi = []
    
    # Pentru fiecare punct din drum, căutăm numele străzii în bază
    for p in puncte:
        cursor.execute("SELECT nume_strada FROM harta_urbana WHERE row = ? AND col = ?", (p[0], p[1]))
        rezultat = cursor.fetchone()
        if rezultat:
            nume_strazi.append(rezultat[0])
        else:
            nume_strazi.append("Zonă necunoscută")

    # Transformăm lista de străzi într-un text frumos
    traseu_text = " -> ".join(nume_strazi)
    
    # Salvăm rezultatul final în istoricul rutelor
    cursor.execute('''
        INSERT INTO istoric_rute (start_punct, destinatie_punct, traseu_complet)
        VALUES (?, ?, ?)
    ''', (str(puncte[0]), str(puncte[-1]), traseu_text))
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "mesaj": "Ruta a fost salvată!", "itinerariu": traseu_text})

if __name__ == "__main__":
    app.run(debug=True)