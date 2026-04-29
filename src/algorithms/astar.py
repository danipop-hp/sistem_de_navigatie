import heapq
import math
from typing import Callable, Dict, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]
Coordinates = Dict[str, Tuple[float, float]]
Heuristic = Callable[[str, str], float]


def _euclidean_heuristic(coordonate: Coordinates) -> Heuristic:
	def h(nod: str, scop: str) -> float:
		if nod not in coordonate or scop not in coordonate:
			return 0.0

		x1, y1 = coordonate[nod]
		x2, y2 = coordonate[scop]
		return math.hypot(x2 - x1, y2 - y1)

	return h


def _zero_heuristic(_: str, __: str) -> float:
	return 0.0


def astar(
	graf: Graph,
	nod_start: str,
	nod_scop: str,
	coordonate: Optional[Coordinates] = None,
	heuristica: Optional[Heuristic] = None,
) -> Tuple[List[str], float]:
	"""Compute a shortest path using A* on positive-weighted graphs."""
	if nod_start not in graf or nod_scop not in graf:
		raise ValueError("Both start and goal must exist in graph")

	if heuristica is None:
		heuristica = _euclidean_heuristic(coordonate) if coordonate else _zero_heuristic

	scor_g: Dict[str, float] = {nod: float("inf") for nod in graf}
	scor_f: Dict[str, float] = {nod: float("inf") for nod in graf}
	precedent: Dict[str, Optional[str]] = {nod: None for nod in graf}

	scor_g[nod_start] = 0.0
	scor_f[nod_start] = heuristica(nod_start, nod_scop)

	coada: List[Tuple[float, str]] = [(scor_f[nod_start], nod_start)]

	while coada:
		_, nod_curent = heapq.heappop(coada)
		if nod_curent == nod_scop:
			return _reconstruct(precedent, nod_start, nod_scop), scor_g[nod_scop]

		for vecin, pondere in graf.get(nod_curent, []):
			if pondere < 0:
				raise ValueError("A* does not support negative edge weights")

			cost_candidat_g = scor_g[nod_curent] + pondere
			if cost_candidat_g < scor_g.get(vecin, float("inf")):
				precedent[vecin] = nod_curent
				scor_g[vecin] = cost_candidat_g
				scor_f[vecin] = cost_candidat_g + heuristica(vecin, nod_scop)
				heapq.heappush(coada, (scor_f[vecin], vecin))

	return [], float("inf")


def _reconstruct(precedent: Dict[str, Optional[str]], nod_start: str, nod_scop: str) -> List[str]:
	drum: List[str] = []
	nod_curent: Optional[str] = nod_scop
	while nod_curent is not None:
		drum.append(nod_curent)
		if nod_curent == nod_start:
			return list(reversed(drum))
		nod_curent = precedent.get(nod_curent)
	return []

