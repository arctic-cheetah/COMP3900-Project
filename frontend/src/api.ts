const API_BASE: string =
    import.meta.env.VITE_API_URL ?? "http://localhost:5001";

type ApiError = {
    error?: string;
}

type ScanResponse = any;
type StoredDataResponse = any;

export const scanURL = async (url: string): Promise<ScanResponse> => {
    const res = await fetch(`${API_BASE}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || "Failed to scan website url");
    }
    return res.json();
};

export const getStoredData = async (): Promise<StoredDataResponse> => {
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

export async function exportScans(): Promise<Blob> {
    const response = await fetch(`${API_BASE}/scans/export`);
    if (!response.ok) throw new Error("Failed to export scans");
    return response.blob();
}
