from __future__ import annotations

from typing import Any

from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource
from app.engines.investigation.models.candidate import (
    CandidateType,
    InvestigationCandidate,
)


class InvestigationCandidateDiscovery:
    """Discover resources that deserve deeper security investigation."""

    def discover(
        self,
        investigation: Investigation,
    ) -> list[InvestigationCandidate]:
        candidates: list[InvestigationCandidate] = []

        finding_resource_ids = {
            finding.resource_id for finding in investigation.findings
        }

        for resource in investigation.resources:
            if resource.id in finding_resource_ids:
                candidates.append(
                    InvestigationCandidate(
                        resource_id=resource.id,
                        candidate_type=CandidateType.COMPROMISE_ANCHOR,
                        reason=(
                            "Resource is associated with an existing security finding."
                        ),
                        evidence=[
                            "resource_has_security_finding",
                        ],
                        confidence=0.90,
                    )
                )
                continue

            entry_point = self._discover_network_entry_point(resource)

            if entry_point is not None:
                candidates.append(entry_point)

        return candidates

    @staticmethod
    def _normalize_string(value: Any) -> str:
        """Normalize scalar HCL values for evidence comparison."""

        if not isinstance(value, str):
            return str(value)

        return value.strip().strip('"').strip("'")

    @classmethod
    def _discover_network_entry_point(
        cls,
        resource: Resource,
    ) -> InvestigationCandidate | None:
        """
        Identify security groups with inbound rules allowing a public source.

        This identifies an investigation candidate. It does not claim that
        the resource is reachable from the internet because routing evidence
        is required to establish actual network reachability.
        """

        if resource.type != "aws_security_group":
            return None

        ingress_rules = resource.metadata.get("ingress")

        if not isinstance(ingress_rules, list):
            return None

        public_rules: list[dict[str, Any]] = []

        for rule in ingress_rules:
            if not isinstance(rule, dict):
                continue

            cidr_blocks = rule.get("cidr_blocks", [])

            if not isinstance(cidr_blocks, list):
                continue

            normalized_cidrs = {cls._normalize_string(cidr) for cidr in cidr_blocks}

            if "0.0.0.0/0" in normalized_cidrs:
                public_rules.append(rule)

        if not public_rules:
            return None

        evidence: list[str] = [
            "ingress_allows_0.0.0.0/0",
        ]

        for rule in public_rules:
            protocol = cls._normalize_string(
                rule.get("protocol", "unknown"),
            )

            from_port = rule.get("from_port")
            to_port = rule.get("to_port")

            if from_port is not None and to_port is not None:
                evidence.append(
                    f"public_ingress={protocol}:{from_port}-{to_port}",
                )
            else:
                evidence.append(
                    f"public_ingress={protocol}",
                )

        return InvestigationCandidate(
            resource_id=resource.id,
            candidate_type=CandidateType.ENTRY_POINT,
            reason=(
                "Security group permits inbound traffic from a public "
                "source and requires investigation."
            ),
            evidence=evidence,
            confidence=0.85,
        )
