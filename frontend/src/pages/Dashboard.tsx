import ExecutiveSummary from "@/components/dashboard/ExecutiveSummary";
import StatsGrid from "@/components/dashboard/StatsGrid";

export default function Dashboard() {
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

      <StatsGrid />

      <ExecutiveSummary />
    </section>
  );
}
