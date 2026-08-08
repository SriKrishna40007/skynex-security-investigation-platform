import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "@/auth/useAuth";

export default function ProtectedRoute() {
  const location = useLocation();
  const { state } = useAuth();

  if (state.isLoading) {
    return null;
  }

  if (!state.isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  return <Outlet />;
}
