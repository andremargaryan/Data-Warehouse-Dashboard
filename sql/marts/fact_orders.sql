-- fact_orders.sql
-- Table de faits centrale avec métriques et clés étrangères

DROP TABLE IF EXISTS fact_orders;

CREATE TABLE fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date                            AS date_id,

    -- Métriques
    o.quantity,
    o.unit_price,
    o.discount,
    o.amount,
    ROUND(o.amount * p.margin_rate, 2)      AS margin_amount,
    o.status,

    -- Flag retour
    CASE WHEN r.order_id IS NOT NULL
         THEN true ELSE false END           AS is_returned,
    r.refund_amount

FROM stg_orders o
LEFT JOIN dim_products  p ON o.product_id  = p.product_id
LEFT JOIN dim_customers c ON o.customer_id = c.customer_id
LEFT JOIN stg_returns   r ON o.order_id    = r.order_id;