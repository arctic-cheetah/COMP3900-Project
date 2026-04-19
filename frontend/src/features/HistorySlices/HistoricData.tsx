/**
 * HistoricData - Main Component Orchestrator
 * Responsibility: Compose all slices and orchestrate their interactions
 *
 * Vertical Slices Architecture:
 * - Filtering Slice: useHistoryFiltering hook + StatsSection component
 * - Selection Slice: useHistorySelection hook + BulkActionBar component
 * - Desktop View Slice: DesktopHistoryView component + DesktopScanRow component
 * - Mobile View Slice: MobileHistoryView component + MobileScanCard component
 *
 */

import { useMediaQuery, useDisclosure } from "@mantine/hooks";
import {
    useHistoryFiltering,
    useHistorySelection,
} from "./hooks/index.js";
import {
    DesktopHistoryView,
    MobileHistoryView,
} from "./components/index.js";
import type { HistoricalDataProps } from "./types.js";

export default function HistoricData({
    history,
    onDelete,
    onDeleteMultiple,
    onHistoryClick,
}: HistoricalDataProps) {
    // Filtering Slice
    const { filter, setFilter, filteredData, stats } =
        useHistoryFiltering(history);

    // Selection Slice
    const {
        selection,
        toggleRow,
        toggleAll: selectionToggleAll,
        executeBulkDelete,
    } = useHistorySelection();

    // Mobile responsive hook
    const isMobile = useMediaQuery("(max-width: 768px)");
    const [mobileModalOpened, { open: openMobileModal, close: closeMobileModal }] =
        useDisclosure(false);

    // Handlers
    const handleToggleAll = () => {
        selectionToggleAll(filteredData);
    };

    const handleBulkDelete = () => {
        executeBulkDelete(onDeleteMultiple, filteredData);
    };

    // Render mobile view
    if (isMobile) {
        return (
            <MobileHistoryView
                opened={mobileModalOpened}
                onOpen={openMobileModal}
                onClose={closeMobileModal}
                totalScans={history.length}
                filteredData={filteredData}
                stats={stats}
                filter={filter}
                selection={selection}
                onFilterChange={setFilter}
                onToggleRow={toggleRow}
                onToggleAll={handleToggleAll}
                onBulkDelete={handleBulkDelete}
                onRowClick={onHistoryClick}
            />
        );
    }

    // Render desktop view
    return (
        <DesktopHistoryView
            filteredData={filteredData}
            stats={stats}
            filter={filter}
            selection={selection}
            onFilterChange={setFilter}
            onToggleRow={toggleRow}
            onToggleAll={handleToggleAll}
            onBulkDelete={handleBulkDelete}
            onDeleteScan={onDelete}
            onRowClick={onHistoryClick}
        />
    );
}

// Export types for consumers
export type { HistoricalDataProps, Scan, FilterType } from "./types.js";
