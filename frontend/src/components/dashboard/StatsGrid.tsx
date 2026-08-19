import type { DashboardSummary } from "@/api/dashboard/dashboardTypes";

import StatCard from "./StatCard";

type StatsGridProps = {
  summary: DashboardSummary | null;
  isLoading: boolean;
};

export default function StatsGrid({
  summary,
  isLoading,
}: StatsGridProps) {
  const value = (
    metric: number | undefined,
  ): string | number => {
    if (isLoading) {
      return "—";
    }

    return metric ?? 0;
  };

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard
        title="Average Risk Score"
        value={
          isLoading
            ? "—"
            : `${summary?.average_risk_score.toFixed(1) ?? "0.0"}`
        }
      />

      <StatCard
        title="Total Investigations"
        value={value(
          summary?.total_investigations,
        )}
      />

      <StatCard
        title="Critical Findings"
        value={value(summary?.critical)}
      />

      <StatCard
        title="Failed Investigations"
        value={value(summary?.failed)}
      />
    </section>
  );
}
