from typing import Dict, Iterable, List, Tuple


CoordinateMap = Dict[str, Tuple[float, float]]


def path_to_gps(drum: Iterable[str], coordonate: CoordinateMap) -> List[List[float]]:
	"""Map a node-id path to [lat, lon] pairs."""
	coordonate_gps: List[List[float]] = []
	for nod in drum:
		latitudine, longitudine = coordonate[nod]
		coordonate_gps.append([latitudine, longitudine])
	return coordonate_gps


def path_to_geojson_line(drum: Iterable[str], coordonate: CoordinateMap) -> Dict[str, object]:
	"""Return a minimal GeoJSON LineString from graph path."""
	linie = []
	for nod in drum:
		latitudine, longitudine = coordonate[nod]
		linie.append([longitudine, latitudine])
	return {
		"type": "Feature",
		"geometry": {
			"type": "LineString",
			"coordinates": linie,
		},
		"properties": {},
	}

