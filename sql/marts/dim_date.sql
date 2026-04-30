-- dim_date.sql
-- Table de dates complète sur toute la période du projet

DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date AS
SELECT
    CAST(d AS DATE)                         AS date_id,
    YEAR(d)                                 AS year,
    MONTH(d)                                AS month,
    DAY(d)                                  AS day,
    QUARTER(d)                              AS quarter,
    WEEK(d)                                 AS week_number,
    DAYOFWEEK(d)                            AS day_of_week,
    DAYNAME(d)                              AS day_name,
    MONTHNAME(d)                            AS month_name,
    YEAR(d) || '-' || LPAD(MONTH(d)::VARCHAR, 2, '0') AS year_month,
    CASE WHEN DAYOFWEEK(d) IN (1, 7)
         THEN true ELSE false END           AS is_weekend
FROM (
    SELECT UNNEST(
        generate_series(
            DATE '2023-01-01',
            DATE '2024-12-31',
            INTERVAL '1 day'
        )
    ) AS d
);