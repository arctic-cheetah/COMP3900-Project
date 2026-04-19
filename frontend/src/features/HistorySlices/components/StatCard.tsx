/**
 * StatCard Component
 * Responsibility: Display individual stat card
 */

import { UnstyledButton, Text } from "@mantine/core";
import type { CSSProperties } from "react";

interface StatCardProps {
    label: string;
    value: number;
    color: string;
    isActive: boolean;
    onClick: () => void;
}

export function StatCard({
    label,
    value,
    color,
    isActive,
    onClick,
}: StatCardProps) {
    const baseStyle: CSSProperties = {
        backgroundColor: `var(--mantine-color-${color}-light)`,
        border: `2px solid ${isActive
            ? `var(--mantine-color-${color}-filled)`
            : "var(--mantine-color-gray-2)"
            }`,
        transition: "all 0.2s ease",
        borderRadius: "8px",
        cursor: "pointer",
    };

    return (
        <UnstyledButton onClick={onClick} p="lg" style={baseStyle}>
            <Text fw={700} size="xl" c={isActive ? `${color}.7` : "dark"}>
                {value}
            </Text>
            <Text size="xs" fw={600} c="dimmed" tt="uppercase">
                {label}
            </Text>
        </UnstyledButton>
    );
}
