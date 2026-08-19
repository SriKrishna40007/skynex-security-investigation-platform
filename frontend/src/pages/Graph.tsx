import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  Box,
  GitBranch,
  Loader2,
  ShieldCheck,
} from "lucide-react";

import { useAuth } from "@/auth/useAuth";
import {
  getInvestigation,
  listInvestigations,
} from "@/api/investigations/investigationApi";
import type {
  InvestigationHistoryResponse,
  InvestigationResponse,
} from "@/api/investigations/investigationTypes";

import Layout from "../components/layout/Layout";

type GraphPath = {
  investigation: InvestigationHistoryResponse;
  analysis: NonNullable<
    InvestigationResponse["attack_path_analysis"]
  >;
};

export default function Graph() {
  const { state: authState } = useAuth();
  const accessToken = authState.session?.accessToken;

  const [paths, setPaths] = useState<GraphPath[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadGraphData() {
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
            const detail = await getInvestigation(
              accessToken,
              investigation.id,
            );

            if (!detail.attack_path_analysis) {
              return null;
            }

            return {
              investigation,
              analysis: detail.attack_path_analysis,
            };
          }),
        );

        if (!cancelled) {
          setPaths(
            results.filter(
              (result): result is GraphPath => result !== null,
            ),
          );
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load infrastructure graph.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadGraphData();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  const selectedPath = paths[selectedIndex];

  const graphNodes = useMemo(() => {
    if (!selectedPath) {
      return [];
    }

    return selectedPath.analysis.nodes.map((name, index) => ({
      name,
      index,
      x:
        10 +
        index *
          (80 /
            Math.max(
              selectedPath.analysis.nodes.length - 1,
              1,
            )),
      y: 50,
    }));
  }, [selectedPath]);

  return (
    <Layout title="Infrastructure Graph">
      <section className="space-y-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
            Security topology
          </p>

          <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white">
            Infrastructure Graph
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Explore the security relationships discovered by SKYNEX during
            investigation traversal.
          </p>
        </div>

        {isLoading && (
          <div className="flex min-h-64 items-center justify-center rounded-2xl border border-white/[0.07] bg-[#0b1222]">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading security graph...
            </div>
          </div>
        )}

        {!isLoading && error && (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-400/[0.06] p-5">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-rose-400" />

              <div>
                <h2 className="text-sm font-semibold text-white">
                  Unable to load graph
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
              No graph data available
            </h2>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
              Run an investigation with an established attack path to
              visualize its discovered security topology.
            </p>
          </div>
        )}

        {!isLoading && !error && selectedPath && (
          <>
            {paths.length > 1 && (
              <div className="flex flex-wrap gap-2">
                {paths.map((path, index) => (
                  <button
                    key={path.investigation.id}
                    type="button"
                    onClick={() => setSelectedIndex(index)}
                    className={`rounded-xl border px-3 py-2 text-xs transition ${
                      index === selectedIndex
                        ? "border-blue-400/30 bg-blue-400/10 text-blue-300"
                        : "border-white/[0.07] bg-white/[0.02] text-slate-500 hover:text-white"
                    }`}
                  >
                    {path.investigation.id}
                  </button>
                ))}
              </div>
            )}

            <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5">
              <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-start">
                <div>
                  <div className="flex items-center gap-2">
                    <Box className="h-4 w-4 text-blue-400" />

                    <span className="text-xs uppercase tracking-wide text-slate-500">
                      {selectedPath.investigation.investigation_type}
                    </span>
                  </div>

                  <h2 className="mt-2 text-base font-semibold text-white">
                    {selectedPath.analysis.source}
                    <span className="mx-2 text-slate-600">→</span>
                    {selectedPath.analysis.target}
                  </h2>
                </div>

                <div className="flex items-center gap-2">
                  <span className="rounded-full border border-orange-400/20 bg-orange-400/10 px-2.5 py-1 text-[10px] font-semibold uppercase text-orange-300">
                    {selectedPath.analysis.risk}
                  </span>

                  <span className="rounded-full border border-white/[0.08] bg-white/[0.03] px-2.5 py-1 text-[10px] font-semibold uppercase text-slate-400">
                    {selectedPath.analysis.hop_count} hops
                  </span>
                </div>
              </div>

              <div className="relative mt-6 min-h-[320px] overflow-hidden rounded-2xl border border-white/[0.06] bg-slate-950/70">
                <div className="absolute inset-0 opacity-20 [background-image:linear-gradient(rgba(148,163,184,0.12)_1px,transparent_1px),linear-gradient(90deg,rgba(148,163,184,0.12)_1px,transparent_1px)] [background-size:48px_48px]" />

                <div className="absolute left-5 top-5 flex items-center gap-2 text-[10px] uppercase tracking-[0.15em] text-slate-600">
                  <GitBranch className="h-3.5 w-3.5" />
                  Security relationship view
                </div>

                <div className="absolute inset-0">
                  {graphNodes.slice(0, -1).map((node, index) => {
                    const next = graphNodes[index + 1];

                    return (
                      <div
                        key={`edge-${node.name}-${index}`}
                        className="absolute h-px origin-left bg-blue-400/30"
                        style={{
                          left: `${node.x}%`,
                          top: `${node.y}%`,
                          width: `${Math.max(next.x - node.x, 5)}%`,
                          transform: `rotate(${(next.y - node.y) * 0.7}deg)`,
                        }}
                      />
                    );
                  })}

                  {graphNodes.map((node, index) => (
                    <div
                      key={`${node.name}-${index}`}
                      className="absolute -translate-x-1/2 -translate-y-1/2"
                      style={{
                        left: `${node.x}%`,
                        top: `${node.y}%`,
                        transform: "translate(-50%, -50%)",
                      }}
                    >
                      <div
                        className={`flex min-w-32 flex-col items-center rounded-2xl border px-4 py-3 shadow-2xl backdrop-blur ${
                          index === 0
                            ? "border-rose-400/30 bg-rose-400/10"
                            : index === graphNodes.length - 1
                              ? "border-orange-400/30 bg-orange-400/10"
                              : "border-blue-400/20 bg-blue-400/10"
                        }`}
                      >
                        <Box className="h-5 w-5 text-blue-300" />

                        <span className="mt-2 max-w-40 truncate text-xs font-medium text-white">
                          {node.name}
                        </span>

                        <span className="mt-1 text-[9px] uppercase tracking-wide text-slate-500">
                          {index === 0
                            ? "Source"
                            : index === graphNodes.length - 1
                              ? "Target"
                              : `Hop ${index}`}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-5 grid gap-3 sm:grid-cols-3">
                <GraphStat
                  label="Nodes"
                  value={String(selectedPath.analysis.nodes.length)}
                />

                <GraphStat
                  label="Hops"
                  value={String(selectedPath.analysis.hop_count)}
                />

                <GraphStat
                  label="Path established"
                  value={selectedPath.analysis.exists ? "Yes" : "No"}
                />
              </div>

              <p className="mt-5 text-sm leading-6 text-slate-400">
                {selectedPath.analysis.description}
              </p>
            </div>
          </>
        )}
      </section>
    </Layout>
  );
}

function GraphStat({
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

      <p className="mt-1 text-sm font-medium text-slate-300">
        {value}
      </p>
    </div>
  );
}
