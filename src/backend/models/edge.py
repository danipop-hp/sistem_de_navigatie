from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
	"""Directed weighted edge between two nodes."""

	source: str
	target: str
	weight: float = 1.0

