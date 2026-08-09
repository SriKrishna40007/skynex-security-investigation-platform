export type AttackPathAnalysisResponse = {
  source: string;
  target: string;
  nodes: string[];
  hop_count: number;
  risk: string;
  description: string;
  exists: boolean;
};

export type BlastRadiusImpactResponse = {
  resource_id: string;
  depth: number;
  relationship_types: string[];
};

export type BlastRadiusAnalysisResponse = {
  compromised_resource: string;
  reachable_resources: string[];
  affected_resource_count: number;
  maximum_depth: number;
  impacts: BlastRadiusImpactResponse[];
};

export type RiskAssessmentResponse = {
  score: number;
  severity: string;
  reasons: string[];
};

export type ReasoningResponse = {
  findings: string[];
  recommendations: string[];
  severity: string;
};

export type InvestigationResponse = {
  id?: string;
  attack_path: string[];
  blast_radius: string[];
  risk_score: number;
  summary: string;
  attack_path_analysis: AttackPathAnalysisResponse | null;
  blast_radius_analysis: BlastRadiusAnalysisResponse | null;
  risk: RiskAssessmentResponse | null;
  reasoning: ReasoningResponse | null;
};

export type InvestigationHistoryResponse = {
  id: string;
  investigation_type: string;
  status: string;
  severity: string;
  risk_score: number;
  summary: string;
  created_at: string;
};

export type InvestigationHistoryCollectionResponse = {
  items: InvestigationHistoryResponse[];
  page: number;
  size: number;
  total: number;
  pages: number;
};
