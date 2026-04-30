-- dim_products.sql

DROP TABLE IF EXISTS dim_products;

CREATE TABLE dim_products AS
SELECT
    product_id,
    product_name,
    category,
    price,
    cost,
    ROUND(price - cost, 2)              AS margin_amount,
    ROUND((price - cost) / price, 4)    AS margin_rate,
    stock
FROM stg_products;