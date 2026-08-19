import { useEffect, useState } from "react";
import {
  AlertTriangle,
  Download,
  FileText,
  Loader2,
  ShieldAlert,
  ShieldCheck,
} from "lucide-react";

import { useAuth } from "@/auth/useAuth";
import {
  exportInvestigation,
  listInvestigations,
} from "@/api/investigations/investigationApi";
import type {
  InvestigationHistoryResponse,
} from "@/api/investigations/investigationTypes";

import Layout from "../components/layout/Layout";

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

export default function Reports() {
  const { state: authState } = useAuth();
  const accessToken = authState.session?.accessToken;

  const [reports, setReports] = useState<
    InvestigationHistoryResponse[]
  >([]);
  const [isLoading, setIsLoading] = useState(true);
  const [exportingId, setExportingId] = useState<string | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadReports() {
      if (!accessToken) {
        setReports([]);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        const response = await listInvestigations(accessToken, {
          page: 1,
          size: 50,
          sort_by: "created_at",
          descending: true,
        });

        if (!cancelled) {
          setReports(response.items);
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load reports.",
          );
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadReports();

    return () => {
      cancelled = true;
    };
  }, [accessToken]);

  async function handleExport(id: string) {
    if (!accessToken) {
      return;
    }

    setExportingId(id);
    setError(null);

    try {
      const report = await exportInvestigation(
        accessToken,
        id,
        "json",
      );

      const blob = new Blob(
        [JSON.stringify(report, null, 2)],
        {
          type: "application/json",
        },
      );

      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");

      anchor.href = url;
      anchor.download = `skynex-investigation-${id}.json`;

      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();

      URL.revokeObjectURL(url);
    } catch (exportError) {
      setError(
        exportError instanceof Error
          ? exportError.message
          : "Unable to export investigation report.",
      );
    } finally {
      setExportingId(null);
    }
  }

  return (
    <Layout title="Reports">
      <section className="space-y-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
            Investigation reporting
          </p>

          <h1 className="mt-2 text-2xl font-semibold tracking-tight text-white">
            Reports
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Review completed investigation reports and export security
            evidence for engineering and security workflows.
          </p>
        </div>

        {error && (
          <div className="rounded-2xl border border-rose-400/20 bg-rose-400/[0.06] p-5">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 text-rose-400" />

              <div>
                <h2 className="text-sm font-semibold text-white">
                  Report operation failed
                </h2>

                <p className="mt-1 text-sm leading-6 text-slate-400">
                  {error}
                </p>
              </div>
            </div>
          </div>
        )}

        {isLoading && (
          <div className="flex min-h-48 items-center justify-center rounded-2xl border border-white/[0.07] bg-[#0b1222]">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <Loader2 className="h-4 w-4 animate-spin" />
              Loading reports...
            </div>
          </div>
        )}

        {!isLoading && reports.length === 0 && !error && (
          <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-8 text-center">
            <FileText className="mx-auto h-8 w-8 text-slate-600" />

            <h2 className="mt-4 text-lg font-semibold text-white">
              No reports available
            </h2>

            <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
              Completed investigations will appear here when report
              data is available.
            </p>
          </div>
        )}

        {!isLoading && reports.length > 0 && (
          <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0b1222]">
            <div className="border-b border-white/[0.07] px-5 py-4">
              <h2 className="text-sm font-semibold text-white">
                Investigation reports
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                {reports.length} available investigation reports
              </p>
            </div>

            <div className="divide-y divide-white/[0.06]">
              {reports.map((report) => (
                <div
                  key={report.id}
                  className="flex flex-col gap-4 px-5 py-5 lg:flex-row lg:items-center lg:justify-between"
                >
                  <div className="flex min-w-0 items-start gap-4">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-400/10">
                      {report.severity === "Critical" ||
                      report.severity === "High" ? (
                        <ShieldAlert className="h-5 w-5 text-orange-400" />
                      ) : (
                        <ShieldCheck className="h-5 w-5 text-emerald-400" />
                      )}
                    </div>

                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <h3 className="font-medium text-white">
                          Investigation {report.id}
                        </h3>

                        <span
                          className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase ${severityClasses[report.severity] ?? "border-white/[0.08] bg-white/[0.03] text-slate-400"}`}
                        >
                          {report.severity}
                        </span>
                      </div>

                      <p className="mt-1 text-sm text-slate-500">
                        {report.investigation_type}
                      </p>

                      <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                        {report.summary}
                      </p>

                      <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-600">
                        <span>
                          Risk score: {report.risk_score}
                        </span>

                        <span>
                          Status: {report.status}
                        </span>

                        <span>
                          {new Date(
                            report.created_at,
                          ).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => void handleExport(report.id)}
                    disabled={exportingId === report.id}
                    className="inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.02] px-4 text-sm font-medium text-slate-300 transition hover:bg-white/[0.05] hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {exportingId === report.id ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Download className="h-4 w-4" />
                    )}

                    {exportingId === report.id
                      ? "Exporting..."
                      : "Export JSON"}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </section>
    </Layout>
  );
}
