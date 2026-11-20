# StreamVault Data Contract

## Candidate input: `data/raw/id_list.csv`
- One required column: `tmdb_id`.
- Preserve every source row, including blank and duplicate entries.
- Trim surrounding whitespace only in a derived normalized field; never overwrite the supplied value.
- Positive integer values are treated as TMDb movie IDs. Values matching `tt` followed by digits are treated as IMDb IDs and resolved through TMDb. Blank and other malformed values are retained and classified, not silently dropped.

## TMDb movie response and cache
- Cache files are stored under `data/raw/movie/<tmdb_id>.json`.
- Each cache record contains an offset-aware `fetched_at` timestamp and a `data` object.
- The movie payload must contain the requested `id` and a `credits` object with list-valued `cast` and `crew`. Invalid or mismatched cache records are ignored and fetched again.
- API calls use a bearer token from the untracked `.env` file or environment variable `TMDB_API_TOKEN`. Never commit the token.

## Processed outputs
- `id_reconciliation.csv` accounts for every original candidate row and records classification, resolution, acquisition status, duplicate status and failure reason.
- Movie, cast, crew and genre tables are derived from successful API responses.
- Licensing metrics are calculated from reported budget and revenue; they are gross-revenue comparisons, not audited profit or true investment ROI.

## Business rules
- A collection is treated as a franchise bundle within a period only when at least two distinct films from that collection appear in that period.
- A collection represented by one film is excluded from the primary comparison and included as standalone only in sensitivity analysis.
- The post-2000 analysis includes release years greater than or equal to 2000.
