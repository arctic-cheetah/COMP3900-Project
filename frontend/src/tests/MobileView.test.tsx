import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeAll } from "vitest";
import { MantineProvider, createTheme } from "@mantine/core";
import { MobileHistoryView } from "../features/HistorySlices/components/MobileView.js";
import type { FilterType } from "../features/HistorySlices/types.js";

beforeAll(() => {
    global.ResizeObserver = class {
        observe() { }
        unobserve() { }
        disconnect() { }
    };
});

const theme = createTheme({});

const renderWithMantine = (ui: React.ReactElement) =>
    render(<MantineProvider theme={theme}>{ui}</MantineProvider>);

// Mock scan data
const MOCK_SCAN = {
    url: "https://example.com",
    isSafe: true,
    timestamp: "2025-01-01",
    confidence: 90,
};

const baseProps = {
    opened: true,
    onOpen: vi.fn(),
    onClose: vi.fn(),
    totalScans: 1,
    filteredData: [MOCK_SCAN],
    stats: { total: 1, safe: 1, phishing: 0 },
    filter: "all" as FilterType,
    selection: [] as any[],
    onFilterChange: vi.fn(),
    onToggleRow: vi.fn(),
    onToggleAll: vi.fn(),
    onBulkDelete: vi.fn(),
    onRowClick: vi.fn(),
};

describe("MobileHistoryView (MobileView)", () => {

    // Check that the button to open the modal is visible
    it("renders open button with scan count", () => {
        renderWithMantine(<MobileHistoryView {...baseProps} opened={false} />);

        expect(
            screen.getByRole("button", { name: /view scan history/i })
        ).toBeInTheDocument();
    });

    // Clicking the main button should trigger modal open
    it("calls onOpen when open button is clicked", () => {
        renderWithMantine(<MobileHistoryView {...baseProps} opened={false} />);

        fireEvent.click(
            screen.getByRole("button", { name: /view scan history/i })
        );

        expect(baseProps.onOpen).toHaveBeenCalled();
    });

    // Modal content should be visible when opened = true
    it("renders modal content when opened", () => {
        renderWithMantine(<MobileHistoryView {...baseProps} />);

        expect(screen.getByText("Scan History")).toBeInTheDocument();
        expect(screen.getByText("https://example.com")).toBeInTheDocument();
    });

    // Clicking close should trigger onClose handler
    it("calls onClose when close button is clicked", () => {
        renderWithMantine(<MobileHistoryView {...baseProps} />);

        fireEvent.click(screen.getByText("Close"));
        expect(baseProps.onClose).toHaveBeenCalled();
    });

    // no scan data
    it("shows empty state when no scans exist", () => {
        renderWithMantine(
            <MobileHistoryView
                {...baseProps}
                filteredData={[]}
            />
        );

        expect(screen.getByText(/no scans found/i)).toBeInTheDocument();
    });

    // delete button should appear when iteams are selected
    it("shows bulk delete button when items are selected", () => {
        renderWithMantine(
            <MobileHistoryView
                {...baseProps}
                selection={[MOCK_SCAN]}
            />
        );

        expect(
            screen.getByText(/delete 1 selected/i)
        ).toBeInTheDocument();
    });

});
