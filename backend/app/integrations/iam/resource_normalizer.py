from __future__ import annotations

from typing import Any

from app.domain.models.resource import Resource


class IAMResourceNormalizer:
    """
    Converts IAM policy resource evidence into canonical SKYNEX resources.

    AWS-specific ARN interpretation terminates at this integration boundary.
    Downstream graph and investigation engines operate only on Resource.
    """

    def normalize_policy_resources(
        self,
        policy_data: dict[str, Any],
    ) -> list[Resource]:
        resources: dict[str, Resource] = {}

        for statement in self._statements(policy_data):
            for resource_arn in self._resource_values(statement):
                resource = self._from_arn(resource_arn)

                if resource is not None:
                    resources.setdefault(
                        resource.id,
                        resource,
                    )

        return list(resources.values())

    @staticmethod
    def _statements(
        policy_data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        statements = policy_data.get("Statement", [])

        if isinstance(statements, dict):
            return [statements]

        if isinstance(statements, list):
            return [
                statement for statement in statements if isinstance(statement, dict)
            ]

        return []

    @staticmethod
    def _resource_values(
        statement: dict[str, Any],
    ) -> list[str]:
        value = statement.get("Resource", [])

        if isinstance(value, str):
            return [value]

        if isinstance(value, list):
            return [item for item in value if isinstance(item, str)]

        return []

    def _from_arn(
        self,
        arn: str,
    ) -> Resource | None:
        if not arn.startswith("arn:"):
            return None

        parts = arn.split(":", 5)

        if len(parts) != 6:
            return None

        _, partition, service, region, account_id, resource_part = parts

        resource_type, resource_name = self._resource_identity(
            service,
            resource_part,
        )

        return Resource(
            id=arn,
            name=resource_name,
            type=resource_type,
            provider="aws",
            metadata={
                "arn": arn,
                "partition": partition,
                "service": service,
                "region": region,
                "account_id": account_id,
                "source": "iam_policy",
            },
        )

    @staticmethod
    def _resource_identity(
        service: str,
        resource_part: str,
    ) -> tuple[str, str]:
        if service == "iam" and resource_part.startswith("role/"):
            return (
                "iam_role",
                resource_part.removeprefix("role/"),
            )

        if service == "iam" and resource_part.startswith("user/"):
            return (
                "iam_user",
                resource_part.removeprefix("user/"),
            )

        if service == "iam" and resource_part.startswith("policy/"):
            return (
                "iam_policy",
                resource_part.removeprefix("policy/"),
            )

        name = resource_part

        if "/" in name:
            name = name.rsplit("/", 1)[-1]

        elif ":" in name:
            name = name.rsplit(":", 1)[-1]

        return (
            f"aws_{service}_resource",
            name or resource_part,
        )
