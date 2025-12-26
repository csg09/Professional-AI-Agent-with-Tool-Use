# Deployment Guide - HuggingFace Spaces

Complete guide for deploying your Professional AI Agent to HuggingFace Spaces.

## 🎯 Why Deploy?

- **24/7 Availability**: Your agent runs even when your computer is off
- **Public Access**: Share a URL with anyone
- **Free Hosting**: HuggingFace offers free CPU hosting
- **Professional**: Makes you look cutting-edge
- **Real Notifications**: Get alerts when people interact with your agent

## 📋 Pre-Deployment Checklist

### Required Files

- [ ] `professional_agent.ipynb` or `app.py`
- [ ] `requirements.txt`
- [ ] `me/linkedin.pdf` (your LinkedIn profile)
- [ ] `me/summary.txt` (your personal summary)

### Required Accounts

- [ ] HuggingFace account (https://huggingface.co)
- [ ] OpenAI API key
- [ ] Pushover account with API keys
- [ ] Pushover app installed on phone

### Configuration

- [ ] Updated `name = "Your Name"` in code
- [ ] Tested locally and it works
- [ ] All secrets in `.env` file (but don't commit it!)

## 🚀 Deployment Methods

### Method 1: Gradio Deploy (Easiest)

**Step 1: Install Gradio**
```bash
pip install gradio
```

**Step 2: Deploy**
```bash
gradio deploy
```

**Step 3: Follow Prompts**
- Space name: `career-assistant` (or your choice)
- App file: `professional_agent.ipynb` or `app.py`
- Hardware: `cpu-basic` (free tier)
- Secrets: Yes, we need to add secrets
- Enter your secrets:
  - `OPENAI_API_KEY`: Your OpenAI key
  - `PUSHOVER_USER`: Your Pushover user key (starts with 'u')
  - `PUSHOVER_TOKEN`: Your Pushover app token (starts with 'a')
- GitHub Actions: No (for now)

**Step 4: Wait for Build**
- Space will build (2-5 minutes)
- You'll get a URL: `https://huggingface.co/spaces/YOUR_USERNAME/career-assistant`

**Step 5: Test**
- Visit your Space URL
- Ask a question
- Check if you get a notification!

### Method 2: HuggingFace Hub (Manual)

**Step 1: Create Space on HuggingFace**
1. Go to https://huggingface.co
2. Click your avatar → "New Space"
3. Space name: `career-assistant`
4. License: MIT
5. Space SDK: Gradio
6. Space hardware: CPU basic (free)
7. Click "Create Space"

**Step 2: Clone Repository**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/career-assistant
cd career-assistant
```

**Step 3: Add Files**
```bash
# Copy your files
cp professional_agent.ipynb .
cp -r me .
cp requirements.txt .

# Create app.py if using notebook
# (HuggingFace needs app.py for Gradio Spaces)
```

**Step 4: Commit and Push**
```bash
git add .
git commit -m "Initial deployment"
git push
```

**Step 5: Add Secrets**
1. Go to your Space settings (gear icon)
2. Scroll to "Variables and Secrets"
3. Add:
   - `OPENAI_API_KEY`
   - `PUSHOVER_USER`
   - `PUSHOVER_TOKEN`
4. Save

**Step 6: Space Rebuilds Automatically**

### Method 3: GitHub → HuggingFace (Advanced)

Connect your GitHub repo to HuggingFace for automatic deployments.

1. Push code to GitHub
2. Create Space on HuggingFace
3. Link GitHub repo in Space settings
4. Every push to GitHub auto-deploys to HuggingFace

## 🔒 Managing Secrets

### View/Edit Secrets

1. Go to your Space on HuggingFace
2. Click Settings (gear icon)
3. Scroll to "Variables and Secrets"
4. Add, edit, or delete secrets

### Best Practices

✅ **Do:**
- Use secrets for all API keys
- Test locally before deploying
- Keep secrets in .env locally (not committed)
- Use different API keys for production if possible

❌ **Don't:**
- Hardcode API keys in code
- Commit .env file to git
- Share your secrets
- Use same keys for testing and production

## 🔧 Creating app.py for Deployment

If deploying from a notebook, create `app.py`:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pypdf import PdfReader
import gradio as gr

# Load environment (for local testing)
load_dotenv(override=True)

# Initialize OpenAI
openai = OpenAI()

# Pushover setup
pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# ... (rest of your code from notebook)

# At the end:
if __name__ == "__main__":
    interface.launch()
```

## 📊 Monitoring Your Deployed Space

### Check Logs

1. Go to your Space
2. Click "Logs" tab
3. See real-time output

### Monitor Usage

1. Go to Space settings
2. See visitor count
3. Track API usage in OpenAI dashboard

### Test Notifications

Send test messages to verify Pushover works:
```python
curl -s \
  --form-string "token=YOUR_TOKEN" \
  --form-string "user=YOUR_USER" \
  --form-string "message=test from HuggingFace" \
  https://api.pushover.net/1/messages.json
```

## 🔄 Updating Your Deployed Space

### Option 1: Redeploy with Gradio

```bash
gradio deploy
```

Gradio detects existing Space and updates it.

### Option 2: Git Push (if using git)

```bash
git add .
git commit -m "Update agent"
git push
```

Space rebuilds automatically.

### Option 3: Edit Files Directly

1. Go to Space → Files tab
2. Edit files directly in browser
3. Commit changes
4. Space rebuilds

## 🐛 Troubleshooting Deployment

### "Space won't start"

**Check logs:**
1. Go to Space → Logs tab
2. Look for error messages

**Common issues:**
- Missing requirements in requirements.txt
- Secrets not set correctly
- File paths wrong (use relative paths)
- Port already in use (don't specify port)

### "Import errors"

Add missing packages to requirements.txt:
```bash
# requirements.txt
openai>=1.0.0
python-dotenv>=1.0.0
pypdf>=3.0.0
gradio>=4.0.0
requests>=2.31.0
```

### "Pushover not working"

1. Check secrets are set in Space settings
2. Verify keys are correct (no spaces/newlines)
3. Test Pushover directly with curl
4. Check Pushover app is installed on phone

### "Can't access files in me/ folder"

Make sure folder structure is:
```
space-root/
├── app.py (or professional_agent.ipynb)
├── me/
│   ├── linkedin.pdf
│   └── summary.txt
└── requirements.txt
```

### "Space is slow"

- CPU basic is slower than local
- Consider upgrading hardware tier
- Optimize code (reduce model calls)
- Use streaming responses

## 💰 Costs

### Free Tier
- CPU basic: **FREE**
- Limitations:
  - Slower inference
  - May sleep after inactivity
  - Public visibility required

### Paid Tiers
| Hardware | Cost/hour | Use case |
|----------|-----------|----------|
| CPU basic | Free | Perfect for this agent |
| CPU upgrade | ~$0.03 | Faster response times |
| GPU T4 | ~$0.60 | Overkill for this use |

### API Costs
- OpenAI (GPT-4o-mini): ~$0.001/query
- Pushover: Free (up to 10k notifications/month)
- **Total per query: ~$0.001**

## 📈 Post-Deployment

### Share Your Space

Get your URL:
```
https://huggingface.co/spaces/YOUR_USERNAME/career-assistant
```

Share it:
- Add to resume/CV
- Include in email signature
- Post on LinkedIn
- Add to portfolio website
- Share on Twitter

### Collect Feedback

Monitor:
- Questions users ask
- Unknown questions logged
- Contact requests received
- Response quality

Iterate:
- Update summary.txt
- Add more tools
- Improve system prompt
- Fix edge cases

### Analytics

Track:
- Daily active users
- Popular questions
- Peak usage times
- Conversion rate (visitors → contacts)

## 🎓 Advanced Deployment

### Custom Domain

1. Buy domain (e.g., talk-to-you.com)
2. Go to Space settings
3. Add custom domain
4. Update DNS records
5. SSL automatically provisioned

### CI/CD Pipeline

Automate deployment:
```yaml
# .github/workflows/deploy.yml
name: Deploy to HuggingFace
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        run: |
          pip install gradio
          gradio deploy --token ${{ secrets.HF_TOKEN }}
```

### Multiple Environments

- Development: Test changes
- Staging: Preview for clients
- Production: Public-facing

### Monitoring & Alerts

- Set up Sentry for error tracking
- Use Grafana for metrics
- Create uptime monitors
- Set up status page

## 📚 Resources

- [HuggingFace Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Deployment Guide](https://gradio.app/guides/sharing-your-app)
- [Pushover API Docs](https://pushover.net/api)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

## 🆘 Getting Help

**HuggingFace Community:**
- Forum: https://discuss.huggingface.co
- Discord: https://discord.gg/huggingface

**Gradio:**
- Discord: https://discord.gg/gradio
- GitHub Issues: https://github.com/gradio-app/gradio

**This Project:**
- Open an issue on GitHub
- Check existing issues first

---

**Good luck with your deployment! 🚀**
