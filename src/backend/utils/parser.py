from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


Graph = Dict[str, List[Tuple[str, float]]]


def parse_adjacency(date_brute: Dict[str, Iterable[Sequence[object]]]) -> Graph:
	"""Validate and normalize a dict adjacency representation."""
	graf: Graph = {}
	for nod, vecini in date_brute.items():
		normalizat: List[Tuple[str, float]] = []
		for muchie in vecini:
			if len(muchie) != 2:
				raise ValueError("Each edge must contain (neighbor, weight)")
			tinta, pondere = muchie
			normalizat.append((str(tinta), float(pondere)))
		graf[str(nod)] = normalizat
	return graf


def build_grid_graph(
	randuri: int,
	coloane: int,
	blocate: Optional[Iterable[Tuple[int, int]]] = None,
	pondere: float = 1.0,
) -> Graph:
	"""Create a 4-neighbor weighted grid graph."""
	multime_blocate: Set[Tuple[int, int]] = set(blocate or [])
	graf: Graph = {}
	directii = ((1, 0), (-1, 0), (0, 1), (0, -1))

	for rand in range(randuri):
		for coloana in range(coloane):
			if (rand, coloana) in multime_blocate:
				continue
			nod = f"{rand},{coloana}"
			graf[nod] = []
			for delta_rand, delta_coloana in directii:
				rand_vecin, coloana_vecin = rand + delta_rand, coloana + delta_coloana
				if rand_vecin < 0 or rand_vecin >= randuri or coloana_vecin < 0 or coloana_vecin >= coloane:
					continue
				if (rand_vecin, coloana_vecin) in multime_blocate:
					continue
				graf[nod].append((f"{rand_vecin},{coloana_vecin}", pondere))
	return graf


def grid_path_to_cells(drum: Iterable[str]) -> List[List[int]]:
	"""Convert path like ['0,0', '0,1'] to [[0,0], [0,1]]."""
	celule: List[List[int]] = []
	for nod in drum:
		rand_s, coloana_s = nod.split(",", maxsplit=1)
		celule.append([int(rand_s), int(coloana_s)])
	return celule

