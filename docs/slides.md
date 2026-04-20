# Final Demo Slides (~20 slides, 15–18 min, 6 members ~2.5 min each)

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
- **Instant and explainable** — returns a safe/phishing verdict + confidence score + a plain-English explanation of why, within 8 seconds
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
| Copy history to clipboard | BK7 |
| Anonymous DB persistence | BK6 |
| REST API (JSON, multi-client) | BK1 |
| Logs with timestamps | BK3 |
| Explainable AI (LIME) | FT5 / BK5 |
| Accessibility (WCAG, mobile-responsive) | FT2 |

---

## SECTION 3 — FRONTEND (Slides 6–10)
*Suggested: 1–2 speakers, ~5 min*

---

### Slide 6 — LIVE DEMO: Scanning a URL
> *Demo: paste a URL (e.g. microsoft.com), hit scan, show result. Then try a phishing URL.*

- User pastes URL into input and submits
- Loading spinner appears immediately (FT7)
- Result appears: Safe/Phishing badge (green/red), confidence score, plain-English explanation
- **Talk point**: results returned within 8 seconds (FT1 requirement) — fast because whitelist check is the first stage and returns immediately for known-safe domains
- **Talk point**: if invalid URL is entered → helpful error message shown (FT1)

---

### Slide 7 — LIVE DEMO: Result Modal
> *Demo: click into a result to open the detail modal*

- Verdict badge (green Safe / red Phishing)
- Confidence score with visual bar
- Analysed URL displayed
- Explanation text — plain English reason why the model flagged it (e.g. *"URL length is longer than usual"*, *"website found on whitelist"*)
- **Talk point**: this directly addresses what VirusTotal and PhishTank lack — the *why*, not just the verdict
- **Talk point**: explanation comes from LIME (covered in ML section)

---

### Slide 8 — LIVE DEMO: Scan History, Filter & Delete
> *Demo: scroll history table, use filter dropdown, delete a scan*

- History table shows all past scans: URL, date/time, result badge, confidence bar (FT6)
- Green = safe, red = phishing — strong at-a-glance indicators
- Filter dropdown: All / Safe / Phishing with live counts (FT6)
- Click any row → opens result modal with full details
- Delete individual scan — disappears from list immediately
- Select multiple + bulk delete
- **Talk point**: all data stored anonymously — no IP, session ID, or user account ever recorded (BK6)

---

### Slide 9 — LIVE DEMO: Export & Copy
> *Demo: hit Export CSV, then Copy*

- **Export CSV**: downloads `scan_history.csv` — columns: id, url, is_safe, confidence, scanned_at, explanation (BK7)
- **Copy**: copies the currently filtered results to clipboard, tab-separated — paste directly into Excel or Sheets (BK7)
- Filter affects what gets copied (e.g. copy only phishing results)
- **Talk point**: useful for small businesses or IT teams wanting to log and share results

---

### Slide 10 — Accessibility & Non-Functional Requirements
- **Mobile-responsive**: layout adapts for phone screens, supports touch scroll (FT2)
- **WCAG-compliant**: button sizing, colour contrast ratios, keyboard navigable (FT2)
- **Browser support**: Chrome, Safari, and major browsers (FT2)
- **Response time**: results within 8 seconds (FT1) — whitelist fast path + lightweight model inference
- **Input sanitisation**: XSS/SQLi prevention, valid scheme enforcement (http/https only)
- **Privacy**: no identifying information stored — anonymous scans only (BK6)

---

## SECTION 4 — BACKEND (Slides 11–14)
*Suggested: 1–2 speakers, ~4 min*

---

### Slide 11 — API Overview
- Flask REST API — JSON responses, supports multiple frontend clients (BK1)
- Endpoints:

| Method | Route | Description |
|---|---|---|
| POST | `/scan` | Submit URL → verdict + confidence + explanation |
| GET | `/scans` | Paginated scan history (limit/offset) |
| POST | `/list_scans` | Legacy alias for `/scans` |
| DELETE | `/scans/<id>` | Delete scan by ID |
| GET | `/scans/export` | Download full history as CSV |
| POST | `/error` | Log errors from frontend/model |

- URL sanitisation before hitting the model (strips whitespace, encodes path/query)
- Scheme validation — only http/https accepted

---

### Slide 12 — Database & Persistence
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

### Slide 13 — Logging & Error Handling
- All API errors logged with timestamp and request context (BK3)
- Critical failures (e.g. DB connection loss at startup) written to a separate log file and cause a clean exit
- Structured JSON log format — easy to grep and parse
- Frontend errors can be forwarded to `/error` endpoint for centralised logging
- **Talk point**: operational visibility without storing any user-identifying information

---

### Slide 14 — Testing
- pytest test suite hitting a live backend + DB (integration tests, not mocks)
- **Route tests**: scan accepts POST, rejects invalid body/URL, error endpoint exists and rejects malformed input
- **Persistence tests**:
  - Scan is saved after `/scan` and appears in `/scans`
  - All expected fields returned (id, url, is_safe, confidence, scanned_at)
  - Pagination enforced (limit/offset)
  - Invalid params (non-integer limit) → 400
  - Delete removes scan, confirmed gone from subsequent list
  - Delete nonexistent scan → 404
  - Export returns `text/csv` with correct header row

---

## SECTION 5 — MACHINE LEARNING (Slides 15–20)
*Suggested: 2 speakers, ~5 min — this section should be the most detailed*

---

### Slide 15 — ML Pipeline Overview
*Diagram recommended: URL → Feature Extraction → Whitelist Check → LR Model → LIME → Result*

Three-stage hybrid pipeline:
1. **URL Feature Extraction** — extract ~50+ features from the URL string alone
2. **Whitelist Check** — fast similarity check against top 100k legitimate domains
3. **Logistic Regression + LIME** — model inference + explanation generation

**Why hybrid?**
- Single-model approaches degrade with concept drift as phishing tactics evolve
- Pipelining faster checks (whitelist) before the model reduces latency and handles known-safe domains instantly
- Matches the approach validated in literature (Sahingoz et al. 2019)

---

### Slide 16 — Stage 1: URL Feature Extraction
- No page content needed — URL string only (fast, private)
- Features extracted by the preprocessor include:
  - URL length, domain length, TLD length
  - Number of digits, special characters, obfuscated characters
  - Presence of IP address as domain
  - Subdomain count
  - Number of slashes, query parameters
  - Has HTTPS
  - Root domain extracted via `tldextract`
- ~50+ features fed as a structured DataFrame into the pipeline

---

### Slide 17 — Stage 2: Whitelist + Similarity Algorithms
- Domain compared against top 100,000 legitimate domains by global traffic rank
- Three similarity scores computed:

| Algorithm | What it measures | Why included |
|---|---|---|
| **Levenshtein distance** | Minimum edit distance between strings | Catches character substitution (paypa**1**.com) |
| **Jaro-Winkler** | String similarity, weighted towards prefix | Catches prefix typosquatting (paypal-secure.com) |
| **LCS (Longest Common Subsequence)** | Longest shared character sequence | Catches reordering attacks |

- Exact whitelist match → immediately returns safe at 100% confidence (fast path, no model call)
- Similarity scores also passed as features into the logistic regression model

---

### Slide 18 — Stage 3: Logistic Regression Model
- Trained on UCI Phishing URL Dataset
- **[INSERT: accuracy, F1, precision, recall, ROC-AUC from training notebook]**
- Why logistic regression:
  - Fast inference — critical for <8s response time requirement
  - Outputs a probability score natively → used directly as the confidence score (0–100%)
  - Strong performance on tabular URL feature datasets
  - Auditable and extensible — no black-box behaviour
  - Works naturally with LIME for explanation generation

---

### Slide 19 — LIME: Explainable AI
- **LIME** = Local Interpretable Model-Agnostic Explanations
- Explains *individual* predictions — not global averages, but *why this specific URL* was flagged
- Model-agnostic: works with logistic regression, or any future model added to the pipeline
- How it works:
  - Perturbs the input features around the specific URL
  - Fits a local linear approximation
  - Identifies which features most influenced the verdict for that URL
- Output converted to plain English:
  - e.g. *"URL length is longer than usual"*, *"does not have HTTPS"*, *"website found on whitelist"*
- Top 3 most influential features shown to the user
- **Talk point**: directly solves the core gap vs VirusTotal/PhishTank — users now understand *why*, not just *what*

---

### Slide 20 — Summary
- Built an accessible, non-technical-user-first phishing detection tool
- Hybrid pipeline addresses concept drift and zero-day phishing better than single-model approaches
- Explainable AI closes the usability gap left by existing tools
- Anonymous by design — privacy without sacrificing functionality
- Fully documented API, DB schema, and test suite
- Thank you — happy to take questions

---

## Speaker Time Guide
| Section | Slides | Approx. Time |
|---|---|---|
| Problem & background | 1–4 | ~3.5 min |
| Feature summary | 5 | ~1 min |
| Frontend (demo-heavy) | 6–10 | ~5 min |
| Backend | 11–14 | ~4 min |
| ML (most detailed) | 15–20 | ~5 min |
| **Total** | | **~18.5 min** → trim as needed |

> Trim tip: Slide 10 (non-functional) can be cut to 30 sec or merged into Slide 6 if running long.
