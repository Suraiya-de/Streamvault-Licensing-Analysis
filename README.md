# StreamVault Licensing Analysis

## Project Overview

StreamVault Licensing Analysis is a data acquisition and analysis project designed to support a proposed **$14 million content licensing decision**.

The project uses movie metadata, financial information and credits from [The Movie Database (TMDb)](https://www.themoviedb.org/) to investigate whether franchise bundles or standalone films offer stronger historical box-office performance.

The analysis compares:
- All available release years in the acquired sample.
- Films released from 2000 onward.
- Primary franchise and standalone classifications.
- An alternative classification that treats single-film collection candidates as standalone units.
- Descriptive director and lead-actor performance.

The objective is to identify content candidates for further commercial and rights due diligence. Historical box-office performance is not treated as a direct measure of licensing value.

**Project deadline:** 18 February 2027

**Analysis status:** Completed, with documented assumptions, limitations and recommendations.

## Key Findings

The final analysis contains 112 unique successfully acquired films from the original 127 candidate rows.

Under the primary classification, franchise bundles outperform standalone films on weighted gross revenue-to-budget return and median unit return in both analysis periods.

| Period | Licensing type | Weighted gross return | Median unit return |
|---|---|---:|---:|
| All years | Franchise bundles | 452.16% | 455.11% |
| All years | Standalone films | 384.95% | 284.48% |
| 2000 onward | Franchise bundles | 415.11% | 361.15% |
| 2000 onward | Standalone films | 324.04% | 284.48% |

The primary franchise screening shortlist is:

1. The Lord of the Rings
2. Ice Age
3. The Avengers

The all-years sensitivity analysis changes the weighted comparison slightly in favour of standalone units when single-film collection candidates are reclassified. Franchise bundles retain the higher median unit return, and the post-2000 comparison continues to favour franchises on both measures.

The results support prioritising franchise candidates for further investigation, not approving a licensing purchase or price.

See `reports/client_memo.md` for the client-facing recommendation and `reports/decision_notes.md` for the methodology and sensitivity analysis.

## Repository Structure

```text
StreamVault_Licensing_Analysis/
|
|-- data/
|   |-- raw/
|   |   |-- id_list.csv
|   |   |-- _fetch_log.csv
|   |   `-- movie/                 # Local API cache; excluded from Git
|   `-- processed/
|       |-- id_reconciliation.csv
|       |-- movies.csv
|       |-- movie_financial_metrics.csv
|       |-- licensing_comparison.csv
|       |-- licensing_units_all_years.csv
|       |-- licensing_units_2000_onward.csv
|       |-- director_performance.csv
|       `-- lead_actor_performance.csv
|
|-- docs/
|   |-- adr/
|   |-- data_contract.md
|   |-- findings.md
|   `-- questions.md
|
|-- notebooks/
|   |-- 01_data_investigation.ipynb
|   |-- 02_data_acquisition.ipynb
|   `-- 03_streamvault_analysis.ipynb
|
|-- reports/
|   |-- client_memo.md
|   `-- decision_notes.md
|
|-- src/
|   |-- __init__.py
|   |-- analysis.py
|   |-- config.py
|   |-- tmdb_client.py
|   `-- validation.py
|
|-- tests/
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md