# AI-Driven Cybersecurity Threat Hunting Assistant

## Overview
The **AI-Driven Cybersecurity Threat Hunting Assistant** automates the parsing of cybersecurity threat reports and identifies critical threats. It uses **Natural Language Processing (NLP)** to extract key entities, categorize threats, and provide actionable insights through an interactive interface.

---

## Features
- **Upload and process cybersecurity threat reports** (PDF or text).
- **Extract key entities** such as:
  - Malware names
  - CVEs (Common Vulnerabilities and Exposures)
  - Affected systems
- **Classify threats** into severity levels: Critical, Medium, Low.
- **Assign a threat score** based on extracted features.
- **Interactive interface** for report parsing and threat insights.

---

## Technology Stack

### Core Tools
- **Programming Language**: Python
- **NLP Libraries**:
  - `spaCy` (for NER and preprocessing)
  - Hugging Face Transformers (for threat classification)
- **Data Handling**: `pandas`, `PyPDF2`
- **Interface**: Streamlit
- **Deployment**: Flask/FastAPI, Streamlit Cloud
- **Visualization**: Plotly, matplotlib

### APIs and Frameworks
- **VirusTotal API**
- **Shodan API** (optional)
- **MITRE ATT&CK Framework**

---

## Project Structure
```plaintext
project-directory/
│
├── data/                   # Data folder for raw and processed datasets
│   ├── raw/                # Raw PDFs and text reports
│   ├── processed/          # Preprocessed data for NLP models
│
├── models/                 # Trained models (NER, classifiers)
│
├── app/                    # Streamlit app files
│   ├── app.py              # Main app script
│
├── scripts/                # Scripts for preprocessing and training
│   ├── preprocess.py       # Text preprocessing
│   ├── ner_training.py     # Named Entity Recognition training
│   ├── classification.py   # Threat classification model training
│
├── docs/                   # Documentation files
├── requirements.txt        # Python dependencies
├── README.md               # Overview of the project
