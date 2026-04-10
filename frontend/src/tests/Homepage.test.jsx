import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import HomePage from "../HomePage";
import * as api from "../api";

jest.mock("../src/api", () => ({
    scanURL: jest.fn(),
}))

// kill the stuff we aren't testing in this file
jest.mock("../src/Navbar", () => () => <nav />);
jest.mock("../src/HistoricData", () => () => <section>History Section</section>);
jest.mock("../src/Resultmodal", () => ({ result }) => (
    <div id="modal-result">{result?.is_safe ? "Verified" : "Danger"}</div>
));

jest.mock("@mantine/core", () => ({
    Loader: () => <span>loading...</span>,
}));

jest.mock("@mantine/hooks", () => ({
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

        const result = await screen.findByText(/verified/i);
        expect(result).toBeInTheDocument();
    });
});
