import streamlit as st
from src.equipe import executar
from pathlib import Path

st.set_page_config(
    page_title="Multi-Agent Analytics",
    page_icon="🤖",
    layout="wide"
)

st.title("Multi-Agent Analytics Pipeline")
st.markdown("7 agentes especializados com CrewAI analisam o pipeline de vendas em sequencia.")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Agentes da equipe")
    agentes = [
        ("Explorador de Dados", "Perfila o dataset e identifica estrutura"),
        ("Analista Estatistico", "Calcula distribuicoes e tendencias"),
        ("Analista de Negocios", "Interpreta KPIs e performance comercial"),
        ("Analista de Insights", "Identifica os 3 insights estrategicos"),
        ("Auditor de Qualidade", "Detecta anomalias e problemas nos dados"),
        ("Engenheiro de Visualizacao", "Gera o dashboard interativo"),
        ("Redator Executivo", "Sintetiza tudo no relatorio final"),
    ]
    for nome, descricao in agentes:
        st.markdown(f"**{nome}** - {descricao}")

with col2:
    st.markdown("### Pipeline de dados")
    st.code("etl_airflow -> DuckDB -> 7 agentes -> relatorio.docx")

st.divider()

if st.button("Executar analise completa", type="primary", use_container_width=True):
    with st.spinner("Agentes trabalhando... isso pode levar alguns minutos."):
        try:
            resultado = executar()
            st.success("Analise concluida!")

            st.markdown("### Resultado final")
            st.markdown(resultado)

            relatorio = Path("relatorios/relatorio.docx")
            if relatorio.exists():
                with open(relatorio, "rb") as f:
                    st.download_button(
                        label="Baixar relatorio DOCX",
                        data=f,
                        file_name="relatorio_vendas.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

            dashboard = Path("dashboard/dashboard.py")
            if dashboard.exists():
                st.info("Dashboard gerado. Para visualizar rode: streamlit run dashboard/dashboard.py")

        except Exception as e:
            st.error(f"Erro: {e}")

