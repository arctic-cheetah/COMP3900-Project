import { useState, useEffect } from "react";
import { scanURL } from "./api";
import "./App.css";

export default function App() {
  const postURL = async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    if (formData == null) {
      return;
    }

    const url = formData.get("url-link");
    if (url == null || url == "") {
      console.log("invalid URL");
      return;
    }
    try {
      const scanResult = await scanURL(url);
      const resultElem = document.getElementById("result");

      if (scanResult) {
        resultElem.textContent = "passed";
      } else {
        resultElem.textContent = "failed";
      }
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Phishing Checker</h1>
      </header>
      <form onSubmit={postURL}>
        <label>
          URL: <input name="url-link" defaultValue="" />
        </label>
        <button type="submit">Submit form</button>
      </form>
      <div id="result" />
    </div>
  );
}
