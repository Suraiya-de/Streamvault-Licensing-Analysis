# Initial Data Investigation Findings

## 1. Dataset Overview

The original candidate dataset, `data/raw/id_list.csv`, contains 127 data rows and one column, `tmdb_id`.

The IDs were loaded as strings to preserve their original representation, including blank entries and literal `N/A` values.

## 2. Initial Data Quality Findings

| Finding | Count |
|---|---:|
| Total original rows | 127 |
| Blank entries | 1 |
| Duplicate occurrences | 6 |
| Distinct nonblank values | 120 |
| Negative IDs | 1 |
| IMDb-style identifiers | 1 |
| Unexpected text values | 1 |

The six duplicated IDs are 155, 680, 278, 603, 1891 and 550. Each appears twice.

## 3. Records Requiring Attention

| Original row | Value | Issue |
|---:|---|---|
| 29 | -1 | Negative identifier |
| 68 | Blank | Missing identifier |
| 94 | tt0468569 | IMDb-style identifier |
| 110 | N/A | Unexpected text value |
| 42, 59, 89, 90, 93, 101 | See duplicate findings | Repeated identifiers |

## 4. Row Reconciliation

The original dataset reconciles as follows:

127 = 1 blank row + 6 duplicate occurrences + 120 distinct nonblank values.

Every original row is accounted for.

## 5. Preliminary Assessment

The dataset contains missing, duplicated and incorrectly formatted identifiers.

The numeric-looking identifiers have not yet been verified against TMDb. Therefore, their appearance alone does not establish that they correspond to existing movie records.

No records have been deleted or modified. Further validation will determine which candidates can be used in the licensing analysis.