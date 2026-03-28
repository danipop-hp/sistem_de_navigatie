from typing import Dict, Iterable, List, Tuple


CoordinateMap = Dict[str, Tuple[float, float]]


def path_to_gps(path: Iterable[str], coordinates: CoordinateMap) -> List[List[float]]:
	"""Map a node-id path to [lat, lon] pairs."""
	gps: List[List[float]] = []
	for node in path:
		lat, lon = coordinates[node]
		gps.append([lat, lon])
	return gps


def path_to_geojson_line(path: Iterable[str], coordinates: CoordinateMap) -> Dict[str, object]:
	"""Return a minimal GeoJSON LineString from graph path."""
	line = []
	for node in path:
		lat, lon = coordinates[node]
		line.append([lon, lat])
	return {
		"type": "Feature",
		"geometry": {
			"type": "LineString",
			"coordinates": line,
		},
		"properties": {},
	}

