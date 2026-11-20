# StreamVault Licensing Analysis — Decision Notes

## 1. Decision question

Assess whether StreamVault should prioritise franchise bundles or standalone films when screening content opportunities for a proposed $14 million licensing decision.

The available dataset contains 112 successfully retrieved movie records. It is a screening dataset, not a complete catalogue of licensable rights.

## 2. Data quality and scope

- The original source file contained 127 data rows.
- One row was blank and two values were invalid identifiers.
- Duplicate source entries were reconciled.
- Five valid-looking TMDb lookups returned 404 responses and were recorded as failures rather than silently dropped.
- The analysis uses 112 unique successfully retrieved movie records.
- Budget and revenue were populated with positive values for the 112 records, but this does not independently verify their accuracy.

The original source file was preserved. Identifier reconciliation, source-row lineage and acquisition failures are retained in the project data.

## 3. Licensing-unit definitions

The primary classification treats a collection with at least two sampled films in the relevant analysis period as a franchise bundle. Films without a collection ID are classified as standalone films.

Films belonging to a collection with only one sampled film in the period are excluded from the primary comparison as single-film collection candidates.

A sensitivity analysis instead treats these single-film collection candidates as standalone licensing units. This is a modelling assumption, not confirmation that the film is independent intellectual property.

The classification is recalculated separately for all release years and for films released from 2000 onward.

## 4. Financial methodology

For each film:

- Gross revenue less production budget = reported revenue minus reported production budget.
- Gross revenue-to-budget return (%) = (reported revenue minus reported production budget) / reported production budget × 100.
- Revenue multiple = reported revenue / reported production budget.

For licensing units, budgets and revenues are aggregated across the films in each unit. Weighted gross return is calculated using the aggregated budget and revenue. Median unit return is also reported to reduce reliance on a single very large unit.

These metrics are box-office screening proxies. Gross revenue less production budget is not studio profit. The calculations exclude marketing, distribution, exhibitor shares, taxes, financing costs and other expenses. They also do not measure licensing fees or StreamVault's expected cash flows.

## 5. Main findings

In the primary comparison, franchise bundles outperform standalone films on weighted and median gross return in both periods.

For all release years:
- Franchise bundles: 452.16% weighted gross return; 455.11% median unit return.
- Standalone films: 384.95% weighted gross return; 284.48% median unit return.

For films released from 2000 onward:
- Franchise bundles: 415.11% weighted gross return; 361.15% median unit return.
- Standalone films: 324.04% weighted gross return; 284.48% median unit return.

In the sensitivity analysis, single-film collection candidates are treated as standalone licensing units:
- All years: standalone units have a 458.57% weighted return versus 452.16% for franchises, but the franchise median remains higher (455.11% versus 400%).
- Post-2000: franchises outperform standalone units on weighted return (415.11% versus 328.84%) and median return (361.15% versus 325.21%).

The sensitivity result shows that classification assumptions can affect the overall comparison. The primary result should therefore be read alongside the sensitivity result.

## 6. Shortlist

### Franchise screening candidates
1. The Lord of the Rings
2. Ice Age
3. The Avengers

The post-2000 franchise shortlist balances relative returns and total reported revenue. Harry Potter is a further alternative worth considering.

### Strict standalone candidates — all years
1. The Good, the Bad and the Ugly
2. Pulp Fiction
3. Schindler's List
4. Spirited Away
5. Forrest Gump

### Strict standalone candidates — post-2000
1. Spirited Away
2. Inception
3. Interstellar
4. Memento
5. The Departed

The standalone shortlist changes materially when the analysis is restricted to post-2000 releases.

## 7. Talent analysis

Director and lead-actor performance is assessed by joining credits to movie financial metrics. Lead actors are defined as the first three cast members by cast order. Directors are identified using the crew job value "Director".

The analysis considers repeat contributors with at least two sampled films when discussing consistency. One-film observations are not sufficient evidence of repeat performance.

Examples of recurring contributors in the post-2000 sample include Peter Jackson, Carlos Saldanha, Anthony Russo and Joe Russo, as well as Elijah Wood, Viggo Mortensen, John Leguizamo, Denis Leary and Ray Romano.

These associations are descriptive only. They do not demonstrate that an individual director or actor caused a film's financial result.

## 8. Assumptions, limitations and risks

1. **Third-party financial data:** TMDb budget and revenue fields may be incomplete, estimated or inconsistent.
2. **No inflation adjustment:** nominal figures across different decades are not directly comparable in purchasing-power terms.
3. **Box office is not licensing value:** historical theatrical revenue does not establish future streaming demand, subscription value or licensing affordability.
4. **No licensing quotes:** the dataset does not contain title-level licensing fees, rights availability or contractual terms.
5. **Collection membership:** TMDb collection membership is a proxy and does not establish ownership, rights availability or a package that can be licensed.
6. **Sample bias:** the 112 successful records are a limited subset of the source list and may not represent the wider content market.
7. **Talent attribution:** financial outcomes cannot be attributed to individual talent from these descriptive comparisons.
8. **Unit aggregation:** summing revenue and budget across films can favour larger bundles and does not account for release timing or differences in title-level performance.

## 9. Decision conditions

Before committing funds, StreamVault should:
- Confirm ownership and licensable rights for each title.
- Verify territory, term, exclusivity, platform, language and window restrictions.
- Obtain actual licensing quotations and payment schedules.
- Forecast audience demand and expected incremental value to StreamVault.
- Calculate contribution after licensing fees and all relevant operating and distribution costs.
- Compare the proposed package against alternative content opportunities.
- Conduct legal and commercial diligence before signing.

The $14 million decision cannot be justified by gross revenue-to-budget ratios alone. The analysis supports prioritising candidates for diligence, not approving a purchase price.

## 10. Recommended improvement

For a catalogue expected to grow to approximately 500 titles and be refreshed quarterly, implement an incremental, resumable acquisition and analysis pipeline.

The existing acquisition process already uses caching, request throttling, transient retries, failure logging, identifier reconciliation and source-row lineage. Retain these controls and extend the pipeline with:
- Scheduled quarterly refreshes.
- Explicit schema and data-quality validation.
- Change detection for financial and metadata fields.
- Automated unit tests for classification and financial calculations.
- A dated snapshot of each quarterly output.
- A run summary reporting processed, cached, updated and failed records.

Measure the improvement using runtime, API request volume, cache-hit rate, failure rate, duplicate rate and the proportion of records reconciled to source rows. Compare these measures across a repeat run and a simulated larger catalogue. Do not claim a measured performance gain until the benchmark has actually been run and recorded.
