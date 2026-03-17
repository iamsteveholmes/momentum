# Model Routing Guide

*Canonical resource for momentum model selection decisions.*
*Condensed from: multi-model-benchmarking-guide-2026-03-13.md*
*Date: 2026-03-14*

---

## Decision Matrix

```
Is the task well-constrained with deterministic validation?
├── YES → Haiku 4.5, effort N/A, validate with schema/tests
│         (If validation fails after 4 retries → escalate to Sonnet)
└── NO
    ├── Does it require novel reasoning or multi-step logic?
    │   ├── YES → Opus 4.6, effort high (or max for hardest problems)
    │   └── NO → Sonnet 4.6, effort medium
    └── Will a human review the output without automated validation?
        ├── YES → Use flagship model (Opus) — invisible errors cost more
        │         than the model price premium (see Cognitive Hazard Rule below)
        └── NO → Optimize for cost with automated validation
```

## Default: Sonnet 4.6 at Medium Effort

Start here. Upgrade to Opus when errors are costly, reasoning is complex, or the task is orchestration. Downgrade to Haiku when the task is well-constrained and outputs can be validated downstream.

## Task-Type-to-Model Mapping

| Task Type | Model | Effort | Rationale |
|---|---|---|---|
| Complex code generation (multi-file) | Opus 4.6 | high | Leads Terminal-bench by ~6pp |
| Routine code generation (single functions) | Sonnet 4.6 | medium | Matches Opus on SWE-bench at 60% cost |
| Code review / validation | Sonnet 4.6 | medium | Good reasoning at lower cost |
| Creative writing / session prep | Sonnet 4.6 | high | Strong writing; Opus adds cost without proportional gain |
| Data extraction / structured output | Haiku 4.5 | -- | Well-constrained; 1/5 cost |
| Summarization | Sonnet 4.6 | low-medium | Haiku works for simple summaries |
| Complex reasoning / analysis | Opus 4.6 | high-max | +17.2pp on GPQA Diamond |
| Simple classification / routing | Haiku 4.5 | -- | Fast, cheap, accurate enough |
| Validation / error checking | Sonnet or Haiku | low-medium | Haiku for structural, Sonnet for semantic |
| Multi-agent orchestrator | Opus 4.6 | high | Best at coordination; cheap models for subtasks |
| Sub-agent search/exploration | Haiku 4.5 | -- | Claude Code's Explore agent defaults to Haiku |

## The Cognitive Hazard Rule

**For outputs without automated validation, use flagship models — the cost premium is cheaper than missed hallucinations.**

Evidence (benchmarking guide Section 3):
- Cheaper models make fewer total errors but more *invisible* errors (embedded hallucinations, subtle logic flaws)
- Automation bias: humans over-rely on AI output, catching ~26% fewer errors than baseline (CDSS research, directionally applicable)
- Vigilance decrement: human error detection drops during sustained review
- Flagship models are trained for calibration — they admit uncertainty rather than hallucinate

When to apply:
- Documents that will be human-reviewed without automated fact-checking
- Architecture decisions, security-sensitive logic, business rules
- Any output where an undetected error compounds downstream

When it does NOT apply:
- Code with comprehensive test suites (tests catch invisible errors)
- Structured output with schema validation
- Classification tasks with known correct answers

## Effort Levels

| Effort Level | Behavior | Use Case | Availability |
|---|---|---|---|
| **max** | Maximum capability, no constraints on thinking depth | Deepest reasoning, most thorough analysis | Opus 4.6 only |
| **high** | Deep reasoning, always thinks. API default. | Complex reasoning, difficult coding, agentic tasks | Opus 4.6, Sonnet 4.6 |
| **medium** | Balanced. May skip thinking for simple queries. | Agentic tasks balancing speed/cost/performance | Opus 4.6, Sonnet 4.6 |
| **low** | Most efficient. Skips thinking for simple tasks. | Simple classification, quick lookups, high-volume subagents | Opus 4.6, Sonnet 4.6 |

**Critical detail**: Thinking tokens are billed at output token rates. For Opus 4.6, that's $25/MTok. A response using 10k thinking tokens costs $0.25 just for thinking. At low effort, Claude may skip thinking entirely — significant cost savings.

## Retry Loop Economics

- Cap retry loops at 4-5 iterations (validate-fix-loop v3 uses 4)
- Context accumulation makes later iterations progressively more expensive
- If a model fails after 3-4 iterations, escalate to a higher-tier model rather than burning more tokens at the same tier
- For simple tasks with deterministic validation, cheap model + retry is almost always cheaper than flagship first-try
- FrugalGPT cascade: route to cheap model first, escalate only on failure — up to 98% cost reduction matching flagship quality

## Cost Comparison (10k input / 2k output)

| Model | Total Cost | Relative |
|---|---|---|
| Haiku 4.5 | $0.02 | 1x |
| Sonnet 4.6 | $0.06 | 3x |
| Opus 4.6 | $0.10 | 5x |
| Opus 4.6 (batch) | $0.05 | 2.5x |

## Claude Code Model Selection Mechanisms

| Method | Scope | Priority |
|---|---|---|
| Managed settings (`availableModels`) | Organization-wide | Highest |
| CLI flag (`--model opus`) | Session | High |
| `/model sonnet` command | Mid-session switch | High |
| `Option+P` (macOS) / `Alt+P` | Mid-prompt switch | High |
| `ANTHROPIC_MODEL` env var | Environment-wide | Medium |
| `settings.json` (`"model": "opus"`) | Persistent default | Low |
| Sub-agent frontmatter (`model: haiku`) | Per sub-agent | Per-agent |
| Skill frontmatter (`model: sonnet`) | Per skill | Per-skill |
| `CLAUDE_CODE_SUBAGENT_MODEL` env var | All sub-agents | Overrides frontmatter |

**opusplan**: Opus for planning, auto-switches to Sonnet for execution. A built-in hybrid routing strategy.

**Effort**: `/effort low|medium|high|max|auto`, `--effort` flag, `CLAUDE_CODE_EFFORT_LEVEL` env var, or `"effortLevel"` in settings.json.

## Observability

- `/cost` command: total cost, API duration, wall duration, lines changed
- `showTurnDuration` setting: per-turn timing
- `--output-format json`: programmatic access to duration, cost, token counts
- `ccusage`: community CLI for cross-session cost tracking
- `CLAUDE_CODE_ENABLE_TELEMETRY=1`: OTel export for metrics and events

## Sources

- Full research: docs/research/multi-model-benchmarking-guide-2026-03-13.md
- Handoff: docs/research/multi-model-benchmarking-handoff-2026-03-14.md
- Cognitive load evidence: benchmarking guide Section 3
- Retry economics: benchmarking guide Section 7.2
- Validate-fix-loop cap: docs/research/validate-fix-loop-framework-v3.json
