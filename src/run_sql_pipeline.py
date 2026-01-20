"""Run SQL pipeline files in order against DuckDB."""

from __future__ import annotations

from pathlib import Path

import duckdb

from config import DUCKDB_PATH, SQL_DIR, SQL_PIPELINE_FILES


def read_sql_file(path: Path) -> str:
    """Read a SQL file and return its contents."""
    if not path.exists():
        raise FileNotFoundError(f"Missing SQL file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    """Execute SQL files in order to build the warehouse."""
    with duckdb.connect(DUCKDB_PATH.as_posix()) as conn:
        for filename in SQL_PIPELINE_FILES:
            sql_path = SQL_DIR / filename
            print(f"Running {sql_path.name}...")
            sql = read_sql_file(sql_path)
            conn.execute(sql)
        print("SQL pipeline completed.")


if __name__ == "__main__":
    main()
