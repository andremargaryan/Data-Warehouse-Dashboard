# E-commerce Analytics — Data Warehouse & Dashboard

Projet data end-to-end simulant un environnement professionnel :
données multi-sources, modélisation en étoile, transformations SQL et dashboard interactif.

## Stack technique

| Outil | Rôle |
|---|---|
| Python + Faker | Génération des données synthétiques |
| DuckDB | Data Warehouse local (RAW → Staging → Marts) |
| Pandas | Manipulation et export des données |
| Streamlit | Dashboard interactif |
| Plotly | Visualisations |

## Architecture

```
Sources CSV (Faker)
      │
      ▼
┌─────────────────────────────────────────┐
│              DuckDB                     │
│                                         │
│  RAW        →   STAGING    →   MARTS   │
│  raw_orders     stg_orders   fact_orders│
│  raw_products   stg_products dim_products│
│  raw_customers  stg_customers dim_customers│
│  raw_returns    stg_returns  dim_date   │
└─────────────────────────────────────────┘
      │
      ▼
Dashboard Streamlit (4 pages)
```

## Structure du projet

```
ecommerce_analytics/
├── config.py                  ← chemins et paramètres centralisés
├── requirements.txt
├── data/
│   ├── raw/                   ← CSV sources générés par Faker
│   ├── warehouse/             ← base DuckDB
│   └── reports/               ← résultats des analyses SQL
├── scripts/
│   ├── generate_data.py       ← génération des données
│   ├── build_warehouse.py     ← construction du warehouse
│   └── run_analyses.py        ← analyses SQL métier
├── sql/
│   ├── raw/                   ← chargement CSV → DuckDB
│   ├── staging/               ← nettoyage et dédoublonnage
│   ├── marts/                 ← schéma en étoile
│   └── analyses/              ← requêtes métier
└── dashboard/
    └── app.py                 ← dashboard Streamlit
```

## Lancer le projet

### 1. Installer les dépendances
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Générer les données
python scripts/generate_data.py

### 3. Construire le warehouse
python scripts/build_warehouse.py

### 4. Lancer les analyses
python scripts/run_analyses.py

### 5. Lancer le dashboard
streamlit run dashboard/app.py

## Données générées

| Source | Volume | Anomalies injectées |
|---|---|---|
| customers.csv | 1 000 clients | nulls email/ville, doublons |
| products.csv | 200 produits | nulls stock |
| orders.csv | 5 000 commandes | dates mixtes, nulls discount, doublons |
| returns.csv | 300 retours | nulls raison |

## Analyses disponibles

- CA mensuel avec croissance MoM (month-over-month)
- Top 10 produits par revenus et taux de retour
- Segmentation clients : Nouveau / Occasionnel / Fidèle
- Taux de retour par catégorie produit