"""
Phase 0 proof — port `recall` skill to agency-swarm spine.

Wraps Cornelius's local-brain-search via subprocess + spins up a one-agent Agency.
Success criterion: same FAISS hits as `/recall` in Claude Code.
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any

from agency_swarm import Agency, Agent, RunContextWrapper, function_tool

CORNELIUS_ROOT = Path(r"C:\Users\Chad\Documents\cornelius")
BRAIN_SEARCH = CORNELIUS_ROOT / "resources" / "local-brain-search"
VENV_PYTHON = BRAIN_SEARCH / "venv" / "Scripts" / "python.exe"
SEARCH_PY = BRAIN_SEARCH / "search.py"
CONNECTIONS_PY = BRAIN_SEARCH / "connections.py"


@function_tool()
async def vault_search(
    wrapper: RunContextWrapper[Any],
    query: str,
    mode: str = "spreading",
    limit: int = 5,
) -> str:
    """Search Chad's Obsidian vault using FAISS semantic search.

    Args:
        query: The search query
        mode: 'spreading' (graph-aware, recommended) or 'static' (pure vector)
        limit: Max results (default 5)
    """
    result = subprocess.run(
        [
            str(VENV_PYTHON),
            str(SEARCH_PY),
            query,
            "--mode", mode,
            "--limit", str(limit),
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return f"Search failed: {result.stderr}"
    try:
        data = json.loads(result.stdout)
        results = data.get("results", [])
        if not results:
            return "No results."
        summary = []
        for r in results[:limit]:
            score = r.get("activation", r.get("similarity", 0))
            label = "activation" if "activation" in r else "similarity"
            title = r.get("title", "Untitled")
            path = r.get("filepath", "")
            summary.append(f"[{score:.1%} {label}] {title}\n  {path}")
        return "\n".join(summary)
    except json.JSONDecodeError:
        return f"Could not parse JSON. Raw output:\n{result.stdout[:500]}"


@function_tool()
async def vault_connections(
    wrapper: RunContextWrapper[Any],
    note_name: str,
) -> str:
    """Find direct connections (linked notes) for a given vault note.

    Args:
        note_name: Exact note title (e.g. 'BEAM-OS Master Plan v2')
    """
    result = subprocess.run(
        [
            str(VENV_PYTHON),
            str(CONNECTIONS_PY),
            note_name,
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return f"Connections lookup failed: {result.stderr}"
    try:
        data = json.loads(result.stdout)
        connections = data.get("connections", [])
        if not connections:
            return f"No connections found for '{note_name}'."
        return "\n".join(f"- {c.get('title', c)}" for c in connections[:10])
    except json.JSONDecodeError:
        return f"Raw output:\n{result.stdout[:500]}"


recall_agent = Agent(
    name="RecallSpecialist",
    description="Searches Chad's Obsidian knowledge vault using semantic FAISS search and graph connections.",
    instructions=(
        "You are the Recall specialist. When asked about Chad's notes, thinking, or vault content, "
        "use vault_search first (mode='spreading' by default). For follow-up depth on the top hit, "
        "use vault_connections. Return a clean summary with note titles, scores, and paths. "
        "Do not invent content — only report what the tools return."
    ),
    tools=[vault_search, vault_connections],
)

agency = Agency(recall_agent)


async def main():
    query = "What is BEAM-OS and why fork agency-swarm?"
    print(f"\n=== Query: {query} ===\n")
    response = await agency.get_response(query)
    print(response.final_output)


if __name__ == "__main__":
    asyncio.run(main())
