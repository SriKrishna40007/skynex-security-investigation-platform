import re
from pprint import pprint

from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource


class InvestigationBuilder:
    """
    Builds canonical Investigation domain models from
    external integration results.
    """

    _REFERENCE_PATTERN = re.compile(
        r"\${([A-Za-z0-9_]+\.[A-Za-z0-9_]+)\.[^}]+}"
    )

    def _extract_references(
        self,
        attributes: dict,
    ) -> list[str]:
        """
        Extract Terraform resource references from resource attributes.

        Example:
            ${aws_vpc.main.id}
                ↓
            aws_vpc.main
        """

        references: set[str] = set()

        def walk(value):
            if isinstance(value, str):
                references.update(
                    self._REFERENCE_PATTERN.findall(value)
                )

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
        scan_result: dict,
    ) -> Investigation:

        pprint(scan_result)

        investigation = Investigation(
            id="terraform-investigation",
            name="Terraform Investigation",
        )

        for sdk_resource in scan_result.get("resources", []):

            tags = {}

            if isinstance(sdk_resource.attributes.get("tags"), dict):
                tags = sdk_resource.attributes["tags"]

            metadata = dict(sdk_resource.attributes)
            metadata["references"] = self._extract_references(
                sdk_resource.attributes
            )

            investigation.resources.append(
                Resource(
                    id=f"{sdk_resource.resource_type}.{sdk_resource.resource_name}",
                    name=sdk_resource.resource_name,
                    type=sdk_resource.resource_type,
                    provider="terraform",
                    tags=tags,
                    metadata=metadata,
                )
            )

        return investigation
