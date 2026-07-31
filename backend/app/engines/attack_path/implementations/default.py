from app.domain.models.attack_path import AttackPath
from app.domain.models.investigation import Investigation
from app.engines.attack_path.base import AttackPathEngine
from app.engines.attack_path.policies import AttackPathSemanticRiskPolicy
from app.engines.graph.algorithms import PathFinder
from app.engines.graph.models import KnowledgeGraph


class DefaultAttackPathEngine(AttackPathEngine):
    """Default attack path implementation."""

    def __init__(self) -> None:
        self._path_finder = PathFinder()
        self._risk_policy = AttackPathSemanticRiskPolicy()

    def analyze(
        self,
        investigation: Investigation,
        source: str,
        target: str,
    ) -> Investigation:
        graph: KnowledgeGraph = investigation.analysis["knowledge_graph"]

        nodes = self._path_finder.shortest_path(
            graph,
            source,
            target,
        )

        attack_path = AttackPath(
            source=source,
            target=target,
            nodes=nodes,
            hop_count=max(len(nodes) - 1, 0),
            exists=len(nodes) > 0,
        )

        risk = self._risk_policy.evaluate(
            graph,
            nodes,
        )

        attack_path.risk = risk.severity
        attack_path.description = risk.description

        investigation.analysis["attack_path"] = attack_path

        return investigation
