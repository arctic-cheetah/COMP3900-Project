import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach, afterEach, type Mock } from "vitest";
import { MantineProvider } from "@mantine/core";
import HomePage from "../HomePage.js";
import * as api from "../api.js";

beforeEach(() => {
    const el = document.createElement("div");
    el.id = "result";
    document.body.appendChild(el);
});

afterEach(() => {
    document.body.innerHTML = "";
});

vi.mock("../api.js", () => ({
    scanURL: vi.fn(),
    getStoredData: vi.fn(() => Promise.resolve({ scans: [] }))
}));

// kill the stuff we aren't testing in this file
vi.mock("../Navbar.js", () => ({
    default: () => <nav />,
}));

vi.mock("../HistoricData.js", () => ({
    default: () => <section>History Section</section>,
}));

vi.mock("../Resultmodal.js", () => ({
    default: ({ result }: { result: any }) => (
        <div id="modal-result">
            {result?.is_safe ? "Verified" : "Danger"}
        </div>
    ),
}));

vi.mock("@mantine/core", async () => {
    const actual = await vi.importActual("@mantine/core");
    return {
        ...actual,
        Loader: () => <span>loading...</span>,
    };
});

vi.mock("@mantine/hooks", () => ({
    useMediaQuery: () => true,
}));

const renderWithMantine = (ui: React.ReactElement) =>
    render(<MantineProvider>{ui}</MantineProvider>);

describe("HomePage Logic", () => {
    it("handles input changes and toggles the submit button", () => {
        renderWithMantine(<HomePage />);

        const urlInput = screen.getByPlaceholderText(/enter url/i) as HTMLInputElement;
        const submitBtn = screen.getByRole("button", { name: /analyse/i });

        // button should be locked if there's no text
        expect(submitBtn).toBeDisabled();

        fireEvent.change(urlInput, { target: { value: "https://fake-url.test" } });

        // make sure the state actually updates
        expect(urlInput.value).toBe("https://fake-url.test");
        expect(submitBtn).not.toBeDisabled();
    });

    it("triggers the scanURL API call on submit", async () => {
        (api.scanURL as Mock).mockResolvedValue({
            is_safe: true,
            confidence: 0.99,
        });

        renderWithMantine(<HomePage />);

        fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
            target: { value: "https://fake-url.test" },
        });

        fireEvent.click(screen.getByRole("button", { name: /analyse/i }));

        await waitFor(() => {
            expect(api.scanURL).toHaveBeenCalledWith("https://fake-url.test");
        });
    });

    it("renders 'Verified' when API returns safe", async () => {
        (api.scanURL as Mock).mockResolvedValue({ is_safe: true });

        renderWithMantine(<HomePage />);

        fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
            target: { value: "https://fake-url.test" },
        });

        fireEvent.click(screen.getByRole("button", { name: /analyse/i }));

        await waitFor(() => {
            const badge = screen.getByText("Safe", {
                selector: ".mantine-Badge-label",
            });

            expect(badge).toBeInTheDocument();
        });
    });
});
