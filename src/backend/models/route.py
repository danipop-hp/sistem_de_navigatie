from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Route:
	"""Represents a path and its aggregate cost."""

	noduri: List[str] = field(default_factory=list)
	cost_total: float = 0.0

	def to_dict(self) -> Dict[str, object]:
		return {
			"noduri": self.noduri,
			"cost_total": self.cost_total,
		}

