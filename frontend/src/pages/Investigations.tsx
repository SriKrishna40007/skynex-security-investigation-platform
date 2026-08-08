import {
  ArrowRight,
  Clock3,
  Filter,
  Plus,
  Search,
  ShieldAlert,
  ShieldCheck,
} from "lucide-react";
import { Link } from "react-router-dom";
import { useInvestigations } from "@/investigations/useInvestigations";


import type { Investigation } from "@/types/investigation";

const riskClasses: Record<Investigation["risk"], string> = {
  Critical: "border-rose-400/20 bg-rose-400/10 text-rose-300",
  High: "border-orange-400/20 bg-orange-400/10 text-orange-300",
  Medium: "border-amber-400/20 bg-amber-400/10 text-amber-300",
  Low: "border-emerald-400/20 bg-emerald-400/10 text-emerald-300",
};

const statusClasses: Record<Investigation["status"], string> = {
  Queued: "text-slate-400",
  Running: "text-blue-300",
  Analyzing: "text-violet-300",
  Completed: "text-emerald-300",
  Failed: "text-rose-300",
};

export default function Investigations() {
  const { investigations } = useInvestigations();

  return (
    <section className="space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-400">
            Security Operations
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
            Investigations
          </h1>

          <p className="mt-2 max-w-2xl text-sm text-slate-400">
            Investigate cloud infrastructure, understand security risk and
            turn findings into actionable engineering decisions.
          </p>
        </div>

        <Link
          to="/app/investigations/new"
          className="inline-flex h-10 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-4 text-sm font-semibold text-white shadow-lg shadow-blue-500/10 transition hover:brightness-110"
        >
          <Plus className="h-4 w-4" />
          New Investigation
        </Link>
      </div>

      <div className="flex flex-col gap-3 rounded-2xl border border-white/[0.07] bg-[#0b1222] p-3 md:flex-row">
        <div className="flex h-10 flex-1 items-center gap-2 rounded-xl border border-white/[0.07] bg-white/[0.02] px-3">
          <Search className="h-4 w-4 text-slate-500" />

          <input
            type="search"
            placeholder="Search investigations..."
            className="min-w-0 flex-1 bg-transparent text-sm text-white outline-none placeholder:text-slate-600"
          />
        </div>

        <button
          type="button"
          className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-white/[0.08] px-4 text-sm text-slate-300 transition hover:bg-white/[0.04]"
        >
          <Filter className="h-4 w-4" />
          Filters
        </button>
      </div>

      <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0b1222]">
        <div className="border-b border-white/[0.07] px-5 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-white">
                Investigation queue
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                {investigations.length} investigations in the workspace
              </p>
            </div>
          </div>
        </div>

        <div className="divide-y divide-white/[0.06]">
          {investigations.map((investigation) => (
            <Link
              key={investigation.id}
              to={`/app/investigations/${investigation.id}`}
              className="group block px-5 py-5 transition hover:bg-white/[0.025]"
            >
              <div className="flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
                <div className="flex min-w-0 items-start gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-blue-400/10 bg-blue-400/10">
                    {investigation.risk === "Critical" ? (
                      <ShieldAlert className="h-5 w-5 text-rose-400" />
                    ) : (
                      <ShieldCheck className="h-5 w-5 text-blue-400" />
                    )}
                  </div>

                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-medium text-white group-hover:text-blue-300">
                        {investigation.name}
                      </h3>

                      <span
                        className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${riskClasses[investigation.risk]}`}
                      >
                        {investigation.risk}
                      </span>
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      {investigation.provider} · {investigation.environment} · {investigation.type}
                    </p>

                    <div className="mt-3 flex flex-wrap items-center gap-4 text-xs text-slate-500">
                      <span>{investigation.findings} findings</span>
                      <span>{investigation.resources} resources</span>

                      <span className="inline-flex items-center gap-1">
                        <Clock3 className="h-3.5 w-3.5" />
                        {investigation.updated}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-5 xl:shrink-0">
                  <span
                    className={`text-xs font-medium ${statusClasses[investigation.status]}`}
                  >
                    {investigation.status}
                  </span>

                  <ArrowRight className="h-4 w-4 text-slate-600 transition group-hover:translate-x-1 group-hover:text-blue-400" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
