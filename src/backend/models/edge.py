from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
	"""Directed weighted edge between two nodes."""

	sursa: str
	tinta: str
	pondere: float = 1.0

