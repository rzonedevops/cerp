# Cognitive ERP Module

OpenCog-inspired HyperGraphQL implementation for Cognitive Enterprise Resource Planning (CERP).

## Overview

This module provides cognitive capabilities for ERPNext by implementing:

1. **HyperGraph Knowledge Representation**: Using atoms (nodes and links) to represent ERP entities and their relationships
2. **AtomSpace**: A central knowledge store inspired by OpenCog's AtomSpace architecture
3. **HyperGraphQL API**: GraphQL-based querying interface for the knowledge graph
4. **ERP Integration**: Seamless integration with existing ERPNext entities

## Architecture

```
cognitive_erp/
├── hypergraph/          # Core hypergraph data structures
│   ├── atom.py         # Atom, Node, and Link classes
│   └── atomspace.py    # AtomSpace knowledge repository
├── graphql_api/        # HyperGraphQL implementation
│   ├── schema.py       # GraphQL schema definition
│   └── resolvers.py    # Query and mutation resolvers
├── atomspace/          # AtomSpace management
│   ├── __init__.py     # Global atomspace instance
│   └── erp_integration.py  # ERP entity integration
└── api.py              # REST API endpoints
```

## Key Concepts

### Atoms

Atoms are the basic building blocks of the knowledge graph:

- **Nodes**: Represent entities (Customer, Product, Invoice, etc.)
- **Links**: Represent relationships between entities

Each atom has:
- `truth_value`: Confidence level (0.0 to 1.0)
- `attention_value`: Importance/relevance score
- `metadata`: Additional custom attributes

### AtomSpace

The AtomSpace is the central repository that:
- Stores all atoms
- Indexes atoms by type for efficient querying
- Tracks relationships between atoms
- Provides pattern matching and traversal capabilities

### HyperGraphQL

A GraphQL interface for querying the knowledge graph with support for:
- Node and link queries
- Graph traversal
- Pattern matching
- Statistics and analytics

## API Endpoints

### REST API

All endpoints require authentication.

#### Get Schema
```
GET /api/method/erpnext.cognitive_erp.api.get_schema
```

#### Add Entity Node
```
POST /api/method/erpnext.cognitive_erp.api.add_entity_node
{
  "entity_type": "Customer",
  "entity_id": "CUST-001",
  "entity_data": {"name": "John Doe", "email": "john@example.com"}
}
```

#### Add Relationship
```
POST /api/method/erpnext.cognitive_erp.api.add_relationship
{
  "relationship_type": "CustomerBuys",
  "source_id": "atom-id-1",
  "target_id": "atom-id-2",
  "metadata": {"date": "2025-10-15"}
}
```

#### Query Entities
```
GET /api/method/erpnext.cognitive_erp.api.query_entities
?entity_type=Customer&pattern=john&min_truth=0.5
```

#### Get Connected Entities
```
GET /api/method/erpnext.cognitive_erp.api.get_connected_entities
?entity_id=atom-id&max_depth=2
```

#### Get Statistics
```
GET /api/method/erpnext.cognitive_erp.api.get_atomspace_statistics
```

#### Cognitive Search
```
GET /api/method/erpnext.cognitive_erp.api.cognitive_search
?query=invoice&limit=20
```

## Usage Examples

### Python API

```python
from erpnext.cognitive_erp.atomspace import get_atomspace
from erpnext.cognitive_erp.atomspace.erp_integration import get_erp_integration

# Get the integration instance
integration = get_erp_integration()

# Add a customer entity
customer_id = integration.create_entity_node(
    entity_type="Customer",
    entity_id="CUST-001",
    entity_data={"name": "John Doe", "email": "john@example.com"}
)

# Add a product entity
product_id = integration.create_entity_node(
    entity_type="Product",
    entity_id="PROD-001",
    entity_data={"name": "Widget", "price": 99.99}
)

# Create a relationship
relationship_id = integration.create_relationship_link(
    relationship_type="CustomerBuys",
    source_id=customer_id,
    target_id=product_id,
    relationship_data={"date": "2025-10-15", "quantity": 5}
)

# Query entities
customers = integration.query_entities_by_pattern(
    entity_type="Customer",
    pattern="john"
)

# Get connected entities
graph = integration.get_connected_entities(customer_id, max_depth=2)
print(f"Connected nodes: {len(graph['nodes'])}")
print(f"Connected links: {len(graph['links'])}")
```

### JavaScript API

```javascript
// Add entity via REST API
frappe.call({
    method: 'erpnext.cognitive_erp.api.add_entity_node',
    args: {
        entity_type: 'Customer',
        entity_id: 'CUST-001',
        entity_data: {
            name: 'John Doe',
            email: 'john@example.com'
        }
    },
    callback: function(r) {
        console.log('Node created:', r.message);
    }
});

// Query entities
frappe.call({
    method: 'erpnext.cognitive_erp.api.query_entities',
    args: {
        entity_type: 'Customer',
        pattern: 'john'
    },
    callback: function(r) {
        console.log('Found entities:', r.message);
    }
});
```

## Benefits

1. **Semantic Knowledge Representation**: ERP data is represented as a semantic knowledge graph
2. **Advanced Querying**: Complex queries and graph traversal beyond traditional SQL
3. **AI-Ready**: Foundation for implementing AI reasoning and cognitive capabilities
4. **Relationship Discovery**: Automatically discover and navigate entity relationships
5. **Flexible Schema**: Dynamic schema that evolves with your data

## Future Enhancements

- Pattern matching engine for complex queries
- Reasoning capabilities (inference, deduction)
- Machine learning integration
- Real-time graph analytics
- Distributed atomspace for scalability
- Integration with actual GraphQL libraries (graphene, ariadne)
- Persistent storage backend

## References

- OpenCog Framework: https://opencog.org/
- HyperGraphQL: https://www.hypergraphql.org/
- Knowledge Graphs: https://en.wikipedia.org/wiki/Knowledge_graph
