"""Reusable licensing and talent analysis functions."""
import numpy as np
import pandas as pd

def build_licensing_units(period_movies, include_single_collections=False):
    period_movies = period_movies.copy()

    collection_sizes = (
        period_movies.dropna(subset=["collection_id"])
        .groupby("collection_id")["tmdb_id"]
        .nunique()
    )

    period_movies["period_collection_count"] = (
        period_movies["collection_id"].map(collection_sizes)
    )

    period_movies["licensing_type"] = np.select(
        [
            period_movies["collection_id"].isna(),
            period_movies["period_collection_count"].ge(2),
            (
                include_single_collections
                & period_movies["period_collection_count"].eq(1)
            )
        ],
        [
            "Standalone film",
            "Franchise bundle",
            "Standalone film"
        ],
        default="Single-film collection candidate"
    )

    comparable = period_movies[
        period_movies["licensing_type"].isin(
            ["Franchise bundle", "Standalone film"]
        )
    ].copy()

    comparable["licensing_unit_id"] = np.where(
        comparable["licensing_type"] == "Franchise bundle",
        "collection_" + comparable["collection_id"].astype(str),
        "movie_" + comparable["tmdb_id"].astype(str)
    )

    units = (
        comparable.groupby(
            ["licensing_type", "licensing_unit_id"],
            as_index=False
        )
        .agg(
            titles=("title", lambda x: " | ".join(x)),
            film_count=("tmdb_id", "nunique"),
            total_budget=("budget", "sum"),
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            median_film_revenue=("revenue", "median"),
            median_film_budget=("budget", "median")
        )
    )

    units["gross_revenue_less_budget"] = (
        units["total_revenue"] - units["total_budget"]
    )

    units["gross_revenue_to_budget_pct"] = np.where(
        units["total_budget"] > 0,
        units["gross_revenue_less_budget"]
        / units["total_budget"] * 100,
        np.nan
    )

    units["revenue_multiple"] = np.where(
        units["total_budget"] > 0,
        units["total_revenue"] / units["total_budget"],
        np.nan
    )

    return units, period_movies


def compare_units(unit_data, analysis_label):

    results = []

    for period_name, units in unit_data.items():

        for licensing_type, group in units.groupby("licensing_type"):

            total_budget = group["total_budget"].sum()
            total_revenue = group["total_revenue"].sum()
            total_profit = group["total_profit"].sum()

            results.append({
                "analysis": analysis_label,
                "period": period_name,
                "licensing_type": licensing_type,
                "licensing_units": len(group),
                "films": group["film_count"].sum(),
                "total_budget": total_budget,
                "total_revenue": total_revenue,
                "gross_revenue_less_budget": total_profit,
                "weighted_gross_return_pct": (
                    total_profit / total_budget * 100
                    if total_budget > 0 else np.nan
                ),
                "median_unit_gross_return_pct": (
                    group["gross_revenue_to_budget_pct"].median()
                ),
                "median_revenue_multiple": (
                    group["revenue_multiple"].median()
                )
            })

    return pd.DataFrame(results)


def analyse_talent(credits, role_name, period_name, movie_metrics, min_films=2):

    period_metrics = movie_metrics.copy()

    if period_name == "2000 onward":
        period_metrics = period_metrics[
            period_metrics["release_year"] >= 2000
        ]

    joined = credits.merge(
        period_metrics,
        on="tmdb_id",
        how="inner"
    )

    # Avoid duplicate credits for the same person and movie.
    joined = joined.drop_duplicates(
        subset=["person_id", "tmdb_id"]
    )

    performance = (
        joined.groupby(["person_id", "name"], as_index=False)
        .agg(
            film_count=("tmdb_id", "nunique"),
            titles=("title", lambda x: " | ".join(sorted(set(x)))),
            total_budget=("budget", "sum"),
            total_revenue=("revenue", "sum"),
            gross_revenue_less_budget=("profit", "sum"),
            median_movie_gross_return_pct=("movie_roi_pct", "median"),
            mean_movie_gross_return_pct=("movie_roi_pct", "mean")
        )
    )

    performance["weighted_gross_return_pct"] = np.where(
        performance["total_budget"] > 0,
        performance["gross_revenue_less_budget"]
        / performance["total_budget"] * 100,
        np.nan
    )

    performance["role"] = role_name
    performance["period"] = period_name

    # Rankings focus on repeat credits to reduce one-film outliers.
    ranked = performance[
        performance["film_count"] >= min_films
    ].copy()

    ranked = ranked.sort_values(
        ["median_movie_gross_return_pct", "film_count"],
        ascending=[False, False]
    )

    return performance, ranked
