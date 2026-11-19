# StreamVault Licensing Analysis

## Project Overview

StreamVault Licensing Analysis is a data acquisition and analysis project designed to support a **$14 million content licensing decision**.

The project uses movie metadata and credits from [The Movie Database (TMDb)](https://www.themoviedb.org/) to investigate whether franchise bundles or standalone films offer stronger historical performance. It compares results across all release years and films released from 2000 onward, while documenting data-quality issues, assumptions and limitations.

**Project deadline:** 18 February 2027

**Analysis status:** In progress. No final licensing recommendation has been made yet.

## Repository Structure

```text
StreamVault_Licensing_Analysis/
├── data/
│   ├── raw/
│   │   └── id_list.csv
│   └── processed/
├── docs/
│   ├── adr/
│   ├── data_contract.md
│   ├── findings.md
│   └── questions.md
├── notebooks/
│   ├── 01_data_investigation.ipynb
│   ├── 02_data_acquisition.ipynb
│   └── 03_streamvault_analysis.ipynb
├── reports/
│   ├── client_memo.md
│   └── decision_notes.md
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── config.py
│   ├── tmdb_client.py
│   └── validation.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Requirements

- Python 3
- Git
- A TMDb API Read Access Token

### Setup

Clone the repository:

```powershell
git clone <your-github-repository-url>
cd StreamVault_Licensing_Analysis
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder with your TMDb Read Access Token:

```text
TMDB_API_TOKEN=your_tmdb_read_access_token_here
```

**Security:** Never commit `.env` or expose your API token. The `.env.example` file contains only a placeholder.

## Data Sources

- **Candidate movie list:** `data/raw/id_list.csv`, supplied for the licensing analysis.
- **Movie metadata and credits:** TMDb API.
- **Inflation reference data:** To be documented when the reference dataset is selected and incorporated.

The original candidate list is preserved. API responses and derived datasets will be handled separately so that the source data is not manually altered.

## Project Workflow

The planned workflow is:

1. Investigate and profile the supplied candidate IDs.
2. Retrieve movie metadata and credits from TMDb.
3. Maintain an ID ledger to account for every input row.
4. Transform API responses into analysis-ready tables.
5. Identify and document data-quality issues.
6. Calculate financial and performance metrics.
7. Compare franchise bundles with standalone films across the two release-year windows.
8. Develop shortlists, talent analysis and a licensing recommendation.
9. Prepare the client memo and supporting documentation.

## Documentation and Deliverables

Project documentation is maintained in the following locations:

- `docs/data_contract.md` — data expectations and rules.
- `docs/findings.md` — investigation findings.
- `docs/questions.md` — outstanding questions and assumptions.
- `reports/decision_notes.md` — analytical decisions and trade-offs.
- `reports/client_memo.md` — final business recommendation for the client.

Further documentation and outputs will be added as the analysis develops.

## Reproducing the Analysis

The project is being developed to support repeatable analysis and future updates to the candidate list.

Execution instructions, configuration settings, test commands and performance measurements will be added as the acquisition and analysis pipeline are implemented and tested.

## Known Limitations

Historical box-office revenue is only a proxy for audience demand. It does not directly measure streaming subscriptions, retention or licensing value.

Data availability, missing financial information, historical reporting differences and the completeness of franchise collections may affect the analysis. These limitations will be assessed and documented before a final recommendation is made.

## Project Status

This repository is under active development. The data investigation, acquisition pipeline, validation, analysis and final client documentation are being built incrementally.

The final recommendation will be supported by documented evidence, reproducible calculations and clearly stated limitations.