"""
Atom Classes

Basic building blocks for the hypergraph knowledge representation system.
Inspired by OpenCog's Atomspace design.
"""

from typing import Any, Dict, List, Optional, Set
from uuid import uuid4


class Atom:
	"""
	Base class for all atoms in the hypergraph.
	
	An atom represents a node or link in the knowledge graph with associated
	truth values and attention values.
	"""

	def __init__(
		self,
		atom_type: str,
		name: Optional[str] = None,
		truth_value: float = 1.0,
		attention_value: float = 0.0,
	):
		self.id = str(uuid4())
		self.atom_type = atom_type
		self.name = name or self.id
		self.truth_value = truth_value  # Confidence in [0, 1]
		self.attention_value = attention_value  # Importance/relevance
		self.metadata: Dict[str, Any] = {}

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(type={self.atom_type}, name={self.name})"

	def to_dict(self) -> Dict[str, Any]:
		"""Convert atom to dictionary representation."""
		return {
			"id": self.id,
			"atom_type": self.atom_type,
			"name": self.name,
			"truth_value": self.truth_value,
			"attention_value": self.attention_value,
			"metadata": self.metadata,
		}


class Node(Atom):
	"""
	Node represents a concept, entity, or data point in the knowledge graph.
	
	Examples: Customer, Product, Invoice, etc.
	"""

	def __init__(
		self,
		node_type: str,
		name: str,
		value: Optional[Any] = None,
		truth_value: float = 1.0,
		attention_value: float = 0.0,
	):
		super().__init__(atom_type=f"Node:{node_type}", name=name, truth_value=truth_value, attention_value=attention_value)
		self.value = value

	def to_dict(self) -> Dict[str, Any]:
		"""Convert node to dictionary representation."""
		data = super().to_dict()
		data["value"] = self.value
		return data


class Link(Atom):
	"""
	Link represents a relationship between atoms in the knowledge graph.
	
	Examples: CustomerBuysProduct, InvoiceHasItem, etc.
	"""

	def __init__(
		self,
		link_type: str,
		outgoing: List[Atom],
		name: Optional[str] = None,
		truth_value: float = 1.0,
		attention_value: float = 0.0,
	):
		super().__init__(atom_type=f"Link:{link_type}", name=name, truth_value=truth_value, attention_value=attention_value)
		self.outgoing = outgoing  # List of atoms this link connects

	def get_outgoing(self) -> List[Atom]:
		"""Get the atoms connected by this link."""
		return self.outgoing

	def to_dict(self) -> Dict[str, Any]:
		"""Convert link to dictionary representation."""
		data = super().to_dict()
		data["outgoing"] = [atom.id for atom in self.outgoing]
		return data
