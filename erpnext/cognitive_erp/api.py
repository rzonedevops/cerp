"""
Cognitive ERP API Endpoints

Provides REST API endpoints for accessing the cognitive layer.
"""

import frappe
from frappe import _
from typing import Any, Dict, List, Optional
from .atomspace import get_atomspace, reset_atomspace
from .atomspace.erp_integration import get_erp_integration
from .graphql_api import get_graphql_schema, get_resolvers


@frappe.whitelist(allow_guest=False)
def get_schema():
	"""
	Get the HyperGraphQL schema definition.
	
	Returns:
		GraphQL schema as a string
	"""
	return {"schema": get_graphql_schema()}


@frappe.whitelist(allow_guest=False)
def execute_query(query: str, variables: Optional[Dict] = None):
	"""
	Execute a GraphQL query against the cognitive knowledge graph.
	
	Args:
		query: GraphQL query string
		variables: Optional variables for the query
		
	Returns:
		Query results
	"""
	# In a full implementation, this would use a GraphQL library like graphene or ariadne
	# For now, we'll provide a simple direct API
	frappe.throw(_("GraphQL query execution not yet implemented. Use direct API endpoints."))


@frappe.whitelist(allow_guest=False)
def add_entity_node(entity_type: str, entity_id: str, entity_data: Dict[str, Any]):
	"""
	Add an ERP entity to the cognitive knowledge graph.
	
	Args:
		entity_type: Type of entity (e.g., "Customer", "Invoice")
		entity_id: Unique identifier
		entity_data: Entity attributes as dictionary
		
	Returns:
		Node information
	"""
	integration = get_erp_integration()
	node_id = integration.create_entity_node(entity_type, entity_id, entity_data)
	atomspace = get_atomspace()
	node = atomspace.get_atom(node_id)
	return node.to_dict() if node else None


@frappe.whitelist(allow_guest=False)
def add_relationship(relationship_type: str, source_id: str, target_id: str, metadata: Optional[Dict] = None):
	"""
	Add a relationship between entities in the knowledge graph.
	
	Args:
		relationship_type: Type of relationship
		source_id: Source atom ID
		target_id: Target atom ID
		metadata: Optional relationship metadata
		
	Returns:
		Link information
	"""
	integration = get_erp_integration()
	link_id = integration.create_relationship_link(relationship_type, source_id, target_id, metadata)
	atomspace = get_atomspace()
	link = atomspace.get_atom(link_id)
	return link.to_dict() if link else None


@frappe.whitelist(allow_guest=False)
def query_entities(entity_type: Optional[str] = None, pattern: Optional[str] = None, min_truth: float = 0.0):
	"""
	Query entities in the knowledge graph.
	
	Args:
		entity_type: Optional entity type filter
		pattern: Optional name pattern
		min_truth: Minimum truth value
		
	Returns:
		List of matching entities
	"""
	integration = get_erp_integration()
	return integration.query_entities_by_pattern(entity_type, pattern, float(min_truth))


@frappe.whitelist(allow_guest=False)
def get_entity_relationships(entity_id: str, relationship_type: Optional[str] = None):
	"""
	Get all relationships for an entity.
	
	Args:
		entity_id: Entity atom ID
		relationship_type: Optional relationship type filter
		
	Returns:
		List of relationships
	"""
	integration = get_erp_integration()
	return integration.get_entity_relationships(entity_id, relationship_type)


@frappe.whitelist(allow_guest=False)
def get_connected_entities(entity_id: str, max_depth: int = 2):
	"""
	Get all entities connected to a given entity.
	
	Args:
		entity_id: Starting entity ID
		max_depth: Maximum traversal depth
		
	Returns:
		Dictionary with nodes and links
	"""
	integration = get_erp_integration()
	return integration.get_connected_entities(entity_id, int(max_depth))


@frappe.whitelist(allow_guest=False)
def get_atomspace_statistics():
	"""
	Get statistics about the cognitive knowledge graph.
	
	Returns:
		Statistics dictionary
	"""
	integration = get_erp_integration()
	return integration.get_statistics()


@frappe.whitelist(allow_guest=False)
def reset_knowledge_graph():
	"""
	Reset the entire knowledge graph (admin only).
	
	Requires System Manager role.
	"""
	if not frappe.has_permission("System Manager"):
		frappe.throw(_("Only System Managers can reset the knowledge graph"))

	reset_atomspace()
	return {"status": "success", "message": "Knowledge graph has been reset"}


@frappe.whitelist(allow_guest=False)
def cognitive_search(query: str, entity_types: Optional[List[str]] = None, limit: int = 20):
	"""
	Perform a cognitive search across the knowledge graph.
	
	Args:
		query: Search query string
		entity_types: Optional list of entity types to search
		limit: Maximum number of results
		
	Returns:
		List of matching entities
	"""
	atomspace = get_atomspace()
	results = []

	if entity_types:
		for entity_type in entity_types:
			nodes = atomspace.query_nodes(node_type=entity_type, name_pattern=query)
			results.extend([node.to_dict() for node in nodes[:limit]])
	else:
		nodes = atomspace.query_nodes(name_pattern=query)
		results.extend([node.to_dict() for node in nodes[:limit]])

	return results[:limit]
