import { ChevronDown, LogOut } from "lucide-react";

import { useAuth } from "@/auth/useAuth";

import Navigation from "./Navigation";

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="flex w-[248px] shrink-0 flex-col border-r border-white/[0.06] bg-[#080d1b]">
      <div className="border-b border-white/[0.06] px-5 py-5">
        <div className="flex items-center gap-3">
          <div className="relative flex h-9 w-9 items-center justify-center overflow-hidden rounded-xl bg-gradient-to-br from-blue-500 to-violet-500 shadow-lg shadow-blue-500/20">
            <span className="text-xs font-bold text-white">SK</span>
          </div>

          <div className="min-w-0">
            <div className="text-sm font-semibold tracking-tight text-white">
              SKYNEX
            </div>

            <div className="mt-0.5 text-[11px] text-slate-500">
              Security Investigation
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-3 py-5">
        <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-600">
          Workspace
        </p>

        <Navigation />
      </div>

      <div className="border-t border-white/[0.06] p-3">
        <div className="flex w-full items-center gap-3 rounded-xl p-3">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-500 text-[11px] font-bold text-white">
            SK
          </div>

          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium text-slate-200">
              Sri Krishna
            </p>

            <p className="text-[10px] text-slate-500">
              Administrator
            </p>
          </div>

          <button
            type="button"
            onClick={logout}
            aria-label="Sign out"
            title="Sign out"
            className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white/[0.05] hover:text-white"
          >
            <LogOut className="h-3.5 w-3.5" />
          </button>

          <ChevronDown className="hidden h-4 w-4 text-slate-600" />
        </div>
      </div>
    </aside>
  );
}
