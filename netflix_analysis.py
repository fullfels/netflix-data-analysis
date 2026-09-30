"""Run a compact exploratory analysis of the Netflix titles dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv"


def load_data(source: str = DATA_URL) -> pd.DataFrame:
    """Load the public TidyTuesday Netflix dataset."""
    return pd.read_csv(source)


def movie_durations(frame: pd.DataFrame) -> pd.Series:
    """Return movie duration as a clean numeric series in minutes."""
    movies = frame.loc[frame["type"] == "Movie", "duration"]
    return pd.to_numeric(movies.str.replace(" min", "", regex=False), errors="coerce").dropna()


def summarize(frame: pd.DataFrame) -> dict[str, object]:
    """Calculate the headline dataset statistics used in the report."""
    types = frame["type"].value_counts()
    durations = movie_durations(frame)
    countries = frame["country"].fillna("Unknown").value_counts()
    ratings = frame["rating"].value_counts()
    return {
        "rows": int(len(frame)),
        "movies": int(types.get("Movie", 0)),
        "tv_shows": int(types.get("TV Show", 0)),
        "mean_movie_duration_minutes": round(float(durations.mean()), 2),
        "top_country": str(countries.index[0]),
        "top_rating": str(ratings.index[0]),
    }


def save_charts(frame: pd.DataFrame, output_dir: Path) -> None:
    """Create the five charts used in the exploratory analysis."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    types = frame["type"].value_counts()
    ax = types.plot(kind="bar", color=["#E50914", "#221f1f"], title="Netflix movies and TV shows")
    ax.set(xlabel="Type", ylabel="Count")
    ax.tick_params(axis="x", rotation=0)
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "content_types.png", dpi=160)
    plt.close(ax.figure)

    countries = frame["country"].fillna("Unknown").value_counts().head(10).sort_values()
    ax = countries.plot(kind="barh", color="#E50914", title="Top 10 countries by title count")
    ax.set(xlabel="Count", ylabel="Country")
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "top_countries.png", dpi=160)
    plt.close(ax.figure)

    by_year = frame.groupby("release_year").size().tail(15)
    ax = by_year.plot(kind="line", marker="o", color="#E50914", title="Titles released by year")
    ax.set(xlabel="Release year", ylabel="Count")
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "release_years.png", dpi=160)
    plt.close(ax.figure)

    ax = movie_durations(frame).plot(kind="hist", bins=30, color="#E50914", edgecolor="black", title="Movie duration")
    ax.set(xlabel="Minutes", ylabel="Movies")
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "movie_duration.png", dpi=160)
    plt.close(ax.figure)

    ratings = frame["rating"].value_counts().head(10)
    ax = ratings.plot(kind="bar", color="#221f1f", title="Top 10 content ratings")
    ax.set(xlabel="Rating", ylabel="Count")
    ax.figure.tight_layout()
    ax.figure.savefig(output_dir / "ratings.png", dpi=160)
    plt.close(ax.figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DATA_URL, help="CSV URL or local path")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    frame = load_data(args.source)
    summary = summarize(frame)
    save_charts(frame, args.output_dir)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
