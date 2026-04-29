/**
 * Export Scans Hook
 * Responsibility: Handle CSV export functionality
 * Vertical Slice: Export feature
 */

import type { Scan } from "../types.js";

export function useExportScans(filteredData: Scan[]) {
    const handleExportCSV = () => {
        try {
            if (!filteredData || filteredData.length === 0) {
                alert("No data to export");
                return;
            }

            const headers = ["URL", "Date/Time Analysed", "Result", "Confidence", "Explanations"];

            const csvRows = filteredData.map(scan => {
                const date = new Date(scan.timestamp).toLocaleString();
                const result = scan.isSafe ? "Safe" : "Phishing";
                const confidence = `${scan.confidence}%`;
                const explanations = (scan.explanation || []).join("; ");

                return `"${scan.url}","${date}","${result}","${confidence}","${explanations}"`;
            });

            const csvContent = [headers.join(","), ...csvRows].join("\n");
            const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
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
