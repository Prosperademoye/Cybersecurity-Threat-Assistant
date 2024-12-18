AI-Driven Cybersecurity Threat Hunting Assistant
================================================

### Project Documentation

* * * * *

Overview
--------

The AI-Driven Cybersecurity Threat Hunting Assistant automates the parsing of cybersecurity threat reports and identifies critical threats. It utilizes Natural Language Processing (NLP) to extract key entities, categorize threats, and provide actionable insights through an interactive interface.

* * * * *

Features
--------

1.  Upload and process cybersecurity threat reports (PDF or text).
2.  Extract key entities like malware names, CVEs, and affected systems.
3.  Classify threats into severity levels: Critical, Medium, Low.
4.  Assign a threat score based on extracted features.
5.  Interactive interface for report parsing and threat insights.

* * * * *

Technology Stack
----------------

### Core Tools

-   Programming Language: Python
-   NLP Libraries:
    -   spaCy (for NER and preprocessing)
    -   Hugging Face Transformers (for threat classification)
-   Data Handling: pandas, PyPDF2
-   Interface: Streamlit
-   Deployment: Flask/FastAPI, Streamlit Cloud
-   Visualization: Plotly, matplotlib

### APIs and Frameworks

-   VirusTotal API
-   Shodan API (optional)
-   MITRE ATT&CK Framework

* * * * *

Project Structure
-----------------




* * * * *

Setup Instructions
------------------

### 1\. Prerequisites

-   Python 3.8+
-   Libraries: Install dependencies using:

    `pip install -r requirements.txt`

-   APIs: Obtain API keys for:
    -   [VirusTotal API](https://www.virustotal.com/).
    -   [Shodan API](https://www.shodan.io/) (if integrating).

### 2\. Data Collection

-   Download threat data from:
    -   MITRE ATT&CK Framework.
    -   [CISA Threat Reports](https://www.cisa.gov/).
-   Store PDFs or text reports in the `data/raw` folder.

### 3\. Data Preprocessing

Run `preprocess.py` to clean and tokenize data:

bash


`python scripts/preprocess.py`

### 4\. Training Models

#### Named Entity Recognition (NER)

Fine-tune an NER model using `ner_training.py`:

bash


`python scripts/ner_training.py`

#### Threat Classification

Train a threat classifier using `classification.py`:

bash

`python scripts/classification.py`

### 5\. Running the Application

Run the Streamlit app to interact with the tool:

bash

`streamlit run app/app.py`

* * * * *

Features in Detail
------------------

### 1\. Data Preprocessing

-   Input: Raw text or PDFs.
-   Process:
    -   Text cleaning: Stop word removal, punctuation stripping.
    -   Tokenization and lemmatization using `spaCy`.

### 2\. Named Entity Recognition

-   Entities:
    -   `MALWARE`: Malware names from reports.
    -   `CVE`: Vulnerability codes (e.g., CVE-2023-1234).
    -   `SYSTEM`: Affected systems (e.g., Windows, Linux).
-   Output: Extracted entities highlighted for insights.

### 3\. Threat Classification

-   Input: Extracted text from reports.
-   Process: Fine-tuned BERT model categorizes threats as:
    -   `Critical`
    -   `Medium`
    -   `Low`
-   Output: Threat level for each identified issue.

### 4\. Scoring Mechanism

-   Algorithm:
    -   Calculate scores using:
        -   Severity of CVEs.
        -   Number of affected systems.
    -   Formula Example:

        scss


        `Threat Score = (CVE Severity * 0.5) + (System Count * 0.3) + Other Factors * 0.2`

-   Visualization: Threat scores displayed in a dashboard.

### 5\. Interface

-   Features:
    -   Upload threat reports.
    -   View extracted entities and threat categories.
    -   Interactive dashboards for scores.
-   Framework: Built with Streamlit for simplicity.

* * * * *

Deployment
----------

### 1\. Local Deployment

-   Use Flask or FastAPI to serve the model as an API.
-   Command to start API server:

    bash

    `uvicorn app:app --reload`

### 2\. Cloud Deployment

-   Host on AWS or GCP using Docker for scalability.
-   Deploy the Streamlit app to Streamlit Cloud.

* * * * *

Future Enhancements
-------------------

1.  Real-Time Alerting:
    -   Integrate Slack or Telegram APIs for critical threat notifications.
2.  Multi-Language Support:
    -   Add pipelines for non-English threat reports.
3.  Adversarial Defense:
    -   Incorporate detection of adversarial examples in text.

* * * * *

Example Use Case
----------------

1.  Analyst uploads a PDF threat report.
2.  Tool extracts malware names (`MALWARE`), vulnerabilities (`CVE`), and affected systems (`SYSTEM`).
3.  Classifies threats into severity levels and assigns a threat score.
4.  Displays insights in an easy-to-read dashboard.

### Example Scenario:

An analyst in a mid-sized company receives weekly threat reports. Without the model, they spend hours reading reports, identifying key vulnerabilities, and determining what to prioritize. With the model:

1.  They upload the reports into the system.
2.  The model extracts malware names, CVEs, and affected systems.
3.  It classifies threats into Critical, Medium, and Low severity.
4.  A dashboard displays the most pressing issues and their threat scores.
5.  The analyst quickly focuses on patching high-severity vulnerabilities and communicating actionable findings to the team.

* * * * *

Acknowledgments
---------------

-   Datasets: MITRE ATT&CK, VirusTotal, CISA.
-   Libraries: spaCy, Hugging Face Transformers, Streamlit.

* * * * *

Contact
-------

For issues or enhancements, contact the developer prosperademoye@gmail.com