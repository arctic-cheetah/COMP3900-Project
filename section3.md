3.0 Design Justifications
TODO: Intro about how our overarching design has evolved from the proposal

DO THE FOLLOWING FOR EVERY CHANGE
Introduce aspect from initial design
State how it has been changed since then → relate to client reqs, realistic scope of task etc
Outline what’s been added and reason for adding
Justify how its more effective
3.1 Frontend
The frontend design has evolved from a simple prototype that was heavily result-focused, into a more user-friendly system. These changes were driven by client requirements and usability considerations, ultimately leading to an improvement in responsiveness, data presentation and explainability. 
3.1.1 Mobile Responsive Analysis Modal
In our initial design, once the user submitted a URL into the input box, an inline section on the page would appear with the results. However, this did not account for mobile screens and led to a heavily cluttered and messy interface.

As required by the client, we implemented a pop-up modal for smaller screen sizes which will ensure the user’s attention is focused on a single modal. This new design adapts appropriately to limited screen space whilst also maintaining usability. This choice was ultimately more effective in improving user readability and directs their attention to the most crucial information.

Figure 8. 
3.1.2 List View and State Expansion 
As the requirement to keep track of all websites in the UI was required we had to implement a table which shows the list of all the past scanned URLs. We added the outcome timestamp and confidence score for each scanned URLs in rows. We added clear user-friendly buttons to filter phishing and safe URLs then also added a drop-down menu to do the same. 

3.1.3 Delete functionality & Accordion
Next we added delete functionality to the history table to be able to delete scans and added a checkbox to make sure we can select multiple to remove old scans from the history. To make the rows not feel cluttered we added an accordion view and also according to the client's requirement we implemented this to make the rows look cleaner. 

3.1.4 History Table Mobile View
This was also implemented in the mobile view which made it modal and user-friendly for mobile users which was a client requirement, so everyday users can check URLs. All the same functionality and designs were ported to the mobile view to be user-friendly and responsive.
3.1.5 Explainable AI Badges
In our initial design, our product was mainly focused on providing a simple result indicating whether a URL was safe or phishing which was displayed using a coloured badge saying “Safe” or “Phishing” along with a confidence score bar which allowed users to quickly understand the outcome of the scan. However, this offered limited insight into how the system reached its decision which limited transparency for users.

Based on our client’s feedback, the design was updated to improve clarity on our classification without overcomplicating the user interface. To improve clarity and user trust, explainable AI badges were added directly beneath the scan result which provided easy to read explanations for the classifications such as “Domain length is shorter/longer than usual”. Thus, these badges allowed non-technical users to understand the reasoning behind each scan result. This approach was most effective since it maintained the same clean user experience whilst improving transparency, helping users interpret results more confidently.

Figure 9. 
3.1.6 Explainable AI in the History Table
Originally, the design only showed the explainable AI badges within the result modal shown immediately after the URL scan. This meant that users could view the reasoning behind the result at the time of analysis, but once the popup closed, they couldn’t access the information again. As the project developed, this was improved so that the explanations were also shown in the history section, based on client and team feedback.

To fix this, the explanation badges were added to the expandable rows in the desktop history table. This meant that users could now click on any past scan and see the same reasons that were shown in the popup, making it more useful because users could review past results and understand them without having to run the scan again.

Figure 10. 
3.1.7 Export CSV button
The CSV button was implemented upon the request of the client as it would make it easier for them to do more research on the scanned links. Which is why we added the button and it downloads the links present in the history table for the user to evaluate further in csv format. We then also made sure it follows the same design and mobile responsiveness as the rest of the frontend.
3.2 Machine Learning Model and Backend
How project requirements for the AI have changed over the sprints
→ demo how constantly developed design
Scrum 1 User stories Backend Feature Evolution:

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
BK2:
Some of these project requirements that were accepted in scrum 1 by the client have changed particularly with user story BK2. The current model now includes two AI models in the pipeline, as seen in figure ___. due to the implementation of the Explainable AI and ML Model.

The acceptance criteria of BK2 in Scrum 1 initially only used URL features in the ML model to test if a URL was safe or phishing. 
Later, the AI model was discovered as inaccurate, and the HTML features and USI index was added into scrum 2 to potentially increase accuracy and more HTML features added by scrum 3. Since the addition of more feature variables to the AI model did not necessarily increase model accuracy, dataset cleaning and making it larger were performed in attempts to increase model accuracy as seen in user story BK9 (figure 7) below. 

Additionally, additional things to improve the AI model such as deploying a HTML fetch engine to ensure dynamically loaded websites are accessible were implemented to improve model accuracy.

Solutions and discussions for model accuracy are discussed in the Appendix.

BK1 and BK3:
Aside from this BK1 and BK3 have remained relatively constant due to their necessity in maintaining the essential data flow between the backend and frontend. For example, the communication between the backend and frontend still utilises API responses in JSON for clarity and extensibility when new features are being added, such as adding the explainable AI in the JSON. 

Additionally, the acceptance criteria of BK3 logging error routes have been effective and useful for both the development team and administrator to understand where the model or system has crashed or why it outputted the result

Product Backlog/ Scrum 2 Backend Feature Evolution:
However, user acceptance and stories have changed from product backlog and Scrum 2. In particular, the following image of the user has been changed

Figure 11. 
Observe that BK4 had been removed because the client does not require the model to be updated when the URL is tested. This also adds unnecessary technical sophistication as the typical ML model is trained prior to deployment. It conventionally does not make sense to continuously train the model while it is running because how would the model be dynamically updated or replaced. By doing so, it reduces unnecessary technical debt associated with implementing a feature to allow team effort to be directed towards features most focal towards the client.

BK7 and BK6:
Are user stories that were proposed by the client and agreed by the team to work because the benefits to the client include:
Ability to analyse the AI model of why it determined the URL to be phishing or safe
Thereby allowing the AI model to be fine tuned and improved due to observing it’s output
Exporting the scanned URLs as a CSV dataset allows for researchers and the client to perform analysis on the AI model 
Thereby allowing further research and improvements from the model.
BK5 was reintroduced back into Scrum 3 due to the client requirement of having an explainable AI model. The benefits confer:
Ability to understand why the AI model outputted the URL to be safe or phishing
Being able to understand the most important feature variables in determining phishing or safe URLS
Future feature engineering of the most important feature variables to determine safe URLs
Doing so allowed us to measure why the accuracy was the reason from the AI model, allowing the team to debug and improve the model

BK9 of improving model accuracy along with trying different models or threshold was simply eventually refined to 
Figure 12. 
model accuracy by the client as the client had observed that the model accuracy was poor, so they desired for the team to increase the accuracy of the AI model by using other datasets. Doing so reduces the incidence of false positives and false negatives. Such as the StealthPhishing dataset or the Kaggle Dataset. The addition of the whitelist/USI scores also falls under BK9. It reduces the number of false positives by the model, which increases accuracy.  

3.2.1 API Layer

The initial design proposed a single `/scan` endpoint that would return a phishing or safe result. The earliest implementation was purely a stub — it returned `True` only if the URL matched the hard-coded string `"realwebsite.com"` and `False` otherwise, with no real model connected. 

During Sprint 1 the API was hardened to satisfy BK1 and BK3. URL validation using `tldextract` and sanitisation (path and query encoding to prevent XSS and SQL injection) were added to the `/scan` route. A CORS whitelist was introduced to restrict which origins could call the API, fulfilling the requirement for an encapsulated backend that supports multiple frontend clients. The `/error` logging route was also introduced in Sprint 1, allowing the ML pipeline to forward structured error entries with timestamps to log files on disk, satisfying the monitoring requirements of BK3.

As the project progressed into Sprints 2 and 3 the API grew substantially to match the expanding frontend feature set:

| Method | Route | Sprint Added | Purpose |
|--------|-------|--------------|---------|
| POST | `/scan` | Sprint 1 | Submit URL to ML pipeline, save and return result |
| POST | `/error` | Sprint 1 | Accept and persist error logs from the ML model |
| POST | `/list_scans` | Sprint 2 | Return scan history (initial implementation) |
| GET | `/scans` | Sprint 3 | Paginated scan history replacing the legacy route |
| DELETE | `/scans/<id>` | Sprint 3 | Delete a single scan by ID |
| GET | `/scans/export` | Sprint 3 | Download full scan history as a CSV file |

The response payload of `/scan` also evolved across sprints. In Sprint 1 it returned only `{ is_safe, confidence }`. When LIME-based explainable AI was integrated in Sprint 3, the payload was extended to include an `explanation` field containing the list of human-readable reason strings. This kept the API extensible — the frontend could immediately begin rendering XAI badges without any other structural changes to the communication layer. The `/scans/export` endpoint was added to satisfy BK7’s requirement for CSV export, allowing researchers and the client to download the full scan dataset for offline analysis.

3.2.2 Persistence and Database

In the initial Sprint 1 proposal, BK6 called for retaining scan data so that the client could analyse results in the future. However, no database was connected during Sprint 1 — each scan result was computed and returned without being saved, meaning all history was lost between requests.

A PostgreSQL database was introduced mid-Sprint 2. PostgreSQL was chosen for its robustness, support for structured queries with typed constraints, and straightforward Docker integration. The initial schema created on 30 March captured the minimal set of scan attributes:

```sqla
CREATE TABLE IF NOT EXISTS scans (
    id          SERIAL          PRIMARY KEY,
    url         TEXT            NOT NULL,
    is_safe     BOOLEAN         NOT NULL,
    confidence  NUMERIC(5, 4)   NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    scanned_at  TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);
```

A dedicated `database.py` module was introduced at the same time, encapsulating all persistence logic behind three functions: `init_db()`, `save_scan()`, and `get_all_scans()`. All storage is anonymous by design — no user-identifying information such as IP addresses or session tokens is recorded, in line with BK6’s data anonymity requirement.

The schema was extended twice as the project evolved. First, the `confidence` column type was changed from `NUMERIC(5,4)` (range 0–1) to `NUMERIC` with a `CHECK (confidence >= 0 AND confidence <= 100)` constraint, after the model’s confidence output was rescaled to a 0–100 percentage for frontend display. Second, an `explanation` column (`TEXT`, nullable) was added in Sprint 3 when XAI was integrated:

```sql
ALTER TABLE scans ADD COLUMN explanation TEXT;
```

This column stores the JSON-serialised LIME explanations alongside each scan. By persisting explanations at the time of scanning rather than recomputing them on demand, the history table could surface the same XAI badges for past scans as are shown in the live result modal, satisfying the client requirement to retain explanation data.

Further refinements to the persistence layer included:

- A `delete_scan()` function added to support the frontend’s delete functionality (Sprint 3), returning `True` on success and `False` if the scan ID does not exist.
- A server-side cap inside `get_all_scans()` that enforces a maximum of 500 rows per request regardless of the `limit` parameter supplied by the frontend, preventing potential abuse from large unbounded queries.
- A context-manager wrapper (`get_cursor()`) around all database access to ensure automatic rollback on failure and guaranteed connection cleanup, improving reliability under concurrent requests.

Together, these incremental changes transformed the persistence layer from a missing piece in Sprint 1 into a fully functional, anonymised scan history that supports querying, deletion, CSV export, and XAI explanation retrieval.

3.3 Algorithms and Tools
Technical complexity of fetching dynamically loading pages 

Figure 13. 
Prior to implementing the PlayWrgiht headless chrome browser, the AI model previously utilised simple GET requests to load HTML pages.This logic was flawed and reduced accuracy because dynamic webpages such as google.com were unable to load

For this reason as seen in the figure below.

Figure 14. 

The scrum master fixed this model inaccuracy by replacing simple GET requests with the python library PlayWright that uses a headless (No GUI) chromium browser to mimic loading a webpage on the browser. Heuristics deployed to observe page completion include
Waiting for the load state to transition to finish on the HTML page
Waiting for the javascript variable document.readyState to enter complete
Waiting for the input tag for some dynamically loading website with input to finish loading
Or when the network is idle.
Doing so allowed us to properly fetch data and in turn increase accuracy. Not only so, it allowed for the team to begin cleaning URLS which are non-reachable because phishing URLS have a short lifespan meaning it is possible to clean the dataset and increase accuracy by using reachable only urls
3.3.1 Heuristic Analysis and Reverse Engineering of UCI HTML Features:
According to the UCI research paper, some of the HTML feature variables as seen in appendix…
Have not been clearly documented on how the NoOFJS  or MaxLineLength had been calculated for example. For this reason, reasonable assumptions have been made such as the fact that NoOfJS really represents the number of script tags, onError, onLoad, etc and javascript URI code that are present in the HTML page or site. Or the MaxLineLength according to the UCI research paper does not specify if HTML page which can be minified should be unminified to provide unbiased MaxLineLength. 

As such, reverse engineering and heuristics were utilised on the implemented feature variables from the UCI dataset to ensure a relatively high accuracy was achieved as seen in appendix.

3.3.2 String Analysis for URL to measure URL Similarity Indexes:
The UCI research paper (include reference) uses a custom algorithm to calculate how similar 2 strings are to each other. The idea is that if a new URL is not identical but very similar to a legitimate URL, it likely means that it is trying to impersonate the legitimate URL. Using this idea as a basis and looking at other papers such as (https://link.springer.com/article/10.1186/s13673-017-0098-1), and (https://www.mdpi.com/1424-8220/26/3/1041), we decided to use Levenshtein distance, Jaro-Winkler distance, and longest common subsequence (LCS) as these were used quite often. These scores can produce values with different ranges, so we normalised them into the range of [0, 1]. This happens before we input the scores as features into the model, so no single metric disproportionately affects the model’s predictions.

Levenshtein distance:
Levenshtein distance measures the number of edits required to change one string into another. The operations used are insertions, deletions, and substitutions of characters. A smaller distance means 2 strings are more similar. (example)


Jaro-Winkler distance:
Jaro-Winkler distance measures similarity between strings by looking at the number of matching characters and the number of transpositions. A transposition is a swap between 2 characters. It also weights prefix matchings heavily, so strings that have the same starting characters are considered more similar. ( example)


Longest Common Subsequence (LCS):
LCS measures the longest sequence of characters that appear in the same order in both strings/ This does not need to be consecutive. ( example)



3.3.3 Explainability using Local Interpretable Model-agnostic Explanations

Machine learning models often act as “black boxes” where inputs are given, and outputs come out, but what happens in the middle is not clear. This makes it difficult for users to understand how and why a particular outcome was reached. In the context of our project, we should provide a reason/explanation for how our prediction of legit/phishing was reached, as it lets users understand what aspects of the URL contributed to the decision. 

To address this issue, our system uses Local Interpretable Model-agnostic Explanations (LIME). LIME is a technique that provides explanations for individual predictions without needing to know the internal structure of the model. It instead approximates the behaviour of a more complex model around a specific prediction (local) by making many new data points that vary slightly, using the features of a specific input (perturbed version). Then, by observing how the model prediction changes, it is able to map which features had the biggest impact on the result.

When a URL is inputted, the logistic regression model first generates a prediction indicating whether or not the URL is phishing. LIME is then used to identify the most influential features that contributed to that prediction. For example, features such as URL length and URL similarity scores may have positive or negative weights indicating their significance.

The use of LIME improves interpretability and transparency by allowing users to see which features contributed the most to the prediction. This improves trust in the system for users and allows developers to validate and debug the results by checking that the model is making decisions based on meaningful features rather than unintended correlations.

LIME is also model-agnostic, which makes the system more flexible. The machine learning model can be changed or updated without needing to change the explanation framework. This improves the maintainability and extensibility of the system design.

Provide explanations and implementation details of complex algorithms and tools we have used.
Showcase research, planning and implementation of difficult problems we had to solve
Demonstrate end-to-end how the system operates 
Support with diagrams, flowchats, pseudocode
