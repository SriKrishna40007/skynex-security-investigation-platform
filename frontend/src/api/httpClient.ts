const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "http://localhost:8000/api/v1";

export type ApiRequestOptions = RequestInit & {
  accessToken?: string;
};

export async function apiRequest<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const {
    accessToken,
    headers,
    ...requestOptions
  } = options;

  const requestHeaders = new Headers(headers);

  if (
    !requestHeaders.has("Content-Type") &&
    requestOptions.body &&
    !(requestOptions.body instanceof FormData)
  ) {
    requestHeaders.set(
      "Content-Type",
      "application/json",
    );
  }

  if (accessToken) {
    requestHeaders.set(
      "Authorization",
      `Bearer ${accessToken}`,
    );
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...requestOptions,
      headers: requestHeaders,
    },
  );

  if (!response.ok) {
    let message =
      `API request failed with status ${response.status}.`;

    try {
      const body = await response.json();

      if (typeof body?.detail === "string") {
        message = body.detail;
      }
    } catch {
      // Preserve the HTTP status error when the response
      // does not contain a JSON error body.
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
