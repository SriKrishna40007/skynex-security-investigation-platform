import { apiRequest } from "@/api/httpClient";

export type LoginRequest = {
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  refresh_token: string;
  session_id: string;
  token_type: string;
};

export type RefreshTokenRequest = {
  refresh_token: string;
};

export type UserResponse = {
  id: string;
  email: string;
  full_name: string;
  role: string;
};

export async function login(
  request: LoginRequest,
): Promise<TokenResponse> {
  return apiRequest<TokenResponse>(
    "/auth/login",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function refreshSession(
  request: RefreshTokenRequest,
): Promise<TokenResponse> {
  return apiRequest<TokenResponse>(
    "/auth/refresh",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export async function logout(
  refreshToken: string,
): Promise<void> {
  await apiRequest<void>(
    "/auth/logout",
    {
      method: "POST",
      body: JSON.stringify({
        refresh_token: refreshToken,
      }),
    },
  );
}

export async function getCurrentUser(
  accessToken: string,
): Promise<UserResponse> {
  return apiRequest<UserResponse>(
    "/auth/me",
    {
      method: "GET",
      accessToken,
    },
  );
}
