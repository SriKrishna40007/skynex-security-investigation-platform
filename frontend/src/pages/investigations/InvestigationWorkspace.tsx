import {
  useEffect,
  useState,
} from "react";

import {
  Activity,
  ArrowLeft,
  Bot,
  GitBranch,
  ShieldAlert,
  ShieldCheck,
  Target,
  Network,
  Lightbulb,
  CheckCircle2,
} from "lucide-react";
import { Link, useParams } from "react-router-dom";

import { useInvestigations } from "@/investigations/useInvestigations";

import type { Investigation } from "@/types/investigation";



const severityClasses: Record<string, string> = {
  Critical: "bg-rose-400/10 text-rose-300 border-rose-400/20",
  High: "bg-orange-400/10 text-orange-300 border-orange-400/20",
};

export default function InvestigationWorkspace() {
  const { id } = useParams();

  const { getById } = useInvestigations();

  const [investigation, setInvestigation] =
    useState<Investigation | undefined>();

  const [isLoading, setIsLoading] =
    useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadInvestigation() {
      if (!id) {
        setInvestigation(undefined);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);

      try {
        const result = await getById(id);

        if (!cancelled) {
          setInvestigation(result);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadInvestigation();

    return () => {
      cancelled = true;
    };
  }, [id, getById]);

  if (isLoading) {
    return (
      <main className="min-h-[70vh] flex items-center justify-center">
        <div className="text-sm text-slate-400">
          Loading investigation...
        </div>
      </main>
    );
  }

  if (!investigation) {
    return (
      <main className="min-h-[70vh] flex items-center justify-center">
        <div className="max-w-md text-center">
          <h1 className="text-2xl font-semibold text-white">
            Investigation not found
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            The investigation you are trying to access does not
            exist or is no longer available.
          </p>

          <Link
            to="/app/investigations"
            className="mt-6 inline-flex h-10 items-center justify-center rounded-xl bg-blue-500 px-4 text-sm font-semibold text-white transition hover:bg-blue-400"
          >
            Back to Investigations
          </Link>
        </div>
      </main>
    );
  }

  return (
    <section className="space-y-6">
      <Link
        to="/app/investigations"
        className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-white"
      >
        <ArrowLeft className="h-4 w-4" />
        Investigations
      </Link>

      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <div className="flex items-center gap-3">
            <span className="rounded-full border border-blue-400/20 bg-blue-400/10 px-2.5 py-1 text-xs font-medium text-blue-300">
              {investigation.status} Investigation
            </span>

            <span className="text-xs text-slate-600">
              {id}
            </span>
          </div>

          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">
            {investigation.name}
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            {investigation.provider} · {investigation.environment} · {investigation.type} · Investigation workspace
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Metric
          label="Risk Score"
          value={String(investigation.riskScore)}
          detail={`${investigation.risk} risk`}
          icon={<ShieldAlert className="h-5 w-5 text-rose-400" />}
        />

        <Metric
          label="Resources"
          value={String(investigation.resources)}
          detail="Analyzed"
          icon={<Activity className="h-5 w-5 text-blue-400" />}
        />

        <Metric
          label="Findings"
          value={String(investigation.findings)}
          detail={`${investigation.findingsList.length} detailed findings`}
          icon={<ShieldCheck className="h-5 w-5 text-orange-400" />}
        />

        <Metric
          label="Attack Paths"
          value={String(investigation.attackPaths)}
          detail="Discovered"
          icon={<GitBranch className="h-5 w-5 text-emerald-400" />}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
        <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222]">
          <div className="border-b border-white/[0.07] px-5 py-4">
            <h2 className="text-sm font-semibold text-white">
              Security findings
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Highest-priority findings discovered during this investigation.
            </p>
          </div>

          <div className="divide-y divide-white/[0.06]">
            {investigation.findingsList.map((finding) => (
              <div key={finding.title} className="px-5 py-5">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-sm font-medium text-white">
                      {finding.title}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {finding.resource}
                    </p>
                  </div>

                  <span
                    className={`shrink-0 rounded-full border px-2 py-1 text-[10px] font-semibold uppercase ${severityClasses[finding.severity]}`}
                  >
                    {finding.severity}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="space-y-6">
          <AnalysisPanel
            title="Risk assessment"
            description="Why SKYNEX assigned this investigation its current risk."
            icon={<ShieldAlert className="h-5 w-5 text-rose-400" />}
          >
            {investigation.riskAssessment ? (
              <>
                <div className="flex items-end gap-3">
                  <span className="text-3xl font-semibold text-white">
                    {investigation.riskAssessment.score}
                  </span>
                  <span className="mb-1 rounded-full border border-rose-400/20 bg-rose-400/10 px-2 py-1 text-[10px] font-semibold uppercase text-rose-300">
                    {investigation.riskAssessment.severity}
                  </span>
                </div>

                <ul className="mt-4 space-y-2">
                  {investigation.riskAssessment.reasons.map((reason) => (
                    <li
                      key={reason}
                      className="flex gap-2 text-sm leading-6 text-slate-400"
                    >
                      <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-rose-400" />
                      {reason}
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <EmptyAnalysis text="Risk assessment details are not available." />
            )}
          </AnalysisPanel>

          <AnalysisPanel
            title="Attack path"
            description="Security traversal from the selected source to target."
            icon={<GitBranch className="h-5 w-5 text-emerald-400" />}
          >
            {investigation.attackPathAnalysis ? (
              <>
                <div className="grid gap-3 sm:grid-cols-2">
                  <AnalysisValue
                    label="Source"
                    value={investigation.attackPathAnalysis.source}
                  />
                  <AnalysisValue
                    label="Target"
                    value={investigation.attackPathAnalysis.target}
                  />
                </div>

                <div className="mt-4 rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">
                  <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-slate-500">
                    <Target className="h-3.5 w-3.5" />
                    Traversal
                  </div>

                  <div className="mt-3 flex flex-wrap items-center gap-2">
                    {investigation.attackPathAnalysis.nodes.map(
                      (node, index) => (
                        <div
                          key={`${node}-${index}`}
                          className="flex items-center gap-2"
                        >
                          <span className="rounded-lg border border-white/[0.08] bg-white/[0.03] px-3 py-2 text-xs text-slate-300">
                            {node}
                          </span>
                          {index <
                            (investigation.attackPathAnalysis?.nodes.length ?? 0) - 1 && (
                            <span className="text-slate-600">
                              {"->"}
                            </span>
                          )}
                        </div>
                      ),
                    )}
                  </div>
                </div>

                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <AnalysisValue
                    label="Exists"
                    value={
                      investigation.attackPathAnalysis.exists ? "Yes" : "No"
                    }
                  />
                  <AnalysisValue
                    label="Hops"
                    value={String(investigation.attackPathAnalysis.hopCount)}
                  />
                  <AnalysisValue
                    label="Risk"
                    value={investigation.attackPathAnalysis.risk}
                  />
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-400">
                  {investigation.attackPathAnalysis.description}
                </p>
              </>
            ) : (
              <EmptyAnalysis text="Attack-path analysis is not available." />
            )}
          </AnalysisPanel>
        </div>

        <div className="space-y-6">
          <AnalysisPanel
            title="Blast radius"
            description="Resources reachable from a compromised resource."
            icon={<Network className="h-5 w-5 text-orange-400" />}
          >
            {investigation.blastRadiusAnalysis ? (
              <>
                <AnalysisValue
                  label="Compromised resource"
                  value={
                    investigation.blastRadiusAnalysis.compromisedResource
                  }
                />

                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  <AnalysisValue
                    label="Affected resources"
                    value={String(
                      investigation.blastRadiusAnalysis.affectedResourceCount,
                    )}
                  />
                  <AnalysisValue
                    label="Maximum depth"
                    value={String(
                      investigation.blastRadiusAnalysis.maximumDepth,
                    )}
                  />
                </div>

                <div className="mt-4">
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Reachable resources
                  </p>

                  <div className="mt-2 space-y-2">
                    {investigation.blastRadiusAnalysis.reachableResources.length > 0 ? (
                      investigation.blastRadiusAnalysis.reachableResources.map(
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
                      <p className="text-sm text-slate-500">
                        No reachable resources identified.
                      </p>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <EmptyAnalysis text="Blast-radius analysis is not available." />
            )}
          </AnalysisPanel>

          <AnalysisPanel
            title="Remediation guidance"
            description="Concrete remediation actions derived from the investigation findings."
            icon={<ShieldCheck className="h-5 w-5 text-emerald-400" />}
          >
            {investigation.remediations.length > 0 ? (
              <div className="space-y-4">
                {investigation.remediations.map((remediation) => (
                  <article
                    key={remediation.findingId}
                    className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4"
                  >
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                      <div className="min-w-0">
                        <h3 className="text-sm font-medium text-white">
                          {remediation.title}
                        </h3>

                        <p className="mt-1 text-xs text-slate-500">
                          Resource: {remediation.resourceId}
                        </p>
                      </div>

                      <div className="flex shrink-0 items-center gap-2">
                        <span className="rounded-full border border-orange-400/20 bg-orange-400/10 px-2 py-1 text-[10px] font-semibold uppercase text-orange-300">
                          {remediation.severity}
                        </span>

                        <span
                          className={`rounded-full border px-2 py-1 text-[10px] font-semibold uppercase ${
                            remediation.executable
                              ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-300"
                              : "border-slate-400/20 bg-slate-400/10 text-slate-400"
                          }`}
                        >
                          {remediation.executable
                            ? "Executable"
                            : "Guidance"}
                        </span>
                      </div>
                    </div>

                    <div className="mt-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">
                        Recommended steps
                      </p>

                      <ol className="mt-3 space-y-2">
                        {remediation.steps.map((step, index) => (
                          <li
                            key={`${remediation.findingId}-${index}`}
                            className="flex gap-3 text-sm leading-6 text-slate-300"
                          >
                            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-white/[0.08] bg-white/[0.03] text-[10px] font-semibold text-slate-400">
                              {index + 1}
                            </span>

                            <span>{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <EmptyAnalysis text="No remediation guidance is available for this investigation." />
            )}
          </AnalysisPanel>

          <AnalysisPanel
            title="Investigation reasoning"
            description="Security findings and recommended engineering actions."
            icon={<Lightbulb className="h-5 w-5 text-blue-400" />}
          >
            {investigation.reasoning ? (
              <div className="space-y-5">
                <ReasoningList
                  title="Findings"
                  items={investigation.reasoning.findings}
                  icon={<ShieldAlert className="h-4 w-4 text-orange-400" />}
                />

                <ReasoningList
                  title="Recommendations"
                  items={investigation.reasoning.recommendations}
                  icon={
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  }
                />
              </div>
            ) : (
              <EmptyAnalysis text="Investigation reasoning is not available." />
            )}
          </AnalysisPanel>
        </div>

        <section className="rounded-2xl border border-blue-400/10 bg-gradient-to-br from-blue-500/[0.08] to-violet-500/[0.05] p-5">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10">
            <Bot className="h-5 w-5 text-blue-300" />
          </div>

          <h2 className="mt-5 text-lg font-semibold text-white">
            AI Investigation
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Ask SKYNEX to explain findings, prioritize remediation and
            investigate relationships across your environment.
          </p>

          <Link
            to="/app/ai-investigation"
            className="mt-5 inline-flex items-center gap-2 text-sm font-medium text-blue-300 hover:text-blue-200"
          >
            Open AI Investigation
            <span>→</span>
          </Link>
        </section>
      </div>
    </section>
  );
}

function AnalysisPanel({
  title,
  description,
  icon,
  children,
}: {
  title: string;
  description: string;
  icon: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
      <div className="flex items-start gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white/[0.03]">
          {icon}
        </div>

        <div>
          <h2 className="text-sm font-semibold text-white">{title}</h2>
          <p className="mt-1 text-xs leading-5 text-slate-500">
            {description}
          </p>
        </div>
      </div>

      <div className="mt-5">{children}</div>
    </section>
  );
}

function AnalysisValue({
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
      <p className="mt-1 break-words text-sm text-slate-300">{value}</p>
    </div>
  );
}

function EmptyAnalysis({ text }: { text: string }) {
  return <p className="text-sm leading-6 text-slate-500">{text}</p>;
}

function ReasoningList({
  title,
  items,
  icon,
}: {
  title: string;
  items: string[];
  icon: React.ReactNode;
}) {
  return (
    <div>
      <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-slate-500">
        {icon}
        {title}
      </div>

      {items.length > 0 ? (
        <ul className="mt-3 space-y-2">
          {items.map((item) => (
            <li
              key={item}
              className="rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2 text-sm leading-6 text-slate-400"
            >
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-3 text-sm text-slate-500">
          No {title.toLowerCase()} were returned.
        </p>
      )}
    </div>
  );
}

function Metric({
  label,
  value,
  detail,
  icon,
}: {
  label: string;
  value: string;
  detail: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
      <div className="flex items-center justify-between">
        <p className="text-xs text-slate-500">{label}</p>
        {icon}
      </div>

      <p className="mt-4 text-3xl font-semibold tracking-tight text-white">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">{detail}</p>
    </div>
  );
}
