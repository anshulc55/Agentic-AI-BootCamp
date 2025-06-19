# 📬 SendGrid Setup for AI Sales Agent (TechLink Course)

This guide walks you through the steps to set up **SendGrid**, which allows your AI-powered sales agent to send cold emails via a verified sender address.

---

## 🔧 Prerequisites

- A [SendGrid](https://sendgrid.com/) account (Free tier available)
- Python project with `dotenv`, `openai`, and `sendgrid` packages
- A `.env` file in your project root

---

## 🛠 Step 1: Create a Free SendGrid Account

1. Visit: [https://sendgrid.com/](https://sendgrid.com/)
2. Sign up for a free account.
3. Complete any email confirmation steps required by SendGrid.

---

## 🔑 Step 2: Generate Your API Key

1. Log in to your SendGrid dashboard.
2. Go to:
   ```
   Settings (left sidebar) → API Keys → Create API Key (top right button)
   ```
3. Choose "Full Access" or "Restricted Access" (for `mail.send` only).
4. Copy the API key to your clipboard.

---

## 🧪 Step 3: Add API Key to Your Project

1. Open your project folder.
2. Locate or create a `.env` file.
3. Add the following line (replace `xxxx` with your actual key):

   ```env
   SENDGRID_API_KEY=xxxx
   ```

---

## ✅ Step 4: Verify Your Sender Email

1. In the SendGrid dashboard, go to:

   ```
   Settings (left sidebar) → Sender Authentication → Verify a Single Sender
   ```

2. Enter your personal or company email (e.g., `you@yourdomain.com`).
3. Confirm the email via the verification link sent to your inbox.

⚠️ You must complete this step. **SendGrid will not send emails from unverified addresses**, even during testing.

---

## ✅ You're Done!

You’re now ready to integrate SendGrid into your agent system.  
In your code, you can now use the `send_email()` function (decorated with `@function_tool`) to dispatch real emails through your AI agent.

---

### 🧠 Bonus Tip

If you’re working with teammates, avoid checking in your `.env` file.  
Instead, share API keys securely or use secret managers in production.

---

> 🔗 Need help integrating SendGrid with your AI Agent SDK workflow?  
Check out the [lecture walkthrough](#) or use the `sales_manager_agent` pattern described in our source code.