from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

class MyCustomPushNotification(BaseModel):
    """A message to be sent to the user"""
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body")

class MyCustomPushNotificationTool(BaseTool):
    """A tool to send push notifications to the user."""
    name: str = "MyCustomPushNotificationTool"  # Unique name for the tool
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = MyCustomPushNotification

    def _run(self, title: str, body: str) -> str:
        """Send a push notification to the user."""
        PUSH_NOTIFICATION_URI="https://api.pushover.net/1/messages.json"
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        if not pushover_user or not pushover_token:
            raise ValueError("PUSHOVER_USER and PUSHOVER_TOKEN must be set in environment variables.")
        data = {
            "token": pushover_token,
            "user": pushover_user,
            "title": title,
            "message": body
        }
        response = requests.post(PUSH_NOTIFICATION_URI, data=data)
        if response.status_code != 200:
            raise Exception(f"Failed to send push notification: {response.text}")
        return f"Push notification sent successfully: {title} - {body}"
        
