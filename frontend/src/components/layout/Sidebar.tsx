import { NavLink } from "react-router-dom";

const navigation = [
  { label: "Dashboard", path: "/" },
  { label: "Investigations", path: "/investigations" },
  { label: "Resources", path: "/resources" },
  { label: "Infrastructure Graph", path: "/graph" },
  { label: "Attack Paths", path: "/attack-paths" },
  { label: "AI Investigation", path: "/ai-investigation" },
  { label: "Reports", path: "/reports" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h1>SKYNEX</h1>

      <nav>
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
