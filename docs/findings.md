# StreamVault Data Quality Findings and Risk Assessment

## 1. Executive Summary

The supplied candidate file contains 127 source rows. The investigation preserved the original values, validated identifier formats, resolved the IMDb-style identifier through TMDb, and reconciled every source row against the acquisition outcome.

The acquisition ledger records 119 acquired source rows, including duplicate entries. These represent 112 unique successfully acquired films. Five distinct TMDb identifiers returned HTTP 404 responses, two entries were invalid, and one entry was blank.

The resulting analysis uses 112 unique films. This is a useful screening sample, but it is not a complete or independently verified catalogue of licensable content. The most important limitations are the five unavailable records, potential selection bias, historical financial comparability, and the difference between theatrical box-office performance and actual licensing value.

## 2. Source Dataset Profile

The original file is `data/raw/id_list.csv`. It contains 127 data rows and one column, `tmdb_id`.

The file was read with identifier values preserved as strings so that blank values, duplicate identifiers and non-numeric entries could be investigated without silently changing the source data.

| Initial finding | Count |
|---|---:|
| Original data rows | 127 |
| Blank entries | 1 |
| Repeated numeric identifier occurrences | 6 |
| Distinct nonblank raw values | 120 |
| Negative identifier | 1 |
| IMDb-style identifier | 1 |
| Unexpected text value (`N/A`) | 1 |

The six repeated numeric identifiers are 155, 680, 278, 603, 1891 and 550. Each appears twice.

The IMDb-style identifier `tt0468569` was resolved through TMDb. It resolved to TMDb ID `155`, which was already present in the source list. This creates an additional duplicate after identifier resolution.

## 3. Detection Methods and Reconciliation

The investigation used the following checks:

1. Loaded the original candidate file without overwriting its supplied values.
2. Checked for blank entries, repeated values, negative numbers and malformed identifiers.
3. Classified numeric TMDb identifiers separately from IMDb-style identifiers.
4. Resolved the IMDb-style identifier through TMDb.
5. Checked whether resolved identifiers had already appeared in the acquisition ledger.
6. Retrieved movie details and credits from TMDb.
7. Recorded successful acquisitions, HTTP 404 responses and invalid or blank entries in `id_reconciliation.csv`.

### Final source-row reconciliation

| Acquisition outcome | Source rows |
|---|---:|
| Acquired, including duplicate rows | 119 |
| TMDb HTTP 404 responses | 5 |
| Invalid identifiers | 2 |
| Blank identifiers | 1 |
| **Total** | **127** |

The 119 acquired source rows represent 112 unique films. Seven acquired rows are duplicates after resolution: six repeated numeric identifiers and the IMDb identifier that resolves to an existing TMDb ID.

The distinct resolved identifier count is 117: 112 successfully acquired identifiers and five identifiers that returned 404 responses.

The five unavailable identifiers are:

| Source ledger row | TMDb ID | Outcome |
|---:|---:|---|
| 18 | 8471293 | HTTP 404 |
| 35 | 9412887 | HTTP 404 |
| 73 | 8471294 | HTTP 404 |
| 93 | 9412888 | HTTP 404 |
| 99 | 7733901 | HTTP 404 |

The invalid entries are `-1` and `N/A`. One additional source entry is blank.

The reconciliation is retained in `data/processed/id_reconciliation.csv`, including the original identifier, normalized value, resolved identifier, status, duplicate flag and failure reason.

No source rows were silently removed. Duplicate records were not fetched repeatedly, but their original source-row lineage remains represented.

## 4. Ranked Data Quality Risks

The following ranking considers the potential effect of each issue on the completeness, comparability and business interpretation of the analysis.

### Risk 1 — Incomplete candidate coverage and selection bias

**Severity: High**

**Finding:** Five distinct candidate identifiers returned HTTP 404 responses and were not included in the 112-film analysis. The original list also contained two invalid identifiers and one blank entry.

**Detection:** Identifier validation, TMDb lookup results and row-level reconciliation.

**Potential impact:** The unavailable films may have different financial performance, franchise membership or genre characteristics from the successfully retrieved films. If the excluded candidates belong to a franchise or perform particularly well or poorly, their absence could change the relative comparison between licensing categories.

**Recommendation:** Obtain corrected identifiers or confirm the records are genuinely unavailable. Re-run the acquisition and analysis when corrections are received. Preserve the current reconciliation so that excluded candidates remain visible.

**Business consequence:** The shortlist should be treated as a screening recommendation based on the available sample, not a definitive ranking of every candidate supplied.

### Risk 2 — Historical financial values are not inflation-adjusted

**Severity: High**

**Finding:** Budget and revenue values are compared in their reported nominal amounts. No inflation adjustment has been applied.

**Detection:** Review of the financial fields and calculation methodology; comparison of films across different release periods.

**Potential impact:** Older films may appear unusually strong or weak when compared directly with newer films because the purchasing power of money, ticket prices and production costs have changed over time. This is particularly important for the all-years comparison.

**Recommendation:** Obtain a consistent external inflation reference series and document the adjustment method before making cross-decade financial comparisons. Keep nominal and adjusted results separate.

**Business consequence:** The all-years results should not be used alone to establish the relative commercial attractiveness of older and newer content. The post-2000 comparison provides a narrower time window, but it is not a complete solution to differences in release-year economics.

### Risk 3 — Box-office metrics are not licensing returns or studio profit

**Severity: High**

**Finding:** The financial analysis uses reported production budgets and theatrical gross revenue. Gross revenue less budget is not studio profit, and revenue-to-budget return is not a licensing return.

**Detection:** Review of the source fields and formulas used in `movie_financial_metrics.csv` and the licensing-unit tables.

**Potential impact:** The calculations exclude marketing, distribution, exhibitor shares, taxes, financing costs and other expenses. They also do not measure streaming demand, subscriber acquisition, retention, licensing fees or StreamVault's expected contribution.

**Recommendation:** Treat the metrics as historical screening indicators only. Obtain title-level licensing quotations, rights information and expected audience or contribution forecasts before making a financial commitment.

**Business consequence:** A high historical gross return does not prove that a title or bundle is worth its asking price.

### Risk 4 — TMDb financial data is not independently audited

**Severity: High**

**Finding:** All 112 successfully acquired films have positive budget and revenue values in the processed financial dataset. However, positive values do not establish that the figures are accurate, complete or consistently reported.

**Detection:** Checks for populated and positive budget and revenue fields, followed by review of the source and calculation methodology.

**Potential impact:** Incorrect or inconsistent financial values can distort film-level returns, franchise aggregates, rankings and the overall franchise-versus-standalone comparison.

**Recommendation:** Verify the financial figures for priority candidates against reliable industry or studio sources where possible. Record discrepancies and retain the original TMDb values separately from any verified replacements.

**Business consequence:** The shortlist should be subjected to financial due diligence before it is used to negotiate a deal.

### Risk 5 — Collection membership is only a proxy for a licensable franchise

**Severity: Medium–High**

**Finding:** The analysis uses TMDb collection membership to identify franchise bundles. A collection is classified as a franchise bundle when at least two distinct sampled films from that collection appear in the relevant analysis period. A collection represented by only one sampled film is excluded from the primary comparison.

**Detection:** Collection identifiers and sampled film counts are examined separately for the all-years and post-2000 periods.

**Potential impact:** A TMDb collection does not prove common ownership, availability of all titles, or the ability to license the films together. The sampled films may also represent only part of a larger franchise.

**Recommendation:** Verify ownership, rights availability and package structure independently. Retain the sensitivity analysis that treats single-film collection candidates as standalone units, while recognising that this is a modelling assumption rather than proof of independent intellectual property.

**Business consequence:** The classification affects the comparison. In the all-years sensitivity analysis, standalone units have a 458.57% weighted gross return compared with 452.16% for franchise bundles, although franchise bundles retain the higher median unit return. The classification assumption must therefore remain visible in the decision.

### Risk 6 — Duplicate and identifier-resolution issues

**Severity: Medium**

**Finding:** The original file contains six repeated numeric identifier occurrences. The IMDb-style identifier also resolves to TMDb ID 155, creating a seventh duplicate row in the resolved acquisition ledger.

**Detection:** Duplicate checks on the raw identifiers and again on the resolved TMDb identifiers.

**Potential impact:** Counting duplicate rows as separate films could inflate film counts, revenues, budgets and the apparent representation of a franchise.

**Recommendation:** Continue deduplicating acquisition requests by resolved TMDb ID while retaining all original source rows in the reconciliation ledger. Use unique film identifiers for analysis.

**Business consequence:** The current process avoids counting repeated source