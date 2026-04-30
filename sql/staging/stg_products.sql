-- stg_products.sql

DROP TABLE IF EXISTS stg_products;

CREATE TABLE stg_products AS
SELECT DISTINCT
    TRIM(product_id)                            AS product_id,
    TRIM(product_name)                          AS product_name,
    TRIM(category)                              AS category,
    CAST(price AS DOUBLE)                       AS price,
    CAST(cost  AS DOUBLE)                       AS cost,
    CAST(COALESCE(stock, 0) AS INTEGER)         AS stock
FROM raw_products
WHERE product_id IS NOT NULL
  AND price > 0;