## Executes each planned search using WebSearchTool

# Import Dependency Libs
from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings


# Agent Instructions: Clear and Direct
RESEARCH_PROMPT = (
    "You are a highly efficient research assistant. "
    "Given a topic, perform a thorough web search and return a well-organized, factual summary "
    "in under 500 words. Summarize clearly, capture core insights, and omit fluff. "
    "No personal opinions or commentary. This is for someone writing a report."
)


# Initialize Web Search Agent
web_search_agent = Agent(
    name="WebSearchAgent",
    instructions=RESEARCH_PROMPT,
    tools=[WebSearchTool(search_context_size='low')],
    model="gpt-4.1-mini",
    model_settings=ModelSettings(tool_choice="required")
)