import { describe, expect, it, vi } from "vitest";

import {
  getCurrentUser,
  login,
  logout,
  refreshSession,
} from "./authApi";

import { apiRequest } from "@/api/httpClient";

vi.mock("@/api/httpClient", () => ({
  apiRequest: vi.fn(),
}));

const mockedApiRequest =
  vi.mocked(apiRequest);

describe("authApi", () => {
  it("sends login credentials to the authentication endpoint", async () => {
    mockedApiRequest.mockResolvedValueOnce({
      access_token: "access",
      refresh_token: "refresh",
      session_id: "session",
      token_type: "bearer",
    });

    const result = await login({
      email: "user@example.com",
      password: "Password123!",
    });

    expect(result.access_token).toBe("access");

    expect(mockedApiRequest).toHaveBeenCalledWith(
      "/auth/login",
      {
        method: "POST",
        body: JSON.stringify({
          email: "user@example.com",
          password: "Password123!",
        }),
      },
    );
  });

  it("sends the refresh token to the refresh endpoint", async () => {
    mockedApiRequest.mockResolvedValueOnce({
      access_token: "new-access",
      refresh_token: "new-refresh",
      session_id: "session",
      token_type: "bearer",
    });

    await refreshSession({
      refresh_token: "old-refresh",
    });

    expect(mockedApiRequest).toHaveBeenCalledWith(
      "/auth/refresh",
      {
        method: "POST",
        body: JSON.stringify({
          refresh_token: "old-refresh",
        }),
      },
    );
  });

  it("sends the refresh token when logging out", async () => {
    mockedApiRequest.mockResolvedValueOnce(
      undefined,
    );

    await logout("refresh-token");

    expect(mockedApiRequest).toHaveBeenCalledWith(
      "/auth/logout",
      {
        method: "POST",
        body: JSON.stringify({
          refresh_token: "refresh-token",
        }),
      },
    );
  });

  it("uses the access token when requesting the current user", async () => {
    mockedApiRequest.mockResolvedValueOnce({
      id: "user-1",
      email: "user@example.com",
      full_name: "Test User",
      role: "investigator",
    });

    const result = await getCurrentUser(
      "access-token",
    );

    expect(result.role).toBe("investigator");

    expect(mockedApiRequest).toHaveBeenCalledWith(
      "/auth/me",
      {
        method: "GET",
        accessToken: "access-token",
      },
    );
  });
});
