from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class BlastRadiusImpact:
    """
    Security impact associated with one reachable canonical resource.

    The model intentionally contains no provider-specific fields.
    Provider integrations are responsible for normalizing evidence before
    blast-radius analysis begins.
    """

    resource_id: str
    depth: int
    relationship_types: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class BlastRadiusAnalysis:
    """
    Provider-neutral explanation of compromise propagation.

    The existing ``analysis["blast_radius"]`` list remains the compatibility
    contract. This model provides richer evidence for investigation,
    reasoning, and future presentation layers.
    """

    compromised_resource: str
    reachable_resources: tuple[str, ...]
    impacts: tuple[BlastRadiusImpact, ...]

    @property
    def affected_resource_count(self) -> int:
        """
        Return the number of resources affected beyond the compromised node.
        """

        return len(
            [
                resource_id
                for resource_id in self.reachable_resources
                if resource_id != self.compromised_resource
            ]
        )

    @property
    def maximum_depth(self) -> int:
        """Return the deepest observed propagation distance."""

        return max(
            (impact.depth for impact in self.impacts),
            default=0,
        )
