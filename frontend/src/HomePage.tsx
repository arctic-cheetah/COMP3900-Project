import { useState, useEffect } from "react";
import { Loader } from '@mantine/core';
import { useMediaQuery } from '@mantine/hooks';

import { scanURL, getStoredData } from "./api.js";
import HistoricalData, { type Scan } from "./HistoricData.js";
import Navbar from "./Navbar.js";
import ResultAnalysis from './ResultAnalysis.js';
import "./App.css";
import logoIcon from "../assets/logo.png";

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

interface CurrentResult {
  url: string;
  isSafe: boolean;
  confidence: number;
}

export default function HomePage() {
  const [history, setHistory] = useState(() => {
    // Load from localStorage on initial mount
    const stored = localStorage.getItem('scanHistory');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        // Convert timestamps back to Date objects
        return parsed.map((item: any) => ({
          ...item,
          timestamp: new Date(item.timestamp)
        }));
      } catch (e) {
        console.error('Failed to parse stored history:', e);
        return DUMMY_HISTORY;
      }
    }
    return DUMMY_HISTORY;
  });
  const [url, setUrl] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [currentResult, setCurrentResult] = useState<CurrentResult | null>(null);
  const [isLoading, setLoading] = useState<boolean>(false);

  // Save history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('scanHistory', JSON.stringify(history));
  }, [history]);

  const handleDeleteScans = (scansToDelete: Scan | Scan []) => {
      const itemsToRemove = Array.isArray(scansToDelete) ? scansToDelete : [scansToDelete];
      setHistory((current: Scan[]) => current.filter((scan) => !itemsToRemove.includes(scan)));
  };

  const isMobile = useMediaQuery('(max-width: 768px)');
  const moveButton = useMediaQuery('(max-width: 1173px)');
  const urlFullText = useMediaQuery('(max-width: 930px)');

  const openHistoryResult = (item: Scan) => {
    setCurrentResult({
      url: item.url,
      isSafe: item.isSafe,
      confidence: item.confidence,
    });

    setIsModalOpen(true);
  };

  // Fetch from backend only if localStorage is empty
  useEffect(() => {
    const stored = localStorage.getItem('scanHistory');
    if (stored) return; // Skip if we have local data

    (async () => {
      try {
        let data = await getStoredData();
        console.log(data)
        let scans = Array.isArray(data["scans"]) ? data["scans"] : []
        let mapped: Scan[] = scans.map((s: any) => ({
          url: s.url,
          timestamp: s.scanned_at,
          isSafe: s.is_safe,
          confidence: s.confidence
        }))
        setHistory(mapped)
      }
      catch (e: any) {
        const resultElem = document.getElementById('result');
        if (resultElem) resultElem.textContent = e.message;
        console.log(e);
      }
    })();
  }, []);


  const postURL = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const form = e.currentTarget;
    const formData = new FormData(form);
    if (formData == null) {
      return;
    }
    const urlValue = formData.get('url-link') as string;
    if (urlValue == null || urlValue == '') {
      console.log('invalid URL');
      setLoading(false);
      return;
    }
    try {
      const scanResult = await scanURL(urlValue);
      console.log(scanResult);
      let { is_safe: isSafe, confidence } = scanResult;

      setTimeout(() => {
        setCurrentResult({ url: urlValue, isSafe, confidence });
        setIsModalOpen(true);

        setHistory((current: Scan[]) => [
          {
            url: urlValue,
            timestamp: new Date(Date.now()),
            isSafe,
            confidence: Math.round(confidence * 100) / 100,
          },
          ...current,
        ]);

        setLoading(false);
      }, 500);
    } catch (e: any) {
      const resultElem = document.getElementById('result');
      if (resultElem) resultElem.textContent = e.message;
      console.log(e);
      setLoading(false);
    }
  };

  return (
    <div className='homepage'>
      <Navbar />
      <img className="logo-homepage" src={logoIcon} />
      <header className="header">
        <h1>Protect Yourself from Phishing Attacks</h1>
      </header>
      <p className='description'>
        Enter any URL below to instantly analyse and detect potential phishing
        threats <br /> using advanced AI-powered detection
      </p>

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
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder={
              urlFullText
                ? 'Enter URL to analyse'
                : 'Enter URL to analyse (e.g, https://example.com)'
            }
          />
        </label>

        {!moveButton && (
          <button
            type='submit'
            className={`inline-btn ${url.trim() ? 'active-btn' : 'inactive-btn'}`}
            disabled={!url.trim()}
          >
            {isLoading ? (
              <span className='loader'>
                <Loader color='white' size='sm' />
                Analysing...
              </span>
            ) : (
              'Analyse URL'
            )}
          </button>
        )}

        {moveButton && (
          <button
            type='submit'
            className={`full-btn ${url.trim() ? 'active-btn' : 'inactive-btn'}`}
            disabled={!url.trim()}
          >
            {isLoading ? (
              <span className='loader'>
                <Loader color='white' size='sm' />
                Analysing...
              </span>
            ) : (
              'Analyse URL'
            )}
          </button>
        )}
      </form>

      {!moveButton && (
        <p className='privacy-text'>
          Your privacy is protected. URLs are analysed securely and not stored
          permanently.
        </p>
      )}

      {moveButton && (
        <div className='space' />
      )}

      {isModalOpen && isMobile && (
        <ResultAnalysis
          result={currentResult}
          onClose={() => setIsModalOpen(false)}
        />
      )}

      <HistoricalData
        history={history}
        onDelete={handleDeleteScans}
        onDeleteMultiple={handleDeleteScans}
        onHistoryClick={openHistoryResult}
      />

      <p className='privacy-text'>
        Your privacy is protected. URLs are analysed securely and not stored
        permanently.
      </p>
    </div>
  );
}
