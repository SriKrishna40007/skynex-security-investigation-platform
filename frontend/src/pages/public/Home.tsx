import {
  ArrowRight,
  Bell,
  Bot,
  ChevronDown,
  ChevronRight,
  Cloud,
  Network,
  Search,
  ShieldCheck,
  Sparkles,
  Users,
  Zap,
} from "lucide-react";
import { Link } from "react-router-dom";

const capabilities = [
  {
    icon: Cloud,
    title: "Infrastructure Investigation",
    description:
      "Analyze Terraform and cloud infrastructure for misconfigurations, exposed resources and security weaknesses.",
    accent: "blue",
  },
  {
    icon: ShieldCheck,
    title: "IAM Intelligence",
    description:
      "Identify excessive permissions, authorization risks and opportunities for least-privilege remediation.",
    accent: "orange",
  },
  {
    icon: Network,
    title: "Attack Path Analysis",
    description:
      "Connect findings into meaningful attack paths and understand how weaknesses combine into exploitable chains.",
    accent: "green",
  },
  {
    icon: Sparkles,
    title: "AI-Powered Insights",
    description:
      "Turn complex security findings into clear explanations, prioritized remediation and engineering decisions.",
    accent: "purple",
  },
];

const metrics = [
  ["10K+", "Investigations Run", ShieldCheck],
  ["5K+", "Resources Analyzed", Cloud],
  ["98%", "Threat Detection Rate", Zap],
  ["80%", "Time Saved", Sparkles],
  ["500+", "Enterprise Teams", Users],
];

const workflow = [
  "Investigate",
  "Analyze",
  "Correlate",
  "Understand risk",
  "Remediate",
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white text-slate-950">
      {/* HEADER */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#05070d]/95 text-white backdrop-blur-xl">
        <div className="mx-auto flex h-[72px] max-w-[1440px] items-center justify-between px-6 lg:px-10">
          <Link to="/" className="flex items-center gap-3">
            <span className="relative flex h-9 w-12 items-center">
              <span className="absolute left-0 text-[34px] font-black leading-none tracking-[-0.18em] text-white">
                S
              </span>
              <span className="absolute left-[15px] top-[1px] text-[31px] font-black leading-none tracking-[-0.15em] text-blue-500">
                K
              </span>
            </span>

            <span className="text-xl font-semibold tracking-[-0.03em]">
              SKYNEX
            </span>
          </Link>

          <nav className="hidden items-center gap-8 text-sm font-medium text-slate-300 lg:flex">
            <a
              href="#product"
              className="transition hover:text-white"
            >
              Product
            </a>

            <a
              href="#solutions"
              className="flex items-center gap-1 transition hover:text-white"
            >
              Solutions
              <ChevronDown className="h-3.5 w-3.5" />
            </a>

            <a
              href="#resources"
              className="flex items-center gap-1 transition hover:text-white"
            >
              Resources
              <ChevronDown className="h-3.5 w-3.5" />
            </a>

            <a
              href="#help"
              className="flex items-center gap-1 transition hover:text-white"
            >
              Help
              <ChevronDown className="h-3.5 w-3.5" />
            </a>

            <a
              href="#pricing"
              className="transition hover:text-white"
            >
              Pricing
            </a>
          </nav>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="hidden text-sm font-medium text-slate-300 transition hover:text-white sm:block"
            >
              Log in
            </Link>

            <Link
              to="/app"
              className="group inline-flex h-10 items-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-5 text-sm font-semibold text-white shadow-lg shadow-blue-500/20 transition hover:-translate-y-0.5 hover:shadow-blue-500/30"
            >
              Try SKYNEX
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-white/20">
                <ArrowRight className="h-3 w-3 transition group-hover:translate-x-0.5" />
              </span>
            </Link>
          </div>
        </div>
      </header>

      <main>
        {/* HERO */}
        <section className="relative overflow-hidden bg-[#05070d] text-white">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_68%_45%,rgba(37,99,235,0.20),transparent_32%),radial-gradient(circle_at_88%_70%,rgba(124,58,237,0.18),transparent_30%)]" />

          <div className="absolute bottom-0 left-0 right-0 h-64 opacity-40">
            <div className="h-full bg-[linear-gradient(120deg,transparent_0%,rgba(37,99,235,0.14)_35%,rgba(124,58,237,0.22)_60%,transparent_100%)] blur-2xl" />
          </div>

          <div className="absolute inset-x-0 bottom-0 h-48 opacity-30 [background-image:radial-gradient(circle,rgba(59,130,246,0.6)_1px,transparent_1px)] [background-size:18px_18px] [mask-image:linear-gradient(to_top,black,transparent)]" />

          <div className="relative mx-auto grid max-w-[1440px] gap-12 px-6 pb-16 pt-16 lg:grid-cols-[0.92fr_1.08fr] lg:items-center lg:px-10 lg:pb-20 lg:pt-20">
            {/* HERO COPY */}
            <div className="relative z-10">
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-2 text-xs font-medium text-slate-300 shadow-lg shadow-black/20">
                <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
                Cloud Security Investigation Platform
                <ChevronRight className="h-3.5 w-3.5 text-slate-500" />
              </div>

              <h1 className="max-w-3xl text-5xl font-semibold leading-[0.98] tracking-[-0.055em] sm:text-6xl lg:text-[64px] xl:text-[72px]">
                Cloud security
                <br />
                investigation,{" "}
                <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-violet-500 bg-clip-text text-transparent">
                  reimagined.
                </span>
              </h1>

              <p className="mt-7 max-w-xl text-base leading-7 text-slate-400 sm:text-lg">
                Investigate infrastructure. Understand risk. Discover attack
                paths. Turn complex security findings into decisions your
                engineering team can act on.
              </p>

              <div className="mt-9 flex flex-col gap-3 sm:flex-row">
                <Link
                  to="/app"
                  className="group inline-flex h-12 items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-7 text-sm font-semibold text-white shadow-xl shadow-blue-500/20 transition hover:-translate-y-0.5"
                >
                  Try SKYNEX
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/20">
                    <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-0.5" />
                  </span>
                </Link>

                <a
                  href="#product"
                  className="inline-flex h-12 items-center justify-center gap-3 rounded-xl border border-white/20 bg-white/[0.03] px-7 text-sm font-semibold text-white transition hover:border-white/30 hover:bg-white/[0.07]"
                >
                  Explore platform
                  <span className="flex h-6 w-6 items-center justify-center rounded-full border border-white/20">
                    <PlayIcon />
                  </span>
                </a>
              </div>

              <div className="mt-9 flex flex-wrap gap-x-8 gap-y-3 text-sm text-slate-300">
                {[
                  "AI-Powered Analysis",
                  "Attack Path Discovery",
                  "Actionable Remediation",
                ].map((item) => (
                  <div key={item} className="flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4 text-blue-400" />
                    {item}
                  </div>
                ))}
              </div>
            </div>

            {/* PRODUCT PREVIEW */}
            <div className="relative z-10">
              <div className="rounded-2xl border border-white/10 bg-[#0b1120]/90 p-2 shadow-2xl shadow-blue-950/40 backdrop-blur">
                <div className="overflow-hidden rounded-xl border border-white/10 bg-[#0b1220]">
                  <div className="flex h-11 items-center border-b border-white/10 px-4">
                    <div className="flex gap-1.5">
                      <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
                      <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
                      <span className="h-2.5 w-2.5 rounded-full bg-white/20" />
                    </div>

                    <span className="ml-4 text-[11px] text-slate-500">
                      SKYNEX Security Workspace
                    </span>
                  </div>

                  <div className="grid min-h-[390px] grid-cols-[125px_1fr]">
                    <aside className="border-r border-white/10 p-4">
                      <div className="flex items-center gap-2">
                        <span className="flex h-6 w-6 items-center justify-center rounded-md bg-gradient-to-br from-blue-500 to-violet-500 text-[9px] font-bold">
                          SK
                        </span>
                        <span className="text-xs font-semibold">
                          SKYNEX
                        </span>
                      </div>

                      <div className="mt-7 space-y-2 text-[10px] text-slate-500">
                        {[
                          "Overview",
                          "Investigations",
                          "Attack Paths",
                          "Graph",
                          "Reports",
                          "Resources",
                          "Settings",
                        ].map((item, index) => (
                          <div
                            key={item}
                            className={`rounded-md px-2 py-2 ${
                              index === 0
                                ? "bg-blue-500/10 text-blue-400"
                                : ""
                            }`}
                          >
                            {item}
                          </div>
                        ))}
                      </div>

                      <div className="mt-10 rounded-lg border border-white/10 bg-white/[0.03] p-2">
                        <div className="flex items-center gap-2">
                          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-500 text-[8px] font-bold">
                            SK
                          </span>
                          <div>
                            <p className="text-[9px] text-white">
                              Sri Krishna
                            </p>
                            <p className="text-[8px] text-slate-500">
                              Admin
                            </p>
                          </div>
                        </div>
                      </div>
                    </aside>

                    <div className="p-4 sm:p-5">
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-xs font-medium text-white">
                          Overview
                        </p>

                        <div className="flex h-7 w-36 items-center gap-2 rounded-md border border-white/10 bg-white/[0.03] px-2 text-[8px] text-slate-500">
                          <Search className="h-3 w-3" />
                          Search investigations...
                        </div>

                        <Bell className="hidden h-4 w-4 text-slate-500 sm:block" />
                      </div>

                      <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.025] p-4">
                        <div className="flex flex-col justify-between gap-6 sm:flex-row">
                          <div>
                            <p className="text-[10px] font-medium text-slate-400">
                              SECURITY POSTURE
                            </p>

                            <div className="mt-3 flex items-center gap-4">
                              <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-[3px] border-blue-500">
                                <div className="absolute inset-[-3px] rounded-full border-[3px] border-transparent border-t-rose-500 border-r-orange-400" />
                                <div className="text-center">
                                  <p className="text-3xl font-semibold">
                                    82
                                  </p>
                                  <p className="text-[8px] text-slate-500">
                                    /100
                                  </p>
                                </div>
                              </div>

                              <div>
                                <p className="text-xs font-semibold text-rose-400">
                                  HIGH RISK
                                </p>
                                <p className="mt-1 text-[9px] text-slate-500">
                                  Investigation risk score
                                </p>
                              </div>
                            </div>
                          </div>

                          <div className="min-w-[150px] space-y-3">
                            {[
                              ["Critical", "2", "bg-rose-500"],
                              ["High", "4", "bg-orange-500"],
                              ["Medium", "8", "bg-yellow-400"],
                              ["Low", "3", "bg-emerald-400"],
                            ].map(([label, value, color]) => (
                              <div
                                key={label}
                                className="flex items-center gap-2 text-[9px]"
                              >
                                <span
                                  className={`h-2 w-2 rounded-full ${color}`}
                                />
                                <span className="text-slate-300">
                                  {label}
                                </span>
                                <span className="ml-auto text-white">
                                  {value}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
                        {[
                          ["Investigations", "24", "blue"],
                          ["Resources", "127", "blue"],
                          ["Attack Paths", "6", "green"],
                          ["Reports", "18", "purple"],
                        ].map(([label, value, tone]) => (
                          <div
                            key={label}
                            className="rounded-xl border border-white/10 bg-white/[0.025] p-3"
                          >
                            <p className="text-[9px] text-slate-500">
                              {label}
                            </p>
                            <p className="mt-2 text-xl font-semibold text-white">
                              {value}
                            </p>

                            <div
                              className={`mt-3 h-1 rounded-full ${
                                tone === "green"
                                  ? "bg-emerald-500/50"
                                  : tone === "purple"
                                    ? "bg-violet-500/50"
                                    : "bg-blue-500/50"
                              }`}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="absolute -bottom-8 -right-8 h-32 w-32 rounded-full bg-blue-500/20 blur-3xl" />
              <div className="absolute -top-8 -left-8 h-24 w-24 rounded-full bg-violet-500/20 blur-3xl" />
            </div>
          </div>
        </section>

        {/* TRUSTED BY */}
        <section className="border-b border-slate-200 bg-white">
          <div className="mx-auto max-w-6xl px-6 py-10">
            <p className="text-center text-sm font-medium text-slate-500">
              Trusted by security and engineering teams
            </p>

            <div className="mt-7 grid grid-cols-2 items-center gap-7 text-center text-lg font-semibold text-slate-500 sm:grid-cols-3 lg:grid-cols-6">
              <span className="text-2xl font-semibold tracking-tight">
                aws
              </span>
              <span>Microsoft Azure</span>
              <span>Google Cloud</span>
              <span className="text-xl">Terraform</span>
              <span className="text-xl">okta</span>
              <span className="text-xl">paloalto</span>
            </div>
          </div>
        </section>

        {/* CAPABILITIES */}
        <section
          id="product"
          className="relative overflow-hidden bg-white px-6 py-24 lg:px-8"
        >
          <div className="absolute inset-0 opacity-40 [background-image:radial-gradient(#dbeafe_1px,transparent_1px)] [background-size:18px_18px] [mask-image:linear-gradient(to_bottom,transparent,black,transparent)]" />

          <div className="relative mx-auto max-w-6xl">
            <div className="mx-auto max-w-2xl text-center">
              <p className="text-sm font-semibold tracking-wide text-blue-600">
                THE SKYNEX PLATFORM
              </p>

              <h2 className="mt-3 text-4xl font-semibold tracking-[-0.04em] text-slate-950 sm:text-5xl">
                Security context, not security noise.
              </h2>

              <p className="mt-5 text-lg leading-8 text-slate-600">
                Bring infrastructure analysis, authorization intelligence,
                attack-path reasoning and AI-powered investigation into one
                engineering workflow.
              </p>
            </div>

            <div
              id="solutions"
              className="mt-14 grid gap-5 md:grid-cols-2 xl:grid-cols-4"
            >
              {capabilities.map((item) => {
                const Icon = item.icon;

                return (
                  <div
                    key={item.title}
                    className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-blue-200 hover:shadow-xl hover:shadow-blue-950/5"
                  >
                    <div
                      className={`flex h-12 w-12 items-center justify-center rounded-xl ${
                        item.accent === "blue"
                          ? "bg-blue-50 text-blue-600"
                          : item.accent === "orange"
                            ? "bg-orange-50 text-orange-500"
                            : item.accent === "green"
                              ? "bg-emerald-50 text-emerald-600"
                              : "bg-violet-50 text-violet-600"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>

                    <h3 className="mt-7 text-xl font-semibold tracking-tight">
                      {item.title}
                    </h3>

                    <p className="mt-3 text-sm leading-6 text-slate-600">
                      {item.description}
                    </p>

                    <Link
                      to="/app"
                      className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-blue-600"
                    >
                      Learn more
                      <ArrowRight className="h-3.5 w-3.5 transition group-hover:translate-x-1" />
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* METRICS */}
        <section className="bg-[#090d1a] px-6 py-10 text-white lg:px-8">
          <div className="mx-auto grid max-w-6xl gap-6 sm:grid-cols-2 lg:grid-cols-5">
            {metrics.map(([value, label, Icon]) => {
              const MetricIcon = Icon as typeof ShieldCheck;

              return (
                <div
                  key={label as string}
                  className="flex items-center gap-4 rounded-xl border border-white/10 bg-white/[0.025] p-4"
                >
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                    <MetricIcon className="h-5 w-5" />
                  </div>

                  <div>
                    <p className="text-2xl font-semibold">
                      {value as string}
                    </p>
                    <p className="text-xs text-slate-500">
                      {label as string}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* WORKFLOW */}
        <section
          id="resources"
          className="border-b border-slate-200 bg-slate-50 px-6 py-24 lg:px-8"
        >
          <div className="mx-auto grid max-w-6xl gap-16 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">
            <div>
              <p className="text-sm font-semibold text-blue-600">
                ONE INVESTIGATION FLOW
              </p>

              <h2 className="mt-3 text-4xl font-semibold tracking-[-0.04em]">
                From finding a weakness to understanding the threat.
              </h2>

              <p className="mt-5 leading-7 text-slate-600">
                SKYNEX connects the evidence behind a security finding so
                engineering teams can understand what happened, why it matters
                and what should happen next.
              </p>

              <Link
                to="/app"
                className="mt-7 inline-flex items-center gap-2 rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white"
              >
                Explore investigations
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>

            <div className="space-y-3">
              {workflow.map((step, index) => (
                <div
                  key={step}
                  className="flex items-center gap-5 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
                >
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-slate-950 text-sm font-semibold text-white">
                    {index + 1}
                  </span>

                  <span className="font-medium">{step}</span>

                  {index < workflow.length - 1 && (
                    <ChevronRight className="ml-auto h-4 w-4 text-slate-300" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* PRICING */}
        <section
          id="pricing"
          className="bg-white px-6 py-24 lg:px-8"
        >
          <div className="mx-auto max-w-5xl rounded-3xl bg-gradient-to-br from-[#07101f] via-[#0b1630] to-[#11102a] p-8 text-white shadow-2xl sm:p-12"
          >
            <div className="grid gap-10 lg:grid-cols-[1fr_auto] lg:items-center">
              <div>
                <p className="text-sm font-semibold text-blue-400">
                  READY WHEN YOU ARE
                </p>

                <h2 className="mt-3 text-4xl font-semibold tracking-tight">
                  Make your next security investigation actionable.
                </h2>

                <p className="mt-4 max-w-2xl leading-7 text-slate-400">
                  Explore the SKYNEX security investigation workspace and see
                  how infrastructure, IAM, attack paths and AI reasoning work
                  together.
                </p>
              </div>

              <Link
                to="/app"
                className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-violet-500 px-6 text-sm font-semibold shadow-lg shadow-blue-500/20"
              >
                Try SKYNEX
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </section>

        {/* HELP */}
        <section
          id="help"
          className="border-t border-slate-200 bg-slate-50 px-6 py-16 lg:px-8"
        >
          <div className="mx-auto max-w-6xl text-center">
            <Bot className="mx-auto h-7 w-7 text-blue-600" />

            <h2 className="mt-4 text-3xl font-semibold">
              Need help understanding SKYNEX?
            </h2>

            <p className="mx-auto mt-3 max-w-xl text-slate-600">
              Explore the investigation platform, review the workflow or
              start a security investigation directly.
            </p>

            <Link
              to="/app"
              className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-blue-600"
            >
              Open SKYNEX
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="bg-[#05070d] px-6 py-10 text-slate-400 lg:px-8">
        <div className="mx-auto flex max-w-6xl flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
          <Link to="/" className="flex items-center gap-3 text-white">
            <span className="relative flex h-8 w-10 items-center">
              <span className="absolute left-0 text-[29px] font-black leading-none tracking-[-0.18em]">
                S
              </span>
              <span className="absolute left-[13px] top-[1px] text-[27px] font-black leading-none tracking-[-0.15em] text-blue-500">
                K
              </span>
            </span>
            <span className="font-semibold">SKYNEX</span>
          </Link>

          <p className="text-xs">
            Cloud security investigation, reimagined.
          </p>
        </div>
      </footer>
    </div>
  );
}

function PlayIcon() {
  return (
    <span className="ml-0.5 block h-0 w-0 border-y-[4px] border-y-transparent border-l-[6px] border-l-white" />
  );
}
