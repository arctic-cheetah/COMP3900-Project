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

        <p>Confidence: {Math.round(result.confidence)}%</p>

        <p>URL: {result.url}</p>
      </div>
    </div>
  );
};

export default ResultModal;
