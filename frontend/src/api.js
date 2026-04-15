const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:5001";

export const scanURL = async (url) => {
  const res = await fetch(`${API_BASE}/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(res.statusText + `${res.status}`|| "Failed to scan website url");
  }
  return res.json();
};

export const getStoredData = async () => {
  const res = await fetch(`${API_BASE}/list_scans`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || "Failed to scan website url");
  }
  return res.json();
}
