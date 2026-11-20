"""Central configuration for StreamVault Licensing Analysis."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MOVIE_CACHE_DIR = RAW_DIR / "movie"
SOURCE_FILE = RAW_DIR / "id_list.csv"
FETCH_LOG_FILE = RAW_DIR / "_fetch_log.csv"
RECONCILIATION_FILE = PROCESSED_DIR / "id_reconciliation.csv"

TMDB_API_BASE_URL = "https://api.themoviedb.org/3"
REQUEST_TIMEOUT = (5, 30)
MAX_WORKERS = 4
MAX_RETRIES = 4
REQUEST_INTERVAL_SECONDS = 0.25
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}
REFRESH_CACHE = False

for directory in (RAW_DIR, PROCESSED_DIR, MOVIE_CACHE_DIR):
    directory.mkdir(parents=True, exist_ok=True)
