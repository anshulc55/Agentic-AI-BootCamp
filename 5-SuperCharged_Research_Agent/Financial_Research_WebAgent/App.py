## The Gradio-powered UI for the end-user to run everything with one click.

import gradio as gr
from dotenv import load_dotenv
from ResearchManager import ResearchManager


# Load .env file in Environment Variable 
load_dotenv(override=True)

# Function to call the Report Manager
async def executeQuery(query: str):
    async for block in ResearchManager().runReport(query):
        yield block


# Gradio with Custom UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("📊 Financial Research Tool")
    query_textbox = gr.Textbox(label="Enter your Financial Research Query...")
    run_button = gr.Button("Run Query", variant="primary")
    report = gr.Markdown(label="Report")

    run_button.click(fn=executeQuery, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=executeQuery, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)



