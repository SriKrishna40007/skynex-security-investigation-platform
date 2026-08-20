# SKYNEX - Cloud Security Investigation Platform

SKYNEX is a cloud security investigation platform designed to help security engineers understand how cloud infrastructure resources are connected and investigate potential security paths through that infrastructure.

## What Problem Does SKYNEX Solve?

Cloud infrastructure is not just a collection of independent resources. Resources are connected through networks, security groups, IAM relationships, dependencies, and other security-relevant relationships.

SKYNEX models these relationships so an investigator can ask questions such as:

- Can a security path exist between two resources?
- What resources are involved in that path?
- What could be affected if a resource is compromised?
- What evidence supports the finding?
- How should the resulting risk be understood?

## V1 Investigation Workflow

```text
Terraform configuration
        |
        v
Resource discovery
        |
        v
Canonical resource model
        |
        v
Security relationship graph
        |
        v
Investigation
        |
        +--------------------+
        |                    |
        v                    v
Attack-path analysis    Blast-radius analysis
        |                    |
        +---------+----------+
                  |
                  v
        Risk + evidence + reasoning