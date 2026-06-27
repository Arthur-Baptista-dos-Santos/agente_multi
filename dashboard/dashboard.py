import streamlit as st
import plotly.express as px
import duckdb
import pandas as pd
from pathlib import Path

CAMINHO_DB = Path("C:/PORTIFÓLIO/etl_airflow/saida/vendas.db")

st.set_page_config(page_title="Dashboard de Vendas", page_icon="📊", layout="wide")
st.title("Dashboard de Vendas")
st.markdown("Gerado pelo pipeline Multi-Agent com CrewAI + DuckDB")

if not CAMINHO_DB.exists():
    st.error("Banco DuckDB não encontrado. Execute o pipeline etl_airflow primeiro.")
    st.stop()

con = duckdb.connect(str(CAMINHO_DB), read_only=True)
df = con.execute("SELECT * FROM vendas").fetchdf()

por_vendedor = con.execute("""
    SELECT vendedor,
           COUNT(*) AS vendas,
           ROUND(SUM(receita), 2) AS receita,
           ROUND(SUM(lucro), 2) AS lucro,
           ROUND(AVG(margem_pct), 2) AS margem_media
    FROM vendas
    GROUP BY vendedor
    ORDER BY lucro DESC
""").fetchdf()

por_regiao = con.execute("""
    SELECT regiao,
           COUNT(*) AS vendas,
           ROUND(SUM(receita), 2) AS receita,
           ROUND(AVG(margem_pct), 2) AS margem_media
    FROM vendas
    GROUP BY regiao
    ORDER BY receita DESC
""").fetchdf()

por_produto = con.execute("""
    SELECT produto,
           COUNT(*) AS vendas,
           ROUND(SUM(receita), 2) AS receita,
           ROUND(SUM(lucro), 2) AS lucro,
           ROUND(AVG(margem_pct), 2) AS margem_media
    FROM vendas
    GROUP BY produto
    ORDER BY receita DESC
""").fetchdf()

con.close()

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total", f"R$ {df['receita'].sum():,.2f}")
col2.metric("Lucro Total", f"R$ {df['lucro'].sum():,.2f}")
col3.metric("Margem Média", f"{df['margem_pct'].mean():.2f}%")
col4.metric("Total de Vendas", f"{len(df)} registros")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    fig1 = px.bar(
        por_vendedor,
        x="vendedor",
        y="receita",
        color="margem_media",
        color_continuous_scale="Greens",
        title="Receita por Vendedor",
        labels={"receita": "Receita (R$)", "vendedor": "Vendedor", "margem_media": "Margem %"},
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    fig2 = px.pie(
        por_regiao,
        names="regiao",
        values="receita",
        title="Receita por Região",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig2, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    df["data"] = pd.to_datetime(df["data"])
    margem_tempo = df.groupby("data")["margem_pct"].mean().reset_index()
    fig3 = px.line(
        margem_tempo,
        x="data",
        y="margem_pct",
        title="Margem Média ao Longo do Tempo",
        labels={"margem_pct": "Margem (%)", "data": "Data"},
        markers=True,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    fig4 = px.bar(
        por_produto,
        x="produto",
        y="lucro",
        color="margem_media",
        color_continuous_scale="Blues",
        title="Lucro por Produto",
        labels={"lucro": "Lucro (R$)", "produto": "Produto", "margem_media": "Margem %"},
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("Dados Detalhados")
st.dataframe(df, use_container_width=True)
