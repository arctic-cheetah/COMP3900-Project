/**
 * Selection Slice Hook
 * Responsibility: Manage selection state and bulk operations
 * Vertical Slice: Selection and bulk delete feature
 */

import { useState } from "react";
import type { Scan } from "../types.js";

interface UseHistorySelectionReturn {
    selection: Scan[];
    toggleRow: (scan: Scan) => void;
    toggleAll: (filteredData: Scan[]) => void;
    clearSelection: () => void;
    executeBulkDelete: (
        onDeleteMultiple: (scans: Scan[]) => void,
        filteredData: Scan[]
    ) => void;
}

export function useHistorySelection(): UseHistorySelectionReturn {
    const [selection, setSelection] = useState<Scan[]>([]);

    const toggleRow = (scan: Scan) => {
        setSelection((current) =>
            current.includes(scan)
                ? current.filter((item) => item !== scan)
                : [...current, scan]
        );
    };

    const toggleAll = (filteredData: Scan[]) => {
        setSelection((current) =>
            current.length === filteredData.length ? [] : [...filteredData]
        );
    };

    const clearSelection = () => {
        setSelection([]);
    };

    const executeBulkDelete = (
        onDeleteMultiple: (scans: Scan[]) => void,
        filteredData: Scan[]
    ) => {
        if (selection.length === 0) return;

        if (
            window.confirm(
                `Are you sure you want to delete ${selection.length} selected scans?`
            )
        ) {
            onDeleteMultiple(selection);
            clearSelection();
        }
    };

    return {
        selection,
        toggleRow,
        toggleAll,
        clearSelection,
        executeBulkDelete,
    };
}

export { useHistoryFiltering } from "./useHistoryFiltering.js";

// Helper to compute selection states
export const computeSelectionStates = (
    selection: Scan[],
    filteredData: Scan[]
) => ({
    isAllSelected:
        selection.length > 0 && selection.length === filteredData.length,
    isPartiallySelected:
        selection.length > 0 && selection.length < filteredData.length,
});
