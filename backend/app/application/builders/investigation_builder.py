from __future__ import annotations

import re
from typing import Any

from app.domain.models.finding import Finding
from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource
from app.integrations.iam.resource_normalizer import IAMResourceNormalizer
from app.integrations.iam.relationship_normalizer import IAMRelationshipNormalizer


class InvestigationBuilder:
    """
    Normalizes external security-engine results into the canonical
    SKYNEX Investigation domain model.

    Provider-specific integrations terminate at this boundary. Downstream
    investigation engines operate only on canonical SKYNEX domain objects.
    """

    _REFERENCE_PATTERN = re.compile(r"\${([A-Za-z0-9_]+\.[A-Za-z0-9_]+)\.[^}]+}")

    def _extract_references(
        self,
        attributes: dict[str, Any],
    ) -> list[str]:
        """Extract Terraform resource references from nested attributes."""

        references: set[str] = set()

        def walk(value: Any) -> None:
            if isinstance(value, str):
                references.update(self._REFERENCE_PATTERN.findall(value))

            elif isinstance(value, dict):
                for item in value.values():
                    walk(item)

            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(attributes)

        return sorted(references)

    def from_terraform_scan(
        self,
        scan_result: dict[str, Any],
    ) -> Investigation:
        """Build a canonical investigation from Terraform scan output."""

        investigation = Investigation()

        for sdk_resource in scan_result.get("resources", []):
            tags: dict[str, str] = {}

            if isinstance(sdk_resource.attributes.get("tags"), dict):
                tags = sdk_resource.attributes["tags"]

            metadata = dict(sdk_resource.attributes)
            metadata["references"] = self._extract_references(sdk_resource.attributes)

            investigation.resources.append(
                Resource(
                    id=(f"{sdk_resource.resource_type}.{sdk_resource.resource_name}"),
                    name=sdk_resource.resource_name,
                    type=sdk_resource.resource_type,
                    provider="terraform",
                    tags=tags,
                    metadata=metadata,
                )
            )

        return investigation

    def from_iam_analysis(
        self,
        analysis_result: Any,
        *,
        policy_data: dict[str, Any] | None = None,
    ) -> Investigation:
        """
        Build a canonical investigation from IAM Intelligence Engine output.

        IAM findings are normalized at this boundary so downstream SKYNEX
        components do not depend on IAM Intelligence Engine domain classes.
        """

        investigation = Investigation()

        summary = analysis_result.summary

        resource_ids: dict[str, str] = {}

        # The IAM policy is a first-class canonical resource regardless of
        # whether the external engine produced findings. Authorization
        # relationships require a stable source node even for clean policies.
        policy_resource_id = self._iam_resource_id("IAM Policy")

        investigation.resources.append(
            Resource(
                id=policy_resource_id,
                name="IAM Policy",
                type="iam_policy",
                provider="aws",
                metadata={
                    "source": "iam_intelligence_engine",
                },
            )
        )

        resource_ids["IAM Policy"] = policy_resource_id

        for engine_finding in summary.findings:
            resource_name = engine_finding.resource or "IAM Policy"

            resource_id = resource_ids.get(resource_name)

            if resource_id is None:
                resource_id = self._iam_resource_id(resource_name)
                resource_ids[resource_name] = resource_id

                investigation.resources.append(
                    Resource(
                        id=resource_id,
                        name=resource_name,
                        type="iam_policy",
                        provider="aws",
                        metadata={
                            "source": "iam_intelligence_engine",
                        },
                    )
                )

            severity = getattr(
                engine_finding.severity,
                "value",
                str(engine_finding.severity),
            )

            investigation.findings.append(
                Finding(
                    id=engine_finding.rule_id,
                    title=engine_finding.rule_name,
                    description=engine_finding.description,
                    severity=severity,
                    resource_id=resource_id,
                    recommendation=engine_finding.recommendation,
                    metadata={
                        "message": engine_finding.message,
                        "passed": engine_finding.passed,
                        "source": "iam_intelligence_engine",
                    },
                )
            )

        investigation.risk_score = float(summary.overall_risk_score)

        investigation.analysis["iam"] = {
            "overall_risk_score": summary.overall_risk_score,
            "recommendations": list(summary.recommendations),
            "correlations": list(summary.correlations),
            "finding_count": len(summary.findings),
        }

        if policy_data is not None:
            investigation.analysis["iam"]["policy"] = policy_data

            normalizer = IAMResourceNormalizer()

            known_resource_ids = {resource.id for resource in investigation.resources}

            for resource in normalizer.normalize_policy_resources(
                policy_data,
            ):
                if resource.id not in known_resource_ids:
                    investigation.resources.append(resource)
                    known_resource_ids.add(resource.id)

            relationship_normalizer = IAMRelationshipNormalizer()

            investigation.relationships.extend(
                relationship_normalizer.normalize_policy_relationships(
                    policy_data,
                    investigation.resources,
                )
            )

        return investigation

    @staticmethod
    def _iam_resource_id(resource_name: str) -> str:
        """Create a stable canonical identifier for an IAM resource."""

        normalized = re.sub(
            r"[^a-z0-9]+",
            "-",
            resource_name.lower(),
        ).strip("-")

        return f"aws.iam_policy.{normalized or 'policy'}"
