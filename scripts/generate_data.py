"""
generate_data.py — Génération des données synthétiques avec Faker
Simule 4 sources CSV : commandes, produits, clients, retours
avec anomalies volontaires (nulls, doublons, formats dates mixtes)
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from faker import Faker
from config import (
    ORDERS_CSV, PRODUCTS_CSV, CUSTOMERS_CSV, RETURNS_CSV,
    DATA_GEN, PRODUCT_CATEGORIES, CATEGORY_MARGINS, ANOMALY_RATES
)

fake = Faker("fr_FR")
Faker.seed(DATA_GEN["seed"])
np.random.seed(DATA_GEN["seed"])

def random_dates(start: str, end: str, n: int) -> list:
    start_ts = pd.Timestamp(start)
    end_ts   = pd.Timestamp(end)
    delta    = (end_ts - start_ts).days
    days     = np.random.randint(0, delta, n)
    return [start_ts + pd.Timedelta(days=int(d)) for d in days]

def inject_nulls(series: pd.Series, rate: float) -> pd.Series:
    """Remplace rate% des valeurs par NaN"""
    mask = np.random.random(len(series)) < rate
    series = series.copy().astype(object)
    series[mask] = np.nan
    return series

def mixed_date_format(dates: list, bad_rate: float) -> list:
    """Mélange 3 formats de dates pour simuler des sources hétérogènes"""
    result = []
    for d in dates:
        r = np.random.random()
        if r < bad_rate:
            result.append(d.strftime("%d/%m/%Y"))       # format FR
        elif r < bad_rate * 2:
            result.append(d.strftime("%m-%d-%Y"))       # format US
        else:
            result.append(d.strftime("%Y-%m-%d"))       # format ISO (normal)
    return result

# 1. Clients

def generate_customers(n: int) -> pd.DataFrame:
    print(f"  Génération de {n} clients...")
    records = []
    for i in range(n):
        records.append({
            "customer_id":  f"C{i+1:04d}",
            "first_name":   fake.first_name(),
            "last_name":    fake.last_name(),
            "email":        fake.email(),
            "city":         fake.city(),
            "country":      "France",
            "signup_date":  fake.date_between(start_date="-3y", end_date="-6m").strftime("%Y-%m-%d"),
            "age":          np.random.randint(18, 75),
        })
    df = pd.DataFrame(records)

    # Anomalies : nulls sur email et city
    df["email"] = inject_nulls(df["email"], ANOMALY_RATES["null_rate"])
    df["city"]  = inject_nulls(df["city"],  ANOMALY_RATES["null_rate"])

    # Doublons
    n_dupes = int(n * ANOMALY_RATES["duplicate_rate"])
    dupes   = df.sample(n_dupes, random_state=1)
    df      = pd.concat([df, dupes], ignore_index=True)

    print(f"    → {len(df)} lignes dont {n_dupes} doublons")
    return df

# 2. Produits

def generate_products(n: int) -> pd.DataFrame:
    print(f"  Génération de {n} produits...")
    records = []
    for i in range(n):
        category = np.random.choice(PRODUCT_CATEGORIES)
        price    = round(np.random.uniform(5, 500), 2)
        margin   = CATEGORY_MARGINS[category]
        cost     = round(price * (1 - margin), 2)
        records.append({
            "product_id":   f"P{i+1:03d}",
            "product_name": fake.catch_phrase(),
            "category":     category,
            "price":        price,
            "cost":         cost,
            "stock":        np.random.randint(0, 500),
        })
    df = pd.DataFrame(records)

    # Anomalies : nulls sur stock
    df["stock"] = inject_nulls(df["stock"], ANOMALY_RATES["null_rate"])

    print(f"    → {len(df)} lignes")
    return df

# 3. Commandes

def generate_orders(n: int, customer_ids: list, product_ids: list) -> pd.DataFrame:
    print(f"  Génération de {n} commandes...")
    dates    = random_dates(DATA_GEN["start_date"], DATA_GEN["end_date"], n)
    statuses = np.random.choice(
        ["completed", "pending", "cancelled", "refunded"],
        size=n,
        p=[0.75, 0.10, 0.08, 0.07]
    )
    records = []
    for i in range(n):
        qty      = np.random.randint(1, 6)
        price    = round(np.random.uniform(10, 500), 2)
        discount = round(np.random.uniform(0, 0.3), 2)
        records.append({
            "order_id":    f"O{i+1:05d}",
            "customer_id": np.random.choice(customer_ids),
            "product_id":  np.random.choice(product_ids),
            "order_date":  dates[i],
            "quantity":    qty,
            "unit_price":  price,
            "discount":    discount,
            "amount":      round(qty * price * (1 - discount), 2),
            "status":      statuses[i],
        })
    df = pd.DataFrame(records)

    # Anomalies : formats de dates mixtes
    df["order_date"] = mixed_date_format(df["order_date"].tolist(), ANOMALY_RATES["bad_date_rate"])

    # Anomalies : nulls sur discount
    df["discount"] = inject_nulls(df["discount"], ANOMALY_RATES["null_rate"])

    # Doublons
    n_dupes = int(n * ANOMALY_RATES["duplicate_rate"])
    dupes   = df.sample(n_dupes, random_state=2)
    df      = pd.concat([df, dupes], ignore_index=True)

    print(f"    → {len(df)} lignes dont {n_dupes} doublons")
    return df

# 4. Retours

def generate_returns(n: int, order_ids: list) -> pd.DataFrame:
    print(f"  Génération de {n} retours...")
    records = []
    sampled_orders = np.random.choice(order_ids, size=n, replace=False)
    reasons = [
        "Produit défectueux", "Ne correspond pas à la description",
        "Mauvaise taille", "Changement d'avis", "Livraison trop longue"
    ]
    for i, oid in enumerate(sampled_orders):
        records.append({
            "return_id":    f"R{i+1:04d}",
            "order_id":     oid,
            "return_date":  fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d"),
            "reason":       np.random.choice(reasons),
            "refund_amount": round(np.random.uniform(10, 400), 2),
        })
    df = pd.DataFrame(records)

    # Anomalies : nulls sur reason
    df["reason"] = inject_nulls(df["reason"], ANOMALY_RATES["null_rate"])

    print(f"    → {len(df)} lignes")
    return df

# Main

if __name__ == "__main__":

    customers = generate_customers(DATA_GEN["n_customers"])
    customers.to_csv(CUSTOMERS_CSV, index=False)
    print(f"Sauvegardé : {CUSTOMERS_CSV}\n")

    products = generate_products(DATA_GEN["n_products"])
    products.to_csv(PRODUCTS_CSV, index=False)
    print(f"Sauvegardé : {PRODUCTS_CSV}\n")

    orders = generate_orders(
        DATA_GEN["n_orders"],
        customers["customer_id"].tolist(),
        products["product_id"].tolist()
    )
    orders.to_csv(ORDERS_CSV, index=False)
    print(f"Sauvegardé : {ORDERS_CSV}\n")

    returns = generate_returns(
        DATA_GEN["n_returns"],
        orders["order_id"].tolist()
    )
    returns.to_csv(RETURNS_CSV, index=False)
    print(f"  Sauvegardé : {RETURNS_CSV}\n")

    print("Résumé des fichiers générés :")
    print(f"   customers.csv : {len(customers):>5} lignes")
    print(f"   products.csv  : {len(products):>5} lignes")
    print(f"   orders.csv    : {len(orders):>5} lignes")
    print(f"   returns.csv   : {len(returns):>5} lignes")