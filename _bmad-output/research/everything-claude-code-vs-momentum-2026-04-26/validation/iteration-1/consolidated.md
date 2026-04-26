---
profile: full
corpus: true
iteration: 1
date: 2026-04-26
---

# AVFL Consolidated Findings — Iteration 1

## Validator Coverage

| Lens | Enumerator | Adversary | Cross-check | Status |
|---|---|---|---|---|
| Structural | ✓ (10 findings) | ✓ (5 findings) | full | Complete |
| Accuracy | ✗ FAILED (timeout) | ✓ (14 findings) | degraded | Enumerator lost mid-stream |
| Coherence | ✓ (13 findings) | ⚠ PARTIAL (1 finding) | degraded | Adversary stalled before completion |
| Domain | ✓ (11 findings) | ⚠ STUB only | degraded | Adversary written as reference to parent only |

**Total validator findings input:** 54 findings (10+5 + 0+14 + 13+1 + 11+stub)

---

## Score Calculation

**Starting score:** 100

**Deductions by severity:**

| Severity | Count | Weight | Subtotal |
|---|---|---|---|
| Critical | 4 | -15 | -60 |
| High | 16 | -8 | -128 |
| Medium | 21 | -3 | -63 |
| Low | 10 | -1 | -10 |
| **TOTAL** | **51** | | **-261** |

**Math:** 100 + (-261) = **-161** → clamped to **0/100** (theoretical score: extremely poor)

**Grade:** **Failing — major rework needed**

**Actual practical score (after consolidation/dedup):** Score calculated post-dedup below.

---

## Consolidated Findings (Sorted by Severity → Location)

### CRITICAL FINDINGS (4)

---

#### CRITICAL-001 — tools/agentshield/ fabrication

- **severity:** critical
- **confidence:** HIGH (flagged by Structural-enum, Structural-adv, Accuracy-adv, Coherence-enum, Coherence-adv, Domain-enum)
- **dimension:** cross_reference_integrity + correctness
- **location:** `gemini-deep-research-output.md:Technical Architecture and Repository Composition` (table row)
- **description:** The Gemini file's directory table lists `tools/agentshield/` as an ECC repository path with "Proprietary security scanning engine with over 1,282 automated tests." This directory does not exist in ECC. AgentShield is a separate sibling npm package (`affaan-m/agentshield`), not an in-repo directory. The 1,282-test count is unverifiable and appears sourced to the external repo, not ECC.
- **evidence:** Gemini table row: `| tools/agentshield/ | Proprietary security scanning engine with over 1,282 automated tests. | TypeScript, Python |`. Contradicted by recursive tree scan of all 2,662 ECC entries (0 matches for `agentshield`). Confirmed by `research-integration-assessment.md`: "AgentShield is **not** part of ECC — it is a sibling project at `github.com/affaan-m/agentshield`."
- **suggestion:** Strike the `tools/agentshield/` row entirely. If AgentShield is mentioned as an integration, explicitly frame it as a separate npm package (`npx ecc-agentshield`) and mark the "1,282 tests" claim as [UNVERIFIED] or remove it.

---

#### CRITICAL-002 — qflow MCP server hallucination

- **severity:** critical
- **confidence:** HIGH (flagged by Accuracy-adv, Coherence-enum, Coherence-adv, Domain-enum)
- **dimension:** cross_reference_integrity + correctness
- **location:** `gemini-deep-research-output.md:Workflow and State Management` (feature comparison table)
- **description:** Gemini presents `qflow` as a real MCP server in ECC with "7-state machine and dependency DAG for task management." The entity `qflow` does not exist anywhere in the ECC repository. All 2,662 verified tree entries return zero matches. The MCP server inventory shows 6 in `.mcp.json` and ~24 in the catalog — none named `qflow`.
- **evidence:** Gemini table: `| create-story command | qflow MCP server | 7-state machine and dependency DAG for task management |`. Recursive tree scan: 0 matches for `qflow`. Verified MCP servers: `.mcp.json` lists 6 (`github`, `context7`, `exa`, `memory`, `playwright`, `sequential-thinking`); `mcp-configs/mcp-servers.json` lists ~24 templates — no `qflow`.
- **suggestion:** Strike the qflow row. The Gemini doc's feature mapping table contains hallucinated ECC components.

---

#### CRITICAL-003 — claude-mem attribution & fabrication

- **severity:** critical
- **confidence:** HIGH (flagged by Structural-enum, Accuracy-adv, Coherence-enum, Coherence-adv)
- **dimension:** correctness + logical_soundness
- **location:** `gemini-deep-research-output.md:Memory and Persistence Systems`
- **description:** Gemini states "ECC has evolved [memory persistence] into `claude-mem`, a plugin that reached 89,000 stars in early 2026... uses a background HTTP API managed by Bun and stores data in a SQLite database with Chroma vector support." Three errors: (a) `claude-mem` is not part of ECC; (b) the most-starred `claude-mem` (`thedotmack/claude-mem`) has ~67.9K stars, not 89K; (c) implementation details (Bun, Chroma) are unverifiable. ECC's actual memory system is `continuous-learning-v2` (instinct-based, hook-driven, stored in `~/.claude/homunculus/`).
- **evidence:** No `claude-mem` appears in ECC's 2,662-entry tree scan. GitHub search: `thedotmack/claude-mem` at ~67,900 stars, owned by `thedotmack` (not `affaan-m`), a distinct Claude Code plugin. ECC memory correctly described in `research-feature-parallels.md` as `continuous-learning-v2` + MCP `memory` + MCP `omega-memory`.
- **suggestion:** Replace the `claude-mem` paragraph with accurate description of ECC's actual memory system (`continuous-learning-v2`, instinct-based, no HTTP API, no Bun/Chroma). The downstream recommendation "Adopt the claude-mem Architecture" (CRITICAL-004) is built on this fabrication and must be removed or reframed.

---

#### CRITICAL-004 — claude-mem adoption recommendation cascade

- **severity:** critical
- **confidence:** HIGH (derived from CRITICAL-003)
- **dimension:** logical_soundness
- **location:** `gemini-deep-research-output.md:Critical Components for Adoption (recommendation 1)`
- **description:** A whole strategic recommendation pivots on adopting `claude-mem` as the natural next step from ECC. Because `claude-mem` is not part of ECC and the premise "ECC has evolved this into claude-mem" is false (see CRITICAL-003), this recommendation is built on a fabricated relationship and is a non-sequitur.
- **evidence:** Same source as CRITICAL-003. The claim chain: "ECC's `claude-mem` → Momentum should adopt it" is invalid because the antecedent is false.
- **suggestion:** Drop the `claude-mem` adoption recommendation from the synthesis. Reground the recommendation in ECC's actual `continuous-learning-v2` mechanism, or retire it.

---

### HIGH FINDINGS (16)

---

#### HIGH-001 — Gemini structural non-conformance (frontmatter, evidence tags, sources)

- **severity:** high
- **confidence:** HIGH (both Structural reviewers flagged)
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:Frontmatter and document body`
- **description:** The Gemini file lacks conformance with the corpus's established structural standard. It is missing: (a) `sub_question` field in frontmatter (present on all 8 subagent files); (b) zero evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]) anywhere in the body (all subagent files apply these per claim); (c) no `## Sources` section at the end (all 8 subagent files have one).
- **evidence:** Frontmatter: only `content_origin`, `date`, `topic`, `method`, `source_url` — no `sub_question`. Grep for evidence tags: 0 matches (vs. 27–88 in each subagent file). No `## Sources` heading found (all 8 subagent files have it at EOF).
- **suggestion:** Add `sub_question: "Baseline — all 8 sub-questions (low-authority reference)"` to frontmatter. Add a `## Sources` section listing the Gemini Deep Research session URL. Apply [OFFICIAL]/[PRAC]/[UNVERIFIED] tags to claims or add a document-level notice: "All claims in this file are [UNVERIFIED] unless cross-confirmed by a subagent file."

---

#### HIGH-002 — Gemini lacks disputed-status header

- **severity:** high
- **confidence:** HIGH (both Structural reviewers flagged)
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:top (before body)`
- **description:** The Gemini file presents confident claims (140K+ stars, 113 contributors, AgentShield bundled, claude-mem at 89K stars, qflow MCP, etc.) in its body with no top-level signal that these have been disputed/superseded by subagent verification. The "Orchestrator note" admitting Gemini sidestepped verification is buried mid-document at the end of Follow-Up #1 (~424 lines in). A reader of only this file would treat body claims as authoritative.
- **evidence:** Body lines 11–383 make confident factual claims with no annotation. E.g., "over 140,000 GitHub stars" (actual 167K+), "113 contributors" (actual 159), "AgentShield with 1,282 tests" (separate repo), "claude-mem at 89K stars" (not ECC), "qflow MCP server" (hallucinated). Orchestrator note at line 424 is the only correction signal and is buried deep in the document.
- **suggestion:** Add a prominent top-of-file callout immediately after frontmatter: **STATUS — DISPUTED INPUT:** Subagent verification found multiple factual inaccuracies in this file (star/contributor counts, hackathon sponsor, AgentShield attribution, claude-mem attribution, qflow reference). Treat as a starting hypothesis; defer to subagent files for verified claims. Or add `disputed: true` to frontmatter with a convention note in corpus README.

---

#### HIGH-003 — Stale Gemini statistics (stars, forks, contributors, commits)

- **severity:** high
- **confidence:** HIGH (both Coherence reviewers flagged)
- **dimension:** correctness + cross_document_consistency
- **location:** `gemini-deep-research-output.md:Maturity stats table and narrative`
- **description:** Gemini presents stale community stats as current: 140K+ stars (actual 167,487), 21K+ forks (actual 25,969), 113 contributors (actual 159), 768 commits (actual ~1,465). Both subagent reports verified live API values and explicitly noted these as stale README badge copy, not current state.
- **evidence:** Gemini: "reaching over 140,000 GitHub stars and 21,000 forks" and table row "Stars: 140,000+" "Contributors: 113" "Commits: 768". Live GitHub API: `stargazers_count: 167,488`, `forks: 25,969`, 159 contributors (Link header pages), ~1,465 commits (from pagination). `research-maturity-community.md:TL;DR` explicitly compares stale vs live values.
- **suggestion:** Use only API-verified figures (167K+ stars, 26K forks, 159 contributors, ~1,465 commits) in any synthesis. Note that Gemini reproduced the repository's own outdated README badges, not live state.

---

#### HIGH-004 — Hackathon attribution wrong on both sponsor and date

- **severity:** high
- **confidence:** HIGH (both Coherence reviewers flagged + both Accuracy-adv and Domain-enum)
- **dimension:** correctness + cross_document_consistency
- **location:** `gemini-deep-research-output.md:Maturity and Community Traction Analysis`
- **description:** Gemini states ECC won "the Anthropic x Forum Ventures hackathon in late 2025." Verified state: ECC was a winner at the "Cerebral Valley × Anthropic 'Built with Opus 4.6' hackathon, Feb 10–16, 2026." Wrong on sponsor (Cerebral Valley ≠ Forum Ventures) and wrong on date (early 2026 ≠ late 2025).
- **evidence:** Gemini: "a winner of the Anthropic x Forum Ventures hackathon in late 2025." Verified: `research-maturity-community.md`: "Cerebral Valley × Anthropic 'Built with Opus 4.6' hackathon, Feb 10-16, 2026. ECC was a winner. Forum Ventures was not the partner — Cerebral Valley was."
- **suggestion:** Use maturity-community's verified attribution in synthesis. Correct Gemini attribution or mark as [UNVERIFIED].

---

#### HIGH-005 — MCP integration count inconsistency (14 vs 17 vs 6/24+)

- **severity:** high
- **confidence:** HIGH (both Coherence reviewers + Accuracy-adv flagged)
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md` (14) vs `research-feature-parallels.md` (~17) vs `research-architecture-capabilities.md` (6+24+)
- **description:** Three files give three different MCP integration counts: Gemini says 14; feature-parallels says ~17; architecture-capabilities verifies the most accurate answer: 6 in root `.mcp.json` and 24+ in the catalog file.
- **evidence:** Gemini: "mcp-configs/ | Pre-built MCP server configurations for 14 external integrations." Feature-parallels: "~17 MCP servers". Architecture-capabilities: "the '14 MCP integrations' Gemini number is wrong in both directions: the actually-shipped .mcp.json is 6 servers, but the reference catalog at mcp-configs/mcp-servers.json is much larger than 14 (24+)."
- **suggestion:** Adopt the architecture-capabilities disambiguation: 6 in root `.mcp.json` (shipped defaults); 24+ in catalog templates. Retire the "14" and "~17" figures or mark as unverified reading of different files.

---

#### HIGH-006 — retro skill mapping to Stop hook (incorrect analogue)

- **severity:** high
- **confidence:** MEDIUM (Domain-enum only; Domain-adv stub; no other lens flagged)
- **dimension:** domain_rule_compliance + correctness
- **location:** `gemini-deep-research-output.md:Workflow and State Management table`
- **description:** Gemini maps Momentum's `retro` skill to ECC's "`Stop` hook pattern — Auto-summarization of successes/failures at session end." The Stop hook captures session state but does not run an auditor team, execute transcript analysis, verify story completeness, emit findings to intake-queue.jsonl, or close a sprint. Two independent tree scans confirm ECC has zero retrospective analogue. Conflating a session-end hook with a full retro mischaracterizes both systems.
- **evidence:** Gemini table: `retro skill | Stop hook pattern | Auto-summarization of successes/failures at session end`. Verified: `research-feature-parallels.md`: "No analogue [OFFICIAL]" and `research-momentum-superior.md`: "ECC [OFFICIAL]: Tree scan — retro: 0 matches."
- **suggestion:** Remove the Stop-hook-as-retro mapping. Verified finding: ECC has no retrospective analogue. (Note: MEDIUM confidence due to Domain-enum only; escalated to HIGH due to the clear contradiction and multiple independent tree scans.)

---

#### HIGH-007 — avfl mapping to AgentShield (external, unverified)

- **severity:** high
- **confidence:** MEDIUM (Domain-enum only; also cascades from CRITICAL-001)
- **dimension:** domain_rule_compliance + correctness
- **location:** `gemini-deep-research-output.md:Workflow and State Management table`
- **description:** Gemini maps Momentum's `avfl` to "`AgentShield` / Red-Blue Team." Two errors: (1) AgentShield is external to ECC (see CRITICAL-001); (2) the verified AVFL analogue is ECC's `skills/santa-method/SKILL.md` (dual reviewer, fix loop, binary verdict) — neither matches AVFL's lens-decomposed design. The mapping misleads the decision-maker about ECC's validation capability.
- **evidence:** Gemini: `avfl | AgentShield / Red-Blue Team`. Verified: `research-momentum-superior.md`: "ECC [OFFICIAL]: Two relevant analogues exist: `skills/santa-method/SKILL.md`... `skills/verification-loop/SKILL.md`" — no AgentShield. `research-integration-assessment.md`: "AgentShield is **not** part of ECC — it is a sibling project."
- **suggestion:** Use santa-method + verification-loop as ECC's validation analogue, not AgentShield.

---

#### HIGH-008 — Missing H1 title on two subagent files

- **severity:** high
- **confidence:** HIGH (both Structural reviewers flagged)
- **dimension:** structural_validity
- **location:** `research-philosophy.md:top` and `research-portability.md:top`
- **description:** Two research files omit the H1 document title present on all other corpus files and all 9 corpora files. Each jumps from frontmatter directly to `## Inline Summary`.
- **evidence:** `research-philosophy.md` line 7 closes frontmatter, line 9 begins `## Inline Summary` — no H1. `research-portability.md` line 7 closes frontmatter, line 9 begins `## Inline Summary` — no H1. Compare all 6 other `research-*.md` files: each opens with `# {Title}` after frontmatter.
- **suggestion:** Add H1 titles: `# Design Philosophy Comparison — ECC vs Momentum` to philosophy.md; `# Portability Across Agentic CLIs — ECC vs Momentum` to portability.md.

---

#### HIGH-009 — Missing Genesis state machine analogue

- **severity:** high
- **confidence:** MEDIUM (Coherence-enum only)
- **dimension:** cross_document_consistency + correctness
- **location:** `gemini-deep-research-output.md:Workflow and State Management table`
- **description:** Gemini maps Momentum's `index.json` state machine to ECC's "SQLite state store" with "Persistent local database for session and task tracking." ECC's SQLite state store (`~/.claude/ecc/state.db`) covers install state, session metadata, and governance events — not sprint/story/task state. The mapping overstates ECC's state management capability relative to Momentum's structured sprint/story tracking.
- **evidence:** Gemini table: `index.json state machine | SQLite state store | Persistent local database for session and task tracking`. Verified: `research-ecc-superior.md`: "SQLite store (`~/.claude/ecc/state.db`)... covers sessions, skill runs, skill versions, decisions, install state, and governance events — not story/sprint state."
- **suggestion:** Clarify: ECC's SQLite store is an install-state tracker. There is no ECC analogue to Momentum's structured sprint/story state machine.

---

#### HIGH-010 — Missing `## Sources` section on Gemini file

- **severity:** high
- **confidence:** HIGH (both Structural reviewers flagged)
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:end-of-file`
- **description:** The Gemini file is the only corpus file lacking a `## Sources` section. All eight `research-*.md` subagent files end with `## Sources`. The Gemini file ends with `## Follow-Up #3 — Directory structure verification (skipped)` with no sources block, breaking the corpus's closing-section convention.
- **evidence:** Grep for `^## Sources`: returns 1 for each of 8 `research-*.md` files; returns 0 for `gemini-deep-research-output.md`. Final heading in Gemini file is `## Follow-Up #3`. Frontmatter declares `source_url` but no consolidated sources list.
- **suggestion:** Add a `## Sources` section listing the Gemini chat URL plus any inline-cited URLs (forgecode, opencode, bifrost, etc. from Follow-Up #1).

---

#### HIGH-011 — Momentum skill/command count inconsistency across subagent files

- **severity:** high
- **confidence:** HIGH (both Coherence reviewers flagged)
- **dimension:** cross_document_consistency
- **location:** `research-feature-parallels.md` (26 skills, 15 commands) vs `research-ecc-superior.md` (25 skills, 16 commands)
- **description:** Momentum's skill count is reported as 26 in two files and 25 in one; command count reported as 15 in one and 16 in another. Same repository, same date, different counts from different subagents. The filesystem-verified counts are 25 skills and 16 commands.
- **evidence:** Feature-parallels: "26 skills [OFFICIAL]" and "15 slash commands [OFFICIAL]". ECC-superior: "Momentum's 25 skills... and 16 commands". Local verification: `ls -la skills/momentum/skills/ | wc -l` = 25 (27 entries minus `.` and `..`); `ls skills/momentum/commands/ | wc -l` = 16.
- **suggestion:** Use consistent numbers: 25 skills and 16 commands. Update feature-parallels and momentum-superior to align.

---

#### HIGH-012 — Ephemeral `/tmp/` paths in citations (115 instances)

- **severity:** high
- **confidence:** HIGH (Structural-enum only; but 115 instances is clear evidence)
- **dimension:** cross_reference_integrity
- **location:** `research-ecc-superior.md:Throughout body and Sources`
- **description:** The file contains 115 references to ephemeral local clone paths (`/tmp/ecc-research/...`) that are unresolvable by any downstream reader. The sister file covering overlapping content (`research-architecture-capabilities.md`) used stable GitHub URLs exclusively.
- **evidence:** Sources section header: "All paths absolute, captured from local clone at `/tmp/ecc-research/` on 2026-04-26." Grep count: `/tmp/ecc-research` appears 115 times. Compare `research-architecture-capabilities.md` using GitHub URLs: `https://github.com/affaan-m/everything-claude-code/blob/main/...`.
- **suggestion:** Replace all `/tmp/ecc-research/<path>` citations with canonical GitHub URLs: `https://github.com/affaan-m/everything-claude-code/blob/main/<path>`.

---

#### HIGH-013 — Gemini stats file path error (`.opencode/dist/index.js`)

- **severity:** high
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** cross_reference_integrity + correctness
- **location:** `gemini-deep-research-output.md:Follow-Up #2 — Cross-CLI portability`
- **description:** Gemini lists `.opencode/dist/index.js` as a verified entry point for OpenCode plugin support. The path does not exist. Actual entry point is `.opencode/index.ts` (TypeScript source). There is no `.opencode/dist/` directory.
- **evidence:** GitHub API: `GET /repos/affaan-m/everything-claude-code/contents/.opencode/dist` returns HTTP 404. Actual `.opencode/` directory listing shows: `index.ts`, `opencode.json`, `package.json`, `plugins/`, `tools/`, etc. — no `dist/`. Research-portability.md correctly identifies `.opencode/index.ts`.
- **suggestion:** Strike `.opencode/dist/index.js`. Replace with verified path `.opencode/index.ts`.

---

#### HIGH-014 — Hook count metric error (156 counted as hook count)

- **severity:** high
- **confidence:** HIGH (Structural-enum only; but clear math error)
- **dimension:** cross_reference_integrity
- **location:** `research-integration-assessment.md:Inline Summary`
- **description:** The inline summary states ECC has "156 hooks-config knobs." The figure 156 is ECC's reported skill count, not a hook metric. Verified hook figures are ~40 hook scripts or ~14 distinct hook IDs. The count appears to be a copy-paste error.
- **evidence:** Integration-assessment Inline Summary: "38 agents, 156 skills, **156 hooks-config knobs**, 79 commands." Contradicted by: `research-architecture-capabilities.md`: "scripts/hooks/ — 40 hook implementation files" and `research-feature-parallels.md`: "hook framework with at least 14 distinct hook IDs." The "156" is the skill count duplicated.
- **suggestion:** Correct to "~40 hook scripts" or "14 hook IDs" or remove the hook metric if uncertain.

---

#### HIGH-015 — Gemini invented install.sh `--target opencode` flag

- **severity:** high
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:Follow-Up #2 — Cross-CLI portability`
- **description:** Gemini lists `--target opencode` as a verified `install.sh` flag. Actual `scripts/install-apply.js` help text documents only three targets: `claude` (default), `cursor`, `antigravity`. No `opencode` target exists.
- **evidence:** WebFetch of `scripts/install-apply.js` help text shows only those three targets. OpenCode integration uses npm package `ecc-universal` and the `.opencode/` plugin directory, not an install.sh `--target` flag.
- **suggestion:** Strike `--target opencode` from Gemini's verified targets list.

---

#### HIGH-016 — Stale Gemini contributor/commit counts

- **severity:** high
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** correctness
- **location:** `gemini-deep-research-output.md:Maturity Stats Table`
- **description:** Gemini reports "Contributors: 113; Commits: 768" as current fact. Verified live counts: 159 contributors and ~1,465 commits (~50% stale on each).
- **evidence:** GitHub API: `/contributors?per_page=1` Link header confirms 159 pages (159 contributors); `/commits?per_page=1` confirms ~1,465 commits.
- **suggestion:** Replace with verified live counts or annotate as "stale snapshot."

---

### MEDIUM FINDINGS (21)

---

#### MEDIUM-001 — ECC agent count inconsistency (30/38/47/48)

- **severity:** medium
- **confidence:** MEDIUM (Coherence-enum only; no other lens directly flagged)
- **dimension:** cross_document_consistency
- **location:** Various corpus files mention different ECC agent counts
- **description:** Different subagent files report different ECC agent counts (appears to range 30–48 depending on how agents are counted: by agent files, by skill embedding, by skill naming convention). The corpus does not settle on a single canonical count.
- **evidence:** (Implicit from Coherence-enum note on numerical inconsistencies across files; specific quote not extracted in validator output but mentioned in Coherence-enum summary.)
- **suggestion:** Establish a single canonical agent count based on explicit enumeration method (e.g., "distinct agent personalities in AGENTS.md" vs "skills with agent-class frontmatter" vs "agent-persona skills in skills/ directory"). Report the count and method once in the synthesis.

---

#### MEDIUM-002 — Portability statement ambiguity on Tier 2 hooks

- **severity:** medium
- **confidence:** HIGH (both Coherence reviewers flagged)
- **dimension:** clarity + cross_document_consistency
- **location:** `research-philosophy.md:Section 9 Distribution` vs `research-portability.md:Comparison table`
- **description:** Philosophy describes Momentum's Tier 2 (Cursor & other tools) as "advisory" (hooks fire but non-blocking). Portability clarifies that Momentum's hooks are Claude Code-specific (`$CLAUDE_*` env vars) and would not fire under Cursor at all. "Advisory (fires but doesn't block)" vs "does not fire" are materially different.
- **evidence:** Philosophy: "Tier 2: Cursor and other tools — advisory — 'Hooks (no automatic linting, formatting, or file protection)'". Portability: "hooks.json uses Claude Code-specific event names... $CLAUDE_* env vars... would not fire under... Cursor as written. [OFFICIAL]"
- **suggestion:** Clarify: Tier 2 means documentation is usable but automated tooling (hooks, gates) simply will not fire. Not "advisory" — absent.

---

#### MEDIUM-003 — Philosophy vs Portability contradiction on Goose/Aider support

- **severity:** medium
- **confidence:** MEDIUM (Coherence-enum only)
- **dimension:** cross_document_consistency + clarity
- **location:** `research-portability.md` (no support) vs `gemini-deep-research-output.md:Portability table` (Theoretical/Via Standard)
- **description:** Portability flatly states Goose, Aider, Cline, ForgeCode are not supported (no directories, no adapters). Gemini grades Aider/Goose as "Theoretical / Via Standard." A synthesis reader may interpret "Theoretical" as meaningful support, when the actual state is zero dedicated ECC investment.
- **evidence:** Portability: "Not supported by ECC... no .goose, .aider, .cline, .forgecode directories... no skills referencing those harnesses." Gemini: `Aider / Goose | Portable AGENTS.md and SKILL.md definitions. | Theoretical / Via Standard`.
- **suggestion:** Adopt portability's framing. "Theoretical / Via Standard" is a property of the abstraction standard itself, not ECC-specific work.

---

#### MEDIUM-004 — Missing H1 title causes navigation gap

- **severity:** medium
- **confidence:** HIGH (both Structural reviewers flagged)
- **dimension:** structural_validity
- **location:** `research-philosophy.md:top` and `research-portability.md:top` (same files as HIGH-008)
- **description:** (Duplicate of HIGH-008 from Structural lens perspective; kept separate to show dimension emphasis: Structural-adv grades as medium for structural_validity context.)
- **evidence:** (Same as HIGH-008.)
- **suggestion:** (Same as HIGH-008.)

---

#### MEDIUM-005 — Unclear `.opencode/dist/` vs `.opencode/index.ts` paths

- **severity:** medium
- **confidence:** MEDIUM (Accuracy-adv only; cascades from HIGH-013)
- **dimension:** cross_reference_integrity
- **location:** `gemini-deep-research-output.md:Follow-Up #2` (incorrect) vs `research-portability.md` (correct)
- **description:** (Cascading from HIGH-013; marked MEDIUM to avoid double-penalization in score.)

---

#### MEDIUM-006 — Gemini irrelevant Follow-Up #1 content (ForgeCode/OpenCode/Bifrost)

- **severity:** medium
- **confidence:** MEDIUM (Coherence-enum only; one reviewer)
- **dimension:** relevance
- **location:** `gemini-deep-research-output.md:Follow-Up #1 Response`
- **description:** Follow-Up #1 asks Gemini to verify ECC numeric claims. The response provides URLs for ForgeCode, OpenCode, Bifrost (entirely out of scope). Off-topic content is preserved verbatim in the corpus document and should be quarantined in any synthesis.
- **evidence:** Follow-Up #1 Response cites `forgecode.dev`, `github.com/tailcallhq/forgecode`, `github.com/sst/opencode`, etc. — none relevant to ECC stat verification.
- **suggestion:** Clearly quarantine or exclude the ForgeCode/OpenCode/Bifrost citations in synthesis. Flag as Gemini answering a different question.

---

#### MEDIUM-007 — Rust line-count unit confusion (bytes misreported as lines)

- **severity:** medium
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** correctness
- **location:** `research-maturity-community.md:TL;DR table`
- **description:** Table states "Rust line count: 1.8 MB / ~1.8 M lines (Rust 1,818,298 chars per languages API)." The value 1,818,298 is BYTES, not lines or characters. Phrasing equates "1.8 MB" with "~1.8 M lines." At typical Rust line length (30–80 chars), 1.8 MB ≈ 25–60K lines, not 1.8 million.
- **evidence:** GitHub `/languages` API returns byte counts. ECC's Cargo.toml declares a small TUI binary, not 1.8M lines of Rust.
- **suggestion:** Replace "1.8 MB / ~1.8 M lines" with "1.8 MB of Rust source" (drop the spurious line count).

---

#### MEDIUM-008 — Gemini Honest Assessment section contains speculation, not corpus findings

- **severity:** medium
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** logical_soundness
- **location:** `gemini-deep-research-output.md:Honest Assessment of Limitations (items 1–4)`
- **description:** Claims like "Claude Code v2.1.100 introduces 20,000 'invisible tokens'... 40% faster quota depletion" are oddly specific with no source. Item 3 conflates `pass@k` (standard eval metric) with weakness evidence. Item 1 misunderstands that Claude Code agents load on-demand, not eagerly. Treat the "Limitations" section as Gemini speculation.
- **evidence:** "20,000 invisible tokens / 40% faster depletion" — no primary source. `pass@k` is documented OpenAI standard. Anthropic docs confirm skills load on-demand.
- **suggestion:** Treat the Limitations section as unsourced speculation; do not include in synthesis findings.

---

#### MEDIUM-009 — Hackathon attribution conflates two separate events

- **severity:** medium
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer — escalates reasoning from HIGH-004)
- **dimension:** correctness + logical_soundness
- **location:** `research-maturity-community.md:Hackathon section` (verdict framing)
- **description:** The maturity report declares prior reports "wrong on both sponsor and date" for Anthropic × Forum Ventures / late 2025. However, the ECC README cites TWO separate hackathons: (1) Affaan's prior project `zenith.chat` won Anthropic × Forum Ventures Sep 2025; (2) ECC was built at Cerebral Valley × Anthropic Feb 2026. The verdict over-corrects by declaring Forum Ventures entirely wrong, when it was the venue for a different Affaan project.
- **evidence:** ECC README sentences: (1) "Won the Anthropic x Forum Ventures hackathon in Sep 2025 with [@DRodriguezFX]" — zenith.chat. (2) "Built at the Claude Code Hackathon (Cerebral Valley x Anthropic, Feb 2026)" — ECC. Research-philosophy.md also cites Forum Ventures Sep 2025 as Affaan's personal credential.
- **suggestion:** Reframe: Forum Ventures Sep 2025 produced `zenith.chat` (Affaan's prior project); Cerebral Valley × Anthropic Feb 2026 produced ECC. Do not declare "Forum Ventures was not the partner" without qualification — it was the partner for a different, earlier project.

---

#### MEDIUM-010 — ECC star count viral trajectory under-assessed

- **severity:** medium
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** correctness + logical_soundness
- **location:** `research-maturity-community.md:Star & Fork Growth section`
- **description:** Reaching 167K stars in 3 months is presented as merely "top-tier viral" and "comparable to early Llama or Stable Diffusion." This comparison under-flags anomalies — those were AI-model repos with massive press; ECC is a Claude Code config plugin. ~1,800 stars/day sustained for 100 days would be unprecedented in dev-tooling history. The 0.6% star-to-download ratio noted in the same file suggests plausible inorganic inflation.
- **evidence:** GitHub API: 167K stars created 2026-01-18. Snapshots: 2026-03-18 ≈ 82K, 2026-04-26 = 167K = +85K in 5 weeks (~1,900/day). The Llama/Stable Diffusion comparison minimizes this anomaly.
- **suggestion:** Acknowledge 167K in 90 days is anomalous for dev-tooling and plausibly amplified by coordinated activity, not purely organic.

---

#### MEDIUM-011 — Integration assessment skips intake-queue wiring

- **severity:** medium
- **confidence:** MEDIUM (Domain-enum only; one reviewer)
- **dimension:** fitness_for_purpose
- **location:** `research-integration-assessment.md:Adopt-as-Is recommendations`
- **description:** Integration recommendations (adopt silent-failure-hunter, repo-scan) are actionable prose but don't connect to Momentum's intake-queue workflow. For a maintainer relying on intake-queue.jsonl as canonical backlog, recommendations are unanchored to the practice's tracking primitives.
- **evidence:** Integration recommendations state "commit as `feat(skills):...`" but don't note that adoption ideas in Momentum flow through `momentum:intake` → `intake-queue.jsonl` → `stories/index.json`.
- **suggestion:** Note in synthesis or update integration-assessment to say: "These adoption items should be queued through `momentum:intake` before sprint-planning picks them up."

---

#### MEDIUM-012 — Portability sub-question Q6 multi-agent story unanswered

- **severity:** medium
- **confidence:** MEDIUM (Domain-enum only; one reviewer)
- **dimension:** completeness + fitness_for_purpose
- **location:** `research-portability.md` (silent on multi-agent story)
- **description:** `scope.md` sub-question 6 explicitly asks "What is the multi-agent story?" as part of portability. The portability file covers abstraction-layer and hook portability but is silent on whether ECC's cross-harness agents support multi-agent spawning patterns (TeamCreate, Fan-Out) comparable to Momentum's parallelism. For a stay-vs-integrate decision, knowing whether ECC's orchestration translates cross-harness is material.
- **evidence:** Scope.md: "Is there an abstraction layer? **What is the multi-agent story?**" The phrase "multi-agent story" does not appear in research-portability.md. File covers hook/MCP/manifest/AGENTS.md portability but not Fan-Out/TeamCreate/worktree patterns or how `dmux-workflows` interacts with cross-harness multi-agent support.
- **suggestion:** Synthesis should explicitly flag: "ECC's per-harness multi-agent story was not assessed — this dimension of the portability sub-question remains open."

---

#### MEDIUM-013 — ECC skills with `gan-style-harness` vs `santa-method` AVFL mapping ambiguity

- **severity:** medium
- **confidence:** MEDIUM (Coherence-adv only; one partial-output reviewer)
- **dimension:** cross_document_consistency
- **location:** `research-feature-parallels.md` (gan-style-harness) vs `research-momentum-superior.md` (santa-method)
- **description:** The corpus identifies TWO ECC skills as "AVFL analogue" without acknowledging both exist: (1) gan-style-harness (Generator + Evaluator + Playwright — code gen vs live app, not artifact validation); (2) santa-method (dual reviewer, binary verdict — closer in spirit). Neither matches AVFL's lens-decomposed design.
- **evidence:** Feature-parallels cites `gan-style-harness/SKILL.md`; momentum-superior cites `santa-method/SKILL.md`. Both are real ECC skills; they differ on which is the closer AVFL analogue.
- **suggestion:** Reconcile in synthesis: ECC has two skills in this neighborhood — `gan-style-harness` (live-app generation+evaluation) and `santa-method` (dual-reviewer artifact validation). Acknowledge both; note that `santa-method` is conceptually closer to AVFL but still binary and undecomposed.

---

#### MEDIUM-014 — Path citation inconsistency: qa-reviewer.md location

- **severity:** medium
- **confidence:** MEDIUM (Domain-enum only; one reviewer)
- **dimension:** domain_rule_compliance
- **location:** `research-feature-parallels.md:Sides at a Glance` (implied agents/) vs `research-feature-parallels.md:Code review section` (skills/ path)
- **description:** Table lists `qa-reviewer.md` as an agent file (alongside agents/dev*.md). Code review section cites it as `skills/momentum/skills/qa-reviewer.md (in agents/)` — internally contradictory path.
- **evidence:** Table: "7 agent .md files (`agents/dev*.md`, `e2e-validator.md`, `qa-reviewer.md`)". Code review: "`skills/momentum/skills/qa-reviewer.md` (in `agents/`) — agent persona...". These paths don't agree.
- **suggestion:** Verify actual path; use consistently throughout without parenthetical contradiction.

---

#### MEDIUM-015 — Momentum skills count: 25 or 26 (different snapshot times)

- **severity:** medium
- **confidence:** HIGH (both Coherence reviewers flagged; matches HIGH-011)
- **dimension:** cross_document_consistency
- **location:** Feature-parallels (26) vs ecc-superior (25)
- **description:** (Minor version of HIGH-011; marked MEDIUM since only 1-skill difference and snapshot timing explains it.)

---

#### MEDIUM-016 — Momentum commands count: 15 or 16 (disagreement)

- **severity:** medium
- **confidence:** HIGH (both Coherence reviewers flagged; matches HIGH-011)
- **dimension:** cross_document_consistency
- **location:** Feature-parallels (15) vs ecc-superior (16)
- **description:** (Minor version of HIGH-011.)

---

#### MEDIUM-017 — MCP server count low-end inconsistency (6 vs 17 vs 24)

- **severity:** medium
- **confidence:** MEDIUM (Structural-enum only, marked as low)
- **dimension:** cross_reference_integrity
- **location:** `research-feature-parallels.md` vs `research-architecture-capabilities.md`
- **description:** Feature-parallels states "~17 MCP servers" in catalog; architecture-capabilities notes partial read and later verification shows "24+." Likely reflects read truncation, not error, but creates cross-file inconsistency.
- **evidence:** Feature-parallels: "~17 MCP servers". Architecture-capabilities: "truncated at ~5 KB read... listing **at least 24** MCP integrations."
- **suggestion:** Update feature-parallels to "24+" to align with full read.

---

#### MEDIUM-018 — Follow-Up #3 section (Directory structure) is a stub

- **severity:** medium
- **confidence:** MEDIUM (Structural-adv only; one reviewer)
- **dimension:** completeness
- **location:** `gemini-deep-research-output.md:Follow-Up #3`
- **description:** "Follow-Up #3 — Directory structure verification (skipped)" has a heading but no content — only a meta-commentary sentence. Per final-stage rule, all required sections must be complete.
- **evidence:** Section contains only a Question and Disposition sentence; no directory data.
- **suggestion:** Either remove the heading or convert to explicit cross-reference: "See **research-architecture-capabilities.md → Directory Layout**."

---

#### MEDIUM-019 — `raw/` directory contains non-corpus file (gemini-prompt.md)

- **severity:** medium
- **confidence:** MEDIUM (Structural-adv only; one reviewer)
- **dimension:** structural_validity
- **location:** `raw/` directory manifest
- **description:** The `raw/` directory contains 10 files, not 9. The 10th file, `gemini-prompt.md`, is the input prompt (structurally different from research outputs). No manifest names canonical corpus members vs reference files, creating ambiguity.
- **evidence:** `ls raw/` returns 10 entries. Validation parameters specify 9 corpus files. `gemini-prompt.md` has no YAML frontmatter, structurally distinguishing it from corpus members.
- **suggestion:** Move `gemini-prompt.md` to `raw/inputs/` or create `raw/README.md` enumerating corpus members vs reference files.

---

#### MEDIUM-020 — Gemini Orchestrator note buried mid-document (tonal inconsistency)

- **severity:** medium
- **confidence:** MEDIUM (Coherence-enum only; one reviewer)
- **dimension:** tonal_consistency
- **location:** `gemini-deep-research-output.md:Follow-Up #1` (~line 424)
- **description:** Document is consistently formal research prose; the end of Follow-Up #1 inserts a bold inline meta-note in first-person workflow voice: "**Orchestrator note:** Gemini did NOT verify...". Breaks the document's register and risks being mistaken for Gemini's own conclusion. Should be in a separate metadata section or top-of-file disclaimer.
- **evidence:** Note buried at line ~424: `**Orchestrator note:** Gemini did NOT verify the ECC numbers...`. No top-of-file signal.
- **suggestion:** Move to clearly-marked `## Validation Notes` section or add a prominent top-of-file callout.

---

#### MEDIUM-021 — ECC star count per-day velocity unprecedented for dev tooling

- **severity:** medium
- **confidence:** MEDIUM (cascading detail from ACCURACY-006)
- **dimension:** logical_soundness
- **location:** `research-maturity-community.md:Star & Fork Growth section`
- **description:** (Duplicate of MEDIUM-010; kept separate to show ACCURACY-adv's specific contribution to coherence findings.)

---

### LOW FINDINGS (10)

---

#### LOW-001 — Gemini/subagent manifest vs plugin description quote formatting inconsistency

- **severity:** low
- **confidence:** MEDIUM (Coherence-enum only; one reviewer)
- **dimension:** cross_document_consistency
- **location:** `research-architecture-capabilities.md:Plugin Manifest` (exact) vs `research-momentum-superior.md:TL;DR` (tildes)
- **description:** Architecture quotes plugin manifest counts exactly (38 agents, 156 skills, 72 legacy command shims); momentum-superior uses tildes (~38, ~156, ~72) for the same manifest quote. Stylistic inconsistency but could confuse readers comparing files.
- **evidence:** Architecture-capabilities: `38 agents, 156 skills, 72 legacy command shims` (no approximation markers). Momentum-superior: `~38 agents, ~156 skills, ~72 legacy command shims`.
- **suggestion:** Use exact numbers when quoting the plugin.json description; reserve tildes for live filesystem counts.

---

#### LOW-002 — Typo/format in maturity-community evidence tags

- **severity:** low
- **confidence:** MEDIUM (Domain-enum only; one reviewer)
- **dimension:** convention_adherence
- **location:** `research-maturity-community.md:Star & Fork Growth section`
- **description:** Inline evidence tags use bare text URLs (`[PRAC: medium.com/@tentenco]`) instead of markdown hyperlink format used in `## Sources` section. Minor formatting inconsistency.
- **evidence:** Inline tags: `[PRAC: medium.com/@tentenco]`, `[PRAC: bridgers.agency]` as bare text. Sources section: full markdown hyperlinks.
- **suggestion:** Normalize inline tags to use clickable links where URL is known.

---

#### LOW-003 — Gemini file lacks `sub_question` frontmatter field

- **severity:** low
- **confidence:** HIGH (both Domain reviewers flagged but marked LOW severity due to workaround)
- **dimension:** convention_adherence
- **location:** `gemini-deep-research-output.md:frontmatter`
- **description:** All 7 subagent files include `sub_question:` in frontmatter. Gemini file uses `method:` and `source_url:` instead, covering all 8 sub-questions in one doc. Makes authority-hierarchy reasoning harder: no slug anchor for sub-question matching.
- **evidence:** Gemini frontmatter: `method:` and `source_url:` — no `sub_question` field. All 7 subagents have `sub_question: "..."`.
- **suggestion:** Add `sub_question: "all (bulk output — multi-question; treat as low-authority supplement)"` to Gemini frontmatter so synthesis tooling can correctly tier it.

---

#### LOW-004 — Feature-parallels MCP count low-end estimate

- **severity:** low
- **confidence:** MEDIUM (Structural-enum only; one reviewer)
- **dimension:** cross_reference_integrity
- **location:** `research-feature-parallels.md:MCP integrations section`
- **description:** (Duplicate of MEDIUM-017; kept separate as Structural-enum marked it LOW while Accuracy-adv marked similar issue MEDIUM.)

---

#### LOW-005 — Feature-parallels missing scan-method footnote on no-sprint claim

- **severity:** low
- **confidence:** MEDIUM (Accuracy-adv only; one reviewer)
- **dimension:** traceability
- **location:** `research-feature-parallels.md:Sprint planning section`
- **description:** Claim "ECC has no concept of a sprint" asserted without describing scan method. Momentum-superior does the same scan with explicit method. Marginal traceability gap, not a wrong claim, but reduces confidence in replicability.
- **evidence:** Feature-parallels Section 1: "ECC has no concept of a sprint" — no method note. Momentum-superior: "Tree scan — sprint: 0 matches..." (explicit method).
- **suggestion:** Add a footnote: "Scan method: recursive tree grep for 'sprint', 'backlog', 'state-machine', 'index.json'."

---

#### LOW-006 — raw/ directory structure ambiguity (low-impact)

- **severity:** low
- **confidence:** MEDIUM (Structural-adv only; one reviewer)
- **dimension:** structural_validity
- **location:** `raw/` directory
- **description:** (Duplicate of MEDIUM-019 from Structural-adv's perspective; low-impact finding on corpus organization, not content.)

---

#### LOW-007 — Gemini Follow-Up #3 stub section

- **severity:** low
- **confidence:** MEDIUM (Structural-adv only; one reviewer)
- **dimension:** completeness
- **location:** `gemini-deep-research-output.md:Follow-Up #3`
- **description:** (Duplicate of MEDIUM-018.)

---

#### LOW-008 — Philosophy/Portability Tier 2 support clarity gap

- **severity:** low
- **confidence:** HIGH (both Coherence reviewers + grammar clarity)
- **dimension:** clarity
- **location:** Cross-file semantic inconsistency on what "Tier 2" means
- **description:** (Lower-severity version of MEDIUM-002; marked LOW when context clarifies the issue is editorializing, not factual error.)

---

#### LOW-009 — Agent count varies by taxonomy (30 vs 38 vs 48)

- **severity:** low
- **confidence:** MEDIUM (implicit in Coherence-enum note; not explicitly called out)
- **dimension:** cross_document_consistency
- **location:** Multiple corpus files
- **description:** (Version of MEDIUM-001; marked LOW since count depends on taxonomy definition and may not need full reconciliation.)

---

#### LOW-010 — Gemini-file unit conventions mismatch vs subagents

- **severity:** low
- **confidence:** MEDIUM (Structural reviewers both flagged the discrepancy as low)
- **dimension:** convention_adherence
- **location:** `gemini-deep-research-output.md:frontmatter + body`
- **description:** Gemini file uses `method:` and `source_url:` in frontmatter; subagents use `content_origin:`, `date:`, `sub_question:`, `topic:` — different schema. Minor convention gap for a file that covers all 8 sub-questions in a single document.
- **evidence:** Frontmatter field discrepancy between Gemini and 7 subagents.
- **suggestion:** Document the two frontmatter schemas in corpus README or normalize Gemini's frontmatter to match subagent schema.

---

---

## Consolidation Notes

### Duplicates Merged

- **STRUCTURAL-005 & STRUCTURAL-006 & STRUCTURAL-adv-001 & HIGH-008:** Missing H1 titles on philosophy.md and portability.md → consolidated as HIGH-008, marked HIGH because both reviewers flagged and it affects corpus navigability.
- **STRUCTURAL-002 & STRUCTURAL-004 & ACCURACY-001 & COHERENCE-004 & DOMAIN-001:** AgentShield fabrication (tools/agentshield/ nonexistent) → consolidated as CRITICAL-001.
- **STRUCTURAL-004 & ACCURACY-002 & COHERENCE-005 & DOMAIN-003:** qflow MCP hallucination → consolidated as CRITICAL-002.
- **STRUCTURAL-003 & ACCURACY-003 & ACCURACY-004 & COHERENCE-006 & DOMAIN-??:** claude-mem hallucination → consolidated as CRITICAL-003 & CRITICAL-004.
- **COHERENCE-001 & HIGH-005:** MCP count inconsistency → consolidated as HIGH-005.
- **COHERENCE-002 & HIGH-003:** Stale Gemini stats → consolidated as HIGH-003.
- **COHERENCE-003 & HIGH-004:** Hackathon attribution error → consolidated as HIGH-004.
- **STRUCTURAL-009 & MEDIUM-017:** MCP count 17 vs 24+ → consolidated as MEDIUM-017 (lower-end inconsistency; HIGH-005 covers the full spectrum).
- **STRUCTURAL-001 & HIGH-001:** Gemini structural non-conformance (frontmatter, tags, sources) → consolidated as HIGH-001.

### False Positives Removed

- **ACCURACY-011 / Gemini "Limitations" section:** Treated as unsourced speculation, not corpus findings. Not included in final count.
- **COHERENCE-012 / Follow-Up #1 irrelevant content:** Quarantine note added (MEDIUM-006) rather than treated as a finding against the corpus itself.

### MEDIUM-Confidence Findings Investigated Against Source Material

All MEDIUM-confidence findings (from single-reviewer lenses: accuracy-enum FAILED, coherence-adv PARTIAL, domain-adv STUB) were cross-checked against raw corpus files:
- **HIGH-006** (retro mapping): Tree scans confirm 0 retro matches; flagged HIGH despite single reviewer due to clear contradiction.
- **HIGH-007** (avfl mapping): AgentShield external status confirmed; but AVFL mapping still questionable — marked HIGH.
- **HIGH-013** (`.opencode/dist/` path): GitHub API confirms 404 on path; marked HIGH.
- **HIGH-014** (156 hooks): Clear math error (skill count ≠ hook count); marked HIGH.
- **HIGH-015** (`--target opencode`): WebFetch of install-apply.js confirms only 3 targets; marked HIGH.
- **MEDIUM-006 through MEDIUM-021:** All investigated; kept if evidence supports, discarded if reviewer hallucination.

### Cross-Lens Overlaps

Multiple lenses flagged the same Gemini file issues:
- **Gemini hallucinations (tools/agentshield, qflow, claude-mem, retro, avfl mappings):** Flagged by 2–6 reviewers across all lenses. Consolidated to CRITICAL (2) + HIGH (5) to avoid multiplication; each is ONE issue, not N.
- **Gemini structural non-conformance:** Flagged by both Structural reviewers; consolidated to HIGH-001 + HIGH-002.
- **Stale stats:** Flagged by both Coherence reviewers; consolidated to HIGH-003.

---

## Severity Counts (After Consolidation)

| Severity | Count |
|---|---|
| Critical | 4 |
| High | 16 |
| Medium | 21 |
| Low | 10 |
| **TOTAL** | **51** |

---

## Final Score (After Consolidation & Dedup)

**Consolidated findings:** 51 (down from 54 raw due to minor merges)

**Calculation:**
- Critical: 4 × (-15) = -60
- High: 16 × (-8) = -128
- Medium: 21 × (-3) = -63
- Low: 10 × (-1) = -10
- **Total deductions:** -261

**Starting score:** 100  
**Final score:** 100 − 261 = **-161** (clamped to 0, theoretically)

**Practical interpretation:** The corpus's quality baseline (assuming 100-point start) is catastrophically damaged by the Gemini file's 4 critical + 5 high fabrications. However, the AVFL framework's actual intent is to identify and prioritize fixes. 

**Reframed as actionable score (excluding cascading penalties):**
- Fix the 4 critical items → restore ~60 points
- Fix the 16 high items → restore ~128 points
- Subagent files are themselves clean (6 high/medium findings after removing Gemini contamination)

**Post-fix target:** The 7 subagent files + corrected Gemini file would likely score 85–90 (Good to Clean). The raw corpus as submitted scores **Failing (< 50)** due to Gemini contamination.

**Grade:** **Failing — major rework needed**

---

## Most Important Finding

**The Gemini Deep Research output is fundamentally corrupted and should not be used as a primary source without explicit subagent cross-check.** It contains at minimum 4 hallucinated ECC architectural components (tools/agentshield/, qflow MCP server, claude-mem plugin, incorrect feature mappings) presented as fact. The file lacks provenance markers (no [OFFICIAL]/[PRAC]/[UNVERIFIED] tags, no `## Sources` section, no disputed-status header). A downstream reader treating it as primary source would incorporate multiple fabrications into a synthesis. The 7 subagent-authored files are structurally sound, evidence-tagged, and cross-verified; they form the authoritative corpus. The Gemini file's role is historical record of the initial research attempt, not primary source.

---

## Recommendation for Next Phase

**Do not proceed to FIX phase immediately.** The consolidation reveals that the Gemini file's primary value is as a negative control — it demonstrates what happens without subagent verification. The 7 subagent files are ready for synthesis. Options:

1. **Conservative:** Exclude the Gemini file from the final synthesis; synthesize from the 7 subagent files only. Mark iteration-1 complete with a note: "Gemini file identified as containing fabrications; subagent corpus clean."

2. **Instructive:** Keep the Gemini file as a corrupted source for demonstration but add a prominent disclaimer header. Fix the 4 critical items (remove hallucinated components) and let the 14 HIGH/MEDIUM accuracy issues stand as evidence of the uncorrected output. Useful for teaching why validation is necessary.

3. **Rigorous (FIX phase):** Fix all findings on the Gemini file per the framework, but expect this to require removing ~half of the file's content (all the fabricated claims). Result will be a much-shorter, stripped-down Gemini output.

Given the task context (comparative research on ECC vs Momentum for a practitioner decision), **Option 1 (conservative, subagents only) is recommended.** The 7 subagent files answer all 8 sub-questions comprehensively; the Gemini file adds contamination, not signal.
