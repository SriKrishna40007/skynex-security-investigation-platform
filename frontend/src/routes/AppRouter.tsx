import {
  BrowserRouter,
  Navigate,
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
import NewInvestigation from "@/pages/investigations/NewInvestigation";
import InvestigationWorkspace from "@/pages/investigations/InvestigationWorkspace";
import Settings from "@/pages/Settings";
import Home from "@/pages/public/Home";
import Login from "@/pages/public/Login";
import NotFound from "@/pages/public/NotFound";
import ProtectedRoute from "@/routes/ProtectedRoute";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/app" element={<AppLayout />}>
            <Route
              index
              element={
                <Navigate
                  to="dashboard"
                  replace
                />
              }
            />

            <Route
              path="dashboard"
              element={<Dashboard />}
            />

            <Route


              path="investigations"


              element={<Investigations />}


            />



            <Route


              path="investigations/new"


              element={<NewInvestigation />}


            />



            <Route


              path="investigations/:id"


              element={<InvestigationWorkspace />}


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

            <Route
              path="settings"
              element={<Settings />}
            />
          </Route>
        </Route>

        <Route
          path="*"
          element={<NotFound />}
        />
      </Routes>
    </BrowserRouter>
  );
}
