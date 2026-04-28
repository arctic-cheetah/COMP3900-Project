import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MantineProvider, createTheme } from "@mantine/core";
import ResultAnalysis from "../ResultAnalysis.js";

const theme = createTheme({});

const renderWithMantine = (ui: React.ReactElement) =>
    render(<MantineProvider theme={theme}>{ui}</MantineProvider>);

// mock data
const SAFE_RESULT = {
    isSafe: true,
    confidence: 85,
    url: "https://example-test.com",
    explanation: ["Valid SSL"],
};

const PHISH_RESULT = {
    isSafe: false,
    confidence: 30,
    url: "http://bad-site.com",
    explanation: ["Suspicious domain"],
};

describe("ResultAnalysis", () => {
    // if no result, modal doesnt render anything
    it("renders nothing when result = null", () => {
        renderWithMantine(<ResultAnalysis result={null} onClose={vi.fn()} />);
        expect(screen.queryByText("Analysis Results")).not.toBeInTheDocument();
    });
    // displays safe result properly
    it("renders safe result correctly", () => {
        renderWithMantine(<ResultAnalysis result={SAFE_RESULT} onClose={vi.fn()} />);

        expect(screen.getByText("Safe")).toBeInTheDocument();
        expect(
            screen.getByText(/legitimate and safe/i)
        ).toBeInTheDocument();
        expect(screen.getByText("85%")).toBeInTheDocument();
        expect(screen.getByText("https://example-test.com")).toBeInTheDocument();
    });

    // shows phishing result
    it("renders phishing result correctly", () => {
        renderWithMantine(<ResultAnalysis result={PHISH_RESULT} onClose={vi.fn()} />);

        expect(screen.getByText("Phishing")).toBeInTheDocument();
        expect(
            screen.getByText(/suspicious patterns/i)
        ).toBeInTheDocument();
        expect(screen.getByText("30%")).toBeInTheDocument();
    });

    // show xai pbadges if there is explanation
    it("renders explanation badges when present", () => {
        renderWithMantine(<ResultAnalysis result={SAFE_RESULT} onClose={vi.fn()} />);

        expect(screen.getByText("Valid SSL")).toBeInTheDocument();
    });

    // no section appears for explanation if there is none
    it("does not render explanation section when empty", () => {
        const resultNoExplanation = { ...SAFE_RESULT, explanation: [] };

        renderWithMantine(
            <ResultAnalysis result={resultNoExplanation} onClose={vi.fn()} />
        );

        expect(
            screen.queryByText("Why this result")
        ).not.toBeInTheDocument();
    });

    // close button clsoes modal
    it("calls onClose when close button is clicked", () => {
        const onClose = vi.fn();

        renderWithMantine(<ResultAnalysis result={SAFE_RESULT} onClose={onClose} />);

        fireEvent.click(screen.getByText("Close"));
        expect(onClose).toHaveBeenCalled();
    });

    // clicking outside of the box closes box
    it("calls onClose when overlay is clicked", () => {
        const onClose = vi.fn();

        const { container } = renderWithMantine(
            <ResultAnalysis result={SAFE_RESULT} onClose={onClose} />
        );

        fireEvent.click(container.querySelector(".overlay")!);
        expect(onClose).toHaveBeenCalled();
    });

    it("does NOT call onClose when clicking inside modal", () => {
        const onClose = vi.fn();

        renderWithMantine(<ResultAnalysis result={SAFE_RESULT} onClose={onClose} />);

        fireEvent.click(screen.getByText("Analysis Results"));
        expect(onClose).not.toHaveBeenCalled();
    });
});
