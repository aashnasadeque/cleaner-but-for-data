"""Load raw CSV into DuckDB staging table with normalized schema."""

from __future__ import annotations

import re
from typing import Dict

import duckdb
import pandas as pd

from config import ARTIFACTS_DIR, DUCKDB_PATH, RAW_CSV_PATH, STAGING_TABLE


def to_snake_case(column: str) -> str:
    """Convert a column name to snake_case."""
    column = re.sub(r"[^a-zA-Z0-9]+", "_", column.strip())
    column = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", column)
    return column.lower().strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and basic types in the raw dataset."""
    rename_map: Dict[str, str] = {col: to_snake_case(col) for col in df.columns}
    df = df.rename(columns=rename_map)

    # Ensure expected boolean columns are 0/1 integers
    for col in ["weekend", "revenue"]:
        if col in df.columns:
            df[col] = df[col].astype(int)

    # Ensure month is text
    if "month" in df.columns:
        df["month"] = df["month"].astype(str)

    # Ensure duration columns are floats
    duration_cols = [
        "administrative_duration",
        "informational_duration",
        "product_related_duration",
    ]
    for col in duration_cols:
        if col in df.columns:
            df[col] = df[col].astype(float)

    return df


def main() -> None:
    """Load raw CSV into DuckDB and create the staging table."""
    if not RAW_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Missing raw CSV at {RAW_CSV_PATH}. See data/README.md for details."
        )

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_CSV_PATH)
    df = normalize_columns(df)

    with duckdb.connect(DUCKDB_PATH.as_posix()) as conn:
        conn.register("raw_df", df)
        conn.execute(f"DROP TABLE IF EXISTS {STAGING_TABLE};")
        conn.execute(
            f"""
            CREATE TABLE {STAGING_TABLE} AS
            SELECT
                row_number() OVER () AS session_id,
                *
            FROM raw_df
            """
        )

    print(f"Loaded {len(df):,} rows into {STAGING_TABLE} in {DUCKDB_PATH}.")


if __name__ == "__main__":
    main()
