"""Export mart views to CSV files in artifacts/."""

from __future__ import annotations

import duckdb

from config import ARTIFACTS_DIR, DUCKDB_PATH


MART_VIEWS = [
    "mart_conversion_by_month",
    "mart_conversion_by_visitor",
    "mart_conversion_by_traffic",
    "mart_conversion_by_device",
    "mart_behavior_summary",
]


def main() -> None:
    """Export mart views from DuckDB to CSV."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(DUCKDB_PATH.as_posix()) as conn:
        for view in MART_VIEWS:
            df = conn.execute(f"SELECT * FROM {view}").fetchdf()
            output_path = ARTIFACTS_DIR / f"{view}.csv"
            df.to_csv(output_path, index=False)
            print(f"Exported {view} to {output_path}.")


if __name__ == "__main__":
    main()
