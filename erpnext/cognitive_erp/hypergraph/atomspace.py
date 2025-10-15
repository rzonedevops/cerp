"""
AtomSpace - Central Knowledge Store

The AtomSpace is the central repository for all atoms (nodes and links) in the
cognitive knowledge graph. It provides methods for adding, querying, and reasoning
over the knowledge base.
"""

from typing import Any, Dict, List, Optional, Set
from .atom import Atom, Node, Link


class AtomSpace:
	"""
	AtomSpace manages the hypergraph knowledge base.
	
	Provides storage, retrieval, and query capabilities for the cognitive layer.
	"""

	def __init__(self):
		self.atoms: Dict[str, Atom] = {}  # id -> Atom
		self.nodes_by_type: Dict[str, Set[str]] = {}  # type -> set of ids
		self.links_by_type: Dict[str, Set[str]] = {}  # type -> set of ids
		self.incoming_links: Dict[str, Set[str]] = {}  # atom_id -> set of link_ids

	def add_atom(self, atom: Atom) -> Atom:
		"""Add an atom to the atomspace."""
		if atom.id in self.atoms:
			return self.atoms[atom.id]

		self.atoms[atom.id] = atom

		# Index by type
		if isinstance(atom, Node):
			if atom.atom_type not in self.nodes_by_type:
				self.nodes_by_type[atom.atom_type] = set()
			self.nodes_by_type[atom.atom_type].add(atom.id)
		elif isinstance(atom, Link):
			if atom.atom_type not in self.links_by_type:
				self.links_by_type[atom.atom_type] = set()
			self.links_by_type[atom.atom_type].add(atom.id)

			# Index incoming links
			for outgoing_atom in atom.get_outgoing():
				if outgoing_atom.id not in self.incoming_links:
					self.incoming_links[outgoing_atom.id] = set()
				self.incoming_links[outgoing_atom.id].add(atom.id)

		return atom

	def add_node(self, node_type: str, name: str, value: Optional[Any] = None, **kwargs) -> Node:
		"""Convenience method to add a node."""
		node = Node(node_type, name, value, **kwargs)
		return self.add_atom(node)

	def add_link(self, link_type: str, outgoing: List[Atom], name: Optional[str] = None, **kwargs) -> Link:
		"""Convenience method to add a link."""
		link = Link(link_type, outgoing, name, **kwargs)
		return self.add_atom(link)

	def get_atom(self, atom_id: str) -> Optional[Atom]:
		"""Get an atom by its ID."""
		return self.atoms.get(atom_id)

	def get_nodes_by_type(self, node_type: str) -> List[Node]:
		"""Get all nodes of a specific type."""
		atom_ids = self.nodes_by_type.get(f"Node:{node_type}", set())
		return [self.atoms[aid] for aid in atom_ids if aid in self.atoms]

	def get_links_by_type(self, link_type: str) -> List[Link]:
		"""Get all links of a specific type."""
		atom_ids = self.links_by_type.get(f"Link:{link_type}", set())
		return [self.atoms[aid] for aid in atom_ids if aid in self.atoms]

	def get_incoming_links(self, atom_id: str) -> List[Link]:
		"""Get all links that reference the given atom."""
		link_ids = self.incoming_links.get(atom_id, set())
		return [self.atoms[lid] for lid in link_ids if lid in self.atoms and isinstance(self.atoms[lid], Link)]

	def query_nodes(
		self, node_type: Optional[str] = None, name_pattern: Optional[str] = None, min_truth: float = 0.0
	) -> List[Node]:
		"""Query nodes with filters."""
		nodes = []

		if node_type:
			nodes = self.get_nodes_by_type(node_type)
		else:
			nodes = [atom for atom in self.atoms.values() if isinstance(atom, Node)]

		# Apply filters
		if name_pattern:
			nodes = [n for n in nodes if name_pattern.lower() in n.name.lower()]

		if min_truth > 0.0:
			nodes = [n for n in nodes if n.truth_value >= min_truth]

		return nodes

	def get_related_atoms(self, atom_id: str, max_depth: int = 1) -> Set[str]:
		"""
		Get all atoms related to the given atom up to max_depth.
		
		Returns a set of atom IDs including the starting atom.
		"""
		related = {atom_id}
		current_level = {atom_id}

		for _ in range(max_depth):
			next_level = set()

			for aid in current_level:
				# Get outgoing atoms from links
				atom = self.atoms.get(aid)
				if atom and isinstance(atom, Link):
					for out_atom in atom.get_outgoing():
						if out_atom.id not in related:
							next_level.add(out_atom.id)
							related.add(out_atom.id)

				# Get incoming links
				for link in self.get_incoming_links(aid):
					if link.id not in related:
						next_level.add(link.id)
						related.add(link.id)

			current_level = next_level
			if not current_level:
				break

		return related

	def get_statistics(self) -> Dict[str, Any]:
		"""Get statistics about the atomspace."""
		node_count = sum(len(ids) for ids in self.nodes_by_type.values())
		link_count = sum(len(ids) for ids in self.links_by_type.values())

		return {
			"total_atoms": len(self.atoms),
			"node_count": node_count,
			"link_count": link_count,
			"node_types": list(self.nodes_by_type.keys()),
			"link_types": list(self.links_by_type.keys()),
		}

	def clear(self):
		"""Clear all atoms from the atomspace."""
		self.atoms.clear()
		self.nodes_by_type.clear()
		self.links_by_type.clear()
		self.incoming_links.clear()
