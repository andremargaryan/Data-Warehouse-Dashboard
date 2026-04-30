-- stg_orders.sql
-- Point clé : normalisation des 3 formats de dates mixtes

DROP TABLE IF EXISTS stg_orders;

CREATE TABLE stg_orders AS
SELECT DISTINCT
    TRIM(order_id)      AS order_id,
    TRIM(customer_id)   AS customer_id,
    TRIM(product_id)    AS product_id,

    -- Gestion des 3 formats : YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY
    CASE
        WHEN order_date LIKE '__/__/____'
            THEN STRPTIME(order_date, '%d/%m/%Y')::DATE
        WHEN order_date LIKE '__-__-____'
            THEN STRPTIME(order_date, '%m-%d-%Y')::DATE
        ELSE CAST(order_date AS DATE)
    END                 AS order_date,

    CAST(quantity   AS INTEGER)                 AS quantity,
    CAST(unit_price AS DOUBLE)                  AS unit_price,
    CAST(COALESCE(discount, 0) AS DOUBLE)       AS discount,
    CAST(amount     AS DOUBLE)                  AS amount,
    LOWER(TRIM(status))                         AS status

FROM raw_orders
WHERE order_id   IS NOT NULL
  AND customer_id IS NOT NULL
  AND product_id  IS NOT NULL
  AND amount > 0;