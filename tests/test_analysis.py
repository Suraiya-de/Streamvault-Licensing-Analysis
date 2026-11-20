import pandas as pd
import pytest
from src.analysis import build_licensing_units, compare_units


def sample_movies():
    return pd.DataFrame(
        [
            {
                "tmdb_id": 1,
                "title": "A1",
                "collection_id": 10,
                "budget": 100,
                "revenue": 250,
                "profit": 150,
            },
            {
                "tmdb_id": 2,
                "title": "A2",
                "collection_id": 10,
                "budget": 100,
                "revenue": 200,
                "profit": 100,
            },
            {
                "tmdb_id": 3,
                "title": "Solo",
                "collection_id": float("nan"),
                "budget": 50,
                "revenue": 100,
                "profit": 50,
            },
            {
                "tmdb_id": 4,
                "title": "One collection",
                "collection_id": 20,
                "budget": 25,
                "revenue": 50,
                "profit": 25,
            },
        ]
    )


def test_primary_classification_excludes_single_film_collection_candidate():
    units, classified = build_licensing_units(sample_movies())
    assert classified["licensing_type"].value_counts().to_dict() == {
        "Franchise bundle": 2,
        "Standalone film": 1,
        "Single-film collection candidate": 1,
    }
    assert set(units["licensing_type"]) == {"Franchise bundle", "Standalone film"}


def test_sensitivity_treats_single_film_collection_as_standalone():
    units, classified = build_licensing_units(
        sample_movies(), include_single_collections=True
    )
    assert (classified["licensing_type"] == "Standalone film").sum() == 2
    assert len(units) == 3


def test_comparison_calculates_weighted_gross_return():
    units, _ = build_licensing_units(sample_movies())
    result = compare_units({"All release years": units}, "test")
    franchise = result[result["licensing_type"] == "Franchise bundle"].iloc[0]
    assert franchise["weighted_gross_return_pct"] == pytest.approx(125.0)


def test_talent_analysis_uses_explicit_movie_metrics():
    from src.analysis import analyze_talent

    metrics = pd.DataFrame(
        [
            {
                "tmdb_id": 1,
                "title": "A",
                "release_year": 2001,
                "budget": 100,
                "revenue": 200,
                "profit": 100,
                "movie_roi_pct": 100.0,
            },
            {
                "tmdb_id": 2,
                "title": "B",
                "release_year": 2002,
                "budget": 100,
                "revenue": 300,
                "profit": 200,
                "movie_roi_pct": 200.0,
            },
        ]
    )
    credits = pd.DataFrame(
        [
            {"tmdb_id": 1, "person_id": 7, "name": "Person", "job": "Director"},
            {"tmdb_id": 2, "person_id": 7, "name": "Person", "job": "Director"},
        ]
    )
    all_rows, ranked = analyze_talent(credits, "Director", "All release years", metrics)
    assert all_rows.iloc[0]["film_count"] == 2
    assert len(ranked) == 1

def test_franchise_titles_are_sorted_and_deduplicated():
    movies = sample_movies()
    movies.loc[0, "title"] = "Zulu"
    movies.loc[1, "title"] = "Alpha"

    # Add another film with the same title to test deduplication.
    duplicate = movies.loc[[1]].copy()
    duplicate["tmdb_id"] = 5
    movies = pd.concat([movies, duplicate], ignore_index=True)

    units, _ = build_licensing_units(movies)

    franchise = units[
        units["licensing_type"] == "Franchise bundle"
    ].iloc[0]

    assert franchise["titles"] == "Alpha | Zulu"


def test_comparison_distinguishes_units_from_films():
    units, _ = build_licensing_units(sample_movies())

    result = compare_units({"All release years": units}, "test")

    franchise = result[
        result["licensing_type"] == "Franchise bundle"
    ].iloc[0]

    assert franchise["licensing_units"] == 1
    assert franchise["films"] == 2