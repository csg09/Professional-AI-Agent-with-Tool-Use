# Professional AI Agent with Tool Use

A production-ready AI agent that represents you professionally on your website or portfolio, with function calling capabilities and real-time notifications. Get instant alerts when someone wants to connect with you or asks a question you can't answer.

## 🎯 What This Does

- **Professional Representation**: Acts as your 24/7 career assistant
- **Tool Integration**: Uses OpenAI function calling for real-world actions
- **Push Notifications**: Get instant alerts via Pushover when users interact
- **Email Capture**: Records user details when they want to connect
- **Gap Tracking**: Logs questions you can't answer to improve your agent
- **Production Ready**: Deployable to HuggingFace Spaces
- **Zero Maintenance**: Fully automated once deployed

## ✨ Key Features

- 📱 Real-time push notifications to your phone
- 🔧 Dynamic tool execution (no hardcoded if/else statements)
- 💼 Professional conversation management
- 📧 Automatic email capture and recording
- ❓ Unknown question tracking
- 🎨 Clean Gradio interface
- ☁️ Easy deployment to cloud
- 🔒 Privacy-protected personal data

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Pushover account (free)
- Your LinkedIn profile as PDF
- A personal summary file

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/csg09/professional-ai-agent.git
cd professional-ai-agent
pip install -r requirements.txt
```

### 2. Set Up Pushover

**Why Pushover?** Get notified on your phone when someone:
- Wants to connect with you
- Asks a question you can't answer

**Setup:**
1. Visit https://pushover.net/
2. Sign up for free account
3. Create an Application/API Token
4. Install Pushover app on your phone

### 3. Configure Environment

Create `.env` file:
```bash
# Required
OPENAI_API_KEY=your_openai_key

# Pushover (get from pushover.net)
PUSHOVER_USER=your_user_key_starts_with_u
PUSHOVER_TOKEN=your_token_starts_with_a
```

### 4. Add Your Personal Data

Create `me/` folder with:

**linkedin.pdf**: Export from LinkedIn
- Go to profile → More → Save to PDF

**summary.txt**: Your personal summary
```text
I am a [role] with [X years] experience...
Key skills: skill1, skill2, skill3...
Notable achievements: achievement1, achievement2...
```

### 5. Update Your Name

Edit the code:
```python
name = "Your Actual Name"  # Change this!
```

### 6. Run Locally

```bash
jupyter notebook professional_agent.ipynb
```

Or:
```bash
python professional_agent.py
```

## 📂 Project Structure

```
professional-ai-agent/
├── professional_agent.ipynb  # Main notebook
├── me/
│   ├── linkedin.pdf         # Your LinkedIn (you create)
│   └── summary.txt          # Your summary (you create)
├── app.py                   # Standalone deployment file
├── requirements.txt         # Dependencies
├── .env.example            # Config template
├── .gitignore              # Privacy protection
├── LICENSE                 # MIT License
├── README.md               # This file
└── DEPLOYMENT.md           # Deployment guide
```

## 💡 How It Works

### User Interaction Flow

```
User asks question
    ↓
AI analyzes with your context
    ↓
AI decides: answer OR use tools
    ↓
Tools execute:
    - record_user_details() → 📱 Push notification
    - record_unknown_question() → 📱 Push notification
    ↓
Tool results sent back to AI
    ↓
AI generates final response
    ↓
User sees response
```

### Available Tools

**1. record_user_details**
- Captures email, name, and conversation notes
- Sends push notification: "New contact from X"
- Use case: User wants to connect

**2. record_unknown_question**
- Logs questions agent can't answer
- Sends push notification: "Question I couldn't answer"
- Use case: Identifying knowledge gaps

### Adding New Tools (Easy!)

```python
# 1. Define function
def schedule_meeting(date, time):
    push(f"Meeting request: {date} at {time}")
    return {"scheduled": "ok"}

# 2. Define schema
schedule_meeting_json = {
    "name": "schedule_meeting",
    "description": "Schedule a meeting",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {"type": "string"},
            "time": {"type": "string"}
        },
        "required": ["date", "time"]
    }
}

# 3. Add to tools
tools.append({"type": "function", "function": schedule_meeting_json})

# Done! No need to modify handler!
```

## 🌐 Deployment to HuggingFace Spaces

Make your agent publicly accessible!

### Quick Deploy

```bash
# Install Gradio CLI
pip install gradio

# Login to HuggingFace
gradio deploy

# Follow prompts:
# - Space name: career-assistant
# - Hardware: cpu-basic (free)
# - Secrets: Enter your API keys
```

### Detailed Steps

**1. HuggingFace Setup:**
- Create account at https://huggingface.co
- Settings → Access Tokens → Create new token (WRITE access)

**2. Deploy:**
```bash
gradio deploy
```

**3. Configure:**
- Name your Space
- Choose hardware (cpu-basic for free tier)
- Add secrets when prompted:
  - OPENAI_API_KEY
  - PUSHOVER_USER
  - PUSHOVER_TOKEN

**4. Access:**
- Your Space: `https://huggingface.co/spaces/YOUR_USERNAME/career-assistant`

See DEPLOYMENT.md for complete guide.

## 📊 Real-World Examples

### Example 1: User Wants to Connect

```
User: "I'd love to discuss opportunities. My email is john@example.com"

Agent: (internally calls record_user_details)
📱 You get notification: "New contact from conversation
   Email: john@example.com
   Notes: User expressed interest in opportunities"

Agent: "Thank you! I've recorded your details and will be in touch soon..."
```

### Example 2: Unknown Question

```
User: "What's your favorite programming language?"

Agent: (internally calls record_unknown_question)
📱 You get notification: "Question I couldn't answer:
   What's your favorite programming language?"

Agent: "That's a great question! I don't have that information
       in my knowledge base. Let me record this for follow-up..."
```

## 🛠️ Customization

### Change Agent Personality

```python
system_prompt = f"You are {name}, a friendly and approachable engineer..."
# Add specific tone, examples, boundaries
```

### Add More Tools

Common additions:
- `search_portfolio()` - Search your projects
- `get_availability()` - Check calendar
- `send_to_crm()` - Log to Salesforce/HubSpot
- `search_knowledge_base()` - RAG integration

### Integrate with Other Services

```python
# Slack notifications
def push_to_slack(message):
    slack_webhook = os.getenv("SLACK_WEBHOOK")
    requests.post(slack_webhook, json={"text": message})

# Email notifications
def send_email(to, subject, body):
    # Use SendGrid, Mailgun, etc.
    pass

# Database logging
def log_to_db(user_data):
    # Store in PostgreSQL, MongoDB, etc.
    pass
```

## 💰 Cost Estimation

| Component | Service | Cost per query | Monthly (1000 queries) |
|-----------|---------|----------------|------------------------|
| AI Model | GPT-4o-mini | ~$0.001 | ~$1.00 |
| Notifications | Pushover | Free (up to 10k/month) | $0 |
| Hosting | HuggingFace | Free (cpu-basic) | $0 |
| **Total** | | **~$0.001** | **~$1.00** |

Incredibly affordable for 24/7 professional representation!

## 🎓 Use Cases

- **Job Seekers**: Portfolio website assistant
- **Freelancers**: Client inquiry handler
- **Consultants**: Lead capture system
- **Entrepreneurs**: Business inquiry router
- **Professionals**: Networking assistant
- **Students**: Academic portfolio helper

## 🐛 Troubleshooting

### Pushover Issues

**"Not receiving notifications"**
```bash
# Test Pushover directly
curl -s \
  --form-string "token=YOUR_TOKEN" \
  --form-string "user=YOUR_USER" \
  --form-string "message=test" \
  https://api.pushover.net/1/messages.json
```

**"Invalid credentials"**
- User key should start with 'u'
- Token should start with 'a'
- Check keys in Pushover dashboard
- Verify app is created

### Tool Calling Issues

**"Tools not being called"**
- Check system prompt mentions tools
- Verify tool schemas are correct JSON
- Look at `finish_reason` in logs
- Test with explicit: "Record my email: test@test.com"

**"Tool execution errors"**
- Check function signatures match schemas
- Verify required parameters
- Look for exceptions in logs
- Test functions individually

### Deployment Issues

**"Gradio deploy fails"**
- Ensure HuggingFace token has WRITE access
- Check: `huggingface-cli whoami`
- Remove any README.md in current directory
- Try: `gradio deploy --verbose`

**"Space crashes after deploy"**
- Check all secrets are set in Space settings
- Verify requirements.txt has all dependencies
- Look at Space logs in HuggingFace
- Test locally first

### General Issues

**"FileNotFoundError: me/linkedin.pdf"**
- Create `me/` folder
- Add linkedin.pdf and summary.txt
- Check file permissions

**"Agent loops infinitely"**
- Check max_iterations in code
- Verify tools return proper JSON
- Look for errors in tool execution

## 📈 Analytics Ideas

Track your agent's performance:

```python
# Add to tool functions
metrics = {
    "total_contacts": 0,
    "unknown_questions": 0,
    "most_common_questions": []
}

def record_user_details(email, name, notes):
    metrics["total_contacts"] += 1
    # ... rest of code
```

Send weekly summaries:
- Number of contacts
- Top questions asked
- Response quality metrics
- Busiest times

## 🤝 Contributing

Ideas for contributions:
- Additional tool integrations (calendar, CRM, etc.)
- Analytics dashboard
- Multi-language support
- Voice interface
- A/B testing framework
- Response quality scoring

## 📚 Learning Resources

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Pushover API](https://pushover.net/api)
- [Gradio Documentation](https://gradio.app/docs)
- [HuggingFace Spaces](https://huggingface.co/docs/hub/spaces)

## 📝 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- Built for professional self-representation
- Combines AI with real-world integrations
- Demonstrates production-ready AI development

## 📧 Questions?

Open an issue or contribute improvements!

---

**Your 24/7 professional assistant - with notifications! 🚀**
