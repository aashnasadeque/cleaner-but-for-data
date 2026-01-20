-- Stage cleaned data for downstream modeling
CREATE OR REPLACE VIEW stg_sessions AS
SELECT
    session_id,
    CAST(administrative AS DOUBLE) AS administrative,
    CAST(administrative_duration AS DOUBLE) AS administrative_duration,
    CAST(informational AS DOUBLE) AS informational,
    CAST(informational_duration AS DOUBLE) AS informational_duration,
    CAST(product_related AS DOUBLE) AS product_related,
    CAST(product_related_duration AS DOUBLE) AS product_related_duration,
    CAST(bounce_rates AS DOUBLE) AS bounce_rates,
    CAST(exit_rates AS DOUBLE) AS exit_rates,
    CAST(page_values AS DOUBLE) AS page_values,
    CAST(special_day AS DOUBLE) AS special_day,
    CAST(month AS TEXT) AS month,
    CAST(operating_systems AS INTEGER) AS operating_systems,
    CAST(browser AS INTEGER) AS browser,
    CAST(region AS INTEGER) AS region,
    CAST(traffic_type AS INTEGER) AS traffic_type,
    CAST(visitor_type AS TEXT) AS visitor_type,
    CAST(weekend AS INTEGER) AS weekend,
    CAST(revenue AS INTEGER) AS revenue
FROM stg_sessions_raw;
