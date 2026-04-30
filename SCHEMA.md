# SCHEMA — Description des tables

## Couche RAW

Tables miroir des CSV sources, sans transformation.

| Table | Source | Description |
|---|---|---|
| raw_customers | customers.csv | Données clients brutes |
| raw_products | products.csv | Catalogue produits brut |
| raw_orders | orders.csv | Commandes brutes avec anomalies |
| raw_returns | returns.csv | Retours bruts |

---

## Couche STAGING

Nettoyage, typage, dédoublonnage.

### stg_customers
| Colonne | Type | Description |
|---|---|---|
| customer_id | VARCHAR | Identifiant unique client |
| first_name | VARCHAR | Prénom (COALESCE → 'Inconnu') |
| last_name | VARCHAR | Nom |
| email | VARCHAR | Email en minuscules |
| city | VARCHAR | Ville |
| country | VARCHAR | Pays |
| signup_date | DATE | Date d'inscription |
| age | INTEGER | Âge |

### stg_products
| Colonne | Type | Description |
|---|---|---|
| product_id | VARCHAR | Identifiant unique produit |
| product_name | VARCHAR | Nom du produit |
| category | VARCHAR | Catégorie |
| price | DOUBLE | Prix de vente |
| cost | DOUBLE | Coût d'achat |
| stock | INTEGER | Stock disponible |

### stg_orders
| Colonne | Type | Description |
|---|---|---|
| order_id | VARCHAR | Identifiant unique commande |
| customer_id | VARCHAR | FK → stg_customers |
| product_id | VARCHAR | FK → stg_products |
| order_date | DATE | Date normalisée (3 formats gérés) |
| quantity | INTEGER | Quantité commandée |
| unit_price | DOUBLE | Prix unitaire |
| discount | DOUBLE | Remise (0 si NULL) |
| amount | DOUBLE | Montant total |
| status | VARCHAR | completed / pending / cancelled / refunded |

### stg_returns
| Colonne | Type | Description |
|---|---|---|
| return_id | VARCHAR | Identifiant unique retour |
| order_id | VARCHAR | FK → stg_orders |
| return_date | DATE | Date du retour |
| reason | VARCHAR | Motif du retour |
| refund_amount | DOUBLE | Montant remboursé |

---

## Couche MARTS — Schéma en étoile

### fact_orders (table de faits)
| Colonne | Type | Description |
|---|---|---|
| order_id | VARCHAR | Clé primaire |
| customer_id | VARCHAR | FK → dim_customers |
| product_id | VARCHAR | FK → dim_products |
| date_id | DATE | FK → dim_date |
| quantity | INTEGER | Quantité |
| unit_price | DOUBLE | Prix unitaire |
| discount | DOUBLE | Remise |
| amount | DOUBLE | Montant HT |
| margin_amount | DOUBLE | Marge brute calculée |
| status | VARCHAR | Statut commande |
| is_returned | BOOLEAN | Flag retour |
| refund_amount | DOUBLE | Montant remboursé |

### dim_customers
| Colonne | Type | Description |
|---|---|---|
| customer_id | VARCHAR | Clé primaire |
| full_name | VARCHAR | Nom complet |
| email | VARCHAR | Email |
| city | VARCHAR | Ville |
| age | INTEGER | Âge |
| age_group | VARCHAR | Tranche d'âge (18-24, 25-34…) |

### dim_products
| Colonne | Type | Description |
|---|---|---|
| product_id | VARCHAR | Clé primaire |
| product_name | VARCHAR | Nom |
| category | VARCHAR | Catégorie |
| price | DOUBLE | Prix |
| cost | DOUBLE | Coût |
| margin_amount | DOUBLE | Marge en € |
| margin_rate | DOUBLE | Taux de marge |

### dim_date
| Colonne | Type | Description |
|---|---|---|
| date_id | DATE | Clé primaire |
| year | INTEGER | Année |
| month | INTEGER | Mois |
| day | INTEGER | Jour |
| quarter | INTEGER | Trimestre |
| week_number | INTEGER | Semaine |
| day_name | VARCHAR | Nom du jour |
| month_name | VARCHAR | Nom du mois |
| year_month | VARCHAR | Format YYYY-MM |
| is_weekend | BOOLEAN | Jour de week-end |