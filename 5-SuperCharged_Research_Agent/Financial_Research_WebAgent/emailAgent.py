## Formats and sends the final markdown report via email using a hosted tool.

from agents import function_tool, Agent
from sendgrid.helpers.mail import Email, To, Content, Mail
import sendgrid, os

# Email Sender Tool
@function_tool
def send_email(subject: str, html_body: str):
     """Send an HTML email with subject and body to the recipient list."""
     sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
     sender = Email("anshulc55@gmail.com")
     recipient = To("anshulc55@icloud.com")
     content = Content("text/html", html_body)
     email = Mail(sender, recipient, subject, content).get()
     response = sg.client.mail.send.post(request_body=email)
     return {"status": "Success" , "code": response.status_code}


# Email Agent
INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="EmailAgent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4.1-mini",
)