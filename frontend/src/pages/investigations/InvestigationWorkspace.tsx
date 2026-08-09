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
