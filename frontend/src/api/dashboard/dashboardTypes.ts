export type DashboardSummary = {
  total_investigations: number;
  completed: number;
  failed: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  average_risk_score: number;
};

export type DashboardActivity = {
  id: string;
  investigation_type: string;
  status: string;
  severity: string;
  summary: string;
  risk_score: number;
  created_at: string;
};

export type TrendPoint = {
  label: string;
  value: number;
};

export type SeverityDistribution = {
  critical: number;
  high: number;
  medium: number;
  low: number;
};

export type InvestigationTypeDistribution = {
  terraform: number;
  iam: number;
};

export type DashboardAnalytics = {
  investigation_trend: TrendPoint[];
  average_risk_trend: TrendPoint[];
  severity_distribution: SeverityDistribution;
  investigation_type_distribution: InvestigationTypeDistribution;
};
