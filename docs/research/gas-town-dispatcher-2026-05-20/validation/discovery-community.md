---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas City community health, communication channels, similar pipeline patterns in the wild"
---

# Gas City Community Health — Discovery Research

## Research Question

Is the Gas City / Gas Town Hall community large, active, and healthy enough to provide meaningful support if Momentum adopts Gas City's Orders system as its dispatch layer? Are there practitioners building multi-stage pipelines with fix loops, barriers, and human review loops similar to what Momentum needs? What are the documented pain points and known workarounds?

## Sources Consulted

- `github.com/gastownhall` org API — all 18 repositories, with full issue/discussion enumeration
- `github.com/gastownhall/gascity` — issues (open + closed), discussions, contributors, commits
- `github.com/gastownhall/gastown` — discussions, issues, forks, watchers
- `github.com/gastownhall/gascity-packs` — full directory tree, all pack READMEs
- `github.com/gastownhall/gascity-packs/pr-pipeline` — PR pipeline pack README
- `github.com/gastownhall/gascity-packs/pr-review` — PR review pack README with `mol-adopt-pr` details
- `github.com/gastownhall/gascity-packs/flywheel` — Flywheel subpack group README
- `github.com/gastownhall/gascity-packs/discord` — Discord pack README
- `github.com/gastownhall/gascity-packs/discord-intake` — Discord intake pack README
- `github.com/gastownhall/gascity-packs/slack-pack` — Slack pack README
- `github.com/gastownhall/gascity-packs/github-intake` — GitHub intake pack README
- `github.com/gastownhall/gascity-packs/rlm` — RLM pack README
- `github.com/gastownhall/gascity/issues/1709` — "Proposal: Orchestration v3" (20 comments)
- `github.com/gastownhall/gascity/issues/2311` — `waits_for = "children-of(X)"` barrier bug
- `github.com/gastownhall/gascity/issues/2131` — dispatcher wedge P1 bug
- `github.com/gastownhall/gascity/issues/2168` — order-tracking watchdog scope P1 bug
- `github.com/gastownhall/gascity/issues/1181` — parallel dispatch clobber (shared working tree)
- `github.com/gastownhall/gascity/issues/1189` — `quorum(N)` gate type feature
- `github.com/gastownhall/gascity/issues/1202` — Policy hook points proposal
- `github.com/gastownhall/gascity/issues/2049` — Sequential pool chains poll latency
- `github.com/gastownhall/gascity/issues/1056` — Pool over-scaling on formula fanout
- `github.com/gastownhall/gascity/issues/622` — Webhook trigger for orders
- `github.com/gastownhall/community/README.md` — Discord invite link, org description
- `github.com/gastownhall/marketplace/README.md` — Wasteland plugin, marketplace overview
- `github.com/gastownhall/wasteland/issues` — Wasteland federation issues list
- `github.com/gastownhall/gascity-otel/README.md` — OTel observability stack README
- `gastownhall.ai/about/` — Website about page, contact, Discord link
- `seanmartinsmith/beadstui` — Community-built TUI for Beads
- `paddo.dev/blog/gastown-two-kinds-of-multi-agent/` — practitioner architectural analysis
- `reviewcommit.substack.com` — Gas Town review: community health, pain points
- `news.ycombinator.com/item?id=46734302` — HN thread (limited technical content)
- Prior corpus files: `research-maturity-production-readiness.md`, `followup-gas-town-vs-gas-city-distinction.md`, `raw/practitioner-notes.md`

---

## Findings

### 1. Community Communication Channels

**Discord — confirmed, two valid invite links.**

CONFIRMED. The community README at `gastownhall/community` documents the Discord as the primary real-time support channel:
- Invite link from community README: `https://discord.gg/gastownhall` [OFFICIAL]
- Invite link from gastownhall.ai/about: `https://discord.gg/xHpUGUzZp2` [OFFICIAL]

Both links point to the same Gas Town Hall Discord server. The website lists Discord as the first support channel, above both X/Twitter and the support email. The about page directs users to Discord for "support, questions, or feedback." [OFFICIAL]

Member count reported in prior research: 2,000+ as of the v1.0 announcement in April 2026. No updated count is displayed on public-facing pages. [CONFIRMED from prior corpus; current count UNKNOWN]

**No Slack workspace.** No reference to Slack in any official source. The Slack pack in `gascity-packs` is an integration tool (bots inside Gas City cities connecting to external Slack workspaces), not a Gas Town Hall community workspace. [CONFIRMED — absence]

**No mailing list or traditional forum.** [CONFIRMED — absence from all official sources]

**GitHub Discussions — active but thin.** Gas Town (`gastownhall/gastown`) has 30+ Discussion threads (mostly Q&A category), the majority from January 2026 when the project was new. The `gastownhall/gascity` repo has only 2 Discussion threads — one administrative (label/triage policy, March 2026) and one from a community member offering help (April 2026), both with 0 replies. [OFFICIAL — GitHub Discussions API]

**GitHub Issues — primary technical channel.** The core team uses GitHub Issues as the primary venue for technical discussion. The "Labels and Triage" discussion from Julian Knutsen explicitly documents how issues are organized and reviewed. Recent issues (May 19–22, 2026 range) have maintainer acknowledgments within hours to days. The `kind/design` label is used for proposals requiring community input. [OFFICIAL]

**X/Twitter: `@gastownhall`.** Used for announcements. Chris Sells (csells on GitHub, with 23 commits to gascity) is listed as the creator and maintainer of Gas Town Hall. [OFFICIAL]

**Response quality and speed — INFERRED.** Based on issue metadata: P1 bugs filed in May 2026 show 0–3 comments and recent activity within days. The Orchestration v3 proposal received 20 comments within 48 hours of filing (2026-05-05 through 2026-05-07). Julian Knutsen (2,605 commits, dominant contributor) has committed four fixes on 2026-05-22 alone. Core team responsiveness appears high for bugs; open issues accumulate at a high rate (404 open in gascity), suggesting triage throughput may be lagging behind intake. [INFERRED]

---

### 2. Community Size and Health Signals

**Contributor concentration is high and concerning.**

CONFIRMED. The gascity contributor breakdown is stark:

| Contributor | Commits |
|---|---|
| julianknutsen | 2,605 |
| sjarmak | 106 |
| quad341 | 103 |
| eric-jones | 28 |
| GraemeF | 24 |
| csells | 23 |
| (remaining 14+) | 9–21 each |

Julian Knutsen owns approximately 2,605 of an estimated 3,500+ commits (~74% of the codebase). The next-most-active contributor (sjarmak) has 106. This is a bus-factor-1 risk for the core SDK. The prior research claimed "450 unique contributors" across Gas Town and Beads combined — but across all three repos, not just gascity. The gascity-specific contributor distribution is heavily concentrated. [OFFICIAL — GitHub Contributors API]

**Repo health metrics (as of 2026-05-22):**
- `gascity`: 254 forks, 807 watchers, 404 open issues, 13 subscribers, pushed 2026-05-22
- `gastown` (legacy): 1,439 forks, 15,509 watchers, 218 open issues, pushed 2026-05-22
- `gascity-packs`: 8 forks, 6 open issues, pushed 2026-05-22
- `wasteland`: 27 forks, 17 open issues, pushed 2026-05-22
- `gascity-otel`: 1 fork, 0 open issues, pushed 2026-05-22

Gastown's significantly higher watcher count (15,509 vs 807) reflects name recognition — users who starred the original repo have not all migrated to following gascity. This suggests the community is larger than gascity's raw numbers indicate, but many members have not yet transitioned to following the actively-developed repo. [OFFICIAL]

**Issue velocity is accelerating.** The gascity open issue count grew from 262 (prior research, May 20) to 404 (current, May 22) — a gain of 142 issues in approximately 2 days. This is unusual, suggesting a batch of community contributions or auto-filed issues from Gas City's own internal tracking system. Given that several issues in the feature list show `Integrate/<name> pr <number>` titles and that Gas City uses Gas City to build itself ("dogfooding" is referenced in multiple sources), this spike may reflect the project's own self-referential issue generation. [INFERRED — issue content supports dogfooding hypothesis; UNKNOWN — cannot confirm without reading individual issues]

**Community events — UNKNOWN.** No office hours, AMAs, or meetups are advertised on any official source. The Wasteland federation (a community work board built on Dolt) serves as an asynchronous community coordination mechanism, but it is not a real-time event venue. [UNKNOWN]

**Question-to-answer ratio — UNKNOWN.** GitHub Discussions data shows low comment counts on most threads (many at 0–1). Discord activity cannot be assessed without joining the server. The prior corpus notes "actively moderated" Discord but provides no Q/A ratio data. [UNKNOWN]

**Third-party integrations in active development.**

CONFIRMED. The following third-party community projects were found:

- `beadstui` (seanmartinsmith) — TUI for Beads, alpha/v0.1.0, ~92k lines of Go, substantial engineering. The author is actively engaged in the Orchestration v3 GitHub issue (#1709 comment on 2026-05-07), requesting Run-ID propagation features specifically for his viewer. [PRAC]
- `CHROTE` — "web dashboard that lets you run AI coding agent swarms from anywhere, on any device" (Gastown Discussions #806, January 2026). Status UNKNOWN. [PRAC]
- `Cortex` — CLI tool for AI to map and explore codebases (Gastown Discussions #704). Status UNKNOWN. [PRAC]
- Flywheel pack group (`cass`, `cm`, `mcp-agent-mail`, `ubs`) — community-contributed subpacks for inter-agent messaging, session search, persistent memory, and bug scanning. Packaged in the official `gascity-packs` repo. [OFFICIAL]
- Slack pack (`slack-pack`) — a community-built port of the official discord pack to Slack. Status: preview/v0.1.0 scaffold; not yet at full discord-pack parity but functional for "multi-session oversight loop end-to-end." [OFFICIAL]

---

### 3. Practitioners Building Similar Pipelines

**The "Orchestration v3" proposal is the most significant finding for Momentum.**

CONFIRMED. Gas City's own maintainers have an open proposal (#1709, filed 2026-05-05, 20 comments) that directly articulates the exact patterns Momentum needs. Key provisions:

**First-class HITL (Human-In-The-Loop):** The proposal defines HITL as a "runtime disposition class with its own pause / notify / authorization machinery" (S4, S5). A formula step can declare a HITL checkpoint; the Run pauses and the human approves/rejects/comments before the Run continues. Rejection terminates the Run via hard-fail. HITL state survives controller restarts. The proposal explicitly defers multi-channel notification and escalation chains, so the initial implementation will be dashboard-only approval. [OFFICIAL — Issue #1709 body, R12–R14]

**Scatter/gather (fan-out → fan-in with policy):** The O3 proposal adds scatter/gather as a first-class sub-formula. Multiple specialized reviewers run in parallel; a gather phase combines verdicts via an author-declared policy (e.g., "pass if 4 of 5 reviewers pass"). Gather policy is expressed in TOML using a condition language that extends Gas City's existing `internal/formula/condition.go`. An escape hatch allows an agent step to make the gather judgment. [OFFICIAL — Issue #1709, S3, R15, TC5]

**Convoy-level barrier:** O3 adds the concept of a "drain" — a loop that parallelizes implementation across beads and only considers the step complete at quiescence (no ready beads, no in-flight workers). This is the barrier pattern for a fan-out across a convoy. [OFFICIAL — Issue #1709, P1, P2]

**Status of O3:** The proposal is in the design/discussion phase (labeled `kind/feature`, 20 comments, no `status/in-progress` label as of May 22). It is not yet implemented. Chris Sells (csells) is the author and active responder. The timeline for O3 implementation is UNKNOWN.

**The `pr-pipeline` and `pr-review` packs demonstrate existing multi-stage pipeline patterns with human gates.**

CONFIRMED. These community packs exist in the official `gascity-packs` repo and demonstrate:

- `pr-pipeline/mol-pr-ship`: A 4-stage pipeline (simplify → self-review iterate → mechanical gates → readiness report) that **stops** at the report and requires explicit human push. This is a soft gate — the formula stops and waits for human action. [OFFICIAL]
- `pr-review/mol-adopt-pr`: A 6-step formula (intake → rebase-check → review → human-gate → finalize → complete) where **step 4 is a hard human gate**: `bd close <human-gate-step-id>` is the only path to continuation. The human reviews parallel multi-model output (Claude + Codex + Gemini) before the formula can finalize and merge. [OFFICIAL]

The `mol-adopt-pr` human gate pattern is the closest existing community example of a human review loop in Gas City. The mechanism is low-tech (`bd close` on a bead) but functional — it blocks step progression until a human explicitly closes the gate bead. This is Gas City v2 formula behavior, predating the O3 HITL system.

**Sequential pool chains with multi-phase pipelines — confirmed in production.**

CONFIRMED. Issue #2049 (filed 2026-05-13) documents a practitioner running a "5-phase SDLC chain" (worker → tester → reviewer → documenter → finalizer) on a single rig. The issue includes empirical timing data from a live run:

| Phase | Duration | Gap to next phase |
|---|---|---|
| worker | 12m 32s | 3m 43s |
| tester | 2m 54s | 2m 47s |
| reviewer | 3m 42s | 2m 20s |
| documenter | 3m 4s | 2m 50s |

The cumulative inter-phase gap was 11m 40s against 22m 12s of actual work — a **52% latency tax** from poll-based pool scaling. The issue is labeled `kind/feature, priority/p2` and is open. [OFFICIAL — Issue #2049]

This pattern — sequential pipeline phases with pool workers — is directly analogous to what Momentum needs (sprint-dev → code review → QA → merge → AVFL → E2E → human review). The 2-4 minute inter-phase transition latency would be a real cost in Momentum's pipeline.

**No documented community examples of corpus-level AVFL fix loops.**

UNKNOWN. No issues, discussions, or packs describe a post-merge corpus-level validation + fix loop pattern equivalent to Momentum's AVFL phase. The closest approximation is the `ubs` (pre-commit bug scanning) subpack in Flywheel, which runs scanning before individual commits — not corpus-level post-integration. [UNKNOWN]

**No documented community examples of worktree-parallel sprint pipelines.**

UNKNOWN. The Gas Town colony (Mayor → multiple Polecats on isolated worktrees) is conceptually similar to Momentum's parallel story dispatch, but the documented Gas City community packs focus on single-rig, sequential-phase workflows. No community pack demonstrates a Gas City-native fan-out across N worktrees with a post-merge barrier. [UNKNOWN]

**CI/CD-style orchestration — INFERRED use but not documented as a pattern.**

INFERRED. The github-intake and discord-intake packs enable external event-triggered dispatch: a GitHub issue comment (`/gc fix`) or Discord message triggers a formula run. The github-intake README's `mol-github-fix-issue` workflow is explicitly framed as a TDD bugfix pipeline. These are CI-adjacent but not full multi-stage pipelines. The webhook trigger for Orders (Issue #622) is a requested feature, not yet implemented. [OFFICIAL for existing packs; INFERRED for CI/CD framing]

---

### 4. Known Issues and Community Pain Points

**Critical (P1) open bugs relevant to Momentum's pipeline model:**

**4a. Barrier primitive is broken (Issue #2311, P2, open).**

CONFIRMED. `waits_for = "children-of(X)"` — the only native Gas City barrier for fan-out/fan-in — does not work correctly when the parent step uses `on_complete` bond fanout. The bug causes step B to become claimable before step A's fanout children have run. The root cause: `waits_for` creates a tracking dep edge against the parent step at plan time (when no children exist yet), but `bd ready` gates only on `blocks` edges, not `waits_for` edges. Step A "closes" when the bond *schedules* the fanout, not when children complete. Result: step B can run before any fanout child has written its output. [OFFICIAL — Issue #2311]

The documented workarounds from the issue reporter:
- Retry-with-sleep in step B's bash (fragile, brittle)
- Restructure step B as a `[[steps.children]]` sibling of A (only works in limited topologies)
- Add `needs = ["A"]` alongside `waits_for` (only gates on A closing, not on A's fanout children)

None of the workarounds fully solve the race. The issue author proposes a runtime fix (insert blocks edges at bond-expansion time), which has not yet been accepted. [OFFICIAL]

**4b. Dispatcher can wedge permanently from ghost tracking beads (Issue #2131, P1, in-progress).**

CONFIRMED. The `order-tracking-sweep` order can self-wedge, accumulating ghost tracking beads that block every recurring order from re-firing. Recovery requires manual `bd close` on affected tracking beads; the automatic watchdog cannot self-heal because the watchdog's own tracking bead is one of the ghosts. The city becomes "functionally inert" until manually recovered. This was observed in production on a city with 19 always-on sessions running 12–24 hours. [OFFICIAL — Issue #2131, status/in-progress]

For Momentum: a persistent dispatcher (the key value proposition of Gas City Orders) that can wedge undetected after a day of operation is a significant operational risk for an automated sprint pipeline.

**4c. Order-tracking watchdog recovery fails after supervisor restart (Issue #2168, P1, open).**

CONFIRMED. After a `gc supervisor stop/start` cycle, open tracking beads from the previous run block order re-firing. The manual `gc order sweep-tracking` recovers immediately, but the automatic watchdog fails to recover within observed 30-minute windows. Any city restart (not just a crash — a clean stop/start) can require manual intervention to resume automated dispatch. [OFFICIAL — Issue #2168]

**4d. Parallel dispatch clobbers shared working tree (Issue #1181, P2, open).**

CONFIRMED. When two agents are dispatched in parallel to the same rig, they share a single working tree. Parallel branch switches clobber uncommitted edits. The issue was observed in practice during Gas City's own development (the gascity repo) and independently flagged by both agents involved. The fix requires Gas City to create isolated worktrees per agent for parallel dispatch — currently an unimplemented feature. [OFFICIAL — Issue #1181]

For Momentum: Momentum already creates isolated worktrees per story (the worktree-per-story pattern is established in sprint-dev). If Momentum uses Gas City for dispatch, the worktree isolation would still be Momentum's responsibility, not Gas City's. Gas City's shared-tree bug does not directly apply to Momentum's current model. [INFERRED]

**4e. Pool over-scaling when formula fanout children count as independent work (Issue #1056, P2, open).**

CONFIRMED. During a formula's intermediate fan-out step, child beads inherit the parent's `gc.routed_to` label and briefly appear as independent work items in the pool reconciler. The reconciler over-scales: a 3-way fanout causes `pool_desired` to spike from 1 to 4 (3 children + 1 follow-on step). Excess sessions spin up, claim nothing, and idle. [OFFICIAL — Issue #1056]

This is directly relevant to the fan-out → barrier → gather pattern Momentum needs. Each story dispatched in a sprint would be a fanout child; the reconciler would count each one as requiring its own session, causing pool thrash.

**4f. Sequential pool chain inter-phase latency (Issue #2049, P2, open).**

CONFIRMED. In sequential pipeline phases, pool scale-check is poll-based (30–60s tick). Each inter-phase transition pays 2–4 minutes of idle latency waiting for the reconciler to discover that the previous phase completed. In a 5-phase chain, this adds ~12 minutes of overhead against ~22 minutes of work. The event-driven fix (Issue #1945, merged) exists in the substrate but the reactor that consumes `session.stopped` events to trigger immediate scale-checks is not yet implemented. [OFFICIAL — Issue #2049]

**4g. PackV2 migration leaves schema in redesign (Issue #2120, P2, open).**

CONFIRMED (carried forward from prior research). Five tracks of post-PackV2 work remain incomplete: legacy surface deprecation, docs/implementation reconciliation, pack registry support, unified `gc pack` CLI, and pack reuse/customization. [OFFICIAL]

**Community workarounds documented:**

- Barrier race: retry-with-sleep in downstream bash (fragile) [OFFICIAL — Issue #2311]
- Dispatcher wedge: manual `bd close` on ghost tracking beads [OFFICIAL — Issue #2131]
- Human gate: `bd close <step-id>` on an explicit gate bead (pre-O3 pattern) [OFFICIAL — mol-adopt-pr]
- Pseudo-convoy hack: stuff entire work context into one bead to avoid per-bead formula runs seeing only fragments [OFFICIAL — Issue #1709 body, "pseudo-convoy hack" named explicitly]
- Sequential chain latency: no documented workaround; the poll gap is accepted as a known cost

---

### 5. Third-Party Ecosystem

**gascity-packs — officially sanctioned community packs repo.**

CONFIRMED. The `gastownhall/gascity-packs` repository is the designated home for community packs. As of 2026-05-22, it contains 13 top-level directories (packs or pack groups):

| Pack/Group | Purpose |
|---|---|
| `discord` | Discord provider extension (replaces `discord-intake`) |
| `discord-intake` | Superseded Discord intake; kept for migration reference |
| `flywheel` | Agent-enhancement group: mcp-agent-mail, cass, cm, ubs |
| `github-intake` | GitHub webhook intake for `/gc fix` slash commands |
| `jeffrey` | UNKNOWN (no README found in investigation) |
| `pr-pipeline` | Author-side PR discipline (4 formulas: plan, blast-radius, review, ship) |
| `pr-review` | Maintainer-side adopt-PR workflow with human gate |
| `rlm` | Recursive Language Model sidecar (long-context helper) |
| `slack-pack` | Slack provider extension (v0.1.0 preview, partial parity) |
| `tmux-theme` | Cosmetic tmux theming |

The `pr-pipeline` and `pr-review` packs together constitute the closest existing community example of a multi-stage pipeline with human review. The `discord` pack demonstrates bidirectional agent-to-human notification. The `flywheel/mcp-agent-mail` pack provides inter-agent messaging. [OFFICIAL]

**Pack registry — not yet implemented.**

CONFIRMED. Issue #2351 (filed 2026-05-19) is an open feature request to "add pack registry and gc pack dependency surface." Pack discovery is currently manual (browse the gascity-packs tree). There is no `gc search` or `gc marketplace` command. The `gastownhall/marketplace` repo hosts a Wasteland plugin for Claude Code's `/plugin marketplace` mechanism, but this is separate from Gas City's own pack distribution. [OFFICIAL]

**gascity-otel — observability stack.**

CONFIRMED. `gastownhall/gascity-otel` is an officially published Docker Compose stack providing VictoriaMetrics + VictoriaLogs + Grafana with pre-built dashboards. The dashboards cover agent lifecycle, bd call performance, session activity, token usage, and API latency. The stack accepts OTEL metrics/logs from both `gc` and `bd` via standard OTLP endpoints. Claude Code telemetry can optionally feed into the same stack. This is production-grade tooling for observing a Gas City city in operation. [OFFICIAL]

**Wasteland — federated work economy.**

CONFIRMED. `gastownhall/wasteland` is a separate federated work coordination system built on DoltHub. The `gastownhall/marketplace` repo provides a Claude Code plugin for participating in the Wasteland. The Wasteland is a community coordination mechanism (community members post work, claim tasks, earn reputation) but is not a Gas City dispatch mechanism — it is a separate system that uses Dolt but does not require Gas City. [OFFICIAL]

**beadstui — community TUI for Beads.**

CONFIRMED. A community-built terminal UI for Beads (`seanmartinsmith/beadstui`), in alpha/v0.1.0. ~92k lines of Go. Active author engagement with the Gas City core team in Issue #1709, requesting specific observability features for Run tracking. Not an official Gas Town Hall project. [PRAC]

**No third-party pipeline visualization tools specifically for Gas City found.**

UNKNOWN. Beyond the official Grafana dashboards in gascity-otel and the community beadstui, no pipeline-specific visualization or monitoring tools for Gas City were found. [UNKNOWN]

---

## Synthesis

### Community channel structure: Discord-primary, GitHub Issues for technical depth

Gas Town Hall runs a Discord-primary community model. The Discord server is the only documented real-time support channel (no Slack, no forum, no mailing list). GitHub Issues is the primary venue for technical proposals and bugs — the quality of technical discussion in Issues (e.g., Issue #1709's 20-comment Orchestration v3 thread, Issue #2311's detailed barrier bug with root-cause analysis and suggested fix) is high. GitHub Discussions are sparse in gascity and historically concentrated in the early Gas Town period.

For Momentum's support needs, the realistic support path is: Discord for orientation and community questions → GitHub Issues for technical bugs and feature requests. The core team (particularly Julian Knutsen, Chris Sells, and Stephanie Jarmak) is visibly active in both venues.

### Orchestration v3 is the pivotal community signal

The most significant finding is that Gas City's own maintainers have identified exactly the primitives Momentum needs — scatter/gather, first-class HITL, convoy-level barriers, sequential phase pipelines — and have documented a detailed architectural proposal (Orchestration v3, Issue #1709) for implementing them. This is not community speculation; it is a structured design from Chris Sells and the Gas City maintainer team, with detailed requirements, technical considerations, and migration plan.

The implication is two-sided. On one hand, it confirms that Momentum's needs are legitimate and within Gas City's intended design space. On the other hand, it means these primitives do not exist yet. Momentum would need to build on workarounds or wait for O3 implementation. The O3 timeline is UNKNOWN — the proposal has been in discussion for ~17 days with no `status/in-progress` label.

### The barrier bug is the highest-risk active defect for Momentum

Issue #2311 documents a confirmed bug in `waits_for = "children-of(X)"` — the only native barrier primitive for fan-out → fan-in synchronization. The bug causes downstream steps to become claimable before upstream fanout children complete. For Momentum's pipeline (dispatch N stories in parallel, wait for all to merge, then run AVFL), this is a correctness defect, not a performance issue. The workarounds are fragile. The fix is proposed but not yet accepted or implemented. Operating without a reliable barrier primitive means either accepting the race condition or building a custom barrier mechanism outside Gas City's formula system.

### Practitioner pipeline patterns exist but are not Momentum-scale

The `pr-pipeline` and `pr-review` packs demonstrate sequential multi-stage formulas with human gates. The `mol-adopt-pr` human gate (`bd close <step-id>`) is the community's current answer to human review loops. The sequential pool chain example (Issue #2049) documents a 5-phase SDLC pipeline with quantified inter-phase latency. These are encouraging existence proofs that Gas City can run multi-stage pipelines.

What does not exist: a community example of a sprint-level fan-out (N parallel story pipelines) with a corpus-level post-integration validation loop. Momentum would be pioneering this pattern. The questions about how to map Momentum's AVFL phase and sprint-level human approval gate to Gas City primitives remain unanswered at the community level.

### The dispatcher reliability bugs are a production risk

Two P1 open bugs (Issues #2131 and #2168) describe scenarios where Gas City's automated order dispatch stops firing after a clean supervisor restart or after extended operation. Manual recovery is required in both cases. For an automated sprint pipeline running unattended, a silent dispatcher wedge would halt the pipeline without notification. The Orchestration v3 proposal notes that HITL notification "survives controller restart" as a requirement — indicating the maintainers are aware that restart resilience is a gap. The gascity-otel observability stack mitigates this by enabling monitoring, but it doesn't prevent the wedge from occurring.

### Third-party ecosystem: thin but intentional

The ecosystem is young. The officially-sanctioned packs are high-quality but narrow (PR workflows, Discord/Slack integration, observability). There is no pack registry, no discovery mechanism, and no community pack for a sprint-level pipeline. The Flywheel group (inter-agent messaging, memory, bug scanning) and the RLM sidecar are the most general-purpose additions. The gascity-otel stack is production-grade observability.

For a Momentum integration, the relevant packs are: discord (for human notification in the review loop) and the human gate pattern from pr-review. Neither is directly usable without adaptation.

---

## Open Questions

1. **What is the O3 implementation timeline?** The Orchestration v3 proposal (Issue #1709) defines exactly the primitives Momentum needs but is not yet in development. Whether O3 lands in weeks, months, or remains a long-term design is the single most consequential unknown for Momentum's adoption decision.

2. **Is the barrier bug (Issue #2311) on the short-term fix schedule?** It is labeled P2 (not P1), suggesting it is below the P1 bugs in priority. Momentum cannot reliably use the `on_complete` bond fanout → `waits_for = "children-of(X)"` pattern without this fix.

3. **How active is the Discord server in practice?** The 2,000+ member count is the only public signal. Question response rate, time-to-answer, and proportion of questions answered by maintainers vs. community members are unknown without access.

4. **What is the O3 HITL notification mechanism?** The proposal commits to dashboard-only for the initial release. Momentum's human review loop requires human notification — if the dashboard is the only mechanism, practitioners must be watching a dashboard. Discord notification would require the discord pack. Is there a path to Discord-backed HITL notification before O3 lands?

5. **Does the dispatcher wedge (Issues #2131, #2168) have a monitoring path?** The gascity-otel Grafana dashboards include an "Agent Operations" dashboard with controller lifecycle events. Whether a wedged dispatcher produces a visible signal in the dashboard (vs. silently stopping order.fired events) would determine whether Momentum could detect and recover from this failure mode automatically.

6. **Is there a community Slack for Gas Town Hall members?** The absence of Slack from all official sources suggests no. But given the Slack pack is under active development, Slack may be used informally by some community members. [UNKNOWN]

---

## Community Verdict

**Community size:** The Gas Town Hall community is real and active at a scale uncommon for a 3-month-old open source project. The Discord exceeds 2,000 members; contributor count across the ecosystem is 450+; gastown has 15,509 GitHub watchers (though most track the legacy project). The gascity repo specifically is smaller (807 watchers, 254 forks) — the community has not fully migrated from the Gas Town namespace to Gas City.

**Community health:** Mixed. Positive signals: daily commits from multiple contributors, P1 bugs acknowledged and labeled within hours, high-quality technical proposals (O3) attracting substantive discussion, official packs showing production-quality engineering. Negative signals: contributor concentration (Julian Knutsen at ~74% of gascity commits is a bus-factor risk), issue intake exceeding triage throughput (404 open), two P1 dispatcher-reliability bugs open with no fix shipped, and the barrier primitive's confirmed bug with no accepted fix.

**Support path for a novel problem:** The realistic support path if Momentum hits a novel pipeline problem is: (1) Discord for initial orientation and community signal, (2) GitHub Issues for a well-documented bug report or feature request. Response from the core team for technical issues is fast (hours to days for P1 bugs). However, Momentum's use case — a non-coding-agent workflow using Gas City Orders for sprint orchestration — is at the frontier of what the community has documented. No existing pack or community example addresses the sprint-level fan-out → barrier → corpus-level validation → human approval pattern. Momentum would be the first practitioner to document and solve this at the community level.

**Actionable conclusion:** The community is large enough and the core team active enough that filing a well-scoped issue on a Momentum-specific integration question would receive a response. The community cannot provide a ready-made solution — Momentum would be building something novel. The core team's Orchestration v3 proposal shows they intend to support exactly this class of workflow, but the timeline is unknown. A PoC that validates Gas City's Orders system with the current `waits_for` workaround (retry-with-sleep or flag-file-based condition trigger) and documents the barrier gap as a GitHub issue would likely attract attention from the core team and could influence O3 prioritization.
