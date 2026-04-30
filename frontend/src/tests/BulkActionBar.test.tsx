import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MantineProvider, createTheme } from "@mantine/core";
import { BulkActionBar } from "../features/HistorySlices/components/BulkActionBar.js";

const theme = createTheme({});

const renderWithMantine = (ui: React.ReactElement) =>
    render(<MantineProvider theme={theme}>{ui}</MantineProvider>);

describe("BulkActionBar", () => {

    // If nothing is selected, the bar should not appear
    it("renders nothing when selectedCount is 0", () => {
        renderWithMantine(
            <BulkActionBar
                selectedCount={0}
                isAllSelected={false}
                isPartiallySelected={false}
                onToggleAll={vi.fn()}
                onDelete={vi.fn()}
            />
        );

        expect(screen.queryByText(/selected/i)).not.toBeInTheDocument();
    });

    // Check that the correct number of selected items is shown
    it("renders selected count correctly", () => {
        renderWithMantine(
            <BulkActionBar
                selectedCount={3}
                isAllSelected={false}
                isPartiallySelected={false}
                onToggleAll={vi.fn()}
                onDelete={vi.fn()}
            />
        );

        expect(screen.getByText("3 items selected")).toBeInTheDocument();
    });

    // In mobile view, text should be shorter
    it("renders mobile view text correctly", () => {
        renderWithMantine(
            <BulkActionBar
                selectedCount={2}
                isAllSelected={false}
                isPartiallySelected={false}
                isMobileView={true}
                onToggleAll={vi.fn()}
                onDelete={vi.fn()}
            />
        );

        expect(screen.getByText(/2. *selected/i)).toBeInTheDocument();
        expect(screen.getByText("All")).toBeInTheDocument();
    });

    // Clicking checkbox should trigger toggle handler
    it("calls onToggleAll when checkbox is clicked", () => {
        const onToggleAll = vi.fn();

        renderWithMantine(
            <BulkActionBar
                selectedCount={2}
                isAllSelected={false}
                isPartiallySelected={false}
                onToggleAll={onToggleAll}
                onDelete={vi.fn()}
            />
        );
        fireEvent.click(screen.getByRole("checkbox"));
        expect(onToggleAll).toHaveBeenCalled();
    });

    // Clicking delete should trigger delete
    it("calls onDelete when delete button is clicked", () => {
        const onDelete = vi.fn();

        renderWithMantine(
            <BulkActionBar
                selectedCount={2}
                isAllSelected={false}
                isPartiallySelected={false}
                onToggleAll={vi.fn()}
                onDelete={onDelete}
            />
        );
        fireEvent.click(screen.getByText("Delete"));
        expect(onDelete).toHaveBeenCalled();
    });

    // Checkbox should reflect whether all items are selected
    it("checkbox reflects selection state", () => {
        renderWithMantine(
            <BulkActionBar
                selectedCount={2}
                isAllSelected={true}
                isPartiallySelected={false}
                onToggleAll={vi.fn()}
                onDelete={vi.fn()}
            />
        );

        const checkbox = screen.getByRole("checkbox") as HTMLInputElement;
        expect(checkbox.checked).toBe(true);
    });

});
