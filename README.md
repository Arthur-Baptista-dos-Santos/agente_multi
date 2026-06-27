# Multi-Agent Analytics Pipeline

> Sistema multi-agente com CrewAI e Ollama que analisa dados de vendas com 7 agentes especializados, gera insights estratégicos e exibe resultados em um dashboard interativo com Streamlit e Plotly.

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3.13-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-red)
![Ollama](https://img.shields.io/badge/Ollama-mistral-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)
![DuckDB](https://img.shields.io/badge/DuckDB-1.5-yellow)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75)

---

## O que faz

Orquestra 7 agentes de IA especializados que trabalham em sequência para analisar um pipeline de vendas: cada agente tem um papel distinto, usa ferramentas reais para acessar o banco de dados e passa seu resultado para o próximo. O sistema encerra com um relatório executivo consolidado e um dashboard visual interativo.

---

## Arquitetura

```
Pipeline de Dados (etl_airflow - DuckDB)
    Equipe Multi-Agent (CrewAI - Process.sequential)
        1. Explorador de Dados        - perfila o dataset
        2. Analista Estatístico       - calcula distribuicoes e tendencias
        3. Analista de Negócios       - interpreta KPIs por vendedor e regiao
        4. Analista de Insights       - identifica os 3 insights estratégicos
        5. Auditor de Qualidade       - verifica nulos, anomalias e consistencia
        6. Engenheiro de Visualizacao - descreve o dashboard ideal
        7. Redator Executivo          - sintetiza tudo em relatorio executivo
    Interface Streamlit (http://localhost:8501)
    Dashboard Interativo (http://localhost:8502)
```

---

## Ferramentas dos agentes

| Ferramenta | O que faz |
|---|---|
| `Ler dados do banco` | Lê todas as vendas do DuckDB e retorna em CSV |
| `Calcular KPIs de vendas` | Calcula receita, lucro e margem por vendedor e região |
| `Verificar qualidade dos dados` | Conta nulos, registros removidos e inconsistências |

---

## Pré-requisitos

- Python 3.10+
- Ollama instalado com `mistral` disponível
- Pipeline [`etl_airflow`](https://github.com/Arthur-Baptista-dos-Santos/etl_airflow) executado ao menos uma vez

---

## Instalação

```bash
git clone https://github.com/Arthur-Baptista-dos-Santos/agente_multi.git
cd agente_multi

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Como usar

```bash
# Garanta que o Ollama está rodando com o modelo disponível
ollama pull mistral

# Suba o pipeline etl_airflow para gerar os dados
cd ../etl_airflow
docker compose up airflow-init
docker compose up webserver scheduler -d
# Acesse http://localhost:8080, ative e dispare a DAG pipeline_vendas
docker compose down

# Rode a interface principal (executa os 7 agentes)
cd ../agente_multi
streamlit run app.py

# Em outro terminal, rode o dashboard visual
streamlit run dashboard/dashboard.py --server.port 8502
```

---

## Estrutura

```
agente_multi/
├── src/
│   ├── ferramentas.py   # 3 ferramentas com @tool decorator (CrewAI)
│   ├── agentes.py       # 7 agentes especializados com roles e backstories
│   ├── tarefas.py       # 7 tarefas com descriptions e expected_outputs
│   └── equipe.py        # Crew com Process.sequential + funcao executar()
├── dashboard/
│   └── dashboard.py     # Dashboard Streamlit com Plotly (KPIs + 4 graficos)
├── relatorios/          # Relatórios gerados (gitignored)
├── app.py               # Interface Streamlit principal
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Conceitos aplicados

- **Multi-Agent System**: múltiplos agentes com papéis distintos colaborando em sequência
- **CrewAI**: framework de orquestração multi-agente com Agent, Task e Crew
- **Process.sequential**: cada agente recebe o output do anterior como contexto
- **@tool decorator**: transforma funções Python em ferramentas que o LLM pode chamar
- **Ollama**: inferência local de LLMs sem custo de API, privacidade total dos dados
- **DuckDB**: banco analítico embutido como fonte de verdade para todos os agentes
- **Streamlit + Plotly**: dashboard interativo com KPIs e gráficos em tempo real
