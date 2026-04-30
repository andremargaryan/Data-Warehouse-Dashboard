"""
app.py — Dashboard Streamlit : Analyse des ventes e-commerce
4 pages : Vue globale / Évolution / Produits / Clients
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import duckdb
from config import DB_PATH

# Config page
st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📦",
    layout="wide",
)

# Connexion DuckDB
@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)

@st.cache_data
def query(sql: str) -> pd.DataFrame:
    con = get_connection()
    return con.execute(sql).df()

# Chargement des données
@st.cache_data
def load_data():
    ca_mensuel = query("""
        SELECT d.year_month, d.year, d.month,
               ROUND(SUM(f.amount), 2)      AS ca,
               COUNT(DISTINCT f.order_id)   AS nb_commandes,
               ROUND(AVG(f.amount), 2)      AS panier_moyen
        FROM fact_orders f
        JOIN dim_date d ON f.date_id = d.date_id
        WHERE f.status = 'completed'
        GROUP BY d.year_month, d.year, d.month
        ORDER BY d.year, d.month
    """)

    top_produits = query("""
        SELECT p.product_name, p.category,
               ROUND(SUM(f.amount), 2)      AS revenu_total,
               SUM(f.quantity)              AS quantite_vendue,
               ROUND(p.price, 2)            AS prix,
               ROUND(SUM(f.margin_amount),2) AS marge_totale,
               SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END) * 100.0
                   / NULLIF(COUNT(*), 0)    AS taux_retour
        FROM fact_orders f
        JOIN dim_products p ON f.product_id = p.product_id
        WHERE f.status = 'completed'
        GROUP BY p.product_name, p.category, p.price
        ORDER BY revenu_total DESC
        LIMIT 10
    """)

    taux_retour = query("""
        SELECT p.category,
               COUNT(DISTINCT f.order_id)   AS nb_commandes,
               SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END) AS nb_retours,
               ROUND(SUM(CASE WHEN f.is_returned THEN 1 ELSE 0 END)
                   * 100.0 / NULLIF(COUNT(*), 0), 2) AS taux_retour_pct
        FROM fact_orders f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY p.category
        ORDER BY taux_retour_pct DESC
    """)

    segmentation = query("""
        WITH cpc AS (
            SELECT customer_id,
                   COUNT(DISTINCT order_id) AS nb_commandes,
                   ROUND(SUM(amount), 2)    AS ca_total,
                   ROUND(AVG(amount), 2)    AS panier_moyen
            FROM fact_orders
            WHERE status = 'completed'
            GROUP BY customer_id
        )
        SELECT
            CASE WHEN nb_commandes = 1 THEN 'Nouveau'
                 WHEN nb_commandes <= 3 THEN 'Occasionnel'
                 ELSE 'Fidèle' END          AS segment,
            COUNT(*)                        AS nb_clients,
            ROUND(AVG(panier_moyen), 2)     AS panier_moyen,
            ROUND(SUM(ca_total), 2)         AS ca_total
        FROM cpc
        GROUP BY segment
    """)

    commandes_jour = query("""
        SELECT DAYNAME(f.date_id)   AS jour,
               HOUR(f.date_id)      AS heure,
               COUNT(*)             AS nb_commandes
        FROM fact_orders f
        WHERE f.status = 'completed'
        GROUP BY jour, heure
        ORDER BY heure
    """)

    return ca_mensuel, top_produits, taux_retour, segmentation, commandes_jour

ca_mensuel, top_produits, taux_retour, segmentation, commandes_jour = load_data()

# Sidebar
st.sidebar.title("📦 E-commerce Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Vue globale", "Évolution", "Produits", "Clients"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtre période**")

all_months   = ca_mensuel["year_month"].tolist()
min_i, max_i = 0, len(all_months) - 1

periode = st.sidebar.select_slider(
    "Sélectionner la période",
    options=all_months,
    value=(all_months[min_i], all_months[max_i])
)

# Filtre appliqué sur ca_mensuel
mask = (ca_mensuel["year_month"] >= periode[0]) & \
       (ca_mensuel["year_month"] <= periode[1])
df_periode = ca_mensuel[mask]

st.sidebar.markdown("---")
st.sidebar.caption("Data Warehouse · DuckDB + Streamlit")

# PAGE 1 — Vue globale
if page == "Vue globale":
    st.title("Vue globale")
    st.markdown(f"Période : **{periode[0]}** → **{periode[1]}**")
    st.markdown("---")

    ca_total      = df_periode["ca"].sum()
    nb_commandes  = df_periode["nb_commandes"].sum()
    panier_moyen  = df_periode["ca"].sum() / df_periode["nb_commandes"].sum() if nb_commandes > 0 else 0
    nb_retours    = query("""
        SELECT COUNT(*) AS n FROM fact_orders WHERE is_returned = true
    """)["n"][0]
    taux_retour_global = round(nb_retours / nb_commandes * 100, 2) if nb_commandes > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CA Total",       f"{ca_total:,.0f} €")
    col2.metric("Commandes",      f"{nb_commandes:,}")
    col3.metric("Panier moyen",   f"{panier_moyen:,.2f} €")
    col4.metric("Taux de retour", f"{taux_retour_global} %")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("CA mensuel")
        fig = px.bar(
            df_periode, x="year_month", y="ca",
            color_discrete_sequence=["#4F8EF7"],
            labels={"year_month": "Mois", "ca": "CA (€)"}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("Taux de retour par catégorie")
        fig2 = px.bar(
            taux_retour, x="taux_retour_pct", y="category",
            orientation="h",
            color="taux_retour_pct",
            color_continuous_scale="Reds",
            labels={"taux_retour_pct": "Taux (%)", "category": "Catégorie"}
        )
        st.plotly_chart(fig2, use_container_width=True)

# ─── PAGE 2 — Évolution ───────────────────────────────────────────────────────
elif page == "Évolution":
    st.title("Évolution du CA")
    st.markdown(f"Période : **{periode[0]}** → **{periode[1]}**")
    st.markdown("---")

    fig = px.line(
        df_periode, x="year_month", y="ca",
        markers=True,
        color_discrete_sequence=["#4F8EF7"],
        labels={"year_month": "Mois", "ca": "CA (€)"},
        title="Chiffre d'affaires mensuel"
    )
    fig.update_traces(line_width=3)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nombre de commandes")
        fig2 = px.bar(
            df_periode, x="year_month", y="nb_commandes",
            color_discrete_sequence=["#F7A74F"],
            labels={"year_month": "Mois", "nb_commandes": "Commandes"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Panier moyen")
        fig3 = px.line(
            df_periode, x="year_month", y="panier_moyen",
            markers=True,
            color_discrete_sequence=["#4FD7A7"],
            labels={"year_month": "Mois", "panier_moyen": "Panier moyen (€)"}
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Données détaillées")
    st.dataframe(df_periode, use_container_width=True)

# PAGE 3 — Produits
elif page == "Produits":
    st.title("Analyse Produits")
    st.markdown("---")

    st.subheader("Top 10 produits par revenu")
    fig = px.bar(
        top_produits.sort_values("revenu_total"),
        x="revenu_total", y="product_name",
        orientation="h",
        color="category",
        labels={"revenu_total": "Revenu (€)", "product_name": "Produit"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prix vs Volume vendu")
        fig2 = px.scatter(
            top_produits,
            x="prix", y="quantite_vendue",
            size="revenu_total",
            color="category",
            hover_name="product_name",
            labels={"prix": "Prix unitaire (€)", "quantite_vendue": "Quantité vendue"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Taux de retour par catégorie")
        fig3 = px.bar(
            taux_retour,
            x="category", y="taux_retour_pct",
            color="taux_retour_pct",
            color_continuous_scale="Reds",
            labels={"taux_retour_pct": "Taux (%)", "category": "Catégorie"}
        )
        fig3.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig3, use_container_width=True)

# PAGE 4 — Clients
elif page == "Clients":
    st.title("Analyse Clients")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Segments clients")
        fig = px.pie(
            segmentation,
            names="segment", values="nb_clients",
            hole=0.4,
            color_discrete_sequence=["#4F8EF7", "#F7A74F", "#4FD7A7"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Panier moyen par segment")
        fig2 = px.bar(
            segmentation,
            x="segment", y="panier_moyen",
            color="segment",
            color_discrete_sequence=["#4F8EF7", "#F7A74F", "#4FD7A7"],
            labels={"panier_moyen": "Panier moyen (€)", "segment": "Segment"}
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Récapitulatif par segment")
    st.dataframe(segmentation, use_container_width=True)