---
validator: AVFL Enumerator — Structural Integrity lens
lens: STRUCTURAL
framing: Enumerator
skepticism: 3 (aggressive)
stage: final
corpus: true
corpus_file_count: 9
date: 2026-04-26
---

# Structural Integrity Findings — Iteration 1

Systematic enumeration across all 9 corpus files. Every structural requirement was checked per file: frontmatter fields, H1 title presence, section structure, evidence tag usage, Sources section, cross-reference integrity (file paths and URLs), and corpus-level completeness against the 8 sub-questions in scope.md.

---

## Findings

---

### STRUCTURAL-001

- **id:** STRUCTURAL-001
- **severity:** high
- **dimension:** structural_validity
- **location:** `gemini-deep-research-output.md:Frontmatter`
- **description:** The Gemini file's frontmatter is missing the `sub_question` field present on all 8 subagent files, has zero evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]) anywhere in the body, and has no `## Sources` section. For a final-stage research corpus where every subagent file consistently uses all three structural conventions, the absence of these elements in the Gemini file makes it structurally non-conformant with the corpus standard.
- **evidence:** Frontmatter contains only `content_origin`, `date`, `topic`, `method`, `source_url` — no `sub_question`. `grep -c "\[OFFICIAL\]\|\[PRAC\]\|\[UNVERIFIED\]"` returns 0 for this file (vs. 27–88 in each subagent file). No `## Sources` heading found. All 8 subagent files have `## Sources` sections.
- **suggestion:** Add a `sub_question: "Baseline comparative analysis — all 8 sub-questions"` (or similar) to frontmatter. Add a `## Sources` section listing the Gemini Deep Research session URL (`https://gemini.google.com/app/86668a7bd7fdd717`). Apply [OFFICIAL]/[PRAC]/[UNVERIFIED] tags to factual claims, or add a header note indicating this is unverified raw Gemini output requiring cross-check against subagent findings.

---

### STRUCTURAL-002

- **id:** STRUCTURAL-002
- **severity:** high
- **dimension:** cross_reference_integrity
- **location:** `gemini-deep-research-output.md:Technical Architecture and Repository Composition`
- **description:** The directory table lists `tools/agentshield/` as an ECC repository path with contents "Proprietary security scanning engine with over 1,282 automated tests." This path does not exist in the ECC repository. The architecture-capabilities subagent verified the full 2,662-entry recursive git tree and found AgentShield is a separate sibling npm package (`ecc-agentshield`), not a subdirectory inside the repo. The integration-assessment subagent also explicitly flags this.
- **evidence:** `gemini-deep-research-output.md` table row: `| \`tools/agentshield/\` | Proprietary security scanning engine with over 1,282 automated tests. | TypeScript, Python |`. Contradicted by `research-architecture-capabilities.md:Repo Overview`: "The repo also publishes a sibling npm package `ecc-agentshield`, referenced by README badges." And `research-integration-assessment.md:What Was Verified Live`: "the security-scan skill calls `npx ecc-agentshield`, which is an **external** package (`github.com/affaan-m/agentshield`). AgentShield is **not** part of ECC — it is a sibling project."
- **suggestion:** Remove the `tools/agentshield/` table row. Replace with: AgentShield is a separate npm package invoked by ECC's `skills/security-scan/SKILL.md` via `npx ecc-agentshield`, not an in-repo directory. The 1,282-test claim should be tagged [UNVERIFIED] and attributed to the external AgentShield repository.

---

### STRUCTURAL-003

- **id:** STRUCTURAL-003
- **severity:** high
- **dimension:** cross_reference_integrity
- **location:** `gemini-deep-research-output.md:Direct Feature Parallels with Momentum`
- **description:** The file claims ECC uses `claude-mem`, described as "a plugin that reached 89,000 stars in early 2026" with "a background HTTP API managed by Bun" and "SQLite database with Chroma vector support for semantic search." No entity named `claude-mem` exists in the ECC repository. The architecture-capabilities subagent catalogued all 2,662 tree entries. ECC's actual memory system is `continuous-learning-v2` with instincts in `~/.claude/homunculus/`, not a Bun/SQLite/Chroma HTTP API.
- **evidence:** `gemini-deep-research-output.md:Memory and Persistence Systems`: "ECC has evolved this into `claude-mem`, a plugin that reached 89,000 stars in early 2026. Unlike Momentum's flat files, `claude-mem` uses a background HTTP API managed by Bun and stores data in a SQLite database with Chroma vector support." Contradicted by `research-momentum-superior.md:Persistent Multi-Conversation Memory`: "ECC's `continuous-learning-v2` is a more sophisticated **automated** memory system." No `claude-mem` reference appears in any of the 8 subagent files. The Gemini Integration Assessment recommendation to "Adopt the `claude-mem` Architecture" is downstream of this fabrication.
- **suggestion:** Replace `claude-mem` with accurate description of ECC's actual memory system: `continuous-learning-v2` (instinct-based, hook-driven, confidence-scored, stored in `~/.claude/homunculus/`). The Adopt-with-modification recommendation for `claude-mem` should be removed or corrected.

---

### STRUCTURAL-004

- **id:** STRUCTURAL-004
- **severity:** high
- **dimension:** cross_reference_integrity
- **location:** `gemini-deep-research-output.md:Direct Feature Parallels with Momentum`
- **description:** The file states ECC uses a `qflow` MCP server as its equivalent for Momentum's sprint state machine and `create-story` command. No `qflow` MCP server appears anywhere in the ECC repository. The architecture-capabilities file enumerates all verified MCP servers (6 in root `.mcp.json`, 24+ in `mcp-configs/mcp-servers.json`) and `qflow` is not among them. All subagents confirm ECC has no sprint/story state management.
- **evidence:** `gemini-deep-research-output.md:Workflow and State Management`: "ECC approaches this through a combination of specialized agents and the `qflow` MCP server." Also: "In ECC, task management is often delegated to an external MCP like `qflow`." Contradicted by `research-momentum-superior.md:Sprint State Machine`: "Tree scan — `sprint: 0 matches`, `backlog: 0 matches`, `epic: 0 matches`, `state-machine: 0 matches`, `index.json: 0 matches`." And `research-architecture-capabilities.md:MCP Configurations`: lists all verified MCP servers with no `qflow` present.
- **suggestion:** Remove `qflow` references. The correct finding (established by all 8 subagents) is that ECC has no equivalent to Momentum's sprint state machine — this is a gap. The Gemini table row mapping `create-story` to "`qflow` MCP server" should be corrected to "No direct analogue."

---

### STRUCTURAL-005

- **id:** STRUCTURAL-005
- **severity:** medium
- **dimension:** structural_validity
- **location:** `research-portability.md:Document structure`
- **description:** The file begins directly with `## Inline Summary` with no H1 document title. All other 7 subagent files and the Gemini file have an H1 title immediately after frontmatter. Missing title makes the file structurally non-conformant with the corpus convention and removes the navigational anchor for readers.
- **evidence:** Lines 8–10 after frontmatter close: `## Inline Summary\n\nECC is **genuinely cross-tool...`. No `# ` heading precedes it. Compare `research-feature-parallels.md` line 8: `# Feature Parallels — \`everything-claude-code\` (ECC) vs Momentum`.
- **suggestion:** Add `# Portability — ECC Across Agentic CLIs` (or similar) before the `## Inline Summary` section.

---

### STRUCTURAL-006

- **id:** STRUCTURAL-006
- **severity:** medium
- **dimension:** structural_validity
- **location:** `research-philosophy.md:Document structure`
- **description:** Same issue as STRUCTURAL-005: the file begins directly with `## Inline Summary` with no H1 title. The file contains 14 numbered sections plus a Synthesis table — a substantial document lacking the identifying header present on all other corpus files.
- **evidence:** Lines 8–10 after frontmatter close: `## Inline Summary\n\nEverything Claude Code (ECC) is a **toolkit-and-distribution platform**...`. No `# ` heading appears before this. The `sub_question` frontmatter field contains `"Design philosophy comparison — ECC vs Momentum"` but does not substitute for a document H1.
- **suggestion:** Add `# Design Philosophy Comparison — ECC vs Momentum` before `## Inline Summary`.

---

### STRUCTURAL-007

- **id:** STRUCTURAL-007
- **severity:** medium
- **dimension:** cross_reference_integrity
- **location:** `research-ecc-superior.md:Throughout body and Sources`
- **description:** The file contains 115 references to `/tmp/ecc-research/` paths (e.g., `/tmp/ecc-research/manifests/install-profiles.json`, `/tmp/ecc-research/scripts/lib/state-store/index.js`) throughout body text and the Sources section. These are ephemeral local clone paths that are unresolvable by any downstream reader. The architecture-capabilities subagent, covering overlapping content, used stable GitHub URLs exclusively.
- **evidence:** Sources section header: "All paths absolute, captured from local clone at `/tmp/ecc-research/` on 2026-04-26." Body example: "Verified in `/tmp/ecc-research/scripts/lib/install/`, `/tmp/ecc-research/manifests/install-profiles.json`, `/tmp/ecc-research/scripts/lib/state-store/index.js`". `grep -c "/tmp/ecc-research"` returns 115. Compare `research-architecture-capabilities.md` which uses `https://github.com/affaan-m/everything-claude-code/blob/main/...` throughout.
- **suggestion:** Replace `/tmp/ecc-research/<path>` citations with canonical GitHub URL equivalents: `https://github.com/affaan-m/everything-claude-code/blob/main/<path>`. The local clone methodology is fine; the persistent citations should use GitHub URLs.

---

### STRUCTURAL-008

- **id:** STRUCTURAL-008
- **severity:** medium
- **dimension:** cross_reference_integrity
- **location:** `research-integration-assessment.md:Inline Summary`
- **description:** The inline summary characterizes ECC as "38 agents, 156 skills, **156 hooks-config knobs**, 79 commands." The figure "156 hooks-config knobs" is internally inconsistent: 156 is ECC's reported skill count, not a hook metric. Verified hook figures across the corpus are ~40 hook scripts (`scripts/hooks/`) or ~14 distinct hook IDs in `hooks/hooks.json`. No corpus source produces a hook-related count of 156.
- **evidence:** `research-integration-assessment.md:Inline Summary`: "ECC is a horizontally-scoped toolkit (38 agents, 156 skills, **156 hooks-config knobs**, 79 commands)." Contradicted by `research-architecture-capabilities.md:Hooks`: "scripts/hooks/ — 40 hook implementation files" and `research-feature-parallels.md:Hooks-driven enforcement`: "hook framework with at least 14 distinct hook IDs."
- **suggestion:** Correct "156 hooks-config knobs" to an accurate hook metric (e.g., "~40 hook scripts" or "14 hook IDs") or remove the hook count from this summary list since it duplicates the skill count by error.

---

### STRUCTURAL-009

- **id:** STRUCTURAL-009
- **severity:** low
- **dimension:** cross_reference_integrity
- **location:** `research-feature-parallels.md:Sides at a Glance` vs `research-architecture-capabilities.md:MCP Configurations`
- **description:** `research-feature-parallels.md` states ECC's `mcp-configs/mcp-servers.json` declares "~17 MCP servers." `research-architecture-capabilities.md` reports "at least 24" MCP integrations in that same file. Both cite `mcp-configs/mcp-servers.json [OFFICIAL]`. The architecture-capabilities file notes the file was "truncated at ~5 KB read," indicating ~17 is a lower bound from a partial read while 24+ reflects a more complete count.
- **evidence:** `research-feature-parallels.md:MCP configs`: "Single `mcp-configs/mcp-servers.json` declaring ~17 MCP servers." `research-architecture-capabilities.md:MCP Configurations`: "a 'kitchen-sink' reference catalog (truncated at ~5 KB read) listing **at least 24** MCP integrations" and summary table: "MCP servers (catalog): **24+**."
- **suggestion:** Update `research-feature-parallels.md` MCP catalog count from "~17" to "24+" (or "17+ at partial read; 24+ per full enumeration") to align with the architecture-capabilities verified count.

---

### STRUCTURAL-010

- **id:** STRUCTURAL-010
- **severity:** low
- **dimension:** cross_reference_integrity
- **location:** `research-feature-parallels.md:Sides at a Glance` and `research-momentum-superior.md:Method and Evidence Discipline`
- **description:** `research-feature-parallels.md` reports Momentum has "26 skills" and "15 slash commands." `research-ecc-superior.md` reports "25 skills" and "16 commands." The actual local directory counts are 25 skills and 16 commands (verified against `/Users/steve/projects/momentum/skills/momentum/skills/` and `/Users/steve/projects/momentum/skills/momentum/commands/`). `research-momentum-superior.md` also says "26 skills." The feature-parallels and momentum-superior files are off by 1 on both metrics.
- **evidence:** `research-feature-parallels.md:Sides at a Glance`: "Skill count: 26 skills [OFFICIAL]" and "Command count: 15 slash commands in `commands/` [OFFICIAL]." `research-ecc-superior.md:Other Notables`: "Momentum's 25 skills, 7 dev agents (in `agents/`), and 16 commands. [OFFICIAL — counts derived from `ls | wc -l` against actual directories]." Local `ls -la skills/momentum/skills/` shows 25 skill directories (27 entries minus `.` and `..`). Local `ls skills/momentum/commands/` shows 16 files.
- **suggestion:** Update `research-feature-parallels.md` and `research-momentum-superior.md` to use "25 skills" and "16 commands" — the filesystem-verified counts established by `research-ecc-superior.md`.

---

## Corpus Completeness Assessment

**dimension:** corpus_completeness  
**result:** CLEAN

All 8 sub-questions in `scope.md` are addressed by at least one dedicated file:

| Sub-question | Covered by |
|---|---|
| 1. Architecture & capabilities | `research-architecture-capabilities.md` |
| 2. Maturity & community signals | `research-maturity-community.md` |
| 3. Direct feature parallels | `research-feature-parallels.md` |
| 4. ECC superior / features Momentum lacks | `research-ecc-superior.md` |
| 5. Momentum superior | `research-momentum-superior.md` |
| 6. Portability across agentic CLIs | `research-portability.md` |
| 7. Philosophy comparison | `research-philosophy.md` |
| 8. Integration assessment | `research-integration-assessment.md` |

No required sub-question is absent from the corpus.

---

## Score Calculation

Starting score: 100

| Finding | Severity | Points |
|---|---|---|
| STRUCTURAL-001 | high | -8 |
| STRUCTURAL-002 | high | -8 |
| STRUCTURAL-003 | high | -8 |
| STRUCTURAL-004 | high | -8 |
| STRUCTURAL-005 | medium | -3 |
| STRUCTURAL-006 | medium | -3 |
| STRUCTURAL-007 | medium | -3 |
| STRUCTURAL-008 | medium | -3 |
| STRUCTURAL-009 | low | -1 |
| STRUCTURAL-010 | low | -1 |

**Score: 100 - 46 = 54 / 100 — Poor (significant problems)**

**Grade breakdown:** 4 high (all in `gemini-deep-research-output.md`), 4 medium (2 structural in subagent files, 1 ephemeral paths, 1 metric error), 2 low (cross-document count inconsistencies).

**Note on distribution:** 8 of 10 findings affect `gemini-deep-research-output.md` or `research-ecc-superior.md`. The 6 other subagent files are structurally sound: correct frontmatter, consistent evidence tags, Sources sections, and internally valid cross-references. The score is pulled down by the Gemini file's four fabricated entity references and structural non-conformance.
