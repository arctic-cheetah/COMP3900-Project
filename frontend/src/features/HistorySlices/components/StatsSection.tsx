/**
 * StatsSection Component
 * Responsibility: Display all stats cards with filtering
 */

import { Group } from "@mantine/core";
import { StatCard } from "./StatCard.js";
import type { FilterType, HistoryStats } from "../types.js";

interface StatsSectionProps {
    stats: HistoryStats;
    filter: FilterType;
    onFilterChange: (filter: FilterType) => void;
}

export function StatsSection({
    stats,
    filter,
    onFilterChange,
}: StatsSectionProps) {
    return (
        <Group grow mb="xl">
            <StatCard
                label="Total"
                value={stats.total}
                color="blue"
                isActive={filter === "all"}
                onClick={() => onFilterChange("all")}
            />
            <StatCard
                label="Safe"
                value={stats.safe}
                color="green"
                isActive={filter === "safe"}
                onClick={() => onFilterChange("safe")}
            />
            <StatCard
                label="Phishing"
                value={stats.phishing}
                color="red"
                isActive={filter === "phishing"}
                onClick={() => onFilterChange("phishing")}
            />
        </Group>
    );
}
