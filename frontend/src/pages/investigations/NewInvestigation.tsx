import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  FileCode2,
  ShieldCheck,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useInvestigations } from "@/investigations/useInvestigations";

export default function NewInvestigation() {
  const navigate = useNavigate();
  const { createAndStart } = useInvestigations();

  const [file, setFile] = useState<File | null>(null);
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isValid =
    file !== null &&
    source.trim().length > 0 &&
    target.trim().length > 0;

  async function handleStart() {
    if (!isValid || !file) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const investigation = await createAndStart({
        name: `${file.name} Investigation`,
        provider: "AWS",
        environment: "Production",
        type: "Terraform",
        terraformFile: file,
        source: source.trim(),
        target: target.trim(),
      });

      navigate(`/app/investigations/${investigation.id}`);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Investigation execution failed.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="space-y-6">
      <Link
        to="/app/investigations"
        className="inline-flex items-center gap-2 text-sm text-slate-400 transition hover:text-white"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Investigations
      </Link>

      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-400">
          Security Investigation
        </p>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
          New Terraform Investigation
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Upload Terraform infrastructure and define the topology
          endpoints SKYNEX should investigate.
        </p>
      </div>

      <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <div className="mb-6 flex items-start gap-4">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10">
            <ShieldCheck className="h-5 w-5 text-blue-400" />
          </div>

          <div>
            <h2 className="text-sm font-semibold text-white">
              Terraform investigation
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              SKYNEX will parse, correlate, analyze, score, and
              persist the investigation.
            </p>
          </div>
        </div>

        <div className="grid gap-5 md:grid-cols-2">
          <label className="block md:col-span-2">
            <span className="text-sm font-medium text-slate-300">
              Terraform file
            </span>

            <div className="mt-2 rounded-xl border border-dashed border-white/[0.12] bg-white/[0.02] p-5">
              <div className="flex items-center gap-3">
                <FileCode2 className="h-5 w-5 text-blue-400" />

                <input
                  type="file"
                  accept=".tf,.tf.json"
                  onChange={(event) =>
                    setFile(event.target.files?.[0] ?? null)
                  }
                  className="block w-full text-sm text-slate-400 file:mr-4 file:rounded-lg file:border-0 file:bg-blue-500/10 file:px-3 file:py-2 file:text-sm file:font-medium file:text-blue-300"
                />
              </div>

              {file && (
                <p className="mt-3 text-xs text-slate-500">
                  Selected: {file.name}
                </p>
              )}
            </div>
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-300">
              Source resource
            </span>

            <input
              type="text"
              value={source}
              onChange={(event) => setSource(event.target.value)}
              placeholder="e.g. aws_instance.web"
              className="mt-2 h-11 w-full rounded-xl border border-white/[0.08] bg-white/[0.02] px-3 text-sm text-white outline-none transition focus:border-blue-400/50"
            />

            <span className="mt-2 block text-xs text-slate-500">
              Starting point for attack-path analysis.
            </span>
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-300">
              Target resource
            </span>

            <input
              type="text"
              value={target}
              onChange={(event) => setTarget(event.target.value)}
              placeholder="e.g. aws_s3_bucket.data"
              className="mt-2 h-11 w-full rounded-xl border border-white/[0.08] bg-white/[0.02] px-3 text-sm text-white outline-none transition focus:border-blue-400/50"
            />

            <span className="mt-2 block text-xs text-slate-500">
              Destination resource to investigate.
            </span>
          </label>
        </div>

        {error && (
          <div className="mt-5 rounded-xl border border-rose-400/20 bg-rose-400/5 px-4 py-3 text-sm text-rose-300">
            {error}
          </div>
        )}

        <div className="mt-6 flex flex-col-reverse justify-end gap-3 border-t border-white/[0.07] pt-6 sm:flex-row">
          <Link
            to="/app/investigations"
            className="inline-flex h-10 items-center justify-center rounded-xl border border-white/[0.08] px-4 text-sm font-medium text-slate-300 transition hover:bg-white/[0.04]"
          >
            Cancel
          </Link>

          <button
            type="button"
            onClick={handleStart}
            disabled={!isValid || isSubmitting}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-5 text-sm font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isSubmitting
              ? "Running Investigation..."
              : "Start Investigation"}

            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </section>
  );
}
