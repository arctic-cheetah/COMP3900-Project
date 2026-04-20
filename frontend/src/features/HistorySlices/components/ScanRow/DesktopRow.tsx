/**
 * DesktopScanRow Component
 * Responsibility: Render expandable scan row for desktop table
 */

import {
    Table,
    Checkbox,
    Text,
    Group,
    Badge,
    Button,
    Progress,
    Collapse,
    Box,
    Stack,
} from "@mantine/core";
import {
    IconCheck,
    IconAlertTriangle,
    IconTrash,
    IconChevronDown,
} from "@tabler/icons-react";
import { format } from "date-fns";
import { useDisclosure } from "@mantine/hooks";
import type { DesktopScanRowProps } from "../../types.js";

export function DesktopScanRow({
    scan,
    isSelected,
    onToggleSelect,
    onDelete,
}: DesktopScanRowProps) {
    const [opened, { toggle }] = useDisclosure(false);

    const handleDelete = (e: React.MouseEvent<HTMLButtonElement>) => {
        e.stopPropagation();
        if (
            window.confirm(
                `Are you sure you want to delete this scan for ${scan.url}?`
            )
        ) {
            onDelete(scan);
        }
    };

    return (
        <>
            <Table.Tr
                onClick={toggle}
                style={{
                    cursor: "pointer",
                    backgroundColor: opened ? "var(--mantine-color-gray-0)" : undefined,
                    transition: "background-color 0.2s ease",
                }}
            >
                <Table.Td onClick={(e) => e.stopPropagation()}>
                    <Checkbox
                        checked={isSelected}
                        onChange={() => onToggleSelect(scan)}
                    />
                </Table.Td>
                <Table.Td>
                    <Text size="sm" fw={500} truncate maw={300}>
                        {scan.url}
                    </Text>
                </Table.Td>
                <Table.Td>
                    <Text size="xs" c="dimmed">
                        {format(new Date(scan.timestamp), "MMM d, yyyy • h:mm a")}
                    </Text>
                </Table.Td>
                <Table.Td>
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
                </Table.Td>
                <Table.Td>
                    <Group justify="flex-end" gap="xs" wrap="nowrap">
                        <IconChevronDown
                            size={16}
                            color="gray"
                            style={{
                                transform: opened ? "rotate(180deg)" : "none",
                                transition: "transform 0.2s ease",
                            }}
                        />
                    </Group>
                </Table.Td>
            </Table.Tr>

            <Table.Tr>
                <Table.Td
                    colSpan={5}
                    p={0}
                    style={{ borderBottom: opened ? undefined : "none" }}
                >
                    <Collapse in={opened}>
                        <Box
                            p="md"
                            bg="gray.0"
                            style={{
                                borderTop: "1px solid var(--mantine-color-gray-2)",
                            }}
                        >
                            <Stack gap="md">
                                <Group justify="space-between" align="flex-start">
                                    <Stack gap="xs" style={{ flex: 1 }}>
                                        <Group
                                            justify="space-between"
                                            align="flex-start"
                                            style={{ width: "100%" }}
                                        >
                                            <Stack gap="xs" style={{ flex: 1 }}>
                                                <Text size="xs" fw={700} c="dimmed">
                                                    FULL URL
                                                </Text>
                                                <Text
                                                    size="sm"
                                                    ff="monospace"
                                                    style={{ wordBreak: "break-all" }}
                                                >
                                                    {scan.url}
                                                </Text>
                                            </Stack>
                                            <Stack gap="xs" style={{ minWidth: "200px" }}>
                                                <Text size="xs" fw={700} c="dimmed">
                                                    CONFIDENCE SCORE
                                                </Text>
                                                <Group gap="xs" align="flex-end">
                                                    <Progress
                                                        value={scan.confidence}
                                                        color={scan.isSafe ? "green" : "red"}
                                                        size="md"
                                                        w={80}
                                                        radius="xl"
                                                    />
                                                    <Text size="sm" fw={700} style={{ minWidth: "50px" }}>
                                                        {scan.confidence}%
                                                    </Text>
                                                </Group>
                                            </Stack>
                                        </Group>
                                    </Stack>
                                    <Button
                                        color="red"
                                        variant="light"
                                        size="xs"
                                        leftSection={<IconTrash size={14} />}
                                        onClick={handleDelete}
                                    >
                                        Delete Record
                                    </Button>
                                </Group>
                            </Stack>
                        </Box>
                    </Collapse>
                </Table.Td>
            </Table.Tr>
        </>
    );
}
