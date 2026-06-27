from crewai import Crew, Process
from src.agentes import (
    explorador, estatistico, analista_negocio,
    analista_insights, auditor_qualidade, visualizador, redator
)
from src.tarefas import (
    tarefa_explorar, tarefa_estatistica, tarefa_negocio,
    tarefa_insights, tarefa_qualidade, tarefa_dashboard, tarefa_relatorio
)


equipe = Crew(
    agents=[
        explorador,
        estatistico,
        analista_negocio,
        analista_insights,
        auditor_qualidade,
        visualizador,
        redator,
    ],
    tasks=[
        tarefa_explorar,
        tarefa_estatistica,
        tarefa_negocio,
        tarefa_insights,
        tarefa_qualidade,
        tarefa_dashboard,
        tarefa_relatorio,
    ],
    process=Process.sequential,
    verbose=True,
)


def executar() -> str:
    resultado = equipe.kickoff()
    return str(resultado)
