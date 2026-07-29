import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import AppLayout from "@/layouts/AppLayout";

import AIInvestigation from "@/pages/AIInvestigation";
import AttackPaths from "@/pages/AttackPaths";
import Dashboard from "@/pages/Dashboard";
import Graph from "@/pages/Graph";
import Investigations from "@/pages/Investigations";
import Reports from "@/pages/Reports";
import Resources from "@/pages/Resources";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Dashboard />} />

          <Route
            path="investigations"
            element={<Investigations />}
          />

          <Route
            path="resources"
            element={<Resources />}
          />

          <Route
            path="graph"
            element={<Graph />}
          />

          <Route
            path="attack-paths"
            element={<AttackPaths />}
          />

          <Route
            path="ai-investigation"
            element={<AIInvestigation />}
          />

          <Route
            path="reports"
            element={<Reports />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
