import { useEffect, useState } from "react";
import {
  AlertTriangle,
  ArrowRight,
  GitBranch,
  Loader2,
  ShieldCheck,
} from "lucide-react";

import Layout from "@/components/layout/Layout";
import { useAuth } from "@/auth/useAuth";
import {
  getInvestigation,
  listInvestigations,
} from "@/api/investigations/investigationApi";
import type {
  InvestigationHistoryResponse,
  InvestigationResponse,
} from "@/api/investigations/investigationTypes";

type AttackPathRecord = {
  investigation: InvestigationHistoryResponse;
  analysis: NonNullable<
    InvestigationResponse["attack_path_analysis"]
  >;
};

export default function AttackPaths() {
  const { state: authState } = useAuth();
  const accessToken = authState.session?.accessToken;

  const [paths, setPaths] = useState<AttackPathRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadAttackPaths() {
      if (!accessToken) {
        setPaths([]);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const history = await listInvestigations(accessToken, {
          page: 1,
          size: 50,
          sort_by: "created_at",
          descending: true,
        });

        const results = await Promise.all(
          history.items.map(async (investigation) => {
            try {
              const detail = await getInvestigation(
                accessToken,
                investigation.id,
              );

              const analysis = detail.attack_path_analysis;

              if (!analysis || !analysis.exists) {
                return null;
              }

              return {
                investigation,
                analysis,
              };
            } catch {
              return null;
            }
          }),
        );

        if (!cancelled) {
          setPaths(
            results.filter(
              (result): result is AttackPathRecord => result !== null,
            ),
          );
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load attack paths.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadAttackPaths();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  return (
    <Layout title="Attack Paths">
      <section className="space-y-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
            Security traversal
          </p>

          <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white">
            Attack Paths
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Review discovered paths between exposed resources and security
            targets across completed investigations.
          </p>
        </div>

        {isLoading && (
          <div className="flex min-h-48 items-center justify-center rounded-2xl border border-white/[0.07] bg-[#0b1222]">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading attack paths...
            </div>
          </div>
        )}

        {!isLoading && error && (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-400/[0.06] p-5">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-rose-400" />

              <div>
                <h2 className="text-sm font-semibold text-white">
                  Unable to load attack paths
                </h2>

                <p className="mt-1 text-sm leading-6 text-slate-400">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {!isLoading && !error && paths.length === 0 && (
          <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-8 text-center">
            <ShieldCheck className="mx-auto h-8 w-8 text-emerald-400" />

            <h2 className="mt-4 text-lg font-semibold text-white">
              No attack paths discovered
            </h2>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
              Completed investigations have not returned an established
              attack path.
            </p>
          </div>
        )}

        {!isLoading && !error && paths.length > 0 && (
          <div className="space-y-4">
            {paths.map(({ investigation, analysis }) => (
              <article
                key={`${investigation.id}-${analysis.source}-${analysis.target}`}
                className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5"
              >
                <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-start">
                  <div>
                    <div className="flex items-center gap-2">
                      <GitBranch className="h-4 w-4 text-emerald-400" />

                      <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                        {investigation.investigation_type}
                      </span>
                    </div>

                    <h2 className="mt-2 text-base font-semibold text-white">
                      {analysis.source}
                      <span className="mx-2 text-slate-600">→</span>
                      {analysis.target}
                    </h2>

                    <p className="mt-1 text-xs text-slate-500">
                      Investigation {investigation.id}
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="rounded-full border border-orange-400/20 bg-orange-400/10 px-2.5 py-1 text-[10px] font-semibold uppercase text-orange-300">
                      {analysis.risk}
                    </span>

                    <span className="rounded-full border border-white/[0.08] bg-white/[0.03] px-2.5 py-1 text-[10px] font-semibold uppercase text-slate-400">
                      {analysis.hop_count} hops
                    </span>
                  </div>
                </div>

                <div className="mt-5 overflow-x-auto">
                  <div className="flex min-w-max items-center gap-2">
                    {analysis.nodes.map((node, index) => (
                      <div
                        key={`${node}-${index}`}
                        className="flex items-center gap-2"
                      >
                        <span className="rounded-xl border border-white/[0.08] bg-white/[0.03] px-3 py-2 text-xs text-slate-300">
                          {node}
                        </span>

                        {index < analysis.nodes.length - 1 && (
                          <ArrowRight className="h-4 w-4 shrink-0 text-slate-600" />
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                <p className="mt-5 text-sm leading-6 text-slate-400">
                  {analysis.description}
                </p>
              </article>
            ))}
          </div>
        )}
      </section>
    </Layout>
  );
}
