from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


def parse_adjacency(raw: Dict[str, Iterable[Sequence[object]]]) -> Graph:
	"""Validate and normalize a dict adjacency representation."""
	graph: Graph = {}
	for node, neighbors in raw.items():
		normalized: List[Tuple[str, float]] = []
		for edge in neighbors:
			if len(edge) != 2:
				raise ValueError("Each edge must contain (neighbor, weight)")
			target, weight = edge
			normalized.append((str(target), float(weight)))
		graph[str(node)] = normalized
	return graph


def build_grid_graph(
	rows: int,
	cols: int,
	blocked: Optional[Iterable[Tuple[int, int]]] = None,
	weight: float = 1.0,
) -> Graph:
	"""Create a 4-neighbor weighted grid graph."""
	blocked_set: Set[Tuple[int, int]] = set(blocked or [])
	graph: Graph = {}
	directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

	for r in range(rows):
		for c in range(cols):
			if (r, c) in blocked_set:
				continue
			node = f"{r},{c}"
			graph[node] = []
			for dr, dc in directions:
				nr, nc = r + dr, c + dc
				if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
					continue
				if (nr, nc) in blocked_set:
					continue
				graph[node].append((f"{nr},{nc}", weight))
	return graph


def grid_path_to_cells(path: Iterable[str]) -> List[List[int]]:
	"""Convert path like ['0,0', '0,1'] to [[0,0], [0,1]]."""
	cells: List[List[int]] = []
	for node in path:
		row_s, col_s = node.split(",", maxsplit=1)
		cells.append([int(row_s), int(col_s)])
	return cells

