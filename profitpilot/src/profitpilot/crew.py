from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_notification import MyCustomPushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage

class CompanyInNews(BaseModel):
    """Company appearing in financial news"""
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Why the company is trending in news")

class CompanyNewsList(BaseModel):
    """List of trending companies in the news"""
    companies: List[CompanyInNews] = Field(description="List of trending companies")

class CompanyResearchReport(BaseModel):
    """Comprehensive financial research on a company"""
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market positioning and competition")
    future_outlook: str = Field(description="Future prospects and growth opportunities")
    investment_potential: str = Field(description="Summary of investment attractiveness")

class CompanyResearchReportList(BaseModel):
    """Collection of research reports for trending companies"""
    research_list: List[CompanyResearchReport] = Field(description="Detailed research on all companies")


@CrewBase
class Profitpilot():
    """Multi-Agent CrewAI Project for Discovering and Selecting Stock Opportunities"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def market_trend_tracker(self) -> Agent:
        return Agent(
            config=self.agents_config['market_trend_tracker'],
            verbose=True,
            tools=[SerperDevTool()],
            memory=True,  # Enable memory for the market trend tracker agent
        )

    @agent
    def deep_dive_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['deep_dive_researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )
    
    @agent
    def equity_selector(self) -> Agent:
        return Agent(
            config=self.agents_config['equity_selector'], # type: ignore[index]
            verbose=True,
            tools=[MyCustomPushNotificationTool()], # Custom tool to send notifications
            memory=True, # Enable memory for the equity selector agent
        )

    @task
    def identify_market_movers(self) -> Task:
        return Task(
            config=self.tasks_config['identify_market_movers'], # type: ignore[index]
            output_pydantic=CompanyNewsList,
        )

    @task
    def analyze_company_fundamentals(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_company_fundamentals'], # type: ignore[index]
            output_pydantic=CompanyResearchReportList,
        )
    
    @task
    def select_top_equity_pick(self) -> Task:
        return Task(
            config=self.tasks_config['select_top_equity_pick'], # type: ignore[index]
        
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Profitpilot crew"""

        manager = Agent(
            config=self.agents_config['investment_manager'],
            allow_delegation=True
        )

        # Long-Term Memory (Persistent across sessions)
        long_term_memory = LongTermMemory(
            storage = LTMSQLiteStorage(
                db_path="./memory/long_term.db", # SQLite database file for long-term memory
            )
        )

        # Short-Term Memory (Session-based)
        short_term_memory = ShortTermMemory(
            storage = RAGStorage(
                embedder_config = {
                    "provider": "openai", # Embedding provider for RAG
                    "config" :{
                        "model": "text-embedding-3-small", # Embedding model for RAG
                        "chunk_size": 512, # Size of text chunks for RAG
                    }
                },
                type="short_term",
                path="./memory/embeddings/", # Directory for storing RAG embeddings
            )
        )

        # Entity Memory (Stores information about specific entities like companies)
        entity_memory = EntityMemory(
            storage = RAGStorage(
                embedder_config = {
                    "provider": "openai", # Embedding provider for RAG
                    "config" :{
                        "model": "text-embedding-3-small", # Embedding model for RAG
                        "chunk_size": 512, # Size of text chunks for RAG
                    }
                },
                type="entity",
                path="./memory/embeddings/entities/", # Directory for storing entity embeddings
            )
        )

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager, # The investment manager agent
            long_term_memory=long_term_memory, # Long-term memory for persistent knowledge
            short_term_memory=short_term_memory, # Short-term memory for session-specific data
            entity_memory=entity_memory, # Entity memory for detailed company information
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
