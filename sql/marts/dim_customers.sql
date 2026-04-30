-- dim_customers.sql

DROP TABLE IF EXISTS dim_customers;

CREATE TABLE dim_customers AS
SELECT
    customer_id,
    first_name,
    last_name,
    first_name || ' ' || last_name  AS full_name,
    email,
    city,
    country,
    signup_date,
    age,
    CASE
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 50 THEN '35-49'
        ELSE '50+'
    END                             AS age_group
FROM stg_customers;