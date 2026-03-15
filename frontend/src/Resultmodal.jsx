export default function Resultmodal({ result, onClose }) {
  if (!result) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <h2>Analysis Results</h2>

        <p>{result.isSafe ? "Safe URL" : "Phishing URL"}</p>
        <p>Confidence: {Math.round(result.confidence * 100)}%</p>
        <p>Analyzed URL: {result.url}</p>

      </div>
    </div>
  );
}