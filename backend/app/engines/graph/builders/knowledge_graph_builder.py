from app.domain.models.investigation import Investigation
from app.engines.graph.models import GraphEdge, GraphNode, KnowledgeGraph


class KnowledgeGraphBuilder:
    """Builds a KnowledgeGraph from an Investigation."""

    def build(
        self,
        investigation: Investigation,
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        for resource in investigation.resources:
            graph.add_node(
                GraphNode(
                    id=resource.id,
                    label=resource.name,
                    resource_type=resource.type,
                    metadata=resource.metadata,
                )
            )

        for relationship in investigation.relationships:
            graph.add_edge(
                GraphEdge(
                    source=relationship.source_id,
                    target=relationship.target_id,
                    relationship_type=relationship.relationship_type,
                    metadata=relationship.metadata,
                )
            )

        return graph
