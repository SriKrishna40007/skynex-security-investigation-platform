import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { ApiError } from "@/api/httpClient";

import {
  login as loginApi,
  logout as logoutApi,
  getCurrentUser,
  refreshSession,
} from "@/api/auth/authApi";

import {
  AuthContext,
  type AuthContextValue,
} from "./AuthContext";

import type {
  AuthSession,
  AuthState,
} from "./authTypes";

import {
  clearStoredSession,
  loadStoredSession,
  saveStoredSession,
} from "./sessionStorage";

type AuthProviderProps = {
  children: ReactNode;
};

const initialState: AuthState = {
  isAuthenticated: false,
  isLoading: true,
  session: null,
};

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [state, setState] =
    useState<AuthState>(initialState);

  useEffect(() => {
    let cancelled = false;

    async function restoreSession() {
      const storedSession = loadStoredSession();

      if (!storedSession) {
        if (!cancelled) {
          setState({
            isAuthenticated: false,
            isLoading: false,
            session: null,
          });
        }

        return;
      }

      try {
        let session = storedSession;

        try {
          const user = await getCurrentUser(
            session.accessToken,
          );

          session = {
            ...session,
            user,
          };
        } catch (error) {
          if (
            !(error instanceof ApiError) ||
            error.status !== 401
          ) {
            throw error;
          }

          const refreshed = await refreshSession({
            refresh_token: session.refreshToken,
          });

          session = {
            accessToken: refreshed.access_token,
            refreshToken: refreshed.refresh_token,
            sessionId: refreshed.session_id,
            tokenType: refreshed.token_type,
            user: null,
          };

          const user = await getCurrentUser(
            session.accessToken,
          );

          session = {
            ...session,
            user,
          };
        }

        if (cancelled) {
          return;
        }

        saveStoredSession(session);

        setState({
          isAuthenticated: true,
          isLoading: false,
          session,
        });
      } catch {
        clearStoredSession();

        if (!cancelled) {
          setState({
            isAuthenticated: false,
            isLoading: false,
            session: null,
          });
        }
      }
    }

    void restoreSession();

    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(
    async (
      email: string,
      password: string,
    ): Promise<void> => {
      setState((current) => ({
        ...current,
        isLoading: true,
      }));

      try {
        const response = await loginApi({
          email,
          password,
        });

        const session: AuthSession = {
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
          sessionId: response.session_id,
          tokenType: response.token_type,
          user: null,
        };

        saveStoredSession(session);

        setState({
          isAuthenticated: true,
          isLoading: false,
          session,
        });
      } catch (error) {
        clearStoredSession();
        setState({
          isAuthenticated: false,
          isLoading: false,
          session: null,
        });
        throw error;
      }
    },
    [],
  );

  const logout = useCallback(
    async (): Promise<void> => {
      const refreshToken =
        state.session?.refreshToken;

      setState((current) => ({
        ...current,
        isLoading: true,
      }));

      try {
        if (refreshToken) {
          await logoutApi(refreshToken);
        }
      } finally {
        clearStoredSession();
        setState({
          isAuthenticated: false,
          isLoading: false,
          session: null,
        });
      }
    },
    [state.session?.refreshToken],
  );

  const value = useMemo<AuthContextValue>(
    () => ({
      state,
      login,
      logout,
    }),
    [state, login, logout],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
