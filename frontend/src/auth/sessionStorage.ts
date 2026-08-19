import type { AuthSession } from "./authTypes";

const STORAGE_KEY = "skynex.auth.session";

export function loadStoredSession(): AuthSession | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);

    if (!raw) {
      return null;
    }

    const parsed: unknown = JSON.parse(raw);

    if (!isAuthSession(parsed)) {
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }

    return parsed;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function saveStoredSession(
  session: AuthSession,
): void {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(session),
  );
}

export function clearStoredSession(): void {
  localStorage.removeItem(STORAGE_KEY);
}

function isAuthSession(
  value: unknown,
): value is AuthSession {
  if (!value || typeof value !== "object") {
    return false;
  }

  const session = value as Record<string, unknown>;

  return (
    typeof session.accessToken === "string" &&
    typeof session.refreshToken === "string" &&
    typeof session.sessionId === "string" &&
    typeof session.tokenType === "string"
  );
}
