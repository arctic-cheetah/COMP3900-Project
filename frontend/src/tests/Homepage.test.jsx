import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import HomePage from "../HomePage";
import * as api from "../api";
import { vi } from "vitest";

beforeEach(() => {
    const el = document.createElement("div");
    el.id = "result";
    document.body.appendChild(el);
});

afterEach(() => {
    document.body.innerHTML = "";
});

vi.mock("../api", () => ({
    scanURL: vi.fn(),
}));

// kill the stuff we aren't testing in this file
vi.mock("../Navbar", () => ({
    default: () => <nav />,
}));

vi.mock("../HistoricData", () => ({
    default: () => <section>History Section</section>,
}));

vi.mock("../Resultmodal", () => ({
    default: ({ result }) => (
        <div id="modal-result">
            {result?.isSafe ? "Verified" : "Danger"}
        </div>
    ),
}));

vi.mock("@mantine/core", () => ({
    Loader: () => <span>loading...</span>,
}));

vi.mock("@mantine/hooks", () => ({
    useMediaQuery: () => true,
}));

describe("HomePage Logic", () => {
    it("handles input changes and toggles the submit button", () => {
        render(<HomePage />);

        const urlInput = screen.getByPlaceholderText(/enter url/i);
        const submitBtn = screen.getByRole("button", { name: /analyse/i });

        // button should be locked if there's no text
        expect(submitBtn).toBeDisabled();

        fireEvent.change(urlInput, { target: { value: "https://fake-url.test" } });

        // make sure the state actually updates
        expect(urlInput.value).toBe("https://fake-url.test");
        expect(submitBtn).not.toBeDisabled();
    });

    it("triggers the scanURL API call on submit", async () => {
        api.scanURL.mockResolvedValue({
            is_safe: true,
            confidence: 0.99,
        });

        render(<HomePage />);

        fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
            target: { value: "https://fake-url.test" },
        });

        fireEvent.click(screen.getByRole("button", { name: /analyse/i }));

        await waitFor(() => {
            expect(api.scanURL).toHaveBeenCalledWith("https://fake-url.test");
        });
    });

    it("renders 'Verified' when API returns safe", async () => {
        api.scanURL.mockResolvedValue({ is_safe: true });

        render(<HomePage />);

        fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
            target: { value: "https://fake-url.test" },
        });

        fireEvent.click(screen.getByRole("button", { name: /analyse/i }));

        await waitFor(() => {
            expect(screen.getByText(/verified/i)).toBeInTheDocument();
        });
    });
});
