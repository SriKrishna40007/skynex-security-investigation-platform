import { useState } from "react";
import { ShieldCheck } from "lucide-react";
import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "@/auth/useAuth";

type LoginLocationState = {
  from?: string;
};

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const {
    state: authState,
    login,
  } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const state =
    location.state as LoginLocationState | null;

  const redirectTo =
    state?.from ?? "/app/dashboard";

  if (authState.isAuthenticated) {
    navigate("/app/dashboard", {
      replace: true,
    });

    return null;
  }

  async function handleLogin() {
    setError(null);

    try {
      await login(email, password);

      navigate(redirectTo, {
        replace: true,
      });
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to sign in.",
      );
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-10">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-md items-center justify-center">
        <div className="w-full">
          <Link
            to="/"
            className="mb-6 inline-flex items-center text-sm text-slate-400 transition hover:text-white"
          >
            Back to SKYNEX
          </Link>

          <div className="rounded-3xl border border-white/10 bg-white p-8 shadow-2xl">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-950 text-white">
              <ShieldCheck className="h-5 w-5" />
            </div>

            <h1 className="mt-7 text-2xl font-semibold tracking-tight text-slate-950">
              Welcome back
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Sign in to your SKYNEX investigation workspace.
            </p>

            <form
              className="mt-8 space-y-4"
              onSubmit={(event) => {
                event.preventDefault();
                void handleLogin();
              }}
            >
              <label className="block text-sm font-medium text-slate-900">
                Email

                <input
                  type="email"
                  placeholder="you@company.com"
                  autoComplete="email"
                  value={email}
                  onChange={(event) =>
                    setEmail(event.target.value)
                  }
                  className="mt-2 h-11 w-full rounded-xl border border-slate-200 px-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10"
                />
              </label>

              <label className="block text-sm font-medium text-slate-900">
                Password

                <input
                  type="password"
                  placeholder="••••••••"
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  className="mt-2 h-11 w-full rounded-xl border border-slate-200 px-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-slate-950 focus:ring-2 focus:ring-slate-950/10"
                />
              </label>

              {error && (
                <p
                  role="alert"
                  className="rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700"
                >
                  {error}
                </p>
              )}

              <button
                type="submit"
                disabled={authState.isLoading}
                className="h-11 w-full rounded-xl bg-slate-950 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-slate-950/20"
              >
                {authState.isLoading
                  ? "Signing in..."
                  : "Sign in"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
