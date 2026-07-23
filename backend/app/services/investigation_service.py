from app.schemas.investigation import (
    Evidence,
    Finding,
    InvestigationReport,
    Summary,
)


class InvestigationService:
    def build_terraform_report(self, scan_result) -> InvestigationReport:
        findings = []

        for finding in scan_result.findings:
            findings.append(
                Finding(
                    scanner="terraform",
                    rule_id=finding.rule_id,
                    title=finding.title,
                    severity=finding.severity,
                    evidence=Evidence(
                        resource=finding.resource,
                        attribute=finding.attribute,
                        value=str(finding.value),
                    ),
                )
            )

        return InvestigationReport(
            summary=Summary(
                scanner="terraform",
                security_score=scan_result.security_score,
                findings=len(findings),
            ),
            findings=findings,
        )

    def build_iam_report(self, analysis_result) -> InvestigationReport:
        findings = []

        for finding in analysis_result.findings:
            findings.append(
                Finding(
                    scanner="iam",
                    rule_id=finding.rule_id,
                    title=finding.title,
                    severity=finding.severity,
                    evidence=Evidence(
                        resource=finding.resource,
                        attribute=finding.attribute,
                        value=str(finding.value),
                    ),
                )
            )

        return InvestigationReport(
            summary=Summary(
                scanner="iam",
                security_score=analysis_result.risk_score,
                findings=len(findings),
            ),
            findings=findings,
        )
