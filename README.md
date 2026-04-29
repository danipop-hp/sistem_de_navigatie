# Sistem de navigație urbană

Aplicația calculează rute reale pe rețeaua rutieră OpenStreetMap pentru zona Baia Mare. Utilizatorul alege punctul de start și destinația direct pe hartă, iar backend-ul calculează cel mai scurt drum pe drumuri reale și îl desenează pe hartă.

## Funcționalități

- rutare pe drumuri reale cu `osmnx` și `networkx`
- rutare automată cu `A*` (fără selecție algoritm în UI)
- selecție start/destinație prin click pe hartă
- afișare traseu pe Leaflet + OpenStreetMap
- calcul distanță și durată estimată
- salvare istoric în SQLite
- cache local pentru graful rutier OSM
- panou istoric rute în interfață (reafișare rută salvată)
- API pentru consultare istoric rute

## Rulare

1. Creează și activează un mediu virtual Python.
2. Instalează dependențele:
	 - `pip install -r requirements.txt`
3. Rulează aplicația:
	 - `python src/backend/app.py`
4. Deschide în browser:
	 - `http://127.0.0.1:5000/map`
5. La prima rulare, aplicația poate descărca graful rutier pentru Baia Mare, deci este nevoie de internet.

## Testare

Rulează suita completă de teste:

- `pytest -q`

Acoperire actuală:

- algoritmi (`A*`, `Dijkstra`, `Bellman-Ford`)
- modele (`Node`, `Edge`, `Route`)
- endpoint-uri principale Flask (calcul rută, salvare, istoric)

## Endpoint-uri API

- `POST /calculeaza-ruta-harta`
	- body: `{"start": {"lat": ..., "lon": ...}, "end": {"lat": ..., "lon": ...}}`
	- răspuns succes: `path_gps`, `distance_m`, `duration_min`, `algorithm`
	- `algorithm` din răspuns este mereu `astar`
- `POST /salveaza_ruta`
	- body: `{"path_gps": [[lat, lon], ...], "distance_m": ..., "duration_min": ..., "tip_ruta": "osm_astar"}`
	- salvează ruta în SQLite
- `GET /istoric_rute?limita=10`
	- întoarce ultimele rute salvate (limita între 1 și 100)

## Bază de date

Aplicația folosește fișierul SQLite `src/backend/navigatie.db`. Tabelul `istoric_rute` salvează:

- `start_punct`
- `destinatie_punct`
- `traseu_complet`
- `data_ora`
- `distanta_m`
- `durata_min`
- `path_gps_json`
- `tip_ruta`
- `sursa`

## Scenariu de prezentare (2-3 minute)

1. Deschide harta (`/map`) și explică faptul că rutarea se face pe drumuri reale OSM.
2. Click pe start și destinație, arată ruta, distanța și durata estimată.
3. Arată că ruta este salvată automat în istoric.
4. Din panoul „Istoric rute”, reafișează o rută salvată.
5. Rulează `pytest -q` pentru a demonstra stabilitatea logicii și a API-ului.

## Observații

- Codul vechi de grid a fost eliminat din fluxul principal.
- Dacă graful OSM nu poate fi încărcat, ruta nu poate fi calculată până când dependențele și cache-ul sunt disponibile.