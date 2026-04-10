import { scanURL } from "../api";

describe("API Service Layer", () => {
    const MOCK_URL = "https://fake-url.test";

    beforeEach(() => {
        // clear everything before every test
        global.fetch = jest.fn();
    });

    afterEach(() => {
        jest.resetAllMocks();
    });

    it("successfully parses data on valid response", async () => {
        const mockData = { is_safe: false, score: 0.2 };

        fetch.mockResolvedValue({
            ok: true,
            json: async () => mockData,
        });

        const out = await scanURL(MOCK_URL);
        expect(fetch).toHaveBeenCalledTimes(1);
        expect(out).toEqual(mockData);
    });

    it("explodes with an error message when 'ok' is false", async () => {
        // simulate a 400/500 error from the server
        fetch.mockResolvedValue({
            ok: false,
            json: async () => ({ error: "Network Error 400" }),
        });

        // catch the throw in the scanURL function
        await expect(scanURL(MOCK_URL)).rejects.toThrow(/network error 400/i);
    });
});
