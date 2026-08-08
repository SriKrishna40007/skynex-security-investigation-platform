import {
  useCallback,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  login as loginApi,
  logout as logoutApi,
} from "@/api/auth/authApi";

import {
  AuthContext,
  type AuthContextValue,
} from "./AuthContext";

import type {
  AuthSession,
  AuthState,
} from "./authTypes";

type AuthProviderProps = {
  children: ReactNode;
};

const initialState: AuthState = {
  isAuthenticated: false,
  isLoading: false,
  session: null,
};

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [state, setState] =
    useState<AuthState>(initialState);

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

        setState({
          isAuthenticated: true,
          isLoading: false,
          session,
        });
      } catch (error) {
        setState(initialState);
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
        setState(initialState);
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
