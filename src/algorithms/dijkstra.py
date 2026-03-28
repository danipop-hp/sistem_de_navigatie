import heapq
from typing import Dict, Iterable, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


def dijkstra(graf: Graph, nod_start: str, nod_scop: Optional[str] = None) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
	"""Compute shortest paths from start for non-negative weighted graphs."""
	distante: Dict[str, float] = {nod: float("inf") for nod in graf}
	precedent: Dict[str, Optional[str]] = {nod: None for nod in graf}

	if nod_start not in graf:
		raise ValueError(f"Unknown start node: {nod_start}")

	distante[nod_start] = 0.0
	coada: List[Tuple[float, str]] = [(0.0, nod_start)]

	while coada:
		distanta_curenta, nod_curent = heapq.heappop(coada)
		if distanta_curenta > distante[nod_curent]:
			continue

		if nod_scop is not None and nod_curent == nod_scop:
			break

		for vecin, pondere in graf.get(nod_curent, []):
			if pondere < 0:
				raise ValueError("Dijkstra does not support negative edge weights")

			cost_candidat = distanta_curenta + pondere
			if cost_candidat < distante.get(vecin, float("inf")):
				distante[vecin] = cost_candidat
				precedent[vecin] = nod_curent
				heapq.heappush(coada, (cost_candidat, vecin))

	return distante, precedent


def reconstruct_path(precedent: Dict[str, Optional[str]], nod_start: str, nod_scop: str) -> List[str]:
	"""Reconstruct path from predecessor links."""
	if nod_start == nod_scop:
		return [nod_start]

	drum: List[str] = []
	nod_curent: Optional[str] = nod_scop
	while nod_curent is not None:
		drum.append(nod_curent)
		if nod_curent == nod_start:
			return list(reversed(drum))
		nod_curent = precedent.get(nod_curent)

	return []


def shortest_path(graf: Graph, nod_start: str, nod_scop: str) -> Tuple[List[str], float]:
	"""Convenience helper returning both path and cost."""
	distante, precedent = dijkstra(graf, nod_start=nod_start, nod_scop=nod_scop)
	drum = reconstruct_path(precedent, nod_start=nod_start, nod_scop=nod_scop)
	return drum, distante.get(nod_scop, float("inf"))

