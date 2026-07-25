from __future__ import annotations

from app.application.graph.edge import GraphEdge
from app.application.graph.graph import KnowledgeGraph
from app.application.graph.node import GraphNode
from app.domain.models.investigation import Investigation


class GraphBuilder:
    """
    Builds a KnowledgeGraph from an Investigation.
    """

    def build(
        self,
        investigation: Investigation,
    ) -> KnowledgeGraph:

        graph = KnowledgeGraph()

        #
        # Add every resource as a node.
        #
        for resource in investigation.resources:
            graph.add_node(
                GraphNode(resource)
            )

        #
        # Add every relationship as a directed edge.
        #
        for relationship in investigation.relationships:

            graph.add_edge(
                source_id=relationship.source_id,
                edge=GraphEdge(relationship),
            )

        return graph
