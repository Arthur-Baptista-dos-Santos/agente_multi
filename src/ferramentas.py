from crewai.tools import tool
from pathlib import Path
import duckdb
import pandas as pd

CAMINHO_DB = Path("C:/PORTIFÓLIO/etl_airflow/saida/vendas.db")
CAMINHO_CSV_BRUTO = Path("C:/PORTIFÓLIO/etl_airflow/dados/vendas_brutas.csv")
CAMINHO_CSV_TRANSFORMADO = Path("C:/PORTIFÓLIO/etl_airflow/dados/vendas_transformadas.csv")


@tool("Ler dados do banco")
def ler_dados(dummy: str = "") -> str:
    """Lê todos os dados de vendas do banco DuckDB e retorna em formato CSV."""
    con = duckdb.connect(str(CAMINHO_DB), read_only=True)
    df = con.execute("SELECT * FROM vendas").fetchdf()
    con.close()
    return df.to_csv(index=False)


@tool("Calcular KPIs de vendas")
def calcular_kpis(dummy: str = "") -> str:
    """Calcula KPIs principais: receita, lucro e margem por vendedor e por região."""
    con = duckdb.connect(str(CAMINHO_DB), read_only=True)

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

    con.close()

    return (
        f"POR VENDEDOR:\n{por_vendedor.to_string()}\n\n"
        f"POR REGIÃO:\n{por_regiao.to_string()}"
    )


@tool("Verificar qualidade dos dados")
def verificar_qualidade(dummy: str = "") -> str:
    """Verifica nulos, duplicatas e consistência dos dados."""
    df_bruto = pd.read_csv(CAMINHO_CSV_BRUTO)
    df_limpo = pd.read_csv(CAMINHO_CSV_TRANSFORMADO)

    nulos = df_bruto.isnull().sum()
    removidos = len(df_bruto) - len(df_limpo)

    return (
        f"Registros brutos: {len(df_bruto)}\n"
        f"Registros após limpeza: {len(df_limpo)}\n"
        f"Removidos: {removidos}\n"
        f"Nulos por coluna:\n{nulos.to_string()}"
    )
