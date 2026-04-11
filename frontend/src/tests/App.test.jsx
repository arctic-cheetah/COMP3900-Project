import { render, screen } from "@testing-library/react";
import App from "../App";

vi.mock("../HomePage", () => ({
    default: () => <div data-testid="hp-mock">Home</div>
}));

describe("Root App Component", () => {
    it("should mount the HomePage on initial load", () => {
        render(<App />);
        // sanity check to make sure the app even starts
        const homeEl = screen.getByTestId("hp-mock");
        expect(homeEl).toBeInTheDocument();
    });
});
