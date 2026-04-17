import "./App.css";

import { useState } from "react";
import {
  Table,
  Badge,
  Text,
  Group,
  Paper,
  Select,
  Progress,
  Stack,
  Title,
  UnstyledButton,
  ScrollArea,
  Checkbox,
  Button,
  Modal,
  Box,
  Collapse,
} from "@mantine/core";
import {
  IconClock,
  IconCheck,
  IconAlertTriangle,
  IconFilter,
  IconTrash,
  IconHistory,
  IconX,
  IconChevronDown,
} from "@tabler/icons-react";
import { format } from "date-fns";
import { useMediaQuery, useDisclosure } from "@mantine/hooks";

// Types and interfaces
export interface Scan {
  url: string;
  isSafe: boolean;
  timestamp: string | number | Date;
  confidence: number;
};

interface HistoricalDataProps {
  history: Scan[];
  onDelete: (scan: Scan) => void;
  onDeleteMultiple: (scans: Scan[]) => void;
  onHistoryClick: (scan: Scan) => void;
};

interface Stats {
  total: number;
  safe: number;
  phishing: number;
}

// Main component logic
export default function HistoricalData({
  history,
  onDelete,
  onDeleteMultiple,
  onHistoryClick,
}: HistoricalDataProps) {
  const [filter, setFilter] = useState<string | null>("all");
  const [selection, setSelection] = useState<Scan[]>([]);

  const isMobile = useMediaQuery("(max-width: 768px)");
  const [opened, { open, close }] = useDisclosure(false);

  // stuff derived from state
  const filteredData = history.filter((item) => {
    if (filter === "all") return true;
    return filter === "safe" ? item.isSafe : !item.isSafe;
  });

    const toggleRow = (scan: Scan) => {
    setSelection((current) =>
      current.includes(scan)
      ? current.filter((item) => item !== scan)
      : [...current, scan]
    );
  };

  const toggleAll = () => {
    setSelection((current) =>
      current.length === filteredData.length ? [] : [...filteredData]
    );
  };

  const handleBulkDelete = () => {
    if (selection.length === 0) return;

    if (window.confirm(
      `Are you sure you want to delete ${selection.length} selected scans?`
    )) {
      onDeleteMultiple(selection);
      setSelection([]);
    }
  };

  const stats: Stats = {
    total: history.length,
    safe: history.filter((h) => h.isSafe).length,
    phishing: history.filter((h) => !h.isSafe).length,
  };

  const allSelected = selection.length > 0 && selection.length === filteredData.length;
  const partiallySelected = selection.length > 0 && selection.length < filteredData.length;

  const BulkActionBar = ({ isMobileView = false }: { isMobileView?: boolean }) => {
    if (selection.length === 0) return null;
    return (
      <Group
        justify="space-between"
        p="xs"
        mb="md"
        bg="red.0"
        style={{
          borderRadius: '8px',
          border: '1px solid var(--mantine-color-red-2)',
        }}
      >
        <Group gap="xs">
          <Checkbox
            size="xs"
            checked={allSelected}
            indeterminate={partiallySelected}
            onChange={toggleAll}
            label={isMobileView ? "All" : "Select All"}
          />
          <Text size="sm" fw={600} c="red.7">
            {selection.length} {isMobileView ? '' : 'items'} selected
          </Text>
        </Group>

        <Button
          color="red"
          size="compact-xs"
          variant="light"
          leftSection={<IconTrash size={14} />}
          onClick={handleBulkDelete}
        >
          Delete
        </Button>
      </Group>
    );
  };

  // Mobile version uses modal with a card layout
  if (isMobile) {
    return (
      <>
        <Button
          onClick={open} fullWidth size="lg" variant="light" leftSection={<IconHistory size={20} />}>
          View Scan History ({history.length})
        </Button>

        <Modal opened={opened} onClose={close} title="Scan History" fullScreen padding="md" closeButtonProps={{ icon: <IconX size={18} />, color: 'red' }}>
          <Stack gap="md">
            <Button onClick={close} color="red" variant="light" leftSection={<IconX size={16} />}>
              Close
            </Button>
            <StatsSection stats={stats} filter={filter} setFilter={setFilter} />
            <BulkActionBar isMobileView />
          </Stack>

          <ScrollArea.Autosize mah="calc(100vh - 220px)">
            <Stack gap="md" py="md">
              {filteredData.length === 0 ? (<Text ta="center" py="xl" c="dimmed">No scans found</Text>) : (
                filteredData.map((scan, i) => (
                  <Paper
                    key={i}
                    p="md"
                    withBorder
                    radius="md"
                    onClick={() => onHistoryClick(scan)}
                    style={{
                      cursor: "pointer",
                      borderLeft: `4px solid ${scan.isSafe ? "var(--mantine-color-green-6)" : "var(--mantine-color-red-6)"}`,
                    }}
                  >
                    <Group justify="space-between" mb="xs" wrap="nowrap">
                      <Checkbox
                        checked={selection.includes(scan)}
                        onChange={() => toggleRow(scan)}
                        onClick={(e) => e.stopPropagation()}
                      />
                      <Badge
                        color={scan.isSafe ? "green" : "red"}
                        variant="light"
                        leftSection={scan.isSafe ? <IconCheck size={12} /> : <IconAlertTriangle size={12} />}
                      >
                        {scan.isSafe ? "Safe" : "Phishing"}
                      </Badge>
                    </Group>

                    <Text size="sm" ff="monospace" style={{ wordBreak: "break-all" }} mb="xs" fw={500}>
                      {scan.url}
                    </Text>

                    <Group justify="space-between">
                      <Group gap={4}>
                        <IconClock size={14} color="gray" />
                        <Text size="xs" c="dimmed">
                          {format(new Date(scan.timestamp), "MMM d, h:mm a")}
                        </Text>
                      </Group>
                      <Text size="xs" fw={700}>{scan.confidence}% Score</Text>
                    </Group>
                  </Paper>
                ))
              )}
              {selection.length > 0 && (
                <Button color="red" fullWidth leftSection={<IconTrash size={16} />} onClick={handleBulkDelete}>
                  Delete {selection.length} Selected
                </Button>
              )}
            </Stack>
          </ScrollArea.Autosize>
        </Modal>
      </>
    );
  }

  // If its not mobile it will be desktop
  return (
    <Paper p="xl" radius="md" withBorder shadow="sm">
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
          onChange={setFilter}
        />
      </Group>

      <StatsSection
        stats={stats}
        filter={filter}
        setFilter={setFilter}
        labels={{ total: "Total Scans", safe: "Safe URLs", phishing: "Phishing Detected" }}
      />

      <BulkActionBar />

      <ScrollArea h={400}>
        <Table verticalSpacing="md">
          <Table.Thead bg="gray.0" style={{ position: "sticky", top: 0, zIndex: 1 }}>
            <Table.Tr>
              <Table.Th w={40}>
                <Checkbox
                  checked={allSelected}
                  indeterminate={partiallySelected}
                  onChange={toggleAll}
                />
              </Table.Th>
              <Table.Th>URL</Table.Th>
              <Table.Th>DATE/TIME ANALYSED</Table.Th>
              <Table.Th>RESULT</Table.Th>
              <Table.Th ta="right">DETAILS</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {filteredData.map((scan, i) => (
              <DesktopScanRow
                key={i}
                scan={scan}
                selection={selection}
                toggleRow={toggleRow}
                onDelete={onDelete}
              />
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Paper>
  );
}

// Reusable components to reduce duplicated code
function StatsSection({ stats, filter, setFilter }: any) {
  return (
    <Group grow mb="xl">
      <StatCard label="Total" value={stats.total} color="blue" active={filter === "all"} onClick={() => setFilter("all")} />
      <StatCard label="Safe" value={stats.safe} color="green" active={filter === "safe"} onClick={() => setFilter("safe")} />
      <StatCard label="Phishing" value={stats.phishing} color="red" active={filter === "phishing"} onClick={() => setFilter("phishing")} />
    </Group>
  );
}

interface StatCardProps {
  label: string;
  value: number;
  color: string;
  active: boolean;
  onClick: () => void;
}

function StatCard({
  label,
  value,
  color,
  active,
  onClick
}: StatCardProps) {
  return (
    <UnstyledButton
      onClick={onClick}
      p="lg"
      style={{
        backgroundColor: `var(--mantine-color-${color}-light)`,
        border: `2px solid ${active ? `var(--mantine-color-${color}-filled)` : "var(--mantine-color-gray-2)"}`,
        transition: "all 0.2s ease",
        borderRadius: "8px",
        cursor: "pointer",
        "&:hover": {
          borderColor: `var(--mantine-color-${color}-filled)`,
          backgroundColor: `var(--mantine-color-${color}-light)`,
        },
      }}
    >
      <Text fw={700} size="xl" c={active ? `${color}.7` : "dark"}>
        {value}
      </Text>
      <Text size="xs" fw={600} c="dimmed" tt="uppercase">
        {label}
      </Text>
    </UnstyledButton>
  );
}

// desktop row
interface DesktopRowProps {
  scan: Scan;
  selection: Scan[];
  toggleRow: (scan: Scan) => void;
  onDelete: (scan: Scan) => void;
};

function DesktopScanRow({
  scan,
  selection,
  toggleRow,
  onDelete
}: DesktopRowProps) {

  const [opened, { toggle }] = useDisclosure(false);
  const isSelected = selection.includes(scan);

  return (
    <>
      <Table.Tr
        onClick={toggle}
        style={{
          cursor: 'pointer',
          backgroundColor: opened ? 'var(--mantine-color-gray-0)' : undefined,
          transition: "background-color 0.2s ease"
        }}
      >
        <Table.Td onClick={(e) => e.stopPropagation()}>
          <Checkbox checked={isSelected} onChange={() => toggleRow(scan)} />
        </Table.Td>
        <Table.Td>
          <Text size="sm" fw={500} truncate maw={300}>{scan.url}</Text>
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
            leftSection={scan.isSafe ? <IconCheck size={12} /> : <IconAlertTriangle size={12} />}
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
                transform: opened ? "rotate(180deg)" : "nowe",
                transition: "transform 0.2s ease",
              }}
            />
          </Group>
        </Table.Td>
      </Table.Tr>

      <Table.Tr>
        <Table.Td colSpan={5} p={0} style={{ borderBottom: opened ? undefined : 'none' }}>
          <Collapse in={opened}>
            <Box p="md" bg="gray.0" style={{ borderTop: '1px solid var(--mantine-color-gray-2)' }}>
              <Stack gap="md">
                <Group justify="space-between" align="flex-start">
                  <Stack gap="xs" style={{ flex: 1 }}>
                    <Group justify="space-between" align="flex-start" style={{ width: '100%' }}>
                      <Stack gap="xs" style={{ flex: 1 }}>
                        <Text size="xs" fw={700} c="dimmed">FULL URL</Text>
                        <Text size="sm" ff="monospace" style={{ wordBreak: "break-all" }}>{scan.url}</Text>
                      </Stack>
                      <Stack gap="xs" style={{ minWidth: '200px' }}>
                        <Text size="xs" fw={700} c="dimmed">CONFIDENCE SCORE</Text>
                        <Group gap="xs" align="flex-end">
                          <Progress
                            value={scan.confidence}
                            color={scan.isSafe ? "green" : "red"}
                            size="md"
                            w={80}
                            radius="xl"
                          />
                          <Text size="sm" fw={700} style={{ minWidth: '50px' }}>{scan.confidence}%</Text>
                        </Group>
                      </Stack>
                    </Group>
                  </Stack>
                  <Button
                    color="red"
                    variant="light"
                    size="xs"
                    leftSection={<IconTrash size={14} />}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.confirm(`Are you sure you want to delete this scan for ${scan.url}?`)) {
                        onDelete(scan);
                      }
                    }}
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
