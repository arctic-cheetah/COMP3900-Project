import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom"; 
import { vi, describe, it, expect } from "vitest";
import App from "../App.js";

vi.mock("../HomePage.js", () => ({
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
