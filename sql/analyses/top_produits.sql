-- top_produits.sql
-- Top 10 produits par revenus et taux de retour

WITH stats AS (
    SELECT
        f.product_id,
        p.product_name,
        p.category,
        p.price,
        COUNT(DISTINCT f.order_id)              AS nb_ventes,
        SUM(f.quantity)                         AS quantite_vendue,
        ROUND(SUM(f.amount), 2)                 AS revenu_total,
        ROUND(SUM(f.margin_amount), 2)          AS marge_totale,
        SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END) AS nb_retours
    FROM fact_orders f
    JOIN dim_products p ON f.product_id = p.product_id
    WHERE f.status = 'completed'
    GROUP BY f.product_id, p.product_name, p.category, p.price
)
SELECT
    product_id,
    product_name,
    category,
    price,
    nb_ventes,
    quantite_vendue,
    revenu_total,
    marge_totale,
    nb_retours,
    ROUND(nb_retours * 100.0 / NULLIF(nb_ventes, 0), 2) AS taux_retour_pct,
    RANK() OVER (ORDER BY revenu_total DESC)             AS rang_revenu
FROM stats
ORDER BY revenu_total DESC
LIMIT 10;