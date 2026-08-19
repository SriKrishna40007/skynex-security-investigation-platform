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

export type InvestigationAttackPath = {
  source: string;
  target: string;
  nodes: string[];
  hopCount: number;
  risk: string;
  description: string;
  exists: boolean;
};

export type InvestigationBlastRadius = {
  compromisedResource: string;
  reachableResources: string[];
  affectedResourceCount: number;
  maximumDepth: number;
  impacts: Array<{
    resourceId: string;
    depth: number;
    relationshipTypes: string[];
  }>;
};

export type InvestigationRiskAssessment = {
  score: number;
  severity: string;
  reasons: string[];
};

export type InvestigationReasoning = {
  findings: string[];
  recommendations: string[];
  severity: string;
};

export type InvestigationRemediation = {
  findingId: string;
  title: string;
  severity: string;
  resourceId: string;
  steps: string[];
  executable: boolean;
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

  attackPathAnalysis: InvestigationAttackPath | null;
  blastRadiusAnalysis: InvestigationBlastRadius | null;
  riskAssessment: InvestigationRiskAssessment | null;
  reasoning: InvestigationReasoning | null;
  remediations: InvestigationRemediation[];
};
