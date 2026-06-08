# src/ — BEAM-OS Source (agency_swarm)

## DOX Protocol
Read this file and the relevant subdirectory CONTEXT.md before making any change.
After editing, update the CONTEXT.md for any directory you modified.
Root `CONTEXT.md` is the formal agent instruction contract — read it first for mandate and policy rules.

---

## What's Here

The BEAM-OS Python framework — a fork of OpenSwarm (MIT). Packages as `agency_swarm`. Provides the multi-agent orchestration layer for BEAM-OS: Agent, Agency, Tools, and communication protocol.

## Directory Map

```
src/agency_swarm/
  agency/         — Agency class: orchestrates multiple agents, manages communication threads
  agent/          — Agent base class: wraps model, tools, instructions, memory
  agents/         — Pre-built agent implementations (reusable agent types)
  cli/            — CLI entry point (agency-swarm command)
  tools/          — Tool base class + built-in tool implementations
  messages/       — Message handling, thread management
  streaming/      — Streaming response support
  integrations/   — Third-party integrations (FastAPI, etc.)
  ui/             — Gradio/web UI components
  utils/          — Shared utilities
  context.py      — Shared context management across agents
  hooks.py        — Lifecycle hooks (before/after tool call, message, etc.)
  __init__.py     — Public API surface
```

## Key Architecture Rules

- **Agency** = the unit of deployment. It contains 2+ agents and defines their communication graph (who can send to whom).
- **Agent** = an LLM + tools + instructions. Agents do not call each other directly — they communicate through the Agency's message-passing layer.
- **Tools** inherit from the Tool base class in `tools/`. All tools are Pydantic models with a `run()` method.
- `context.py` is the shared state bus — agents read/write shared context here, not via direct references.
- `hooks.py` intercepts the execution lifecycle — use for logging, validation, guardrails. Do not add business logic here.

## Entry Points

- `run/setup.sh` — environment setup
- `src/agency_swarm/cli/` — `agency-swarm` CLI
- `examples/` — reference implementations (do not modify; use as read-only reference)
