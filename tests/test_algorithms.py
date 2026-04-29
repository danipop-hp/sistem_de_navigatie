import pytest

from src.algorithms.astar import astar
from src.algorithms.bellman_ford import NegativeCycleError, bellman_ford
from src.algorithms.dijkstra import dijkstra, shortest_path


def test_dijkstra_gaseste_drum_minim():
	graf = {
		"A": [("B", 2.0), ("C", 5.0)],
		"B": [("C", 1.0), ("D", 4.0)],
		"C": [("D", 1.0)],
		"D": [],
	}

	drum, cost = shortest_path(graf, nod_start="A", nod_scop="D")

	assert drum == ["A", "B", "C", "D"]
	assert cost == pytest.approx(4.0)


def test_dijkstra_respinge_ponderi_negative():
	graf = {
		"A": [("B", -2.0)],
		"B": [],
	}

	with pytest.raises(ValueError, match="negative"):
		dijkstra(graf, nod_start="A")


def test_bellman_ford_detecteaza_ciclu_negativ():
	graf = {
		"A": [("B", 1.0)],
		"B": [("C", -3.0)],
		"C": [("A", 1.0)],
	}

	with pytest.raises(NegativeCycleError):
		bellman_ford(graf, nod_start="A")


def test_astar_cu_coordonate_returneaza_drum_minim():
	graf = {
		"A": [("B", 1.0), ("C", 4.0)],
		"B": [("D", 1.0)],
		"C": [("D", 1.0)],
		"D": [],
	}
	coordonate = {
		"A": (0.0, 0.0),
		"B": (1.0, 0.0),
		"C": (0.0, 1.0),
		"D": (2.0, 0.0),
	}

	drum, cost = astar(graf, nod_start="A", nod_scop="D", coordonate=coordonate)

	assert drum == ["A", "B", "D"]
	assert cost == pytest.approx(2.0)


def test_astar_noduri_inexistente():
	graf = {
		"A": [("B", 1.0)],
		"B": [],
	}

	with pytest.raises(ValueError):
		astar(graf, nod_start="A", nod_scop="Z")
