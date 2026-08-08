import {
  BarChart3,
  Bot,
  FileBarChart,
  FolderSearch,
  GitBranch,
  Network,
  Settings,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigation = [
  {
    to: "/app/dashboard",
    label: "Overview",
    icon: BarChart3,
  },
  {
    to: "/app/investigations",
    label: "Investigations",
    icon: FolderSearch,
  },
  {
    to: "/app/ai-investigation",
    label: "AI Investigation",
    icon: Bot,
  },
  {
    to: "/app/attack-paths",
    label: "Attack Paths",
    icon: GitBranch,
  },
  {
    to: "/app/graph",
    label: "Graph",
    icon: Network,
  },
  {
    to: "/app/reports",
    label: "Reports",
    icon: FileBarChart,
  },
  {
    to: "/app/resources",
    label: "Resources",
    icon: FolderSearch,
  },
  {
    to: "/app/settings",
    label: "Settings",
    icon: Settings,
  },
];

export default function Navigation() {
  return (
    <nav className="space-y-1">
      {navigation.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            [
              "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition",
              isActive
                ? "bg-blue-500/10 text-blue-400 ring-1 ring-blue-500/10"
                : "text-slate-400 hover:bg-white/[0.04] hover:text-slate-100",
            ].join(" ")
          }
        >
          {({ isActive }) => (
            <>
              <Icon
                className={[
                  "h-4 w-4 shrink-0 transition",
                  isActive
                    ? "text-blue-400"
                    : "text-slate-500 group-hover:text-slate-300",
                ].join(" ")}
              />
              <span>{label}</span>
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}
