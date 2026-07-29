export default function Sidebar() {
  return (
    <aside className="flex w-64 flex-col border-r border-slate-800 bg-slate-900">
      <div className="border-b border-slate-800 p-6">
        <h1 className="text-xl font-bold tracking-wide">
          SKYNEX
        </h1>

        <p className="mt-1 text-xs text-slate-400">
          Security Investigation Platform
        </p>
      </div>

      <nav className="flex-1 p-4">
        <p className="text-sm text-slate-500">
          Navigation coming soon...
        </p>
      </nav>
    </aside>
  );
}
