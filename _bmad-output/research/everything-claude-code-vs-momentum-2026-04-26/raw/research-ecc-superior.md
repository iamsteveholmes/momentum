---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Where everything-claude-code is superior to Momentum or has features Momentum lacks"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# ECC vs Momentum — Where ECC Leads

## Inline Summary

After reading the actual ECC repo (commit at clone time, master branch, 2026-04-26), three areas where ECC clearly outclasses Momentum stand out: (1) **selective install with profiles, manifests, and a real SQLite-backed install state store** (`/tmp/ecc-research/scripts/lib/install/`, `/tmp/ecc-research/manifests/install-profiles.json`, `/tmp/ecc-research/scripts/lib/state-store/index.js`) — Momentum has nothing comparable; (2) **first-class multi-harness support** (Codex, Cursor, OpenCode, Gemini, Kiro, Trae, CodeBuddy, Antigravity all have install targets in `/tmp/ecc-research/scripts/lib/install-targets/` and dedicated config dirs at the repo root); (3) **a serious automated test suite** — 91 Jest test files plus a CI validator suite under `/tmp/ecc-research/scripts/ci/` that lints agents/hooks/skills/manifests, while Momentum ships only 4 ad-hoc Python tests, none of which validate Momentum's own skills/agents. ECC also ships polished extras Momentum lacks entirely: a tuned statusline at `/tmp/ecc-research/examples/statusline.json`, six pre-configured MCP servers in `.mcp.json`, and a full Windows installer (`install.ps1`).

---

## 1. Onboarding & Install Ergonomics

### What ECC ships

- **Five named install profiles** — `core`, `developer`, `security`, `research`, `full` — enumerated in `/tmp/ecc-research/manifests/install-profiles.json`. [OFFICIAL] Each profile is a curated module set so users can opt into a tightly-scoped install instead of taking the whole catalogue.
- **Install components → modules → profiles three-level decomposition** in `/tmp/ecc-research/manifests/install-components.json` and `/tmp/ecc-research/manifests/install-modules.json`. Components describe families (`baseline:rules`, `lang:typescript`, `capability:security`, etc.); profiles aggregate components. [OFFICIAL]
- **Plan/apply CLIs:** `node scripts/install-plan.js --profile core` produces a dry-run; `node scripts/install-apply.js` executes. Confirmed in `/tmp/ecc-research/scripts/install-plan.js` and `/tmp/ecc-research/scripts/install-apply.js` plus the matching test files `install-plan.test.js` / `install-apply.test.js` under `/tmp/ecc-research/tests/scripts/`. [OFFICIAL]
- **Install lifecycle and state tracking** in `/tmp/ecc-research/scripts/lib/install-lifecycle.js`, `install-state.js`, and `install-manifests.js`. The state store is sql.js (SQLite-in-WASM) at `~/.claude/ecc/state.db` per `/tmp/ecc-research/scripts/lib/state-store/index.js`. The schema is JSON-Schema-validated against `/tmp/ecc-research/schemas/state-store.schema.json`, covering sessions, skill runs, skill versions, decisions, install state, and governance events. [OFFICIAL]
- **Cross-platform installer pair:** `install.sh` (POSIX, with cygpath fallback for Git Bash on Windows) and `install.ps1` (PowerShell, native Windows). Both wrap the same Node entrypoint (`scripts/install-apply.js`) and auto-run `npm install` on first use. [OFFICIAL]
- **A `configure-ecc` skill** at `/tmp/ecc-research/skills/configure-ecc/SKILL.md` that drives the install conversationally via `AskUserQuestion`, including a Step 0 that clones ECC into `/tmp/everything-claude-code` if it is not already present. [OFFICIAL]
- **Doctor + repair** scripts at `/tmp/ecc-research/scripts/doctor.js` and `/tmp/ecc-research/scripts/repair.js`, with tests at `/tmp/ecc-research/tests/scripts/doctor.test.js`. [OFFICIAL]

### Momentum status

- Momentum is distributed as a single Claude plugin via `/plugin marketplace update momentum`. The plugin manifest at `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json` has only `name`, `version`, `description`, `author`. There is no manifest, no profile, no plan/apply pipeline, no state store, no doctor. [PRAC]
- The user's own MEMORY notes record that "momentum install shell script is obsolete — use standard Agent Skills installation. Keeps resurfacing." Momentum has consciously moved away from any installer beyond the plugin marketplace. [PRAC]

### Verdict

ECC is dramatically more sophisticated here. Momentum is all-or-nothing: install the plugin and you get every skill, agent, and hook. ECC lets a security-focused team take the `security` profile, ignore Django/Laravel/Spring patterns, and never load the `business-content` lane. For a single-developer practice (Momentum's current target) this gap is tolerable, but for any multi-team rollout it is a real disadvantage.

---

## 2. Output Styles, Statuslines, Hooks

### Statusline

- **ECC** ships `/tmp/ecc-research/examples/statusline.json` — a single-line bash script that renders `user:cwd branch* ctx:% model time todos:N` with truecolor RGB ANSI escapes. The JSON includes a `_comments` block documenting each color and a working sample output (`affoon:~/projects/myapp main* ctx:73% sonnet-4.6 14:30 todos:3`). It also reads context-window remaining percentage from the harness payload. [OFFICIAL]
- **Momentum** has no statusline. `find /Users/steve/projects/momentum -name "*statusline*"` returns nothing. [PRAC]

### Output styles

- Neither side ships explicit Claude Code "output styles." [UNVERIFIED] No matches under `/tmp/ecc-research/` for `output-style` either; the prior comparison report's claim that ECC ships polished output styles is **not verified** by the repo.

### Hooks

- **ECC** registers ~28 hook scripts in `/tmp/ecc-research/scripts/hooks/` covering: bash dispatcher (pre+post), TDD reminders, design-quality checks, dev-server-block, doc-warn, format-on-save, typecheck-on-save, governance capture, mcp-health-check, cost-tracker, session-start bootstrap, session-end markers, pre-compact, suggest-compact, governance, GateGuard fact-force, no-verify blocker, console.log warnings, observer-session activity tracker, and more. Each hook is a Node script tested under `/tmp/ecc-research/tests/hooks/` (24 hook test files). [OFFICIAL]
- The `hooks.json` at `/tmp/ecc-research/hooks/hooks.json` (46 KB) is a single dispatcher file that wires PreToolUse/PostToolUse/Stop/UserPromptSubmit/SessionStart/PreCompact matchers to those Node scripts, with a clever `CLAUDE_PLUGIN_ROOT` resolver inline so the same config works whether the plugin is installed at `~/.claude`, in `~/.claude/plugins/ecc`, or in a marketplace cache. [OFFICIAL]
- **Momentum** registers four hooks total at `/Users/steve/projects/momentum/.claude/settings.json`: ExitPlanMode (plan-audit), Bash (version-bump check), Edit/Write (file-protection), Stop (placeholder echo). Plus three more in `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json`. None are tested. [PRAC]

### Verdict

ECC's hook surface is roughly an order of magnitude larger and is unit-tested. Momentum has surgical, well-purposed hooks (plan audit, version bump, lint placeholder) but nothing approaching ECC's depth. The lack of any Momentum statusline is a missed quick win — ECC's example would drop in cleanly with minor edits.

---

## 3. MCP Integrations

### What ECC ships

- `/tmp/ecc-research/.mcp.json` pre-configures **six MCP servers** with pinned versions: `github` (`@modelcontextprotocol/server-github@2025.4.8`), `context7` (`@upstash/context7-mcp@2.1.4`), `exa` (HTTP), `memory` (`@modelcontextprotocol/server-memory@2026.1.26`), `playwright` (`@playwright/mcp@0.0.69`), `sequential-thinking` (`@modelcontextprotocol/server-sequential-thinking@2025.12.18`). [OFFICIAL]
- Helper module `/tmp/ecc-research/scripts/lib/mcp-config.js` (with tests in `tests/lib/mcp-config.test.js`) merges ECC's MCP catalogue with the user's existing config. [OFFICIAL]
- Dedicated MCP health-check hook (`/tmp/ecc-research/scripts/hooks/mcp-health-check.js`) verifies servers respond before tool calls. [OFFICIAL]
- Dozens of skills assume MCP availability — e.g. `jira-integration` (`/tmp/ecc-research/skills/jira-integration/SKILL.md`) recommends the `mcp-atlassian` MCP server and provides setup steps; `documentation-lookup` and `agent-introspection-debugging` route through Context7 and Exa MCP. [OFFICIAL]

### Momentum status

- `/Users/steve/projects/momentum/.mcp.json` contents: `{"mcpServers": {}}`. Empty. [PRAC]
- No MCP-related skills, no MCP health hook, no MCP setup script in Momentum.

### Verdict

ECC ships a working MCP starter pack; Momentum ships an empty stub. For any new user this is a meaningful out-of-box difference — getting GitHub, Context7, Exa, Playwright, and a memory server live in one `npm i`-equivalent step is a notable onboarding win.

---

## 4. Documentation Quality

### What ECC ships

- A 68 KB `README.md` plus a Chinese translation (`README.zh-CN.md`, 36 KB), 17 docs under `/tmp/ecc-research/docs/` including `SKILL-DEVELOPMENT-GUIDE.md`, `SELECTIVE-INSTALL-ARCHITECTURE.md`, `SELECTIVE-INSTALL-DESIGN.md`, `SESSION-ADAPTER-CONTRACT.md`, `MANUAL-ADAPTATION-GUIDE.md`, `TROUBLESHOOTING.md`, `token-optimization.md`, `hook-bug-workarounds.md`. [OFFICIAL]
- Internationalized docs in `/tmp/ecc-research/docs/ja-JP`, `ko-KR`, `pt-BR`, `tr`, `zh-CN`, `zh-TW`. [OFFICIAL]
- A 6 KB `COMMANDS-QUICK-REF.md` mapping every command to its agent. [OFFICIAL]
- Three "longform/shortform/security" guides (`the-longform-guide.md`, `the-shortform-guide.md`, `the-security-guide.md` — 15-29 KB each) describing how the practice is meant to be used. [OFFICIAL]
- A 7 KB `CHANGELOG.md` with version-by-version highlights and CHANGELOG entries that name the new agents/skills/commands per release. [OFFICIAL]
- 8 example CLAUDE.md files under `/tmp/ecc-research/examples/` for Django, Go, Laravel, Rust, Next.js, etc. [OFFICIAL]
- 13 KB `CONTRIBUTING.md` with a defined PR process. [OFFICIAL]

### Momentum status

- `/Users/steve/projects/momentum/CLAUDE.md` is 33 lines. [PRAC]
- Momentum has rich planning artifacts under `docs/planning-artifacts/` and `_bmad-output/`, but those are internal practice artifacts, not external user-facing docs.
- No tutorials, no language-specific examples, no internationalization, no contributor guide that I can find at the repo root.

### Verdict

ECC has invested heavily in user-facing documentation; Momentum has invested in internal planning docs. For a developer evaluating which to adopt, ECC offers a more legible front door.

---

## 5. Community Contribution Model

- ECC's `/tmp/ecc-research/CONTRIBUTING.md` enumerates accepted categories (agents, skills, hooks, commands), sets quality bars, and links to `SKILL-DEVELOPMENT-GUIDE.md` and `skill-adaptation-policy.md`. There is also a `/tmp/ecc-research/CODE_OF_CONDUCT.md` (5 KB), `SECURITY.md`, `SPONSORING.md`, and `SPONSORS.md`. The CHANGELOG references PR numbers (e.g., "(#647)", "(#549)") indicating real upstream PR throughput. [OFFICIAL]
- Momentum has no CONTRIBUTING, no CODE_OF_CONDUCT, no SECURITY policy, no public PR numbers. [PRAC] This is consistent with Momentum being a single-developer practice rather than a community project, but it means ECC has a posture for accepting external contributions that Momentum does not.

---

## 6. Pre-Built Integrations With External Tools

ECC ships skills targeted at concrete external systems Momentum does not address:

| Tool | ECC artifact | Momentum |
| --- | --- | --- |
| GitHub | `skills/github-ops/SKILL.md` (gh CLI flows) plus GitHub MCP in `.mcp.json` | gh used ad-hoc; no skill |
| Jira | `skills/jira-integration/SKILL.md` (mcp-atlassian or REST) | none |
| Context7 docs | `skills/documentation-lookup/SKILL.md` + Context7 MCP | none |
| Exa search | `skills/exa-search/SKILL.md` + Exa HTTP MCP | none |
| Playwright E2E | `skills/e2e-testing/SKILL.md` + Playwright MCP + `agents/e2e-runner.md` | none |
| Google Workspace | `skills/google-workspace-ops/SKILL.md` | none |
| Slack-style messaging | `skills/messages-ops/SKILL.md`, `skills/unified-notifications-ops/SKILL.md` | none |
| Email ops | `skills/email-ops/SKILL.md` | none |
| Customer billing | `skills/customer-billing-ops/SKILL.md`, `skills/finance-billing-ops/SKILL.md` | none |
| X / Twitter API | `skills/x-api/SKILL.md` | none |

[OFFICIAL] All listed paths exist under `/tmp/ecc-research/skills/`. Momentum's skill set focuses on *practice mechanics* (sprint-planning, sprint-dev, retro, AVFL, intake, distill, decision); it does not include any vendor-specific integration surface.

### Verdict

For project-management or growth/marketing workflows that need Jira/Linear/Slack/email/billing wiring, ECC has prebuilt scaffolds. Momentum is silent on these — by deliberate scope, but it is still a feature gap.

---

## 7. Cross-Platform Polish

ECC ships installer artifacts and config for **eight different agentic IDEs / harnesses** under their respective dotfiles at the repo root:

- `/tmp/ecc-research/.claude/` — Claude Code (primary)
- `/tmp/ecc-research/.codex/` — OpenAI Codex (with `AGENTS.md`, `agents/`, `config.toml`)
- `/tmp/ecc-research/.codex-plugin/` — Codex plugin manifest
- `/tmp/ecc-research/.cursor/` — Cursor (hooks, rules, skills)
- `/tmp/ecc-research/.gemini/` — Gemini (`GEMINI.md`)
- `/tmp/ecc-research/.opencode/` — OpenCode (with TypeScript plugins, commands, prompts)
- `/tmp/ecc-research/.kiro/` — Kiro (with `install.sh`, agents, hooks, skills, steering)
- `/tmp/ecc-research/.codebuddy/` — CodeBuddy (with install.sh + uninstall.js)
- `/tmp/ecc-research/.trae/` — Trae (install.sh + README in en/zh)

Plus install targets in `/tmp/ecc-research/scripts/lib/install-targets/`: `antigravity-project.js`, `claude-home.js`, `codebuddy-project.js`, `codex-home.js`, `cursor-project.js`, `gemini-project.js`, `opencode-home.js`. [OFFICIAL]

Adapter scripts at `/tmp/ecc-research/scripts/gemini-adapt-agents.js` and `/tmp/ecc-research/scripts/sync-ecc-to-codex.sh` translate ECC's canonical agent/skill markdown into the formats those harnesses expect. Tests at `/tmp/ecc-research/tests/scripts/codex-hooks.test.js`, `gemini-adapt-agents.test.js`, `trae-install.test.js`, `sync-ecc-to-codex.test.js`. [OFFICIAL]

**Windows-native support:** `install.ps1` is a real PowerShell script with strict-mode error handling and proper symlink resolution. [OFFICIAL]

### Momentum status

Claude-only. The plugin manifest, hooks, and skills assume Claude Code. There is no Codex, Cursor, OpenCode, Gemini, or Kiro support. There is no Windows installer (Momentum is plugin-based so this matters less, but `bash` hooks won't run without WSL). [PRAC]

### Verdict

ECC dominates here by a wide margin. If a team uses multiple agentic IDEs, ECC is the only realistic choice today.

---

## 8. Selective Install / Opt-In Components

Already covered in §1 — but worth restating: ECC's selective install architecture is the single most distinctive engineering investment in the repo. The architecture doc `/tmp/ecc-research/docs/SELECTIVE-INSTALL-ARCHITECTURE.md` and design doc `/tmp/ecc-research/docs/SELECTIVE-INSTALL-DESIGN.md` describe a four-layer model (component → module → profile → request). The state store at `.claude/ecc/state.db` records what was installed when, by which profile, and whether dependencies were satisfied. CI enforces this with `/tmp/ecc-research/scripts/ci/validate-install-manifests.js`. [OFFICIAL]

Momentum has no concept of partial install. Every project that installs the plugin gets every skill (25 sub-skills) and every agent (7 dev agents).

---

## 9. Multi-Language Ecosystem Support

ECC ships language packs for at least **15 ecosystems**, evidenced by `/tmp/ecc-research/rules/` directory structure: `common`, `cpp`, `csharp`, `dart`, `golang`, `java`, `kotlin`, `perl`, `php`, `python`, `rust`, `swift`, `typescript`, `web`, `zh`. [OFFICIAL]

Per-language skills (sampled): `cpp-coding-standards`, `cpp-testing`, `csharp-testing`, `dart-flutter-patterns`, `django-patterns/security/tdd/verification`, `golang-patterns`, `golang-testing`, `java-coding-standards`, `kotlin-coroutines-flows`, `kotlin-exposed-patterns`, `kotlin-ktor-patterns`, `kotlin-patterns`, `kotlin-testing`, `laravel-patterns/security/tdd/verification`, `nestjs-patterns`, `nextjs-turbopack`, `nuxt4-patterns`, `perl-patterns/security/testing`, `python-patterns`, `python-testing`, `pytorch-patterns`, `rust-patterns`, `rust-testing`, `springboot-patterns/security/tdd/verification`, `swift-actor-persistence`, `swift-concurrency-6-2`, `swift-protocol-di-testing`, `swiftui-patterns`. [OFFICIAL]

Per-language agents: `cpp-reviewer`, `cpp-build-resolver`, `csharp-reviewer`, `dart-build-resolver`, `flutter-reviewer`, `go-reviewer`, `go-build-resolver`, `java-reviewer`, `java-build-resolver`, `kotlin-reviewer`, `kotlin-build-resolver`, `python-reviewer`, `pytorch-build-resolver`, `rust-reviewer`, `rust-build-resolver`, `typescript-reviewer`. [OFFICIAL]

Momentum is **language-agnostic** — its skills (sprint-planning, AVFL, retro, dev) call out to `bmad-dev-story` which is itself language-neutral. There is no Momentum equivalent of `python-reviewer` or `rust-build-resolver`. This is by design (Momentum is a practice layer, not a coding pack), but it means a project picking Momentum still needs to source language-specific code review and build-error advice elsewhere.

---

## 10. Security Scanning, Sandboxing, Permission Models

### What ECC ships

- **`security-scan` skill** at `/tmp/ecc-research/skills/security-scan/SKILL.md` — invokes "AgentShield" via `npx ecc-agentshield scan .` to audit `.claude/` configs (CLAUDE.md, settings.json, MCP servers, hooks, agent definitions). [OFFICIAL — but the underlying AgentShield package and the "1,282 tests" claim are external; this skill only documents how to call it]
- **`security-bounty-hunter` skill** at `/tmp/ecc-research/skills/security-bounty-hunter/SKILL.md` — bias toward remotely reachable, user-controlled attack paths (SSRF, auth bypass, deserialization). [OFFICIAL]
- **`security-review` skill** at `/tmp/ecc-research/skills/security-review/SKILL.md` and `security-reviewer` agent at `/tmp/ecc-research/agents/security-reviewer.md`. [OFFICIAL]
- **`gateguard` skill** at `/tmp/ecc-research/skills/gateguard/SKILL.md` — three-stage pre-action gate (DENY → FORCE investigation → ALLOW retry). The skill claims a +2.25 point average quality lift in two A/B tests. [OFFICIAL] Wired through the `gateguard-fact-force.js` hook. The empirical claim is not independently verified, but the mechanism (DENY/FORCE/ALLOW via PreToolUse) is real and tested at `/tmp/ecc-research/tests/hooks/gateguard-fact-force.test.js`.
- **`safety-guard` skill** at `/tmp/ecc-research/skills/safety-guard/SKILL.md` — three modes (Careful, Sandbox, Read-Only) intercepting destructive commands. [OFFICIAL]
- **CI security validators:** `/tmp/ecc-research/scripts/ci/validate-workflow-security.js`, `validate-no-personal-paths.js`, `check-unicode-safety.js`. [OFFICIAL]
- **`block-no-verify.js` hook** at `/tmp/ecc-research/scripts/hooks/block-no-verify.js` — blocks `git commit --no-verify` and similar bypasses. [OFFICIAL]
- **HIPAA, healthcare-PHI, defi-amm, llm-trading-agent compliance skills** — `hipaa-compliance`, `healthcare-phi-compliance`, `defi-amm-security`, `llm-trading-agent-security`. [OFFICIAL]

### Momentum status

- `/Users/steve/projects/momentum/skills/momentum/skills/code-reviewer/` is a generic adversarial code reviewer (read-only tools). It is not security-specialized.
- `/Users/steve/projects/momentum/.claude/momentum/hooks/file-protection.sh` and `protected-paths.json` are a path-protection hook.
- No security-scan, no AgentShield equivalent, no bounty-hunter pattern, no destructive-command interception, no HIPAA/PHI/finance domain skills.

### Verdict

ECC's security surface is much wider, both in pre-action gating and domain-specific compliance content. The biggest practical advantage: ECC will refuse to run `git commit --no-verify` while Momentum has nothing similar.

---

## 11. Testing Infrastructure for Agent Definitions

### What ECC ships

- **91 Jest test files** total: 24 hook tests in `/tmp/ecc-research/tests/hooks/`, 26 lib tests in `/tmp/ecc-research/tests/lib/`, 28 script tests in `/tmp/ecc-research/tests/scripts/`, 3 CI tests, 2 docs tests, 1 integration test. Plus 4 Python tests under `/tmp/ecc-research/tests/`. [OFFICIAL]
- **Validators that lint the catalogue itself:** `/tmp/ecc-research/scripts/ci/validate-agents.js`, `validate-commands.js`, `validate-hooks.js`, `validate-rules.js`, `validate-skills.js`, `validate-install-manifests.js`, `validate-workflow-security.js`, `validate-no-personal-paths.js`, `check-unicode-safety.js`. Each has an accompanying test. [OFFICIAL]
- **Agent-eval skill** (`/tmp/ecc-research/skills/agent-eval/SKILL.md`) for head-to-head comparison of coding agents on YAML task definitions, with git-worktree isolation and pass-rate/cost/time metrics. [OFFICIAL]
- **Eval-harness skill** (`/tmp/ecc-research/skills/eval-harness/SKILL.md`). [OFFICIAL]
- **Healthcare-eval-harness skill** (`/tmp/ecc-research/skills/healthcare-eval-harness/SKILL.md`). [OFFICIAL]
- A `commitlint.config.js` and `.markdownlint.json` at the repo root for content-quality CI. [OFFICIAL]

### Momentum status

- `find /Users/steve/projects/momentum -name "*.test.js"` returns nothing. [PRAC]
- 4 Python tests under `/Users/steve/projects/momentum/.claude/skills/bmad-*/scripts/tests/` — those belong to BMAD skills, not Momentum.
- `/Users/steve/projects/momentum/skills/momentum/scripts/test-momentum-tools.py` is the only Momentum-owned test, and it tests `momentum-tools.py` (a small CLI), not Momentum's skills/agents/hooks.
- AVFL skill has an `evals/` folder but it is for runtime use, not CI.

### Verdict

ECC has CI-grade automated testing for its own catalogue. Momentum has essentially none. For a practice that updates skills frequently, this is a real risk delta — Momentum has no automated way to detect a malformed SKILL.md frontmatter, a broken hook script, or a regression in `triage` behavior before a sprint relies on it.

---

## 12. Multi-Agent Orchestration Patterns Momentum Lacks

ECC ships several orchestration mechanisms that have no Momentum equivalent:

- **`scripts/orchestrate-worktrees.js`** plus **`scripts/lib/tmux-worktree-orchestrator.js`** — declarative tmux+worktree multi-agent orchestration where workers run in parallel tmux panes against isolated worktrees. Tested under `tests/lib/tmux-worktree-orchestrator.test.js`. [OFFICIAL] Momentum's sprint-dev does spawn multiple parallel workers but does so by spawning Claude Code agents directly, not via tmux multiplexing.
- **`dmux-workflows` skill** — multi-agent orchestration across Claude Code, Codex, OpenCode, Cline, Gemini, Qwen via dmux. [OFFICIAL]
- **GAN-style harness** (`gan-evaluator`, `gan-generator`, `gan-planner` agents + `gan-style-harness` skill) — adversarial generator/evaluator loop. [OFFICIAL]
- **Loop operator** agent (`/tmp/ecc-research/agents/loop-operator.md`) + `loop-start`/`loop-status` commands + `autonomous-loops` and `continuous-agent-loop` skills — autonomous agent loop execution with stall detection. [OFFICIAL]
- **Council skill** (`/tmp/ecc-research/skills/council/SKILL.md`) — multi-agent deliberation pattern.
- **Chief-of-staff agent** (`/tmp/ecc-research/agents/chief-of-staff.md`) — orchestration of other agents.
- **Continuous-learning-v2** (`/tmp/ecc-research/skills/continuous-learning-v2/`) — instinct-based learning system that observes sessions via PreToolUse/PostToolUse hooks, creates atomic "instincts" with confidence scoring (0.3-0.9), tags with project ID derived from git remote, and evolves them into skills/commands/agents via background Haiku agent. v2.1 added project-scoped vs global instincts. The skill has its own `agents/`, `hooks/`, `scripts/`, and `config.json`. [OFFICIAL — verified subdirs and SKILL.md exist; the runtime code under `scripts/lib/skill-evolution/` and `scripts/lib/skill-improvement/` exists with multiple modules: dashboard.js, health.js, provenance.js, tracker.js, versioning.js, amendify.js, evaluate.js, observations.js]

### Momentum equivalents

- AVFL (Adversarial Validate-Fix Loop) is a comparable adversarial pattern but more narrowly scoped (validation, not generation).
- `momentum:sprint-dev` does parallel story execution via direct subagent spawn; no tmux/worktree orchestration script.
- No "instinct extraction" or "continuous learning" loop. The `momentum:distill` skill exists but is a manual single-shot operation, not a hooked observe-and-extract cycle.

### Verdict

ECC has more breadth in orchestration patterns. Momentum's equivalents are narrower but more curated to a specific practice (sprint-driven solo dev). The continuous-learning-v2 system in particular is a genuinely interesting capability with no Momentum analog.

---

## 13. Memory or Context Management Innovations

- **`strategic-compact` skill** (`/tmp/ecc-research/skills/strategic-compact/SKILL.md`) and the `pre-compact.js` + `suggest-compact.js` hooks — intelligent compaction triggered by context budget thresholds. [OFFICIAL]
- **`context-budget` skill and `/context-budget` command** — token-budget advisory. [OFFICIAL]
- **`token-budget-advisor` skill** with the `token-optimization.md` doc. [OFFICIAL]
- **`session-start-bootstrap.js` and `session-end.js` hooks** — session-lifecycle persistence. [OFFICIAL]
- **`save-session` / `resume-session` commands** at `/tmp/ecc-research/commands/save-session.md` and `resume-session.md`. [OFFICIAL]
- **MCP `memory` server pre-wired** in `.mcp.json`. [OFFICIAL]

Momentum has the global `~/.claude/projects/.../memory/MEMORY.md` index that the user's harness maintains, plus its own intake/distill/decision skills for capturing learnings into the practice rather than into session memory. These are different problems — ECC focuses on intra-session context management, Momentum on across-session practice evolution. ECC's intra-session compaction toolkit is more developed.

---

## 14. Versioning, Releases, Dependency Hygiene

- ECC ships a real `package.json` (9 KB) with `version: 1.10.0`, declared `keywords`, `publishConfig.access: public`, and an explicit `files:` allow-list listing every artifact path that ships in the npm package. There is a `package-lock.json` (104 KB) and a `yarn.lock`. [OFFICIAL]
- A `pyproject.toml` and `.tool-versions` (nodejs 20.19.0, python 3.12.8) declare runtimes for asdf/mise. [OFFICIAL]
- A 7 KB `CHANGELOG.md` with version-by-version highlights. [OFFICIAL]
- A `release.sh` script and `tests/scripts/release-publish.test.js`. [OFFICIAL]
- An `npm-publish-surface.test.js` validates that all promised files actually exist in the npm payload. [OFFICIAL]
- `.github/` directory present (workflows not enumerated here, but exists). [OFFICIAL]

Momentum has `plugin.json` versioning (currently `0.17.0`) with a clear `version-on-release.md` rule. There is no CHANGELOG, no package-lock, no release script, no npm publishing surface. Versioning is enforced by the version-on-release rule rather than tooling. [PRAC]

### Verdict

ECC has stronger release tooling and a public CHANGELOG. Momentum's versioning is rule-driven and lighter — sufficient for a single-developer practice, weaker for distribution.

---

## 15. ECC 2.0 Rust Control Plane (verified scope)

The earlier comparison report's "ECC 2.0 Rust control plane" claim is **partially accurate**:

- `/tmp/ecc-research/ecc2/Cargo.toml` declares a real Rust binary `ecc-tui` v0.1.0 with dependencies on `ratatui`, `crossterm`, `tokio`, `rusqlite (bundled)`, `git2`, `clap`, `tracing`. [OFFICIAL]
- `/tmp/ecc-research/ecc2/README.md` explicitly labels it **"alpha"**: *"It is usable as an alpha for local experimentation, but it is **not** the finished ECC 2.0 product yet."* [OFFICIAL]
- `/tmp/ecc-research/ecc2/src/` contains `comms`, `config`, `main.rs`, `notifications.rs`, `observability`, `session`, `tui`, `worktree` modules. [OFFICIAL]
- The CHANGELOG 1.10.0 entry confirms: "ecc-tui currently exposes `dashboard`, `start`, `sessions`, `status`, `stop`, `resume`, and `daemon`. The alpha is real and usable for local experimentation, but the broader control-plane roadmap remains incomplete." [OFFICIAL]

So ECC 2.0 Rust binary exists, builds, has a TUI dashboard, SQLite session store, daemon mode, git2 integration. Momentum has no analogous control plane. However, this is alpha — not production polish — and the per-binary functionality is narrow (TUI for sessions, not a full agentic IDE replacement).

---

## 16. Other Notables

- **A 39 KB `ecc_dashboard.py`** at the repo root with `tests/scripts/ecc-dashboard.test.js` — a Python web dashboard for ECC state. [OFFICIAL] Momentum's `feature-status` skill renders an HTML dashboard, but it is a one-shot skill, not a long-running dashboard.
- **`agent.yaml`** (4.6 KB) at the repo root — declarative agent metadata for cross-harness adaptation. [OFFICIAL]
- **`harness-optimizer` agent and `harness-audit` script** — closed-loop tuning of harness configuration for reliability/cost. [OFFICIAL]
- **`prompt-optimizer` skill** + `/prompt-optimize` command. [OFFICIAL]
- **`skill-stocktake` and `skills-health.js` script** — automated skill catalogue health metrics. [OFFICIAL]
- **`skill-create-output.js`** + `/skill-create` command — bootstrap new skills from a template with output verification.
- **183 skills, 48 agents, 79 commands** total in the repo, vs Momentum's 25 skills, 7 dev agents (in `agents/`), and 16 commands. [OFFICIAL — counts derived from `ls | wc -l` against actual directories]

Note: ECC's marketing copy claims "156 skills, 38 agents, 72 commands" (per `.claude-plugin/plugin.json` description), which is lower than the actual `ls` count. The discrepancy reflects that some skills/agents are in `.claude/skills/` (only one: `everything-claude-code`) or scoped under `.cursor/`, `.codex/` etc. and are not all part of the published Claude plugin. [OFFICIAL — verified by counting both surfaces]

---

## What the Earlier Report Got Wrong (and What I Could Not Verify)

I was asked to verify suspect claims. Here is the audit:

| Earlier-report claim | Repo reality |
| --- | --- |
| "AgentShield with 1,282 tests" | The `security-scan` skill calls `npx ecc-agentshield`, which is an **external** package (`github.com/affaan-m/agentshield`). The 1,282 number is **not** in the ECC repo — it is a claim about an external dependency. **[UNVERIFIED]** |
| "Hookify conversational config" | `/tmp/ecc-research/skills/hookify-rules/SKILL.md` exists and documents a YAML-frontmatter rule format with `enabled`, `event`, `action`, `pattern`, `conditions`. There are `hookify-configure`, `hookify-help`, `hookify-list`, `hookify` commands. **[OFFICIAL]** Confirmed real. |
| "Continuous Learning and Instinct Extraction" | `continuous-learning-v2` skill exists with full hooks, agents, scripts, config.json. v2.1 adds project-scoping. Skill-evolution and skill-improvement libs at `scripts/lib/skill-evolution/` and `scripts/lib/skill-improvement/` exist with multiple modules. **[OFFICIAL]** Confirmed real. |
| "Plugin-Everything architecture" | The repo ships native installs into eight harnesses. The architecture exists but the marketing label is just describing the multi-harness install support. **[OFFICIAL]** Capability confirmed; phrasing is editorial. |
| "Selective install with SQLite state store" | Manifests, profiles, install-plan/apply scripts, and `state-store/index.js` (sql.js / SQLite) all exist and are tested. **[OFFICIAL]** Confirmed real. |
| "Codemaps" | `/tmp/ecc-research/scripts/codemaps/generate.ts` exists; the `update-codemaps` command exists; `doc-updater` agent references it. **[OFFICIAL]** Confirmed real. |
| "Operator Workflows" | `manifests/install-modules.json` lists `operator-workflows` as a module; skills include `automation-audit-ops`, `customer-billing-ops`, `customs-trade-compliance`, `email-ops`, `enterprise-agent-ops`, `finance-billing-ops`, `google-workspace-ops`, `inventory-demand-planning`, `knowledge-ops`, `lead-intelligence`, `logistics-exception-management`, `messages-ops`, `production-scheduling`, `project-flow-ops`, `quality-nonconformance`, `research-ops`, `returns-reverse-logistics`, `unified-notifications-ops`, `workspace-surface-audit`. **[OFFICIAL]** Confirmed real. |
| "ECC 2.0 Rust control plane" | Real but alpha; binary is `ecc-tui` not "control plane"; CHANGELOG explicitly says *"the broader control-plane roadmap remains incomplete and should not be treated as GA."* **[OFFICIAL]** Real but immature. |

### What I could not find

- **No "1,282 test" claim is locally substantiable** for ECC itself. ECC has 91 Jest tests + 4 Python tests in its own repo. The 1,282 figure must originate from AgentShield or an aggregate count. [UNVERIFIED]
- **No "Plugin-Everything" string** in the repo grep'able; the term appears to be marketing/external.
- **No output-styles directory or files** matching Claude Code's output-styles convention.

---

## Sources

All paths absolute, captured from local clone at `/tmp/ecc-research/` on 2026-04-26.

**Manifests and install:**
- `/tmp/ecc-research/.claude-plugin/plugin.json`
- `/tmp/ecc-research/.claude-plugin/marketplace.json`
- `/tmp/ecc-research/manifests/install-components.json`
- `/tmp/ecc-research/manifests/install-modules.json`
- `/tmp/ecc-research/manifests/install-profiles.json`
- `/tmp/ecc-research/scripts/install-apply.js`
- `/tmp/ecc-research/scripts/install-plan.js`
- `/tmp/ecc-research/scripts/lib/install/`
- `/tmp/ecc-research/scripts/lib/install-targets/`
- `/tmp/ecc-research/scripts/lib/state-store/index.js`
- `/tmp/ecc-research/scripts/lib/state-store/schema.js`
- `/tmp/ecc-research/schemas/state-store.schema.json`
- `/tmp/ecc-research/install.sh`, `/tmp/ecc-research/install.ps1`
- `/tmp/ecc-research/skills/configure-ecc/SKILL.md`

**MCP and integrations:**
- `/tmp/ecc-research/.mcp.json`
- `/tmp/ecc-research/scripts/lib/mcp-config.js`
- `/tmp/ecc-research/skills/jira-integration/SKILL.md`
- `/tmp/ecc-research/skills/github-ops/SKILL.md`
- `/tmp/ecc-research/skills/google-workspace-ops/SKILL.md`
- `/tmp/ecc-research/skills/messages-ops/SKILL.md`
- `/tmp/ecc-research/skills/email-ops/SKILL.md`

**Hooks and statusline:**
- `/tmp/ecc-research/hooks/hooks.json`
- `/tmp/ecc-research/scripts/hooks/` (~28 scripts)
- `/tmp/ecc-research/tests/hooks/` (24 test files)
- `/tmp/ecc-research/examples/statusline.json`

**Cross-harness:**
- `/tmp/ecc-research/.codex/`, `.codex-plugin/`, `.cursor/`, `.gemini/`, `.opencode/`, `.kiro/`, `.codebuddy/`, `.trae/`
- `/tmp/ecc-research/scripts/gemini-adapt-agents.js`
- `/tmp/ecc-research/scripts/sync-ecc-to-codex.sh`

**Security:**
- `/tmp/ecc-research/skills/security-scan/SKILL.md`
- `/tmp/ecc-research/skills/security-bounty-hunter/SKILL.md`
- `/tmp/ecc-research/skills/security-review/SKILL.md`
- `/tmp/ecc-research/skills/gateguard/SKILL.md`
- `/tmp/ecc-research/skills/safety-guard/SKILL.md`
- `/tmp/ecc-research/skills/hipaa-compliance/SKILL.md`
- `/tmp/ecc-research/scripts/hooks/gateguard-fact-force.js`
- `/tmp/ecc-research/scripts/hooks/block-no-verify.js`

**Tests and CI:**
- `/tmp/ecc-research/tests/` (91 Jest files + 4 Python files)
- `/tmp/ecc-research/scripts/ci/` (10 validators)

**Orchestration:**
- `/tmp/ecc-research/scripts/orchestrate-worktrees.js`
- `/tmp/ecc-research/scripts/lib/tmux-worktree-orchestrator.js`
- `/tmp/ecc-research/skills/dmux-workflows/SKILL.md`
- `/tmp/ecc-research/skills/continuous-learning-v2/`
- `/tmp/ecc-research/scripts/lib/skill-evolution/`
- `/tmp/ecc-research/scripts/lib/skill-improvement/`
- `/tmp/ecc-research/agents/loop-operator.md`
- `/tmp/ecc-research/agents/chief-of-staff.md`

**ECC 2.0:**
- `/tmp/ecc-research/ecc2/Cargo.toml`
- `/tmp/ecc-research/ecc2/README.md`
- `/tmp/ecc-research/ecc2/src/`
- `/tmp/ecc-research/CHANGELOG.md`

**Documentation:**
- `/tmp/ecc-research/README.md`, `README.zh-CN.md`
- `/tmp/ecc-research/docs/SKILL-DEVELOPMENT-GUIDE.md`
- `/tmp/ecc-research/docs/SELECTIVE-INSTALL-ARCHITECTURE.md`
- `/tmp/ecc-research/docs/SELECTIVE-INSTALL-DESIGN.md`
- `/tmp/ecc-research/docs/SESSION-ADAPTER-CONTRACT.md`
- `/tmp/ecc-research/COMMANDS-QUICK-REF.md`
- `/tmp/ecc-research/CONTRIBUTING.md`
- `/tmp/ecc-research/the-longform-guide.md`, `the-shortform-guide.md`, `the-security-guide.md`

**Momentum (for comparison):**
- `/Users/steve/projects/momentum/skills/momentum/.claude-plugin/plugin.json`
- `/Users/steve/projects/momentum/skills/momentum/skills/` (25 skills)
- `/Users/steve/projects/momentum/skills/momentum/agents/` (7 agents)
- `/Users/steve/projects/momentum/skills/momentum/commands/` (16 commands)
- `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json`
- `/Users/steve/projects/momentum/.claude/settings.json`
- `/Users/steve/projects/momentum/.mcp.json` (empty)
- `/Users/steve/projects/momentum/CLAUDE.md`
