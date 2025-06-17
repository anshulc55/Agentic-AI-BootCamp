"""
LLM Tool Call Demo App
----------------------
- Sends mobile notifications via Pushover
- Records user details and unknown questions
- Reads profile/summary from local files
- Simulates tool call dispatching (e.g., from OpenAI function calling)
- Exposes a Gradio Chat Interface for conversation
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from types import SimpleNamespace
from pypdf import PdfReader
from openai import OpenAI
import gradio as gr

# --- Load Environment Variables ---
load_dotenv(override=True)

# --- Mobile Notification Setup ---
PUSH_NOTIFICATION_URI = "https://api.pushover.net/1/messages.json"
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

def push_notification(message: str):
    data = {
        "token": pushover_token,
        "user": pushover_user,
        "message": message
    }
    response = requests.post(PUSH_NOTIFICATION_URI, data)
    if response.status_code == 200:
        return "Notification sent!"
    return f"Failed to send: {response.text}"

# --- Tool Functions ---
def record_user_details(email, name="Name not provided", notes="not provided"):
    push_notification(f"[User Interest] {name} ({email}) | Notes: {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push_notification(f"[Unknown Question] {question}")
    return {"recorded": "ok"}

# --- Tool Schemas ---
record_user_details_json = {
    "name": "record_user_details",
    "description": "Record a user's interest using their email and optional details.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "User's email address"},
            "name": {"type": "string", "description": "User's name"},
            "notes": {"type": "string", "description": "Additional context or comments"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Log a question that the assistant couldn't answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The unanswerable question"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# --- Tool Dispatcher ---
TOOL_FUNCTIONS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}

def dispatch_tool_calls(tool_calls):
    results = []
    for call in tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments)
        print(f"Tool called: {name}")
        func = TOOL_FUNCTIONS.get(name)
        if func:
            try:
                result = func(**args)
            except Exception as e:
                result = {"error": f"Execution failed: {str(e)}"}
        else:
            result = {"error": f"Unknown tool: {name}"}

        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "name": name,
            "tool_call_id": call.id
        })
    return results

# --- Load Profile and Summary Data ---
project_root = Path.cwd().parent
profile_path = project_root / "Resourses" / "Profile.pdf"
summary_path = project_root / "Resourses" / "Summary.txt"

prof_summary = "".join(
    page.extract_text() or "" for page in PdfReader(profile_path).pages
)

with open(summary_path, "r", encoding="utf-8") as f:
    summary = f.read()

# --- System Prompt ---
name = "Parag Agrawal"
system_prompt = (
    f"You are acting as {name}, representing {name} on their website. "
    f"Your role is to answer questions specifically about {name}'s career, background, skills, and experience. "
    f"You must faithfully and accurately portray {name} in all interactions. "
    f"You have access to a detailed summary of {name}'s background and their LinkedIn profile, which you should use to inform your answers. "
    f"Maintain a professional, engaging, and approachable tone. "
    f"Always record any unanswered questions using the record_unknown_question tool. "
    f"If the user continues chatting, encourage them to share their email address, then use the record_user_details tool."
    f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{prof_summary}\n"
)

# --- OpenAI Clients ---
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_client = OpenAI(api_key=gemini_api_key, base_url=gemini_base_url)

openai_api_key = os.getenv('API_TOKEN')
deepseek_base_url = "https://api.deepseek.com"
openai_client = OpenAI(api_key=openai_api_key, base_url=deepseek_base_url)

# --- Conversation Handler ---
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

def run_conversation(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    finishLoop = False
    message_obj = None

    while not finishLoop:
        response = openai_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message_obj = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        print(f"Finish Reason : {finish_reason}")

        if finish_reason == "tool_calls":
            tool_calls = response.choices[0].message.tool_calls
            messages.append(message_obj)
            tool_result = dispatch_tool_calls(tool_calls)
            messages.extend(tool_result)
            finishLoop = True
        else:
            finishLoop = True

    return message_obj

# --- Gradio UI ---
gr.ChatInterface(run_conversation, type="messages").launch(share=True)