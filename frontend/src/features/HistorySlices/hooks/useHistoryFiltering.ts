/**
 * Filtering Slice Hook
 * Responsibility: Manage filtering state and logic
 * Vertical Slice: Filtering feature
 */

import { useState } from "react";
import type { Scan, FilterType, HistoryStats } from "../types.js";

interface UseHistoryFilteringReturn {
    filter: FilterType;
    setFilter: (filter: FilterType) => void;
    filteredData: Scan[];
    stats: HistoryStats;
}

export function useHistoryFiltering(
    history: Scan[]
): UseHistoryFilteringReturn {
    const [filter, setFilter] = useState<FilterType>("all");

    // Calculate statistics once
    const stats: HistoryStats = {
        total: history.length,
        safe: history.filter((h) => h.isSafe).length,
        phishing: history.filter((h) => !h.isSafe).length,
    };

    // Filter data based on current filter
    const filteredData = history.filter((item) => {
        if (filter === "all") return true;
        return filter === "safe" ? item.isSafe : !item.isSafe;
    });

    return {
        filter,
        setFilter,
        filteredData,
        stats,
    };
}
