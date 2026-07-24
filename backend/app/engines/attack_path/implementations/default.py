from app.domain.models.investigation import Investigation
from app.engines.attack_path.base import AttackPathEngine
from app.engines.graph.algorithms import PathFinder
from app.engines.graph.models import KnowledgeGraph


class DefaultAttackPathEngine(AttackPathEngine):
    """Default attack path implementation."""

    def __init__(self) -> None:
        self._path_finder = PathFinder()

    def analyze(
        self,
        investigation: Investigation,
        source: str,
        target: str,
    ) -> Investigation:
        graph: KnowledgeGraph = investigation.analysis["knowledge_graph"]

        investigation.analysis["attack_path"] = (
            self._path_finder.shortest_path(
                graph,
                source,
                target,
            )
        )

        return investigation
