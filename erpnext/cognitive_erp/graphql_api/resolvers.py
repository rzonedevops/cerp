"""
GraphQL Resolvers

Implements the resolver functions for the HyperGraphQL API.
"""

from typing import Any, Dict, List, Optional
from ..hypergraph import AtomSpace, Node, Link


class CognitiveResolvers:
	"""Resolvers for the cognitive GraphQL API."""

	def __init__(self, atomspace: AtomSpace):
		self.atomspace = atomspace

	def resolve_atom(self, parent: Any, info: Any, id: str) -> Optional[Dict]:
		"""Resolve a single atom by ID."""
		atom = self.atomspace.get_atom(id)
		if atom:
			return atom.to_dict()
		return None

	def resolve_nodes(
		self, parent: Any, info: Any, filter: Optional[Dict] = None, limit: Optional[int] = None
	) -> List[Dict]:
		"""Resolve nodes with optional filtering."""
		if not filter:
			filter = {}

		node_type = filter.get("nodeType")
		name_pattern = filter.get("namePattern")
		min_truth = filter.get("minTruth", 0.0)

		nodes = self.atomspace.query_nodes(node_type=node_type, name_pattern=name_pattern, min_truth=min_truth)

		if limit:
			nodes = nodes[:limit]

		return [node.to_dict() for node in nodes]

	def resolve_links(
		self, parent: Any, info: Any, filter: Optional[Dict] = None, limit: Optional[int] = None
	) -> List[Dict]:
		"""Resolve links with optional filtering."""
		if not filter:
			filter = {}

		link_type = filter.get("linkType")

		if link_type:
			links = self.atomspace.get_links_by_type(link_type)
		else:
			links = [atom for atom in self.atomspace.atoms.values() if isinstance(atom, Link)]

		if limit:
			links = links[:limit]

		return [link.to_dict() for link in links]

	def resolve_nodes_by_type(self, parent: Any, info: Any, nodeType: str) -> List[Dict]:
		"""Get all nodes of a specific type."""
		nodes = self.atomspace.get_nodes_by_type(nodeType)
		return [node.to_dict() for node in nodes]

	def resolve_links_by_type(self, parent: Any, info: Any, linkType: str) -> List[Dict]:
		"""Get all links of a specific type."""
		links = self.atomspace.get_links_by_type(linkType)
		return [link.to_dict() for link in links]

	def resolve_related_atoms(
		self, parent: Any, info: Any, atomId: str, maxDepth: Optional[int] = 1
	) -> Dict:
		"""Get related atoms (subgraph) from a starting atom."""
		related_ids = self.atomspace.get_related_atoms(atomId, max_depth=maxDepth or 1)

		nodes = []
		links = []

		for atom_id in related_ids:
			atom = self.atomspace.get_atom(atom_id)
			if atom:
				if isinstance(atom, Node):
					nodes.append(atom.to_dict())
				elif isinstance(atom, Link):
					links.append(atom.to_dict())

		return {"nodes": nodes, "links": links, "stats": self.atomspace.get_statistics()}

	def resolve_atomspace_stats(self, parent: Any, info: Any) -> Dict:
		"""Get atomspace statistics."""
		stats = self.atomspace.get_statistics()
		return {
			"totalAtoms": stats["total_atoms"],
			"nodeCount": stats["node_count"],
			"linkCount": stats["link_count"],
			"nodeTypes": stats["node_types"],
			"linkTypes": stats["link_types"],
		}

	def resolve_cognitive_query(self, parent: Any, info: Any, pattern: str) -> List[Dict]:
		"""
		Execute a cognitive query pattern.
		
		This is a simplified pattern matching system. In a full implementation,
		this would support complex pattern matching and reasoning.
		"""
		# Simple pattern matching: search for nodes containing the pattern
		nodes = self.atomspace.query_nodes(name_pattern=pattern)
		return [node.to_dict() for node in nodes]

	def resolve_add_node(
		self,
		parent: Any,
		info: Any,
		nodeType: str,
		name: str,
		value: Optional[Any] = None,
		truthValue: float = 1.0,
		attentionValue: float = 0.0,
	) -> Dict:
		"""Add a new node to the atomspace."""
		node = self.atomspace.add_node(
			node_type=nodeType, name=name, value=value, truth_value=truthValue, attention_value=attentionValue
		)
		return node.to_dict()

	def resolve_add_link(
		self,
		parent: Any,
		info: Any,
		linkType: str,
		outgoingIds: List[str],
		name: Optional[str] = None,
		truthValue: float = 1.0,
		attentionValue: float = 0.0,
	) -> Dict:
		"""Add a new link to the atomspace."""
		# Get the outgoing atoms
		outgoing = []
		for atom_id in outgoingIds:
			atom = self.atomspace.get_atom(atom_id)
			if atom:
				outgoing.append(atom)

		if not outgoing:
			raise ValueError("No valid atoms found for the link")

		link = self.atomspace.add_link(
			link_type=linkType, outgoing=outgoing, name=name, truth_value=truthValue, attention_value=attentionValue
		)
		return link.to_dict()

	def resolve_update_truth_value(self, parent: Any, info: Any, atomId: str, truthValue: float) -> Optional[Dict]:
		"""Update an atom's truth value."""
		atom = self.atomspace.get_atom(atomId)
		if atom:
			atom.truth_value = truthValue
			return atom.to_dict()
		return None

	def resolve_update_attention_value(
		self, parent: Any, info: Any, atomId: str, attentionValue: float
	) -> Optional[Dict]:
		"""Update an atom's attention value."""
		atom = self.atomspace.get_atom(atomId)
		if atom:
			atom.attention_value = attentionValue
			return atom.to_dict()
		return None


def get_resolvers(atomspace: AtomSpace) -> Dict[str, Any]:
	"""
	Get the resolver functions for the GraphQL schema.
	
	Args:
		atomspace: The AtomSpace instance to query
		
	Returns:
		Dictionary mapping resolver names to functions
	"""
	resolver = CognitiveResolvers(atomspace)

	return {
		"Query": {
			"atom": resolver.resolve_atom,
			"nodes": resolver.resolve_nodes,
			"links": resolver.resolve_links,
			"nodesByType": resolver.resolve_nodes_by_type,
			"linksByType": resolver.resolve_links_by_type,
			"relatedAtoms": resolver.resolve_related_atoms,
			"atomSpaceStats": resolver.resolve_atomspace_stats,
			"cognitiveQuery": resolver.resolve_cognitive_query,
		},
		"Mutation": {
			"addNode": resolver.resolve_add_node,
			"addLink": resolver.resolve_add_link,
			"updateTruthValue": resolver.resolve_update_truth_value,
			"updateAttentionValue": resolver.resolve_update_attention_value,
		},
	}
