import type { DashboardActivity } from "@/api/dashboard/dashboardTypes";

type RecentActivityProps = {
  activity: DashboardActivity[];
  isLoading: boolean;
  error: string | null;
};

function formatDate(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Unknown date";
  }

  return new Intl.DateTimeFormat("en-AU", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function severityClass(severity: string): string {
  switch (severity.toUpperCase()) {
    case "CRITICAL":
      return "text-red-400";
    case "HIGH":
      return "text-orange-400";
    case "MEDIUM":
      return "text-yellow-400";
    case "LOW":
      return "text-emerald-400";
    default:
      return "text-slate-400";
  }
}

export default function RecentActivity({
  activity,
  isLoading,
  error,
}: RecentActivityProps) {
  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222]">
      <div className="border-b border-white/[0.07] px-6 py-5">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Recent Activity
        </p>

        <h3 className="mt-1 text-lg font-semibold text-white">
          Investigation activity
        </h3>
      </div>

      {isLoading && (
        <div className="px-6 py-8 text-sm text-slate-400">
          Loading recent activity...
        </div>
      )}

      {!isLoading && error && (
        <div className="px-6 py-8 text-sm text-red-400">
          Unable to load recent activity.
        </div>
      )}

      {!isLoading && !error && activity.length === 0 && (
        <div className="px-6 py-8 text-sm text-slate-400">
          No investigations have been recorded yet.
        </div>
      )}

      {!isLoading && !error && activity.length > 0 && (
        <div className="divide-y divide-white/[0.05]">
          {activity.map((item) => (
            <article
              key={item.id}
              className="grid gap-3 px-6 py-5 sm:grid-cols-[1fr_auto]"
            >
              <div>
                <div className="flex flex-wrap items-center gap-3">
                  <h4 className="font-medium text-white">
                    {item.summary || "Security investigation"}
                  </h4>

                  <span
                    className={`text-xs font-semibold uppercase tracking-wide ${severityClass(
                      item.severity,
                    )}`}
                  >
                    {item.severity}
                  </span>
                </div>

                <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
                  <span>{item.investigation_type}</span>
                  <span>{item.status}</span>
                  <span>{formatDate(item.created_at)}</span>
                </div>
              </div>

              <div className="sm:text-right">
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Risk score
                </p>

                <p className="mt-1 text-lg font-semibold text-white">
                  {Math.round(item.risk_score)}
                </p>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
