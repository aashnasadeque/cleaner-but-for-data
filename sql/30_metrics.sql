-- Metrics marts for analytics

CREATE OR REPLACE VIEW mart_conversion_by_month AS
SELECT
    dim_date.month_name,
    COUNT(*) AS sessions,
    SUM(fct_sessions.converted) AS conversions,
    SUM(fct_sessions.converted)::DOUBLE / NULLIF(COUNT(*), 0) AS conversion_rate
FROM fct_sessions
JOIN dim_date ON dim_date.date_id = fct_sessions.date_id
GROUP BY dim_date.month_name
ORDER BY conversion_rate DESC;

CREATE OR REPLACE VIEW mart_conversion_by_visitor AS
SELECT
    dim_visitor.visitor_type,
    COUNT(*) AS sessions,
    SUM(fct_sessions.converted) AS conversions,
    SUM(fct_sessions.converted)::DOUBLE / NULLIF(COUNT(*), 0) AS conversion_rate
FROM fct_sessions
JOIN dim_visitor ON dim_visitor.visitor_id = fct_sessions.visitor_id
GROUP BY dim_visitor.visitor_type
ORDER BY conversion_rate DESC;

CREATE OR REPLACE VIEW mart_conversion_by_traffic AS
SELECT
    dim_traffic.traffic_type,
    COUNT(*) AS sessions,
    SUM(fct_sessions.converted) AS conversions,
    SUM(fct_sessions.converted)::DOUBLE / NULLIF(COUNT(*), 0) AS conversion_rate
FROM fct_sessions
JOIN dim_traffic ON dim_traffic.traffic_id = fct_sessions.traffic_id
GROUP BY dim_traffic.traffic_type
ORDER BY conversion_rate DESC;

CREATE OR REPLACE VIEW mart_conversion_by_device AS
SELECT
    dim_device.browser,
    dim_device.operating_systems,
    COUNT(*) AS sessions,
    SUM(fct_sessions.converted) AS conversions,
    SUM(fct_sessions.converted)::DOUBLE / NULLIF(COUNT(*), 0) AS conversion_rate
FROM fct_sessions
JOIN dim_device ON dim_device.device_id = fct_sessions.device_id
GROUP BY dim_device.browser, dim_device.operating_systems
ORDER BY conversion_rate DESC;

CREATE OR REPLACE VIEW mart_behavior_summary AS
SELECT
    fct_sessions.converted,
    AVG(fct_sessions.total_pageviews) AS avg_total_pageviews,
    AVG(fct_sessions.total_duration) AS avg_total_duration,
    AVG(fct_sessions.bounce_rates) AS avg_bounce_rates,
    AVG(fct_sessions.exit_rates) AS avg_exit_rates,
    AVG(fct_sessions.page_values) AS avg_page_values
FROM fct_sessions
GROUP BY fct_sessions.converted
ORDER BY fct_sessions.converted DESC;
