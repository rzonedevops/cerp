"""
Tests for Cognitive ERP Module

Basic tests to validate the hypergraph and cognitive capabilities.
"""

import unittest
from .hypergraph import Atom, Node, Link, AtomSpace
from .atomspace import get_atomspace, reset_atomspace
from .atomspace.erp_integration import get_erp_integration


class TestAtom(unittest.TestCase):
	"""Test Atom classes."""

	def test_node_creation(self):
		"""Test creating a node."""
		node = Node("Customer", "John Doe", value={"email": "john@example.com"})
		self.assertEqual(node.atom_type, "Node:Customer")
		self.assertEqual(node.name, "John Doe")
		self.assertEqual(node.value["email"], "john@example.com")
		self.assertEqual(node.truth_value, 1.0)

	def test_link_creation(self):
		"""Test creating a link between nodes."""
		customer = Node("Customer", "John Doe")
		product = Node("Product", "Widget")
		link = Link("Buys", [customer, product])

		self.assertEqual(link.atom_type, "Link:Buys")
		self.assertEqual(len(link.get_outgoing()), 2)
		self.assertIn(customer, link.get_outgoing())
		self.assertIn(product, link.get_outgoing())


class TestAtomSpace(unittest.TestCase):
	"""Test AtomSpace functionality."""

	def setUp(self):
		"""Set up a fresh atomspace for each test."""
		self.atomspace = AtomSpace()

	def test_add_node(self):
		"""Test adding a node to atomspace."""
		node = self.atomspace.add_node("Customer", "John Doe", value={"email": "john@example.com"})
		self.assertIsNotNone(node.id)
		self.assertEqual(self.atomspace.get_atom(node.id), node)

	def test_add_link(self):
		"""Test adding a link to atomspace."""
		customer = self.atomspace.add_node("Customer", "John Doe")
		product = self.atomspace.add_node("Product", "Widget")
		link = self.atomspace.add_link("Buys", [customer, product])

		self.assertIsNotNone(link.id)
		self.assertEqual(len(link.get_outgoing()), 2)

	def test_get_nodes_by_type(self):
		"""Test querying nodes by type."""
		self.atomspace.add_node("Customer", "John Doe")
		self.atomspace.add_node("Customer", "Jane Smith")
		self.atomspace.add_node("Product", "Widget")

		customers = self.atomspace.get_nodes_by_type("Customer")
		self.assertEqual(len(customers), 2)

		products = self.atomspace.get_nodes_by_type("Product")
		self.assertEqual(len(products), 1)

	def test_query_nodes(self):
		"""Test querying nodes with filters."""
		self.atomspace.add_node("Customer", "John Doe")
		self.atomspace.add_node("Customer", "Jane Doe")
		self.atomspace.add_node("Customer", "Bob Smith")

		# Query by pattern
		doe_customers = self.atomspace.query_nodes(name_pattern="Doe")
		self.assertEqual(len(doe_customers), 2)

		# Query by type and pattern
		doe_customers = self.atomspace.query_nodes(node_type="Customer", name_pattern="John")
		self.assertEqual(len(doe_customers), 1)

	def test_incoming_links(self):
		"""Test getting incoming links for a node."""
		customer = self.atomspace.add_node("Customer", "John Doe")
		product1 = self.atomspace.add_node("Product", "Widget")
		product2 = self.atomspace.add_node("Product", "Gadget")

		link1 = self.atomspace.add_link("Buys", [customer, product1])
		link2 = self.atomspace.add_link("Buys", [customer, product2])

		# Get incoming links for customer
		incoming = self.atomspace.get_incoming_links(customer.id)
		self.assertEqual(len(incoming), 2)

	def test_related_atoms(self):
		"""Test getting related atoms."""
		customer = self.atomspace.add_node("Customer", "John Doe")
		product = self.atomspace.add_node("Product", "Widget")
		link = self.atomspace.add_link("Buys", [customer, product])

		# Get atoms related to customer
		related = self.atomspace.get_related_atoms(customer.id, max_depth=1)
		self.assertIn(customer.id, related)
		self.assertIn(link.id, related)
		self.assertIn(product.id, related)

	def test_statistics(self):
		"""Test atomspace statistics."""
		self.atomspace.add_node("Customer", "John Doe")
		self.atomspace.add_node("Product", "Widget")
		customer = self.atomspace.add_node("Customer", "Jane Smith")
		product = self.atomspace.add_node("Product", "Gadget")
		self.atomspace.add_link("Buys", [customer, product])

		stats = self.atomspace.get_statistics()
		self.assertEqual(stats["total_atoms"], 5)
		self.assertEqual(stats["node_count"], 4)
		self.assertEqual(stats["link_count"], 1)


class TestERPIntegration(unittest.TestCase):
	"""Test ERP integration functionality."""

	def setUp(self):
		"""Set up fresh atomspace for each test."""
		reset_atomspace()
		self.integration = get_erp_integration()

	def test_create_entity_node(self):
		"""Test creating an ERP entity node."""
		node_id = self.integration.create_entity_node(
			entity_type="Customer", entity_id="CUST-001", entity_data={"name": "John Doe", "email": "john@example.com"}
		)
		self.assertIsNotNone(node_id)

		atomspace = get_atomspace()
		node = atomspace.get_atom(node_id)
		self.assertIsNotNone(node)
		self.assertEqual(node.value["name"], "John Doe")

	def test_create_relationship_link(self):
		"""Test creating a relationship between entities."""
		customer_id = self.integration.create_entity_node(
			entity_type="Customer", entity_id="CUST-001", entity_data={"name": "John Doe"}
		)
		product_id = self.integration.create_entity_node(
			entity_type="Product", entity_id="PROD-001", entity_data={"name": "Widget"}
		)

		link_id = self.integration.create_relationship_link(
			relationship_type="CustomerBuys",
			source_id=customer_id,
			target_id=product_id,
			relationship_data={"date": "2025-10-15"},
		)
		self.assertIsNotNone(link_id)

		atomspace = get_atomspace()
		link = atomspace.get_atom(link_id)
		self.assertIsNotNone(link)
		self.assertEqual(link.metadata["date"], "2025-10-15")

	def test_query_entities(self):
		"""Test querying entities."""
		self.integration.create_entity_node(
			entity_type="Customer", entity_id="CUST-001", entity_data={"name": "John Doe"}
		)
		self.integration.create_entity_node(
			entity_type="Customer", entity_id="CUST-002", entity_data={"name": "Jane Doe"}
		)

		results = self.integration.query_entities_by_pattern(entity_type="Customer", pattern="Doe")
		self.assertEqual(len(results), 2)

	def test_get_connected_entities(self):
		"""Test getting connected entities."""
		customer_id = self.integration.create_entity_node(
			entity_type="Customer", entity_id="CUST-001", entity_data={"name": "John Doe"}
		)
		product_id = self.integration.create_entity_node(
			entity_type="Product", entity_id="PROD-001", entity_data={"name": "Widget"}
		)

		self.integration.create_relationship_link(
			relationship_type="CustomerBuys", source_id=customer_id, target_id=product_id
		)

		graph = self.integration.get_connected_entities(customer_id, max_depth=1)
		self.assertGreater(len(graph["nodes"]), 0)
		self.assertGreater(len(graph["links"]), 0)


if __name__ == "__main__":
	unittest.main()
