import type { DashboardSummary } from "@/api/dashboard/dashboardTypes";

type ExecutiveSummaryProps = {
  summary: DashboardSummary | null;
  isLoading: boolean;
};

export default function ExecutiveSummary({
  summary,
  isLoading,
}: ExecutiveSummaryProps) {
  if (isLoading) {
    return (
      <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Executive Summary
        </p>

        <p className="mt-3 text-sm text-slate-400">
          Loading current security posture...
        </p>
      </section>
    );
  }

  const critical = summary?.critical ?? 0;
  const high = summary?.high ?? 0;
  const failed = summary?.failed ?? 0;
  const total = summary?.total_investigations ?? 0;

  const requiresAttention =
    critical > 0 || high > 0 || failed > 0;

  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Executive Summary
        </p>

        <h3 className="mt-2 text-lg font-semibold text-white">
          {requiresAttention
            ? "Current security posture requires attention"
            : "Current security posture is stable"}
        </h3>

        <p className="mt-3 max-w-4xl text-sm leading-6 text-slate-400">
          {total} investigation{total === 1 ? "" : "s"} recorded.
          {" "}
          {critical} critical and {high} high-severity finding
          {critical + high === 1 ? "" : "s"} are currently reflected
          in the dashboard, with {failed} failed investigation
          {failed === 1 ? "" : "s"}.
        </p>
      </div>
    </section>
  );
}
