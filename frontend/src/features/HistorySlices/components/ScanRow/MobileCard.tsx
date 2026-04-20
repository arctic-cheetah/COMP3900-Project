/**
 * MobileScanCard Component
 * Responsibility: Render scan as card for mobile view
 */

import { Paper, Group, Badge, Text, Checkbox } from "@mantine/core";
import {
    IconCheck,
    IconAlertTriangle,
    IconClock,
} from "@tabler/icons-react";
import { format } from "date-fns";
import type { Scan, MobileScanCardProps } from "../../types.js";

export function MobileScanCard({
    scan,
    isSelected,
    onToggleSelect,
    onClick,
}: MobileScanCardProps) {
    return (
        <Paper
            p="md"
            withBorder
            radius="md"
            onClick={onClick}
            style={{
                cursor: "pointer",
                borderLeft: `4px solid ${scan.isSafe
                    ? "var(--mantine-color-green-6)"
                    : "var(--mantine-color-red-6)"
                    }`,
            }}
        >
            <Group justify="space-between" mb="xs" wrap="nowrap">
                <Checkbox
                    checked={isSelected}
                    onChange={() => onToggleSelect(scan)}
                    onClick={(e) => e.stopPropagation()}
                />
                <Badge
                    color={scan.isSafe ? "green" : "red"}
                    variant="light"
                    leftSection={
                        scan.isSafe ? (
                            <IconCheck size={12} />
                        ) : (
                            <IconAlertTriangle size={12} />
                        )
                    }
                >
                    {scan.isSafe ? "Safe" : "Phishing"}
                </Badge>
            </Group>

            <Text
                size="sm"
                ff="monospace"
                style={{ wordBreak: "break-all" }}
                mb="xs"
                fw={500}
            >
                {scan.url}
            </Text>

            <Group justify="space-between">
                <Group gap={4}>
                    <IconClock size={14} color="gray" />
                    <Text size="xs" c="dimmed">
                        {format(new Date(scan.timestamp), "MMM d, h:mm a")}
                    </Text>
                </Group>
                <Text size="xs" fw={700}>
                    {scan.confidence}% Score
                </Text>
            </Group>
        </Paper>
    );
}
