"""Interactive CLI for a persistent Letta memory agent."""

from __future__ import annotations

import os
from typing import Any, Iterable

from dotenv import load_dotenv
from letta_client import Letta
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule

try:
    from letta_client.core.api_error import ApiError
except Exception:  # pragma: no cover - keeps older SDKs usable.
    ApiError = Exception  # type: ignore[assignment]


console = Console()

DEFAULT_BASE_URL = "http://localhost:8283"
DEFAULT_AGENT_NAME = "letta-starter-agent"
DEFAULT_MODEL = "openai/Qwen/Qwen3-30B-A3B"
DEFAULT_EMBEDDING = "openai/Qwen/Qwen3-Embedding-8B"


def env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else default


def make_client() -> Letta:
    """Connect to Letta Cloud or a local Letta Docker server."""
    kwargs: dict[str, Any] = {
        "base_url": env("LETTA_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
    }

    api_key = os.getenv("LETTA_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key

    return Letta(**kwargs)


def page_items(page: Any) -> Iterable[Any]:
    return getattr(page, "items", page)


def get_or_create_agent(client: Letta) -> tuple[Any, bool]:
    agent_name = env("LETTA_AGENT_NAME", DEFAULT_AGENT_NAME)

    agents = client.agents.list(name=agent_name, limit=10)
    for agent in page_items(agents):
        if getattr(agent, "name", None) == agent_name:
            return agent, False

    create_kwargs: dict[str, Any] = {
        "name": agent_name,
        "model": env("LETTA_MODEL", DEFAULT_MODEL),
        "memory_blocks": [
            {
                "label": "human",
                "value": (
                    "The human has not shared personal details yet. "
                    "Track useful facts, preferences, goals, and projects here."
                ),
                "limit": 5000,
            },
            {
                "label": "persona",
                "value": (
                    "My name is Sam. I am a concise, friendly Letta starter "
                    "agent that remembers important details across sessions."
                ),
                "limit": 5000,
            },
        ],
    }

    embedding = os.getenv("LETTA_EMBEDDING", DEFAULT_EMBEDDING).strip()
    if embedding:
        create_kwargs["embedding"] = embedding

    return client.agents.create(**create_kwargs), True


def content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("content")
            else:
                text = getattr(item, "text", None) or getattr(item, "content", None)
            if text:
                parts.append(str(text))
        return "\n".join(parts)
    return str(content)


def assistant_reply(response: Any) -> str:
    replies: list[str] = []
    for message in getattr(response, "messages", []):
        if getattr(message, "message_type", None) == "assistant_message":
            text = content_to_text(getattr(message, "content", None)).strip()
            if text:
                replies.append(text)
    return "\n\n".join(replies).strip()


def memory_value(client: Letta, agent_id: str, label: str) -> str:
    block = client.agents.blocks.retrieve(agent_id=agent_id, block_label=label)
    return str(getattr(block, "value", "")).strip()


def show_memory(client: Letta, agent_id: str) -> None:
    console.print(Rule("[bold cyan]Core memory"))
    for label in ("human", "persona"):
        try:
            value = memory_value(client, agent_id, label)
        except ApiError:
            value = "Memory block is not available."
        console.print(Panel(value or "(empty)", title=label, border_style="cyan"))


def print_banner() -> None:
    console.print(
        Panel.fit(
            "[bold]Letta Starter[/bold]\n"
            "A stateful CLI agent with persistent self-editing memory.",
            border_style="cyan",
        )
    )


def run_cli() -> None:
    load_dotenv()
    print_banner()

    try:
        client = make_client()
        agent, created = get_or_create_agent(client)
    except Exception as exc:
        console.print("[bold red]Could not connect to the Letta server.[/bold red]")
        console.print("Start it with [bold]docker compose up -d[/bold], then run again.")
        console.print(f"[dim]{exc}[/dim]")
        raise SystemExit(1) from exc

    status = "created" if created else "loaded"
    console.print(f"[green]Agent {status}:[/green] {agent.name} ({agent.id})")
    show_memory(client, agent.id)

    console.print("\nType your message. Use [bold]exit[/bold] or [bold]quit[/bold] to leave.\n")

    while True:
        try:
            user_text = Prompt.ask("[bold cyan]You[/bold]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit", "/exit", "/quit"}:
            console.print("[dim]Goodbye.[/dim]")
            break

        try:
            response = client.agents.messages.create(
                agent_id=agent.id,
                messages=[{"role": "user", "content": user_text}],
            )
        except Exception as exc:
            console.print("[bold red]Message failed.[/bold red]")
            console.print(f"[dim]{exc}[/dim]")
            continue

        reply = assistant_reply(response)
        console.print(Panel(reply or "(no assistant message returned)", title="Sam", border_style="green"))
        show_memory(client, agent.id)


if __name__ == "__main__":
    run_cli()
