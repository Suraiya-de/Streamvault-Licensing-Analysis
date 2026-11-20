"""Input classification and row-level validation helpers."""
import re
import pandas as pd

def classify_id(value):
    """Classify a normalized candidate as blank, IMDb, TMDb, or invalid."""
    value = "" if value is None or pd.isna(value) else str(value).strip()
    if value == "":
        return "blank"
    if re.fullmatch(r"tt\d+", value, flags=re.IGNORECASE):
        return "imdb"
    if re.fullmatch(r"-?\d+", value):
        return "tmdb" if int(value) > 0 else "invalid"
    return "invalid"

def prepare_candidate_ids(frame):
    """Return a copy with source-row, normalized ID and classification fields."""
    if list(frame.columns) != ["tmdb_id"]:
        raise ValueError("Expected the source CSV to contain only the 'tmdb_id' column.")
    result = frame.copy()
    result["source_row"] = range(2, len(result) + 2)
    result["original_id"] = result["tmdb_id"]
    result["normalized_id"] = result["tmdb_id"].astype("string").str.strip()
    result["id_type"] = result["normalized_id"].apply(classify_id)
    result["tmdb_id_resolved"] = pd.NA
    result["status"] = ""
    result["failure_reason"] = ""
    result.loc[result["id_type"] == "blank", "status"] = "blank"
    result.loc[result["id_type"] == "invalid", "status"] = "invalid_id"
    result.loc[result["id_type"] == "tmdb", "tmdb_id_resolved"] = result.loc[result["id_type"] == "tmdb", "normalized_id"]
    return result

def unique_resolved_ids(frame):
    """Return positive resolved TMDb IDs once each, preserving source order."""
    values = frame["tmdb_id_resolved"].dropna().astype(str).drop_duplicates().tolist()
    return [int(value) for value in values if value.isdigit() and int(value) > 0]
