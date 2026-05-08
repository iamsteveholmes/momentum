## Quick Routing

### FastAPI — Dependency Injection

| Symptom | Query |
|---|---|
| "How do I inject a database session / shared resource into route handlers?" | `wiki-query FastAPI dependency injection patterns` |
| "My Depends() dependency is being re-evaluated on every request — how do I cache it?" | `wiki-query FastAPI Depends caching use_cache yield class-based` |
| "How do I override a dependency in tests?" | `wiki-query FastAPI dependency override testing` |
| "I want a sub-dependency or chained Depends() — how does that work?" | `wiki-query FastAPI sub-dependencies Depends chaining` |

### FastAPI — Routing and Async Execution

| Symptom | Query |
|---|---|
| "My sync route handler is blocking the event loop — do I need async def?" | `wiki-query FastAPI async vs sync route execution threadpool` |
| "How do I structure a large FastAPI app with multiple routers?" | `wiki-query FastAPI application structure APIRouter multi-file` |
| "Route is returning a 422 Unprocessable Entity from Pydantic — how do I customize the error?" | `wiki-query FastAPI error handling RequestValidationError HTTPException` |
| "How do I stream a response from a FastAPI route?" | `wiki-query FastAPI streaming responses SSE server-sent events` |

### FastAPI — Lifecycle and Middleware

| Symptom | Query |
|---|---|
| "How do I run startup/shutdown code — lifespan vs on_event?" | `wiki-query FastAPI lifespan context manager app.state startup` |
| "How do I add middleware and in what order does it execute?" | `wiki-query FastAPI middleware BaseHTTPMiddleware execution order` |
| "I need to run a background job after returning the HTTP response." | `wiki-query FastAPI background tasks BackgroundTasks add_task` |
| "How do I load settings from environment variables in FastAPI?" | `wiki-query FastAPI settings pydantic-settings BaseSettings Depends` |

### Pydantic v2 — Models and Validation

| Symptom | Query |
|---|---|
| "How do I write a custom field validator in Pydantic v2?" | `wiki-query Pydantic v2 field_validator model_validator ConfigDict` |
| "I'm migrating from Pydantic v1 — what changed and how do I use bump-pydantic?" | `wiki-query Pydantic v1 to v2 migration bump-pydantic API changes` |
| "How do I validate or parse a type without a full model — TypeAdapter?" | `wiki-query Pydantic v2 TypeAdapter parse validate` |
| "How do I control JSON serialization output (aliases, by_alias, exclude)?" | `wiki-query Pydantic v2 serialization model_serializer ConfigDict` |

### PydanticAI — Agent and Tool Definition

| Symptom | Query |
|---|---|
| "How do I register a tool on a PydanticAI agent?" | `wiki-query PydanticAI tool registration @agent.tool docstring schema` |
| "How do I pass shared dependencies (DB, config) into my agent tools at runtime?" | `wiki-query PydanticAI RunContext dependency injection deps` |
| "Agent tool raised a validation error and I want to retry the model — how?" | `wiki-query PydanticAI ModelRetry @agent.tool_plain` |
| "How do I give my agent a system prompt, and can it be dynamic?" | `wiki-query PydanticAI system prompts static dynamic @agent.system_prompt` |

### PydanticAI — Structured Output and Streaming

| Symptom | Query |
|---|---|
| "How do I make my agent return a structured Pydantic model instead of plain text?" | `wiki-query PydanticAI structured output output_type ToolOutput NativeOutput` |
| "How do I stream tokens from a PydanticAI agent?" | `wiki-query PydanticAI streaming run_stream agent.iter StreamedRunResult` |
| "How do I compose multiple tools into a reusable toolset?" | `wiki-query PydanticAI Toolsets AbstractToolset FunctionToolset MCPServer` |

### PydanticAI — Testing and Evaluation

| Symptom | Query |
|---|---|
| "How do I unit-test a PydanticAI agent without hitting the real LLM?" | `wiki-query PydanticAI TestModel FunctionModel ALLOW_MODEL_REQUESTS` |
| "How do I run agent tests alongside pytest-asyncio fixtures without event loop conflicts?" | `wiki-query PydanticAI TestModel pytest-asyncio agent.override event loop` |
| "How do I build an evaluation dataset and score agent outputs with an LLM judge?" | `wiki-query PydanticAI pydantic-evals Dataset Case Evaluator LLMJudge` |

### PydanticAI — Model Configuration

| Symptom | Query |
|---|---|
| "How do I set temperature, max_tokens, or thinking mode for a PydanticAI agent?" | `wiki-query PydanticAI ModelSettings temperature max_tokens precedence` |
| "How do I switch between Haiku, Sonnet, and Opus per call in PydanticAI?" | `wiki-query PydanticAI model configuration model selection per-run` |

### Cross-cutting — FastAPI + PydanticAI Integration

| Symptom | Query |
|---|---|
| "How do I wire a PydanticAI agent into a FastAPI route with streaming SSE output?" | `wiki-query FastAPI SSE streaming PydanticAI agent run_stream` |
| "How do I inject the same dependencies into both my FastAPI Depends chain and my agent RunContext?" | `wiki-query PydanticAI RunContext FastAPI Depends dependency injection shared` |
