import type {
  DashboardAnalytics,
  TrendPoint,
} from "@/api/dashboard/dashboardTypes";

type DashboardAnalyticsPanelProps = {
  analytics: DashboardAnalytics | null;
  isLoading: boolean;
};

function maxValue(points: TrendPoint[]): number {
  return Math.max(...points.map((point) => point.value), 1);
}

function TrendChart({
  title,
  points,
}: {
  title: string;
  points: TrendPoint[];
}) {
  const width = 640;
  const height = 220;
  const padding = 32;
  const max = maxValue(points);

  const usableWidth = width - padding * 2;
  const usableHeight = height - padding * 2;

  const coordinates = points.map((point, index) => {
    const x =
      points.length <= 1
        ? width / 2
        : padding +
          (index / (points.length - 1)) *
            usableWidth;

    const y =
      height -
      padding -
      (point.value / max) * usableHeight;

    return { ...point, x, y };
  });

  const polyline = coordinates
    .map((point) => `${point.x},${point.y}`)
    .join(" ");

  return (
    <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-white">
          {title}
        </h4>

        <span className="text-xs text-slate-500">
          {points.length} points
        </span>
      </div>

      {points.length === 0 ? (
        <p className="mt-8 text-sm text-slate-500">
          No trend data available yet.
        </p>
      ) : (
        <>
          <svg
            className="mt-5 h-56 w-full"
            viewBox={`0 0 ${width} ${height}`}
            role="img"
            aria-label={title}
            preserveAspectRatio="none"
          >
            <line
              x1={padding}
              y1={height - padding}
              x2={width - padding}
              y2={height - padding}
              stroke="currentColor"
              className="text-white/10"
            />

            <line
              x1={padding}
              y1={padding}
              x2={padding}
              y2={height - padding}
              stroke="currentColor"
              className="text-white/10"
            />

            <polyline
              points={polyline}
              fill="none"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-blue-400"
            />

            {coordinates.map((point) => (
              <circle
                key={`${point.label}-${point.x}`}
                cx={point.x}
                cy={point.y}
                r="4"
                className="fill-blue-400"
              />
            ))}
          </svg>

          <div className="mt-2 flex justify-between gap-2 text-xs text-slate-500">
            {coordinates.map((point) => (
              <span key={`${point.label}-label`}>
                {point.label}
              </span>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function Distribution({
  title,
  values,
}: {
  title: string;
  values: Record<string, number>;
}) {
  const entries = Object.entries(values);
  const total = entries.reduce(
    (sum, [, value]) => sum + value,
    0,
  );

  return (
    <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
      <h4 className="text-sm font-semibold text-white">
        {title}
      </h4>

      <div className="mt-5 space-y-4">
        {entries.map(([label, value]) => {
          const percentage =
            total > 0 ? (value / total) * 100 : 0;

          return (
            <div key={label}>
              <div className="mb-1 flex justify-between text-xs">
                <span className="capitalize text-slate-400">
                  {label}
                </span>

                <span className="font-medium text-white">
                  {value}
                </span>
              </div>

              <div className="h-2 overflow-hidden rounded-full bg-white/[0.06]">
                <div
                  className="h-full rounded-full bg-blue-400"
                  style={{
                    width: `${percentage}%`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function DashboardAnalyticsPanel({
  analytics,
  isLoading,
}: DashboardAnalyticsPanelProps) {
  if (isLoading) {
    return (
      <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Analytics
        </p>

        <p className="mt-3 text-sm text-slate-400">
          Loading dashboard analytics...
        </p>
      </section>
    );
  }

  if (!analytics) {
    return (
      <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Analytics
        </p>

        <p className="mt-3 text-sm text-slate-500">
          No analytics data available.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
      <div className="mb-5">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Analytics
        </p>

        <h3 className="mt-1 text-lg font-semibold text-white">
          Security investigation trends
        </h3>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <TrendChart
          title="Investigation Trend"
          points={analytics.investigation_trend}
        />

        <TrendChart
          title="Average Risk Trend"
          points={analytics.average_risk_trend}
        />

        <Distribution
          title="Severity Distribution"
          values={analytics.severity_distribution}
        />

        <Distribution
          title="Investigation Type"
          values={analytics.investigation_type_distribution}
        />
      </div>
    </section>
  );
}
