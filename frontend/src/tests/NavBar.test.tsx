import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Navbar from "../Navbar.js";

describe("Navbar", () => {
    // Check that the site title is displayed
    it("renders the website name", () => {
        render(<Navbar />);
        expect(screen.getByText("Phishy Links")).toBeInTheDocument();
    });

    // Check that the logo image is in the document
    it("renders the logo image", () => {
        render(<Navbar />);

        const logo = document.querySelector(".logo");
        expect(logo).toBeInTheDocument();
    });

});
