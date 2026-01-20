"""Train baseline and tree-based models for conversion prediction."""

from __future__ import annotations

import json

import duckdb
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import ARTIFACTS_DIR, DUCKDB_PATH


def load_training_data() -> pd.DataFrame:
    """Load model features from DuckDB."""
    query = """
        SELECT
            fct.administrative,
            fct.administrative_duration,
            fct.informational,
            fct.informational_duration,
            fct.product_related,
            fct.product_related_duration,
            fct.bounce_rates,
            fct.exit_rates,
            fct.page_values,
            fct.special_day,
            fct.total_pageviews,
            fct.total_duration,
            fct.avg_duration_per_page,
            dim_device.operating_systems,
            dim_device.browser,
            dim_geo.region,
            dim_traffic.traffic_type,
            dim_visitor.visitor_type,
            dim_date.month_name,
            dim_date.is_weekend,
            fct.converted
        FROM fct_sessions fct
        JOIN dim_device ON dim_device.device_id = fct.device_id
        JOIN dim_geo ON dim_geo.geo_id = fct.geo_id
        JOIN dim_traffic ON dim_traffic.traffic_id = fct.traffic_id
        JOIN dim_visitor ON dim_visitor.visitor_id = fct.visitor_id
        JOIN dim_date ON dim_date.date_id = fct.date_id
    """
    with duckdb.connect(DUCKDB_PATH.as_posix()) as conn:
        return conn.execute(query).fetchdf()


def build_preprocessor(
    numeric_features: list[str], categorical_features: list[str]
) -> ColumnTransformer:
    """Create a ColumnTransformer for numeric and categorical inputs."""
    numeric_pipeline = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_pipeline = Pipeline(
        steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )


def main() -> None:
    """Train Logistic Regression and Random Forest models."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_training_data()
    target = "converted"

    numeric_features = [
        "administrative",
        "administrative_duration",
        "informational",
        "informational_duration",
        "product_related",
        "product_related_duration",
        "bounce_rates",
        "exit_rates",
        "page_values",
        "special_day",
        "total_pageviews",
        "total_duration",
        "avg_duration_per_page",
    ]
    categorical_features = [
        "operating_systems",
        "browser",
        "region",
        "traffic_type",
        "visitor_type",
        "month_name",
        "is_weekend",
    ]

    X = df[numeric_features + categorical_features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    log_reg_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, solver="lbfgs")),
        ]
    )

    rf_model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200, random_state=42, n_jobs=-1
                ),
            ),
        ]
    )

    log_reg_model.fit(X_train, y_train)
    rf_model.fit(X_train, y_train)

    joblib.dump(log_reg_model, ARTIFACTS_DIR / "logistic_regression.joblib")
    joblib.dump(rf_model, ARTIFACTS_DIR / "random_forest.joblib")

    metrics = {
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "positive_rate": float(y.mean()),
    }
    with (ARTIFACTS_DIR / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Models trained and saved to artifacts/.")


if __name__ == "__main__":
    main()
