from pathlib import Path
from flask import Flask, jsonify, render_template, request
import folium
DIRECTOR_BAZA = Path(__file__).resolve().parent

app = Flask(
    __name__,
    # Păstrăm setările pentru folderele de frontend
    template_folder=str(DIRECTOR_BAZA.parent / "frontend" / "templates"),
    static_folder=str(DIRECTOR_BAZA.parent / "frontend" / "static"),
)

# Traseul proiectat din grid in coordonate GPS.
traseu_gps_proiectat = []

# Punct de referinta (coltul stanga-sus al grid-ului 5x5) in Baia Mare.
GRID_REFERENCE_LAT = 47.6568
GRID_REFERENCE_LON = 23.5688
GRID_OFFSET_DEGREES = 0.001

# 1. RUTA EXISTENTĂ: Grid-ul interactiv
@app.route("/")
def index():
    return render_template("index.html")

# 2. RUTA NOUĂ: Harta reală (OpenStreetMap + Folium)
@app.route("/map")
def show_map():
    # Coordonate de start: Centrul orasului Baia Mare
    coordonate_start = [GRID_REFERENCE_LAT, GRID_REFERENCE_LON]

    # Creăm obiectul hartă
    harta = folium.Map(
        location=coordonate_start,
        zoom_start=16,
        tiles="OpenStreetMap"
    )

    if traseu_gps_proiectat:
        folium.PolyLine(
            locations=traseu_gps_proiectat,
            color="red",
            weight=6,
            opacity=0.9,
            tooltip="Drumul optim proiectat din grid"
        ).add_to(harta)

        folium.Marker(
            location=traseu_gps_proiectat[0],
            popup="Start",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(harta)

        folium.Marker(
            location=traseu_gps_proiectat[-1],
            popup="Destinație",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(harta)
    else:
        # Dacă nu avem încă un traseu, afișăm doar punctul de referință.
        folium.Marker(
            location=coordonate_start,
            popup="Centrul Baia Mare",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(harta)

    # Transformăm obiectul harta în HTML pentru a fi afișat de browser
    return harta._repr_html_()


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

if __name__ == "__main__":
    app.run(debug=True)