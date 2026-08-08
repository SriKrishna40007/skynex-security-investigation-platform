import type { UserResponse } from "@/api/auth/authApi";

export type AuthSession = {
  accessToken: string;
  refreshToken: string;
  sessionId: string;
  tokenType: string;
  user: UserResponse | null;
};

export type AuthState = {
  isAuthenticated: boolean;
  isLoading: boolean;
  session: AuthSession | null;
};
