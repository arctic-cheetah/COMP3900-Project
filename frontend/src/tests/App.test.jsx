import { render, screen } from "@testing-library/react";
import App from "../App";

jest.mock("../src/HomePage", () => () => (
    <div data-testid="hp-mock">Home</div>
));

describe("Root App Component", () => {
    it("should mount the HomePage on initial load", () => {
        render(<App />);
        // sanity check to make sure the app even starts
        const homeEl = screen.getByTestId("hp-mock");
        expect(homeEl).toBeInTheDocument();
    });
});
