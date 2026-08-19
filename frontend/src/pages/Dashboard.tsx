import {
  useEffect,
  useState,
} from "react";

import { useAuth } from "@/auth/useAuth";
import {
  getDashboardActivity,
  getDashboardAnalytics,
  getDashboardSummary,
} from "@/api/dashboard/dashboardApi";
import type {
  DashboardActivity,
  DashboardAnalytics,
  DashboardSummary,
} from "@/api/dashboard/dashboardTypes";

import DashboardAnalyticsPanel from "@/components/dashboard/DashboardAnalyticsPanel";
import ExecutiveSummary from "@/components/dashboard/ExecutiveSummary";
import RecentActivity from "@/components/dashboard/RecentActivity";
import StatsGrid from "@/components/dashboard/StatsGrid";

type DashboardState = {
  summary: DashboardSummary | null;
  activity: DashboardActivity[];
  analytics: DashboardAnalytics | null;
  isLoading: boolean;
  error: string | null;
};

const initialState: DashboardState = {
  summary: null,
  activity: [],
  analytics: null,
  isLoading: true,
  error: null,
};

export default function Dashboard() {
  const { state: authState } = useAuth();

  const [dashboard, setDashboard] =
    useState<DashboardState>(initialState);

  useEffect(() => {
    const accessToken =
      authState.session?.accessToken;

    if (!accessToken) {
      return;
    }

    let cancelled = false;

    async function loadDashboard(token: string) {
      setDashboard({
        summary: null,
        activity: [],
        analytics: null,
        isLoading: true,
        error: null,
      });

      try {
        const [
          summary,
          activity,
          analytics,
        ] = await Promise.all([
          getDashboardSummary(token),
          getDashboardActivity(token, 10),
          getDashboardAnalytics(token),
        ]);

        if (cancelled) {
          return;
        }

        setDashboard({
          summary,
          activity,
          analytics,
          isLoading: false,
          error: null,
        });
      } catch (error) {
        if (cancelled) {
          return;
        }

        setDashboard({
          summary: null,
          activity: [],
          analytics: null,
          isLoading: false,
          error:
            error instanceof Error
              ? error.message
              : "Unable to load dashboard data.",
        });
      }
    }

    void loadDashboard(accessToken);

    return () => {
      cancelled = true;
    };
  }, [authState.session?.accessToken]);

  return (
    <section className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold tracking-tight text-white">
          Dashboard
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Overview of your cloud security posture
        </p>
      </header>

      {dashboard.error && (
        <div
          role="alert"
          className="rounded-2xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300"
        >
          {dashboard.error}
        </div>
      )}

      <StatsGrid
        summary={dashboard.summary}
        isLoading={dashboard.isLoading}
      />

      <ExecutiveSummary
        summary={dashboard.summary}
        isLoading={dashboard.isLoading}
      />

      <RecentActivity
        activity={dashboard.activity}
        isLoading={dashboard.isLoading}
        error={dashboard.error}
      />

      <DashboardAnalyticsPanel
        analytics={dashboard.analytics}
        isLoading={dashboard.isLoading}
      />
    </section>
  );
}
