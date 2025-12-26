"""
Professional AI Agent with Tool Use - Production Version
Class-based architecture for clean, maintainable code
"""

from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

# Load environment variables
load_dotenv(override=True)


def push(text):
    """Send push notification via Pushover"""
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": text,
            }
        )
        response.raise_for_status()
        print(f"📱 Notification sent: {text}")
    except Exception as e:
        print(f"⚠️ Notification failed: {e}")


def record_user_details(email, name="Name not provided", notes="not provided"):
    """Record user contact information"""
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    """Record questions that couldn't be answered"""
    push(f"Recording question: {question}")
    return {"recorded": "ok"}


# Tool schemas
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]


class Me:
    """
    Professional AI Agent that represents you on your website.
    
    This class encapsulates all functionality for your personal AI agent:
    - Loads your LinkedIn and summary
    - Handles conversations
    - Executes tools (function calling)
    - Manages the agentic loop
    """
    
    def __init__(self):
        """Initialize the agent with personal data"""
        self.openai = OpenAI()
        self.name = "Your Name"  # ← CHANGE THIS TO YOUR NAME!
        
        # Load LinkedIn profile
        try:
            reader = PdfReader("me/linkedin.pdf")
            self.linkedin = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.linkedin += text
            print(f"✓ LinkedIn loaded ({len(self.linkedin)} chars)")
        except FileNotFoundError:
            self.linkedin = "No LinkedIn data available."
            print("⚠️ linkedin.pdf not found in 'me' folder")
        
        # Load personal summary
        try:
            with open("me/summary.txt", "r", encoding="utf-8") as f:
                self.summary = f.read()
            print(f"✓ Summary loaded ({len(self.summary)} chars)")
        except FileNotFoundError:
            self.summary = "No summary available."
            print("⚠️ summary.txt not found in 'me' folder")
        
        print(f"✓ Agent initialized for: {self.name}")
    
    def handle_tool_call(self, tool_calls):
        """
        Execute tool calls from the AI model.
        
        Uses dynamic dispatch via globals() to avoid hardcoded if/else statements.
        
        Args:
            tool_calls: List of tool calls from OpenAI response
        
        Returns:
            List of tool results in OpenAI format
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Tool called: {tool_name}", flush=True)
            
            # Dynamic tool execution
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {"error": f"Tool {tool_name} not found"}
            
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        
        return results
    
    def system_prompt(self):
        """
        Generate the system prompt with personal context.
        
        Returns:
            Complete system prompt string
        """
        prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool."
        
        prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        
        return prompt
    
    def chat(self, message, history):
        """
        Main chat function with agentic tool-calling loop.
        
        Process:
        1. Add user message to conversation
        2. Call AI model with tools
        3. If AI wants to use tools, execute them
        4. Send tool results back to AI
        5. Repeat until AI generates final response
        
        Args:
            message: User's message
            history: Conversation history from Gradio
        
        Returns:
            AI's final response
        """
        messages = [
            {"role": "system", "content": self.system_prompt()}
        ] + history + [
            {"role": "user", "content": message}
        ]
        
        done = False
        iteration = 0
        max_iterations = 10
        
        while not done and iteration < max_iterations:
            iteration += 1
            
            # Call OpenAI with tools
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools
            )
            
            finish_reason = response.choices[0].finish_reason
            
            # Check if AI wants to call tools
            if finish_reason == "tool_calls":
                message_with_tools = response.choices[0].message
                tool_calls = message_with_tools.tool_calls
                
                # Execute tools
                results = self.handle_tool_call(tool_calls)
                
                # Add to conversation
                messages.append(message_with_tools)
                messages.extend(results)
            else:
                done = True
        
        if iteration >= max_iterations:
            print("⚠️ Max iterations reached")
        
        return response.choices[0].message.content


if __name__ == "__main__":
    # Initialize agent
    me = Me()
    
    # Create Gradio interface
    interface = gr.ChatInterface(
        me.chat,
        type="messages",
        title=f"Chat with {me.name}'s AI Agent",
        description=f"Ask me about {me.name}'s background, skills, and experience!",
        examples=[
            "What's your background?",
            "What technologies do you work with?",
            "I'd like to connect. My email is example@email.com"
        ]
    )
    
    # Launch
    interface.launch()
