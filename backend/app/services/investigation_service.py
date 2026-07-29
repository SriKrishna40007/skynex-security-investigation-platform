from app.schemas.investigation import (
    Evidence,
    Finding,
    InvestigationReport,
    Remediation,
    Risk,
    Summary,
)


class InvestigationService:
    """
    Builds canonical investigation reports from scanner results.
    """

    def build_terraform_report(self, scan_result: dict) -> InvestigationReport:
        findings = []

        high = 0
        medium = 0
        low = 0

        for sdk_finding in scan_result["findings"]:
            severity = sdk_finding.severity.upper()

            if severity == "HIGH":
                high += 1
                score = 90
            elif severity == "MEDIUM":
                medium += 1
                score = 60
            else:
                low += 1
                score = 30

            findings.append(
                Finding(
                    scanner="terraform",
                    rule_id=sdk_finding.rule_id,
                    title=sdk_finding.title,
                    description=sdk_finding.title,
                    severity=severity,
                    resource=sdk_finding.resource,
                    evidence=Evidence(
                        resource=sdk_finding.resource,
                        attribute="N/A",
                        value="N/A",
                    ),
                    risk=Risk(
                        level=severity,
                        score=score,
                    ),
                    remediation=Remediation(
                        title="Recommended Fix",
                        steps=[
                            sdk_finding.recommendation,
                        ],
                    ),
                )
            )

        return InvestigationReport(
            summary=Summary(
                scanner="terraform",
                security_score=scan_result["security_score"],
                total_findings=len(findings),
                high=high,
                medium=medium,
                low=low,
            ),
            findings=findings,
        )

    def build_iam_report(self, analysis_result):
        raise NotImplementedError("IAM integration will be updated next.")
