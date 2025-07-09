## Defines the agent responsible for converting a user query into meaningful search tasks.

from pydantic import BaseModel
from agents import Agent

# Define structured output for each search item
class SearchTask(BaseModel):
    reason: str  # Why this particular search matters
    query: str   # The actual web search string

# The full output schema from the planner
class SearchPlan(BaseModel):
    searches: list[SearchTask]  # A list of search instructions

# How many searches should the planner generate?
NUMBER_OF_SEARCHES=3

# Instructions: Well-formed prompt for planning
PLANNER_PROMPT = (
    f"You are a financial research planner. Given a user query, identify {NUMBER_OF_SEARCHES} distinct search terms "
    "that would help answer it comprehensively. For each search, include a short reason explaining its relevance."
)

# Agent to generate the structured search plan
search_planner_agent = Agent(
    name="SearchPlannerAgent",
    instructions=PLANNER_PROMPT,
    model="gpt-4.1-mini",
    output_type=SearchPlan  # Agent is expected to output a Pydantic structure
)