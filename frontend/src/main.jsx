import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider } from '@mantine/core'; //
import App from "./App.jsx";
import '@mantine/core/styles.css'; // Essential for styling
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <MantineProvider defaultColorScheme="light">
      <App />
    </MantineProvider>
  </React.StrictMode>,
);