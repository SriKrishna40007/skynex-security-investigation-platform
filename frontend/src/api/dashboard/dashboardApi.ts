import { apiRequest } from "@/api/httpClient";

import type {
  DashboardActivity,
  DashboardAnalytics,
  DashboardSummary,
} from "./dashboardTypes";

export async function getDashboardSummary(
  accessToken: string,
): Promise<DashboardSummary> {
  return apiRequest<DashboardSummary>(
    "/dashboard/summary",
    {
      method: "GET",
      accessToken,
    },
  );
}

export async function getDashboardActivity(
  accessToken: string,
  limit = 10,
): Promise<DashboardActivity[]> {
  return apiRequest<DashboardActivity[]>(
    `/dashboard/activity?limit=${encodeURIComponent(String(limit))}`,
    {
      method: "GET",
      accessToken,
    },
  );
}

export async function getDashboardAnalytics(
  accessToken: string,
): Promise<DashboardAnalytics> {
  return apiRequest<DashboardAnalytics>(
    "/dashboard/analytics",
    {
      method: "GET",
      accessToken,
    },
  );
}
