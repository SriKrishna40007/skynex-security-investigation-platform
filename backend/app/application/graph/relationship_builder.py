from app.domain.models.investigation import Investigation


class RelationshipBuilder:
    """
    Builds relationships between infrastructure resources.

    Responsibility:
        Discover how infrastructure resources are connected.

    Input:
        Investigation

    Output:
        Investigation with populated relationships
    """

    def build(self, investigation: Investigation) -> Investigation:
        """
        Current Sprint:
            Placeholder implementation.

        Future:
            - Internet Gateway
            - Route Tables
            - VPC
            - Subnets
            - Security Groups
            - Load Balancers
            - EC2
            - RDS
            - Lambda
        """

        return investigation


