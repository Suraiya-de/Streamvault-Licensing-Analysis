"""TMDb HTTP, retry and local-cache helpers."""
import json
import os
import tempfile
import threading
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from . import config

_request_lock = threading.Lock()
_last_request_time = 0.0

def get_api_token():
    """Load the token from .env or the process environment without printing it."""
    load_dotenv(config.PROJECT_ROOT / ".env")
    token = os.getenv("TMDB_API_TOKEN")
    if not token:
        raise ValueError("TMDB_API_TOKEN was not found. Check your .env file.")
    return token

def cache_path(movie_id):
    return config.MOVIE_CACHE_DIR / f"{int(movie_id)}.json"

def save_to_cache(movie_id, payload):
    config.MOVIE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "data": payload,
    }

    final_path = cache_path(movie_id)
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=config.MOVIE_CACHE_DIR,
            prefix=f"{final_path.stem}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(record, handle, ensure_ascii=False, indent=2)

        temp_path.replace(final_path)

    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()

def load_from_cache(movie_id):
    path = cache_path(movie_id)
    if not path.exists():
        return None
    try:
        with path.open(encoding="utf-8") as handle:
            record = json.load(handle)
        fetched_at = datetime.fromisoformat(record["fetched_at"])
        data = record["data"]
        if fetched_at.utcoffset() is None or not isinstance(data, dict) or data.get("id") != int(movie_id):
            return None
        credits = data.get("credits")
        if not isinstance(credits, dict) or not isinstance(credits.get("cast"), list) or not isinstance(credits.get("crew"), list):
            return None
        return record
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None

def wait_for_request_slot():
    """Space out request starts across concurrent workers."""
    global _last_request_time
    with _request_lock:
        elapsed = time.monotonic() - _last_request_time
        delay = config.REQUEST_INTERVAL_SECONDS - elapsed
        if delay > 0:
            time.sleep(delay)
        _last_request_time = time.monotonic()

def get_retry_after(response):
    value = response.headers.get("Retry-After")
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_time = parsedate_to_datetime(value)
            if retry_time.tzinfo is None:
                retry_time = retry_time.replace(tzinfo=timezone.utc)
            return max(0.0, (retry_time - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError):
            return None

def request_tmdb(url, params=None, token=None):
    """GET a TMDb endpoint, retrying only rate limits and transient failures."""
    token = token or get_api_token()
    headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
    for attempt in range(config.MAX_RETRIES + 1):
        try:
            wait_for_request_slot()
            response = requests.get(url, headers=headers, params=params, timeout=config.REQUEST_TIMEOUT)
            if response.status_code == 429 or response.status_code in config.RETRYABLE_STATUS_CODES:
                if attempt == config.MAX_RETRIES:
                    response.raise_for_status()
                # Request spacing is enforced separately by wait_for_request_slot().
                # This is additional exponential backoff when Retry-After is unavailable.
                wait = get_retry_after(response) if response.status_code == 429 else None
                time.sleep(wait if wait is not None else 2 ** attempt)
                continue
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt == config.MAX_RETRIES:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("TMDb request failed after all retry attempts.")

def get_movie(movie_id, token=None, refresh_cache=None):
    """Return validated movie data from cache or TMDb."""
    refresh = config.REFRESH_CACHE if refresh_cache is None else refresh_cache
    if not refresh:
        cached = load_from_cache(movie_id)
        if cached is not None:
            return cached["data"]
    payload = request_tmdb(f"{config.TMDB_API_BASE_URL}/movie/{int(movie_id)}", {"append_to_response": "credits"}, token=token)
    if not isinstance(payload, dict) or payload.get("id") != int(movie_id):
        raise ValueError(f"TMDb returned an invalid or unexpected movie ID for {movie_id}.")
    save_to_cache(movie_id, payload)
    return payload
