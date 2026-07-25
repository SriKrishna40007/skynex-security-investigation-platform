from app.domain.models.investigation import Investigation
from app.domain.models.resource import Resource


class InvestigationBuilder:
    """
    Builds canonical Investigation domain models from
    external integration results.
    """

    def from_terraform_scan(
        self,
        scan_result: dict,
    ) -> Investigation:
        from pprint import pprint

        pprint(scan_result)

        investigation = Investigation(
            id="terraform-investigation",
            name="Terraform Investigation",
        )

        for sdk_resource in scan_result.get("resources", []):

            investigation.resources.append(
                Resource(
                    id=f"{sdk_resource.resource_type}.{sdk_resource.resource_name}",
                    name=sdk_resource.resource_name,
                    type=sdk_resource.resource_type,
                    provider="terraform",
                    metadata=sdk_resource.attributes,
                )
            )

        return investigation