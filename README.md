# Netflix Catalog Analysis

A compact exploratory data analysis of the public Netflix Movies and TV Shows dataset. The project loads the TidyTuesday copy of the data, cleans selected fields, calculates headline statistics, and exports five charts.

## Questions explored

- How many movies and TV shows are in the dataset?
- Which countries contribute the most titles?
- How did the number of releases change over time?
- What does the movie-duration distribution look like?
- Which content ratings appear most often?

## Quick start

```bash
python -m venv .venv
pip install -r requirements.txt
python netflix_analysis.py --output-dir artifacts
python -m pytest -q
```

You can also analyze a compatible local CSV:

```bash
python netflix_analysis.py --source data/netflix_titles.csv
```

## Dataset

The script uses the [TidyTuesday Netflix titles dataset](https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-20), originally collected by Flixable. The included report describes 7,787 titles and should be read as a snapshot of that historical dataset, not the current Netflix catalog.

## Repository contents

- `netflix_analysis.py` - reusable analysis functions and CLI
- `tests/` - offline tests built from a small in-memory sample
- `report/netflix_analysis_report.pdf` - original Russian-language report with charts and findings

## License

MIT
