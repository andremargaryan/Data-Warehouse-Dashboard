"""
run_analyses.py — Exécute les analyses SQL et sauvegarde les résultats en CSV
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import duckdb
import pandas as pd
from config import DB_PATH, SQL_ANALYSES, REPORTS_DIR

def run_analysis(con, filepath: Path, output_name: str, label: str):
    print(f"  ▶ {label}")
    sql = filepath.read_text()
    df  = con.execute(sql).df()
    out = REPORTS_DIR / output_name
    df.to_csv(out, index=False)
    print(f"    → {len(df)} lignes sauvegardées dans {output_name}")
    return df

if __name__ == "__main__":
    print("Lancement des analyses\n")
    con = duckdb.connect(str(DB_PATH))

    run_analysis(con, SQL_ANALYSES / "ca_mensuel.sql",
                 "ca_mensuel.csv",        "CA mensuel & croissance MoM")

    run_analysis(con, SQL_ANALYSES / "top_produits.sql",
                 "top_produits.csv",      "Top 10 produits")

    run_analysis(con, SQL_ANALYSES / "taux_retour.sql",
                 "taux_retour.csv",       "Taux de retour par catégorie")

    run_analysis(con, SQL_ANALYSES / "segmentation_clients.sql",
                 "segmentation_clients.csv", "Segmentation clients")

    con.close()