-- segmentation_clients.sql
-- Nouveaux vs récurrents, panier moyen par segment

WITH commandes_par_client AS (
    SELECT
        f.customer_id,
        COUNT(DISTINCT f.order_id)   AS nb_commandes,
        ROUND(SUM(f.amount), 2)      AS ca_total,
        ROUND(AVG(f.amount), 2)      AS panier_moyen,
        MIN(f.date_id)               AS premiere_commande,
        MAX(f.date_id)               AS derniere_commande
    FROM fact_orders f
    WHERE f.status = 'completed'
    GROUP BY f.customer_id
),
segmented AS (
    SELECT
        c.customer_id,
        c.full_name,
        c.city,
        c.age_group,
        cpc.nb_commandes,
        cpc.ca_total,
        cpc.panier_moyen,
        cpc.premiere_commande,
        cpc.derniere_commande,
        CASE
            WHEN cpc.nb_commandes = 1 THEN 'Nouveau'
            WHEN cpc.nb_commandes <= 3 THEN 'Occasionnel'
            ELSE 'Fidèle'
        END AS segment
    FROM commandes_par_client cpc
    JOIN dim_customers c ON cpc.customer_id = c.customer_id
)
SELECT
    segment,
    COUNT(*)                        AS nb_clients,
    ROUND(AVG(nb_commandes), 2)     AS moy_commandes,
    ROUND(AVG(panier_moyen), 2)     AS panier_moyen_segment,
    ROUND(SUM(ca_total), 2)         AS ca_total_segment,
    ROUND(AVG(ca_total), 2)         AS ca_moyen_par_client
FROM segmented
GROUP BY segment
ORDER BY ca_total_segment DESC;