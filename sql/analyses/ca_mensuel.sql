-- ca_mensuel.sql
-- CA mensuel + croissance MoM (month-over-month)

WITH monthly AS (
    SELECT
        d.year_month,
        d.year,
        d.month,
        ROUND(SUM(f.amount), 2)       AS ca,
        COUNT(DISTINCT f.order_id)    AS nb_commandes,
        ROUND(AVG(f.amount), 2)       AS panier_moyen
    FROM fact_orders f
    JOIN dim_date d ON f.date_id = d.date_id
    WHERE f.status = 'completed'
    GROUP BY d.year_month, d.year, d.month
)
SELECT
    year_month,
    year,
    month,
    ca,
    nb_commandes,
    panier_moyen,
    LAG(ca) OVER (ORDER BY year, month)  AS ca_mois_precedent,
    ROUND(
        (ca - LAG(ca) OVER (ORDER BY year, month))
        / NULLIF(LAG(ca) OVER (ORDER BY year, month), 0) * 100
    , 2)                                 AS croissance_mom_pct
FROM monthly
ORDER BY year, month;