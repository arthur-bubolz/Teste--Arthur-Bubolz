from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

#Carrega variáveis de ambiente (como chaves de API)
load_dotenv()

#Modelo de Saída (Pydantic) - JSON
class OutputItem(BaseModel):
    titulo: str = Field(description="O título final e otimizado do artigo.")
    conteudo: str = Field(description="O corpo completo do artigo, formatado para leitura.")
    palavras_chave: List[str] = Field(description="Lista de palavras-chave mais relevantes para SEO.")

#Definição da Crew
@CrewBase
class AiLatestDevelopment():
    
    #Tipagem dos atributos da CrewBase
    agents: List[BaseAgent]
    tasks: List[Task]

    # ------------------- AGENTES -------------------

    #Agente focado em buscar informações de sites relativas ao tema
    @agent
    def retrieve_news(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieve_news'],
            tools=[SerperDevTool()],
            verbose=True
        )

    #Agente especializado em aplicar scrapping no conteúdo complementar do website
    @agent
    def website_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['website_scraper'],
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )

    #Agente responsável por resumir e consolidar as informações encontradas no wikipedia e site externo
    @agent
    def summarizer_of_websites(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_of_websites'],
            verbose=True
        )

    #Agente final que reescreve o texto para SEO e gera a estrutura JSON final
    @agent
    def text_seo_optmizer(self) -> Agent:
        return Agent(
            config=self.agents_config['text_seo_optmizer'],
            verbose=True
        )


    # ------------------- TAREFAS -------------------

    #Tarefa: Pesquisar o tópico e os itens relativos mais recentes.
    @task
    def retrieve_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_news_task']
        )

    #Tarefa: Aplicar scrapping no conteúdo encontrado no site pelo agente anterior
    @task
    def website_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['website_scrape_task']
        )

    #Tarefa: Resumir e consolidar todo o texto coletado (Wikipedia + Raspagem)
    @task
    def summarizer_of_websites_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarizer_of_websites_task']
        )
    
    #Tarefa: Otimizar o conteúdo consolidado para SEO e gerar a saída estruturada
    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            output_json=OutputItem
        )

    # ------------------- CREW -------------------

    #Cria e retorna a crew principal com Agentes e Tarefas definidos
    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
