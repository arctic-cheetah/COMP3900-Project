import './App.css';

const ResultModal = ({ result, onClose }) => {
  if (!result) return null;

  return (
    <div className="overlay">
      <div className="modal">
        <h2>Scan Results</h2>
        <p><strong>URL:</strong> {result.url}</p>

        <div className="result-icon">
          {result.isSafe ? '✅ URL IS SAFE!' : '⚠️ URL IS PHISHING'}
        </div>

        <p>Confidence: {Math.round(result.confidence)}%</p>
        <button onClick={onClose} className="close-button">Close</button>
      </div>
    </div>
  );
};

export default ResultModal;