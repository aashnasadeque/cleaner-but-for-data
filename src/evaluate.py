"""Evaluate trained models and generate plots."""

from __future__ import annotations

import json
from pathlib import Path

import duckdb
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

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


def get_feature_names(preprocessor) -> list[str]:
    """Extract feature names from the ColumnTransformer."""
    feature_names: list[str] = []
    for name, transformer, columns in preprocessor.transformers_:
        if name == "num":
            feature_names.extend(columns)
        elif name == "cat":
            encoder = transformer.named_steps["onehot"]
            feature_names.extend(encoder.get_feature_names_out(columns).tolist())
    return feature_names


def load_metrics(path: Path) -> dict:
    """Load existing metrics.json if present."""
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    """Evaluate trained models and save plots/metrics."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_training_data()
    target = "converted"

    feature_cols = [col for col in df.columns if col != target]
    X = df[feature_cols]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    log_reg = joblib.load(ARTIFACTS_DIR / "logistic_regression.joblib")
    rf = joblib.load(ARTIFACTS_DIR / "random_forest.joblib")

    models = {"logistic_regression": log_reg, "random_forest": rf}
    metrics = load_metrics(ARTIFACTS_DIR / "metrics.json")
    metrics.setdefault("evaluation", {})

    plt.figure(figsize=(6, 5))
    for name, model in models.items():
        y_proba = model.predict_proba(X_test)[:, 1]
        y_pred = (y_proba >= 0.5).astype(int)
        model_metrics = {
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
            "precision": float(precision_score(y_test, y_pred)),
            "recall": float(recall_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
        }
        metrics["evaluation"][name] = model_metrics

        RocCurveDisplay.from_predictions(
            y_test, y_proba, name=name.replace("_", " ")
        )

    plt.tight_layout()
    plt.savefig(ARTIFACTS_DIR / "roc_curve.png", dpi=150)
    plt.close()

    rf_proba = rf.predict_proba(X_test)[:, 1]
    rf_pred = (rf_proba >= 0.5).astype(int)
    cm = confusion_matrix(y_test, rf_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues")
    plt.tight_layout()
    plt.savefig(ARTIFACTS_DIR / "confusion_matrix.png", dpi=150)
    plt.close()

    rf_preprocessor = rf.named_steps["preprocessor"]
    rf_features = get_feature_names(rf_preprocessor)
    rf_importances = rf.named_steps["classifier"].feature_importances_
    rf_series = pd.Series(rf_importances, index=rf_features).sort_values(ascending=False)
    rf_series.head(15).sort_values().plot(kind="barh", figsize=(8, 5))
    plt.title("Random Forest Feature Importance (Top 15)")
    plt.tight_layout()
    plt.savefig(ARTIFACTS_DIR / "feature_importance.png", dpi=150)
    plt.close()

    log_preprocessor = log_reg.named_steps["preprocessor"]
    log_features = get_feature_names(log_preprocessor)
    log_coefs = log_reg.named_steps["classifier"].coef_[0]
    log_series = pd.Series(log_coefs, index=log_features).abs().sort_values(ascending=False)
    log_series.head(15).sort_values().plot(kind="barh", figsize=(8, 5))
    plt.title("Logistic Regression Coefficient Magnitudes (Top 15)")
    plt.tight_layout()
    plt.savefig(ARTIFACTS_DIR / "logistic_coefficients.png", dpi=150)
    plt.close()

    with (ARTIFACTS_DIR / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Evaluation complete. Metrics and plots saved to artifacts/.")


if __name__ == "__main__":
    main()
