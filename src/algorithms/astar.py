import heapq
import math
from typing import Callable, Dict, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]
Coordinates = Dict[str, Tuple[float, float]]
Heuristic = Callable[[str, str], float]


def _euclidean_heuristic(coordinates: Coordinates) -> Heuristic:
	def h(node: str, goal: str) -> float:
		x1, y1 = coordinates[node]
		x2, y2 = coordinates[goal]
		return math.hypot(x2 - x1, y2 - y1)

	return h


def _zero_heuristic(_: str, __: str) -> float:
	return 0.0


def astar(
	graph: Graph,
	start: str,
	goal: str,
	coordinates: Optional[Coordinates] = None,
	heuristic: Optional[Heuristic] = None,
) -> Tuple[List[str], float]:
	"""Compute a shortest path using A* on positive-weighted graphs."""
	if start not in graph or goal not in graph:
		raise ValueError("Both start and goal must exist in graph")

	if heuristic is None:
		heuristic = _euclidean_heuristic(coordinates) if coordinates else _zero_heuristic

	g_score: Dict[str, float] = {node: float("inf") for node in graph}
	f_score: Dict[str, float] = {node: float("inf") for node in graph}
	previous: Dict[str, Optional[str]] = {node: None for node in graph}

	g_score[start] = 0.0
	f_score[start] = heuristic(start, goal)

	queue: List[Tuple[float, str]] = [(f_score[start], start)]

	while queue:
		_, current = heapq.heappop(queue)
		if current == goal:
			return _reconstruct(previous, start, goal), g_score[goal]

		for neighbor, weight in graph.get(current, []):
			if weight < 0:
				raise ValueError("A* does not support negative edge weights")

			candidate_g = g_score[current] + weight
			if candidate_g < g_score.get(neighbor, float("inf")):
				previous[neighbor] = current
				g_score[neighbor] = candidate_g
				f_score[neighbor] = candidate_g + heuristic(neighbor, goal)
				heapq.heappush(queue, (f_score[neighbor], neighbor))

	return [], float("inf")


def _reconstruct(previous: Dict[str, Optional[str]], start: str, goal: str) -> List[str]:
	path: List[str] = []
	current: Optional[str] = goal
	while current is not None:
		path.append(current)
		if current == start:
			return list(reversed(path))
		current = previous.get(current)
	return []

