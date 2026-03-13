import { scanURL } from './api';
import { useState } from 'react';
import HistoricalData from './HistoricData';
import './App.css';

// --- DUMMY DATA FOR PREVIEW ---
const DUMMY_HISTORY = [
  { url: 'https://example-bank-secure.com', timestamp: new Date(2026, 2, 1, 14, 30), isSafe: true, confidence: 95 },
  { url: 'http://paypa1-verify.tk/login', timestamp: new Date(2026, 2, 1, 12, 15), isSafe: false, confidence: 98 },
  { url: 'https://microsoft.com', timestamp: new Date(2026, 2, 1, 16, 45), isSafe: true, confidence: 99 },
  { url: 'http://amaz0n-account-verify.xyz', timestamp: new Date(2026, 2, 1, 10, 20), isSafe: false, confidence: 97 },
  { url: 'https://github.com', timestamp: new Date(2026, 1, 28, 13, 10), isSafe: true, confidence: 99 },
];

export default function HomePage() {
  const [history, setHistory] = useState(DUMMY_HISTORY);
  const postURL = async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    if (formData == null) {
      return;
    }

    const url = formData.get('url-link');
    if (url == null || url == '') {
      console.log('invalid URL');
      return;
    }
    try {
      const scanResult = await scanURL(url);
      const resultElem = document.getElementById('result');

      if (scanResult) {
        resultElem.textContent = 'passed';
      } else {
        resultElem.textContent = 'failed';
      }
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className='homepage'>
      <header className='header'>
        <h1> Yourself from Phishing Attacks</h1>
      </header>
      <div className='description'>
        <p>
          Enter any URL below to instantly analyze and detect potential phishing
          threats <br /> using advanced Al-powered detection
        </p>
      </div>
      <form onSubmit={postURL} className='url-form'>
        <label>
          <input
            name='url-link'
            defaultValue=''
            placeholder='Enter URL to analyze (e.g., https://example.com)'
          />
        </label>
        <button type='submit'>Analyse URL</button>
      </form>
      <p className='privacy-text'>
        Your privacy is protected. URLs are analyzed securely and not stored
        permanently.
      </p>
      <div id='result' />
      
      <HistoricalData history={history} />
      <p className='privacy-text'>
        Your privacy is protected. URLs are analyzed securely and not stored permanently.
      </p>
    </div>
  );
}
