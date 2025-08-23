from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from crewai.memory import UserMemory
from pathlib import Path


@CrewBase
class Optionstrader():
    """Optionstrader crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def signal_master(self) -> Agent:
        return Agent(
            config=self.agents_config['signal_master'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def sentiment_scanner(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_scanner'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )
    
    @agent
    def option_chain_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['option_chain_strategist'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )
    

    @agent
    def trade_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['trade_writer'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def performance_logger(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_logger'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
        )
    
    @task
    def generate_signals(self) -> Task:
        return Task(
            config=self.tasks_config['generate_signals'], # type: ignore[index]
        )

    @task
    def scan_sentiment(self) -> Task:
        return Task(
            config=self.tasks_config['scan_sentiment'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def analyze_option_chain(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_option_chain'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def write_trade_idea(self) -> Task:
        return Task(
            config=self.tasks_config['write_trade_idea'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def log_trade(self) -> Task:
        return Task(
            config=self.tasks_config['log_trade'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def log_feedback(self) -> Task:
        return Task(
            config=self.tasks_config['log_feedback'], # type: ignore[index]
            output_file='report.md'
        )
    
    def create_memory(self, crew: Crew) -> UserMemory:
        memory_path = Path(__file__).parent.parent.parent / "memory.json"
        return UserMemory(
            config={"path": str(memory_path)}
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Optionstrader crew"""

        #memory = self.create_memory(self)

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            #memory=memory, # Use JSON-based memory for trade logging
        )
