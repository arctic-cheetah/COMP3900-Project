code import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider } from '@mantine/core';
import App from "./App.jsx";
import '@mantine/core/styles.css';
import "./index.css";

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <MantineProvider defaultColorScheme="light">
      <App />
    </MantineProvider>
  </React.StrictMode>,
);
