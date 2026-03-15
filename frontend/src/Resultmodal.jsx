import './ResultModal.css';

const ResultModal = ({ result, onClose }) => {
  if (!result) return null;

  return (
    <div className='overlay'>
      <div className='modal'>
        <p className='analysis-result-text'>Analysis Results</p>

        <div className='result-icon'>
          {result.isSafe ? '✅ URL IS SAFE!' : '⚠️ URL IS PHISHING'}
        </div>

        <div className='result-text'>
          {result.isSafe
            ? 'This URL appears to be legitimate and safe to visit.'
            : 'This URL exhibits suspicious patterns commonly associated with phishing attacks.'}
        </div>

        <div className="result-cards">

          <div className="result-card">
            <p className="card-title">Confidence Score</p>
            <p className="card-value">{Math.round(result.confidence)}%</p>
          </div>

          <div className="result-card">
            <p className="card-title">Analyzed URL</p>
            <p className="card-url">{result.url}</p>
          </div>

        </div>

      </div>
    </div>
  );
};

export default ResultModal;
