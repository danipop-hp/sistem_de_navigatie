from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Node:
	"""Graph node with optional cartesian and GPS coordinates."""

	id_nod: str
	x: Optional[float] = None
	y: Optional[float] = None
	latitudine: Optional[float] = None
	longitudine: Optional[float] = None

