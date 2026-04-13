# Sistem de navigație urbană

Aplicația calculează rute reale pe rețeaua rutieră OpenStreetMap pentru zona Baia Mare. Utilizatorul alege punctul de start și destinația direct pe hartă, iar backend-ul calculează cel mai scurt drum pe drumuri reale și îl desenează pe hartă.

## Funcționalități

- rutare pe drumuri reale cu `osmnx` și `networkx`
- selecție start/destinație prin click pe hartă
- afișare traseu pe Leaflet + OpenStreetMap
- calcul distanță și durată estimată
- salvare istoric în SQLite
- cache local pentru graful rutier OSM

## Rulare

1. Instalează dependențele din `requirements.txt`.
2. Pornește aplicația Flask din `src/backend/app.py`.
3. La prima rulare, aplicația poate descărca graful rutier pentru Baia Mare, deci este nevoie de internet.

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

## Observații

- Codul vechi de grid a fost eliminat din fluxul principal.
- Dacă graful OSM nu poate fi încărcat, ruta nu poate fi calculată până când dependențele și cache-ul sunt disponibile.