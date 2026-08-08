import { ShieldCheck } from "lucide-react";

export default function Settings() {
  return (
    <section className="space-y-6">
      <div>
        <p className="text-xs font-medium uppercase tracking-[0.16em] text-blue-400">
          Workspace
        </p>

        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">
          Settings
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Manage your SKYNEX investigation workspace and security preferences.
        </p>
      </div>

      <div className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10">
            <ShieldCheck className="h-5 w-5 text-blue-400" />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-white">
              Security workspace
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Authentication, access control and workspace configuration will
              be connected during the application integration phase.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
