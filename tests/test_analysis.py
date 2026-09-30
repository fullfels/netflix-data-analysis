import pandas as pd

from netflix_analysis import movie_durations, summarize


def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "type": ["Movie", "Movie", "TV Show", "Movie"],
            "country": ["United States", "India", None, "United States"],
            "release_year": [2020, 2021, 2020, 2019],
            "duration": ["90 min", "110 min", "2 Seasons", "bad value"],
            "rating": ["TV-MA", "PG", "TV-MA", "R"],
        }
    )


def test_movie_durations_are_numeric_and_invalid_values_are_removed():
    durations = movie_durations(sample_data())
    assert durations.tolist() == [90.0, 110.0]


def test_summary_counts_content_types():
    summary = summarize(sample_data())
    assert summary["rows"] == 4
    assert summary["movies"] == 3
    assert summary["tv_shows"] == 1
    assert summary["mean_movie_duration_minutes"] == 100.0
