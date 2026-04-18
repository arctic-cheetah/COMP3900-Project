import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach, afterEach, beforeAll } from "vitest";
import { MantineProvider } from "@mantine/core";
import HistoricalData, { type Scan } from "../HistoricData.js";

beforeAll(() => {
    Object.defineProperty(window, "matchMedia", {
        writable: true,
        value: vi.fn().mockImplementation((query: string) => ({
            matches: false,
            media: query,
            onchange: null,
            addListener: vi.fn(),
            removeListener: vi.fn(),
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
            dispatchEvent: vi.fn(),
        })),
    });

    global.ResizeObserver = class {
        observe() { }
        unobserve() { }
        disconnect() { }
    };
});

vi.mock("@mantine/hooks", async (importOriginal) => {
    const actual = await importOriginal<typeof import("@mantine/hooks")>();
    return {
        ...actual,
        useMediaQuery: () => false,
    };
});

const renderWithMantine = (ui: React.ReactElement) =>
    render(<MantineProvider>{ui}</MantineProvider>);

const MOCK_SCANS: Scan[] = [
    {
        url: "https://safe-url.test",
        isSafe: true,
        timestamp: "2025-01-01T10:00:00Z",
        confidence: 95,
    },
    {
        url: "https://fake-url.test",
        isSafe: false,
        timestamp: "2025-01-02T11:00:00Z",
        confidence: 23,
    },
];

const makeProps = (overrides = {}) => ({
    history: MOCK_SCANS,
    onDelete: vi.fn(),
    onDeleteMultiple: vi.fn(),
    onHistoryClick: vi.fn(),
    ...overrides,
});

describe("HistoricalData — persistence", () => {
    beforeEach(() => {
        vi.spyOn(window, "confirm").mockReturnValue(true);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it("shows saved URLs when history is loaded", () => {
        renderWithMantine(<HistoricalData {...makeProps()} />);

        expect(screen.getAllByText("https://safe-url.test")[0]).toBeInTheDocument();
        expect(screen.getAllByText("https://fake-url.test")[0]).toBeInTheDocument();
    });

    // click the row to expand it, then hit delete — url should be gone
    it("removes a URL from the list when deleted", async () => {
        const onDelete = vi.fn();
        renderWithMantine(<HistoricalData {...makeProps({ onDelete })} />);

        fireEvent.click(screen.getAllByText("https://fake-url.test")[0]!);

        const deleteBtn = await screen.findByRole("button", { name: /delete record/i });
        fireEvent.click(deleteBtn);

        expect(onDelete).toHaveBeenCalledWith(MOCK_SCANS[1]);
    });
});
