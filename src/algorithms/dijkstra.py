import heapq
from typing import Dict, Iterable, List, Optional, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


def dijkstra(graph: Graph, start: str, goal: Optional[str] = None) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
	"""Compute shortest paths from start for non-negative weighted graphs."""
	distances: Dict[str, float] = {node: float("inf") for node in graph}
	previous: Dict[str, Optional[str]] = {node: None for node in graph}

	if start not in graph:
		raise ValueError(f"Unknown start node: {start}")

	distances[start] = 0.0
	queue: List[Tuple[float, str]] = [(0.0, start)]

	while queue:
		current_distance, current_node = heapq.heappop(queue)
		if current_distance > distances[current_node]:
			continue

		if goal is not None and current_node == goal:
			break

		for neighbor, weight in graph.get(current_node, []):
			if weight < 0:
				raise ValueError("Dijkstra does not support negative edge weights")

			candidate = current_distance + weight
			if candidate < distances.get(neighbor, float("inf")):
				distances[neighbor] = candidate
				previous[neighbor] = current_node
				heapq.heappush(queue, (candidate, neighbor))

	return distances, previous


def reconstruct_path(previous: Dict[str, Optional[str]], start: str, goal: str) -> List[str]:
	"""Reconstruct path from predecessor links."""
	if start == goal:
		return [start]

	path: List[str] = []
	current: Optional[str] = goal
	while current is not None:
		path.append(current)
		if current == start:
			return list(reversed(path))
		current = previous.get(current)

	return []


def shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
	"""Convenience helper returning both path and cost."""
	distances, previous = dijkstra(graph, start=start, goal=goal)
	path = reconstruct_path(previous, start=start, goal=goal)
	return path, distances.get(goal, float("inf"))

