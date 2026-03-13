import React, { useState } from 'react';
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
  Box,
  UnstyledButton,
  ScrollArea
} from '@mantine/core';
import { IconClock, IconCheck, IconAlertTriangle, IconFilter } from '@tabler/icons-react';
import { format } from 'date-fns';

export default function HistoricalData({ history }) {
  const [filter, setFilter] = useState('all');

  const filteredData = history.filter((item) => {
    if (filter === 'all') return true;
    return filter === 'safe' ? item.isSafe : !item.isSafe;
  });

  const stats = {
    total: history.length,
    safe: history.filter(h => h.isSafe).length,
    phishing: history.filter(h => !h.isSafe).length
  };

  const rows = filteredData.map((scan, index) => (
    <Table.Tr key={index}>
      <Table.Td style={{ fontFamily: 'monospace' }}>{scan.url}</Table.Td>
      <Table.Td>
        <Group gap="xs">
          <IconClock size={16} color="gray" />
          <Box>
            <Text size="sm">{format(scan.timestamp, 'MMM d, yyyy')}</Text>
            <Text size="xs" c="dimmed">{format(scan.timestamp, 'p')}</Text>
          </Box>
        </Group>
      </Table.Td>
      <Table.Td>
        <Badge 
          color={scan.isSafe ? 'green' : 'red'} 
          variant="light" 
          leftSection={scan.isSafe ? <IconCheck size={12} /> : <IconAlertTriangle size={12} />}
          size="lg"
        >
          {scan.isSafe ? 'Safe' : 'Phishing'}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Group justify="flex-end" gap="sm">
          <Box style={{ width: 100 }}>
            <Progress 
              value={scan.confidence} 
              color={scan.isSafe ? 'green' : 'red'} 
              size="sm" 
              radius="xl" 
            />
          </Box>
          <Text size="sm" fw={700}>{scan.confidence}%</Text>
        </Group>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Paper p="xl" radius="md" withBorder shadow="sm">
      {/* Header Section */}
      <Group justify="space-between" mb="xl" align="flex-start">
        <Stack gap={4}>
          <Title order={3}>Past URLs Analyzed</Title>
          <Text size="sm" c="dimmed">Review your recent scans and historical analysis results</Text>
        </Stack>
        <Select
          leftSection={<IconFilter size={16} />}
          data={[
            { value: 'all', label: `All Results (${stats.total})` },
            { value: 'safe', label: `Safe (${stats.safe})` },
            { value: 'phishing', label: `Phishing (${stats.phishing})` },
          ]}
          value={filter}
          onChange={setFilter}
        />
      </Group>

      {/* Stats Cards Section */}
      <Group grow mb="xl">
        <StatCard 
          label="Total Scans" value={stats.total} color="blue" 
          active={filter === 'all'} onClick={() => setFilter('all')} 
        />
        <StatCard 
          label="Safe URLs" value={stats.safe} color="green" 
          active={filter === 'safe'} onClick={() => setFilter('safe')} 
        />
        <StatCard 
          label="Phishing Detected" value={stats.phishing} color="red" 
          active={filter === 'phishing'} onClick={() => setFilter('phishing')} 
        />
      </Group>

      {/* Table Section */}
      <ScrollArea h={400}>
        <Table verticalSpacing="md">
          <Table.Thead bg="gray.0" style={{ position: 'sticky', top: 0, zIndex: 1 }}>
            <Table.Tr>
              <Table.Th>URL</Table.Th>
              <Table.Th>DATE/TIME ANALYZED</Table.Th>
              <Table.Th>RESULT</Table.Th>
              <Table.Th textAlign="right">CONFIDENCE SCORE</Table.Th>
            </Table.Tr>
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
        border: `2px solid ${active ? `var(--mantine-color-${color}-filled)` : 'var(--mantine-color-gray-2)'}`,
        transition: 'all 0.2s ease',
        borderRadius: '8px',
        cursor: 'pointer',
        '&:hover': {
          borderColor: `var(--mantine-color-${color}-filled)`,
          backgroundColor: `var(--mantine-color-${color}-light)`,
        },
      }}
    >
      <Text fw={700} size="xl" c={active ? `${color}.7` : 'dark'}>{value}</Text>
      <Text size="xs" fw={600} c="dimmed" tt="uppercase">{label}</Text>
    </UnstyledButton>
  );
}