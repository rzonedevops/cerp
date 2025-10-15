"""
Demo Script for Cognitive ERP

Demonstrates the capabilities of the OpenCog-inspired HyperGraphQL implementation.
"""

from .atomspace import get_atomspace, reset_atomspace
from .atomspace.erp_integration import get_erp_integration


def demo_basic_operations():
	"""Demonstrate basic atomspace operations."""
	print("=" * 60)
	print("COGNITIVE ERP DEMO - Basic Operations")
	print("=" * 60)

	# Reset atomspace for clean demo
	reset_atomspace()
	atomspace = get_atomspace()

	# Create some nodes
	print("\n1. Creating nodes...")
	customer1 = atomspace.add_node("Customer", "John Doe", value={"email": "john@example.com", "city": "New York"})
	customer2 = atomspace.add_node("Customer", "Jane Smith", value={"email": "jane@example.com", "city": "Boston"})
	product1 = atomspace.add_node("Product", "Widget Pro", value={"price": 99.99, "category": "Electronics"})
	product2 = atomspace.add_node("Product", "Gadget X", value={"price": 149.99, "category": "Electronics"})
	print(f"   Created {atomspace.get_statistics()['node_count']} nodes")

	# Create relationships
	print("\n2. Creating relationships...")
	link1 = atomspace.add_link(
		"Buys", [customer1, product1], name="Purchase-001", truth_value=1.0, attention_value=0.8
	)
	link2 = atomspace.add_link(
		"Buys", [customer1, product2], name="Purchase-002", truth_value=1.0, attention_value=0.7
	)
	link3 = atomspace.add_link(
		"Buys", [customer2, product1], name="Purchase-003", truth_value=1.0, attention_value=0.9
	)
	print(f"   Created {atomspace.get_statistics()['link_count']} links")

	# Query nodes
	print("\n3. Querying nodes...")
	customers = atomspace.get_nodes_by_type("Customer")
	print(f"   Found {len(customers)} customers:")
	for customer in customers:
		print(f"      - {customer.name}: {customer.value}")

	# Query with pattern
	print("\n4. Pattern-based search...")
	john_nodes = atomspace.query_nodes(name_pattern="John")
	print(f"   Found {len(john_nodes)} nodes matching 'John':")
	for node in john_nodes:
		print(f"      - {node.name}")

	# Get incoming links
	print("\n5. Getting customer purchases...")
	purchases = atomspace.get_incoming_links(customer1.id)
	print(f"   Customer '{customer1.name}' has {len(purchases)} purchases")

	# Get related atoms
	print("\n6. Finding related entities...")
	related = atomspace.get_related_atoms(customer1.id, max_depth=2)
	print(f"   Found {len(related)} related atoms (depth=2)")

	# Statistics
	print("\n7. Atomspace Statistics:")
	stats = atomspace.get_statistics()
	print(f"   Total atoms: {stats['total_atoms']}")
	print(f"   Nodes: {stats['node_count']}")
	print(f"   Links: {stats['link_count']}")
	print(f"   Node types: {', '.join([t.replace('Node:', '') for t in stats['node_types']])}")
	print(f"   Link types: {', '.join([t.replace('Link:', '') for t in stats['link_types']])}")


def demo_erp_integration():
	"""Demonstrate ERP integration capabilities."""
	print("\n" + "=" * 60)
	print("COGNITIVE ERP DEMO - ERP Integration")
	print("=" * 60)

	# Reset atomspace
	reset_atomspace()
	integration = get_erp_integration()

	# Create ERP entities
	print("\n1. Creating ERP entities...")
	customer_id = integration.create_entity_node(
		entity_type="Customer",
		entity_id="CUST-001",
		entity_data={"name": "Acme Corp", "email": "contact@acme.com", "industry": "Manufacturing"},
	)
	print(f"   Created customer: CUST-001")

	invoice_id = integration.create_entity_node(
		entity_type="Invoice",
		entity_id="INV-001",
		entity_data={"total": 5000.00, "date": "2025-10-15", "status": "Paid"},
	)
	print(f"   Created invoice: INV-001")

	item1_id = integration.create_entity_node(
		entity_type="Item", entity_id="ITEM-001", entity_data={"name": "Widget", "quantity": 10, "price": 100.00}
	)
	print(f"   Created item: ITEM-001")

	item2_id = integration.create_entity_node(
		entity_type="Item", entity_id="ITEM-002", entity_data={"name": "Gadget", "quantity": 20, "price": 200.00}
	)
	print(f"   Created item: ITEM-002")

	# Create relationships
	print("\n2. Creating relationships...")
	integration.create_relationship_link(
		relationship_type="HasInvoice",
		source_id=customer_id,
		target_id=invoice_id,
		relationship_data={"created_date": "2025-10-15"},
	)
	print(f"   Customer -> Invoice")

	integration.create_relationship_link(
		relationship_type="Contains",
		source_id=invoice_id,
		target_id=item1_id,
		relationship_data={"line_number": 1},
	)
	print(f"   Invoice -> Item 1")

	integration.create_relationship_link(
		relationship_type="Contains",
		source_id=invoice_id,
		target_id=item2_id,
		relationship_data={"line_number": 2},
	)
	print(f"   Invoice -> Item 2")

	# Query entities
	print("\n3. Querying entities...")
	customers = integration.query_entities_by_pattern(entity_type="Customer")
	print(f"   Found {len(customers)} customers")

	invoices = integration.query_entities_by_pattern(entity_type="Invoice", pattern="INV")
	print(f"   Found {len(invoices)} invoices matching 'INV'")

	# Get relationships
	print("\n4. Getting entity relationships...")
	customer_rels = integration.get_entity_relationships(customer_id)
	print(f"   Customer has {len(customer_rels)} relationships")

	# Get connected entities
	print("\n5. Getting connected entities (knowledge graph)...")
	graph = integration.get_connected_entities(customer_id, max_depth=2)
	print(f"   Connected nodes: {len(graph['nodes'])}")
	print(f"   Connected links: {len(graph['links'])}")
	print(f"   Graph structure:")
	for node in graph["nodes"]:
		entity_type = node["atom_type"].replace("Node:", "")
		print(f"      - {entity_type}: {node['name']}")

	# Statistics
	print("\n6. Knowledge Graph Statistics:")
	stats = integration.get_statistics()
	print(f"   Total entities: {stats['total_atoms']}")
	print(f"   Entity types: {', '.join([t.replace('Node:', '') for t in stats['node_types']])}")


def demo_cognitive_queries():
	"""Demonstrate cognitive query capabilities."""
	print("\n" + "=" * 60)
	print("COGNITIVE ERP DEMO - Cognitive Queries")
	print("=" * 60)

	atomspace = get_atomspace()

	# Pattern matching
	print("\n1. Pattern-based queries...")
	all_items = atomspace.query_nodes(node_type="Item")
	print(f"   Total items: {len(all_items)}")

	# Truth value filtering
	print("\n2. Truth value filtering...")
	high_confidence = atomspace.query_nodes(min_truth=0.9)
	print(f"   High confidence entities (truth >= 0.9): {len(high_confidence)}")

	# Graph traversal
	print("\n3. Graph traversal example...")
	integration = get_erp_integration()
	customers = integration.query_entities_by_pattern(entity_type="Customer")
	if customers:
		customer = customers[0]
		print(f"   Starting from: {customer['name']}")

		# Traverse 1 level
		graph_1 = integration.get_connected_entities(customer["id"], max_depth=1)
		print(f"   Level 1: {len(graph_1['nodes'])} nodes, {len(graph_1['links'])} links")

		# Traverse 2 levels
		graph_2 = integration.get_connected_entities(customer["id"], max_depth=2)
		print(f"   Level 2: {len(graph_2['nodes'])} nodes, {len(graph_2['links'])} links")


def run_full_demo():
	"""Run the complete demo."""
	demo_basic_operations()
	demo_erp_integration()
	demo_cognitive_queries()

	print("\n" + "=" * 60)
	print("DEMO COMPLETED")
	print("=" * 60)
	print("\nCognitive ERP module successfully demonstrated!")
	print("Check the README.md for API documentation and usage examples.")
	print("=" * 60 + "\n")


if __name__ == "__main__":
	run_full_demo()
