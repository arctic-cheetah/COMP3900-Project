const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

export const scanURL = async () => {
  const res = await fetch(`${API_BASE}/scan`);
  if (!res.ok) throw new Error("Failed to scan website url");
  return res.json();
};
