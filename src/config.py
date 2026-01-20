"""Project configuration for paths and constants."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SQL_DIR = PROJECT_ROOT / "sql"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

RAW_CSV_FILENAME = "online_shoppers_intention.csv"
RAW_CSV_PATH = DATA_DIR / RAW_CSV_FILENAME

DUCKDB_FILENAME = "warehouse.duckdb"
DUCKDB_PATH = PROJECT_ROOT / DUCKDB_FILENAME

STAGING_TABLE = "stg_sessions_raw"

SQL_PIPELINE_FILES = [
    "00_staging.sql",
    "10_dimensions.sql",
    "20_facts.sql",
    "30_metrics.sql",
    "99_sanity_checks.sql",
]
