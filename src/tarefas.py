from crewai import Task
from src.agentes import (
    explorador, estatistico, analista_negocio,
    analista_insights, auditor_qualidade, visualizador, redator
)


tarefa_explorar = Task(
    description=(
        "Use a ferramenta 'Ler dados do banco' e analise o dataset de vendas. "
        "Identifique: número de registros, colunas disponíveis, tipos de dados, "
        "intervalo de datas, produtos únicos, vendedores e regiões presentes. "
        "Responda em português brasileiro."
    ),
    expected_output="Perfil completo do dataset com estrutura, dimensões e características gerais, em português.",
    agent=explorador,
)

tarefa_estatistica = Task(
    description=(
        "Use a ferramenta 'Ler dados do banco' e calcule estatísticas descritivas. "
        "Analise: distribuição de receita e lucro, média e desvio padrão por produto, "
        "tendência de vendas ao longo do tempo, produtos mais e menos vendidos. "
        "Responda em português brasileiro."
    ),
    expected_output="Relatório estatístico com distribuições, médias, desvios e tendências temporais, em português.",
    agent=estatistico,
)

tarefa_negocio = Task(
    description=(
        "Use a ferramenta 'Calcular KPIs de vendas' e interprete os resultados. "
        "Identifique: melhor e pior vendedor por margem e receita, região mais lucrativa, "
        "produtos com melhor ROI e oportunidades de melhoria. "
        "Responda em português brasileiro."
    ),
    expected_output="Análise de negócio com KPIs, ranking de vendedores e regiões, em português.",
    agent=analista_negocio,
)

tarefa_insights = Task(
    description=(
        "Com base nas análises anteriores, identifique os 3 insights mais importantes. "
        "Cada insight deve ter: título, descrição, impacto no negócio e ação recomendada. "
        "Responda em português brasileiro."
    ),
    expected_output="Lista dos 3 principais insights estratégicos com ações recomendadas, em português.",
    agent=analista_insights,
)

tarefa_qualidade = Task(
    description=(
        "Use as ferramentas disponíveis para auditar a qualidade dos dados. "
        "Verifique: registros nulos removidos, anomalias estatísticas, "
        "consistência entre receita e custo, integridade geral dos dados. "
        "Responda em português brasileiro."
    ),
    expected_output="Relatório de auditoria com score de qualidade e anomalias encontradas, em português.",
    agent=auditor_qualidade,
)

tarefa_dashboard = Task(
    description=(
        "Use a ferramenta 'Calcular KPIs de vendas' e descreva em detalhes "
        "como seria o dashboard ideal para os dados analisados. "
        "Descreva: KPI cards, tipos de gráficos, filtros e insights visuais. "
        "Responda em português brasileiro."
    ),
    expected_output="Descrição detalhada do dashboard ideal com justificativa de cada elemento visual, em português.",
    agent=visualizador,
)

tarefa_relatorio = Task(
    description=(
        "Use a ferramenta 'Calcular KPIs de vendas' para obter os números reais. "
        "Depois sintetize todas as análises anteriores em um relatório executivo completo. "
        "IMPORTANTE: Use APENAS números reais das ferramentas. NUNCA escreva placeholders como [valor] ou [x%]. "
        "Estrutura obrigatória: Resumo Executivo, Perfil dos Dados, Análise Estatística, "
        "KPIs e Performance, Insights Estratégicos, Qualidade dos Dados, Conclusão e Próximos Passos. "
        "Responda em português brasileiro."
    ),
    expected_output="Relatório executivo completo com números reais, sem placeholders, em português brasileiro.",
    agent=redator,
)
