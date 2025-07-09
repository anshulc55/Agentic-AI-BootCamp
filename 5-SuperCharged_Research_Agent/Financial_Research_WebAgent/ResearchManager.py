## Orchestrates the async pipeline: plan → search → write → email.

import asyncio
from agents import Runner, gen_trace_id, trace
from searchPlanner import search_planner_agent, SearchTask, SearchPlan
from webSearchAgent import web_search_agent
from reportWriterAgent import writer_agent, ReportData
from emailAgent import email_agent


class ResearchManager:

    # First generate a reasoned plan before searching.
    async def search_planner(self, query: str):
        """Use planner_agent to generate a structured list of web searches for a given research query."""
        print("Planning for searches...")
        result = await Runner.run(search_planner_agent, query)
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output
    
    # Function to Perform WebSearch : OpenAI WebSearch Tool
    async def web_search(self, search_task: SearchTask):
        """Run a single web search using the search_agent for a given query and reason."""
        input = f"Search term: {search_task.query}\nReason for searching: {search_task.reason}"
        result = await Runner.run(web_search_agent, input)
        return result.final_output
    
    # Running web_search in parallel
    async def perform_parallel_searches(self, search_plan: SearchPlan):
        """Perform web searches in parallel using asyncio to speed up data collection."""
        print("Perform Parallel Searching...")
        tasks = [asyncio.create_task(self.web_search(task)) for task in search_plan.searches]
        results = await asyncio.gather(*tasks)
        print("Finished searching !!!")
        return results
    
    # Generate Report from Search Results
    async def generate_detailed_report(self, user_query: str, search_summaries: list[str]):
        """Use the WriterAgent to compile a structured, markdown-based research report."""
        print("Thinking deeply about the report...")
        prompt_input = f"Original query: {user_query}\nSummarized search results: {search_summaries}"
        result = await Runner.run(writer_agent, prompt_input)
        print("Finished writing the report!")
        return result.final_output
    
    # Email the Final Report
    async def dispatch_report_via_email(self, report: ReportData):
        """Use the EmailAgent to send the formatted report via HTML email."""
        print("Preparing email...")
        result = await Runner.run(email_agent, report.markdown_report)
        print("Email sent successfully!")
        return report

    # Pipeline Function for Deep Research 
    async def runReport(self, query: str):
        """Run the deep research process, yielding the status updates and the final report"""
        trace_hash = gen_trace_id()
        with trace("Financial Research :: ", trace_id=trace_hash):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_hash}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_hash}"

            print("Starting research on User Query...")
            yield f"Starting full research pipeline..."
            search_plan = await self.search_planner(query)
            yield f"Search planner Completed, starting to search..."
            search_results = await self.perform_parallel_searches(search_plan)
            yield f"Searches completed, writing report..."
            final_report = await self.generate_detailed_report(query, search_results)
            yield "Report Writing is done, sending email..."
            await self.dispatch_report_via_email(final_report)
            yield "🎉 Research workflow completed! Check your inbox."
            yield final_report.markdown_report
        

