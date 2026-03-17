# RuFlo Risk Assessment and Momentum Fit Analysis

**Date:** 2026-03-15
**Analyst:** Research Agent (claude-sonnet-4-6)
**Subject:** ruvnet/ruflo (GitHub), v3.5.15, formerly ruvnet/claude-flow
**Momentum version context:** Pre-release, process backlog has 23 open tasks
**Research depth:** Maximum — direct source code inspection, GitHub API, issue tracker, release history, npm stats

---

## Executive Summary

RuFlo presents as an enterprise-grade AI orchestration platform with 21,225 stars, 60+ agents, swarm consensus protocols, and a Rust/WASM ML layer. **The reality uncovered by source inspection is substantially different.** The most critical finding is an open GitHub issue (filed 2026-03-09, still open 2026-03-15) providing a line-by-line audit showing that SONA, EWC++, HNSW, all 9 RL algorithms, and the WASM Agent Booster — every feature driving the headline performance claims — have either no implementation or are explicitly mocked/stubbed. The "Agent Booster" that powers the "250% subscription extension" claim resolves to a `// TODO: Call actual MCP tool here` comment that simulates edits by appending a comment to the file. The maintainer has not responded substantively to the audit.

For Momentum specifically: RuFlo's philosophy (runtime-heavy, dependency-rich Node.js orchestration layer) is architecturally opposed to Momentum's core advantage (zero-dependency markdown files installable without npm, Node.js, or PostgreSQL). There is no integration path that preserves Momentum's portability.

**Recommendation: Avoid.** Monitor only if the codebase gap between claims and implementation narrows substantially over the next 6 months.

---

## Part 1: Risk Registry

| Risk | Severity | Likelihood | Mitigation Options | Evidence |
|------|----------|------------|-------------------|----------|
| **R-01: Claimed features are unimplemented stubs** | Critical | Confirmed | None — requires re-evaluation from scratch | Issue #1326 (2026-03-09); direct source inspection of SONA, HNSW, Agent Booster, LoRA, consensus |
| **R-02: Single-maintainer bus factor** | High | High | Fork; pin to a release | 5,852 of 5,912 total contributions from ruvnet; "claude" (Anthropic bot) accounts for 50; external contributors account for 10 combined |
| **R-03: Excessive token consumption** | High | Confirmed | Agent-level token caps | Issue #1330 (2026-03-11): "thousands to millions of tokens within 0-30 minutes for simple tasks"; unresolved |
| **R-04: Version instability / breaking changes** | High | High | Pin exact version; integration test suite | Version history: v2.0.0-alpha → v2.7.4-alpha → v3.0.0-alpha.79 → v3.5.15 with release tags like `task-20250926-192626` (raw checkpoint tags); 5,960 commits in ~9 months; 13 patch releases in 5 days (v3.5.3 through v3.5.15) |
| **R-05: Supply-chain risk (install.sh curl-pipe)** | High | Medium | Pin SHA; use npm directly | `curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/claude-flow@main/scripts/install.sh | bash` — CDN serves from HEAD of main branch; no integrity hash; previously contained obfuscated preinstall script (removed in v3.5.3 per release notes: "Removed obfuscated preinstall script") |
| **R-06: Hardcoded credentials in public repo** | High | Confirmed for v2 | Upgrade to v3; don't use auth service | Security audit (2026-01-03): `admin@claude-flow.local` / `admin123`, `service@claude-flow.local` / `service123` hardcoded in `src/api/auth-service.ts` with SHA-256+static-salt hashing |
| **R-07: Claude Code tight coupling** | High | High | None — by design | Package name is `claude-flow` in package.json `bin`; MCP server name mismatch causes failures (issue #1344); entire value proposition depends on Claude Code hooks |
| **R-08: Claude Code hooks path fragility** | Medium | Confirmed | Use `$CLAUDE_PROJECT_DIR` | v3.5.15 was a hotfix for hooks path resolution breaking when Claude Code changes working directory; this is a structural coupling between RuFlo's hook system and Claude Code's internal CWD management |
| **R-09: Node.js/npm dependency chain fragility** | High | Medium | Lock dependencies; Docker | `better-sqlite3` binding failure on macOS ARM64 (issue #360, 2025-07-17); `npm ECOMPROMISED` cache corruption blocking installs (issue #1231); ESM/CJS interop failures in ruvector-training (issue #1334) |
| **R-10: PostgreSQL optional but load-bearing** | Medium | Medium | Stay on SQLite/AgentDB backend | RuVector production use requires PostgreSQL + custom `@ruvector/postgres-cli` extension (ADR-027); adds significant ops overhead |
| **R-11: Anthropic TOS / trademark** | Medium | Low-Medium | None needed; name changed | Project renamed from "claude-flow" to "ruflo"; package.json still uses `claude-flow` as binary name and `repository` URL; README retains "claude-flow" extensively; partial rename only |
| **R-12: "250% extension" claim** | Medium | Confirmed misleading | N/A — don't cite claim | The "250% extension" is predicated on the Agent Booster WASM engine routing simple edits away from the LLM at <1ms cost; the Agent Booster is a confirmed stub (`callAgentBooster` resolves to `// TODO` with simulated response appending a comment) |
| **R-13: Contributor injection / shady behavior** | Low-Medium | Unverified | Audit installed agent files | Issue #1323 (2026-03-09) alleges repo owner injects himself as contributor via agent tool descriptions; not independently verified in sampled agent files; maintainer not responsive |
| **R-14: "Kitchen sink" thin-implementation risk** | High | Confirmed | N/A — is actualized | 76 agent definitions, 93 slash commands, 28 skills, Raft/BFT/Gossip/CRDT, HNSW, SONA, EWC++, LoRA, 9 RL algorithms — the breadth is confirmed to be a documentation surface rather than implemented functionality |
| **R-15: Open issue backlog** | Medium | High | N/A | 467 open issues; 45 open in the sampled 100; issues covering daemon workers not firing, ESM/CJS interop, MCP tool failures, hook stdin hang, incorrect API key warnings, missing dist files — these are basic operational failures |
| **R-16: Self-developed security framework ("AIDefence")** | Medium | Medium | External audit required | AIDefence is an internal module; no CVEs in NVD for this project (project too young/obscure); security audit written by "Code Reviewer Agent" (self-review); hardcoded credentials in public repo undermine security claims |

---

## Part 2: Anthropic TOS / Rename Analysis

### The Rename

The project repository is `ruvnet/claude-flow`, which redirects to `ruvnet/ruflo` (GitHub redirects the old URL). This is a name change, not a new repository. The package.json at v3.5.15 shows:

- `"name": "claude-flow"` — npm package name still `claude-flow`
- `"bin": { "claude-flow": "./bin/cli.js" }` — CLI binary still `claude-flow`
- `"repository": { "url": "https://github.com/ruvnet/claude-flow.git" }` — still points to old URL
- The README calls it "Ruflo" throughout but also extensively uses "Claude Flow"

The README explicitly explains the rename: "Claude Flow is now Ruflo — named by Ruv, who loves Rust, flow states, and building things that feel inevitable." This is presented as a branding choice, not a compliance-driven change. However, the timing is consistent with Anthropic's trademark policies, which prohibit using "Claude" in product names in ways that imply Anthropic endorsement or affiliation.

**Assessment:** The rename is incomplete and largely cosmetic. The npm package, binary, and repository URL retain "claude-flow." Whether this constitutes trademark compliance depends on Anthropic's enforcement posture. There is no public record of Anthropic issuing a formal takedown notice.

### Usage Policy Concerns

**"250% subscription extension" claim:** The claim is that the Agent Booster WASM engine routes simple edits away from Claude LLM calls entirely, effectively extending the Claude Max usage quota. The Agent Booster is confirmed to be a stub. The mechanism for actually extending a Claude subscription does not exist. The claim is not a TOS violation per se — it is simply false advertising. However, if a real WASM bypass were implemented, it would raise legitimate questions about circumventing Anthropic's fair-use quota system.

**Hooks and MCP:** RuFlo uses Claude Code's officially documented hooks system and MCP integration. These are supported mechanisms. The risk is that Anthropic changes their behavior, not that RuFlo is using undocumented capabilities.

**"claude" contributor account:** The GitHub contributor named "claude" with the `@anthropics` company affiliation and 50 contributions is the official Anthropic account (created 2009-05-07). These 50 commits likely represent contributions made while running Claude Code on the repository itself, where Claude Code commits under the `claude` GitHub user if configured to do so. This is normal Claude Code usage, not an impersonation concern.

**Rate limit circumvention:** There is no evidence of rate limit circumvention. The token explosion issue (issue #1330) is the opposite problem — RuFlo consumes tokens excessively, not frugally.

---

## Part 3: Security Surface Analysis

### Confirmed Vulnerabilities (as of internal audit, 2026-01-03)

The security audit document at `v3/implementation/security/SECURITY_AUDIT_REPORT.md` (written against v2.7.47) found 18 vulnerabilities:

| ID | Severity | Finding | Status in v3.5.15 |
|----|----------|---------|------------------|
| CVE-1 | High | Vulnerable deps: `@anthropic-ai/claude-code` < 2.0.31 (command injection), `@modelcontextprotocol/sdk` < 1.24.0 (DNS rebinding) | Addressed per CVE remediation tracker |
| CVE-2 | Critical | SHA-256 + hardcoded salt password hashing in auth-service | Moved to v3 bcrypt; v2 code remains |
| CVE-3 | High | Hardcoded credentials (`admin123`, `service123`) in public repo | Addressed in v3 per CVE tracker |
| CVE-4 | High | Command injection in `hook.ts` and `error-recovery.ts` | Partially addressed in ADR-061 (execSync → execFileSync) |
| CVE-5 | High | Path traversal in `task.ts:67` | ADR-012 claims fix |
| CVE-6 | Medium | `Math.random()` for token generation in `mcp/auth.ts:375` | v3 uses `crypto.randomBytes()` per ADR-012 |
| CVE-7 | Medium | DNS rebinding in MCP WebSocket | ADR-012 claims fix |

### Supply Chain Risk

The install script `curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/claude-flow@main/scripts/install.sh | bash` fetches from jsDelivr CDN pointing to HEAD of main. This means:

1. Any push to main can silently change what users receive on next install
2. The preinstall script in `v3/@claude-flow/cli/bin/preinstall.cjs` was previously obfuscated — this is confirmed in the v3.5.3 release notes: "Removed obfuscated preinstall script (#1...)" — meaning an obfuscated script was being executed during `npm install` before version 3.5.3
3. No SHA-pinning or integrity verification in the curl-pipe install
4. CDN serves content without the benefit of npm's package integrity checks

The obfuscated preinstall script history is a serious supply chain incident. Code that was intentionally obfuscated was executing during `npm install` for an unknown period prior to March 5, 2026. The nature of the obfuscated code is not documented in the release notes.

### MCP Trust Boundary

RuFlo as an MCP server inherits all of Claude Code's granted tool permissions. When installed with `--full`, it configures itself in the project's `.mcp.json` with access to file system, bash execution, and git operations. The trust model relies entirely on RuFlo's own validation — which, as shown above, has had multiple confirmed vulnerabilities and was still in "NOT PRODUCTION READY" state as of its own internal audit in January 2026.

### Multi-Agent Injection Risk

The swarm architecture allows agents to write to shared memory and spawn sub-agents. The `@claude-flow/guidance` package includes a `ThreatDetector` with prompt-injection pattern matching, but this is TypeScript running in the Node.js process, not a cryptographic boundary. An agent that receives malicious input can write to shared memory before the detector runs; there is no atomic check-and-write. The guidance module represents sound defensive design philosophy, but it is a software-level control, not a trust boundary.

---

## Part 4: Implementation Reality — What Is and Is Not Built

This is the most important section for a build-vs-adopt decision.

### What the README claims is implemented

Per README and architecture diagrams: SONA (Self-Optimizing Neural Architecture), EWC++ (Elastic Weight Consolidation), Flash Attention (2.49-7.47x speedup), HNSW (150x-12,500x faster vector search), ReasoningBank, 9 RL algorithms (Q-Learning, SARSA, A2C, PPO, DQN, Decision Transformer, etc.), LoRA/MicroLoRA (128x compression), Int8 Quantization, Byzantine fault tolerance, Raft consensus, Gossip protocol, CRDT, WASM Agent Booster (<1ms, $0 cost for simple edits), 60+ specialized agents.

### What source inspection reveals

**HNSW (ruvector-upstream/bridges/hnsw.ts):** The `init()` method checks if a WASM module `micro-hnsw-wasm` can be loaded. The fallback (which is what executes because no WASM binary ships) is a pure JavaScript brute-force cosine similarity loop over a `Map`. The `save()` method returns `new Uint8Array(0)`. The `load()` method is a no-op. This is not HNSW. Performance claims of "150x-12,500x faster" are generated from a JavaScript Map, not HNSW.

**SONA (ruvector-upstream/bridges/sona.ts):** The `init()` method calls `this.createMockModule()`. The mock module is explicitly labeled as mock. There is no WASM binary, no LoRA weight management, no EWC penalty calculation. The `learn()` function in the mock does not train anything.

**Agent Booster WASM (v2/src/cli/simple-commands/agent-booster.js):** The `callAgentBooster()` function contains `// TODO: Call actual MCP tool here` and then simulates a successful response by appending the string `\n// Edited with Agent Booster\n` to the file contents. The "352x faster" benchmark compares the setTimeout latency of the stub against a fabricated `avgBooster * 352` estimate labeled "LLM API (est)".

**Core agent execution (v3/src/agent-lifecycle/domain/Agent.ts):** The `processTaskExecution()` method — the function that actually executes agent work — is `await new Promise(resolve => setTimeout(resolve, overhead))` where overhead is 1-10ms. The comment says: "Actual task work is performed by onExecute callback." The `onExecute` callback is an optional field on the Task type; whether any real work is wired up depends entirely on the caller.

**Raft and Byzantine consensus (v3/@claude-flow/swarm/src/consensus/):** These modules have real TypeScript implementations with proper data structures (RaftNode, RaftLogEntry, ByzantineMessage phases, PBFT-style pre-prepare/prepare/commit). However, in a Claude Code context these "nodes" are JavaScript objects in a single Node.js process — there is no actual distributed system. "Consensus" here means coordinating multiple in-process agent objects, not distributed systems fault tolerance. The consensus algorithms are architecturally sound as coordination primitives but the marketing framing ("Byzantine fault tolerance") is grossly misleading for an application that runs on a single developer's machine.

**Q-Learning Router:** This is an 882-line, genuine implementation with LRU cache, epsilon decay, experience replay buffer, and model persistence to `.swarm/q-learning-model.json`. It routes between different LLM model tiers (Haiku/Sonnet/Opus) based on task complexity. This is one of the few features that appears substantially real, though its effectiveness depends on having persistent usage history and the routing targets being actual LLMs rather than stubs.

**Summary of implementation status:**

| Feature | README claim | Actual status |
|---------|-------------|---------------|
| SONA | Production ML component | Explicitly mocked |
| EWC++ | Catastrophic forgetting prevention | Mocked in SONA mock |
| HNSW vector search | 150x-12,500x faster | JS Map brute-force fallback |
| 9 RL algorithms | Full suite | Q-Learning appears real; SARSA/PPO/DQN/etc. not found in source |
| LoRA/MicroLoRA | 128x compression | Mocked in SONA mock |
| WASM Agent Booster | <1ms, $0 LLM bypass | Confirmed stub with TODO comment |
| 60+ agents | Specialized workers | Markdown files with persona descriptions; task execution is setTimeout |
| Raft consensus | Distributed fault tolerance | In-process TypeScript coordination; architecturally correct but not distributed |
| Byzantine fault tolerance | Production-grade | Same as Raft — in-process coordination |
| Flash attention | 2.49-7.47x speedup | File exists in v3/@claude-flow/cli/src/ruvector/ but no mock/stub markers found; status unclear |

---

## Part 5: Momentum Fit Analysis

Momentum's current architecture: zero-dependency markdown skill files + Claude Code native agent loop. No Node.js requirement. No npm. No PostgreSQL. Installable as Agent Skills. The core value is that Momentum travels with a developer to any project without infrastructure prerequisites.

### Workflow 1: Multi-Agent Research
**Current:** 6 parallel Sonnet subagents via Claude Code's native Task tool.

**(A) What RuFlo could add:** RuFlo's swarm coordination offers structured parallel agent spawning with memory sharing via AgentDB/SQLite. The Q-Learning router could theoretically direct some research queries to Haiku when complexity is low, reducing cost. The `.guidance` module's threat detection could flag prompt injection in research outputs.

**(B) Cost/risk:** Requires Node.js 20+, npm install, MCP configuration. Adds a persistent daemon process. The memory coordination overhead (SQLite writes between agent steps) adds latency. Token explosion risk (issue #1330) in swarm mode is unmitigated. The actual feature providing parallel coordination (swarm spawning) uses Claude Code's `Task` tool under the hood — the same mechanism Momentum already uses directly.

**(C) Net verdict: Clear loss.** Momentum's parallel enumerator/adversary pattern achieves the same parallelism via native Claude Code subagents with zero infrastructure overhead. RuFlo adds a Node.js orchestration layer around the same underlying mechanism without adding real capability.

---

### Workflow 2: Validate-Fix-Loop (VFL)
**Current:** Structured prompting with a VFL framework; up to 4-5 iterations with explicit cost cap.

**(A) What RuFlo could add:** The Raft/BFT consensus modules could theoretically provide multi-agent agreement on validation results (e.g., require 2/3 of validator agents to agree before accepting a fix). The `@claude-flow/guidance` package's authority hierarchy (agent/human/institutional/regulatory) maps conceptually to Momentum's three-tier enforcement model.

**(B) Cost/risk:** Consensus protocols are in-process JavaScript coordination. For VFL with 3-5 agents, a quorum majority is achievable with a simple vote-counting function in 10 lines of code. Raft consensus is designed for persistent distributed systems where nodes can crash and restart — this overhead is irrelevant for a 4-iteration validation loop. The iteration cost tax of adding an orchestration layer to each VFL cycle would likely push cost above Momentum's 4-5 iteration cap faster.

**(C) Net verdict: Clear loss.** The governance primitives in `@claude-flow/guidance` have interesting design but are over-engineered for VFL's use case. Momentum's structured prompting with explicit iteration caps is leaner and cost-controlled.

---

### Workflow 3: Sprint Orchestration
**Current:** Markdown-based sprint planning skills.

**(A) What RuFlo could add:** RuFlo has `.claude/agents/github/` agents for PR management, issue tracking, release management. These are markdown agent definitions that orchestrate GitHub CLI calls. The SPARC methodology agents (specification, pseudocode, architecture, refinement) provide structured decomposition.

**(B) Cost/risk:** The GitHub agents are markdown files with hooks that call `git` and `gh`. This is the same architecture as Momentum's BMAD skills. RuFlo's SPARC agents duplicate what Momentum's BMAD pipeline already does more completely (Brief → PRD → Architecture → Epics → Stories). Adopting RuFlo's SPARC would mean replacing BMAD with a less complete spec-driven workflow.

**(C) Net verdict: Neutral to slight loss.** Some individual agent definitions could inform Momentum's agent writing without adopting RuFlo as a dependency. The SPARC templates are not competitive with BMAD's full pipeline.

---

### Workflow 4: Code Review
**Current:** Parallel blind hunter / edge case hunter / acceptance auditor agents via Claude Code subagents.

**(A) What RuFlo could add:** RuFlo has a code review swarm (`github/code-review-swarm.md`) and security auditor. The `@claude-flow/guidance` threat detection patterns could be adapted for code review (detecting "ignore previous instructions" style injections in PR descriptions). The `IrreversibilityClassifier` (ADR-G021) that classifies actions as reversible/costly-reversible/irreversible is an interesting primitive for a code review gate.

**(B) Cost/risk:** Momentum's parallel blind hunter pattern already implements separation of concerns in code review. The RuFlo swarm adds coordination overhead. The security detection patterns from `@claude-flow/guidance` could be extracted as standalone Momentum rules without taking a RuFlo dependency.

**(C) Net verdict: Neutral.** The `IrreversibilityClassifier` concept and the threat pattern library in `@claude-flow/guidance` have non-trivial value as design inspiration. These ideas can be incorporated into Momentum's code review rules without taking a runtime dependency on RuFlo.

---

### Workflow 5: Story Creation and Dev Story Execution
**Current:** Markdown spec files + dev agent.

**(A) What RuFlo could add:** RuFlo's task decomposition in the `goal/` agents (goal-planner, code-goal-planner) and the `WorkflowEngine` break complex tasks into subtasks. The hive-mind queen/worker pattern (queen coordinator → worker specialists) maps to Momentum's orchestrator/implementer pattern.

**(B) Cost/risk:** The `WorkflowEngine` at `v3/src/task-execution/application/WorkflowEngine.ts` is a real implementation. However, it is coupled to AgentDB for task persistence and the MCP server for inter-agent communication. Story creation in Momentum is currently a human+agent collaborative process guided by BMAD spec documents; automating it via a workflow engine that requires a running Node.js daemon would remove human authorship from specifications — which is architecturally prohibited by Momentum's Authority Hierarchy (specifications > tests > code, human-authored).

**(C) Net verdict: Clear loss.** Automated story generation via workflow engine conflicts with Momentum's philosophy that specifications are human-authored artifacts. The WorkflowEngine is solving a different problem (automated task decomposition for coding tasks) than Momentum's story creation (structured human-AI collaborative specification writing).

---

### Workflow 6: Cross-Project Portability
**Current:** Agent Skills (.claude/skills/), installs via standard Agent Skills mechanism, no runtime dependencies.

**(A) What RuFlo could add:** Nothing. RuFlo decreases portability.

**(B) Cost/risk:** RuFlo requires Node.js 20+, npm, and for full capability: PostgreSQL with the `@ruvector/postgres-cli` extension, a running MCP server daemon, and per-project initialization (`npx ruflo@latest init`). This is the opposite of Agent Skills portability.

**(C) Net verdict: Clear loss.** This is the sharpest incompatibility between RuFlo and Momentum. Momentum's zero-dependency property is not a nice-to-have; it is what makes Momentum a practice module rather than a platform. A developer opening a new project should be able to start coding with Momentum available immediately — no npm install, no daemon, no PostgreSQL.

---

### Workflow 7: The Pure Markdown Advantage
**Current:** No installation, no dependencies, no runtime, no compiled code.

Momentum's entire value proposition rests on the observation that Claude Code's markdown-based agent and skill system is powerful enough to implement sophisticated workflows without any compiled code. The advantage is:
- Zero supply chain surface
- Zero version fragility
- Zero platform compatibility issues
- Zero ops burden
- Transferable to any Claude Code project in seconds
- Human-readable and auditable with no tooling

RuFlo gives up all of these for a runtime orchestration layer whose advertised capabilities are mostly unimplemented stubs, and whose real capabilities (Q-Learning router, in-process consensus, AgentDB SQLite storage) replicate things Claude Code's native subagent system already provides.

**(C) Net verdict: Clear loss.** If Momentum depended on RuFlo, it would cease to be Momentum.

---

## Part 6: Integration Cost Estimate

If Momentum were to integrate with RuFlo despite the above findings, the actual integration cost would be:

| Phase | Work | Estimate | Risk |
|-------|------|----------|------|
| **Baseline validation** | Audit which RuFlo features actually work end-to-end | 3-5 days | High — many features are stubs; may find nothing usable |
| **Dependency onboarding** | Node.js 20+ requirement, npm, MCP server configuration, per-project init | 1 day per project | Medium — manageable but eliminates zero-dependency property |
| **Integration shim** | Adapt Momentum markdown skills to call RuFlo MCP tools | 1-2 weeks | High — MCP tool stability is poor (issue #1343, #1344, #1333 all filed this week) |
| **Hook integration** | Wire RuFlo's hooks system with Momentum's stop hook / pre-edit hook | 1 week | High — hooks are the most bug-prone subsystem (v3.5.15 was a hooks hotfix; issues #1331, #1341, #1322 all hooks bugs) |
| **Token cost management** | Implement per-agent token caps to prevent the runaway consumption described in issue #1330 | 3-5 days | High — no built-in cap mechanism exists |
| **Ongoing maintenance** | Track RuFlo's breaking changes across 13+ releases in 5 days | Continuous | Very high — release velocity makes API stability impossible to assume |
| **Feature gap documentation** | Document which RuFlo claims are actually implemented in each version used | Ongoing | Critical — feature presence cannot be assumed from README claims |

**Total minimum integration cost:** 3-5 weeks to establish a stable integration baseline, assuming the baseline is achievable at all. Ongoing maintenance cost is proportional to RuFlo's release velocity, which has been 13 releases in 5 days (2026-03-05 through 2026-03-09).

---

## Part 7: Recommendation Summary

### Verdict: Avoid

**Reasoning:**

**1. The advertised capabilities do not exist.** The features that would justify integration — HNSW vector search, SONA self-optimization, WASM Agent Booster, RL-based routing, Byzantine consensus for distributed fault tolerance — are confirmed stubs, mocks, or TODO comments. This was publicly documented in issue #1326 (filed 2026-03-09, no substantive maintainer response as of 2026-03-15). Building on a foundation where the foundation does not exist is not a technical risk; it is a category error.

**2. Architectural incompatibility is fundamental.** RuFlo is a runtime orchestration platform (Node.js daemon + MCP server + optional PostgreSQL). Momentum is a zero-dependency markdown practice module. These are not different tools solving the same problem — they represent different philosophies about where workflow intelligence should live. Momentum's intelligence lives in Claude Code's native context window via structured markdown. RuFlo's intelligence is supposed to live in a persistent learning layer; in practice, it lives in neither place because the learning layer is unimplemented.

**3. Supply chain and security posture are not acceptable for a practice module.** The previously obfuscated preinstall script (removed in v3.5.3 without explanation of what it did), the curl-pipe install from CDN HEAD, the hardcoded admin credentials in a public repository, and the 18-vulnerability internal audit that rated the project "NOT PRODUCTION READY" as of January 2026 — none of these are individually disqualifying for an experimental tool. Collectively, for a module that installs into `.claude/` with file system and bash access across all projects, they represent an unacceptable trust surface.

**4. Bus factor is effectively 1.** 5,852 of 5,912 total contributions are from ruvnet. External contributors total 10 combined. The "claude" contributor (50 contributions) is the Anthropic bot account, not an independent human maintainer. If ruvnet stops maintaining RuFlo, the project is abandoned. The 467 open issues with no triage labels and a 45% open rate on the 100-issue sample suggest the current maintenance load already exceeds capacity.

**5. Token consumption risk is unmitigated.** Issue #1330 describes "thousands to millions of tokens within 0-30 minutes for simple tasks" in swarm mode. Momentum is designed around explicit cost management (4-5 iteration VFL caps, model selection discipline, cost observability). A dependency that can consume millions of tokens for a simple task is incompatible with that discipline.

### Selective Extraction (Limited Value)

The following RuFlo artifacts have standalone value as design references without requiring a RuFlo dependency:

- **`@claude-flow/guidance` authority/capability model** (ADR-G021): The typed authority hierarchy (agent/human/institutional/regulatory) and IrreversibilityClassifier concepts are worth incorporating into Momentum's code review rules and stop hook logic as design patterns, not as code.
- **`@claude-flow/guidance` threat detection pattern library**: The categorized prompt injection patterns (override attempts, memory poisoning signatures, privilege escalation markers) could inform Momentum's adversarial review agent persona.
- **Q-Learning Router (v3/@claude-flow/cli/src/ruvector/q-learning-router.ts)**: The 882-line implementation is a genuine, well-structured RL routing approach. It is worth studying for Momentum's PT-016 model routing strategy, as design reference.
- **Agent taxonomy in `.claude/agents/`**: The directory structure (core/orchestration/platform/specialized/methodology) is a reasonable organizational model for large agent libraries.

None of these require installing RuFlo or taking any runtime dependency.

### Monitor Condition

If any of the following occur, re-evaluate in 6 months (September 2026):

1. Issue #1326 is closed with a maintainer response that either (a) provides evidence the features exist in the external `@ruvector/*` npm packages with functioning WASM modules, or (b) transparently labels unimplemented features as roadmap items in the README
2. A second significant contributor (not a bot) accounts for 20%+ of commit activity over a sustained 3-month period
3. The token consumption issue (#1330) is resolved with a documented token budget enforcement mechanism

---

## Sources

All sources retrieved 2026-03-15 via GitHub API and npm registry.

| Source | Date | Notes |
|--------|------|-------|
| `ruvnet/ruflo` GitHub repository metadata | 2026-03-15 | Stars: 21,225; forks: 2,337; open issues: 467 |
| Commit history (last 30 commits) | 2026-03-09 to 2026-03-15 | 100% from ruvnet alias |
| Contributor list | 2026-03-15 | ruvnet: 5,852; claude (bot): 50; all others: 10 combined |
| Release history | 2026-03-09 (latest: v3.5.15) | Version trajectory: alpha → v3.5.x in 9 months |
| `package.json` (v3.5.15) | 2026-03-15 | Only hard deps: semver, zod; all ML/DB deps are optional |
| `scripts/install.sh` | 2026-03-15 | curl-pipe from CDN HEAD; no integrity hash |
| `v3/@claude-flow/cli/bin/preinstall.cjs` | 2026-03-15 | No-op comment; previously obfuscated (removed v3.5.3) |
| `v3/implementation/security/SECURITY_AUDIT_REPORT.md` | 2026-01-03 | Against v2.7.47; 18 vulns; "NOT PRODUCTION READY" |
| `v3/implementation/security/SECURITY_SUMMARY.md` | 2026-01-03 | Hardcoded credentials confirmed |
| `v3/@claude-flow/swarm/src/consensus/raft.ts` | 2026-03-15 | Real TypeScript implementation; in-process only |
| `v3/@claude-flow/swarm/src/consensus/byzantine.ts` | 2026-03-15 | PBFT-style implementation; in-process only |
| `v3/@claude-flow/cli/src/ruvector/q-learning-router.ts` | 2026-03-15 | 882 lines; genuine RL implementation |
| `v3/plugins/ruvector-upstream/src/bridges/hnsw.ts` | 2026-03-15 | Mock fallback confirmed; JS Map brute-force |
| `v3/plugins/ruvector-upstream/src/bridges/sona.ts` | 2026-03-15 | `createMockModule()` confirmed |
| `v2/src/cli/simple-commands/agent-booster.js` | 2026-03-15 | `// TODO: Call actual MCP tool here` confirmed |
| `v3/src/agent-lifecycle/domain/Agent.ts` | 2026-03-15 | `processTaskExecution` = setTimeout(1-10ms) confirmed |
| Issue #1326 | 2026-03-09 | "Most advertised core features are completely unimplemented" — community audit, unanswered |
| Issue #1323 | 2026-03-09 | Contributor injection allegation; unverified |
| Issue #1330 | 2026-03-11 | Token explosion: millions of tokens in 30 minutes; unresolved |
| Issue #1344 | 2026-03-13 | `doctor` checks wrong MCP server name; basic operational failure |
| Issue #1343 | 2026-03-13 | AgentDB bridge missing from dist; unresolved |
| Issue #640 | 2025-08-11 | "CRITICAL: Verification & Truth Enforcement System Failure in Multi-Agent Architecture" — 9 comments; older than Sept 2025 threshold, flagged |
| Issue #360 | 2025-07-17 | `better-sqlite3` ARM64 binding failure — flagged, older than Sept 2025 |
| ADR-012 | 2026-01-05 | MCP security features; CVEs claimed fixed |
| ADR-027 | 2026-01-16 | PostgreSQL integration; optional but load-bearing for production |
| ADR-G021 | 2026-02-01 | Human authority/irreversibility model; design value |
| ADR-026 | 2026-01-14 | Agent Booster routing — "Implemented" but implementation is stub |
| `v3/implementation/integration/AGENTS-SKILLS-COMMANDS-HOOKS.md` | 2026-03-15 | 76 agents, 28 skills, 93 commands — counts confirmed |
| npm download stats (claude-flow) | 2026-03-15 | ~605k total since June 2025; ~50k last 30 days |
| ADR-061 release notes (v3.5.14) | 2026-03-06 | `execSync` → `execFileSync`; latest security sprint |
| v3.5.15 release notes | 2026-03-09 | Hooks path resolution hotfix; last commit before report date |

**Flagged sources older than September 2025:** Issues #640 (2025-08-11) and #360 (2025-07-17) are cited but predate the September 2025 threshold. They are included because they document persistent architectural issues that have not been resolved in subsequent versions.
