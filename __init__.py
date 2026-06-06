"""
Odysseus Wrapper
A Pythonic interface for the Odysseus self-hosted AI workspace.

Usage:
    from odysseus import OdysseusClient

    client = OdysseusClient(base_url="http://localhost:7000", api_key="your-key")
    response = client.chat.send_message("Hello!")
"""

__version__ = "0.1.0"
__author__ = "q15004040209-creator"
__license__ = "MIT"

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import urllib.request
import urllib.error
import json


@dataclass
class ChatResponse:
    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


@dataclass
class MemoryResult:
    id: str
    content: str
    score: float
    tags: List[str]
    metadata: Dict[str, Any]


@dataclass
class Event:
    id: str
    title: str
    start: datetime
    end: datetime
    description: str
    calendar_id: str


@dataclass
class Email:
    id: str
    subject: str
    from_: str
    to: str
    date: datetime
    body: str
    is_read: bool


class OdysseusClient:
    """Python client for Odysseus AI workspace."""

    def __init__(
        self,
        base_url: str = "http://localhost:7000",
        api_key: Optional[str] = None,
        timeout: int = 120,
        verify_ssl: bool = True
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self._session_token = None

        if api_key:
            self._authenticate()

    def _authenticate(self):
        """Authenticate and get session token."""
        import urllib.request, urllib.error, json
        data = json.dumps({"username": "admin", "password": self.api_key}).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/auth/login",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            self._session_token = json.loads(resp.read())["access_token"]
        except Exception:
            pass  # Will fall back to API key auth

    def _request(self, method: str, path: str, data: Optional[Dict] = None):
        """Make an HTTP request to Odysseus."""
        import urllib.request, urllib.error, json
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}
        if self._session_token:
            headers["Authorization"] = f"Bearer {self._session_token}"
        elif self.api_key:
            headers["X-API-Key"] = self.api_key

        req = urllib.request.Request(url, headers=headers, method=method)
        if data:
            req.data = json.dumps(data).encode()

        try:
            resp = urllib.request.urlopen(req, timeout=self.timeout)
            return json.loads(resp.read()) if resp.read() else {}
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.read().decode()}"}
        except Exception as e:
            return {"error": str(e)}

    @property
    def chat(self):
        return ChatInterface(self)

    @property
    def agent(self):
        return AgentInterface(self)

    @property
    def research(self):
        return ResearchInterface(self)

    @property
    def memory(self):
        return MemoryInterface(self)

    @property
    def documents(self):
        return DocumentsInterface(self)

    @property
    def email(self):
        return EmailInterface(self)

    @property
    def calendar(self):
        return CalendarInterface(self)

    @property
    def skills(self):
        return SkillsInterface(self)


class ChatInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def send_message(
        self,
        prompt: str,
        model: str = "openai/gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> ChatResponse:
        data = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        result = self._client._request("POST", "/api/chat", data)
        return ChatResponse(
            content=result.get("content", result.get("error", "No response")),
            model=model,
            usage=result.get("usage", {}),
            finish_reason=result.get("finish_reason", "stop")
        )

    def create_conversation(self, model: str = "openai/gpt-4o"):
        return Conversation(self._client, model=model)


class Conversation:
    def __init__(self, client: OdysseusClient, model: str):
        self._client = client
        self.model = model
        self.history: List[Dict] = []

    def send_message(self, prompt: str, **kwargs) -> ChatResponse:
        response = self._client.chat.send_message(prompt, model=self.model, **kwargs)
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response.content})
        return response

    def get_history(self) -> List[Dict]:
        return self.history.copy()


class AgentInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def run(
        self,
        task: str,
        tools: List[str] = None,
        model: str = "openai/gpt-4o",
        max_steps: int = 10,
        **kwargs
    ):
        data = {
            "task": task,
            "model": model,
            "max_steps": max_steps,
            "tools": tools or ["shell", "memory"],
            **kwargs
        }
        result = self._client._request("POST", "/api/agent/run", data)
        return AgentResult(
            final_response=result.get("response", result.get("error", "")),
            steps=result.get("steps", max_steps),
            tools_used=result.get("tools_used", [])
        )


@dataclass
class AgentResult:
    final_response: str
    steps: int
    tools_used: List[str]


class ResearchInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def run(self, topic: str, depth: str = "standard", sources: List[str] = None):
        data = {
            "topic": topic,
            "depth": depth,
            "sources": sources or ["web"]
        }
        result = self._client._request("POST", "/api/research", data)
        return ResearchReport(
            title=result.get("title", topic),
            sections=result.get("sections", []),
            markdown=result.get("markdown", f"# {topic}\n\n{result.get('content', '')}"),
            sources=result.get("sources", [])
        )


@dataclass
class ResearchReport:
    title: str
    sections: List[Dict]
    markdown: str
    sources: List[str]


class MemoryInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def add(self, content: str, tags: List[str] = None, metadata: Dict = None):
        data = {
            "content": content,
            "tags": tags or [],
            "metadata": metadata or {}
        }
        return self._client._request("POST", "/api/memory", data)

    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Dict = None,
        **kwargs
    ) -> List[MemoryResult]:
        data = {"query": query, "limit": limit, "filters": filters or {}, **kwargs}
        result = self._client._request("POST", "/api/memory/search", data)
        items = result.get("results", result.get("error", []))
        if isinstance(items, str):
            return []
        return [
            MemoryResult(
                id=r.get("id", ""),
                content=r.get("content", ""),
                score=r.get("score", 0.0),
                tags=r.get("tags", []),
                metadata=r.get("metadata", {})
            )
            for r in items
        ]

    def list(self, limit: int = 50) -> List[MemoryResult]:
        result = self._client._request("GET", f"/api/memory?limit={limit}")
        items = result.get("items", result.get("error", []))
        if isinstance(items, str):
            return []
        return [MemoryResult(id=i.get("id", ""), content=i.get("content", ""),
                             score=1.0, tags=i.get("tags", []),
                             metadata=i.get("metadata", {})) for i in items]


class DocumentsInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def create(self, title: str, content: str, format: str = "markdown"):
        data = {"title": title, "content": content, "format": format}
        result = self._client._request("POST", "/api/documents", data)
        return Document(
            id=result.get("id", ""),
            title=title,
            content=content,
            format=format
        )

    def get_suggestions(self, doc_id: str):
        result = self._client._request("GET", f"/api/documents/{doc_id}/suggestions")
        suggestions = result.get("suggestions", result.get("error", []))
        if isinstance(suggestions, str):
            return []
        return [Suggestion(s.get("id", ""), s.get("line", 0), s.get("text", ""))
                for s in suggestions]

    def apply_suggestion(self, doc_id: str, suggestion_id: str):
        return self._client._request("POST", f"/api/documents/{doc_id}/suggestions/{suggestion_id}/apply")


@dataclass
class Document:
    id: str
    title: str
    content: str
    format: str


@dataclass
class Suggestion:
    id: str
    line: int
    suggestion: str


class EmailInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def list(self, folder: str = "INBOX", unread_only: bool = False, limit: int = 20):
        params = f"?folder={folder}&unread_only={unread_only}&limit={limit}"
        result = self._client._request("GET", f"/api/email/list{params}")
        emails = result.get("emails", result.get("error", []))
        if isinstance(emails, str):
            return []
        return [
            Email(
                id=e.get("id", ""),
                subject=e.get("subject", ""),
                from_=e.get("from", ""),
                to=e.get("to", ""),
                date=datetime.fromisoformat(e.get("date", "2026-01-01")),
                body=e.get("body", ""),
                is_read=e.get("is_read", False)
            )
            for e in emails
        ]

    def send(self, to: str, subject: str, body: str, draft: bool = False):
        data = {"to": to, "subject": subject, "body": body, "draft": draft}
        result = self._client._request("POST", "/api/email/send", data)
        return EmailDraft(id=result.get("id", ""), to=to, subject=subject)

    def triage(self, folder: str = "INBOX", strategy: str = "urgency"):
        result = self._client._request("POST", "/api/email/triage", {"folder": folder, "strategy": strategy})
        return TriageResult(
            urgent=result.get("urgent", []),
            action_required=result.get("action_required", []),
            can_wait=result.get("can_wait", [])
        )


@dataclass
class EmailDraft:
    id: str
    to: str
    subject: str


@dataclass
class TriageResult:
    urgent: List[Email]
    action_required: List[Email]
    can_wait: List[Email]


class CalendarInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def list_calendars(self):
        result = self._client._request("GET", "/api/calendar/calendars")
        cals = result.get("calendars", result.get("error", []))
        if isinstance(cals, str):
            return []
        return [Calendar(c.get("id", ""), c.get("name", ""), c.get("color", "#000"))
                for c in cals]

    def list(self, start: str, end: str, calendar_ids: List[str] = None):
        params = f"?start={start}&end={end}"
        if calendar_ids:
            params += f"&calendar_ids={','.join(calendar_ids)}"
        result = self._client._request("GET", f"/api/calendar/events{params}")
        events = result.get("events", result.get("error", []))
        if isinstance(events, str):
            return []
        return [
            Event(
                id=e.get("id", ""),
                title=e.get("title", ""),
                start=datetime.fromisoformat(e.get("start", "2026-01-01T00:00:00")),
                end=datetime.fromisoformat(e.get("end", "2026-01-01T00:00:00")),
                description=e.get("description", ""),
                calendar_id=e.get("calendar_id", "")
            )
            for e in events
        ]

    def create(self, title: str, start: str, end: str, description: str = "", calendar_id: str = None):
        data = {"title": title, "start": start, "end": end,
                "description": description, "calendar_id": calendar_id}
        result = self._client._request("POST", "/api/calendar/events", data)
        return Event(
            id=result.get("id", ""),
            title=title,
            start=datetime.fromisoformat(start),
            end=datetime.fromisoformat(end),
            description=description,
            calendar_id=calendar_id or ""
        )


@dataclass
class Calendar:
    id: str
    name: str
    color: str


class SkillsInterface:
    def __init__(self, client: OdysseusClient):
        self._client = client

    def list(self):
        result = self._client._request("GET", "/api/skills")
        skills = result.get("skills", result.get("error", []))
        if isinstance(skills, str):
            return []
        return [Skill(s.get("name", ""), s.get("description", ""), s.get("enabled", True))
                for s in skills]


@dataclass
class Skill:
    name: str
    description: str
    enabled: bool