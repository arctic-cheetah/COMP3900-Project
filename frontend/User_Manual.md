# Phishy Links – Frontend User Manual

Welcome to the Phishing and Spam Detection tool! PHISHY LINKS! This application provides a simple, intuitive web interface to analyze URLs and determine if they are safe or potentially malicious (phishing).

---

## 1. Using the Dashboard (Home Page)

The Home Page is your main dashboard for performing new URL security checks.

### Scanning a URL

1. **Locate the Input Field:** Look for the main text box labeled with the placeholder **"Enter URL"**.
2. **Enter the Link:** Paste or type the complete URL of the website you want to check.
    - _Note: The "Analyse" button will remain locked (disabled) until you enter text into the field._
3. **Start the Scan:** Click the **"Analyse"** button.
4. **Processing:** A loading indicator will appear while our backend AI model analyzes the webpage's structure, URL characteristics, and contents.

### Understanding the Results

Once the scan is complete, a **Result Modal** will pop up on your screen, displaying:

- **Status Badge:** A clear **"Safe"** (Verified) or **"Danger"** (Phishing) indicator.
- **Confidence Score:** A percentage showing how confident the AI model is in its assessment.
- **Explanations:** The AI will provide a list of specific reasons for its decision (e.g., "number of special characters in URL is higher than usual" or "website found on whitelist").

---

## 2. Managing Scan History (Historical Data)

The application automatically keeps track of the URLs you have previously scanned so you can easily review, filter, and export them later. Navigate to the **Historical Data** section via the Navigation Bar to access these features.

### Viewing Past Scans

The history table displays a list of your previous scans, including:

- The **URL** that was scanned.
- The **Status** (Safe or Phishing).
- The **Confidence Score**.
- The **Timestamp** of when the scan occurred.
- The **Explanations** reasons why its Safe/Phishing.

### Filtering the History Table

You can easily narrow down your scan history to find exactly what you are looking for:

- **Filter by Safe:** Click the **"Safe"** filter button above the table. The table will instantly update to show _only_ the URLs that were flagged as secure.
- **Filter by Phishing:** Click the **"Phishing"** filter button. The table will update to show _only_ the malicious URLs.
- **Clear Filters:** Click the active filter button again or click a "Clear/All" button to reset the table and view your entire scan history.

### Exporting Data to CSV

You can download your scan history to your local computer for reporting or offline analysis using the **Export** feature.

- **Download All Records:** While viewing the full history table (no filters applied), click the **"Export CSV"** button. A file containing your entire scan history will be downloaded.
- **Download Filtered Records:** The CSV export is _context-aware_. If you apply a filter first (e.g., you click the "Phishing" button), clicking **"Export CSV"** will download _only_ the filtered links currently visible in the table. This is highly useful for creating isolated reports of just your dangerous links!

### Interacting with History Records

- **Expand Details:** Click on any individual row in the history list to expand it and view more specific details about that past scan.
- **Delete a Record:** To remove a specific URL from your history, click on the expanded record and press the **"Delete record"** button.
- **Batch Deletion:** You can also clear multiple records from your history at once using the bulk delete functionality if you need to clean up your dashboard.
