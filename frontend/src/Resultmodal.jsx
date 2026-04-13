import './ResultModal.css';
import { useMantineTheme } from '@mantine/core';

const ResultModal = ({ result, onClose }) => {
  if (!result) return null;
  const theme = useMantineTheme();

  return (
    <div className='overlay' onClick={onClose}>
      <div className='modal' onClick={(e) => e.stopPropagation()}>
        <p className='analysis-result-text'>Analysis Results</p>

        <div className='result-icon'>
          {result.isSafe ? '✅ URL IS SAFE!' : '⚠️ URL IS PHISHING'}
        </div>

        <div className='result-text'>
          {result.isSafe
            ? 'This URL appears to be legitimate and safe to visit.'
            : 'This URL exhibits suspicious patterns commonly associated with phishing attacks.'}
        </div>

        <div className='result-cards'>
          <div className='confidence-result-card'>
            <p className='card-title'>Confidence Score</p>

            <div className='confidence-row'>
              <div className='confidence-bar'>
                <div
                  className='confidence-fill'
                  style={{
                    width: `${result.confidence}%`,
                    backgroundColor: result.isSafe
                      ? theme.colors.green[6]
                      : theme.colors.red[6],
                  }}
                />
              </div>

              <span className='confidence-value'>
                {Math.round(result.confidence)}%
              </span>
            </div>
          </div>

          <div className='result-card'>
            <p className='card-title'>Analysed URL</p>
            <p className='card-url'>{result.url}</p>
          </div>
        </div>
        <button onClick={onClose} className='close-button'>
          Close
        </button>
      </div>
    </div>
  );
};

export default ResultModal;
