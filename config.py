from pathlib import Path

ROOT_DIR      = Path(__file__).parent.resolve()

DATA_DIR      = ROOT_DIR / "data"
RAW_DIR       = DATA_DIR / "raw"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
REPORTS_DIR   = DATA_DIR / "reports"

SQL_DIR       = ROOT_DIR / "sql"
SQL_RAW       = SQL_DIR / "raw"
SQL_STAGING   = SQL_DIR / "staging"
SQL_MARTS     = SQL_DIR / "marts"
SQL_ANALYSES  = SQL_DIR / "analyses"

ORDERS_CSV    = RAW_DIR / "orders.csv"
PRODUCTS_CSV  = RAW_DIR / "products.csv"
CUSTOMERS_CSV = RAW_DIR / "customers.csv"
RETURNS_CSV   = RAW_DIR / "returns.csv"

DB_PATH = WAREHOUSE_DIR / "ecommerce.duckdb"

DATA_GEN = {
    "n_orders":    5000,
    "n_products":   200,
    "n_customers": 1000,
    "n_returns":    300,
    "start_date":  "2023-01-01",
    "end_date":    "2024-12-31",
    "seed":        42,
}

PRODUCT_CATEGORIES = [
    "Électronique", "Mode & Vêtements", "Maison & Jardin",
    "Sports & Loisirs", "Beauté & Santé", "Alimentation",
    "Jouets & Jeux", "Livres & Médias",
]

CATEGORY_MARGINS = {
    "Électronique": 0.15, "Mode & Vêtements": 0.45,
    "Maison & Jardin": 0.35, "Sports & Loisirs": 0.30,
    "Beauté & Santé": 0.50, "Alimentation": 0.20,
    "Jouets & Jeux": 0.40, "Livres & Médias": 0.25,
}

ANOMALY_RATES = {
    "null_rate":      0.03,
    "duplicate_rate": 0.02,
    "bad_date_rate":  0.05,
}

for _dir in [RAW_DIR, WAREHOUSE_DIR, REPORTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)