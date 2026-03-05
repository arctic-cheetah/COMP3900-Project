import { scanURL } from "./api";
import "./App.css";

export default function HomePage() {
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
    <div className="homepage">
      <header className="header">
        <h1>Protect Yourself from Phishing Attacks</h1>
      </header>
      <p>Enter any URL below to instantly analyze and detect potential phishing threats using advanced Al-powered detection</p>
      <form onSubmit={postURL}>
        <label>
          <input name="url-link" defaultValue="Enter URL to analyze (e.g., https://example.com)" />
        </label>
        <button type="submit">Analyse URL</button>
      </form>
      <p>Your privacy is protected. URLs are analyzed securely and not stored permanently.</p>
      <div id="result" />
    </div>
  );
}
