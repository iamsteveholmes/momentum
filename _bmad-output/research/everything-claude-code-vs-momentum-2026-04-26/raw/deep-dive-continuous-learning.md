---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Deep dive — ECC's continuous-learning-v2: mechanism, integration paths, concerns"
topic: "everything-claude-code vs Momentum — comparative analysis"
parent_question: "Q4 from practitioner Q&A — better understanding requested"
---

# Deep Dive — ECC's `continuous-learning-v2`

## Inline Summary

`continuous-learning-v2` is a hook-driven, background-agent system that fires on every Claude tool call, writes observations to a per-project JSONL file, and periodically runs a Haiku-powered background process that reads those observations and writes atomic "instinct" YAML files with confidence scores (0.3–0.9). Project-to-global promotion is **not automatic by default** — the `instinct-cli.py promote` command must be run explicitly, though it has an auto-mode for instincts that appear in 2+ projects with average confidence ≥ 0.8. The most plausible integration path with Momentum is to use the observation-capture mechanism (the `observe.sh` hook) as a feeder into `intake-queue.jsonl`, with Momentum's `triage` skill acting as the human gate before anything reaches `distill` or a story stub — effectively making ECC supply the candidates and Momentum supply the judgment.

---

## 1. The Actual File Structure

The `continuous-learning-v2` directory in the ECC repo (`skills/continuous-learning-v2/`) contains: [OFFICIAL]

```
SKILL.md          # 12,601 bytes — main documentation and command spec
config.json       # 135 bytes — observer toggle and interval settings
hooks/
  observe.sh      # 17,703 bytes — PreToolUse/PostToolUse hook script
agents/
  observer.md          # Haiku agent prompt/specification
  observer-loop.sh     # 9,876 bytes — background loop script (runs observer.md via Claude CLI)
  start-observer.sh    # 7,522 bytes — start/stop/status lifecycle manager
  session-guardian.sh  # 6,392 bytes — gating logic (time windows, cooldown, idle detection)
scripts/
  detect-project.sh    # 8,254 bytes — project ID derivation from git remote
  instinct-cli.py      # 57,750 bytes — CLI for managing instincts (promote, export, import, etc.)
  test_parse_instinct.py # 33,106 bytes — test suite for instinct parsing
```

This is not a thin wrapper. The `instinct-cli.py` alone is nearly 58 KB — a real Python program. The test suite is 33 KB. This is the most substantial self-contained subsystem in the ECC repo.

---

## 2. What Triggers an Observation

The hook is `observe.sh`, registered in `hooks/hooks.json` as both a `PreToolUse` and `PostToolUse` matcher on `*` (all tools). The SKILL.md installation section says: [OFFICIAL]

> "If installed as a plugin (recommended): No extra `settings.json` hook block is required. Claude Code v2.1+ auto-loads the plugin `hooks/hooks.json`, and `observe.sh` is already registered there."

**Every single tool call** — Read, Edit, Write, Bash, WebFetch, and all MCP tool calls — triggers `observe.sh`. This is the key architectural difference from v1, which used a Stop hook (session end only, fired ~50-80% of the time per Claude's judgment). The SKILL.md states plainly: "Hooks fire **100% of the time**, deterministically." [OFFICIAL]

The `observe.sh` script:
1. Parses the hook payload from stdin as JSON (tool name, tool input, current working directory)
2. Extracts the working directory and resolves it to a git repository root
3. Runs several **skip guards** before writing anything:
   - Skips if running from CLI/automation contexts (only fires for `cli`, `sdk-ts`, `claude-desktop` entrypoints)
   - Skips if `ECC_HOOK_PROFILE=minimal` is set
   - Skips if `ECC_SKIP_LEARNING=1` is set
   - Skips if the tool call touches files in excluded paths (the skill's own hooks directory, etc.) — anti-self-observation guard
4. Truncates the observation payload to 5,000 characters
5. **Scrubs secrets** matching patterns like `api_key`, `token`, `password`, `secret` before writing
6. Derives the project ID via `detect-project.sh` (described below)
7. Appends the observation as a single JSON line to `~/.claude/homunculus/projects/<project-hash>/observations.jsonl`
8. Archives the file if it exceeds 10MB; purges archives older than 30 days (runs once per session)
9. Optionally signals the background observer loop via SIGUSR1 if one is running

[OFFICIAL — verified by reading the WebFetch summary of observe.sh]

---

## 3. What Gets Written and Where

**Observations file:** `~/.claude/homunculus/projects/<project-hash>/observations.jsonl` [OFFICIAL]

Each line is a JSON object capturing the tool event, truncated and scrubbed. The exact schema is not fully documented in the SKILL.md but based on the observe.sh behavior, it captures tool name, tool input (scrubbed), and project context.

**Global fallback:** If no git repo is detected, observations go to `~/.claude/homunculus/observations.jsonl`.

**Projects registry:** `~/.claude/homunculus/projects.json` maps project hashes to human-readable names.

**Instinct files:** Written by the observer agent to:
- Project-scoped: `~/.claude/homunculus/projects/<hash>/instincts/personal/<id>.yaml`
- Global: `~/.claude/homunculus/instincts/personal/<id>.yaml`

**Evolved artifacts:** After `/evolve` is run, output goes to:
- Project-scoped: `~/.claude/homunculus/projects/<hash>/evolved/{skills,commands,agents}/`
- Global: `~/.claude/homunculus/evolved/{skills,commands,agents}/`

The full directory tree from SKILL.md: [OFFICIAL]

```
~/.claude/homunculus/
├── identity.json           # Profile, technical level
├── projects.json           # Registry: project hash → name/path/remote
├── observations.jsonl      # Global observations (fallback only)
├── instincts/
│   ├── personal/           # Global auto-learned instincts
│   └── inherited/          # Global imported instincts
├── evolved/
│   ├── agents/
│   ├── skills/
│   └── commands/
└── projects/
    └── a1b2c3d4e5f6/       # Project hash (from git remote URL)
        ├── project.json
        ├── observations.jsonl
        ├── observations.archive/
        ├── instincts/
        │   ├── personal/   # Project-specific auto-learned
        │   └── inherited/  # Project-specific imported
        └── evolved/
            ├── skills/
            ├── commands/
            └── agents/
```

---

## 4. Project ID Derivation

The `detect-project.sh` script uses this priority order: [OFFICIAL]

1. `CLAUDE_PROJECT_DIR` environment variable (highest priority — for CI/automation)
2. `git remote get-url origin` — hashed to a 12-character ID. This is the portable hash: same repo on different machines gets the same ID.
3. `git rev-parse --show-toplevel` — fallback to repo path (machine-specific, less portable)
4. Global fallback — if no project detected at all

This is structurally identical to Momentum's own project-scoped memory path (`~/.claude/projects/<project-hash>/memory/`), which also derives the hash from the git remote URL. [PRAC — Momentum's hash derivation is Claude Code's native behavior; ECC reimplements an analogous scheme in a different location.]

---

## 5. What an "Instinct" Looks Like

The SKILL.md gives a complete example: [OFFICIAL]

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**Fields:**
- `id` — kebab-case, unique identifier, must be stable for confidence tracking
- `trigger` — "when writing new functions" — the context that makes this instinct relevant
- `confidence` — float 0.3–0.9. Initial value scales with observation frequency: 0.3 for 1-2 observations, up to 0.85 for 11+ observations [OFFICIAL]
- `domain` — one of: `code-style`, `testing`, `git`, `debugging`, `workflow`, etc.
- `source` — how it was created: `session-observation`, `imported`, etc.
- `scope` — `project` or `global`
- `project_id` / `project_name` — populated only for project-scoped instincts

The body follows the trigger with an `## Action` section (what to do) and an `## Evidence` section (the observation record that created it).

---

## 6. Who Runs the Haiku Analyzer — and When

The background observer is a **separate Claude process** invoked by `observer-loop.sh` using the Claude CLI (`claude --model claude-haiku-3-5` or similar, run in `--print` mode with limited tools: Read and Write only). [OFFICIAL — observer-loop.sh WebFetch confirms "Invokes Claude with Haiku model in `--print` mode, limited to Read/Write tools"]

**The observer is off by default.** The `config.json` ships with `"observer": { "enabled": false }`. [OFFICIAL] To enable it, the user must either:
- Set `enabled: true` in `config.json` and run `start-observer.sh start`
- Or invoke the observer manually via `instinct-cli.py`

When enabled, the loop fires every `run_interval_minutes` (default: 5 minutes). Before each analysis cycle, `session-guardian.sh` applies three gates in order: [OFFICIAL]

1. **Time window gate** — skip if current local time is outside `OBSERVER_ACTIVE_HOURS_START`–`OBSERVER_ACTIVE_HOURS_END` (defaults 8 AM – 11 PM). The gate supports overnight windows.
2. **Project cooldown gate** — skip if the same project was analyzed within `OBSERVER_INTERVAL_SECONDS` (default: 300 seconds). Uses `mkdir`-based file locking for concurrency safety.
3. **Idle detection gate** — skip if user has been idle longer than `OBSERVER_MAX_IDLE_SECONDS` (default: 1800 seconds = 30 min). Designed so the observer doesn't churn when no active work is happening.

The minimum observations threshold (`min_observations_to_analyze`: default 20) means the observer won't fire until at least 20 events have been logged. This prevents spurious instinct generation from a brief session.

When the analysis does run, `observer-loop.sh`:
1. Validates prerequisites (observations file exists, Claude CLI available)
2. Samples the last 500 lines of the observations file (not the whole file — memory management)
3. Writes the sample to a temp file
4. Invokes the Claude Haiku agent with that temp file as input
5. The agent writes instinct YAML files directly to the instincts directory
6. Archives processed observations with timestamps

**Re-entrancy guard:** The loop will not start a second analysis while one is running. Cooldown throttling (default 60 seconds) prevents rapid-fire concurrent Claude processes. [OFFICIAL — observer-loop.sh WebFetch confirms "re-entrancy guards preventing concurrent analysis runs, plus cooldown throttling"]

---

## 7. The Observer Agent's Pattern Recognition

The `observer.md` agent spec (the Haiku prompt) targets four pattern types: [OFFICIAL]

1. **User corrections** — "No, use X instead of Y" — explicit feedback to the model
2. **Error resolutions** — tool errors followed by successful corrections — learned error-handling
3. **Repeated workflows** — same sequence of tool calls appearing 3+ times — habitual patterns
4. **Tool preferences** — consistent choice of one tool over alternatives — workflow preferences

The agent is instructed: "Default to `scope: project` — it's safer to be project-specific and promote later than to contaminate the global space." [OFFICIAL]

For domains clearly universal (security practices, general best practices, git workflow), the agent may assign `scope: global` directly. For language/framework-specific or file-structure preferences, it assigns `scope: project`.

---

## 8. Confidence Scoring in Detail

Initial confidence is observation-count-derived: [OFFICIAL]
- 1-2 observations → 0.3 (tentative)
- 3-5 observations → 0.5 (moderate)
- 6-10 observations → 0.7 (strong)
- 11+ observations → 0.85 (near-certain)

Dynamic adjustment: [OFFICIAL]
- `+0.05` for each confirming observation (pattern seen again without contradiction)
- `-0.1` for each contradicting observation (user explicitly corrects the behavior)
- Decay over time without observation (rate not specified in SKILL.md — likely in `instinct-cli.py`)

The SKILL.md describes four behavioral tiers: [OFFICIAL]

| Score | Behavior |
|-------|----------|
| 0.3 | Suggested but not enforced |
| 0.5 | Applied when relevant |
| 0.7 | Auto-approved for application |
| 0.9 | Core behavior |

The distinction between 0.5 ("applied when relevant") and 0.7 ("auto-approved") is meaningful: below 0.7, instincts are suggestions that the agent considers; above 0.7, they are instructions that apply without requiring deliberation. There is no explicit UI notification when an instinct crosses the 0.7 threshold — the promotion to "auto-approved" is silent.

---

## 9. Project-to-Global Promotion — Is It Automatic or Gated?

**It is not automatic by default.** Promotion requires running the `promote` command explicitly: [OFFICIAL]

```bash
# Promote a specific instinct
python3 instinct-cli.py promote prefer-explicit-errors

# Auto-promote all qualifying instincts
python3 instinct-cli.py promote

# Preview without changes
python3 instinct-cli.py promote --dry-run
```

The `/evolve` slash command within a Claude session also "suggests promotion candidates" — but suggestion is not execution.

**Auto-promotion criteria** (for `python3 instinct-cli.py promote` with no arguments): [OFFICIAL]
- Same instinct `id` appears in 2+ projects
- Average confidence across those projects ≥ 0.8

When both criteria are met, running `promote` without an explicit ID will promote all qualifying instincts from project to global scope. The `--dry-run` flag allows previewing before committing.

**The human-in-the-loop gap:** The auto-mode (`promote` with no argument) will execute without per-instinct confirmation. There is no described approval step — the user runs the command and qualifying instincts are promoted. If the user runs `promote` without `--dry-run` first, promotion is irreversible (though the project-scoped copy remains). This is the primary human-in-the-loop gap in the system.

**The `/evolve` command** clusters related instincts and proposes evolution into full skills/commands/agents. The SKILL.md presents this as an interactive step (the command "suggests" — implies user review before execution), but the observer-loop.sh analysis notes that the Haiku agent "must write instinct files directly (not ask permission)." The *instinct writing* step is fully autonomous; the *evolution-to-skill* step appears to require the user to invoke `/evolve` explicitly. [OFFICIAL]

---

## 10. How Instincts Are Surfaced to the Agent

The SKILL.md is less explicit about surfacing than about capture. Based on the file structure and command descriptions, the mechanism is: [OFFICIAL, partially UNVERIFIED]

1. At session start (or when relevant), the agent reads instinct files from the project-scoped and global `instincts/personal/` directories [OFFICIAL — the directory structure exists and instincts are YAML files the agent can Read]
2. The `/instinct-status` command displays all instincts with their confidence scores — this is the explicit visibility command
3. Instincts at confidence ≥ 0.7 are described as "auto-approved for application" — the SKILL.md implies they are injected into the agent's context as behavioral instructions
4. The `identity.json` file at `~/.claude/homunculus/identity.json` stores a user profile and technical level — likely read as part of session initialization

**What is NOT specified:** Whether there is a SessionStart hook that automatically reads and injects instincts into the system prompt, or whether the agent only applies them if it happens to read the instinct files during a session. The SKILL.md says instincts at 0.7 are "auto-approved for application" but does not describe the mechanical injection pathway. Given that `observer.md` writes files and `observer-loop.sh` runs Claude in `--print` mode with Read/Write tools only, the observer itself doesn't inject instincts — it writes them. How they get read back into active sessions is [UNVERIFIED] at the file level, though it's plausible that the same hook system that feeds `observe.sh` could also feed an instinct-loading step.

---

## 11. The v1 → v2 → v2.1 Evolution

| Dimension | v1 | v2 | v2.1 |
|---|---|---|---|
| Observation trigger | Stop hook (session end) | PreToolUse/PostToolUse | Same as v2 |
| Analysis location | Main Claude context | Background Haiku agent | Same as v2 |
| Granularity | Full skills | Atomic instincts | Same as v2 |
| Confidence scoring | None | 0.3-0.9 weighted | Same as v2 |
| Evolution path | Instinct → skill (direct) | Instinct → cluster → skill/command/agent | Same as v2 |
| Sharing | None | Export/import | Same as v2 + promote/projects commands |
| Scope | Global only (`~/.claude/homunculus/`) | Global only | Project-scoped by default + global |
| Cross-project contamination | High risk | High risk | Isolated by project hash |
| Promotion path | N/A | N/A | Project → global when 2+ projects, confidence ≥ 0.8 |

[OFFICIAL — directly from v2.1 SKILL.md upgrade tables]

The key v1 → v2 change was moving from the Stop hook to PreToolUse/PostToolUse. The Stop hook fired ~50-80% of the time based on Claude's judgment. PreToolUse/PostToolUse fires 100% deterministically. This is the change that makes the observation record comprehensive rather than sampling-based.

The key v2 → v2.1 change was project scoping. Without project scoping, instincts from a React project would leak into Python work. With v2.1, a project hash (derived from git remote URL) gates all writes to and reads from the project's own instinct directory.

---

## 12. Comparison to Momentum's Analogous Concepts

### vs. `momentum:distill`

Momentum's `distill` skill (at `skills/momentum/skills/distill/`) is the closest functional analog. The comparison is stark: [OFFICIAL]

| Dimension | ECC `continuous-learning-v2` | Momentum `distill` |
|---|---|---|
| Trigger | Every tool call, via hook — autonomous | Human-invoked directly or from retro Phase 5 — always intentional |
| Observer | Background Haiku agent running in a separate process | Parallel Enumerator + Adversary agents spawned within the main session |
| Candidate generation | Automatic — Haiku reads observations and writes candidates | Human-described — developer provides the learning in natural language |
| Adversarial check | None — observer writes instincts without challenge | Mandatory — Adversary checks for redundancy, conflict, scope fit |
| Output | YAML instinct file with confidence score | Targeted edit to a specific rule/reference/skill file |
| Human approval | Not required for instinct writing; required for promotion (via `promote` command) | Required at Phase 1 (before any write) |
| Rollback | No explicit mechanism described | No rollback, but AVFL validation runs post-write |
| Versioning | Confidence decay; no commit | Git commit created as part of the workflow |
| Scope decision | Observer decides (defaults to project) | Enumerator classifies as Path A/B/C; developer approves |
| Low-confidence tail | Yes — 0.3 instincts exist and persist | No — if the adversary blocks, nothing is written |

The philosophical divergence: ECC's `continuous-learning-v2` optimizes for **coverage** (capture everything, filter by confidence later). Momentum's `distill` optimizes for **precision** (don't write anything that isn't already validated). ECC produces a long tail of tentative candidates; Momentum produces a short list of high-certainty rule changes.

### vs. `intake-queue.jsonl`

Momentum's `intake-queue.jsonl` is an append-only event log at `_bmad-output/implementation-artifacts/intake-queue.jsonl`. Each line is a JSON object with fields including `id`, `timestamp`, `source`, `kind`, `status`, `title`, `description`. The `kind` field can be `handoff`, `shape`, `watch`, `rejected`. [OFFICIAL]

ECC's `~/.claude/homunculus/projects/<hash>/observations.jsonl` is also an append-only JSONL file, but it captures raw tool events rather than classified human-intent items. The observations are lower-level (individual tool calls) and higher-volume than Momentum's queue.

The Momentum `intake-queue.jsonl` captures **human-level observations** about the project (story ideas, decisions, findings). The ECC observations file captures **machine-level events** about the session (what tools were called, what errors occurred). These are different layers of abstraction.

### vs. Momentum's typed memory (`MEMORY.md`)

Momentum uses `~/.claude/projects/<hash>/memory/MEMORY.md` as an index into named per-type memory files (`feedback_*.md`, `reference_*.md`, `project_*.md`). These are written explicitly — either by the developer after giving feedback, or by Momentum's `distill`/`retro` workflow. [PRAC]

ECC's `~/.claude/homunculus/instincts/personal/` stores auto-generated YAML files. The difference is authorship: Momentum's memory is developer-authored; ECC's instincts are Haiku-authored. Both have the project hash isolation pattern; both serve the purpose of "teach the agent about my preferences."

### vs. `momentum:triage`

Momentum's `triage` skill is a batch-classification skill that takes a list of observations and classifies them into six classes (ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT), then delegates to downstream executors. [OFFICIAL — triage/workflow.md]

`triage` is explicitly human-gated: Step 4 ("Batch approval — present classification for developer review") is marked `<critical>Batch approval is required before any execution. Never skip it, even for a single-item triage session.</critical>`. [OFFICIAL]

ECC has no equivalent triage step — observations become instincts without human classification. The gap is intentional by design: ECC assumes the agent can distinguish signal from noise via confidence scoring; Momentum assumes the human provides the signal/noise distinction.

---

## 13. Integration Paths

Steve's specific question: **Could ECC's mechanism sit underneath Momentum's gate — auto-extract candidates, human approves before promotion?**

The answer is yes, and there are two coherent paths:

### Path A: `observe.sh` feeds `intake-queue.jsonl` (mechanism reuse)

Use ECC's `observe.sh` hook as-is to capture tool events into `~/.claude/homunculus/projects/<hash>/observations.jsonl`. Separately, modify (or adapt) the Haiku observer step to write its candidate instincts not to YAML files but as `kind: shape` events to Momentum's `intake-queue.jsonl`. Then run `momentum:triage` periodically to classify and route them.

**What this achieves:** The observation infrastructure (100% hook coverage, 5,000-char truncation, secret scrubbing, project scoping, archiving, session-guardian gating) is reused verbatim. The human gate is Momentum's `triage`. The instinct-to-rule application is Momentum's `distill`.

**What would conflict:** The YAML instinct format and the JSONL event format are different schemas. An adapter layer would be needed to translate an ECC instinct candidate into a Momentum `intake-queue.jsonl` entry. The `instinct-cli.py` is 58 KB of Python — it could be called directly, or just the observation-capture portion could be reused. Also, ECC's instincts live in `~/.claude/homunculus/` (global, cross-project-indexed), while Momentum's queue is per-project in `_bmad-output/`. This is a structural mismatch that would need a choice: keep ECC's global storage and query it per-project, or adapt observations to write into the Momentum project tree.

**Token cost:** `observe.sh` runs on every tool call (hundreds per sprint). It writes to disk but does not invoke the LLM on every call — that's only the background observer, which fires at most every 5 minutes and is off by default. The hook itself is pure bash — no token cost per call. [OFFICIAL]

### Path B: Periodic export as triage input

Leave ECC's instinct system running as-is (observer writes YAML instincts to `~/.claude/homunculus/`). Periodically run `/instinct-status` or `instinct-cli.py list` to dump candidates, then pipe them as a list into `momentum:triage`. Triage classifies them (DISTILL for good ones, REJECT for noise, SHAPE for uncertain), and approved DISTILL items go to `momentum:distill` for the actual rule-update.

**What this achieves:** No code changes. Pure workflow composition. ECC does the extraction; Momentum does the curation. Human gate happens at triage, not at observation.

**What would conflict:** Philosophically, this puts Momentum in the role of "garbage collector for ECC's outputs." If ECC generates many low-confidence instincts (0.3 tentative), most triage sessions will be dominated by rejections. The signal-to-noise ratio of ECC's observation stream is unknown until tested in practice. Also, ECC's instincts are project-scoped to `~/.claude/homunculus/` while Momentum's `triage` expects to be run from within a project context — the cross-directory sourcing would require explicit setup.

### Path C: Adopt `observe.sh` only, discard the rest

Use `observe.sh` purely as a lightweight session diary — hook fires, writes events, nothing else runs. Periodically (at retro, or weekly) run a `momentum:triage` pass over the raw observations log to identify patterns worth distilling. Skip ECC's background Haiku observer entirely; use Momentum's `distill` for the actual write step.

**What this achieves:** The cheapest possible integration. No ongoing LLM cost. No YAML instinct files. The observation log becomes a human-readable session diary that can inform retro (in addition to DuckDB transcript mining). The triage pattern-recognition step would be simpler than ECC's Haiku observer (Haiku reads raw events; triage reads classified findings), but with human judgment driving classification.

**What would conflict:** Nothing, technically. This is additive. The session diary path (`~/.claude/homunculus/projects/<hash>/observations.jsonl`) is separate from everything Momentum writes. The only friction is adding the `observe.sh` hook to Momentum's `hooks/hooks.json`.

---

## 14. Concerns

### Token cost

The background Haiku observer runs every 5 minutes when enabled. It processes up to 500 lines of observations per cycle. At Haiku pricing (roughly $0.80/M input tokens as of 2026), a 500-line observation sample at ~100 tokens/line is 50K tokens → ~$0.04 per cycle. At 5-minute intervals during an 8-hour session, that is ~96 cycles → ~$3.84/session in Haiku costs. This is low but not zero. **The observer is off by default for this reason.** [OFFICIAL — confirmed by `"enabled": false` in config.json and the SKILL.md note that it must be explicitly started]

The `observe.sh` hook itself has no LLM cost — it is pure bash disk I/O. The cost is only in the background observer loop.

### Bad pattern propagation

The confidence decay and contradiction mechanisms are designed to prevent a bad instinct from becoming permanent. But they have gaps:

1. **Silent auto-approval at 0.7:** An instinct at 0.7 is "auto-approved for application." If a bad instinct is reinforced by 6-10 observations (e.g., a bad habit the developer was in the middle of refactoring), it silently becomes auto-approved with no notification. [OFFICIAL — the 0.7 threshold is in SKILL.md; the lack of a notification mechanism is UNVERIFIED but implied by absence]

2. **Auto-promotion without per-instinct confirmation:** `python3 instinct-cli.py promote` (no argument) promotes all instincts meeting the 2-projects/≥0.8-confidence criteria without requiring per-instinct review. If a bad convention appears in two projects by coincidence (e.g., developer was debugging something temporarily), it can reach global scope. The `--dry-run` flag exists but isn't required. [OFFICIAL]

3. **No rollback:** Once promoted to global, an instinct persists until manually deleted via `instinct-cli.py`. There is no git-backed history; deleting a YAML file is the rollback. [OFFICIAL — instincts are files; no rollback mechanism described]

4. **Observer confidence drift:** The observer sees the last 500 lines of observations. If early observations showed one pattern and late observations contradict it, the 500-line window may only show the early pattern, reinforcing a stale instinct. The archive/purge cycle (30-day retention, 10MB rollover) means old observations are eventually deleted. [OFFICIAL — archiving described in observe.sh]

### Privacy

The SKILL.md describes several privacy protections: [OFFICIAL]

- Observations stay local — no upload, no remote call
- Secret scrubbing patterns: `api_key`, `token`, `password`, `secret` (and likely others in the full regex)
- Raw observations are never exported — only instinct YAML files can be exported
- Project-scoped isolation prevents cross-project leakage of sensitive patterns

The concerns:
- Secret scrubbing uses pattern matching on field names, not semantic analysis. A credential stored in a field named `auth` or `bearer` or `x-api-key` might pass through unredacted. [UNVERIFIED — the exact regex is in observe.sh code not quoted verbatim in the WebFetch summary]
- 5,000-character truncation means long tool calls (e.g., a large file edit) are captured but truncated — the truncation could cut off a sensitive section or could leave sensitive content in the retained portion. [OFFICIAL — 5,000 char limit described]
- The observations file contains tool call inputs, which may include file paths, code snippets, and partial file contents. Even with scrubbing, a developer working on healthcare or financial code should review what the observation file contains before enabling the background observer. [PRAC]

### Observation volume at scale

At roughly 100-500 tool calls per hour of active development, a full sprint week generates 4,000–20,000 observation lines. The 10MB archival trigger and 30-day purge manage this, but the file-based storage is sequential (no indexing). The `instinct-cli.py` reads and parses observations in Python, which should handle this volume, but it hasn't been validated against large repositories or long-running projects in Momentum's context. [UNVERIFIED — no explicit performance benchmarks in the repo]

### ECC's own mitigation for these concerns

ECC ships `session-guardian.sh` with three gates (time window, project cooldown, idle detection) that collectively reduce observer frequency significantly. The `ECC_SKIP_LEARNING=1` env var provides a per-session escape hatch. The `--dry-run` flag on `promote` and the `ECC_HOOK_PROFILE=minimal` setting give additional levers. These are thoughtful mitigations, not afterthoughts, but they require the user to actively configure them. [OFFICIAL]

---

## 15. What ECC Does Not Say

Several things the SKILL.md is silent on that matter for integration:

1. **How instincts are injected into active sessions.** The storage structure is clear; the read-back pathway is not. Is there a `SessionStart` hook that loads instincts? Does the user need to `/instinct-status` explicitly? The SKILL.md says 0.7+ instincts are "auto-approved for application" but doesn't describe the mechanism. [UNVERIFIED]

2. **What happens to evolved artifacts (`evolved/skills/`, `evolved/commands/`).** These appear to be placed in the homunculus directory, not the project's `.claude/skills/` path. Whether Claude Code auto-discovers them or whether a manual registration step is needed is not specified. [UNVERIFIED]

3. **The `identity.json` file format and how it interacts with instinct generation.** The SKILL.md mentions it stores "your profile, technical level" but doesn't describe who writes it or when. [UNVERIFIED]

---

## Sources

**ECC repo — directly read:**
- `skills/continuous-learning-v2/SKILL.md` (v2.1, 12,601 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/config.json` (135 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/hooks/observe.sh` (17,703 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/agents/observer.md` (7,396 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/agents/observer-loop.sh` (9,876 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/agents/start-observer.sh` (7,522 bytes) — fetched via `raw.githubusercontent.com` [OFFICIAL]
- `skills/continuous-learning-v2/agents/session-guardian.sh` (6,392 bytes) — first 80 lines decoded via GitHub API [OFFICIAL]
- `skills/continuous-learning-v2/scripts/` directory listing — `detect-project.sh`, `instinct-cli.py`, `test_parse_instinct.py` [OFFICIAL]
- Directory listings for `hooks/`, `agents/`, `scripts/` via GitHub API [OFFICIAL]

**Momentum local repo — directly read:**
- `skills/momentum/skills/distill/SKILL.md` and `workflow.md` — `/Users/steve/projects/momentum/` [OFFICIAL]
- `skills/momentum/skills/triage/SKILL.md` and `workflow.md` — `/Users/steve/projects/momentum/` [OFFICIAL]
- `_bmad-output/implementation-artifacts/intake-queue.jsonl` (first 25 lines) — `/Users/steve/projects/momentum/` [OFFICIAL]

**Prior research context — read for background:**
- `raw/research-feature-parallels.md` — verified earlier parallel analysis [OFFICIAL]
- `raw/research-ecc-superior.md` — verified earlier ECC-superior analysis [OFFICIAL]

All ECC behavioral claims are tagged [OFFICIAL] when sourced directly from ECC files. Claims about expected behavior not explicitly stated in source files are tagged [UNVERIFIED]. Momentum-specific practice notes from memory or rules files are tagged [PRAC].
