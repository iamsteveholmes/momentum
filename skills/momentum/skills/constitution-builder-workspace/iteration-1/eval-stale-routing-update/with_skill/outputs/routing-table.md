## Quick Routing

Use this table first. Match your situation to a scenario and run the wiki-query before answering.

### Dependency Injection

- **Route depends on database session, auth token, or shared service and you need to wire it cleanly** → `wiki-query FastAPI Depends dependency injection yield scoped resources`
- **Dependency is being called multiple times per request when it should be cached** → `wiki-query quick answer: FastAPI Depends caching use_cache behavior`
- **Need to apply auth or rate-limit to every route in a router without repeating Depends on each function** → `wiki-query FastAPI router-level global dependencies`
- **Service logic coupled to Depends makes it unusable in background workers or CLI scripts** → `wiki-query FastAPI Depends architectural warning service layer coupling`
- **Testing a route that uses Depends — need to mock the dependency without changing app code** → `wiki-query FastAPI dependency_overrides testing pattern`

### Pydantic v2 Models and Validation

- **ValidationError not surfacing to the caller or returning 500 instead of 422** → `wiki-query FastAPI Pydantic v2 RequestValidationError custom error handler`
- **Field validator not running or running at wrong phase — before vs after vs plain mode** → `wiki-query Pydantic v2 field_validator modes before after plain wrap`
- **Cross-field validation needed (e.g. end date must be after start date)** → `wiki-query Pydantic v2 model_validator after mode cross-field`
- **How to wire a Pydantic model as a FastAPI response that strips private fields** → `wiki-query FastAPI response_model Pydantic serialization field exclusion`
- **Migrating from Pydantic v1 class Config to v2 ConfigDict** → `wiki-query quick answer: Pydantic v1 to v2 migration ConfigDict validator decorator changes`
- **Validating a type that is not a BaseModel subclass (e.g. list[int] from a raw payload)** → `wiki-query Pydantic v2 TypeAdapter validate_python non-model types`
- **Need context-aware validation — validator needs to know allowed roles or tenant at runtime** → `wiki-query Pydantic v2 validation context ValidationInfo model_validate context`

### Async Routing and Execution Model

- **Accidentally blocking the event loop inside an async def route** → `wiki-query FastAPI async def blocking operations run_in_threadpool`
- **Sync SDK call inside an async route causing hangs or latency spikes** → `wiki-query FastAPI run_in_threadpool Starlette concurrency blocking inside async`
- **How to organize routes across multiple files without circular imports** → `wiki-query FastAPI APIRouter include_router multi-file structure`

### PydanticAI Agent Integration

- **How to call a PydanticAI agent from a FastAPI route handler** → `wiki-query PydanticAI agent run async FastAPI route integration lifespan`
- **Agent needs access to the HTTP client or DB session from FastAPI's dependency system — how to bridge Depends into RunContext** → `wiki-query RunContext dependency injection dataclass deps agent.run`
- **Agent should share a singleton HTTP client across all requests — how to initialize and close it properly** → `wiki-query FastAPI lifespan asynccontextmanager app.state agent initialization`
- **How to register a function as an LLM-callable tool with automatic schema from docstring** → `wiki-query PydanticAI agent.tool decorator schema docstring RunContext`
- **Tool needs to signal the model to retry with corrected arguments** → `wiki-query PydanticAI ModelRetry tool retry mechanism`
- **Tool does not need dependencies — simpler registration path** → `wiki-query quick answer: PydanticAI agent.tool_plain decorator without RunContext`

### Async Agent Calls and Streaming

- **Streaming PydanticAI agent output token-by-token to a browser via SSE** → `wiki-query PydanticAI run_stream EventSourceResponse FastAPI SSE integration`
- **Agent stops executing tools after first structured output match** → `wiki-query PydanticAI run_stream stop-at-first-output behavior agent.iter full execution`
- **Need step-by-step visibility into agent graph nodes (ModelRequestNode, CallToolsNode) during a request** → `wiki-query PydanticAI agent.iter node-by-node graph traversal UserPromptNode CallToolsNode`
- **FastAPI SSE endpoint drops connection through Nginx — events are buffered** → `wiki-query FastAPI SSE X-Accel-Buffering nginx proxy buffering EventSourceResponse`
- **Need typed SSE events serialized on the Rust side for performance** → `wiki-query FastAPI native SSE EventSourceResponse Rust-side Pydantic serialization 0.135`

### Structured Agent Output

- **Agent should return a Pydantic model instead of raw text — how to declare and enforce output type** → `wiki-query PydanticAI output_type structured output BaseModel ToolOutput`
- **Agent returns wrong structured type or validation fails silently** → `wiki-query PydanticAI output_validator ModelRetry structured output validation stages`
- **Streaming partial structured output as fields are populated** → `wiki-query PydanticAI run_stream stream_output partial structured data`
- **Which output mode to use — ToolOutput vs NativeOutput vs PromptedOutput** → `wiki-query quick answer: PydanticAI output modes ToolOutput NativeOutput PromptedOutput decision`

### System Prompts and Model Configuration

- **Dynamic system prompt needs user context from the database at request time** → `wiki-query PydanticAI dynamic system prompt agent.system_prompt decorator RunContext`
- **Static and dynamic prompts combine in wrong order** → `wiki-query quick answer: PydanticAI system prompt ordering static dynamic combination`
- **Need to tune temperature or max_tokens per request without changing agent definition** → `wiki-query PydanticAI ModelSettings three-level precedence runtime override`

### Testing Agents

- **Unit-testing a tool without making real LLM API calls** → `wiki-query PydanticAI TestModel agent.override unit testing tools`
- **Test needs to verify a specific tool was called with specific arguments** → `wiki-query PydanticAI FunctionModel ToolCallPart conditional tool invocation testing`
- **Accidentally making real LLM calls in CI — how to guard against it** → `wiki-query PydanticAI ALLOW_MODEL_REQUESTS guard conftest pytest`
- **`agent.run_sync()` raises "event loop is already running" inside pytest-asyncio test** → `wiki-query PydanticAI run_sync vs await agent.run pytest-asyncio event loop conflict`
- **Tool mock dep not visible inside tool when asyncio.create_task is used** → `wiki-query PydanticAI agent.override contextvar propagation asyncio create_task`
