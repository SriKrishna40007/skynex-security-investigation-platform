import { apiRequest } from "@/api/httpClient";

import type {
  Investigation,
  InvestigationFinding,
} from "@/types/investigation";

import type {
  CreateInvestigationInput,
  InvestigationRepository,
} from "./InvestigationRepository";

type BackendInvestigationResponse = {
  id?: string;
  attack_path: string[];
  blast_radius: string[];
  risk_score: number;
  summary: string;

  attack_path_analysis?: {
    source: string;
    target: string;
    nodes: string[];
    hop_count: number;
    risk: string;
    description: string;
    exists: boolean;
  } | null;

  blast_radius_analysis?: {
    compromised_resource: string;
    reachable_resources: string[];
    affected_resource_count: number;
    maximum_depth: number;
    impacts: Array<{
      resource_id: string;
      depth: number;
      relationship_types: string[];
    }>;
  } | null;

  risk?: {
    score: number;
    severity: string;
    reasons: string[];
  } | null;

  reasoning?: {
    findings: string[];
    recommendations: string[];
    severity: string;
  } | null;
};

type BackendHistoryItem = {
  id: string;
  investigation_type: string;
  status: string;
  severity: string;
  risk_score: number;
  summary: string;
  created_at: string;
};

type BackendHistoryResponse = {
  items: BackendHistoryItem[];
  page: number;
  size: number;
  total: number;
  pages: number;
};

function mapRiskSeverity(
  severity: string,
): Investigation["risk"] {
  const normalized = severity.toLowerCase();

  if (
    normalized === "critical" ||
    normalized === "high" ||
    normalized === "medium" ||
    normalized === "low"
  ) {
    return (
      normalized.charAt(0).toUpperCase() +
      normalized.slice(1)
    ) as Investigation["risk"];
  }

  return "Medium";
}

function mapResponse(
  response: BackendInvestigationResponse,
  input?: CreateInvestigationInput,
  id?: string,
): Investigation {
  const severity =
    response.risk?.severity ??
    response.reasoning?.severity ??
    "LOW";

  const findingMessages =
    response.reasoning?.findings ?? [];

  const findings: InvestigationFinding[] =
    findingMessages.map((finding, index) => ({
      id: `finding-${index + 1}`,
      title: finding,
      severity: mapRiskSeverity(severity),
      resource: "Investigation",
    }));

  const attackPaths =
    response.attack_path_analysis?.exists
      ? 1
      : response.attack_path.length > 0
        ? 1
        : 0;

  return {
    id: id ?? response.id ?? `inv-${crypto.randomUUID()}`,
    name:
      input?.name ??
      response.summary ??
      "Security Investigation",

    provider:
      input?.provider ?? "AWS",

    environment:
      input?.environment ?? "Production",

    type:
      input?.type ?? "Terraform",

    status: "Completed",
    risk: mapRiskSeverity(severity),
    riskScore: response.risk_score,

    resources:
      response.blast_radius_analysis
        ?.affected_resource_count ??
      response.blast_radius.length,

    findings: findings.length,

    attackPaths,

    updated: "Just now",

    findingsList: findings,
  };
}

function mapHistoryItem(
  item: BackendHistoryItem,
): Investigation {
  return {
    id: item.id,
    name:
      item.summary || "Security Investigation",
    provider: "AWS",
    environment: "Production",
    type:
      item.investigation_type === "terraform"
        ? "Terraform"
        : "IAM",

    status:
      item.status === "completed"
        ? "Completed"
        : "Failed",

    risk: mapRiskSeverity(item.severity),
    riskScore: item.risk_score,

    resources: 0,
    findings: 0,
    attackPaths: 0,

    updated: item.created_at,
    findingsList: [],
  };
}

export class ApiInvestigationRepository
  implements InvestigationRepository
{
  private readonly accessToken: string;

  constructor(accessToken: string) {
    this.accessToken = accessToken;
  }

  async create(
    input: CreateInvestigationInput,
  ): Promise<Investigation> {
    if (!input.terraformFile) {
      throw new Error(
        "A Terraform file is required.",
      );
    }

    const formData = new FormData();

    formData.append(
      "terraform_file",
      input.terraformFile,
    );

    formData.append(
      "source",
      input.source ?? "",
    );

    formData.append(
      "target",
      input.target ?? "",
    );

    const response =
      await apiRequest<BackendInvestigationResponse>(
        "/investigations/terraform",
        {
          method: "POST",
          body: formData,
          accessToken: this.accessToken,
        },
      );

    return mapResponse(response, input);
  }

  async getById(
    id: string,
  ): Promise<Investigation | undefined> {
    try {
      const response =
        await apiRequest<BackendInvestigationResponse>(
          `/investigations/${id}`,
          {
            method: "GET",
            accessToken: this.accessToken,
          },
        );

      return mapResponse(response, undefined, id);
    } catch (error) {
      if (
        error instanceof Error &&
        error.message.includes("404")
      ) {
        return undefined;
      }

      throw error;
    }
  }

  async list(): Promise<Investigation[]> {
    const response =
      await apiRequest<BackendHistoryResponse>(
        "/investigations",
        {
          method: "GET",
          accessToken: this.accessToken,
        },
      );

    return response.items.map(mapHistoryItem);
  }

  async delete(
    id: string,
  ): Promise<void> {
    await apiRequest<void>(
      `/investigations/${id}`,
      {
        method: "DELETE",
        accessToken: this.accessToken,
      },
    );
  }
}
