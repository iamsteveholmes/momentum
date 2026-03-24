# Configuration Gap Detection

Reference document for detecting, classifying, surfacing, and resolving configuration gaps. Loaded by workflow.md at session start and workflow step entry.

---

## Gap Inventory

The minimum configuration gaps Impetus must detect. This list grows as FR9 is exercised in production.

### Protocol Mapping Table (FR35)

**What:** The protocol mapping binds abstract protocol types (e.g., `code-reviewer:review`) to concrete tool invocations. If a workflow step references a protocol type and no binding exists, the step cannot dispatch.

**Detection:** At workflow step entry, if the step dispatches to a protocol-bound tool and the protocol mapping does not include a binding for that protocol type.

**Classification:** Non-blocking unless the step would silently skip a required output.

### MCP Provider

**What:** Some workflow steps require an MCP server (e.g., for file operations, git operations, or external service access). If `.mcp.json` does not configure the required provider, the step will fail.

**Detection:** At session start (scan `.mcp.json` for known required providers) and at workflow step entry (check if the specific step's MCP dependency is satisfied).

**Classification:** Blocking — a missing MCP server required for the next workflow step prevents that step from executing.

### ATDD Tool Binding

**What:** The acceptance test workflow step needs a test runner binding (e.g., which framework runs the Gherkin scenarios). If no binding is configured, test generation can proceed but test execution cannot.

**Detection:** At workflow step entry when the ATDD step fires.

**Classification:** Non-blocking unless the specific step would silently skip output (e.g., test results that feed into a decision gate).

---

## Blocking vs. Non-Blocking Classification

### Blocking Gaps

A gap is blocking when proceeding would cause:
- **Silent output loss** — a required output would be silently skipped, and the developer would not know
- **Step failure** — the next workflow step requires the missing config to execute at all

Blocking gaps halt the workflow at the point of detection. Impetus explains why and guides resolution before proceeding.

### Non-Blocking Gaps

All other gaps are non-blocking. The workflow continues, and Impetus offers resolution when the conversational floor is open (no subagent running, no pending decision).

### Decision Rule

Ask: "If I proceed without this config, will the developer lose output they expect, or will the step silently do nothing?" If yes → blocking. If no → non-blocking.

---

## Detection Timing

### At Session Start

During the orientation phase (integrates with Story 2.2 journal read — same phase, no duplication):

1. Check `installed.json` for component completeness
2. Scan protocol mapping for unbound protocol types that active workflows reference
3. Check `.mcp.json` for required MCP providers
4. Surface any detected gaps using the proactive-offer pattern (non-blocking gaps) or blocking-gap pattern (blocking gaps)

### At Workflow Step Entry

Before executing a workflow step:

1. Check if the step has config dependencies (protocol binding, MCP provider, tool binding)
2. If a dependency is unmet, classify as blocking or non-blocking
3. Blocking: halt and guide resolution
4. Non-blocking: note the gap, continue, offer resolution when the floor is open

---

## Gap Surfacing Format

Never show a raw config file. Always surface gaps conversationally.

### Pattern

```
[What's missing] — clear description
[Why it matters] — impact on the current workflow
[Resolution offer] — targeted question to start filling the gap
```

### Example

```
?  No ATDD tool binding is configured for this project.
   The acceptance test step can generate scenarios, but can't run them without a test runner.
   What test framework does this project use? I'll set up the binding.
```

### Anti-Pattern

```
Your .mcp.json is missing the following configuration:
{
  "servers": {
    "atdd-runner": {
      "command": "...",
      "args": ["..."]
    }
  }
}
Please add this and restart.
```

---

## Resolution Conversation Pattern

When a developer accepts a gap resolution offer, guide them step by step.

### Flow

1. **Ask one targeted question** — "What test framework does this project use?"
2. **Receive the answer** — developer responds naturally
3. **Confirm understanding** — "Got it — I'll configure Jest as the ATDD runner."
4. **Write the config entry** — with developer confirmation before writing
5. **Verify** — confirm the gap is resolved

### Rules

- One question at a time — never present a multi-field form
- Confirm before writing any config file
- If the developer provides partial information, ask a follow-up — don't guess
- If the developer wants to handle it manually, respect that and move on (record as declined offer)

---

## Proactive Offer Integration

Gap detection uses the proactive-offer pattern (UX-DR8):

- Surface with `?` symbol when the conversational floor is open
- Developer can decline — record in journal thread state, do not re-offer (UX-DR8 no-re-offer rule)
- Developer can accept — guide through resolution conversation
- Developer can ignore — follow the developer's lead, do not insist

See `spec-contextualization.md` for the motivated disclosure framing that applies to gap surfacing (why it matters before what's missing).
