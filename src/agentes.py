from crewai import Agent, LLM
from src.ferramentas import ler_dados, calcular_kpis, verificar_qualidade

LLM = LLM(model="ollama/mistral", base_url="http://localhost:11434")

IDIOMA = (
    " IMPORTANTE: Você DEVE responder SEMPRE em português brasileiro. "
    "Nunca responda em inglês. Use linguagem formal e profissional."
)


explorador = Agent(
    role="Explorador de Dados",
    goal="Perfilar o dataset de vendas identificando estrutura, tipos de dados e características gerais." + IDIOMA,
    backstory=(
        "Você é um especialista brasileiro em data profiling com anos de experiência "
        "em entender datasets novos rapidamente e produzir análises claras e detalhadas."
    ),
    tools=[ler_dados],
    llm=LLM,
    verbose=True,
)

estatistico = Agent(
    role="Analista Estatístico",
    goal="Calcular distribuições, médias, desvios padrão e tendências nos dados de vendas." + IDIOMA,
    backstory=(
        "Você é um estatístico brasileiro com profundo conhecimento em análise descritiva "
        "e identificação de padrões em dados comerciais."
    ),
    tools=[ler_dados],
    llm=LLM,
    verbose=True,
)

analista_negocio = Agent(
    role="Analista de Negócios",
    goal=(
        "Interpretar os números em linguagem de negócio, identificar KPIs "
        "e comparar a performance entre vendedores e regiões." + IDIOMA
    ),
    backstory=(
        "Você é um analista de negócios sênior brasileiro com experiência em varejo "
        "e análise de performance comercial."
    ),
    tools=[calcular_kpis],
    llm=LLM,
    verbose=True,
)

analista_insights = Agent(
    role="Analista de Insights Estratégicos",
    goal=(
        "Cruzar todas as análises anteriores e identificar os 3 insights "
        "mais relevantes para o negócio." + IDIOMA
    ),
    backstory=(
        "Você é um cientista de dados sênior brasileiro especializado em "
        "transformar dados em decisões estratégicas de alto impacto."
    ),
    tools=[ler_dados, calcular_kpis],
    llm=LLM,
    verbose=True,
)

auditor_qualidade = Agent(
    role="Auditor de Qualidade de Dados",
    goal="Detectar anomalias, inconsistências e problemas de qualidade nos dados." + IDIOMA,
    backstory=(
        "Você é um engenheiro de dados brasileiro especializado em qualidade "
        "e governança de dados, com foco em integridade e confiabilidade."
    ),
    tools=[verificar_qualidade, ler_dados],
    llm=LLM,
    verbose=True,
)

visualizador = Agent(
    role="Engenheiro de Visualização",
    goal=(
        "Descrever em detalhes como seria o dashboard ideal para os dados "
        "de vendas analisados, com KPIs, gráficos e filtros." + IDIOMA
    ),
    backstory=(
        "Você é um engenheiro brasileiro especializado em visualização de dados "
        "e desenvolvimento de dashboards profissionais com Streamlit e Plotly."
    ),
    tools=[calcular_kpis],
    llm=LLM,
    verbose=True,
)

redator = Agent(
    role="Redator Executivo",
    goal=(
        "Sintetizar todas as análises em um relatório executivo profissional e completo. "
        "NUNCA use placeholders como [valor], sempre use os dados reais das ferramentas." + IDIOMA
    ),
    backstory=(
        "Você é um consultor sênior brasileiro especializado em transformar análises técnicas "
        "em relatórios executivos claros e acionáveis. "
        "Você sempre consulta os dados reais antes de escrever qualquer número."
    ),
    tools=[calcular_kpis, ler_dados],
    llm=LLM,
    verbose=True,
)
