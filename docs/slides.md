# Final Demo Slides (~21 slides, 15–18 min, 6 members ~2.5 min each)

> Structure: Problem/Background → Feature Summary → Frontend → Backend → ML
> Demo is live throughout — no code shown. Approach explanation woven into each section.

---

## SECTION 1 — PROBLEM & BACKGROUND (Slides 1–4)
*Suggested: 1–2 speakers, ~3.5 min*

---

### Slide 1 — Title
- Project title
- Team member names
- COMP3900 | T1 2026

---

### Slide 2 — The Problem
- Phishing is the #1 initial access vector — 36% of all breaches start with phishing (Verizon 2025)
- AI has driven a 1,265% increase in phishing emails
- Human error (a single misclick) contributes to ~60% of confirmed breaches
- Average cost of a phishing-related breach: $4.88M (IBM 2024)
- Modern phishing sites deliberately mimic legitimate ones — non-technical users cannot reliably tell the difference

---

### Slide 3 — Existing Tools & The Gap
- **VirusTotal**: scans across 70+ engines, but not phishing-specific, technically complex results, no explanation of *why* something is flagged
- **PhishTank**: phishing-focused, but no UI, requires developer API integration, registration closed since 2020
- **The gap**: no accessible, user-friendly phishing detection tool for everyday users that also *explains* its verdict
- Our project addresses this directly

---

### Slide 4 — Our Solution
- **Instant and explainable** — returns a safe/phishing verdict + confidence score + a plain-English explanation of why
- **Accessible to anyone** — no account, no technical knowledge required; works on mobile and desktop, simple one-input UI
- **Persistent and exportable** — every scan is saved anonymously, viewable in a history table, and exportable to CSV for record-keeping or analysis

*[System diagram: React frontend → Flask REST API → ML Pipeline → PostgreSQL]*

---

## SECTION 2 — FEATURE SUMMARY (Slide 5)
*Suggested: same speaker or brief handoff, ~1 min*

---

### Slide 5 — What We Built (Feature Overview)
*One slide mapping all implemented requirements — helps assessor follow along*

| Feature | Requirement |
|---|---|
| URL scan → safe/phishing verdict + confidence score | FT1 |
| Loading indicator during scan | FT7 |
| Clear input / new scan | FT3 |
| Result modal with confidence + explanation | FT5 |
| Scan history with colour indicators (green/red) | FT6 |
| Filter history: All / Safe / Phishing | FT6 |
| Delete individual or multiple scans | FT6 |
| Export scan history to CSV | BK7 |
| Anonymous DB persistence | BK6 |
| REST API (JSON, multi-client) | BK1 |
| Logs with timestamps | BK3 |
| Explainable AI (LIME) | FT5 / BK5 |
| Accessibility (WCAG, mobile-responsive) | FT2 |

---

## SECTION 3 — FRONTEND (Slides 6–9)
*Suggested: 1–2 speakers, ~4.5 min*

---

### Slide 6 — LIVE DEMO: Scanning a URL
> *Demo: paste a URL (e.g. microsoft.com), hit scan, show result. Then try a phishing URL.*

- User pastes URL into input and submits
- Loading spinner appears immediately (FT7)
- Result appears: Safe/Phishing badge (green/red), confidence score, plain-English explanation
- **Talk point**: invalid URL → helpful error message (FT1)
- **Talk point**: input is sanitised server-side — path/query encoded to prevent XSS/SQLi

---

### Slide 7 — LIVE DEMO: Result Modal
> *Demo: click into a result to open the detail modal*

- Verdict badge (green Safe / red Phishing)
- Confidence score with visual bar
- Analysed URL displayed
- Explanation text — plain English reason why the model flagged it (e.g. *"URL length is longer than usual"*, *"website found on whitelist"*)
- **Talk point**: directly addresses what VirusTotal and PhishTank lack — the *why*, not just the verdict

---

### Slide 8 — LIVE DEMO: Scan History, Filter & Delete
> *Demo: scroll history table, use filter dropdown, delete a scan*

- History table: URL, date/time, result badge, confidence bar (FT6)
- Green = safe, red = phishing
- Filter: All / Safe / Phishing with live counts (FT6)
- Delete individual scan or select multiple + bulk delete — removed from DB immediately
- **Talk point**: all data stored anonymously — no IP, session ID, or user account ever recorded (BK6)

---

### Slide 9 — LIVE DEMO: Export CSV
> *Demo: hit Export CSV*

- Downloads `scan_history.csv` — columns: id, url, is_safe, confidence, scanned_at, explanation (BK7)
- Works on both desktop and mobile
- **Talk point**: useful for small businesses or IT teams wanting to log and review results

---

## SECTION 4 — BACKEND (Slides 10–13)
*Suggested: 1–2 speakers, ~4 min*

---

### Slide 10 — API Overview
- Flask REST API — JSON responses, supports multiple frontend clients (BK1)
- Endpoints:

| Method | Route | Description |
|---|---|---|
| POST | `/scan` | Submit URL → verdict + confidence + explanation |
| GET | `/scans` | Paginated scan history (limit/offset) |
| DELETE | `/scans/<id>` | Delete scan by ID |
| GET | `/scans/export` | Download full history as CSV |
| POST | `/error` | Log errors from frontend/model |

- URL sanitisation before hitting the model (strips whitespace, encodes path/query to prevent XSS/SQLi)
- Scheme validation — only http/https accepted

---

### Slide 11 — Database & Persistence
- PostgreSQL via Docker, schema initialised at startup (BK6)
- `scans` table:

| Column | Type | Detail |
|---|---|---|
| id | SERIAL PK | Auto-incrementing |
| url | TEXT | Sanitised URL |
| is_safe | BOOLEAN | Model verdict |
| confidence | NUMERIC | 0–100, 4dp |
| scanned_at | TIMESTAMPTZ | UTC, auto-set |
| explanation | TEXT | JSON list of LIME explanation strings |

- Every scan saved automatically after model runs
- Anonymous — no user/IP/session stored

---

### Slide 12 — Logging & Error Handling
- All API errors logged with timestamp and request context (BK3)
- Critical failures (e.g. DB connection loss at startup) written to a separate log file
- Structured JSON log format
- **Talk point**: full operational visibility without storing any user-identifying information

---

### Slide 13 — Testing
- pytest integration test suite hitting a live backend + DB (not mocks)
- **Route tests**: scan, error logging, invalid inputs
- **Persistence tests**:
  - Scan saved after `/scan` and appears in `/scans`
  - All expected fields returned
  - Pagination enforced, invalid params → 400
  - Delete removes from DB, confirmed gone from list
  - Delete nonexistent scan → 404
  - Export returns `text/csv` with correct headers

---

## SECTION 5 — MACHINE LEARNING (Slides 14–21)
*Suggested: 2 speakers, ~5.5 min — most detailed section*

---

### Slide 14 — ML Pipeline Overview
*Diagram: URL → Feature Extraction (URL + HTML) → Whitelist Check → LR Model → LIME → Result*

Three-stage hybrid pipeline:
1. **Feature Extraction** — URL features + HTML page analysis
2. **Whitelist Check** — fast similarity check against top 100k legitimate domains
3. **Logistic Regression + LIME** — model inference + explanation generation

**Why hybrid?**
- Single-model URL approaches degrade with concept drift as phishing tactics evolve
- HTML analysis catches attacks that disguise themselves with clean-looking URLs
- Pipelining faster checks (whitelist) before the model reduces latency

---

### Slide 15 — Stage 1a: URL Feature Extraction
- Features extracted from the URL string alone — no page visit needed for this stage
- Includes: URL length, domain length, TLD length, digit count, special character count, obfuscated characters, subdomain count, presence of IP as domain, slash count, query parameters, HTTPS
- Root domain extracted via `tldextract`
- ~50+ URL features fed into the model

---

### Slide 16 — Stage 1b: HTML Feature Analysis
**Why URL features alone weren't enough:**
- Attackers can craft URLs that look clean — the real giveaways are in the page content
- HTML analysis catches a different class of phishing patterns

**How it works:**
- Playwright headlessly loads the page and captures the full rendered DOM
- HTML features extracted:

| Feature | Why it matters |
|---|---|
| `URLTitleMatchScore` | Phishing pages often have a title mismatched from the hostname |
| `HasCopyrightInfo` | Phishing sites rarely include copyright notices |
| `IsResponsive` | Phishing pages are often not mobile/desktop friendly |
| `HasSocialNet` | Legitimate sites link to social media; phishing sites avoid it |
| `NoOfExternalRef` | High external redirects is a common phishing pattern |
| `HasSubmitButton` | Credential-harvesting pages always have a form submit |
| `HasHiddenFields` | Hidden form fields used to pass stolen data covertly |
| `NoOfJS` | High JS count can indicate obfuscated malicious scripts |

- Combined with URL features into a single feature vector

---

### Slide 17 — Stage 2: Whitelist + Similarity Algorithms
- Domain compared against top 100,000 legitimate domains by global traffic rank
- Three similarity scores computed:

| Algorithm | What it measures | Why included |
|---|---|---|
| **Levenshtein distance** | Minimum edit distance between strings | Catches character substitution (paypa**1**.com) |
| **Jaro-Winkler** | Similarity weighted towards prefix | Catches prefix typosquatting (paypal-secure.com) |
| **LCS (Longest Common Subsequence)** | Longest shared character sequence | Catches reordering attacks |

- Exact whitelist match → immediately returns safe at 100% confidence (fast path, no model call)
- Similarity scores also passed as features into the model

---

### Slide 18 — Stage 3: Logistic Regression Model
- Trained on UCI Phishing URL Dataset
- **[INSERT: accuracy, F1, precision, recall, ROC-AUC from training notebook]**
- Why logistic regression:
  - Fast inference — keeps response time low
  - Outputs a probability score natively → used directly as the confidence score (0–100%)
  - Strong performance on tabular URL/HTML feature datasets
  - Auditable — no black-box behaviour
  - Compatible with LIME for explanation generation

---

### Slide 19 — LIME: Explainable AI
- **LIME** = Local Interpretable Model-Agnostic Explanations
- Explains *individual* predictions — why *this specific URL* was flagged, not global averages
- Model-agnostic: works with logistic regression or any future model
- How it works:
  - Perturbs input features around the specific URL
  - Fits a local linear approximation
  - Identifies which features most influenced the verdict
- Output converted to plain English:
  - e.g. *"URL length is longer than usual"*, *"does not have HTTPS"*, *"website found on whitelist"*
- Top 3 most influential features shown to the user
- **Talk point**: directly solves the gap vs VirusTotal/PhishTank — users understand *why*, not just *what*

---

### Slide 20 — Dataset & Model Performance
- Trained on UCI Phishing URL Dataset
- **[INSERT: accuracy, F1, precision, recall, ROC-AUC]**
- Whitelist: top 100k domains by global traffic rank
- Evaluation metrics: precision, recall, F1, accuracy, ROC-AUC

---

### Slide 21 — Summary
- Built an accessible, non-technical-user-first phishing detection tool
- Hybrid pipeline (URL features + HTML analysis + whitelist + LR + LIME) addresses concept drift better than single-model approaches
- Explainable AI closes the usability gap left by VirusTotal and PhishTank
- Anonymous by design — privacy without sacrificing functionality
- Thank you — happy to take questions

---

## Speaker Time Guide
| Section | Slides | Approx. Time |
|---|---|---|
| Problem & background | 1–4 | ~3 min |
| Feature summary | 5 | ~1 min |
| Frontend (demo-heavy) | 6–9 | ~4.5 min |
| Backend | 10–13 | ~3.5 min |
| ML (most detailed) | 14–21 | ~6 min |
| **Total** | | **~18 min** |

> Trim tip: Slides 20 (dataset metrics) and 13 (testing) can be cut short if running long.
