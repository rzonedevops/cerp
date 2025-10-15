# OpenCog HyperGraphQL CERP Implementation

## Overview

This document describes the implementation of OpenCog-inspired HyperGraphQL capabilities for Cognitive Enterprise Resource Planning (CERP) in ERPNext.

## What Was Implemented

### 1. HyperGraph Knowledge Representation

**File**: `hypergraph/atom.py`

Implemented three core classes inspired by OpenCog's Atomspace:

- **Atom**: Base class for all entities in the knowledge graph
  - Unique ID (UUID)
  - Truth value (confidence: 0.0 to 1.0)
  - Attention value (importance/relevance)
  - Metadata dictionary for custom attributes

- **Node**: Represents entities (customers, products, invoices, etc.)
  - Typed nodes (e.g., "Customer", "Product")
  - Can hold arbitrary data as value
  - Inherits cognitive attributes from Atom

- **Link**: Represents relationships (hyperedges)
  - Connects multiple atoms (true hypergraph support)
  - Typed links (e.g., "Purchases", "Contains")
  - Can represent N-ary relationships

### 2. AtomSpace - Central Knowledge Repository

**File**: `hypergraph/atomspace.py`

The AtomSpace provides:

- **Storage**: Central repository for all atoms
- **Indexing**: Efficient indexing by type for fast queries
- **Relationship Tracking**: Incoming and outgoing link tracking
- **Query Capabilities**:
  - Query by type
  - Pattern matching (name-based search)
  - Truth value filtering
  - Graph traversal with configurable depth
- **Statistics**: Real-time statistics about the knowledge graph

Key Methods:
```python
add_node(node_type, name, value)
add_link(link_type, outgoing_atoms)
get_nodes_by_type(node_type)
query_nodes(node_type, name_pattern, min_truth)
get_incoming_links(atom_id)
get_related_atoms(atom_id, max_depth)
get_statistics()
```

### 3. HyperGraphQL Schema

**File**: `graphql_api/schema.py`

Comprehensive GraphQL schema supporting:

**Types**:
- Atom, Node, Link
- AtomSpaceStats
- KnowledgeGraph (nodes + links)

**Queries**:
- `atom(id)`: Get single atom
- `nodes(filter)`: Query nodes with filters
- `links(filter)`: Query links with filters
- `nodesByType(nodeType)`: Get all nodes of a type
- `linksByType(linkType)`: Get all links of a type
- `relatedAtoms(atomId, maxDepth)`: Get subgraph
- `atomSpaceStats`: Get statistics
- `cognitiveQuery(pattern)`: Pattern-based search

**Mutations**:
- `addNode()`: Create new node
- `addLink()`: Create new link
- `updateTruthValue()`: Update atom confidence
- `updateAttentionValue()`: Update atom importance

### 4. GraphQL Resolvers

**File**: `graphql_api/resolvers.py`

Complete resolver implementation for all queries and mutations:
- CognitiveResolvers class with 12+ resolver methods
- Full CRUD operations on the knowledge graph
- Pattern matching and graph traversal
- Support for filtering and pagination

### 5. ERP Integration Layer

**File**: `atomspace/erp_integration.py`

ERPCognitiveIntegration class providing:

```python
create_entity_node(entity_type, entity_id, entity_data)
create_relationship_link(relationship_type, source_id, target_id)
get_entity_relationships(entity_id)
get_connected_entities(entity_id, max_depth)
query_entities_by_pattern(entity_type, pattern)
```

This bridges ERP entities with the cognitive layer.

### 6. REST API Endpoints

**File**: `api.py`

Frappe whitelisted endpoints:

- `get_schema()`: Get GraphQL schema
- `add_entity_node()`: Add ERP entity to knowledge graph
- `add_relationship()`: Create entity relationship
- `query_entities()`: Search entities
- `get_entity_relationships()`: Get entity relationships
- `get_connected_entities()`: Get knowledge subgraph
- `get_atomspace_statistics()`: Get stats
- `reset_knowledge_graph()`: Reset atomspace (admin only)
- `cognitive_search()`: Advanced search

All endpoints require authentication and use Frappe's permission system.

### 7. Documentation

**File**: `README.md`

Comprehensive documentation including:
- Architecture overview
- Key concepts explanation
- API reference with examples
- Python and JavaScript usage examples
- Benefits and use cases
- Future enhancement roadmap

### 8. Tests

**File**: `test_cognitive_erp.py`

Unit tests covering:
- Atom, Node, Link creation
- AtomSpace operations
- Query functionality
- Graph traversal
- ERP integration
- Statistics

### 9. Demo Script

**File**: `demo.py`

Demonstrates:
- Basic atomspace operations
- ERP entity integration
- Cognitive queries
- Graph traversal
- Pattern matching

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ERPNext Frontend                     │
│           (JavaScript/Vue Components)                   │
└─────────────────┬───────────────────────────────────────┘
                  │ REST API Calls
                  ▼
┌─────────────────────────────────────────────────────────┐
│              Cognitive ERP API Layer                    │
│                 (api.py)                                │
│  - add_entity_node()                                    │
│  - add_relationship()                                   │
│  - query_entities()                                     │
│  - cognitive_search()                                   │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│          ERP Integration Layer                          │
│        (atomspace/erp_integration.py)                   │
│  - Converts ERP entities to nodes                       │
│  - Creates relationship links                           │
│  - Provides high-level query interface                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              AtomSpace (Core)                           │
│           (hypergraph/atomspace.py)                     │
│  - Central knowledge repository                         │
│  - Indexing and querying                                │
│  - Graph traversal                                      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│         HyperGraph Data Structures                      │
│            (hypergraph/atom.py)                         │
│  - Atom (base class)                                    │
│  - Node (entities)                                      │
│  - Link (relationships)                                 │
└─────────────────────────────────────────────────────────┘

                  Parallel Path:
                  
┌─────────────────────────────────────────────────────────┐
│            HyperGraphQL Interface                       │
│          (graphql_api/schema.py)                        │
│          (graphql_api/resolvers.py)                     │
│  - GraphQL schema definition                            │
│  - Query and mutation resolvers                         │
│  - Advanced querying capabilities                       │
└─────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. OpenCog Inspiration
- **Truth Values**: Represent confidence in facts (probabilistic reasoning)
- **Attention Values**: Represent importance/relevance (focus of attention)
- **Hypergraph Structure**: Links can connect multiple atoms (not just pairs)

### 2. Minimal Dependencies
- Pure Python implementation
- No external AI/ML libraries required
- Can be extended with actual OpenCog or GraphQL libraries later

### 3. Integration with Frappe
- Uses Frappe's @whitelist decorator for API endpoints
- Follows Frappe's permission model
- Compatible with ERPNext's architecture

### 4. Extensibility
- Modular architecture allows easy extension
- Open for adding reasoning engines
- Ready for ML/AI integration
- Can add persistent storage backend

## Usage Example

```python
from erpnext.cognitive_erp.atomspace import get_atomspace
from erpnext.cognitive_erp.atomspace.erp_integration import get_erp_integration

# Get integration instance
integration = get_erp_integration()

# Add customer
customer_id = integration.create_entity_node(
    entity_type="Customer",
    entity_id="CUST-001",
    entity_data={"name": "Acme Corp", "email": "contact@acme.com"}
)

# Add product
product_id = integration.create_entity_node(
    entity_type="Product",
    entity_id="PROD-001",
    entity_data={"name": "Widget", "price": 99.99}
)

# Create relationship
integration.create_relationship_link(
    relationship_type="Purchases",
    source_id=customer_id,
    target_id=product_id,
    relationship_data={"date": "2025-10-15", "quantity": 5}
)

# Query
customers = integration.query_entities_by_pattern(
    entity_type="Customer",
    pattern="acme"
)

# Get knowledge graph around customer
graph = integration.get_connected_entities(customer_id, max_depth=2)
print(f"Nodes: {len(graph['nodes'])}, Links: {len(graph['links'])}")
```

## Benefits

1. **Semantic Knowledge Representation**: ERP data as semantic knowledge graph
2. **Advanced Querying**: Graph traversal beyond traditional SQL
3. **AI-Ready Foundation**: Base for cognitive reasoning capabilities
4. **Relationship Discovery**: Navigate complex entity relationships
5. **Probabilistic Knowledge**: Truth values support uncertain information
6. **Attention Mechanism**: Focus on important entities
7. **Flexible Schema**: Dynamic, evolves with data

## Future Enhancements

1. **Pattern Language**: Implement full pattern matching engine (like OpenCog's PatternMatcher)
2. **Reasoning**: Add inference and deduction capabilities
3. **Persistence**: Add database backend for persistent storage
4. **Machine Learning**: Integrate with ML frameworks for learning
5. **Distributed**: Scale to distributed atomspace
6. **Real GraphQL**: Use actual GraphQL libraries (graphene, ariadne)
7. **Visualization**: Add graph visualization UI
8. **SPARQL**: Add SPARQL query support
9. **Neural-Symbolic**: Integrate neural networks with symbolic reasoning
10. **Time-Awareness**: Add temporal reasoning capabilities

## Testing

The implementation has been validated with:
- Unit tests for all core classes
- Integration tests for ERP functionality
- Manual testing of API endpoints
- Validation script demonstrating all features

All tests pass successfully ✓

## Conclusion

This implementation provides a solid foundation for cognitive ERP capabilities in ERPNext. It brings OpenCog-inspired knowledge representation and HyperGraphQL querying to the ERP domain, enabling advanced AI-driven business intelligence and reasoning capabilities.

The modular architecture allows for incremental enhancement while maintaining backward compatibility with existing ERPNext functionality.
