# Background Agent Coordination — Research Findings

Story 2.10 | Date: 2026-03-24 | Agent Model: claude-opus-4-6

This document satisfies the Architecture Decision 4c gate: "Do not implement productive waiting or background VFL execution until spike result is documented."

## Mechanism Investigated

Four potential inter-agent communication mechanisms were investigated for Claude Code:

1. **`Agent` tool** — A tool that spawns a subagent with its own context and returns structured results. Referenced in Claude Code documentation and Momentum architecture as the `context:fork` pattern.
2. **`SendMessage` tool** — A hypothetical tool for sending messages to a running agent by ID, enabling checkpoint/resume mid-task. Referenced in the original Story 2.Spike definition.
3. **`run_in_background: true` on the `Bash` tool** — A parameter that runs a shell command in the background, returning a task ID and output file path. The caller is not blocked and can continue issuing other tool calls.
4. **`TaskOutput`** — A hypothetical tool for reading structured output from a background task.

## Test Methodology

All tests were executed live within a Claude Code CLI session (claude-opus-4-6 model) on 2026-03-24. The environment was a standard Claude Code session with the default tool set plus deferred tools loaded via `ToolSearch`.

### Test 1: Tool Existence Discovery

Used `ToolSearch` to search for `Agent`, `SendMessage`, `subagent`, `spawn`, `fork`, and related keywords. Searched both exact names (`select:Agent`) and keyword queries.

### Test 2: Background Bash Execution

Ran a Bash command with `run_in_background: true`:
```
echo "Background task started" && sleep 2 && echo "Result: {\"status\": \"complete\"}"
```
Observed the return value (task ID + output file path) and read the output file after completion.

### Test 3: Concurrent Background Tasks

Launched two background Bash commands simultaneously — one sleeping 3 seconds (Task A), one sleeping 1 second (Task B). Verified both ran concurrently and completed independently.

### Test 4: Mid-Task Communication (Checkpoint/Resume)

Created a named pipe (`mkfifo`) and launched a background task that blocked on reading the pipe. From a separate Bash call, wrote data to the pipe. Verified the background task received the data and continued.

### Test 5: Deferred Tool Registry Scan

Searched the deferred tool registry for any tools related to agents, messaging, or background task management. Catalogued all available tools.

## Results

### Finding 1: No `Agent` Tool Exists in This Environment

`ToolSearch` for `Agent`, `subagent`, `spawn`, and `fork` returned no matching tools. The `Agent` tool referenced in Claude Code Skills documentation (the `context:fork` mechanism) is **not available as a callable tool in the current Claude Code CLI session**. This means the architecture's assumption that "Claude Code subagents explicitly support foreground/background modes" refers to a capability that is either:
- Available only in specific Claude Code configurations (e.g., with Skills installed that define `context:fork` subagents)
- A planned but not-yet-shipped feature
- Available only through the Skills framework's SKILL.md `context:fork` declarations, not as a general-purpose tool

**Implication:** There is no way to spawn an autonomous subagent with its own context window from within a Claude Code session using a built-in tool.

### Finding 2: No `SendMessage` Tool Exists

`SendMessage` does not exist in any form — not as a loaded tool, not as a deferred tool, not discoverable via any keyword search. The original spike definition's premise ("Validate that the SendMessage API reliably supports background agent checkpoint/resume") is based on a mechanism that does not exist in Claude Code.

**Implication:** Mid-task checkpoint/resume via an API-level messaging mechanism is not possible. There is no way to send structured data to a running agent or background task through Claude Code's tool system.

### Finding 3: `run_in_background: true` on Bash Works Reliably

The Bash tool's `run_in_background` parameter is the **only built-in mechanism** for background execution. Behavior:

| Aspect | Observed Behavior |
|---|---|
| Return value | Immediate: `{task_id, output_file_path}` |
| Output location | `/private/tmp/claude-{uid}/.../tasks/{task_id}.output` |
| Concurrency | Multiple background tasks run simultaneously |
| Output reading | File is readable via `Read` tool or `cat` after task completes |
| Blocking | Caller is NOT blocked — can issue other tool calls immediately |
| Mid-task input | Not supported via tool API; possible only via OS-level workarounds (named pipes) |
| Notification | Claude Code notifies the session when a background task completes |

### Finding 4: No `TaskOutput` Tool Exists as Described

There is no dedicated `TaskOutput` tool. The output of a background Bash task is simply a file on disk at the path returned when the task was launched. Reading it requires `Read` or `cat` — there is no structured API for querying task status or output.

### Finding 5: OS-Level Workarounds Are Possible but Not Practical

Named pipes (`mkfifo`) can bridge data between a foreground Bash call and a background Bash process. However, this is:
- Fragile (pipe lifecycle management, blocking semantics)
- Not integrated with Claude Code's tool system (no notification, no structured data)
- Limited to shell processes — cannot communicate with an agent's reasoning context
- Not a viable foundation for checkpoint/resume in a production workflow

### Finding 6: `context:fork` Is a Skills Framework Concept, Not a Tool

The `context:fork` pattern referenced in Momentum's architecture is a **Skills framework declaration** in SKILL.md files. It defines that a skill step should run in a subagent with isolated context. The Skills runtime (not the agent itself) manages the fork. This means:
- The orchestrating agent (Impetus) cannot programmatically spawn a subagent via a tool call
- Subagent execution is declared statically in SKILL.md, not dynamically dispatched
- The subagent runs to completion and returns its result — there is no mid-execution communication channel
- The orchestrating agent receives the subagent's final output, not intermediate checkpoints

## Constraints and Failure Modes

### Constraint 1: Fire-and-Forget Only

Background execution in Claude Code follows a **fire-and-forget model**. Once a background Bash command is launched:
- No input can be sent to it through the tool API
- No progress can be queried until it completes
- The only signal is the completion notification + output file

### Constraint 2: Background Tasks Are Shell Commands, Not Agents

`run_in_background` runs a **shell command**, not an agent with reasoning capabilities. A background task cannot:
- Make tool calls
- Read files intelligently
- Reason about intermediate results
- Adapt its behavior based on new information

This is fundamentally different from the architecture's vision of "background agents" that can run multi-step story implementations.

### Constraint 3: No Structured Return Contract

Background task output is raw text written to a file. There is no structured JSON return contract, no status field, no error handling framework. The orchestrating agent must parse raw output and infer success/failure.

### Constraint 4: `context:fork` Subagents Run to Completion

When a SKILL.md step uses `context:fork`, the subagent:
- Gets its own context window (isolated from the main conversation)
- Runs to completion (all steps in the forked context)
- Returns its final output to the orchestrating agent
- Cannot be paused, resumed, or checkpointed mid-execution

### Failure Mode: Dead Air During Subagent Execution

If a `context:fork` subagent runs as a foreground operation (the default), the main conversation is blocked until it completes. This creates the "dead air" failure mode that Decision 4c identifies. The mitigation is behavioral, not mechanical — Impetus should provide context and expectations before launching the subagent, then process results when it returns.

### Failure Mode: Background Task Silent Failure

If a `run_in_background` Bash task fails (non-zero exit, crash, timeout), the only evidence is in the output file. There is no structured error notification. The orchestrating agent must explicitly check the output file and handle failures.

## Recommendation for Story 4.3

### Revised Architecture Pattern: Declared Subagents + Behavioral Productive Waiting

The checkpoint/resume pattern envisioned in the original architecture is **not implementable** with current Claude Code capabilities. Neither `SendMessage` nor any equivalent inter-agent messaging mechanism exists. The recommended pattern for Story 4.3 is:

#### 1. Use `context:fork` for Subagent Isolation (Not Background Execution)

Subagents declared via `context:fork` in SKILL.md provide the isolation needed for story implementation. However, they run as foreground operations — the orchestrating agent waits for their completion.

#### 2. Productive Waiting Is Behavioral, Not Mechanical

Since the orchestrating agent cannot maintain a parallel conversation while a subagent runs (there is no background agent mechanism), "productive waiting" must be redefined:

- **Before subagent launch:** Impetus previews what the subagent will do, sets expectations for duration, summarizes the plan
- **After subagent returns:** Impetus synthesizes results, maps to ACs, identifies issues
- **Dead air mitigation:** Keep subagent tasks small enough that wait times are manageable (seconds to low minutes, not extended periods)

#### 3. Background Bash for Non-Reasoning Tasks Only

`run_in_background: true` on Bash is appropriate for:
- Running tests in the background while the agent continues conversation
- Linting or formatting operations
- File system operations that take time

It is NOT appropriate for tasks that require agent reasoning (code generation, analysis, decision-making).

#### 4. Revised Decision 4c Guidance

Replace the checkpoint/resume aspiration with:
- Subagent tasks should be decomposed into small, completable units
- Impetus maintains engagement through pre-launch briefing and post-completion synthesis
- Background Bash handles mechanical tasks (test runs, builds) while Impetus converses
- No mid-task communication with subagents — design workflows to not require it

#### 5. Impact on Story 4.3 Implementation

Story 4.3 (full story cycle with background agents) should:
- Use `context:fork` subagents for implementation steps (each step runs to completion)
- Use `run_in_background` Bash for test execution and build steps
- Not attempt checkpoint/resume — instead, decompose work into discrete subagent invocations
- Implement productive waiting as behavioral skill instructions (what Impetus says before/after), not as a runtime mechanism
