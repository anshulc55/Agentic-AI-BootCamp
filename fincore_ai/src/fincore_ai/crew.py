from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool


@CrewBase
class FincoreAi():
    """FincoreAi crew : For financial research and market reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def financial_research_expert(self) -> Agent:
        """Creates the lead financial researcher agent"""
        return Agent(
            config=self.agents_config['financial_research_expert'], 
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def market_insight_analyst(self) -> Agent:
        """Creates the market analyst agent responsible for generating structured reports"""
        return Agent(
            config=self.agents_config['market_insight_analyst'], 
            verbose=True
        )


    @task
    def company_research_task(self) -> Task:
        """Task: Research the company's current state, history, news, and future outlook"""
        return Task(
            config=self.tasks_config['company_research_task'], 
        )

    @task
    def company_analysis_task(self) -> Task:
        """Task: Analyze the research and generate a polished market insights report"""
        return Task(
            config=self.tasks_config['company_analysis_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the full CrewAI setup with agents and tasks"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
