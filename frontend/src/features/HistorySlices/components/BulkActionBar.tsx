/**
 * BulkActionBar Component
 * Responsibility: Display bulk delete action bar
 */

import { Group, Text, Button, Checkbox } from "@mantine/core";
import { IconTrash } from "@tabler/icons-react";

interface BulkActionBarProps {
    selectedCount: number;
    isAllSelected: boolean;
    isPartiallySelected: boolean;
    isMobileView?: boolean;
    onToggleAll: () => void;
    onDelete: () => void;
}

export function BulkActionBar({
    selectedCount,
    isAllSelected,
    isPartiallySelected,
    isMobileView = false,
    onToggleAll,
    onDelete,
}: BulkActionBarProps) {
    // Hide if nothing selected
    if (selectedCount === 0) return null;

    return (
        <Group
            justify="space-between"
            p="xs"
            mb="md"
            bg="red.0"
            style={{
                borderRadius: "8px",
                border: "1px solid var(--mantine-color-red-2)",
            }}
        >
            <Group gap="xs">
                <Checkbox
                    size="xs"
                    checked={isAllSelected}
                    indeterminate={isPartiallySelected}
                    onChange={onToggleAll}
                    label={isMobileView ? "All" : "Select All"}
                />
                <Text size="sm" fw={600} c="red.7">
                    {selectedCount} {isMobileView ? "" : "items"} selected
                </Text>
            </Group>

            <Button
                color="red"
                size="compact-xs"
                variant="light"
                leftSection={<IconTrash size={14} />}
                onClick={onDelete}
            >
                Delete
            </Button>
        </Group>
    );
}
