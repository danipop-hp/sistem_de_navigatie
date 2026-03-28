from typing import Dict, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


class NegativeCycleError(ValueError):
	"""Raised when a reachable negative cycle exists in the graph."""


def bellman_ford(graph: Graph, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
	"""Compute shortest path distances and detect reachable negative cycles."""
	if start not in graph:
		raise ValueError(f"Unknown start node: {start}")

	distances: Dict[str, float] = {node: float("inf") for node in graph}
	previous: Dict[str, Optional[str]] = {node: None for node in graph}
	distances[start] = 0.0

	nodes = list(graph.keys())
	for _ in range(max(len(nodes) - 1, 0)):
		changed = False
		for node in nodes:
			if distances[node] == float("inf"):
				continue
			for neighbor, weight in graph.get(node, []):
				candidate = distances[node] + weight
				if candidate < distances.get(neighbor, float("inf")):
					distances[neighbor] = candidate
					previous[neighbor] = node
					changed = True
		if not changed:
			break

	for node in nodes:
		if distances[node] == float("inf"):
			continue
		for neighbor, weight in graph.get(node, []):
			if distances[node] + weight < distances.get(neighbor, float("inf")):
				raise NegativeCycleError("Negative cycle detected")

	return distances, previous

