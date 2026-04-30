-- taux_retour.sql
-- Taux de retour par catégorie — indicateur qualité produit

SELECT
    p.category,
    COUNT(DISTINCT f.order_id)                          AS nb_commandes,
    SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END)      AS nb_retours,
    ROUND(
        SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(DISTINCT f.order_id), 0)
    , 2)                                                AS taux_retour_pct,
    ROUND(SUM(COALESCE(f.refund_amount, 0)), 2)         AS montant_rembourse
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.status IN ('completed', 'refunded')
GROUP BY p.category
ORDER BY taux_retour_pct DESC;