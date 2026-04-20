import './ResultAnalysis.css';
import { useMantineTheme, Badge } from '@mantine/core';
import { IconCheck, IconAlertTriangle } from '@tabler/icons-react';

type Result = {
  isSafe: boolean;
  confidence: number;
  url: string;
  explanation: string[];
};

type ResultModalVars = {
  result: Result | null;
  onClose: () => void;
};

const ResultAnalysis: React.FC<ResultModalVars> = ({ result, onClose }) => {
  if (!result) return null;
  const theme = useMantineTheme();

  return (
    <div className='overlay' onClick={onClose}>
      <div className='modal' onClick={(e) => e.stopPropagation()}>
        <p className='analysis-result-text'>Analysis Results</p>

        <div className='result-icon'>
          <Badge
            color={result.isSafe ? 'green' : 'red'}
            variant='light'
            size='lg'
            leftSection={
              result.isSafe ? (
                <IconCheck size={22} />
              ) : (
                <IconAlertTriangle size={22} />
              )
            }
          >
            {result.isSafe ? 'Safe' : 'Phishing'}
          </Badge>
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

          <div className='result-text'>
            {result.isSafe
              ? 'This URL appears to be legitimate and safe to visit.'
              : 'This URL exhibits suspicious patterns commonly associated with phishing attacks.'}
          </div>

          <div className='result-card'>
            <p className='card-title'>Analysed URL</p>
            <p className='card-url'>{result.url}</p>
          </div>
            {result.explanation && result.explanation.length > 0 && (
                <div className='result-card'>
                    <p className='card-title'>Why this result</p>
                    <div className='explanation-badges'>
                        {result.explanation.map((point, i) => (
                            <Badge
                                key={i}
                                color={result.isSafe ? 'green' : 'red'}
                                variant='light'
                                size='sm'
                            >
                                {point}
                            </Badge>
                        ))}
                    </div>
                </div>
            )}
        </div>
        <button
          onClick={onClose}
          className='close-button'
          style={{ backgroundColor: theme.colors.blue[6] }}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default ResultAnalysis;
