import json
from datetime import datetime, timezone
from unittest.mock import Mock
import pytest
import requests
from src import config
from src.tmdb_client import save_to_cache, load_from_cache, get_retry_after, request_tmdb

def valid_payload(movie_id=550):
    return {
        "id": movie_id,
        "title": "Test",
        "budget": 100,
        "revenue": 200,
        "credits": {"cast": [], "crew": []},
    }

def test_cache_round_trip_and_id_validation(tmp_project):
    save_to_cache(550, valid_payload())
    assert load_from_cache(550)["data"]["title"] == "Test"
    assert load_from_cache(551) is None

def test_corrupt_cache_is_ignored(tmp_project):
    config.MOVIE_CACHE_DIR.mkdir(parents=True)
    (config.MOVIE_CACHE_DIR / "550.json").write_text("{broken", encoding="utf-8")
    assert load_from_cache(550) is None

def test_failed_cache_write_cleans_up_temp_file(tmp_project):
    payload = valid_payload()
    payload["invalid"] = object()

    with pytest.raises(TypeError):
        save_to_cache(550, payload)

    assert not (config.MOVIE_CACHE_DIR / "550.json").exists()
    assert list(config.MOVIE_CACHE_DIR.glob("550.*.tmp")) == []

def test_retry_after_numeric_header():
    response = Mock(headers={"Retry-After": "3"})
    assert get_retry_after(response) == 3.0

def test_request_retries_temporary_server_error(monkeypatch):
    first, second = Mock(status_code=503), Mock(status_code=200)
    second.json.return_value = {"ok": True}
    monkeypatch.setattr("src.tmdb_client.wait_for_request_slot", lambda: None)
    monkeypatch.setattr("src.tmdb_client.time.sleep", lambda _: None)
    monkeypatch.setattr("src.tmdb_client.requests.get", Mock(side_effect=[first, second]))
    first.raise_for_status.side_effect = requests.HTTPError("503")
    assert request_tmdb("https://example.test", token="test") == {"ok": True}

def test_request_does_not_retry_not_found(monkeypatch):
    response = Mock(status_code=404)
    response.raise_for_status.side_effect = requests.HTTPError("404")
    get = Mock(return_value=response)
    monkeypatch.setattr("src.tmdb_client.wait_for_request_slot", lambda: None)
    monkeypatch.setattr("src.tmdb_client.requests.get", get)
    with pytest.raises(requests.HTTPError):
        request_tmdb("https://example.test", token="test")
    assert get.call_count == 1

def test_rate_limit_without_retry_after_uses_exponential_backoff(monkeypatch):
    first = Mock(status_code=429, headers={})
    second = Mock(status_code=200)
    second.json.return_value = {"ok": True}

    sleep_delays = []

    monkeypatch.setattr(
        "src.tmdb_client.wait_for_request_slot",
        lambda: None,
    )
    monkeypatch.setattr(
        "src.tmdb_client.time.sleep",
        lambda delay: sleep_delays.append(delay),
    )
    monkeypatch.setattr(
        "src.tmdb_client.requests.get",
        Mock(side_effect=[first, second]),
    )

    result = request_tmdb("https://example.test", token="test")

    assert result == {"ok": True}
    assert sleep_delays == [1]

@pytest.mark.parametrize("field,value", [
    ("budget", -1),
    ("budget", "unknown"),
    ("budget", True),
    ("revenue", -1),
    ("revenue", "unknown"),
    ("revenue", True),
])
def test_invalid_financial_cache_values_are_ignored(tmp_project, field, value):
    save_to_cache(550, valid_payload())
    path = config.MOVIE_CACHE_DIR / "550.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["data"][field] = value
    path.write_text(json.dumps(record), encoding="utf-8")

    assert load_from_cache(550) is None
