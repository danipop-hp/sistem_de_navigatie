from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Node:
	"""Graph node with optional cartesian and GPS coordinates."""

	node_id: str
	x: Optional[float] = None
	y: Optional[float] = None
	lat: Optional[float] = None
	lon: Optional[float] = None

