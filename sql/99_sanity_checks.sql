-- Sanity checks for warehouse integrity

WITH
counts AS (
    SELECT
        (SELECT COUNT(*) FROM stg_sessions_raw) AS raw_rows,
        (SELECT COUNT(*) FROM fct_sessions) AS fact_rows
),
null_keys AS (
    SELECT
        SUM(CASE WHEN date_id IS NULL THEN 1 ELSE 0 END) AS null_date_id,
        SUM(CASE WHEN visitor_id IS NULL THEN 1 ELSE 0 END) AS null_visitor_id,
        SUM(CASE WHEN device_id IS NULL THEN 1 ELSE 0 END) AS null_device_id,
        SUM(CASE WHEN geo_id IS NULL THEN 1 ELSE 0 END) AS null_geo_id,
        SUM(CASE WHEN traffic_id IS NULL THEN 1 ELSE 0 END) AS null_traffic_id
    FROM fct_sessions
),
converted_values AS (
    SELECT
        SUM(CASE WHEN converted NOT IN (0, 1) THEN 1 ELSE 0 END) AS invalid_converted
    FROM fct_sessions
),
rate_bounds AS (
    SELECT
        SUM(
            CASE
                WHEN conversion_rate < 0 OR conversion_rate > 1 THEN 1 ELSE 0
            END
        ) AS invalid_rates
    FROM mart_conversion_by_month
)
SELECT 'row_count_match' AS check_name,
       CASE WHEN counts.raw_rows = counts.fact_rows THEN 'PASS' ELSE 'FAIL' END AS status,
       counts.raw_rows,
       counts.fact_rows
FROM counts
UNION ALL
SELECT 'null_dimension_keys' AS check_name,
       CASE
           WHEN (null_date_id + null_visitor_id + null_device_id + null_geo_id + null_traffic_id) = 0
           THEN 'PASS' ELSE 'FAIL'
       END AS status,
       (null_date_id + null_visitor_id + null_device_id + null_geo_id + null_traffic_id) AS null_key_count,
       NULL AS fact_rows
FROM null_keys
UNION ALL
SELECT 'converted_values_valid' AS check_name,
       CASE WHEN invalid_converted = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
       invalid_converted,
       NULL
FROM converted_values
UNION ALL
SELECT 'conversion_rate_bounds' AS check_name,
       CASE WHEN invalid_rates = 0 THEN 'PASS' ELSE 'FAIL' END AS status,
       invalid_rates,
       NULL
FROM rate_bounds;
