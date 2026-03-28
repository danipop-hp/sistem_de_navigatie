from pathlib import Path
from flask import Flask, jsonify, render_template, request
import folium 
BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    # Păstrăm setările pentru folderele de frontend
    template_folder=str(BASE_DIR.parent / "frontend" / "templates"),
    static_folder=str(BASE_DIR.parent / "frontend" / "static"),
)

# Traseul proiectat din grid in coordonate GPS.
projected_gps_path = []

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
    start_coords = [GRID_REFERENCE_LAT, GRID_REFERENCE_LON]

    # Creăm obiectul hartă
    m = folium.Map(
        location=start_coords, 
        zoom_start=16,
        tiles="OpenStreetMap"
    )
    
    if projected_gps_path:
        folium.PolyLine(
            locations=projected_gps_path,
            color="red",
            weight=6,
            opacity=0.9,
            tooltip="Drumul optim proiectat din grid"
        ).add_to(m)

        folium.Marker(
            location=projected_gps_path[0],
            popup="Start",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(m)

        folium.Marker(
            location=projected_gps_path[-1],
            popup="Destinație",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m)
    else:
        # Dacă nu avem încă un traseu, afișăm doar punctul de referință.
        folium.Marker(
            location=start_coords,
            popup="Centrul Baia Mare",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

    # Transformăm obiectul harta în HTML pentru a fi afișat de browser
    return m._repr_html_()


@app.route("/proiecteaza-harta", methods=["POST"])
def proiecteaza():
    data = request.get_json(silent=True) or {}
    grid_path = data.get("path", [])

    if not isinstance(grid_path, list) or not grid_path:
        return jsonify({"status": "error", "message": "Path invalid."}), 400

    gps_coords = []
    for point in grid_path:
        if not isinstance(point, list) or len(point) != 2:
            return jsonify({"status": "error", "message": "Punct de grid invalid."}), 400

        x, y = point
        if not isinstance(x, int) or not isinstance(y, int):
            return jsonify({"status": "error", "message": "Coordonatele trebuie sa fie intregi."}), 400

        real_lat = GRID_REFERENCE_LAT - (x * GRID_OFFSET_DEGREES)
        real_lon = GRID_REFERENCE_LON + (y * GRID_OFFSET_DEGREES)
        gps_coords.append([real_lat, real_lon])

    global projected_gps_path
    projected_gps_path = gps_coords
    return jsonify({"status": "success", "points": len(gps_coords)})

if __name__ == "__main__":
    app.run(debug=True)