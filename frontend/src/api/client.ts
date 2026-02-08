const API_URL = import.meta.env.VITE_API_URL 

export async function apiFetch(
  path: string,
  options: RequestInit = {},
  token?: string
) {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => null);
    throw new Error(error?.detail || "API error");
  }

  if (res.status === 204) return null;
  return res.json();
}
