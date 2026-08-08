export default function ExecutiveSummary() {
  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-blue-400">
          Executive Summary
        </p>

        <h3 className="mt-2 text-lg font-semibold text-white">
          Current security posture requires attention
        </h3>

        <p className="mt-3 max-w-4xl text-sm leading-6 text-slate-400">
          Production infrastructure contains multiple privilege escalation
          paths and publicly accessible resources. Immediate remediation is
          recommended for high-risk IAM permissions and exposed
          infrastructure.
        </p>
      </div>
    </section>
  );
}
