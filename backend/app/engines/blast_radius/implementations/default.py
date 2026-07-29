from app.domain.models.investigation import Investigation
from app.engines.blast_radius.base import BlastRadiusEngine
from app.engines.graph.algorithms import BreadthFirstTraversal
from app.engines.graph.models import KnowledgeGraph


class DefaultBlastRadiusEngine(BlastRadiusEngine):
    """Default blast radius implementation."""

    def __init__(self) -> None:
        self._traversal = BreadthFirstTraversal()

    def analyze(
        self,
        investigation: Investigation,
        compromised_resource: str,
    ) -> Investigation:
        graph: KnowledgeGraph = investigation.analysis["knowledge_graph"]

        investigation.analysis["blast_radius"] = self._traversal.traverse(
            graph,
            compromised_resource,
        )

        return investigation
