import pandas as pd
import pytest
from src.validation import classify_id, prepare_candidate_ids, unique_resolved_ids

@pytest.mark.parametrize(("value", "expected"), [
    ("", "blank"), ("  ", "blank"), ("155", "tmdb"), (" tt0468569 ", "imdb"),
    ("-1", "invalid"), ("N/A", "invalid"), ("abc", "invalid"),
])
def test_classify_id(value, expected):
    assert classify_id(value) == expected

def test_prepare_preserves_source_rows_and_original_values():
    source = pd.DataFrame({"tmdb_id": ["155", " 155 ", "", "N/A", "tt0468569"]})
    result = prepare_candidate_ids(source)
    assert result["source_row"].tolist() == [2, 3, 4, 5, 6]
    assert result["original_id"].tolist() == source["tmdb_id"].tolist()
    assert result["id_type"].tolist() == ["tmdb", "tmdb", "blank", "invalid", "imdb"]
    assert source.columns.tolist() == ["tmdb_id"]

def test_rejects_unexpected_input_columns():
    with pytest.raises(ValueError):
        prepare_candidate_ids(pd.DataFrame({"id": [1]}))

def test_unique_resolved_ids_deduplicates_in_source_order():
    frame = pd.DataFrame({"tmdb_id_resolved": ["155", "155", pd.NA, "680"]})
    assert unique_resolved_ids(frame) == [155, 680]
