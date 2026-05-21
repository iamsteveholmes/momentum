---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "What would change in Momentum if Gas Town took over dispatch? How do sprint-dev, intake, quick-fix, retro map to Gas Town?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

## What Gas Town Is and Why the Question Matters

Gas Town is a multi-agent workspace manager built by Steve Yegge and released in January 2026 [OFFICIAL]. It coordinates fleets of AI coding agents (primarily Claude Code) across git repositories using a structured hierarchy of specialized roles, a persistent Git-backed state store called Beads, and a workflow abstraction called Molecules. By v1.0 in April 2026, it had stabilized enough to claim production-ready status [PRAC].

Momentum currently runs without a persistent dispatcher. A human starts a Claude Code session, invokes a skill (e.g., `momentum:sprint-dev`), and that session acts as the orchestrator — spawning subagents via the Agent tool, waiting for results, and merging. When the session ends, the orchestrator is gone. State lives in story files, `sprints/index.json`, and git history; there is no watchdog, no merge queue, and no ability to restart mid-sprint if the orchestrating session dies.

The question is whether Gas Town's dispatcher model — persistent Mayor, Polecat workers, Witness health monitoring, Refinery merge queue — could replace or augment Momentum's session-local orchestration, and what the cost of that migration would be.

---

## Gas Town's Core Primitives

Understanding the mapping requires a clear picture of Gas Town's abstractions [OFFICIAL]:

**Beads**: Atomic work units stored as JSONL in Git. Every piece of work — from a single task to a sprint epic — is a Bead with a unique ID, status, and full event log. The Beads database is queryable via SQL and survives any agent crash because it lives in git. [OFFICIAL]

**Molecules / Formulas**: A Formula is a TOML-defined multi-step workflow template. When "cooked," it becomes a Protomolecule (a frozen template), which can be "poured" into a live Molecule — an instantiated, step-tracked workflow graph. Steps are marked `in_progress` before execution and `closed` immediately after, creating a timestamped audit ledger. The canonical Shiny Workflow is `design → implement → review → test → submit`. [OFFICIAL]

**Polecats**: Ephemeral worker agents. Each Polecat gets a git worktree, a slot name (e.g., "Toast"), and an assigned Bead. It runs the assigned work and calls `gt done` when complete, which pushes the branch, submits to the Refinery merge queue, and self-nukes the agent. There is no idle state — a Polecat is working, stalled, or done. [OFFICIAL]

**Mayor**: The persistent, singleton global coordinator. It receives high-level goals, decomposes them into Beads, assigns Polecats, monitors convoy status, and surfaces only actionable information to the human operator. The Mayor is always running; it is not a session that starts and ends. [OFFICIAL]

**Witness / Deacon / Refinery**: The three-tier health and merge system. Witness monitors per-rig Polecat health, detects stalls, and triggers recovery. Deacon runs cross-rig patrols. Refinery processes the merge queue using a Bors-style bisecting strategy. None of these require human intervention for normal operation. [OFFICIAL]

**Convoys**: Batches of Beads grouped for coordinated delivery. A convoy is the "single view of what's in flight" — analogous to a sprint slice. Convoys can span rigs and provide historical records. [OFFICIAL]

**The Propulsion Principle**: "If you find something on your hook, YOU RUN IT." Agents don't wait for permission after assignment. The hook is checked at startup; if work exists, it begins immediately. [OFFICIAL]

---

## How sprint-dev Would Map

Momentum's `sprint-dev` flow is: read the sprint, identify ready stories, spawn one dev agent per story in parallel (each in its own worktree), wait for all merges, then run AVFL post-merge validation.

Gas Town's equivalent is structurally close but mechanically different in three ways:

**1. The Convoy replaces the sprint slice.** In Gas Town terms, a Momentum sprint would be modeled as a Convoy — a named batch of Beads (stories). `sprint-dev` currently reads `sprints/index.json` to find the active sprint's stories. Under Gas Town, the orchestrator would instead create a Convoy containing one Bead per ready story, then `gt sling` each Bead to an available Polecat slot. [OFFICIAL]

**2. Polecats replace Agent tool spawns.** Momentum today calls the Agent tool once per story. Gas Town replaces this with `gt sling <bead-id> <rig>`, which allocates a named Polecat slot, creates a worktree, and starts a Claude Code session with the Bead on the hook. The Polecat then executes the story via its own session — not a child of the orchestrating session. This is a critical difference: Gas Town's workers are **independent peer sessions**, not Agent-tool subprocesses. The orchestrator doesn't block waiting for them. [OFFICIAL]

**3. The Refinery replaces manual merge logic.** Momentum's `sprint-dev` currently has the orchestrator merge each worktree branch after the dev agent signals completion. Gas Town's Refinery runs this continuously as a background process — when a Polecat calls `gt done`, the branch goes into the Refinery queue automatically. The Refinery handles ordering, conflict detection, and verification gates. [OFFICIAL]

**What stays the same:** The worktree-per-story model is already how Momentum works. Gas Town formalizes and automates what Momentum does manually: worktree creation, branch naming, post-merge cleanup, and progress visibility. Momentum's `sprint-manager` would need to write Beads instead of updating `stories/index.json` directly, but the conceptual model is compatible.

**What changes structurally:** The orchestrating session no longer blocks on story completion. Under Gas Town, `sprint-dev` would become a Convoy creation script rather than a long-running orchestrator. Monitoring shifts from `gt feed` (Gas Town's TUI) instead of watching the Claude session scroll. The human's approval gate for pushes would route through Gas Town's escalation API rather than a session-level approval prompt.

**AVFL post-merge** is the least clean fit. Momentum runs AVFL as a multi-lens validation pass after all stories merge. Gas Town has no built-in parallel-lens validation step. AVFL would need to be modeled as a Formula (a Molecule with steps: enumerate-findings → adversarial-review → fix → re-validate), poured after the sprint Convoy reaches 100% completion. The Deacon could trigger this automatically via a plugin gate on convoy-completion events. [PRAC]

---

## How intake Would Map

Momentum's `intake` is a lightweight single-turn operation: capture a story idea, write a stub to the backlog. It has no persistent state requirements — a single session runs, writes a `.md` file, and exits.

**Gas Town mapping:** `intake` maps almost directly to Bead creation — `bd new` with a description and a rig assignment. The key question is who runs intake in Gas Town's model. Gas Town assumes the Mayor handles high-level decomposition; a human describes a feature, the Mayor creates the Beads. Momentum's `intake` is designed to be invoked mid-conversation to capture an idea before context is lost. [PRAC]

The fit here is good but requires a naming convention: Momentum backlog stories would be Gas Town Beads with a `status: backlog` tag and no rig assignment yet. `sprint-planning` would then query backlog Beads, select a subset, assign to rigs, and add to a new Convoy. This is exactly how Gas Town's Mayor is designed to work. [OFFICIAL]

**What changes:** Story files (`.momentum/stories/*.md`) would become Beads in the Gas Town Beads DB. The Markdown frontmatter format Momentum uses (status, epic_slug, change_type, etc.) would need to be preserved either as Bead metadata fields or as attached documents linked to the Bead. Gas Town's Beads are JSON-structured, not Markdown-first, so Momentum's rich story format (with EDD/TDD sections, Gherkin specs) would likely live as a linked artifact rather than the Bead itself. [UNVERIFIED]

---

## How quick-fix Would Map

Momentum's `quick-fix` is a single-story end-to-end cycle: define → implement → validate → merge, all in one session. It's the smallest unit of autonomous work in the practice.

**Gas Town mapping:** This is the **canonical Polecat use case**. The Shiny Workflow formula (`design → implement → review → test → submit`) is nearly identical to quick-fix's `define → implement → validate → merge` sequence. A `quick-fix` invocation would:

1. Create a Bead with the story spec
2. Cook the Shiny Workflow formula into a Molecule attached to the Bead
3. Sling the Bead to one Polecat
4. Let the Polecat self-drive through the Molecule's steps, closing each on completion
5. `gt done` triggers Refinery merge

The key advantage Gas Town adds: crash recovery. If the Claude session dies mid-implement, the Polecat slot persists, the Molecule step is still `in_progress`, and the next session can pick up via `gt prime` (context recovery from predecessor seances). Momentum's current `quick-fix` has no crash recovery — if the session dies mid-fix, work is lost. [PRAC]

**What changes:** The quick-fix "define" phase (Momentum's spec writing with the PM agent) would need to happen before Bead creation, or be modeled as early Molecule steps assigned to a Crew agent (the persistent design worker) rather than a Polecat. Gas Town distinguishes between design work (Crew, persistent) and implementation work (Polecat, ephemeral). Momentum's quick-fix currently conflates these in one session. [UNVERIFIED]

**What doesn't change:** The worktree isolation model. Quick-fix already creates a worktree per fix. This is exactly the Polecat pattern.

---

## How retro Would Map

Momentum's `retro` is the most complex workflow to map. It involves: reading the sprint transcript (via DuckDB), spawning parallel auditor agents with TeamCreate for collaborative analysis, synthesizing findings, and writing a retrospective document.

**Gas Town mapping:** This is the hardest fit. Gas Town's parallelism model is **peer Polecats working on independent Beads** — not collaborating agents sharing context. Momentum's retro auditor team is explicitly collaborative: auditors read each other's findings, cross-reference, and the Documenter requests deeper investigation from specific auditors. [PRAC]

Gas Town has no built-in TeamCreate equivalent. The closest mechanism is Crew agents (persistent workers with dedicated clones) that communicate via the Mail protocol — but Gas Town's mail is asynchronous and routed, not the synchronous back-and-forth that Momentum's retro TeamCreate enables. [OFFICIAL]

**Option A: Force-fit to Gas Town parallelism.** Model each auditor lens as an independent Bead, sling each to a separate Polecat, and collect output artifacts via the Convoy completion event. Synthesis would be a final Molecule step run by the Mayor after all auditor Beads close. This loses the collaborative cross-referencing but gains crash recovery and structured output ledger. [UNVERIFIED]

**Option B: Keep retro outside Gas Town.** The retro is a low-frequency, high-coordination workflow. Running it as a Momentum session-local workflow (current model) while routing sprint-dev and quick-fix through Gas Town would be a pragmatic split. Gas Town's Convoy completion data would feed the retro as input rather than the retro running inside Gas Town. [UNVERIFIED]

**Option C: Deacon plugin trigger.** Gas Town's plugin system allows Markdown+TOML plugins with cron or event triggers. A retrospective plugin triggered on Convoy 100% completion could kick off a retro workflow — but it would run as a Dog worker (infrastructure helper), not with the full agent context that Momentum's retro needs. This would require significant architectural work in the plugin layer. [PRAC]

---

## What Would Need to Change in Momentum's Architecture

A Gas Town adoption is not a superficial configuration change. It requires rearchitecting Momentum's state layer, orchestration model, and approval gating:

**1. Replace story files with Beads.** Momentum's `.momentum/stories/*.md` format is the source of truth for story state. Gas Town's Beads DB would become the source of truth instead. Story Markdown would become an attached artifact (linked document), not the primary record. The `sprint-manager` skill, which exclusively writes `stories/index.json` and `sprints/index.json`, would need a Gas Town equivalent that writes to the Beads DB. [UNVERIFIED]

**2. Replace the session-local orchestrator with the Mayor.** Momentum's `sprint-dev` is a long-running Claude Code session that blocks on subagent completion. Gas Town's Mayor is a persistent coordinator that dispatches work and monitors via the feed TUI. The human-facing interaction model changes from "talk to the orchestrator" to "talk to the Mayor, monitor via `gt feed`." [OFFICIAL]

**3. Reroute human approval gates.** Momentum requires human approval before git push. Gas Town's escalation API (`gt escalate`) routes blockers by severity through Deacon → Mayor → Overseer. Push approval would need to be modeled as a CRITICAL escalation requiring Overseer (human) confirmation before the Refinery executes a push-to-remote step. [OFFICIAL]

**4. Model Momentum's change-type taxonomy in Gas Town's schema.** Momentum classifies stories by `change_type` (code, agent, rule, doc, spike) to route them to appropriate dev skills. Gas Town's Polecats are generic — they execute whatever is on their hook. Momentum's routing logic would need to be encoded into the Formula or into the Claude Code prompt attached to the Bead, not into Gas Town's dispatch layer natively. [UNVERIFIED]

**5. AVFL has no Gas Town equivalent.** Gas Town has no parallel validation lens system. AVFL would remain a Momentum-native workflow, triggered as a post-Convoy step either via a Deacon plugin or by the human operator. The integration point is the Convoy completion event, not a Gas Town-internal primitive. [UNVERIFIED]

---

## Structural Compatibility Assessment

| Momentum Concept | Gas Town Equivalent | Fit |
|---|---|---|
| Sprint | Convoy | Good — both batch multiple work items for delivery |
| Story | Bead | Good — atomic tracked work unit; Markdown artifact linked |
| Worktree-per-story | Polecat worktree | Excellent — identical isolation model |
| Agent tool spawn | `gt sling` + Polecat | Good — different mechanism, same intent |
| Orchestrator session | Mayor + Deacon | Partial — Mayor is persistent; orchestrator session is not |
| Manual merge | Refinery merge queue | Good — Refinery automates what Momentum does manually |
| AVFL | No equivalent | Poor — requires external integration or workaround |
| Retro TeamCreate | No equivalent | Poor — collaborative multi-agent loop not supported |
| intake | Bead creation | Good — thin wrapper on `bd new` |
| quick-fix | Shiny Workflow Molecule | Excellent — canonical Polecat use case |
| Human push approval | Escalation API | Partial — requires Overseer role configuration |
| sprint-manager writes | Beads DB writes | Requires new integration layer |
| Sprint-planning | Mayor decomposition | Partial — Mayor does AI-driven decomposition; Momentum uses human-curated story selection |

---

## Key Risks and Gaps

**Gas Town is not designed for Momentum's planning discipline.** Gas Town's Mayor does AI-driven decomposition from high-level feature prompts. Momentum's sprint-planning is human-curated story selection from a pre-groomed backlog. These are philosophically different: Gas Town optimizes for "describe a feature, get it built"; Momentum optimizes for "deliberate story prioritization with human approval at each gate." Adopting Gas Town's Mayor would require resisting the pull of its "just describe the feature" model. [PRAC]

**The Beads DB is Dolt-backed, not plain git.** Gas Town requires Dolt (a MySQL-compatible version-controlled database) for the Beads DB. This is a significant infrastructure dependency Momentum doesn't currently have. [OFFICIAL]

**Gas Town targets Stage 7-8 developers running 20-30 parallel agents.** Momentum is designed for a solo developer with one sprint at a time. The cost ($100/hour token burn at full capacity) and complexity of Gas Town are calibrated for much higher throughput than a single-person Momentum sprint. [PRAC]

**Session-local orchestration vs. persistent daemon is a workflow culture shift.** Momentum's model puts the human in the driver's seat of a session. Gas Town puts the Mayor in the driver's seat of a persistent system. This is not just a technical change — it changes how the developer interacts with their practice daily. [PRAC]

---

## Sources

- [Gas Town Docs — Architecture Overview](https://docs.gastownhall.ai/) [OFFICIAL]
- [Gas Town Docs — Polecat Lifecycle](https://docs.gastownhall.ai/concepts/polecat-lifecycle) [OFFICIAL]
- [Gas Town Docs — Molecules and Formulas](https://docs.gastownhall.ai/concepts/molecules) [OFFICIAL]
- [Gas Town Docs — Propulsion Principle](https://docs.gastownhall.ai/concepts/propulsion-principle) [OFFICIAL]
- [Gas Town Docs — Federation Architecture](https://docs.gastownhall.ai/design/federation) [OFFICIAL]
- [Gas Town Docs — Agent Identity](https://docs.gastownhall.ai/concepts/identity) [OFFICIAL]
- [Gas Town Docs — Plugin System](https://docs.gastownhall.ai/design/plugin-system) [OFFICIAL]
- [GitHub — gastownhall/gastown (README)](https://github.com/gastownhall/gastown) [OFFICIAL]
- [GitHub — gastownhall/gascity (README)](https://github.com/gastownhall/gascity) [OFFICIAL]
- [Steve Yegge — Gas Town: from Clown Show to v1.0 (Medium, Apr 2026)](https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec) [PRAC]
- [Steve Yegge — Welcome to Gas Town (Medium)](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) [PRAC]
- [Better Stack — Building with Gas Town: Multi-Agent AI Development Guide](https://betterstack.com/community/guides/ai/gas-town-multi-agent/) [PRAC]
- [re-cinq — Multi-Agent Orchestration: BMAD, Claude Flow, and Gas Town](https://re-cinq.com/blog/multi-agent-orchestration-bmad-claude-flow-gastown) [PRAC]
- [Maggie Appleton — Gas Town's Agent Patterns, Design Bottlenecks, and Vibecoding at Scale](https://maggieappleton.com/gastown) [PRAC]
- [paddo.dev — GasTown and the Two Kinds of Multi-Agent](https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/) [PRAC]
- [Cloud Native Now — Gas Town: What Kubernetes for AI Coding Agents Actually Looks Like](https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/) [PRAC]
- [Torq Software Reading List — Gas Town Multi-Agent Orchestration Framework](https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/) [PRAC]
