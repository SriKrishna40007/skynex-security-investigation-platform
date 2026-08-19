import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Lightbulb,
  Loader2,
  ShieldAlert,
  Target,
} from "lucide-react";
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Layout from "@/components/layout/Layout";
import { useInvestigations } from "@/investigations/useInvestigations";

const severityClasses: Record<string, string> = {
  Critical:
    "border-rose-400/20 bg-rose-400/10 text-rose-300",
  High:
    "border-orange-400/20 bg-orange-400/10 text-orange-300",
  Medium:
    "border-amber-400/20 bg-amber-400/10 text-amber-300",
  Low:
    "border-emerald-400/20 bg-emerald-400/10 text-emerald-300",
};

export default function AIInvestigation() {
  const {
    investigations,
    isLoading,
  } = useInvestigations();

  const [selectedId, setSelectedId] = useState("");

  const selectedInvestigation = useMemo(() => {
    if (!selectedId) {
      return investigations[0];
    }

    return investigations.find(
      (investigation) =>
        investigation.id === selectedId,
    );
  }, [investigations, selectedId]);

  if (isLoading) {
    return (
      <Layout title="AI Investigation">
        <div className="flex min-h-64 items-center justify-center rounded-2xl border border-white/[0.07] bg-[#0b1222]">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <Loader2 className="h-4 w-4 animate-spin" />
            Loading investigation intelligence...
          </div>
        </div>
      </Layout>
    );
  }

  if (!selectedInvestigation) {
    return (
      <Layout title="AI Investigation">
        <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-8 text-center">
          <Target className="mx-auto h-8 w-8 text-slate-600" />

          <h2 className="mt-4 text-lg font-semibold text-white">
            No investigations available
          </h2>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
            Run an investigation first. SKYNEX will generate
            investigation reasoning from its security analysis.
          </p>

          <Link
            to="/app/investigations/new"
            className="mt-5 inline-flex h-10 items-center gap-2 rounded-xl bg-blue-500 px-4 text-sm font-semibold text-white transition hover:bg-blue-400"
          >
            Start Investigation
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </Layout>
    );
  }

  const reasoning =
    selectedInvestigation.reasoning;

  return (
    <Layout title="AI Investigation">
      <section className="space-y-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
            Security intelligence
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
            Investigation Intelligence
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
            Review structured security reasoning generated from the
            investigation's attack-path, blast-radius and risk analysis.
          </p>
        </div>

        <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="min-w-0">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Investigation
              </p>

              <h2 className="mt-2 text-lg font-semibold text-white">
                {selectedInvestigation.name}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {selectedInvestigation.provider} ·{" "}
                {selectedInvestigation.environment} ·{" "}
                {selectedInvestigation.type}
              </p>
            </div>

            <select
              value={selectedInvestigation.id}
              onChange={(event) =>
                setSelectedId(event.target.value)
              }
              className="h-10 rounded-xl border border-white/[0.08] bg-white/[0.03] px-3 text-sm text-slate-300 outline-none focus:border-blue-400/40"
            >
              {investigations.map(
                (investigation) => (
                  <option
                    key={investigation.id}
                    value={investigation.id}
                    className="bg-slate-900"
                  >
                    {investigation.name}
                  </option>
                ),
              )}
            </select>
          </div>
        </section>

        <div className="grid gap-4 md:grid-cols-3">
          <InsightMetric
            label="Risk score"
            value={String(
              selectedInvestigation.riskScore,
            )}
            detail={`${selectedInvestigation.risk} severity`}
          />

          <InsightMetric
            label="Attack paths"
            value={String(
              selectedInvestigation.attackPaths,
            )}
            detail="Discovered paths"
          />

          <InsightMetric
            label="Affected resources"
            value={String(
              selectedInvestigation.blastRadiusAnalysis
                ?.affectedResourceCount ?? 0,
            )}
            detail="Blast-radius impact"
          />
        </div>

        <section className="rounded-2xl border border-blue-400/10 bg-gradient-to-br from-blue-500/[0.08] to-violet-500/[0.05] p-6">
          <div className="flex items-start gap-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10">
              <Lightbulb className="h-5 w-5 text-blue-300" />
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-semibold text-white">
                  Security reasoning
                </h2>

                <span
                  className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase ${
                    severityClasses[
                      reasoning?.severity ??
                        selectedInvestigation.risk
                    ] ??
                    severityClasses.Medium
                  }`}
                >
                  {reasoning?.severity ??
                    selectedInvestigation.risk}
                </span>
              </div>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                {reasoning
                  ? "SKYNEX generated this assessment from structured security analysis."
                  : "No reasoning data was returned for this investigation."}
              </p>
            </div>
          </div>
        </section>

        <div className="grid gap-6 xl:grid-cols-2">
          <InsightList
            title="Key findings"
            description="Security evidence identified during analysis."
            items={reasoning?.findings ?? []}
            icon={
              <ShieldAlert className="h-4 w-4 text-orange-400" />
            }
            emptyText="No findings were returned."
          />

          <InsightList
            title="Recommended actions"
            description="Engineering actions suggested by the analysis."
            items={reasoning?.recommendations ?? []}
            icon={
              <CheckCircle2 className="h-4 w-4 text-emerald-400" />
            }
            emptyText="No recommendations were returned."
          />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <ContextPanel
            title="Attack-path context"
            icon={
              <Target className="h-4 w-4 text-rose-400" />
            }
          >
            {selectedInvestigation.attackPathAnalysis ? (
              <div className="space-y-3">
                <ContextValue
                  label="Source"
                  value={
                    selectedInvestigation
                      .attackPathAnalysis.source
                  }
                />

                <ContextValue
                  label="Target"
                  value={
                    selectedInvestigation
                      .attackPathAnalysis.target
                  }
                />

                <ContextValue
                  label="Risk"
                  value={
                    selectedInvestigation
                      .attackPathAnalysis.risk
                  }
                />

                <ContextValue
                  label="Path"
                  value={selectedInvestigation.attackPathAnalysis.nodes.join(
                    " → ",
                  )}
                />

                <p className="text-sm leading-6 text-slate-400">
                  {
                    selectedInvestigation
                      .attackPathAnalysis.description
                  }
                </p>
              </div>
            ) : (
              <EmptyState text="No attack-path analysis is available." />
            )}
          </ContextPanel>

          <ContextPanel
            title="Blast-radius context"
            icon={
              <AlertTriangle className="h-4 w-4 text-amber-400" />
            }
          >
            {selectedInvestigation.blastRadiusAnalysis ? (
              <div className="space-y-4">
                <ContextValue
                  label="Compromised resource"
                  value={
                    selectedInvestigation
                      .blastRadiusAnalysis
                      .compromisedResource
                  }
                />

                <div className="grid grid-cols-2 gap-3">
                  <ContextValue
                    label="Affected"
                    value={String(
                      selectedInvestigation
                        .blastRadiusAnalysis
                        .affectedResourceCount,
                    )}
                  />

                  <ContextValue
                    label="Maximum depth"
                    value={String(
                      selectedInvestigation
                        .blastRadiusAnalysis
                        .maximumDepth,
                    )}
                  />
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-600">
                    Reachable resources
                  </p>

                  <div className="mt-2 space-y-2">
                    {selectedInvestigation
                      .blastRadiusAnalysis
                      .reachableResources.length > 0 ? (
                      selectedInvestigation
                        .blastRadiusAnalysis
                        .reachableResources.map(
                          (resource) => (
                            <div
                              key={resource}
                              className="rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2 text-xs text-slate-300"
                            >
                              {resource}
                            </div>
                          ),
                        )
                    ) : (
                      <EmptyState text="No reachable resources identified." />
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <EmptyState text="No blast-radius analysis is available." />
            )}
          </ContextPanel>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link
            to={`/app/investigations/${selectedInvestigation.id}`}
            className="inline-flex h-10 items-center gap-2 rounded-xl border border-white/[0.08] px-4 text-sm font-medium text-slate-300 transition hover:bg-white/[0.04] hover:text-white"
          >
            Open Investigation Workspace
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>
    </Layout>
  );
}

function InsightMetric({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail: string;
}) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-3 text-3xl font-semibold tracking-tight text-white">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {detail}
      </p>
    </div>
  );
}

function InsightList({
  title,
  description,
  items,
  icon,
  emptyText,
}: {
  title: string;
  description: string;
  items: string[];
  icon: React.ReactNode;
  emptyText: string;
}) {
  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
      <div className="flex items-start gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white/[0.03]">
          {icon}
        </div>

        <div>
          <h2 className="text-sm font-semibold text-white">
            {title}
          </h2>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            {description}
          </p>
        </div>
      </div>

      {items.length > 0 ? (
        <ul className="mt-5 space-y-2">
          {items.map((item) => (
            <li
              key={item}
              className="rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-3 text-sm leading-6 text-slate-400"
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-5 text-sm text-slate-500">
          {emptyText}
        </p>
      )}
    </section>
  );
}

function ContextPanel({
  title,
  icon,
  children,
}: {
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
      <div className="flex items-center gap-2">
        {icon}

        <h2 className="text-sm font-semibold text-white">
          {title}
        </h2>
      </div>

      <div className="mt-5">
        {children}
      </div>
    </section>
  );
}

function ContextValue({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-3">
      <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-600">
        {label}
      </p>

      <p className="mt-1 break-words text-sm text-slate-300">
        {value}
      </p>
    </div>
  );
}

function EmptyState({ text }: { text: string }) {
  return (
    <p className="text-sm leading-6 text-slate-500">
      {text}
    </p>
  );
}
