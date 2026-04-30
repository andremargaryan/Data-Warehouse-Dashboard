"""
build_warehouse.py — Construction du Data Warehouse DuckDB
Charge les CSV → RAW → STAGING → MARTS (schéma en étoile)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import duckdb
from config import DB_PATH, SQL_RAW, SQL_STAGING, SQL_MARTS

def run_sql_file(con, filepath: Path, label: str):
    """Lit et exécute un fichier .sql"""
    print(f"  ▶ {label}")
    sql = filepath.read_text()
    con.execute(sql)
    print(f"OK")

if __name__ == "__main__":
    print(f"Construction du warehouse...\n")
    print(f"   DB : {DB_PATH}\n")

    con = duckdb.connect(str(DB_PATH))

    # Couche RAW
    print("Couche RAW — chargement des CSV")
    run_sql_file(con, SQL_RAW / "load_raw.sql",       "Chargement tables RAW")

    # Couche STAGING
    print("\n🧹 Couche STAGING — nettoyage")
    run_sql_file(con, SQL_STAGING / "stg_customers.sql",  "stg_customers")
    run_sql_file(con, SQL_STAGING / "stg_products.sql",   "stg_products")
    run_sql_file(con, SQL_STAGING / "stg_orders.sql",     "stg_orders")
    run_sql_file(con, SQL_STAGING / "stg_returns.sql",    "stg_returns")

    # Couche MARTS
    print("\nCouche MARTS — schéma en étoile")
    run_sql_file(con, SQL_MARTS / "dim_customers.sql",  "dim_customers")
    run_sql_file(con, SQL_MARTS / "dim_products.sql",   "dim_products")
    run_sql_file(con, SQL_MARTS / "dim_date.sql",       "dim_date")
    run_sql_file(con, SQL_MARTS / "fact_orders.sql",    "fact_orders")

    # Vérification
    print("\nVérification des tables créées :")
    tables = con.execute("SHOW TABLES").fetchall()
    for t in tables:
        count = con.execute(f"SELECT COUNT(*) FROM {t[0]}").fetchone()[0]
        print(f"   {t[0]:<25} {count:>6} lignes")

    con.close()