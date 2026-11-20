import pytest

@pytest.fixture
def tmp_project(tmp_path, monkeypatch):
    from src import config
    monkeypatch.setattr(config, "MOVIE_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(config, "MAX_RETRIES", 2)
    monkeypatch.setattr(config, "REQUEST_INTERVAL_SECONDS", 0)
    return tmp_path
