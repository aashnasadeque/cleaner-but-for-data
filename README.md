# Lead Funnel Warehouse + ML

## Problem Statement
Build a small, end-to-end portfolio project that shows how to clean raw session data,
model it in a warehouse-style schema, run business analytics with SQL, and train a
baseline ML model to predict conversion (purchase intent).

Dataset: **Online Shoppers Purchasing Intention Dataset (UCI)**  
Label: `Revenue` (renamed to `converted`, 0/1)

---

## Project Structure

```
lead-funnel-warehouse/
├── data/
│   ├── README.md
│   └── online_shoppers_intention.csv
├── sql/
├── src/
├── artifacts/
├── notebooks/
└── requirements.txt
```

---

## Data Model (Star Schema)

Fact table: `fct_sessions` (1 row per session)  
Dimensions: `dim_date`, `dim_visitor`, `dim_device`, `dim_geo`, `dim_traffic`

```
dim_date     dim_visitor     dim_device     dim_geo     dim_traffic
   |              |              |            |            |
   +--------------+--------------+------------+------------+
                     fct_sessions
```

Note: `dim_date.is_weekend` is based on the dataset’s `Weekend` field (session occurred
on a weekend), not a calendar date.

---

## How to Run

1) Install dependencies:

```
pip install -r requirements.txt
```

2) Download the CSV into `data/` (see `data/README.md`).

3) Load raw CSV into DuckDB:

```
python src/load_to_duckdb.py
```

4) Build the warehouse model:

```
python src/run_sql_pipeline.py
```

5) Export marts to CSV:

```
python src/export_marts.py
```

6) Train models:

```
python src/train.py
```

7) Evaluate and generate plots:

```
python src/evaluate.py
```

---

## Key SQL Insights (Business Questions)

Use the marts in `sql/30_metrics.sql` to answer questions like:

1) Which month has the highest conversion rate?
2) Returning vs new visitors: which converts more?
3) Which traffic_type converts best?
4) Which browsers convert best (top 5)?
5) Compare average total_pageviews between converted vs not.
6) Compare bounce_rates summary stats by conversion.
7) High-intent sessions (e.g., total_pageviews > 10 AND exit_rates < 0.1): what’s the conversion rate?
8) Which segments (visitor_type + traffic_type) are strongest?

The marts are exported as CSVs in `artifacts/` for easy inspection.

---

## Model Results

After running `train.py` and `evaluate.py`, review `artifacts/metrics.json` and plots.
Fill in the table below with the latest metrics:

| Model | ROC-AUC | Precision | Recall | F1 |
|------|---------|-----------|--------|----|
| Logistic Regression | (from metrics.json) | (from metrics.json) | (from metrics.json) | (from metrics.json) |
| Random Forest | (from metrics.json) | (from metrics.json) | (from metrics.json) | (from metrics.json) |

Artifacts generated:
- `artifacts/roc_curve.png`
- `artifacts/confusion_matrix.png`
- `artifacts/feature_importance.png`
- `artifacts/logistic_coefficients.png`

---

## Key Findings (Update After Running)

Use `mart_*` outputs to capture 3–5 takeaways. Example structure:

- Conversion rate is highest in [Month], suggesting seasonality.
- Returning visitors convert more often than new visitors.
- Certain traffic types drive higher conversion (likely campaigns or referrals).
- Converted sessions show higher page_values and lower bounce_rates.

---

## Tradeoffs & Next Steps

- Handle class imbalance (class weights, resampling).
- Calibrate probabilities for better decision thresholds.
- Add cross-validation and hyperparameter tuning.
- Consider point-in-time feature engineering if moving to event-level data.
- Scale the pipeline to BigQuery/GCP for production workloads.

---

## Notes

This project intentionally avoids Git initialization and commits, per requirement.
