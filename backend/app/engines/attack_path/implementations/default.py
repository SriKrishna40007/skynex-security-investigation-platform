from app.domain.models.attack_path import AttackPath
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

        if attack_path.hop_count >= 5:
            attack_path.risk = "CRITICAL"
            attack_path.description = (
                "Long attack chain with multiple pivot opportunities."
            )
        elif attack_path.hop_count >= 3:
            attack_path.risk = "HIGH"
            attack_path.description = (
                "Attacker can reach the target through several connected resources."
            )
        elif attack_path.hop_count >= 1:
            attack_path.risk = "MEDIUM"
            attack_path.description = (
                "Target is reachable through a limited attack path."
            )
        else:
            attack_path.risk = "LOW"
            attack_path.description = (
                "No attack path could be established."
            )

        investigation.analysis["attack_path"] = attack_path

        return investigation
