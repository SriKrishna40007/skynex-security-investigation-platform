export type InvestigationStatus =
  | "Queued"
  | "Running"
  | "Analyzing"
  | "Completed"
  | "Failed";

export type RiskLevel =
  | "Critical"
  | "High"
  | "Medium"
  | "Low";

export type CloudProvider =
  | "AWS"
  | "Microsoft Azure"
  | "Google Cloud";

export type InvestigationEnvironment =
  | "Production"
  | "Staging"
  | "Development"
  | "Security";

export type InvestigationType =
  | "Cloud Security"
  | "IAM Analysis"
  | "Infrastructure Security"
  | "Attack Path Analysis"
  | "Terraform"
  | "IAM";

export type InvestigationFinding = {
  id: string;
  title: string;
  severity: RiskLevel;
  resource: string;
};

export type Investigation = {
  id: string;
  name: string;
  provider: CloudProvider;
  environment: InvestigationEnvironment;
  type: InvestigationType;

  status: InvestigationStatus;
  risk: RiskLevel;

  riskScore: number;

  resources: number;
  findings: number;
  attackPaths: number;

  updated: string;

  findingsList: InvestigationFinding[];
};
