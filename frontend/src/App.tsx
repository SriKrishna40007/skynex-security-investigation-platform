import { AuthProvider } from "@/auth/AuthProvider";
import { InvestigationProvider } from "@/investigations/InvestigationProvider";
import AppRouter from "@/routes/AppRouter";

export default function App() {
  return (
    <AuthProvider>
      <InvestigationProvider>
        <AppRouter />
      </InvestigationProvider>
    </AuthProvider>
  );
}
