/**
 * Shared types for History feature slices
 * Vertical Slice: Type definitions
 */

export interface Scan {
    id?: number;
    url: string;
    isSafe: boolean;
    timestamp: string | number | Date;
    confidence: number;
}

export interface HistoryStats {
    total: number;
    safe: number;
    phishing: number;
}

export type FilterType = "all" | "safe" | "phishing";

export interface HistoryActions {
    onDelete: (scan: Scan) => void;
    onDeleteMultiple: (scans: Scan[]) => void;
    onHistoryClick: (scan: Scan) => void;
}

export interface HistoricalDataProps extends HistoryActions {
    history: Scan[];
}

export interface MobileScanCardProps {
    scan: Scan;
    isSelected: boolean;
    onToggleSelect: (scan: Scan) => void;
    onClick: () => void;
}

export interface DesktopScanRowProps {
    scan: Scan;
    isSelected: boolean;
    onToggleSelect: (scan: Scan) => void;
    onDelete: (scan: Scan) => void;
}
