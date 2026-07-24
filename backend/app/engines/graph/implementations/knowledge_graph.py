from app.domain.models.investigation import Investigation
from app.engines.graph.base import GraphEngine
from app.engines.graph.builders import KnowledgeGraphBuilder


class KnowledgeGraphEngine(GraphEngine):
    """Builds an in-memory knowledge graph from an investigation."""

    def __init__(self) -> None:
        self._builder = KnowledgeGraphBuilder()

    def build(self, investigation: Investigation) -> Investigation:
        investigation.analysis["knowledge_graph"] = self._builder.build(
            investigation
        )
        return investigation
