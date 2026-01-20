-- Fact table at session grain
CREATE OR REPLACE TABLE fct_sessions AS
SELECT
    stg.session_id,
    dim_date.date_id,
    dim_visitor.visitor_id,
    dim_device.device_id,
    dim_geo.geo_id,
    dim_traffic.traffic_id,
    stg.administrative,
    stg.administrative_duration,
    stg.informational,
    stg.informational_duration,
    stg.product_related,
    stg.product_related_duration,
    stg.bounce_rates,
    stg.exit_rates,
    stg.page_values,
    stg.special_day,
    CAST(stg.administrative + stg.informational + stg.product_related AS INTEGER) AS total_pageviews,
    stg.administrative_duration
        + stg.informational_duration
        + stg.product_related_duration AS total_duration,
    CASE
        WHEN (stg.administrative + stg.informational + stg.product_related) > 0 THEN
            (
                stg.administrative_duration
                + stg.informational_duration
                + stg.product_related_duration
            )
            / (stg.administrative + stg.informational + stg.product_related)
        ELSE 0
    END AS avg_duration_per_page,
    stg.revenue AS converted
FROM stg_sessions stg
LEFT JOIN dim_date
    ON dim_date.month_name = stg.month
    AND dim_date.is_weekend = CASE WHEN stg.weekend = 1 THEN TRUE ELSE FALSE END
LEFT JOIN dim_visitor
    ON dim_visitor.visitor_type = stg.visitor_type
LEFT JOIN dim_device
    ON dim_device.operating_systems = stg.operating_systems
    AND dim_device.browser = stg.browser
LEFT JOIN dim_geo
    ON dim_geo.region = stg.region
LEFT JOIN dim_traffic
    ON dim_traffic.traffic_type = stg.traffic_type;
