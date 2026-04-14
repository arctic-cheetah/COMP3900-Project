import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import HomePage from "../src/HomePage";
import * as api from "../src/api";

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

    fireEvent.change(urlInput, { target: { value: "https://google.com" } });
    
    // make sure the state actually updates
    expect(urlInput.value).toBe("https://google.com");
    expect(submitBtn).not.toBeDisabled();
  });

  it("triggers the scanURL API call on form submission", async () => {
    const apiSpy = jest.spyOn(api, "scanURL").mockResolvedValue({
      is_safe: true,
      confidence: 0.99
    });

    render(<HomePage />);

    fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
      target: { value: "https://test-site.org" }
    });
    
    fireEvent.click(screen.getByText(/analyse url/i));

    // need to wait for the async stuff to settle
    await waitFor(() => {
      expect(apiSpy).toHaveBeenCalledWith("https://test-site.org");
    });
  });

  it("renders the modal with 'Verified' when API returns safe", async () => {
    jest.spyOn(api, "scanURL").mockResolvedValue({ is_safe: true });

    render(<HomePage />);
    
    fireEvent.change(screen.getByPlaceholderText(/enter url/i), {
      target: { value: "https://safe.com" }
    });
    fireEvent.click(screen.getByText(/analyse url/i));

    // use findBy because it polls until the element shows up
    const result = await screen.findByText(/verified/i);
    expect(result).toBeInTheDocument();
  });
});