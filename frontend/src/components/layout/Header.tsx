import { Bell, Search } from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-[68px] shrink-0 items-center justify-between border-b border-white/[0.06] bg-[#080d1b]/95 px-6 backdrop-blur">
      <div className="min-w-0">
        <h1 className="truncate text-sm font-semibold text-white">
          Cloud Security Investigation
        </h1>

        <p className="mt-0.5 text-[11px] text-slate-500">
          Enterprise Security Workspace
        </p>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden h-9 w-[260px] items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-3 md:flex">
          <Search className="h-4 w-4 text-slate-600" />

          <span className="text-xs text-slate-600">
            Search investigations...
          </span>

          <span className="ml-auto rounded border border-white/[0.08] px-1.5 py-0.5 text-[9px] text-slate-600">
            /
          </span>
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.03] text-slate-400 transition hover:bg-white/[0.06] hover:text-white"
        >
          <Bell className="h-4 w-4" />
        </button>
      </div>
    </header>
  );
}
