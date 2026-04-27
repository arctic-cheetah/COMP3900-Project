/**
 * DesktopHistoryView Component
 * Responsibility: Render full desktop table view with all features
 */

import {
    Paper,
    Group,
    Stack,
    Title,
    Text,
    Select,
    Table,
    ScrollArea,
    Checkbox,
    Button,
} from "@mantine/core";
import { IconFilter, IconDownload } from "@tabler/icons-react";
import type { Scan, FilterType, HistoryStats } from "../types.js";
import { StatsSection } from "./StatsSection.js";
import { BulkActionBar } from "./BulkActionBar.js";
import { DesktopScanRow } from "./ScanRow/index.js";
import { computeSelectionStates, useExportScans } from "../hooks/index.js";

interface DesktopHistoryViewProps {
    filteredData: Scan[];
    stats: HistoryStats;
    filter: FilterType;
    selection: Scan[];
    onFilterChange: (filter: FilterType) => void;
    onToggleRow: (scan: Scan) => void;
    onToggleAll: () => void;
    onBulkDelete: () => void;
    onDeleteScan: (scan: Scan) => void;
}

export function DesktopHistoryView({
    filteredData,
    stats,
    filter,
    selection,
    onFilterChange,
    onToggleRow,
    onToggleAll,
    onBulkDelete,
    onDeleteScan,
}: DesktopHistoryViewProps) {
    const { isAllSelected, isPartiallySelected } = computeSelectionStates(
        selection,
        filteredData
    );

    const { handleExportCSV } = useExportScans(filteredData);

    return (
        <Paper p="xl" radius="md" withBorder shadow="sm">
            {/* Header with title and filter */}
            <Group justify="space-between" mb="xl" align="flex-start">
                <Stack gap={4}>
                    <Title order={3}>Past URLs Analysed</Title>
                    <Text size="sm" c="dimmed">
                        Review your recent scans and historical analysis results
                    </Text>
                </Stack>
                <Select
                    leftSection={<IconFilter size={16} />}
                    data={[
                        { value: "all", label: `All Results (${stats.total})` },
                        { value: "safe", label: `Safe (${stats.safe})` },
                        { value: "phishing", label: `Phishing (${stats.phishing})` },
                    ]}
                    value={filter}
                    onChange={(value) => onFilterChange((value as FilterType) || "all")}
                />
                <Button
                    onClick={handleExportCSV}
                    variant="light"
                    leftSection={<IconDownload size={16} />}
                >
                    Export CSV
                </Button>
            </Group>

            {/* Stats section */}
            <StatsSection
                stats={stats}
                filter={filter}
                onFilterChange={onFilterChange}
            />

            {/* Bulk action bar */}
            <BulkActionBar
                selectedCount={selection.length}
                isAllSelected={isAllSelected}
                isPartiallySelected={isPartiallySelected}
                onToggleAll={onToggleAll}
                onDelete={onBulkDelete}
            />

            {/* Table */}
            <ScrollArea h={400}>
                <Table verticalSpacing="md">
                    <Table.Thead
                        bg="gray.0"
                        style={{ position: "sticky", top: 0, zIndex: 1 }}
                    >
                        <Table.Tr>
                            <Table.Th w={40}>
                                <Checkbox
                                    checked={isAllSelected}
                                    indeterminate={isPartiallySelected}
                                    onChange={onToggleAll}
                                />
                            </Table.Th>
                            <Table.Th>URL</Table.Th>
                            <Table.Th>DATE/TIME ANALYSED</Table.Th>
                            <Table.Th>RESULT</Table.Th>
                            <Table.Th ta="right">EXPLANATIONS</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {filteredData.map((scan) => (
                            <DesktopScanRow
                                key={scan.url + scan.timestamp}
                                scan={scan}
                                isSelected={selection.includes(scan)}
                                onToggleSelect={onToggleRow}
                                onDelete={onDeleteScan}
                            />
                        ))}
                    </Table.Tbody>
                </Table>
            </ScrollArea>
        </Paper>
    );
}
