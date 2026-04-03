import "./App.css";

import React, { useState } from "react";
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
} from "@mantine/core";
import {
  IconClock,
  IconCheck,
  IconAlertTriangle,
  IconFilter,
  IconTrash,
  IconHistory,
} from "@tabler/icons-react";
import { format } from "date-fns";
import { useMediaQuery, useDisclosure } from "@mantine/hooks";

export default function HistoricalData({ history, onDelete, onDeleteMultiple, onHistoryClick }) {
  const [filter, setFilter] = useState("all");

  const [selection, setSelection] = useState([]);

  const isMobile = useMediaQuery('(max-width: 768px)');
  const [opened, {open, close}] = useDisclosure(false);

  const filteredData = history.filter((item) => {
    if (filter === "all") return true;
    return filter === "safe" ? item.isSafe : !item.isSafe;
  });

  const toggleRow = (scan) => {
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

    if (window.confirm(`Are you sure you want to delete ${selection.length} selected scans?`)) {
      onDeleteMultiple(selection);
      setSelection([]);
    }
  };


  const renderTableHeader = () => (
    <Table.Tr>
      <Table.Th w={40}>
        <Checkbox
          checked={selection.length > 0 && selection.length === filteredData.length}
          indeterminate={selection.length > 0 && selection.length < filteredData.length}
          onChange={toggleAll}
        />
      </Table.Th>
      <Table.Th>URL</Table.Th>
      <Table.Th>DATE/TIME ANALYSED</Table.Th>
      <Table.Th>RESULT</Table.Th>
      <Table.Th ta="right">CONFIDENCE SCORE</Table.Th>
    </Table.Tr>
  );
    
  const stats = {
    total: history.length,
    safe: history.filter((h) => h.isSafe).length,
    phishing: history.filter((h) => !h.isSafe).length,
  };

  const rows = filteredData.map((scan, index) => (
  <Table.Tr 
    key={index} 
    onClick={() => onHistoryClick(scan)} 
    style={{ cursor: 'pointer' }}
  >
    <Table.Td onClick={(e) => e.stopPropagation()}>
      <Checkbox
        checked={selection.includes(scan)}
        onChange={() => toggleRow(scan)}
      />
    </Table.Td>
    <Table.Td>
      <Text size="sm" fw={500} truncate maxWidth={300}>{scan.url}</Text>
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
        leftSection={scan.isSafe ? <IconCheck size={12}/> : <IconAlertTriangle size={12}/>}
      >
        {scan.isSafe ? "Safe" : "Phishing"}
      </Badge>
    </Table.Td>
    <Table.Td ta="right">
      <Group justify="flex-end" gap="xs">
        <Text size="sm" fw={700}>{scan.confidence}%</Text>
        <Progress value={scan.confidence} color={scan.isSafe ? "green" : "red"} size="sm" w={50} radius="xl" />
      </Group>
    </Table.Td>
  </Table.Tr>
));

  return (
    <Paper p="xl" radius="md" withBorder shadow="sm">
      {/* Header Section */}
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

      {/* Stats Cards Section */}
      <Group grow mb="xl">
        <StatCard
          label="Total Scans"
          value={stats.total}
          color="blue"
          active={filter === "all"}
          onClick={() => setFilter("all")}
        />
        <StatCard
          label="Safe URLs"
          value={stats.safe}
          color="green"
          active={filter === "safe"}
          onClick={() => setFilter("safe")}
        />
        <StatCard
          label="Phishing Detected"
          value={stats.phishing}
          color="red"
          active={filter === "phishing"}
          onClick={() => setFilter("phishing")}
        />
      </Group>

      {selection.length > 0 && (
        <Group justify="flex-start" mb="md" p="xs" bg="red.0" style={{ borderRadius: '8px' }}>
          <Text size="sm" fw={500} c="red.7">{selection.length} items selected</Text>
          <Button 
            color="red" 
            size="xs" 
            variant="light" 
            leftSection={<IconTrash size={14} />} 
            onClick={handleBulkDelete}
          >
            Delete Selected
          </Button>
        </Group>
      )}

      {/* Table Section */}
      <ScrollArea h={400}>
        <Table verticalSpacing="md">
          <Table.Thead
            bg="gray.0"
            style={{ position: "sticky", top: 0, zIndex: 1 }}
          >
            {renderTableHeader()}
          </Table.Thead>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </ScrollArea>
    </Paper>
  );
}

function StatCard({ label, value, color, active, onClick }) {
  return (
    <UnstyledButton
      onClick={onClick}
      p="lg"
      radius="md"
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
