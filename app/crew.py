from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class OutputItem(BaseModel):
    title: str = Field(description="O título do item de saída")
    content: str = Field(description="O conteúdo do item de saída")
    keywords: List[str] = Field(description="Lista de palavras-chave associadas ao item")

@CrewBase
class AiLatestDevelopment():
    """AiLatestDevelopment crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def retrieve_news(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieve_news'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def website_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['website_scraper'],
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def summarizer_of_websites(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_of_websites'],
            verbose=True
        )

    @agent
    def text_seo_optmizer(self) -> Agent:
        return Agent(
            config=self.agents_config['text_seo_optmizer'],
            verbose=True
        )


####################################################################


    @task
    def retrieve_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_news_task']
        )

    @task
    def website_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['website_scrape_task']
        )

    @task
    def summarizer_of_websites_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarizer_of_websites_task']
        )
    
    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            output_json=OutputItem
        )


####################################################################

    @crew
    def crew(self) -> Crew:
        """Creates the AiLatestDevelopment crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
