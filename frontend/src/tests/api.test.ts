import { vi, describe, beforeEach, afterEach, it, expect, type Mock } from "vitest";
import { scanURL } from "../api.js";

describe("API Service Layer", () => {
    const MOCK_URL = "https://fake-url.test";

    beforeEach(() => {
        global.fetch = vi.fn() as Mock;
    });

    afterEach(() => {
        vi.resetAllMocks();
    });

    it("successfully parses data on valid response", async () => {
        const mockData = { is_safe: false, score: 0.2 };

        (global.fetch as Mock).mockResolvedValue({
            ok: true,
            json: async () => mockData,
        });

        const out = await scanURL(MOCK_URL);

        expect(global.fetch).toHaveBeenCalledTimes(1);
        expect(out).toEqual(mockData);
    });

    it("throws error when response is not ok", async () => {
        (global.fetch as Mock).mockResolvedValue({
            ok: false,
            json: async () => ({ error: "Network Error 400" }),
        });

        await expect(scanURL(MOCK_URL))
            .rejects.toThrow(/network error 400/i);
    });
});
