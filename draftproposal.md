nalysis 
The current landscape for existing systems reveals a major gap: there are no accessible, user-friendly phishing detection systems that exist for non-technical users. While powerful tools such as VirusTotal and PhishTank serve security professionals, they fail to address the needs of:
General users who need simple and instant verification of suspicious links
Small businesses without dedicated IT security teams 
Mobile users who require instant verification via a dedicated mobile interface, which is largely absent in existing tools that mostly only provide a web interface

Furthermore, as highlighted in the project specification, existing ML approaches often suffer from concept drift, where models lose effectiveness as phishing tactics evolve. Many systems rely on static features, such as specific URL structures that attackers can quickly change.

As such, our project addresses this gap by developing an intuitive web and mobile application that combines machine learning algorithms for accurate phishing detection, a user-friendly interface designed for nontechnical users, real-time verification with clear and actionable results, as well as educational components to improve user phishing awareness.

2.0 User Stories and Sprint:
2.1 Scope Statement
The project will deliver a functional and mobile-friendly website where ordinary users can submit a URL to a search box to determine whether a particular webpage is considered phishing or not with high accuracy and speed. It is required that users can log in and access their own history of checking for phishing websites. The client will also need an API available in addition to the interactivity on the front end, as well as documentation of the architecture and usage of the product.

2.1.1 Jira Sprint 1 Kanban Board:

Figure 1. 
2.2 Sprint 1 User StoriesTable 1. 

Jira issue code
User
Acceptance criteria
FT1
As a user, I want to be able to input a URL/link so that I can check if it's phishing or not.
When a user inputs a URL and presses the check button, the system should return either
Phishing, Legit or Unsure
The result should appear within 8 seconds
Invalid URLS should return a helpful error message such as “Please enter a valid URL”
The UI displays a confidence score or some helpful snippet
e.g. “Detected suspicious domain by model”
FT2
As a user, I want high accessibility through buttons and clear indicators so that I can easily access core features.
Core buttons like scan, etc are accessible according to the WCAG guidelines
Buttons are large enough for mobile devices
The UI supports touch scroll 
The contrast of the UI is suitable for phones
It works on Chrome, Safari, and other major browsers
FT3
As a user, I want to clear my input so that I can quickly check multiple links.
A user can manually clear the input
After a successful scan, the user can reset the result display
A “Clear” or “New Scan” button resets input and results
Resetting does not delete scan history



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
How to deploy the app locally
BK3
As an app owner, I want logs from the system so that I can monitor errors and usage health.
All API errors are logged with timestamps 
Critical failures inside logs.

Table 2. 
2.3 Product Backlog

Figure 2. 


Frontend:
Jira issue code
User
Acceptance criteria
FT4
As a user, I want to create an account and log in so that my scan history is saved securely.
The user can register using an email and a password
Invalid credentials return a clear error message
The password field is masked
Successful login redirects to the main dashboard
A user can log out and end the session 
FT5
As a user, I want to view more details about a scan result so that I can understand why a link was flagged.
Clicking a result expands or opens a detail view
The detail view displays:
Outcome
Confidence score
Timestamp
The modal can be closed easily
FT8
Add Modal / Drop down / For information


FT6
As a user, I want a list-based display of scanned URLS with strong visual indicators like red/green so that I can quickly see outcomes.
Each item shows: URL + outcome + indicator+ confidence score
Outcomes are:
Phishing
Legit
Unsure
The list supports filtering or sorting by outcome
FT7
As a user, I want visual feedback while the system is checking a URL so that I know it is processing.
When the check button is pressed, a loading indicator appears immediately
Indicator percentage (NO NEED TIME RN)
If the request fails (network error or timeout), a helpful error message is displayed
The loading indicator disappears once a result or error is returned

Table 3. 

Backend:


Application Owner
Acceptance Criteria
BK4
As an app owner, I want the AI model to continually improve so that it can detect new and emerging techniques.
Create the tests instead
Update the model when the admin clicks train
The admin can select to update the entire model or a single one in the pipeline




BK5
As an app owner, I want to see the output of each model in the pipeline so that I can assess the AI's effectiveness.
Admins can see the models used in the scan
The confidence score and other statistics associated with each model outcome are displayed
BK7
Add API endpoints  to fetch and store data
Export csv 
Be copiable
BK9
Improve model accuracy and try different models => Similarity models

How to test the threshold such that it detects safe 
Jaccard index
USI
What is the threshold??
BK6
As an app owner, I want to retain scan data so that I can analyse the results in the future.
Every user scan is saved to the database (URL, Outcome, Confidence, Timestamp)
Data is stored anonymously 
Database schema documented

Table 4. 
WE COULD GIVE OPTIONS TO USER TO SELECT MODELS 
Scrum 3:
