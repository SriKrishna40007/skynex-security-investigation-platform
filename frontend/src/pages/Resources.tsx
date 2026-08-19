import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  Box,
  Loader2,
  ShieldAlert,
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

type InvestigationResourceData = {
  investigation: InvestigationHistoryResponse;
  detail: InvestigationResponse;
};

type ResourceRecord = {
  id: string;
  role: "Source" | "Target" | "Reachable";
  investigationId: string;
  investigationType: string;
};

export default function Resources() {
  const { state: authState } = useAuth();
  const accessToken = authState.session?.accessToken;

  const [investigations, setInvestigations] = useState<
    InvestigationResourceData[]
  >([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadResources() {
      if (!accessToken) {
        setInvestigations([]);
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
          history.items.map(async (investigation) => ({
            investigation,
            detail: await getInvestigation(
              accessToken,
              investigation.id,
            ),
          })),
        );

        if (!cancelled) {
          setInvestigations(results);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load resources.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadResources();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  const resources = useMemo<ResourceRecord[]>(() => {
    const records = new Map<string, ResourceRecord>();

    for (const { investigation, detail } of investigations) {
      const attackPath = detail.attack_path_analysis;

      if (attackPath) {
        attackPath.nodes.forEach((node, index) => {
          const role =
            index === 0
              ? "Source"
              : index === attackPath.nodes.length - 1
                ? "Target"
                : "Reachable";

          records.set(`${investigation.id}:${node}`, {
            id: node,
            role,
            investigationId: investigation.id,
            investigationType: investigation.investigation_type,
          });
        });
      }

      const blastRadius = detail.blast_radius_analysis;

      if (blastRadius) {
        records.set(
          `${investigation.id}:${blastRadius.compromised_resource}`,
          {
            id: blastRadius.compromised_resource,
            role: "Source",
            investigationId: investigation.id,
            investigationType: investigation.investigation_type,
          },
        );

        blastRadius.reachable_resources.forEach((resource) => {
          const key = `${investigation.id}:${resource}`;

          if (!records.has(key)) {
            records.set(key, {
              id: resource,
              role: "Reachable",
              investigationId: investigation.id,
              investigationType: investigation.investigation_type,
            });
          }
        });
      }
    }

    return Array.from(records.values());
  }, [investigations]);

  const sourceCount = resources.filter(
    (resource) => resource.role === "Source",
  ).length;

  const targetCount = resources.filter(
    (resource) => resource.role === "Target",
  ).length;

  return (
    <Layout title="Resources">
      <section className="space-y-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
            Security inventory
          </p>

          <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white">
            Resources
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Resources observed during SKYNEX investigation traversal,
            including attack-path and blast-radius relationships.
          </p>
        </div>

        {isLoading && (
          <div className="flex min-h-48 items-center justify-center rounded-2xl border border-white/[0.07] bg-[#0b1222]">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading resources...
            </div>
          </div>
        )}

        {!isLoading && error && (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-400/[0.06] p-5">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-rose-400" />

              <div>
                <h2 className="text-sm font-semibold text-white">
                  Unable to load resources
                </h2>

                <p className="mt-1 text-sm leading-6 text-slate-400">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {!isLoading && !error && (
          <>
            <div className="grid gap-4 md:grid-cols-3">
              <ResourceMetric
                label="Observed Resources"
                value={String(resources.length)}
                icon={<Box className="h-5 w-5 text-blue-400" />}
              />

              <ResourceMetric
                label="Source Resources"
                value={String(sourceCount)}
                icon={<ShieldAlert className="h-5 w-5 text-rose-400" />}
              />

              <ResourceMetric
                label="Target Resources"
                value={String(targetCount)}
                icon={<ShieldCheck className="h-5 w-5 text-emerald-400" />}
              />
            </div>

            {resources.length === 0 ? (
              <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-8 text-center">
                <Box className="mx-auto h-8 w-8 text-slate-600" />

                <h2 className="mt-4 text-lg font-semibold text-white">
                  No observed resources
                </h2>

                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
                  Run an investigation to populate the security resource
                  inventory.
                </p>
              </div>
            ) : (
              <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0b1222]">
                <div className="border-b border-white/[0.07] px-5 py-4">
                  <h2 className="text-sm font-semibold text-white">
                    Observed resource inventory
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    Derived from investigation attack-path and blast-radius
                    evidence.
                  </p>
                </div>

                <div className="divide-y divide-white/[0.06]">
                  {resources.map((resource) => (
                    <div
                      key={`${resource.investigationId}:${resource.id}`}
                      className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
                    >
                      <div className="flex min-w-0 items-center gap-3">
                        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-400/10">
                          <Box className="h-4 w-4 text-blue-300" />
                        </div>

                        <div className="min-w-0">
                          <p className="truncate text-sm font-medium text-white">
                            {resource.id}
                          </p>

                          <p className="mt-1 text-xs text-slate-600">
                            Investigation {resource.investigationId} ·{" "}
                            {resource.investigationType}
                          </p>
                        </div>
                      </div>

                      <span
                        className={`w-fit rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase ${
                          resource.role === "Source"
                            ? "border-rose-400/20 bg-rose-400/10 text-rose-300"
                            : resource.role === "Target"
                              ? "border-orange-400/20 bg-orange-400/10 text-orange-300"
                              : "border-blue-400/20 bg-blue-400/10 text-blue-300"
                        }`}
                      >
                        {resource.role}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </section>
    </Layout>
  );
}

function ResourceMetric({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
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
    </div>
  );
}
