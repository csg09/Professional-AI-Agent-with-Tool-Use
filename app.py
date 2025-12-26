"""
Professional AI Agent with Tool Use
Standalone app.py for deployment to HuggingFace Spaces
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import gradio as gr

# Load environment variables (for local testing)
load_dotenv(override=True)

# Initialize OpenAI
openai = OpenAI()

# Pushover configuration
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# Pushover notification function
def push(message):
    """Send push notification via Pushover"""
    print(f"📱 Push notification: {message}")
    
    if not pushover_user or not pushover_token:
        print("⚠️ Pushover not configured")
        return None
    
    payload = {
        "user": pushover_user,
        "token": pushover_token,
        "message": message
    }
    
    try:
        response = requests.post(pushover_url, data=payload)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"✗ Notification error: {e}")
        return None

# Tool functions
def record_user_details(email, name="Name not provided", notes="not provided"):
    """Record user contact information"""
    notification = f"📧 New contact from {name}\nEmail: {email}\nNotes: {notes}"
    push(notification)
    return {"recorded": "ok", "message": "Contact details saved"}

def record_unknown_question(question):
    """Record questions the agent couldn't answer"""
    notification = f"❓ Question I couldn't answer:\n{question}"
    push(notification)
    return {"recorded": "ok", "message": "Question logged"}

# Tool schemas
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional information about the conversation"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

# Tool execution handler
def handle_tool_calls(tool_calls):
    """Execute tool calls dynamically"""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 Tool called: {tool_name}")
        
        # Dynamic tool execution (no hardcoded if/else!)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {"error": f"Tool {tool_name} not found"}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    
    return results

# Load personal data
try:
    reader = PdfReader("me/linkedin.pdf")
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text
    print(f"✓ LinkedIn loaded ({len(linkedin)} chars)")
except FileNotFoundError:
    linkedin = "No LinkedIn data available."
    print("⚠️ linkedin.pdf not found")

try:
    with open("me/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    print(f"✓ Summary loaded ({len(summary)} chars)")
except FileNotFoundError:
    summary = "No summary available."
    print("⚠️ summary.txt not found")

# Configuration
name = "Your Name"  # ← CHANGE THIS!

# System prompt
system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

# Main chat function
def chat(message, history):
    """Chat function with tool support"""
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    
    done = False
    iteration = 0
    max_iterations = 10
    
    while not done and iteration < max_iterations:
        iteration += 1
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )
        
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == "tool_calls":
            message_with_tools = response.choices[0].message
            tool_calls = message_with_tools.tool_calls
            
            results = handle_tool_calls(tool_calls)
            
            messages.append(message_with_tools)
            messages.extend(results)
        else:
            done = True
    
    return response.choices[0].message.content

# Create interface
interface = gr.ChatInterface(
    chat,
    type="messages",
    title=f"Chat with {name}'s AI Agent",
    description=f"Ask me about {name}'s background, skills, and experience. I can also help you get in touch!",
    examples=[
        "What's your background?",
        "What technologies do you work with?",
        "I'd like to connect. My email is example@email.com"
    ]
)

# Launch
if __name__ == "__main__":
    interface.launch()
