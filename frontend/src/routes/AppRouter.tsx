import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import Investigations from "../pages/Investigations";
import Resources from "../pages/Resources";
import Graph from "../pages/Graph";
import AttackPaths from "../pages/AttackPaths";
import AIInvestigation from "../pages/AIInvestigation";
import Reports from "../pages/Reports";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route
          path="/investigations"
          element={<Investigations />}
        />
        <Route
          path="/resources"
          element={<Resources />}
        />
        <Route path="/graph" element={<Graph />} />
        <Route
          path="/attack-paths"
          element={<AttackPaths />}
        />
        <Route
          path="/ai-investigation"
          element={<AIInvestigation />}
        />
        <Route
          path="/reports"
          element={<Reports />}
        />
      </Routes>
    </BrowserRouter>
  );
}
