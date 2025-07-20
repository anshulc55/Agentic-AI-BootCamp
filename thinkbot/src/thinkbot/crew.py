from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Thinkbot():
    """Thinkbot crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def argubot(self) -> Agent:
        return Agent(
            config=self.agents_config['argubot'], # type: ignore[index]
            verbose=True
        )

    @agent
    def verdictobot(self) -> Agent:
        return Agent(
            config=self.agents_config['verdictobot'], # type: ignore[index]
            verbose=True
        )


    @task
    def make_case(self) -> Task:
        return Task(
            config=self.tasks_config['make_case'], # type: ignore[index]
            output_file='output/make_case.md'
        )

    @task
    def break_case(self) -> Task:
        return Task(
            config=self.tasks_config['break_case'], # type: ignore[index]
            output_file='output/break_case.md'
        )
    
    @task
    def render_verdict(self) -> Task:
        return Task(
            config=self.tasks_config['render_verdict'], # type: ignore[index]
            output_file='output/render_verdict.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Thinkbot crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            )
