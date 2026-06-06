# Odysseus Wrapper🤖

> A self-hosted AI workspace — the privacy-first, local-first alternative to ChatGPT and Claude.

## What is Odysseus?

**Odysseus** is a powerful, self-hosted AI workspace built with Python (FastAPI). It provides a complete local AI experience including chat with any LLM, autonomous agents, deep research, document editing, email triage, calendar sync, and more — all running on your own hardware with your own data.

This wrapper provides a Pythonic interface for interacting with Odysseus deployments programmatically.

##⭐ Key Features

- **Chat** — Talk to any local model (vLLM, llama.cpp, Ollama) or API (OpenRouter, OpenAI, Copilot)
- **Agent** — Autonomous agent with tools (MCP, shell, file ops, skills, memory)
- **Deep Research** — Multi-step research pipelines with visual reports
- **Compare** — Blind model comparison testing
- **Documents** — Multi-tab editor with AI assistance
- **Memory / Skills** — Persistent vector memory with ChromaDB
- **Email** — IMAP/SMTP inbox with AI triage
- **Calendar** — CalDAV sync to Radicale/Nextcloud/Apple/Fastmail
- **Mobile-friendly** — Responsive PWA design

## 📦 Installation

```bash
pip install odysseus-wrap
```

Or install from source:

```bash
git clone https://github.com/q15004040209-creator/odysseus-wrap.git
cd odysseus-wrap
pip install -e .
```

## 🚀 Quick Start

```python
from odysseus import OdysseusClient

# Connect to a local Odysseus instance
client = OdysseusClient(base_url="http://localhost:7000", api_key="your-api-key")

# Chat with a model
response = client.chat.send_message(
    prompt="What is the capital of France?",
    model="openai/gpt-4o"
)
print(response.content)

# Run an agent task
result = client.agent.run(
    task="Search for the latest news about AI agents",
    tools=["web_search", "memory"]
)
print(result)

# Query memory
memories = client.memory.search(query="my previous projects", limit=5)
for m in memories:
    print(f"- {m.content}")
```

## 🔧 Configuration

```python
from odysseus import OdysseusClient

client = OdysseusClient(
    base_url="http://localhost:7000",  # Odysseus server URL
    api_key="your-api-key",            # API key from Settings
    timeout=120,                       # Request timeout in seconds
    verify_ssl=True # Set False for self-signed certs
)
```

## 📚 API Reference

### Chat

```python
# Send a simple message
response = client.chat.send_message(
    prompt="Explain quantum computing in simple terms",
    model="ollama/llama3", # Model identifier
    temperature=0.7,
    max_tokens=500
)

# Multi-turn conversation
conversation = client.chat.create_conversation()
conversation.send_message("Hello, I'm learning Python")
conversation.send_message("What should I start with?")
history = conversation.get_history()
```

### Agent

```python
# Run an autonomous agent with specific tools
result = client.agent.run(
    task="Find all PDF files in the current directory and summarize them",
    tools=["file_read", "shell", "memory"],
    model="openrouter/anthropic/claude-3-opus",
    max_steps=10
)
print(result.final_response)
```

### Deep Research

```python
# Conduct multi-step research
report = client.research.run(
    topic="The impact of LLMs on software development",
    depth="comprehensive", # quick / standard / comprehensive
    sources=["web", "arxiv", "github"]
)

# Save the report
with open("research_report.md", "w") as f:
    f.write(report.markdown)
```

### Memory / Skills

```python
# Store information in persistent memory
client.memory.add(
    content="User prefers to receive summaries in bullet points",
    tags=["preference", "formatting"],
    metadata={"source": "conversation"}
)

# Search memory
results = client.memory.search(
    query="user formatting preferences",
    limit=10,
    filters={"tags": ["preference"]}
)

# List all skills
skills = client.skills.list()
for skill in skills:
    print(f"- {skill.name}: {skill.description}")
```

### Documents

```python
# Create and edit documents with AI assistance
doc = client.documents.create(
    title="Project Notes",
    content="# My Project\n\nThis is my project.",
    format="markdown"
)

# AI-assisted editing
suggestions = client.documents.get_suggestions(doc.id)
for suggestion in suggestions:
    print(f"Line {suggestion.line}: {suggestion.suggestion}")
```

### Email (IMAP/SMTP)

```python
# List emails
emails = client.email.list(folder="INBOX", unread_only=True, limit=20)

# Send email
client.email.send(
    to="recipient@example.com",
    subject="Quick Update",
    body="Here's a quick summary of today's meeting...",
    draft=True  # Save as draft instead of sending
)

# Triage emails
triage = client.email.triage(folder="INBOX", strategy="urgency")
for item in triage.urgent:
    print(f"URGENT: {item.subject}")
```

### Calendar

```python
# List events
events = client.calendar.list(
    start="2026-01-01",
    end="2026-01-31",
    calendar_ids=["work", "personal"]
)

# Create event
event = client.calendar.create(
    title="Team Meeting",
    start="2026-01-15T10:00:00",
    end="2026-01-15T11:00:00",
    description="Weekly sync",
    calendar_id="work"
)
```

##🌐 Deployment

### Docker (Recommended)

```bash
git clone https://github.com/pewdiepie-archdaemon/odysseus.git
cd odysseus
cp .env.example .env
docker compose up -d --build
```

Then open `http://localhost:7000` and configure your models in Settings.

### Native (Linux/macOS)

```bash
git clone https://github.com/pewdiepie-archdaemon/odysseus.git
cd odysseus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py
python -m uvicorn app:app --host 127.0.0.1 --port 7000
```

### Windows

```powershell
git clone https://github.com/pewdiepie-archdaemon/odysseus.git
cd odysseus
powershell -ExecutionPolicy Bypass -File .\launch-windows.ps1
```

## 🔒 Security Notes

- Always keep `AUTH_ENABLED=true` for network deployments
- Use `SECURE_COOKIES=true` when behind HTTPS reverse proxy
- Never expose Odysseus directly to the public internet
- Rotate API keys if ever shared in chats/logs

## 📄 License

- **This wrapper**: MIT License
- **Odysseus**: MIT License — [pewdiepie-archdaemon/odysseus](https://github.com/pewdiepie-archdaemon/odysseus)

## 🔗 Links

- 🌐 [Odysseus Official Site](https://odysseus.io)
- 📖 [Odysseus Documentation](https://github.com/pewdiepie-archdaemon/odysseus)
- 💬 [Discord Community](https://discord.gg/odysseus)
- 🐛 [Report Issues](https://github.com/pewdiepie-archdaemon/odysseus/issues)