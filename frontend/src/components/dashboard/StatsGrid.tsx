import StatCard from "./StatCard";

export default function StatsGrid() {
  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <StatCard
        title="Security Score"
        value={91}
      />

      <StatCard
        title="Resources"
        value={127}
      />

      <StatCard
        title="Critical Findings"
        value={18}
      />

      <StatCard
        title="Attack Paths"
        value={6}
      />
    </section>
  );
}
