from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Pybotx():
    """Pybotx crew - Python Agent that writes and runs Python code"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def code_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_engineer'], # type: ignore[index]
            verbose=True,
            allow_code_execution=True,  # Allows the agent to execute Python code
            code_execution_mode="safe",
            max_code_execution_time=30,  # Maximum time in seconds for code execution
            max_retry_limit=3,  # Maximum number of retries for code execution
        )

    @task
    def develop_python_solution(self) -> Task:
        return Task(
            config=self.tasks_config['develop_python_solution'], # type: ignore[index]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Pybotx crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
