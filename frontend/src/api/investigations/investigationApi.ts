import { apiRequest } from "@/api/httpClient";

import type {
  InvestigationHistoryCollectionResponse,
  InvestigationResponse,
} from "./investigationTypes";

export type InvestigationHistoryQuery = {
  page?: number;
  size?: number;
  status?: string;
  severity?: string;
  investigation_type?: string;
  search?: string;
  sort_by?: string;
  descending?: boolean;
};

export async function executeTerraformInvestigation(
  accessToken: string,
  file: File,
  source: string,
  target: string,
): Promise<InvestigationResponse> {
  const formData = new FormData();

  formData.append("terraform_file", file);
  formData.append("source", source);
  formData.append("target", target);

  return apiRequest<InvestigationResponse>("/investigations/terraform", {
    method: "POST",
    body: formData,
    accessToken,
  });
}

export async function listInvestigations(
  accessToken: string,
  query: InvestigationHistoryQuery = {},
): Promise<InvestigationHistoryCollectionResponse> {
  const params = new URLSearchParams();

  if (query.page !== undefined) {
    params.set("page", String(query.page));
  }

  if (query.size !== undefined) {
    params.set("size", String(query.size));
  }

  if (query.status) {
    params.set("status", query.status);
  }

  if (query.severity) {
    params.set("severity", query.severity);
  }

  if (query.investigation_type) {
    params.set("investigation_type", query.investigation_type);
  }

  if (query.search) {
    params.set("search", query.search);
  }

  if (query.sort_by) {
    params.set("sort_by", query.sort_by);
  }

  if (query.descending !== undefined) {
    params.set("descending", String(query.descending));
  }

  const suffix = params.toString()
    ? `?${params.toString()}`
    : "";

  return apiRequest<InvestigationHistoryCollectionResponse>(
    `/investigations${suffix}`,
    {
      method: "GET",
      accessToken,
    },
  );
}

export async function getInvestigation(
  accessToken: string,
  investigationId: string,
): Promise<InvestigationResponse> {
  return apiRequest<InvestigationResponse>(
    `/investigations/${encodeURIComponent(investigationId)}`,
    {
      method: "GET",
      accessToken,
    },
  );
}

export async function deleteInvestigation(
  accessToken: string,
  investigationId: string,
): Promise<void> {
  await apiRequest<void>(
    `/investigations/${encodeURIComponent(investigationId)}`,
    {
      method: "DELETE",
      accessToken,
    },
  );
}

export async function exportInvestigation(
  accessToken: string,
  investigationId: string,
  format = "json",
): Promise<unknown> {
  return apiRequest(
    `/investigations/${encodeURIComponent(investigationId)}/export?format=${encodeURIComponent(format)}`,
    {
      method: "GET",
      accessToken,
    },
  );
}
