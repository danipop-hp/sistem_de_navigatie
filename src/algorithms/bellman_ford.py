from typing import Dict, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


class NegativeCycleError(ValueError):
	"""Raised when a reachable negative cycle exists in the graph."""


def bellman_ford(graf: Graph, nod_start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
	"""Compute shortest path distances and detect reachable negative cycles."""
	if nod_start not in graf:
		raise ValueError(f"Unknown start node: {nod_start}")

	distante: Dict[str, float] = {nod: float("inf") for nod in graf}
	precedent: Dict[str, Optional[str]] = {nod: None for nod in graf}
	distante[nod_start] = 0.0

	noduri = list(graf.keys())
	for _ in range(max(len(noduri) - 1, 0)):
		modificat = False
		for nod in noduri:
			if distante[nod] == float("inf"):
				continue
			for vecin, pondere in graf.get(nod, []):
				cost_candidat = distante[nod] + pondere
				if cost_candidat < distante.get(vecin, float("inf")):
					distante[vecin] = cost_candidat
					precedent[vecin] = nod
					modificat = True
		if not modificat:
			break

	for nod in noduri:
		if distante[nod] == float("inf"):
			continue
		for vecin, pondere in graf.get(nod, []):
			if distante[nod] + pondere < distante.get(vecin, float("inf")):
				raise NegativeCycleError("Negative cycle detected")

	return distante, precedent

