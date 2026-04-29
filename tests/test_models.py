from src.backend.models import Edge, Node, Route


def test_node_memoreaza_coordonate():
	nod = Node(
		id_nod="N1",
		x=10.0,
		y=20.0,
		latitudine=47.65,
		longitudine=23.57,
	)

	assert nod.id_nod == "N1"
	assert nod.x == 10.0
	assert nod.latitudine == 47.65


def test_edge_are_valori_implicite_corecte():
	muchie = Edge(sursa="A", tinta="B")

	assert muchie.sursa == "A"
	assert muchie.tinta == "B"
	assert muchie.pondere == 1.0


def test_route_to_dict_functioneaza():
	ruta = Route(noduri=["A", "B", "C"], cost_total=12.5)

	assert ruta.to_dict() == {
		"noduri": ["A", "B", "C"],
		"cost_total": 12.5,
	}
