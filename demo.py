#!/usr/bin/env python3
"""
Odysseus Wrapper - Demo Script
A Pythonic interface for interacting with Odysseus AI workspace.

This demo showcases the main features of the odysseus-wrap library.
Run with: python demo.py
"""

import time
from odysseus import OdysseusClient


def demo_basic_chat():
    """Basic chat interaction with a local or API model."""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Chat")
    print("=" * 60)

    client = OdysseusClient(
        base_url="http://localhost:7000",
        api_key="your-api-key-here"
    )

    print("\nSending message to GPT-4o...")
    response = client.chat.send_message(
        prompt="What is the difference between a transformer and an RNN?",
        model="openai/gpt-4o",
        temperature=0.7,
        max_tokens=300
    )
    print(f"\n🤖 Response:\n{response.content}")

    return client


def demo_conversation():
    """Multi-turn conversation with context."""
    print("\n" + "=" * 60)
    print("DEMO 2: Multi-Turn Conversation")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")
    conv = client.chat.create_conversation(model="ollama/llama3")

    messages = [
        "Hello! I'm just getting started with Python.",
        "What's the first thing I should learn?",
        "Can you show me a simple example?",
    ]

    for msg in messages:
        print(f"\n👤 You: {msg}")
        response = conv.send_message(msg)
        print(f"🤖 Bot: {response.content}")
        time.sleep(0.5)


def demo_agent():
    """Run an autonomous agent to complete a task."""
    print("\n" + "=" * 60)
    print("DEMO 3: Autonomous Agent Task")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

    task = """
    Find all Python files in the current directory,
    count the total lines of code, and save a summary to memory.
    """

    print(f"\n🧠 Running agent with task:\n{task}")
    print("\n⏳ This may take a minute...\n")

    result = client.agent.run(
        task=task,
        tools=["shell", "file_read", "memory"],
        model="openrouter/anthropic/claude-3-opus",
        max_steps=15
    )

    print(f"\n✅ Agent completed in {result.steps} steps")
    print(f"📋 Final Response:\n{result.final_response}")


def demo_deep_research():
    """Conduct comprehensive research on a topic."""
    print("\n" + "=" * 60)
    print("DEMO 4: Deep Research")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

   print("\n🔬 Starting comprehensive research on 'LLM Agents'...")
    print("⏳ This may take several minutes for full depth...\n")

    report = client.research.run(
        topic="The current state of LLM agents in software development",
        depth="standard",  # quick / standard / comprehensive
        sources=["web", "github", "arxiv"]
    )

    print("📊 Research Report Generated!\n")
    print(f"Title: {report.title}")
    print(f"Sections: {len(report.sections)}")
    print(f"\n{report.markdown[:500]}...")

    # Save to file
    with open("research_report.md", "w") as f:
        f.write(report.markdown)
    print("\n💾 Report saved to research_report.md")


def demo_memory():
    """Store and retrieve information from persistent memory."""
    print("\n" + "=" * 60)
    print("DEMO 5: Persistent Memory")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

    # Add personal information
    memories = [
        {
            "content": "User works as a backend engineer specializing in Python and Go",
            "tags": ["work", "role"]
        },
        {
            "content": "User prefers concise, code-heavy explanations",
            "tags": ["preference", "communication"]
        },
        {
            "content": "User is interested in AI agents and automation",
            "tags": ["interest", "ai"]
        }
    ]

    print("\n📝 Storing memories...")
    for mem in memories:
        client.memory.add(
            content=mem["content"],
            tags=mem["tags"],
            metadata={"source": "demo"}
        )
        print(f"  ✅ Added: {mem['content'][:50]}...")

    # Search memory
    print("\n🔍 Searching for 'Python engineer preferences'...")
    results = client.memory.search(
        query="Python backend engineer preferences",
        limit=5,
        filters={"tags": ["preference"]}
    )

    print(f"\nFound {len(results)} relevant memories:")
    for r in results:
        print(f"  • {r.content[:80]}... (score: {r.score:.2f})")


def demo_document_editing():
    """Create and edit documents with AI assistance."""
    print("\n" + "=" * 60)
    print("DEMO 6: AI-Assisted Document Editing")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

    # Create a document
    content = """# Project Roadmap

## Q1 Goals
- Build core API
- Set up CI/CD
- Write documentation

## Q2 Goals
- Add user authentication
- Implement billing
- Launch beta
"""
    doc = client.documents.create(
        title="Q1-Q2 Roadmap",
        content=content,
        format="markdown"
    )
    print(f"\n📄 Created document: {doc.title} (ID: {doc.id})")

    # Get AI suggestions
    suggestions = client.documents.get_suggestions(doc.id)
    print(f"\n💡 Got {len(suggestions)} AI suggestions:")
    for s in suggestions:
        print(f"  Line {s.line}: {s.suggestion[:100]}...")

    # Apply a suggestion
    if suggestions:
        client.documents.apply_suggestion(doc.id, suggestions[0].id)
        print(f"\n✅ Applied suggestion #{suggestions[0].id}")


def demo_email_triage():
    """Manage email with AI-powered triage."""
    print("\n" + "=" * 60)
    print("DEMO 7: Email Triage")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

    # List unread emails
    print("\n📬 Fetching unread emails...")
    emails = client.email.list(folder="INBOX", unread_only=True, limit=10)

    if not emails:
        print("No unread emails found.")
        return

    print(f"Found {len(emails)} unread emails:")
    for email in emails:
        print(f"  • From: {email.from_}")
        print(f"    Subject: {email.subject}")
        print(f"    Date: {email.date}")
        print()

    # Send a draft email
    print("\n📤 Creating draft reply...")
    draft = client.email.send(
        to=emails[0].from_,
        subject=f"Re: {emails[0].subject}",
        body="Thank you for your email. I'll get back to you shortly.",
        draft=True
    )
    print(f"  ✅ Draft saved (ID: {draft.id})")

    # Run AI triage on inbox
    print("\n🤖 Running AI triage...")
    triage = client.email.triage(folder="INBOX", strategy="urgency")

    print(f"\n📊 Triage Results:")
    print(f"  🚨 Urgent: {len(triage.urgent)}")
    print(f"  📌 Action Required: {len(triage.action_required)}")
    print(f"  ✅ Can Wait: {len(triage.can_wait)}")


def demo_calendar():
    """Calendar management with CalDAV sync."""
    print("\n" + "=" * 60)
    print("DEMO 8: Calendar Management")
    print("=" * 60)

    client = OdysseusClient(base_url="http://localhost:7000")

    # List calendars
    calendars = client.calendar.list_calendars()
    print(f"\n📅 Found {len(calendars)} calendars:")
    for cal in calendars:
        print(f"  • {cal.name} ({cal.id}) - {cal.color}")

    # List upcoming events
    print("\n📆 Upcoming events this month:")
    events = client.calendar.list(
        start="2026-06-01",
        end="2026-06-30"
    )

    if not events:
        print("  No events found.")
    else:
        for event in events:
            print(f"  • {event.start.strftime('%m/%d %H:%M')} - {event.title}")

    # Create an event
    print("\n🆕 Creating new event...")
    new_event = client.calendar.create(
        title="Team Standup",
        start="2026-06-10T09:00:00",
        end="2026-06-10T09:30:00",
        description="Daily team sync",
        calendar_id=calendars[0].id if calendars else None
    )
    print(f"  ✅ Event created (ID: {new_event.id})")


def main():
    """Run all demos."""
    print("\n" + "🎯" * 30)
    print("\n Odysseus Wrapper - Demo Suite")
    print("\n" + "🎯" * 30)
    print("\nMake sure Odysseus is running at http://localhost:7000")
    print("Update the API key in demo_basic_chat() if needed.\n")

    try:
        # Run demos (some may fail if Odysseus isn't configured)
        demo_basic_chat()
    except Exception as e:
        print(f"\n⚠️ Demo1 (Chat) failed: {e}")
        print("   Make sure AUTH_ENABLED=true and you have a valid API key.\n")

    try:
        demo_memory()
    except Exception as e:
        print(f"\n⚠️  Demo 5 (Memory) failed: {e}\n")

    try:
        demo_calendar()
    except Exception as e:
        print(f"\n⚠️  Demo 8 (Calendar) failed: {e}\n")

    print("\n" +"🏁" * 30)
    print("\n Demo suite complete!")
    print("\n📚 For more examples, see the README.md")
   print("🌐 https://github.com/q15004040209-creator/odysseus-wrap")


if __name__ == "__main__":
    main()