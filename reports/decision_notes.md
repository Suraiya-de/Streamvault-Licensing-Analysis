# StreamVault Licensing Analysis — Decision Notes

## 1. Decision question

Assess whether StreamVault should prioritise franchise bundles or standalone films when screening content opportunities for a proposed $14 million licensing decision.

The analysis uses 112 unique successfully acquired films from the supplied candidate list. It is a screening exercise, not a complete catalogue valuation or a recommendation to commit the full budget.

The central question is which content opportunities deserve further commercial and legal due diligence, not which titles StreamVault should purchase at any price.

## 2. Data quality and scope

The original source file contained 127 data rows.

The acquisition and reconciliation process identified:

- 119 acquired source rows, including duplicate entries.
- 112 unique successfully acquired films.
- Five distinct valid-looking TMDb identifiers returning HTTP 404.
- Two invalid identifiers (`-1` and `N/A`).
- One blank identifier.
- Seven duplicate rows after identifier resolution: six repeated numeric identifiers and one IMDb identifier resolving to an already-listed TMDb ID.

The 112 acquired films form the analysis sample. The five unavailable identifiers remain unresolved and could affect the results if their absence is not random.

Budget and revenue values were populated with positive values for the 112 films, but this does not independently establish their accuracy.

The original source file was preserved. Identifier reconciliation, source-row lineage and acquisition failures are retained in `data/processed/id_reconciliation.csv`.

See `docs/findings.md` for the detailed data-quality assessment.

## 3. Licensing-unit definitions

The primary classification treats a collection with at least two sampled films in the relevant analysis period as a franchise bundle.

Films without a collection ID are classified as standalone films. Films belonging to a collection with only one sampled film in the period are excluded from the primary comparison as single-film collection candidates.

A sensitivity analysis instead treats these single-film collection candidates as standalone licensing units. This is a modelling assumption, not confirmation that the film is independent intellectual property.

The classification is recalculated separately for all release years and for films released from 2000 onward.

The resulting primary comparison contains:

| Period | Franchise bundles | Standalone films | Total units |
|---|---:|---:|---:|
| All release years | 23 | 16 | 39 |
| 2000 onward | 17 | 8 | 25 |

The all-years analysis excludes nine single-film collection candidates from the primary comparison. The post-2000 analysis excludes seven.

## 4. Financial methodology

For each film:

- Gross revenue less production budget = reported revenue minus reported production budget.
- Gross revenue-to-budget return (%) = (reported revenue minus reported production budget) / reported production budget × 100.
- Revenue multiple = reported revenue / reported production budget.

For licensing units, budgets and revenues are aggregated across the films in each unit. Weighted gross return is calculated using the aggregated budget and revenue. Median unit return is also reported to reduce reliance on a single very large unit.

These metrics are box-office screening proxies.

Gross revenue less production budget is not studio profit. The calculations exclude marketing, distribution, exhibitor shares, taxes, financing costs and other expenses. They also do not measure licensing fees, streaming demand, subscriber acquisition, retention or StreamVault's expected cash flows.

No inflation adjustment has been applied. Nominal financial values from different release periods should therefore not be interpreted as directly comparable in purchasing-power terms.

## 5. Main findings

In the primary comparison, franchise bundles outperform standalone films on weighted and median gross return in both periods.

| Period | Licensing type | Weighted gross return | Median unit return |
|---|---|---:|---:|
| All years | Franchise bundles | 452.16% | 455.11% |
| All years | Standalone films | 384.95% | 284.48% |
| 2000 onward | Franchise bundles | 415.11% | 361.15% |
| 2000 onward | Standalone films | 324.04% | 284.48% |

### Sensitivity analysis

When single-film collection candidates are treated as standalone licensing units:

- All years: standalone weighted return rises to 458.57%, compared with 452.16% for franchises. However, the franchise median remains higher at 455.11%, compared with 400% for standalone units.
- Post-2000: franchises retain the advantage on weighted return (415.11% versus 328.84%) and median return (361.15% versus 325.21%).

The all-years weighted comparison therefore changes direction under the alternative classification. The post-2000 comparison is more consistent in favour of franchises.

The franchise recommendation is supported by the primary results, but it is not unconditional. The classification assumption and sensitivity result must accompany any decision based on the comparison.

## 6. Content shortlist and prioritisation

### Franchise candidates

The strongest franchise candidates by the observed post-2000 gross revenue-to-budget comparison are:

| Priority | Franchise | Films | Reported budget | Reported gross revenue | Gross return |
|---:|---|---:|---:|---:|---:|
| 1 | The Lord of the Rings | 3 | $266m | $2.92bn | 996.45% |
| 2 | Ice Age | 3 | $229m | $1.93bn | 743.21% |
| 3 | The Avengers | 4 | $1.111bn | $7.92bn | 612.81% |

Harry Potter is a further candidate worth investigating. Its eight sampled post-2000 films generated approximately $7.76bn in reported gross revenue against $1.28bn in reported production budgets, giving a 506.23% gross return.

The Lord of the Rings is the first candidate I would send to commercial and rights due diligence because it has the strongest observed return among these post-2000 franchise bundles. Ice Age is the second candidate based on its strong return and lower aggregate reported production budget. The Avengers is third: it has the highest total gross revenue among these three, but also a much larger reported production budget and a lower gross return.

This is a priority order for investigation, not a purchase recommendation. The dataset does not establish whether the titles are available, what their licensing fees would be, or whether their audiences match StreamVault's target market.

### Strict standalone candidates — all years

The highest-return standalone screening candidates include:

1. The Good, the Bad and the Ugly
2. Pulp Fiction
3. Schindler's List
4. Spirited Away
5. Forrest Gump

These results are historical nominal comparisons and should be treated cautiously because the films span different release periods.

### Strict standalone candidates — post-2000

The post-2000 standalone shortlist is:

1. Spirited Away
2. Inception
3. Interstellar
4. Memento
5. The Departed

The standalone shortlist changes materially when the analysis is restricted to post-2000 releases. This reinforces the importance of evaluating both time windows rather than relying exclusively on all-years results.

## 7. Talent analysis

Director and lead-actor performance is assessed by joining credits to movie financial metrics.

Lead actors are defined as the first three cast members by cast order. Directors are identified using the crew job value `Director`.

The analysis considers repeat contributors with at least two sampled films when discussing consistency.

Examples in the post-2000 sample include:

- Peter Jackson: six films, approximately 475.99% weighted gross return.
- Christopher Nolan: seven films, approximately 337.86% weighted gross return.
- Carlos Saldanha: two films, approximately 810.40% weighted gross return.
- Daniel Radcliffe: eight films, approximately 506.23% weighted gross return.
- Robert Downey Jr.: seven films, approximately 526.53% weighted gross return.
- Ian McKellen: six films, approximately 475.99% weighted gross return.

These figures are descriptive associations, not evidence that an individual caused a film's financial outcome. Multiple actors may share identical results because they appear in the same franchise films. The results should not be interpreted as independent causal measurements of talent.

## 8. Ranked decision risks

| Risk | Priority | Why it matters |
|---|---|---|
| Rights availability and licensing price are unknown | Critical | A strong historical performer may be unavailable or commercially unaffordable. |
| Historical gross revenue is not licensing value | High | Box-office performance does not establish StreamVault's expected return. |
| Financial data is not independently verified | High | Incorrect budgets or revenues can change rankings and comparisons. |
| Five candidate IDs remain unavailable | High | Excluded films could change the sample and shortlist. |
| No inflation adjustment | High | Cross-decade nominal comparisons may be misleading. |
| Collection membership is a proxy | Medium–High | TMDb collection membership does not establish common ownership or licensable package rights. |
| Duplicate and invalid identifiers | Medium | Incorrect handling could inflate counts or omit candidates; the current reconciliation addresses these issues. |
| Talent comparisons are descriptive | Medium | Shared film outcomes and limited samples prevent causal conclusions. |

### Cost of getting the decision wrong

If StreamVault treats historical box-office returns as licensing returns, it could overpay for a package that does not generate sufficient audience demand or contribution.

If the franchise classification is wrong, the comparison may direct attention towards bundles that cannot actually be licensed together. If unavailable records contain materially different results, the current shortlist could also be biased.

The potential cost is not limited to the licensing fee. It includes opportunity cost, contractual restrictions, operating costs and the risk of tying up capital in content that does not meet platform objectives.

## 9. Decision conditions

Before committing funds, StreamVault should:

1. Confirm ownership and licensable rights for each title.
2. Verify territory, term, exclusivity, platform, language and window restrictions.
3. Obtain actual licensing quotations and payment schedules.
4. Forecast audience demand and expected incremental value to StreamVault.
5. Calculate contribution after licensing fees and relevant operating and distribution costs.
6. Compare the proposed package against alternative content opportunities.
7. Conduct legal and commercial due diligence before signing.
8. Revisit the analysis when the five unavailable candidate records are resolved.

The proposed $14 million decision cannot be justified by gross revenue-to-budget ratios alone. The analysis supports prioritising candidates for diligence; it does not establish a defensible licensing price, budget allocation or purchase approval.

## 10. Recommended data pipeline improvement

For a catalogue expected to grow to approximately 500 titles and be refreshed quarterly, implement an incremental, resumable acquisition and analysis pipeline.

The existing acquisition process already uses caching, request throttling, transient retries, failure logging, identifier reconciliation and source-row lineage.

Retain these controls and extend the pipeline with:

- Scheduled quarterly refreshes.
- Explicit schema and data-quality validation.
- Change detection for financial and metadata fields.
- Automated unit tests for classification and financial calculations.
- Dated snapshots of quarterly outputs.
- A run summary reporting processed, cached, updated and failed records.

Measure the improvement using runtime, API request volume, cache-hit rate, failure rate, duplicate rate and the proportion of records reconciled to source rows.

Compare these measures across a repeat run and a simulated larger catalogue. Do not claim a measured performance gain until the benchmark has actually been run and recorded.