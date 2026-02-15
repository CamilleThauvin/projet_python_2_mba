"""Interface Streamlit pour visualiser les données de transactions bancaires."""

import os
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Banking Transactions Dashboard",
    page_icon="💳",
    layout="wide"
)

# Title
st.title("💳 Banking Transactions Analytics Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Choisir une page",
    ["📊 Vue d'ensemble", "💰 Transactions", "👥 Clients", "🚨 Fraude", "📈 Statistiques"]
)

def fetch_data(endpoint):
    """Récupère les données depuis l'API."""
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données: {e}")
        return None

# Page: Vue d'ensemble
if page == "📊 Vue d'ensemble":
    st.header("Vue d'ensemble du système")

    col1, col2, col3, col4 = st.columns(4)

    # Récupérer les stats
    stats = fetch_data("/api/stats/overview")
    if stats:
        with col1:
            st.metric("Total Transactions", f"{stats.get('total_transactions', 0):,}")
        with col2:
            st.metric("Montant Moyen", f"${stats.get('avg_amount', 0):.2f}")
        with col3:
            st.metric("Taux de Fraude", f"{stats.get('fraud_rate', 0)*100:.2f}%")
        with col4:
            st.metric("Type Principal", stats.get('most_common_type', 'N/A'))

    # Stats par type
    st.subheader("Répartition par type de transaction")
    stats_by_type = fetch_data("/api/stats/by-type")
    if stats_by_type:
        df_types = pd.DataFrame(stats_by_type)
        fig = px.pie(df_types, values='count', names='type',
                     title='Distribution des types de transactions')
        st.plotly_chart(fig, use_container_width=True)

# Page: Transactions
elif page == "💰 Transactions":
    st.header("Transactions récentes")

    limit = st.slider("Nombre de transactions à afficher", 10, 100, 20)
    transactions = fetch_data(f"/api/transactions/recent?limit={limit}")

    if transactions and 'transactions' in transactions:
        df = pd.DataFrame(transactions['transactions'])
        st.dataframe(df, use_container_width=True)

        # Distribution des montants
        st.subheader("Distribution des montants")
        fig = px.histogram(df, x='amount', nbins=50,
                          title='Distribution des montants de transaction')
        st.plotly_chart(fig, use_container_width=True)

# Page: Clients
elif page == "👥 Clients":
    st.header("Analyse des clients")

    # Top clients
    st.subheader("Top 10 Clients par nombre de transactions")
    top_customers = fetch_data("/api/customers/top?limit=10")

    if top_customers:
        df_customers = pd.DataFrame(top_customers)
        fig = px.bar(df_customers, x='customer_id', y='transaction_count',
                     title='Top 10 Clients',
                     labels={'customer_id': 'Client ID',
                            'transaction_count': 'Nombre de transactions'})
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_customers, use_container_width=True)

# Page: Fraude
elif page == "🚨 Fraude":
    st.header("Détection de fraude")

    fraud_summary = fetch_data("/api/fraud/summary")
    if fraud_summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Fraudes", fraud_summary.get('total_frauds', 0))
        with col2:
            st.metric("Détectées", fraud_summary.get('flagged', 0))
        with col3:
            st.metric("Précision", f"{fraud_summary.get('precision', 0)*100:.1f}%")
        with col4:
            st.metric("Rappel", f"{fraud_summary.get('recall', 0)*100:.1f}%")

    # Fraude par type
    st.subheader("Taux de fraude par type de transaction")
    fraud_by_type = fetch_data("/api/fraud/by-type")
    if fraud_by_type:
        df_fraud = pd.DataFrame(fraud_by_type)
        fig = px.bar(df_fraud, x='type', y='fraud_rate',
                     title='Taux de fraude par type',
                     labels={'type': 'Type', 'fraud_rate': 'Taux de fraude'})
        st.plotly_chart(fig, use_container_width=True)

# Page: Statistiques
elif page == "📈 Statistiques":
    st.header("Statistiques détaillées")

    # Évolution quotidienne
    st.subheader("Évolution quotidienne des transactions")
    days = st.slider("Nombre de jours", 7, 30, 14)
    daily_stats = fetch_data(f"/api/stats/daily?days={days}")

    if daily_stats:
        df_daily = pd.DataFrame(daily_stats)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_daily['day'], y=df_daily['count'],
                                mode='lines+markers', name='Nombre'))
        fig.add_trace(go.Scatter(x=df_daily['day'], y=df_daily['avg_amount'],
                                mode='lines+markers', name='Montant moyen',
                                yaxis='y2'))
        fig.update_layout(
            title='Évolution quotidienne',
            yaxis=dict(title='Nombre de transactions'),
            yaxis2=dict(title='Montant moyen', overlaying='y', side='right')
        )
        st.plotly_chart(fig, use_container_width=True)

    # Distribution des montants
    st.subheader("Distribution des montants")
    amount_dist = fetch_data("/api/stats/amount-distribution")
    if amount_dist:
        fig = px.bar(x=amount_dist['bins'], y=amount_dist['counts'],
                     title='Distribution des montants de transaction',
                     labels={'x': 'Tranche de montant', 'y': 'Nombre'})
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Banking Transactions Analytics Dashboard - Projet Python MBA*")
