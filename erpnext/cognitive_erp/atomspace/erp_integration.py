"""
ERP Integration Module

Provides integration between ERP entities and the cognitive atomspace.
Converts ERP documents to hypergraph nodes and links.
"""

from typing import Any, Dict, List, Optional
from . import get_atomspace


class ERPCognitiveIntegration:
	"""
	Integrates ERP entities with the cognitive atomspace.
	
	Provides methods to represent ERP documents as nodes and relationships as links.
	"""

	def __init__(self):
		self.atomspace = get_atomspace()

	def create_entity_node(
		self, entity_type: str, entity_id: str, entity_data: Dict[str, Any], truth_value: float = 1.0
	) -> str:
		"""
		Create a node representing an ERP entity.
		
		Args:
			entity_type: Type of entity (e.g., "Customer", "Invoice", "Product")
			entity_id: Unique identifier for the entity
			entity_data: Dictionary of entity attributes
			truth_value: Confidence in this entity (default 1.0)
			
		Returns:
			Node ID
		"""
		node_name = f"{entity_type}:{entity_id}"
		node = self.atomspace.add_node(
			node_type=entity_type, name=node_name, value=entity_data, truth_value=truth_value
		)
		return node.id

	def create_relationship_link(
		self,
		relationship_type: str,
		source_id: str,
		target_id: str,
		relationship_data: Optional[Dict[str, Any]] = None,
		truth_value: float = 1.0,
	) -> str:
		"""
		Create a link representing a relationship between ERP entities.
		
		Args:
			relationship_type: Type of relationship (e.g., "CustomerBuys", "InvoiceContains")
			source_id: Source atom ID
			target_id: Target atom ID
			relationship_data: Optional dictionary of relationship attributes
			truth_value: Confidence in this relationship (default 1.0)
			
		Returns:
			Link ID
		"""
		source_atom = self.atomspace.get_atom(source_id)
		target_atom = self.atomspace.get_atom(target_id)

		if not source_atom or not target_atom:
			raise ValueError("Source or target atom not found")

		link = self.atomspace.add_link(
			link_type=relationship_type, outgoing=[source_atom, target_atom], truth_value=truth_value
		)

		if relationship_data:
			link.metadata.update(relationship_data)

		return link.id

	def get_entity_relationships(self, entity_id: str, relationship_type: Optional[str] = None) -> List[Dict]:
		"""
		Get all relationships for an entity.
		
		Args:
			entity_id: Entity atom ID
			relationship_type: Optional filter by relationship type
			
		Returns:
			List of relationship dictionaries
		"""
		incoming_links = self.atomspace.get_incoming_links(entity_id)

		if relationship_type:
			incoming_links = [link for link in incoming_links if link.atom_type == f"Link:{relationship_type}"]

		return [link.to_dict() for link in incoming_links]

	def get_connected_entities(self, entity_id: str, max_depth: int = 2) -> Dict[str, Any]:
		"""
		Get all entities connected to the given entity.
		
		Args:
			entity_id: Starting entity atom ID
			max_depth: Maximum depth to traverse (default 2)
			
		Returns:
			Dictionary with connected nodes and links
		"""
		related_ids = self.atomspace.get_related_atoms(entity_id, max_depth=max_depth)

		nodes = []
		links = []

		for atom_id in related_ids:
			atom = self.atomspace.get_atom(atom_id)
			if atom:
				atom_dict = atom.to_dict()
				if atom.atom_type.startswith("Node:"):
					nodes.append(atom_dict)
				elif atom.atom_type.startswith("Link:"):
					links.append(atom_dict)

		return {"nodes": nodes, "links": links}

	def query_entities_by_pattern(
		self, entity_type: Optional[str] = None, pattern: Optional[str] = None, min_truth: float = 0.0
	) -> List[Dict]:
		"""
		Query entities by type and pattern.
		
		Args:
			entity_type: Optional entity type filter
			pattern: Optional name pattern to match
			min_truth: Minimum truth value threshold
			
		Returns:
			List of matching entity dictionaries
		"""
		nodes = self.atomspace.query_nodes(node_type=entity_type, name_pattern=pattern, min_truth=min_truth)
		return [node.to_dict() for node in nodes]

	def get_statistics(self) -> Dict[str, Any]:
		"""Get statistics about the cognitive ERP knowledge graph."""
		return self.atomspace.get_statistics()


# Singleton instance
_erp_integration = None


def get_erp_integration() -> ERPCognitiveIntegration:
	"""Get or create the global ERP integration instance."""
	global _erp_integration
	if _erp_integration is None:
		_erp_integration = ERPCognitiveIntegration()
	return _erp_integration
