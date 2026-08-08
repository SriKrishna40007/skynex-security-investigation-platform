import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Cloud,
  ShieldCheck,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

import { useInvestigations } from "@/investigations/useInvestigations";





import type {
  CloudProvider,
  InvestigationEnvironment,
  InvestigationType,
} from "@/types/investigation";

export default function NewInvestigation() {
  const navigate = useNavigate();

  const { createAndStart } = useInvestigations();


  const [name, setName] = useState(
    "Production Cloud Security Review",
  );

  const [provider, setProvider] =
    useState<CloudProvider>("AWS");

  const [environment, setEnvironment] =
    useState<InvestigationEnvironment>(
      "Production",
    );

  const [type, setType] =
    useState<InvestigationType>(
      "Cloud Security",
    );

  const isValid = name.trim().length >= 3;

  function handleStart() {
    if (!isValid) {
      return;
    }

    const started = createAndStart({
      name: name.trim(),
      provider,
      environment,
      type,
    });

    if (!started) {
      return;
    }

    navigate(
      `/app/investigations/${started.id}`,
    );
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
          Investigation Setup
        </p>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
          New Investigation
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Define the investigation scope before SKYNEX analyzes
          your infrastructure.
        </p>
      </div>

      <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <div className="mb-6 flex items-start gap-4">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10">
            <ShieldCheck className="h-5 w-5 text-blue-400" />
          </div>

          <div>
            <h2 className="text-sm font-semibold text-white">
              Investigation configuration
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              These fields define the initial investigation context.
            </p>
          </div>
        </div>

        <div className="grid gap-5 md:grid-cols-2">
          <label className="block md:col-span-2">
            <span className="text-sm font-medium text-slate-300">
              Investigation name
            </span>

            <input
              type="text"
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
              placeholder="Production Cloud Security Review"
              className="mt-2 h-11 w-full rounded-xl border border-white/[0.08] bg-white/[0.02] px-3 text-sm text-white outline-none transition focus:border-blue-400/50"
            />

            {!isValid && (
              <span className="mt-2 block text-xs text-rose-400">
                Investigation name must contain at least 3 characters.
              </span>
            )}
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-300">
              Cloud provider
            </span>

            <div className="relative mt-2">
              <Cloud className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />

              <select
                value={provider}
                onChange={(event) =>
                  setProvider(
                    event.target.value as CloudProvider,
                  )
                }
                className="h-11 w-full appearance-none rounded-xl border border-white/[0.08] bg-[#0b1222] pl-10 pr-3 text-sm text-white outline-none focus:border-blue-400/50"
              >
                <option>AWS</option>
                <option>Microsoft Azure</option>
                <option>Google Cloud</option>
              </select>
            </div>
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-300">
              Environment
            </span>

            <select
              value={environment}
              onChange={(event) =>
                setEnvironment(
                  event.target.value as InvestigationEnvironment,
                )
              }
              className="mt-2 h-11 w-full rounded-xl border border-white/[0.08] bg-[#0b1222] px-3 text-sm text-white outline-none focus:border-blue-400/50"
            >
              <option>Production</option>
              <option>Staging</option>
              <option>Development</option>
              <option>Security</option>
            </select>
          </label>

          <label className="block md:col-span-2">
            <span className="text-sm font-medium text-slate-300">
              Investigation type
            </span>

            <select
              value={type}
              onChange={(event) =>
                setType(
                  event.target.value as InvestigationType,
                )
              }
              className="mt-2 h-11 w-full rounded-xl border border-white/[0.08] bg-[#0b1222] px-3 text-sm text-white outline-none focus:border-blue-400/50"
            >
              <option>Cloud Security</option>
              <option>IAM Analysis</option>
              <option>Infrastructure Security</option>
              <option>Attack Path Analysis</option>
            </select>
          </label>
        </div>

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
            disabled={!isValid}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-5 text-sm font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Start Investigation
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </section>
  );
}
