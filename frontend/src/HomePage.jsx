import { scanURL } from './api';
import { useState } from 'react';
import HistoricalData from './HistoricData';
import Navbar from './Navbar';
import './App.css';

// --- DUMMY DATA FOR PREVIEW ---
const DUMMY_HISTORY = [
  {
    url: 'https://example-bank-secure.com',
    timestamp: new Date(2026, 2, 1, 14, 30),
    isSafe: true,
    confidence: 95,
  },
  {
    url: 'http://paypa1-verify.tk/login',
    timestamp: new Date(2026, 2, 1, 12, 15),
    isSafe: false,
    confidence: 98,
  },
  {
    url: 'https://microsoft.com',
    timestamp: new Date(2026, 2, 1, 16, 45),
    isSafe: true,
    confidence: 99,
  },
  {
    url: 'http://amaz0n-account-verify.xyz',
    timestamp: new Date(2026, 2, 1, 10, 20),
    isSafe: false,
    confidence: 97,
  },
  {
    url: 'https://github.com',
    timestamp: new Date(2026, 1, 28, 13, 10),
    isSafe: true,
    confidence: 99,
  },
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
      <Navbar />
      <header className='header'>
        <h1>Protect Yourself from Phishing Attacks</h1>
      </header>
      <div className='description'>
        <p>
          Enter any URL below to instantly analyse and detect potential phishing
          threats <br /> using advanced Al-powered detection
        </p>
      </div>
      <form onSubmit={postURL} className='url-form'>
        <span className='search-icon'>
          <svg width='25' height='25' viewBox='0 0 24 24' fill='none'>
            <circle cx='11' cy='11' r='7' stroke='#9aa4b2' strokeWidth='1.5' />
            <line
              x1='16.5'
              y1='16.5'
              x2='21'
              y2='21'
              stroke='#9aa4b2'
              strokeWidth='1.5'
            />
          </svg>
        </span>
        
        <label>
          <input
            name='url-link'
            defaultValue=''
            placeholder='Enter URL to analsze (e.g., https://example.com)'
          />
        </label>
        <button type='submit'>Analyse URL</button>
      </form>
      <p className='privacy-text'>
        Your privacy is protected. URLs are analszed securely and not stored
        permanently.
      </p>
      <div id='result' />

      <HistoricalData history={history} />
      <p className='privacy-text'>
        Your privacy is protected. URLs are analysed securely and not stored
        permanently.
      </p>
    </div>
  );
}
