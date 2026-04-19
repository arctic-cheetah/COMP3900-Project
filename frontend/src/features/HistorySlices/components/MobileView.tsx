/**
 * MobileHistoryView Component
 * Responsibility: Render full mobile modal view with all features
 */

import {
    Button,
    Modal,
    Stack,
    ScrollArea,
    Text,
} from "@mantine/core";
import { IconHistory, IconX, IconTrash } from "@tabler/icons-react";
import type { Scan, FilterType, HistoryStats } from "../types.js";
import { StatsSection } from "./StatsSection.js";
import { BulkActionBar } from "./BulkActionBar.js";
import { MobileScanCard } from "./ScanRow/index.js";
import { computeSelectionStates } from "../hooks/index.js";

interface MobileHistoryViewProps {
    opened: boolean;
    onOpen: () => void;
    onClose: () => void;
    totalScans: number;
    filteredData: Scan[];
    stats: HistoryStats;
    filter: FilterType;
    selection: Scan[];
    onFilterChange: (filter: FilterType) => void;
    onToggleRow: (scan: Scan) => void;
    onToggleAll: () => void;
    onBulkDelete: () => void;
    onRowClick: (scan: Scan) => void;
}

export function MobileHistoryView({
    opened,
    onOpen,
    onClose,
    totalScans,
    filteredData,
    stats,
    filter,
    selection,
    onFilterChange,
    onToggleRow,
    onToggleAll,
    onBulkDelete,
    onRowClick,
}: MobileHistoryViewProps) {
    const { isAllSelected, isPartiallySelected } = computeSelectionStates(
        selection,
        filteredData
    );

    return (
        <>
            {/* Button to open modal */}
            <Button
                onClick={onOpen}
                fullWidth
                size="lg"
                variant="light"
                leftSection={<IconHistory size={20} />}
            >
                View Scan History ({totalScans})
            </Button>

            {/* Modal content */}
            <Modal
                opened={opened}
                onClose={onClose}
                title="Scan History"
                fullScreen
                padding="md"
                closeButtonProps={{ icon: <IconX size={18} />, color: "red" }}
            >
                <Stack gap="md">
                    <Button
                        onClick={onClose}
                        color="red"
                        variant="light"
                        leftSection={<IconX size={16} />}
                    >
                        Close
                    </Button>
                    <StatsSection
                        stats={stats}
                        filter={filter}
                        onFilterChange={onFilterChange}
                    />
                    <BulkActionBar
                        selectedCount={selection.length}
                        isAllSelected={isAllSelected}
                        isPartiallySelected={isPartiallySelected}
                        isMobileView
                        onToggleAll={onToggleAll}
                        onDelete={onBulkDelete}
                    />
                </Stack>

                <ScrollArea.Autosize mah="calc(100vh - 220px)">
                    <Stack gap="md" py="md">
                        {filteredData.length === 0 ? (
                            <Text ta="center" py="xl" c="dimmed">
                                No scans found
                            </Text>
                        ) : (
                            filteredData.map((scan) => (
                                <MobileScanCard
                                    key={scan.url + scan.timestamp}
                                    scan={scan}
                                    isSelected={selection.includes(scan)}
                                    onToggleSelect={onToggleRow}
                                    onClick={() => onRowClick(scan)}
                                />
                            ))
                        )}
                        {selection.length > 0 && (
                            <Button
                                color="red"
                                fullWidth
                                leftSection={<IconTrash size={16} />}
                                onClick={onBulkDelete}
                            >
                                Delete {selection.length} Selected
                            </Button>
                        )}
                    </Stack>
                </ScrollArea.Autosize>
            </Modal>
        </>
    );
}
