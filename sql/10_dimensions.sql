-- Dimension tables for star schema

CREATE OR REPLACE TABLE dim_date AS
SELECT
    row_number() OVER (ORDER BY month_name, is_weekend) AS date_id,
    month_name,
    month_num,
    is_weekend
FROM (
    SELECT DISTINCT
        month AS month_name,
        CASE
            WHEN month = 'Jan' THEN 1
            WHEN month = 'Feb' THEN 2
            WHEN month = 'Mar' THEN 3
            WHEN month = 'Apr' THEN 4
            WHEN month = 'May' THEN 5
            WHEN month = 'June' THEN 6
            WHEN month = 'Jul' THEN 7
            WHEN month = 'Aug' THEN 8
            WHEN month = 'Sep' THEN 9
            WHEN month = 'Oct' THEN 10
            WHEN month = 'Nov' THEN 11
            WHEN month = 'Dec' THEN 12
            ELSE NULL
        END AS month_num,
        CASE WHEN weekend = 1 THEN TRUE ELSE FALSE END AS is_weekend
    FROM stg_sessions
) months;

CREATE OR REPLACE TABLE dim_visitor AS
SELECT
    row_number() OVER (ORDER BY visitor_type) AS visitor_id,
    visitor_type,
    CASE WHEN visitor_type = 'Returning_Visitor' THEN TRUE ELSE FALSE END AS is_returning
FROM (
    SELECT DISTINCT visitor_type
    FROM stg_sessions
) visitors;

CREATE OR REPLACE TABLE dim_device AS
SELECT
    row_number() OVER (ORDER BY operating_systems, browser) AS device_id,
    operating_systems,
    browser
FROM (
    SELECT DISTINCT operating_systems, browser
    FROM stg_sessions
) devices;

CREATE OR REPLACE TABLE dim_geo AS
SELECT
    row_number() OVER (ORDER BY region) AS geo_id,
    region
FROM (
    SELECT DISTINCT region
    FROM stg_sessions
) geos;

CREATE OR REPLACE TABLE dim_traffic AS
SELECT
    row_number() OVER (ORDER BY traffic_type) AS traffic_id,
    traffic_type
FROM (
    SELECT DISTINCT traffic_type
    FROM stg_sessions
) traffic;
