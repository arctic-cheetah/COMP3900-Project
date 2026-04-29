3.0 Design Justifications
TODO: Intro about how our overarching design has evolved from proposal

DO THE FOLLOWING FOR EVERY CHANGE
Introduce aspect from initial design
State how it has been changed since then → relate to client reqs, realistic scope of task etc
Outline what’s been added and reason for adding
Justify how its more effective
3.1 Frontend
The frontend design has evolved from a simple prototype that was heavily result-focused, into a more user friendly system. These changes were driven by client requirements and usability considerations ultimately leading to an improvement in responsiveness, data presentation and explainability. 
3.1.1 Mobile Responsive Analysis Modal
In our initial design, once the user submitted a URL into the input box, an inline section on the page would appear with the results. However, this did not account for mobile screens and led to a heavily cluttered and messy interface.

As required by the client, we implemented a pop-up modal for smaller screen sizes which will ensure the user’s attention is focused on a single modal. This new design adapts appropriately to limited screen space whilst also maintaining usability. This choice was ultimately more effective in improving user readability and directs their attention to the most crucial information.

3.1.2 List View and State Expansion 
As the requirement to keep track of all websites in the UI was required we had to implement a table which shows the list of all the past scanned URLs. We added the outcome timestamp and confidence score for each scanned URLs in rows. We added clear user-friendly buttons to filter phishing and safe URLs then also added a drop-down menu to do the same. 

3.1.3 Delete functionality & Accordion
Next we added delete functionality to the history table to be able to delete scans and added a checkbox to make sure we can select multiple to remove old scans from the history. To make the rows not feel cluttered we added an accordion view and also according to the client's requirement we implemented this to make the rows look cleaner. 

3.1.4 History Table Mobile View
This was also implemented in the mobile view which made it modal and user-friendly for mobile users which was a client requirement, so everyday users can check URLs. All the same functionality and designs were ported to the mobile view to be user-friendly and responsive.
3.1.5 Explainable AI Badges
In our initial design, our product was mainly focused on providing a simple result indicating whether a URL was safe or phishing which was displayed using a coloured badge saying “Safe” or “Phishing” along with a confidence score bar which allowed users to quickly understand the outcome of the scan. However, this offered limited insight into how the system reached its decision which limited transparency for users.

Based on our client’s feedback, the design was updated to improve clarity on our classification without overcomplicating the user interface. To improve clarity and user trust, explainable AI badges were added directly beneath the scan result which provided easy to read explanations for the classifications such as “Domain length is shorter/longer than usual”. Thus, these badges allowed non-technical users to understand the reasoning behind each scan result. This approach was most effective since it maintained the same clean user experience whilst improving transparency, helping users interpret results more confidently.

3.1.6 Explainable AI in the History Table
Originally, the design only showed the explainable AI badges within the result modal shown immediately after the URL scan. This meant that users could view the reasoning behind the result at the time of analysis, but once the popup closed, they couldn’t access the information again. As the project developed, this was improved so that the explanations were also shown in the history section, based on client and team feedback.

To fix this, the explanation badges were added to the expandable rows in the desktop history table. This meant that users could now click on any past scan and see the same reasons that were shown in the popup, making it more useful because users could review past results and understand them without having to run the scan again.

3.2 Machine Learning Model and Backend
How project requirements for the AI have changed over the sprints
→ demo how constantly developed design

Previously in Scrum 1 User stories were:

Jira Issue code
Application Owner
Acceptance Criteria
BK1
As an app owner, I want an encapsulated backend so that it supports multiple frontend clients.
API responses are in JSON
API is documented with clear params and returns


BK2
As an app owner, I want the core logic to be clearly documented so that I can understand how the backend and the one AI model in the pipeline work.
README includes setup flow or architecture diagrams
Documents explain:
API routes
Dataflow and typing
Explain how to run tests for URL validation and model inference
BK3
As an app owner, I want logs from the system so that I can monitor errors and usage health.
All API errors are logged with timestamps 
Critical failures inside logs.

Table 2. 

Some of these project requirements that were accepted in scrum 1 by the client have changed particularly with user story BK2. The current model now includes two AI models in the pipeline, as seen in figure ___. due to the implementation of the Explainable AI and ML Model.

Aside from this BK1 and BK3 have remained relatively constant due to their necessity in maintaining the essential data flow between the backend and frontend.

However user acceptance and stories have changed from product backlog and scrum 2. In particular the following image of the user has been changed

Figure 6. 
Observe that BK4 had been removed because the client does not require the model to be updated when the URL is tested. This also adds unnecessary technical sophistication as the typical ML model is trained prior to deployment. It conventionally does not make sense to continuously train the model while it is running because how would the model be dynamically updated or replaced. By doing so, it reduces unnecessary technical debt associated with implementing a feature to allow team effort to be directed towards features most focal towards the client.

BK7 and BK6 are user stories that were proposed by the client and agreed by the team to work because the benefits to the client include:
Ability to analyse the AI model of why it determined the URL to be phishing or safe
Thereby allowing the AI model to be fine tuned and improved due to observing it’s output
Exporting the scanned URL’s as a CSV dataset allows for researchers and the client to perform analysis on the AI model 
Thereby allowing further research and improvements from the model.
BK5 was reintroduced back into Scrum 3 due to the client requirement of having an explainable AI model. The benefits confer:
Ability to understand why the AI model outputted the URL to be safe or phishing
Being able to understand the most important feature variables in determining phishing or safe URLS
Future feature engineering of the most important feature variables to determine safe URLs
Doing so allowed us to measure why the accuracy was the reason from the AI model, allowing the team to debug and improve the model

BK9 of improving model accuracy along with trying different models or threshold was simply eventually refined to 
Figure 7. 
model accuracy by the client as the client had observed that the model accuracy was poor, so they desired for the team to increase the accuracy of the AI model by using other datasets. Doing so reduces the incidence of false positive and false negatives. Such as the StealthPhishing dataset or the Kaggle Dataset.



DO THE FOLLOWING FOR EVERY CHANGE
Introduce aspect from initial design
State how it has been changed since then → relate to client reqs, realistic scope of task etc
Outline what’s been added and reason for adding
Justify how its more effective
3.4 Algorithms and Tools
Technical complexity of fetching dynamically loading pages 

Figure 8. 
Prior to implementing the PlayWrgiht headless chrome browser, the AI model previously utilised simple GET requests to load HTML pages.This logic was flawed and reduced accuracy because dynamic webpages such as google.com were unable to load

For this reason as seen in the figure below.

Figure 9. 

The scrum master fixed this model inaccuracy by replacing simple GET requests with the python library PlayWright that uses a headless (No GUI) chromium browser to mimic a loading a webpage on the browser. Heuristics deployed to observe page completion include
Waiting for the load state to transition to finish on the HTML page
Waiting for the javascript variable document.readyState to enter complete
Waiting for the input tag for some dynamically loading website with input to finish loading
Or when the network is idle.
Doing so allowed us to properly fetch data and in turn increase accuracy. Not only so, it allowed for the team to begin cleaning URLS which are non-reachable because phishing URLS have a short lifespan meaning it is possible to clean the dataset and increase accuracy by using reachable only urls
Heuristic Analysis and Reverse Engineering of UCI HTML Features:
According to the UCI research paper, some of the HTML feature variables as seen in appendix…
Have not been clearly documented on how the NoOFJS  or MaxLineLength had been calculated for example. For this reason, reasonable assumptions have been made such as the fact that NoOfJS really represents the number of script tags, onError, onLoad, etc and javascript URI code that are present in the HTML page or site. Or the MaxLineLength according to the UCI research paper does not specify if HTML page which can be minified should be unminified to provide unbiased MaxLineLength. 

As such, reverse engineering and heuristics were utilised on the implemented feature variables from the UCI dataset to ensure a relatively high accuracy was achieved as seen in appendix.

String Analysis for URL to measure URL Similarity Indexes:
The UCI research paper (include reference) uses a custom algorithm to calculate how similar 2 strings are to each other. The idea is that if a new URL is not identical but very similar to a legitimate URL, it likely means that it is trying to impersonate the legitimate URL. Using this idea as a basis and looking at other papers such as (https://link.springer.com/article/10.1186/s13673-017-0098-1), and (https://www.mdpi.com/1424-8220/26/3/1041), we decided to use Levenshtein distance, Jaro-Winkler distance, and longest common subsequence (LCS) as these were used quite often. These were also normalised to improve its compatibility with machine learning models.

Levenshtein distance:
Levenshtein distance measure the number of edits required to change one string into another. The operations used are insertions, deletionsm, and substitutions of characters. A smaller distance means 2 strings are more similar. (maybe example)


Jaro-Winkler distance:
Jaro-Winkler distance measures similarity betweens strings by looking at the number of matching characters and the number of transpostions. Transpostions. (maybe example)


Levenshtein distance:
Levenshtein distance measure the number of edits required to change one string into another. The operations used are insertions, deletionsm, and substitutions of characters. A smaller distance means 2 strings are more similar. (maybe example)



Provide explanations and implementation details of complex algorithms and tools we have used.
Showcase research, planning and implementation of difficult problems we had to solve
Demonstrate end-to-end how the system operates 
Support with diagrams, flowchats, pseudocode


## 4.0 User-Driven Evaluation of Solution

The primary purpose of Phishy Links is to provide everyday users with a fast, accessible, and transparent tool for identifying potentially malicious URLs. Our main features of the design include the following:

- **URL Phishing Detection** — Users submit a URL and receive an immediate binary classification (Safe or Phishing) accompanied by a confidence score.
- **Explainable AI Predictions** — Each classification is supported by three human-readable reasons generated by the LIME (Local Interpretable Model-agnostic Explanations) framework, allowing users to understand why a URL was flagged.
- **Domain Whitelist Fast-Path** — Well-known trusted domains are identified via string similarity against a curated list of the top 100,000 legitimate domains, using Levenshtein distance, Jaro-Winkler similarity, and Longest Common Subsequence (LCS) metrics, bypassing the ML model entirely for a near-instantaneous result.
- **Dynamic Webpage Handling** — The system uses Playwright with a headless Chromium browser to render JavaScript-heavy pages before feature extraction, improving coverage of modern websites.
- **Persistent Scan History** — All scan results are stored anonymously in a PostgreSQL database and surfaced in a browsable history view with summary statistics.
- **Scan Management** — Users can filter history by safety status and date range, delete individual or multiple records, and export their full history as a CSV file.

These features are evaluated below across a defined set of effectiveness criteria, system objectives, and functional requirements.

---

## 4.1 Effectiveness Criteria

The following criteria are used to evaluate the effectiveness of the solution from the perspective of both the client and the target user — a non-technical individual seeking to verify URLs before engaging with them.

| ID | Criterion | Description | Measurement |
|----|-----------|-------------|-------------|
| EC-1 | **Classification Accuracy** | The model correctly classifies URLs as safe or phishing at a high rate | Accuracy, precision, recall, and F1 score on an 80/20 held-out test split and external validation datasets (see Appendix) |
| EC-2 | **Prediction Explainability** | Every classification is accompanied by meaningful, human-readable reasons | Presence of three LIME-generated feature explanations per result; assessed for relevance and interpretability |
| EC-3 | **User Comprehensibility** | Results are presented in plain language understandable without technical knowledge | Verdict label (Safe/Phishing), confidence percentage, and plain-text explanations are surfaced clearly in the UI |
| EC-4 | **Dynamic Content Coverage** | The system correctly handles modern websites that render content via JavaScript | Ability to extract HTML features from JS-rendered pages, assessed qualitatively across a range of target URLs |
| EC-5 | **History Accessibility** | Users can retrieve, filter, and export their full scan history reliably | History persists across sessions, supports filtering and bulk deletion, and is exportable as CSV |
| EC-6 | **System Reliability** | The system handles edge cases (invalid URLs, unreachable pages, slow-loading pages) gracefully without crashing | Error handling and fallback behaviour under failure conditions |

---

## 4.2 System Objectives

The following objectives describe the core goals of the AI and ML pipeline. Each is evaluated against the effectiveness criteria defined above.

### 4.2.1 Providing Clear Safe/Phishing URL Output

The primary AI objective is to allow a user to submit a URL and receive a clear classification indicating whether the URL is likely safe or phishing. This is achieved through the `/scan` endpoint, where the backend passes the submitted URL through the AI pipeline and returns a JSON response containing:

- `is_safe` — a boolean indicating safe (`true`) or phishing (`false`)
- `confidence` — a float representing model certainty (0–100%)
- `explanation` — an array of three human-readable strings describing the top features driving the prediction

The frontend surfaces these in the Result Analysis modal as a colour-coded verdict badge (green for Safe, red for Phishing), a confidence progress bar, and three explanation tags.

**Evaluation against EC-1, EC-3:** This objective is substantially met. The output is presented clearly and accessibly, satisfying EC-3. EC-1 is partially met — while the model achieves strong accuracy on test data (see Appendix), it may still misclassify edge cases. False positive and false negative rates are non-zero, meaning the system can occasionally flag a legitimate site as phishing or fail to detect a malicious one. This limitation is discussed further in §5.1.

### 4.2.2 Providing Accurate URL Classification

The model is required to achieve high accuracy across both the training validation split and external datasets. This is achieved by:

- Training on a combination of the UCI Phishing URL Dataset and the StealthPhisher2025 dataset
- Evaluating with an 80/20 train/test split, measuring accuracy, precision, recall, and F1 score
- Running the trained model against additional compatible external datasets to assess generalisation beyond the training distribution

**Evaluation against EC-1:** This objective is partially met. The model achieves satisfactory performance on held-out test data as reported in the Appendix. However, real-world performance may differ due to distribution shift between academic datasets and live URLs encountered in practice. The model may be less reliable on novel phishing techniques not well-represented in the training data. This is discussed further in §5.1.

### 4.2.3 Handling of Dynamic Webpages

The AI model originally relied on simple HTTP GET requests to fetch webpage content. This was insufficient for modern websites that dynamically render HTML via JavaScript — static requests return only the initial HTML shell, missing much of the content that the model relies on for feature extraction.

To address this, the system introduced Playwright with a headless Chromium browser to render pages realistically before extracting features. The system waits for one or more of the following conditions before beginning extraction:

- Page load state transitions to `domcontentloaded`
- `document.readyState` equals `"complete"`
- Input elements are present in the DOM (for form-heavy sites)
- Network activity becomes idle

**Evaluation against EC-4:** This objective is substantially met. The introduction of Playwright significantly improves feature coverage for JS-rendered pages compared to static HTTP requests. However, the system enforces an 8-second timeout, meaning pages that are very slow to load or that rely on complex asynchronous rendering may time out before content is fully captured, resulting in degraded feature extraction. This limitation is discussed in §5.2.

### 4.2.4 Explainability of Predictions via LIME

A key objective is to ensure that the system's predictions are not black-box outputs but are accompanied by interpretable reasons that help users understand why a URL was classified as safe or phishing. This is achieved using LIME (Local Interpretable Model-agnostic Explanations), which approximates the model's local decision boundary for each individual prediction and identifies the top contributing features.

For each scan, the system:

1. Passes the extracted 35-feature vector to the LIME `LimeTabularExplainer`
2. Generates a local explanation using 50 perturbed samples around the input
3. Selects the top 3 features by absolute contribution weight
4. Converts the feature names and their directional influence into plain-text sentences surfaced in the UI

**Evaluation against EC-2, EC-3:** This objective is largely met. Every prediction is accompanied by three LIME-generated explanations, satisfying EC-2. The frontend renders these as readable explanation tags (e.g., "URL contains a high proportion of special characters"), satisfying EC-3 for most users. However, some features and thresholds (e.g., Levenshtein distance values, character continuation rates) may not be immediately intuitive to non-technical users, representing a partial gap discussed in §5.3.

### 4.2.5 Domain Whitelist Fast-Path for Trusted URLs

A separate objective is to provide high-confidence, near-instantaneous results for well-known legitimate domains, reducing unnecessary ML computation and increasing user trust for commonly visited sites. This is achieved through a whitelist pipeline that runs before the logistic regression model:

1. The root domain is extracted from the submitted URL using `tldextract`
2. The domain is compared against the top 100,000 most-visited legitimate domains
3. If an exact or subdomain match is found (e.g., `mail.google.com` → `google.com`), the system returns `is_safe=true`, `confidence=100`, and the explanation `"Website found on whitelist"` — bypassing the ML model entirely
4. If no exact match is found, Levenshtein distance, Jaro-Winkler similarity, and LCS scores to the closest matching trusted domain are computed and passed as features to the ML model

**Evaluation against EC-1, EC-6:** This objective is fully met for domains present on the whitelist, delivering deterministic, high-confidence results and contributing to system reliability (EC-6). The primary limitation is that the whitelist is a static snapshot and may not reflect newly registered legitimate domains or sites that have fallen out of the top 100,000. This is discussed in §5.4.

---

## 4.3 Functional Requirement 1 — URL Submission and Scanning

**Overview:** The core user-facing feature of the system is the ability to submit a URL and receive a phishing/safe classification with an associated confidence score.

**System Operation:** On the homepage, the user enters a URL into the input field and clicks the Scan button (disabled until input is non-empty). The frontend sends a `POST /scan` request to the backend with the body `{"url": "<submitted_url>"}`. The backend validates the input, passes the URL through the AI pipeline — whitelist check, then feature extraction via Playwright and BeautifulSoup, then Logistic Regression prediction and LIME explanation — and returns a JSON response. The frontend renders a loading spinner during processing and then presents the result in the Result Analysis modal. On desktop, the new result also appears at the top of the history panel.

[Figure 4.3.1: Homepage with URL input field and Scan button]

[Figure 4.3.2: Loading state displayed during scan processing]

**Evaluation against EC-1, EC-3, EC-4, EC-6:** This requirement is substantially met. The end-to-end scan flow is functional across the majority of URLs tested, and dynamic content is handled via Playwright (EC-4). Results are clearly presented in accessible language (EC-3). Two partial gaps exist: the system may time out on very slow-loading URLs (EC-6 — see §5.2), and classification accuracy is not guaranteed for all URL types (EC-1 — see §5.1).

---

## 4.4 Functional Requirement 2 — Classification Result Display

**Overview:** Once a scan completes, the system must present the result in a format immediately understandable to a non-technical user.

**System Operation:** The Result Analysis modal is rendered after a successful scan response. It displays:

- A colour-coded verdict badge: green **Safe** or red **Phishing**
- A horizontal confidence progress bar showing the model's certainty as a percentage (e.g., 94.71%), colour-coded to match the verdict
- Three plain-text explanation badges generated by LIME describing the primary features that drove the classification (e.g., "Domain found on trusted whitelist", "URL contains no obfuscated characters", "Page title closely matches domain name")
- The submitted URL displayed at the bottom of the modal for reference

The modal is dismissible via a close button or by clicking the overlay, and on mobile it occupies a full-screen overlay for readability.

[Figure 4.4.1: Result Analysis modal — Safe classification with confidence bar and explanation badges]

[Figure 4.4.2: Result Analysis modal — Phishing classification]

**Evaluation against EC-2, EC-3:** This requirement is fully met. The verdict, confidence, and explanations are surfaced clearly in plain language (EC-3), and every result is accompanied by three LIME-generated explanations (EC-2). A minor gap is that some explanation text may use terminology unfamiliar to non-expert users. This is discussed in §5.3.

---

## 4.5 Functional Requirement 3 — Persistent Scan History and Statistics

**Overview:** The system stores all scan results persistently and surfaces them in a browsable history view with aggregate statistics, enabling users to review past scans across sessions.

**System Operation:** Scan results are written to a PostgreSQL database on each `/scan` call and retrieved via `GET /scans` (paginated, up to 500 results per request, ordered most-recent-first). The History page displays:

- **Statistics cards** — Total scans performed, total Safe results, and total Phishing results
- **Desktop table view** — Each scan shown as a row with columns for URL, status badge, confidence percentage, timestamp, and action buttons (view detail, delete)
- **Mobile card view** — The same data presented in a stacked card layout optimised for smaller screens

Scan records persist across browser sessions using a combination of the PostgreSQL database and a localStorage cache on the client, ensuring history is available even on page refresh.

[Figure 4.5.1: History page — desktop view with statistics cards and scan table]

[Figure 4.5.2: History page — mobile card layout]

**Evaluation against EC-5:** This requirement is fully met. History is persistent across sessions, viewable on both desktop and mobile, and includes meaningful aggregate statistics. The identified limitation is that history is anonymous and not user-scoped — all scans from any user are stored in the same table without authentication, meaning users share a single history view. This is discussed in §5.5.

---

## 4.6 Functional Requirement 4 — Filtering and Scan Management

**Overview:** Users can filter their scan history by safety status and date range, and manage records through individual or bulk deletion.

**System Operation:**

- **Filtering:** A dropdown allows users to filter history by "All", "Safe", or "Phishing". A date range picker further narrows results by scan date. Filters are applied client-side to the currently loaded result set.
- **Individual deletion:** Each table row and mobile card has a delete button that triggers a `DELETE /scans/<id>` request, removing the record from both the database and the local UI state immediately.
- **Bulk deletion:** Users can select multiple scans via per-row checkboxes, using a select-all toggle to mark the entire loaded page. A bulk delete button removes all selected records in a single action.

[Figure 4.6.1: Filter controls — safety dropdown and date range picker in use]

[Figure 4.6.2: Bulk selection with checkboxes and bulk delete button]

**Evaluation against EC-5, EC-6:** This requirement is substantially met. Filtering and individual/bulk deletion function correctly (EC-5, EC-6). A partial gap exists in that filtering is performed client-side against the currently loaded page of results (up to 500 scans), rather than as a server-side database query. For users with very large scan histories exceeding the page limit, filters will not apply to records beyond the loaded window. This is discussed in §5.5.

---

## 4.7 Functional Requirement 5 — CSV Export

**Overview:** Users can export their complete scan history as a CSV file for offline analysis or record-keeping purposes.

**System Operation:** An export button on the History page triggers a `GET /scans/export` request to the backend. The backend queries the full `scans` table and streams the results as a CSV file download with the following columns: `id`, `url`, `is_safe`, `confidence`, `scanned_at`, `explanation`. The browser initiates a file download automatically upon receiving the response, requiring no additional steps from the user.

[Figure 4.7.1: Export button on the history page]

[Figure 4.7.2: Sample of a downloaded CSV file showing exported scan records]

**Evaluation against EC-5:** This requirement is fully met. The export covers all records stored in the database (not limited to the currently loaded page), is delivered in a universally readable CSV format, and requires a single click to initiate. No significant limitations were identified for this feature.
