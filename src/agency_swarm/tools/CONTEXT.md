# tools/ — Tool Base Class and Built-in Tools

## What's Here

Tool base class and all built-in tool implementations. This is the extension point for adding capabilities to agents.

## How Tools Work

All tools are Pydantic models with a `run()` method. The base class handles:
- Schema generation (used by the LLM to know how to call the tool)
- Input validation (Pydantic)
- Execution tracing (hooks integration)

## Key Rules

- Every tool must inherit from the Tool base class.
- `run()` must be synchronous unless explicitly async.
- Tool field descriptions are part of the schema the LLM sees — write them for the model, not for humans.
- Do not add side effects outside `run()` — all tool logic belongs there.
- Tools are stateless — do not store state on the tool instance between calls.
