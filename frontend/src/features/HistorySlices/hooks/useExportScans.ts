/**
 * Export Scans Hook
 * Responsibility: Handle CSV export functionality
 * Vertical Slice: Export feature
 */

import { exportScans } from "../../../api.js";

export function useExportScans() {
    const handleExportCSV = async () => {
        try {
            const blob = await exportScans();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "scan_history.csv";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error("Export failed:", error);
            alert("Failed to export scans");
        }
    };

    return { handleExportCSV };
}
