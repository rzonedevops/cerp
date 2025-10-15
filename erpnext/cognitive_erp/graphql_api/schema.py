"""
HyperGraphQL Schema

Defines the GraphQL schema for querying the hypergraph knowledge base.
"""


def get_graphql_schema() -> str:
	"""
	Return the GraphQL schema for the cognitive ERP system.
	
	This schema defines queries for nodes, links, and knowledge graph traversal.
	"""
	return """
		type Atom {
			id: ID!
			atomType: String!
			name: String!
			truthValue: Float!
			attentionValue: Float!
			metadata: JSON
		}
		
		type Node {
			id: ID!
			atomType: String!
			name: String!
			truthValue: Float!
			attentionValue: Float!
			value: JSON
			metadata: JSON
			incomingLinks: [Link]
		}
		
		type Link {
			id: ID!
			atomType: String!
			name: String!
			truthValue: Float!
			attentionValue: Float!
			outgoing: [Atom]
			metadata: JSON
		}
		
		type AtomSpaceStats {
			totalAtoms: Int!
			nodeCount: Int!
			linkCount: Int!
			nodeTypes: [String]
			linkTypes: [String]
		}
		
		type KnowledgeGraph {
			nodes: [Node]
			links: [Link]
			stats: AtomSpaceStats
		}
		
		input NodeFilter {
			nodeType: String
			namePattern: String
			minTruth: Float
		}
		
		input LinkFilter {
			linkType: String
		}
		
		type Query {
			# Get atom by ID
			atom(id: ID!): Atom
			
			# Query nodes
			nodes(filter: NodeFilter, limit: Int): [Node]
			
			# Query links
			links(filter: LinkFilter, limit: Int): [Link]
			
			# Get nodes by type
			nodesByType(nodeType: String!): [Node]
			
			# Get links by type
			linksByType(linkType: String!): [Link]
			
			# Get related atoms (subgraph)
			relatedAtoms(atomId: ID!, maxDepth: Int): KnowledgeGraph
			
			# Get atomspace statistics
			atomSpaceStats: AtomSpaceStats
			
			# Cognitive query - find patterns in the knowledge graph
			cognitiveQuery(pattern: String!): [Node]
		}
		
		type Mutation {
			# Add a node to the atomspace
			addNode(
				nodeType: String!
				name: String!
				value: JSON
				truthValue: Float
				attentionValue: Float
			): Node
			
			# Add a link to the atomspace
			addLink(
				linkType: String!
				outgoingIds: [ID!]!
				name: String
				truthValue: Float
				attentionValue: Float
			): Link
			
			# Update atom truth value
			updateTruthValue(atomId: ID!, truthValue: Float!): Atom
			
			# Update atom attention value
			updateAttentionValue(atomId: ID!, attentionValue: Float!): Atom
		}
		
		scalar JSON
	"""
