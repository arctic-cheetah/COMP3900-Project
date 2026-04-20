/**
 * HistoricData - Backward compatibility wrapper
 *
 * This file re-exports from the refactored vertical slices architecture.
 * The component has been reorganized for:
 * - Low Coupling: Each slice is independent
 * - High Cohesion: Related logic and UI together
 *
 * See: src/features/HistorySlices/ for the actual implementation
 */

import { HistoricData as HistoricDataComponent, type Scan } from "./features/HistorySlices/index.js";

/**
 * Backward compatible export - simply re-exports the refactored component
 */
export default HistoricDataComponent;

// Export types for consumers
export type { Scan };
