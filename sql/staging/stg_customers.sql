-- stg_customers.sql
-- Nettoyage : trim, nulls, doublons, normalisation

DROP TABLE IF EXISTS stg_customers;

CREATE TABLE stg_customers AS
SELECT DISTINCT
    TRIM(customer_id)                        AS customer_id,
    TRIM(COALESCE(first_name, 'Inconnu'))    AS first_name,
    TRIM(COALESCE(last_name,  'Inconnu'))    AS last_name,
    LOWER(TRIM(COALESCE(email, 'no-email@unknown.com'))) AS email,
    TRIM(COALESCE(city, 'Ville inconnue'))   AS city,
    TRIM(country)                            AS country,
    CAST(signup_date AS DATE)                AS signup_date,
    CAST(COALESCE(age, 0) AS INTEGER)        AS age
FROM raw_customers
WHERE customer_id IS NOT NULL;