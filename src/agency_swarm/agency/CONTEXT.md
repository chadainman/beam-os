# agency/ — Agency Orchestration Layer

## What's Here

The `Agency` class — the top-level unit of deployment. Defines the agent communication graph and manages the shared thread/message infrastructure.

## Key Responsibilities

- Instantiates and wires together multiple agents
- Defines communication flows (which agents can message which)
- Manages the shared message thread between agents
- Provides the entry point for user interaction (`agency.get_completion()`)

## Key Rules

- The communication graph is defined at Agency construction time — you cannot add new communication paths at runtime.
- Agents in an Agency share a thread context but have separate instruction sets and tool sets.
- Do not add business logic to Agency — it is an orchestration container, not a domain object.
- Changes to the message-passing protocol here affect ALL agent communication — test thoroughly before modifying.
