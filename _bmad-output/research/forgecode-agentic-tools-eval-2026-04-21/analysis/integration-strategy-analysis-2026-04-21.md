---
title: "Integration Strategy Analysis — ForgeCode / OpenCode / Goose / JetBrains Air vs Momentum"
date: 2026-04-21
type: Strategic Analysis
status: Complete
content_origin: claude-code-analysis
human_verified: true
derives_from:
  - path: final/forgecode-agentic-tools-eval-final-2026-04-21.md
    relationship: extends
  - path: raw/followup-jetbrains-integration-licensing.md
    relationship: extends
  - path: raw/practitioner-notes.md
    relationship: informed_by
supplements: research/forgecode-agentic-tools-eval-2026-04-21
---

# Integration Strategy Analysis — ForgeCode / OpenCode / Goose / JetBrains Air vs Momentum

This analysis extends the consolidated research report with a focused exploration of three strategic questions the developer surfaced post-synthesis:

1. **Is MCP integration actually valuable, or is process isolation sufficient?**
2. **Does Goose have deterministic behaviors or events, and how do they compare to hooks?**
3. **Could CMUX act as the integration substrate instead of MCP?**

The analysis resolves with a revised three-layer integration strategy that treats CMUX as Momentum's primary integration substrate, with MCP reserved for the narrow cases where autonomous inline dispatch is required.

## 1. Process Isolation Beats MCP Integration for Momentum

### The initial framing (walked back)

The final research report recommended MCP integrations (`opencode-mcp`, AgentAPI-wrapped Goose) as the cleanest path for Claude Code to call other agentic tools as subagents. That framing undersold the value of a simpler architecture: **run each tool in its own cmux workspace with git-worktree isolation, and let the human orchestrate across them.**

### Why process-isolation is structurally better for Momentum

- **Respects Momentum's "visible to the developer" principle.** Every tool runs in its own pane; no hidden sub-process dispatch.
- **Zero integration shims to maintain.** Each tool runs natively with its own model, its own loop, its own UI. No MCP wrapper configuration to keep in sync with upstream.
- **Clearer failure modes.** If OpenCode breaks, Claude Code is untouched; no MCP tool surface to debug.
- **Preserves each tool's full capability surface.** MCP exposure of OpenCode flattens its 25+ plugin events and client/server architecture into a function-call interface. Native execution in a pane retains the full capability surface.
- **Natural git discipline.** Worktree per tool per story. Coordination happens through the filesystem and through pull requests the human reviews.

### Where MCP's unique value actually lives

MCP integration is worth the cost **only** when you need:

- **Autonomous inline dispatch**: Claude Code programmatically decides *during its own loop* to invoke another tool and read the result back into its context window for a real-time decision.
- **Structured return values in Claude Code's context**: the invoking agent reads the returned output and acts on it without human intervention.

For Momentum's current orchestration model (Impetus + subagents + human approval gates), autonomous inline dispatch is rare. Most sub-task dispatch happens at workflow-step boundaries where a cmux pane + filesystem sentinel is sufficient.

**Revised guidance:** Process isolation + cmux is Momentum's default integration pattern. MCP integration is the exception, reserved for autonomous-loop cases.

## 2. Goose's Determinism — Recipes, Not Events

### The finding

Goose has **no hook/event subscription surface** comparable to Claude Code or OpenCode. This was the dominant surprise when walking through Goose's documentation directly.

- No `PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `Stop` equivalents.
- No user-configurable lifecycle event subscription model.
- MCP event handling is the closest analog, but it operates at the MCP-protocol level (tool_call / tool_result), not at the Goose-session level.

Goose's determinism story lives entirely in the **Recipe system**.

### Recipes as composition-layer determinism

A Recipe is a YAML file declaring:
- Ordered steps (sequential execution by default)
- Extensions to load (MCP servers scoped to the recipe)
- Parameters with types, defaults, and Jinja2 interpolation
- `sub_recipes` with explicit value mapping

A well-written Recipe is effectively a contract: given these inputs, run these steps in this order, invoke these extensions, return this shape. Determinism emerges from structure, not from event callbacks.

### Hooks vs Recipes as orthogonal primitives

| Primitive | What it answers | Where determinism lives | Best-fit use |
|---|---|---|---|
| **Hooks** (Claude Code, Cline, OpenCode via plugins) | "When X happens, run Y to gate/observe/modify" | Interception points in the agent loop | Policy enforcement, audit logging, guard-rails |
| **Recipes** (Goose) | "Here are the steps that must happen, in this order, with these tools" | The workflow definition itself | Commodity workflow execution with reproducible outputs |

These are **complementary, not substitutable**. A mature practice benefits from both: hooks for interception/policy, recipes for composition/reproducibility.

### Implication for Momentum

The Goose primitive worth importing is the **declared-composition model** — `sub_recipes` with parameter mapping is cleaner than Momentum's current convention of "skill spawns subagent via Agent tool and prompt-templates the inputs." Formalizing skill composition in YAML frontmatter would give Momentum:

- Static dependency analysis (orphan skills, unused parameters)
- Explicit parameter flow between composing skills
- A canonical serialization for sharing / versioning skill graphs

Worth importing regardless of whether Momentum ever runs Goose as a host.

## 3. Sprint-Stage and Story-Type Tool Mapping

Different Momentum phases have different signatures that map to different tools:

| Phase / Story Type | Best Tool | Rationale |
|---|---|---|
| **Intake, research** | Claude Code (Momentum's `intake`, `research` skills) | Structured outputs, AVFL validation, Momentum's own conventions |
| **Create-story, sprint-planning** | Claude Code | Authority-hierarchy rules, TeamCreate for team composition, Gherkin ATDD, Impetus orchestration |
| **Dev stories — architectural / cross-cutting** | Claude Code + Sonnet 4.6 / Opus | Deep context understanding, subagent orchestration, hook-driven gates |
| **Dev stories — bulk mechanical edits, scaffolding, CRUD, migrations** | OpenCode or Aider with DeepSeek/Qwen via OpenRouter | ~4× token efficiency on compact-diff edits; cheap models; OpenCode runs from same `.claude/skills/` |
| **Dev stories — commodity workflows (schema migrations, changelog, dep audit, PR descriptions)** | Goose via curated recipe | Community-maintained recipes; local-model lanes; AAIF-stewarded ecosystem |
| **AVFL / parallel review** | OpenCode (genuinely different harness = genuine adversarial signal) | Different prompts, tool-call strategy, and failure modes — strictly better than same-model second pass |
| **Retro auditor team / sprint review** | Claude Code | TeamCreate + SendMessage for multi-agent dialogue — unique to Claude Code |
| **Long-running, privacy-sensitive, sovereign-operation tasks** | Goose on local models (Ollama) | Zero cloud-API cost, full data control |
| **Visual / symbol-precise task dispatch on JVM code** | JetBrains Air + Junie (if JetBrains-fluent) | Symbol-context model + JVM tuning |

### Story-level dispatch via change-type classifier

Momentum's `create-story` workflow already classifies change-type. Extending the classifier with a `preferred_host` field would enable automatic dispatch in sprint-dev:

- `backend-architectural` → Claude Code
- `frontend-boilerplate` → OpenCode
- `schema-migration` → Goose recipe
- `research-spike` → Claude Code (intake/research skills)
- `bulk-refactor` → OpenCode or Aider

This would be a concrete, shippable sprint-dev enhancement with measurable cost and quality benefits.

## 4. CMUX as the Integration Substrate — the Architectural Insight

### The core recognition

Momentum already has the perfect integration substrate: **CMUX's CLI primitives** (`cmux new-split`, `cmux respawn-pane`, `cmux send`, `cmux capture-pane`, `cmux rename-tab`) give Claude Code everything it needs for programmatic tool orchestration, *and* the pattern respects Momentum's "visible to the developer" principle.

### The pattern

```bash
# Claude Code (or a Momentum skill) dispatches to OpenCode in a new pane:
SURFACE=$(cmux new-split down --json | jq -r '.surface')
cmux rename-tab --surface $SURFACE "opencode: bulk-rename"
cmux respawn-pane --surface $SURFACE \
  --command "cd /path/to/worktree && opencode -p 'rename all foo_bar to fooBar across src/' > /tmp/opencode-result.md && touch /tmp/opencode-result.md.done"

# Claude Code waits for completion via filesystem sentinel:
until [ -f /tmp/opencode-result.md.done ]; do sleep 2; done

# Claude Code reads the result:
cat /tmp/opencode-result.md

# Same pattern works for Goose:
cmux respawn-pane --surface $SURFACE \
  --command "goose run --recipe schema-migration --params '{...}' --output /tmp/goose-result.json"
```

### Why this is better than MCP for Momentum

- **The developer literally sees the other tool working in a labeled pane.** Practice-principle alignment.
- **Each tool runs in its full native UI.** No capability flattening.
- **Debugging is trivial** — just look at the pane.
- **Worktree isolation is already cmux-idiomatic.**
- **Fits the existing Momentum practice** — CMUX is already Momentum's visibility substrate.

### Proposed Momentum skill: `momentum:dispatch-to-pane`

A helper skill exposing the pattern:

1. Creates a new pane with a descriptive label
2. Spawns the target tool with a specific command
3. Monitors for completion via a filesystem sentinel
4. Reads and returns the result to the caller
5. Closes the pane when complete (or leaves it open for inspection based on a flag)

This would be genuinely differentiating — no other practice layer has a visible-to-developer multiplexer integration model.

### CMUX-native tool availability — honest assessment

CMUX is the developer's own tool. No external agentic tool is explicitly "CMUX-native." The practical question is: which tools fit most naturally into cmux panes?

**Best cmux-pane citizens (pure terminal):**
- Claude Code, OpenCode, ForgeCode, Aider, Crush, Codex CLI, Goose CLI

**Awkward or non-cmux-native:**
- JetBrains Air (GUI), Cline / Roo / Kilo / Continue (VS Code), Goose Desktop (own window), Junie IDE plugin

**Related pattern validation:** Terminal-Bench benchmark runs agents inside tmux (CMUX's upstream substrate), validating the "multiplexer-as-substrate" architecture at a community scale.

## 5. Revised Three-Layer Integration Strategy

### Layer 1 — Process-isolation baseline (do first)

Set up three Momentum-aware cmux workspaces:

- `momentum-primary` — Claude Code + Impetus (authoritative Momentum orchestrator)
- `momentum-opencode` — OpenCode with its own git worktree (bulk edits, parallel review, AVFL)
- `momentum-goose` — Goose with curated recipe library (commodity workflows, local-model lanes)

Each reads from the same repo via worktrees. Human orchestrates across them by watching panes. No integration code required.

**Cost:** Essentially zero — cmux workspaces are a few commands to set up.
**Value:** Immediate access to cheaper-model bulk editing and Goose's recipe ecosystem.

### Layer 2 — CMUX-driven autonomous dispatch (differentiator)

Ship a `momentum:dispatch-to-pane` skill that lets Momentum subagents spawn OpenCode / Goose / Aider tasks in labeled panes with filesystem-sentinel completion signals.

**Cost:** ~3-5 days of skill development.
**Value:** Autonomous sub-task dispatch while retaining full visibility. The most practice-aligned integration pattern available to Momentum today.

### Layer 3 — MCP integration (only where Layer 2 isn't enough)

Use `opencode-mcp` or AgentAPI-wrapped Goose only for cases where Claude Code needs the result **inline in its own context window for a real-time loop decision**. Most Momentum work doesn't need this — filesystem + pane capture is sufficient.

**Cost:** Variable, depends on the specific MCP wrapper being adopted.
**Value:** Narrow — use only when autonomous inline dispatch is the actual requirement.

## 6. Cross-Cutting Clarifications Worth Recording

### ClaudeCode model routing is more flexible than commonly assumed

Claude Code does **not** require Anthropic models. Three documented paths:

- `ANTHROPIC_BASE_URL=https://openrouter.ai/api` + OpenRouter API key → any of 290+ models
- Self-hosted LiteLLM proxy accepting Anthropic-format requests → 100+ provider backends with fallback chains, budgets, per-key telemetry
- `claude-code-router` community proxy with `<CCR-SUBAGENT-MODEL>provider,model</CCR-SUBAGENT-MODEL>` directive for per-subagent model selection

Plus native per-subagent `model:` field and `CLAUDE_CODE_SUBAGENT_MODEL` env var.

**If cost is the only goal, the `ANTHROPIC_BASE_URL` route is strictly simpler than MCP integration.** MCP integration's value is a different agent architecture (different prompts, tool-call formats, plugin ecosystems), not model routing.

### Claude Pro/Max subscription is not usable in any third-party tool

Per Anthropic's Consumer Terms of Service update of 2026-02-20 and enforcement beginning 2026-04-04: OAuth tokens from Claude Free/Pro/Max subscriptions may only be used with Claude Code and Claude.ai. Third-party tools (including the Agent SDK, Goose, OpenCode, JetBrains Air) are explicitly prohibited. Community workaround plugins exist but violate the ToS and credentials are tagged for enforcement.

**Practical implication:** Run Goose/OpenCode/Air on non-Anthropic models (DeepSeek, Qwen on Cerebras or OpenRouter, Gemini, local Ollama) and keep Claude Code on the Claude subscription for the primary driver role. Or budget separately for API-key billing if running those tools on Claude models.

### Junie CLI and OpenCode both ride the shared SKILL.md convention

Both tools load Agent Skills from convention paths (`.junie/skills/` and `.claude/skills/` respectively). Any Momentum-authored skill at `.claude/skills/<name>/SKILL.md` is already portable to Junie (and vice versa) with zero rework. This is strong validation for the strategic recommendation to author on the cross-vendor SKILL.md substrate rather than anything Claude-specific.

## 7. Decision-Ready Framings

This analysis surfaces three concrete decisions the developer can take to `momentum:decision`:

### Decision A — Integration substrate: cmux vs MCP

**Framing:** Should Momentum's default pattern for invoking other agentic tools be (i) cmux pane dispatch with filesystem coordination, or (ii) MCP integration?

**Recommendation:** **cmux pane dispatch** as the default; MCP only for autonomous-loop inline dispatch.

**Evidence:** Process isolation + cmux respects the "visible to the developer" principle; preserves each tool's full capability surface; requires no integration shims; matches Momentum's existing architecture. MCP's unique value is autonomous inline dispatch, which is rare in Momentum's human-orchestrated flow.

### Decision B — Story-level dispatch by change type

**Framing:** Should sprint-dev route stories to different tools based on change-type classification?

**Recommendation:** Yes — extend `create-story`'s change-type classifier with a `preferred_host` field and have `sprint-dev` honor it for routing.

**Evidence:** Different stories have different characteristics — architectural work needs Claude Code's deep-context handling; bulk mechanical edits benefit from OpenCode's compact-diff format (~4× cheaper); commodity workflows fit Goose recipes. Automatic dispatch removes a judgment burden.

### Decision C — Momentum skill additions

**Framing:** Should Momentum ship `momentum:dispatch-to-pane` and `momentum:analysis` as new skills?

**Recommendation:** Yes on both, though `momentum:analysis` can be intaked later.

**Evidence:**
- `momentum:dispatch-to-pane` — enables Layer 2 of the integration strategy; differentiating primitive; ~3-5 days of work; unlocks cmux-native tool orchestration.
- `momentum:analysis` — fills the gap between `research` and `decision`; this analysis document itself is evidence of the need; would formalize the option-exploration and decision-framing phase that currently has no skill.

## 8. Open Questions Deferred to Next Session

- **Does JetBrains Air embed Claude Code or just the Claude Agent SDK?** Critical for Momentum: hooks and skills only work if full Claude Code is embedded. Resolution: install Air, plant a test hook + skill, observe firing behavior.
- **Is Block's unified-tooling RFC ([block/goose#6202](https://github.com/block/goose/discussions/6202)) on track to ship?** If yes, Goose's parallel-track viability improves materially.
- **Will OpenCode add an inter-agent messaging primitive** (TeamCreate + SendMessage equivalent)? If yes, full-migration viability improves.
- **What's the concrete ROI of `momentum:dispatch-to-pane` vs separate-workspaces baseline?** Worth a spike: run one contained workflow both ways and compare time, cost, and quality.

## Sources

This analysis extends:
- [final/forgecode-agentic-tools-eval-final-2026-04-21.md](../final/forgecode-agentic-tools-eval-final-2026-04-21.md)
- [raw/followup-jetbrains-integration-licensing.md](../raw/followup-jetbrains-integration-licensing.md)
- [raw/practitioner-notes.md](../raw/practitioner-notes.md)

New sources consulted during analysis:
- [OpenRouter — Claude Code integration docs](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration)
- [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
- [luohy15/y-router — simple proxy for Claude Code ↔ OpenRouter](https://github.com/luohy15/y-router)
- [Terminal-Bench — multiplexer-as-substrate validation](https://www.tbench.ai/)
- [Block/Goose discussion #6202 — unified tooling RFC](https://github.com/block/goose/discussions/6202)
- [Goose Recipes documentation](https://goose-docs.ai/docs/guides/recipes/)
- [/Users/steve/.claude/rules/cmux.md — CMUX CLI reference](/Users/steve/.claude/rules/cmux.md)
