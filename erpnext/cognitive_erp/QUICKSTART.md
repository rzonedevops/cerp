# Cognitive ERP Quick Start Guide

Get started with the OpenCog HyperGraphQL Cognitive ERP module in 5 minutes.

## What is Cognitive ERP?

Cognitive ERP extends ERPNext with OpenCog-inspired knowledge representation and HyperGraphQL querying capabilities. It allows you to:

- Represent ERP data as a semantic knowledge graph
- Query relationships using graph traversal
- Apply cognitive attributes (truth values, attention values)
- Discover hidden patterns in your business data

## Quick Start

### 1. Basic Usage (Python)

```python
from erpnext.cognitive_erp.atomspace import get_atomspace

# Get the atomspace
atomspace = get_atomspace()

# Create a customer node
customer = atomspace.add_node(
    "Customer",
    "Acme Corporation",
    value={"email": "contact@acme.com", "industry": "Manufacturing"}
)

# Create a product node
product = atomspace.add_node(
    "Product",
    "Widget Pro",
    value={"price": 99.99, "sku": "WGT-001"}
)

# Create a relationship
purchase_link = atomspace.add_link(
    "Purchases",
    [customer, product],
    truth_value=1.0,  # 100% confident
    attention_value=0.8  # High importance
)

# Query customers
all_customers = atomspace.get_nodes_by_type("Customer")
print(f"Found {len(all_customers)} customers")

# Pattern search
acme_entities = atomspace.query_nodes(name_pattern="Acme")
print(f"Found {len(acme_entities)} entities matching 'Acme'")
```

### 2. Using the ERP Integration

```python
from erpnext.cognitive_erp.atomspace.erp_integration import get_erp_integration

integration = get_erp_integration()

# Add customer with ERP context
customer_id = integration.create_entity_node(
    entity_type="Customer",
    entity_id="CUST-00001",
    entity_data={
        "name": "Acme Corp",
        "email": "contact@acme.com",
        "credit_limit": 100000
    }
)

# Add invoice
invoice_id = integration.create_entity_node(
    entity_type="Invoice",
    entity_id="INV-00001",
    entity_data={
        "total": 5000.00,
        "date": "2025-10-15",
        "status": "Paid"
    }
)

# Link customer to invoice
relationship_id = integration.create_relationship_link(
    relationship_type="HasInvoice",
    source_id=customer_id,
    target_id=invoice_id,
    relationship_data={"created_on": "2025-10-15"}
)

# Get all invoices for this customer
graph = integration.get_connected_entities(customer_id, max_depth=1)
print(f"Customer has {len(graph['links'])} relationships")
```

### 3. REST API Usage (JavaScript)

```javascript
// Add a customer to the knowledge graph
frappe.call({
    method: 'erpnext.cognitive_erp.api.add_entity_node',
    args: {
        entity_type: 'Customer',
        entity_id: 'CUST-00001',
        entity_data: {
            name: 'Acme Corp',
            email: 'contact@acme.com'
        }
    },
    callback: function(r) {
        if (r.message) {
            console.log('Node created:', r.message);
            let node_id = r.message.id;
            
            // Now add a product
            addProduct(node_id);
        }
    }
});

function addProduct(customer_id) {
    frappe.call({
        method: 'erpnext.cognitive_erp.api.add_entity_node',
        args: {
            entity_type: 'Product',
            entity_id: 'PROD-00001',
            entity_data: {
                name: 'Widget',
                price: 99.99
            }
        },
        callback: function(r) {
            if (r.message) {
                let product_id = r.message.id;
                
                // Create relationship
                createRelationship(customer_id, product_id);
            }
        }
    });
}

function createRelationship(customer_id, product_id) {
    frappe.call({
        method: 'erpnext.cognitive_erp.api.add_relationship',
        args: {
            relationship_type: 'Purchases',
            source_id: customer_id,
            target_id: product_id,
            metadata: {
                date: frappe.datetime.get_today(),
                quantity: 10
            }
        },
        callback: function(r) {
            console.log('Relationship created:', r.message);
        }
    });
}

// Query entities
frappe.call({
    method: 'erpnext.cognitive_erp.api.query_entities',
    args: {
        entity_type: 'Customer',
        pattern: 'Acme'
    },
    callback: function(r) {
        console.log('Found entities:', r.message);
    }
});

// Get knowledge graph around an entity
frappe.call({
    method: 'erpnext.cognitive_erp.api.get_connected_entities',
    args: {
        entity_id: customer_id,
        max_depth: 2
    },
    callback: function(r) {
        let graph = r.message;
        console.log('Nodes:', graph.nodes.length);
        console.log('Links:', graph.links.length);
    }
});
```

### 4. Running the Demo

```python
from erpnext.cognitive_erp.demo import run_full_demo

# Run the full demonstration
run_full_demo()
```

This will:
1. Create sample nodes and links
2. Demonstrate querying capabilities
3. Show graph traversal
4. Display statistics

## Common Use Cases

### 1. Customer Relationship Analysis

```python
# Find all customers who purchased a specific product
product_id = "..."  # product atom ID
incoming = atomspace.get_incoming_links(product_id)

customers = []
for link in incoming:
    if link.atom_type == "Link:Purchases":
        customer = link.get_outgoing()[0]
        customers.append(customer)
```

### 2. Product Recommendation

```python
# Find products frequently bought together
customer_id = "..."
graph = integration.get_connected_entities(customer_id, max_depth=2)

# Analyze graph to find common patterns
# (This is simplified - real implementation would use ML)
```

### 3. Supply Chain Analysis

```python
# Create supply chain relationships
supplier_id = integration.create_entity_node("Supplier", "SUP-001", {...})
manufacturer_id = integration.create_entity_node("Manufacturer", "MFG-001", {...})
product_id = integration.create_entity_node("Product", "PROD-001", {...})

# Link them
integration.create_relationship_link("Supplies", supplier_id, manufacturer_id)
integration.create_relationship_link("Manufactures", manufacturer_id, product_id)

# Trace the supply chain
supply_chain = integration.get_connected_entities(product_id, max_depth=3)
```

### 4. Cognitive Search

```python
# Search with high attention (important entities)
results = atomspace.query_nodes(min_truth=0.9)

# Pattern-based search
results = integration.query_entities_by_pattern(
    entity_type="Invoice",
    pattern="2025-10"
)
```

## API Endpoints

### GET Endpoints

- `get_schema`: Get GraphQL schema
- `query_entities`: Query entities with filters
- `get_entity_relationships`: Get entity relationships
- `get_connected_entities`: Get knowledge subgraph
- `get_atomspace_statistics`: Get statistics
- `cognitive_search`: Search with pattern matching

### POST Endpoints

- `add_entity_node`: Add new entity
- `add_relationship`: Create relationship
- `reset_knowledge_graph`: Reset atomspace (admin)

## GraphQL Schema (Preview)

```graphql
type Node {
    id: ID!
    atomType: String!
    name: String!
    truthValue: Float!
    attentionValue: Float!
    value: JSON
    incomingLinks: [Link]
}

type Query {
    nodes(filter: NodeFilter): [Node]
    relatedAtoms(atomId: ID!, maxDepth: Int): KnowledgeGraph
    cognitiveQuery(pattern: String!): [Node]
}

type Mutation {
    addNode(nodeType: String!, name: String!, value: JSON): Node
    addLink(linkType: String!, outgoingIds: [ID!]!): Link
}
```

## Next Steps

1. **Read the Documentation**: Check out [README.md](README.md) for detailed API documentation
2. **Explore Implementation**: See [IMPLEMENTATION.md](IMPLEMENTATION.md) for architecture details
3. **Run Tests**: Execute the test suite to understand capabilities
4. **Build Integration**: Integrate with your ERPNext workflows

## Tips

1. **Use Truth Values**: Set lower truth values for uncertain data
2. **Use Attention Values**: Highlight important entities with higher values
3. **Graph Depth**: Start with depth=1 or 2 for performance
4. **Pattern Matching**: Use lowercase for case-insensitive search
5. **Relationships**: Create meaningful relationship types that match your domain

## Support

For questions, issues, or contributions:
- Check the comprehensive README.md
- Review the implementation documentation
- Explore the demo.py examples
- Run the test suite for validation

---

**Ready to make your ERP cognitive!** 🧠🚀
