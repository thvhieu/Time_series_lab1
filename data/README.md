# Data contract

- Raw input: `data/raw/air_passengers.csv`.
- Canonical clean file: `data/processed/series.csv`.
- Columns: `date,value`.
- `date` must be unique, sorted, monthly and formatted as ISO date.
- `value` must be numeric and non-null in the canonical clean file.
