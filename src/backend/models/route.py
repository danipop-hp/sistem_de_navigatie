from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Route:
	"""Represents a path and its aggregate cost."""

	nodes: List[str] = field(default_factory=list)
	total_cost: float = 0.0

	def to_dict(self) -> Dict[str, object]:
		return {
			"nodes": self.nodes,
			"total_cost": self.total_cost,
		}

