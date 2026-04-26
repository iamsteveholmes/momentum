---
validator: coherence-enum
lens: coherence
lens_id: COHERENCE
framing: Enumerator
skepticism: 3
stage: final
corpus_file_count: 9
date: 2026-04-26
---

# AVFL Validation — Coherence & Craft (Enumerator)

**Corpus:** 9 files under `_bmad-output/research/everything-claude-code-vs-momentum-2026-04-26/raw/`
**Lens dimensions:** consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence, cross_document_consistency

---

## Enumerated Check List

The following shared claims were enumerated and verified across all applicable files:

1. ECC GitHub star count
2. ECC fork count
3. ECC contributor count
4. ECC commit count
5. ECC agent count
6. ECC skill count
7. ECC command count
8. Hackathon name/sponsor/date
9. ECC current version
10. ECC creation date
11. MCP integration count
12. Automated test count ("1,282 tests")
13. Terminology: "ECC" used consistently
14. Terminology: AVFL / AGENTS.md capitalization
15. Recommendation summary alignment (integrate / cherry-pick / independent)
16. Date/temporal consistency (today = 2026-04-26)
17. Per-file: internal consistency
18. Per-file: relevance to assigned sub-question
19. Per-file: conciseness
20. Per-file: tonal consistency

---

## Findings

### COHERENCE-001

- **severity:** high
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Structural Layout table` vs `research-architecture-capabilities.md:Summary of Hard Counts` vs `research-feature-parallels.md:Sides at a Glance`
- **description:** Three files give three different MCP integration counts for the same ECC repository, without reconciliation. The Gemini file states 14. The feature-parallels file states ~17. The architecture report gives the most detailed answer: 6 in root `.mcp.json` and 24+ in the catalog file — and explicitly states the Gemini "14" figure is "wrong in both directions."
- **evidence:**
  - `gemini-deep-research-output.md` directory table: `"mcp-configs/ | Pre-built Model Context Protocol (MCP) server configurations for 14 external integrations."`
  - `research-architecture-capabilities.md:MCP Configurations`: `"So the '14 MCP integrations' Gemini number is wrong in both directions: the actually-shipped .mcp.json is 6 servers, but the reference catalog at mcp-configs/mcp-servers.json is much larger than 14 (24+)."`
  - `research-feature-parallels.md:Sides at a Glance table`: `"mcp-configs/mcp-servers.json declaring ~17 MCP servers (jira, github, firecrawl, supabase, memory, omega-memory, sequential-thinking, vercel, railway, cloudflare-docs…)"`
- **suggestion:** Settle on the architecture report's verified figure: 6 in root `.mcp.json`; 24+ in the catalog. Retire the "14" and "~17" figures or note explicitly that they are unverified reading of different files.

---

### COHERENCE-002

- **severity:** high
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Technical Architecture / Maturity table` vs `research-architecture-capabilities.md:Repo Overview` vs `research-maturity-community.md:TL;DR`
- **description:** The Gemini file presents stale community stats as current fact — 140,000+ stars, 21,000+ forks, 113 contributors, 768 commits. Both subagent reports independently verified the live GitHub API values as 167,487–167,488 stars, 25,969 forks, 159 contributors, ~1,465 commits, and explicitly label the lower numbers as stale README badge copy.
- **evidence:**
  - `gemini-deep-research-output.md`: `"reaching over 140,000 GitHub stars and 21,000 forks"` and maturity table: `"Stars | 140,000+"`, `"Contributors | 113"`, and narrative: `"113 contributors and over 768 commits"`
  - `research-architecture-capabilities.md:Repo Overview`: `"Stars / forks / watchers / issues: 167,488 / 25,969 / 864 / 166 [OFFICIAL]"`
  - `research-maturity-community.md:TL;DR table`: `"Stars | 140,000+ | 167,487 | Higher than claimed"`, `"Contributors | 113 | 159 | Higher than claimed"`, `"Total commits | 768 | 1,465 | Roughly 2x higher than claimed"`
- **suggestion:** Use only API-verified figures (167K stars, 26K forks, 159 contributors, ~1,465 commits) in the synthesis. Note that Gemini reproduced the repository's own stale README badge, not live state.

---

### COHERENCE-003

- **severity:** high
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Maturity and Community Traction Analysis` vs `research-maturity-community.md:Section 9 Hackathon`
- **description:** Hackathon attribution disagrees on both sponsor and date. Gemini says "Anthropic x Forum Ventures hackathon in late 2025." The maturity subagent verified it was "Cerebral Valley × Anthropic 'Built with Opus 4.6' hackathon, Feb 10–16, 2026." The architecture report independently flagged the Forum Ventures / late 2025 attribution as UNVERIFIED.
- **evidence:**
  - `gemini-deep-research-output.md`: `"a winner of the Anthropic x Forum Ventures hackathon in late 2025"`
  - `research-maturity-community.md:Section 9`: `"actual event was Cerebral Valley × Anthropic 'Built with Opus 4.6' hackathon, Feb 10-16, 2026. ECC was a winner."` and `"Forum Ventures was not the partner — Cerebral Valley was. [OFFICIAL]"`
  - `research-architecture-capabilities.md:Verification table`: `"UNVERIFIED (no primary source for 'Forum Ventures' or 'late 2025')"`
- **suggestion:** Use the maturity report's verified attribution in the synthesis. Flag the Gemini attribution as incorrect.

---

### COHERENCE-004

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Structural Layout table` vs `research-ecc-superior.md:What Was Verified Live` vs `research-integration-assessment.md:Sources`
- **description:** The Gemini structural table includes a row for `tools/agentshield/` described as "Proprietary security scanning engine with over 1,282 automated tests." The ecc-superior subagent cloned the live repo and found no such directory — AgentShield is a separate external repo (`affaan-m/agentshield`), not a subdirectory of ECC. The integration-assessment report confirms the same.
- **evidence:**
  - `gemini-deep-research-output.md` table: `"tools/agentshield/ | Proprietary security scanning engine with over 1,282 automated tests. | TypeScript, Python"`
  - `research-ecc-superior.md:What Was Verified Live`: `"AgentShield is NOT part of ECC — it is a sibling project. The '1,282 tests in AgentShield' claim from the prior report cannot be verified from inside ECC. [UNVERIFIED]"`
  - `research-integration-assessment.md:Sources`: `"AgentShield reference (sibling project): affaan-m/agentshield cited in … exists as separate repo, not part of ECC [OFFICIAL for the reference; UNVERIFIED for '1,282 tests' claim]"`
- **suggestion:** Discard the `tools/agentshield/` directory entry from the structural analysis entirely. Any reference to "1,282 tests" should be attributed to an unverified external repo claim, not to ECC's own test suite.

---

### COHERENCE-005

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Workflow and State Management table` vs `research-momentum-superior.md:Section 3`
- **description:** The Gemini comparison table maps Momentum's `create-story` to a "`qflow` MCP server" in ECC ("7-state machine and dependency DAG for task management") and maps Momentum's `index.json` state machine to ECC's "SQLite state store." Neither claim is supported by the subagent corpus. The momentum-superior report ran a full 2,662-path tree scan and returned zero matches for `sprint`, `backlog`, `epic`, `state-machine`, `index.json`. The ECC SQLite store (verified by ecc-superior) is an install-state database, not a task/sprint tracker. No `qflow` MCP server appears in any subagent report.
- **evidence:**
  - `gemini-deep-research-output.md:Workflow table`: `"create-story command | qflow MCP server | 7-state machine and dependency DAG"` and `"index.json state machine | SQLite state store | Persistent local database for session and task tracking"`
  - `research-momentum-superior.md:Section 3`: `"ECC [OFFICIAL]: Tree scan — sprint: 0 matches, backlog: 0 matches, epic: 0 matches, state-machine: 0 matches, index.json: 0 matches, sole-writer: 0 matches."`
  - `research-ecc-superior.md:Section 1`: ECC's SQLite store (`~/.claude/ecc/state.db`) covers `"sessions, skill runs, skill versions, decisions, install state, and governance events"` — not story/sprint state
- **suggestion:** Remove `qflow` attribution from the synthesis. ECC's SQLite state store is an install-state tracker. The Gemini equivalences in the workflow table are hallucinated.

---

### COHERENCE-006

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `gemini-deep-research-output.md:Memory and Persistence Systems`
- **description:** The Gemini file introduces `claude-mem` as "a plugin that reached 89,000 stars in early 2026" with "a background HTTP API managed by Bun" and "Chroma vector support for semantic search." This product is entirely absent from all eight subagent reports. The architecture report exhaustively enumerated 2,662 ECC path entries and found no `claude-mem` component. The ecc-superior and feature-parallels reports both describe ECC's memory system without mentioning `claude-mem`.
- **evidence:**
  - `gemini-deep-research-output.md:Memory and Persistence`: `"ECC has evolved this into claude-mem, a plugin that reached 89,000 stars in early 2026. Unlike Momentum's flat files, claude-mem uses a background HTTP API managed by Bun and stores data in a SQLite database with Chroma vector support for semantic search."`
  - `research-architecture-capabilities.md`: no `claude-mem` in the 2,662-entry tree scan
  - `research-ecc-superior.md:Section 13 Memory`: lists ECC memory as MCP `memory` server, `omega-memory`, `continuous-learning-v2`; no `claude-mem`
  - `research-feature-parallels.md:Section 6 Memory`: lists `continuous-learning-v2`, MCP `memory`, MCP `omega-memory`; no `claude-mem`
- **suggestion:** Exclude `claude-mem` from the synthesis as a Gemini hallucination. Use the subagent-verified memory components only.

---

### COHERENCE-007

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `research-feature-parallels.md:Sides at a Glance` vs `research-ecc-superior.md:Section 16` vs `research-momentum-superior.md:TL;DR`
- **description:** Momentum's skill count is reported as 26 in feature-parallels and momentum-superior (both from `ls`), but as 25 in ecc-superior. The discrepancy is one skill and likely reflects a different snapshot time (the git status shows new story files were created between reports). Minor but a synthesis reader may notice.
- **evidence:**
  - `research-feature-parallels.md:Sides at a Glance`: `"Skill count | 26 skills [OFFICIAL]"`
  - `research-momentum-superior.md:TL;DR`: `"Skill count from ls skills/momentum/skills/: 26 skills"`
  - `research-ecc-superior.md:Section 16`: `"vs Momentum's 25 skills, 7 dev agents (in agents/), and 16 commands"`
- **suggestion:** Use 26 (the value two reports agree on from direct `ls`). Note in the synthesis that counts reflect the repository state at 2026-04-26.

---

### COHERENCE-008

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `research-feature-parallels.md:Sides at a Glance` vs `research-ecc-superior.md:Section 16`
- **description:** Momentum's command count is reported as 15 in feature-parallels and 16 in ecc-superior. Same repository, same date, different count.
- **evidence:**
  - `research-feature-parallels.md:Sides at a Glance table`: `"Command count | 15 slash commands in commands/ [OFFICIAL]"`
  - `research-ecc-superior.md:Section 16`: `"vs Momentum's 25 skills, 7 dev agents (in agents/), and 16 commands"`
- **suggestion:** Minor. Verify and use a single consistent number. The synthesis should not present both.

---

### COHERENCE-009

- **severity:** medium
- **dimension:** cross_document_consistency
- **location:** `research-philosophy.md:Section 9 Distribution` vs `research-portability.md:Comparison table`
- **description:** The philosophy report describes Momentum as having a "Tier 2: Cursor and other tools — advisory" mode, implying hooks exist but fire non-blocking. The portability report documents that Momentum's hooks use `$CLAUDE_*` env vars that are Claude Code-specific and would not fire at all under Cursor. "Advisory (fires but doesn't block)" and "does not fire" are materially different claims.
- **evidence:**
  - `research-philosophy.md:Section 9`: `"Tier 2: Cursor and other tools — advisory — 'Hooks (no automatic linting, formatting, or file protection); Global rules (no ~/.claude/rules/ auto-loading)'"`
  - `research-portability.md`: `"hooks.json uses Claude Code-specific event names (PreToolUse, PostToolUse, Stop) and the $CLAUDE_PROJECT_DIR and $CLAUDE_TOOL_INPUT_FILE_PATH environment variables. These are CC-only event names; they would not fire under Codex, OpenCode, or Cursor as written. [OFFICIAL]"`
  - `research-portability.md:Comparison table`: `"Hook portability | CC-only, $CLAUDE_* env vars | None"`
- **suggestion:** The synthesis should clarify: Tier 2 means the practice *documentation* (rules, references, skill prose) is usable by a Cursor developer, but the automated tooling (hooks, gates) simply will not fire. Not "advisory" — absent.

---

### COHERENCE-010

- **severity:** low
- **dimension:** cross_document_consistency
- **location:** `research-architecture-capabilities.md:Plugin Manifest` vs `research-momentum-superior.md:TL;DR`
- **description:** The architecture report quotes the plugin manifest counts exactly (38 agents, 156 skills, 72 legacy command shims). Momentum-superior approximates with tildes (~38, ~156, ~72) when quoting the same manifest. Stylistic inconsistency but could confuse a reader comparing files.
- **evidence:**
  - `research-architecture-capabilities.md:Plugin Manifest`: `"38 agents, 156 skills, 72 legacy command shims"` (no approximation markers)
  - `research-momentum-superior.md:TL;DR`: `"~38 agents, ~156 skills, ~72 legacy command shims (per README.md 'What's New v1.10.0')"`
- **suggestion:** When quoting the plugin.json description, use exact numbers. Reserve tildes for live filesystem counts.

---

### COHERENCE-011

- **severity:** low
- **dimension:** tonal_consistency
- **location:** `gemini-deep-research-output.md` — end of Follow-Up #1 section
- **description:** The document is consistently formal research prose, but the end of the Follow-Up #1 response inserts a bold inline orchestrator meta-note in first-person workflow voice: "**Orchestrator note:** Gemini did NOT verify the ECC numbers in this follow-up…" This is a process annotation to a workflow system, not research content. Breaks the document's register and risks being mistaken for Gemini's own conclusion.
- **evidence:** `gemini-deep-research-output.md:Follow-Up #1`: `"**Orchestrator note:** Gemini did NOT verify the ECC numbers in this follow-up. Instead it provided verifications for unrelated tools (ForgeCode, OpenCode, Bifrost) and AI model releases. This strongly suggests the original ECC numbers may be hallucinated."`
- **suggestion:** Move to a clearly-marked metadata section (e.g., `## Validation Notes`) or prefix with a horizontal rule and header to make clear it is a process annotation, not a research finding.

---

### COHERENCE-012

- **severity:** low
- **dimension:** relevance
- **location:** `gemini-deep-research-output.md:Follow-Up #1 Response`
- **description:** Follow-Up #1 asks Gemini to verify the ECC numeric claims. The response provides URLs for ForgeCode TermBench scores, OpenCode providers, and Bifrost gateway latency — entirely out of scope. This off-topic content is included verbatim in the corpus document.
- **evidence:** `gemini-deep-research-output.md:Follow-Up #1 Response`: cites `forgecode.dev`, `github.com/tailcallhq/forgecode`, `github.com/sst/opencode`, `github.com/mark-hingston/opencode-workflows`, `github.com/maximhq/bifrost` — none relevant to ECC stat verification.
- **suggestion:** The irrelevant ForgeCode/OpenCode/Bifrost citations should be clearly quarantined or excluded in the synthesis. They represent Gemini answering a different question and should not be treated as ECC research evidence.

---

### COHERENCE-013

- **severity:** low
- **dimension:** clarity
- **location:** `research-portability.md:Section on Goose, Aider, Cline, ForgeCode` vs `gemini-deep-research-output.md:Portability table`
- **description:** The portability report flatly states Goose, Aider, Cline, and ForgeCode are not supported by ECC (no adapters, no directories). The Gemini table grades Aider and Goose as "Theoretical / Via Standard." A synthesis reader seeing both may read "Theoretical / Via Standard" as a meaningful support tier, when the actual state is no dedicated investment — only the general property that any tool can read markdown.
- **evidence:**
  - `research-portability.md:Section on Goose/Aider/Cline/ForgeCode`: `"Not supported by ECC. The repository contains no .goose, .aider, .cline, or .forgecode directories, no skills referencing those harnesses, and no installer adapters for them. [OFFICIAL]"`
  - `gemini-deep-research-output.md:Portability table`: `"Aider / Goose | Portable AGENTS.md and SKILL.md definitions. | Theoretical / Via Standard"`
- **suggestion:** The synthesis should adopt the portability subagent's framing. "Theoretical" support via AGENTS.md is a property of the standard, not ECC-specific work.

---

## Score Calculation

Starting score: 100

| Finding ID | Severity | Points |
|---|---|---|
| COHERENCE-001 | high | -8 |
| COHERENCE-002 | high | -8 |
| COHERENCE-003 | high | -8 |
| COHERENCE-004 | medium | -3 |
| COHERENCE-005 | medium | -3 |
| COHERENCE-006 | medium | -3 |
| COHERENCE-007 | medium | -3 |
| COHERENCE-008 | medium | -3 |
| COHERENCE-009 | medium | -3 |
| COHERENCE-010 | low | -1 |
| COHERENCE-011 | low | -1 |
| COHERENCE-012 | low | -1 |
| COHERENCE-013 | low | -1 |

**Total deductions:** -46
**Score:** 54/100
**Grade:** Poor — significant problems
**Pass threshold:** 95
**Result:** FAIL — proceed to fix phase

---

## Summary

14 findings. The corpus's quality issues are concentrated in a single file: `gemini-deep-research-output.md` is the source of all three high-severity findings and three of the six medium-severity findings. Its community stats are stale (README badge vs live API), its hackathon attribution is wrong on both sponsor and date, it contains a fabricated directory entry (`tools/agentshield/`), it references a hallucinated companion product (`claude-mem`, 89k stars), it attributes a non-existent `qflow` MCP server to ECC, and its MCP count (14) is contradicted by the architecture report's verified figure (6/24+). The eight subagent-authored files are internally consistent, on-topic, and tonally appropriate throughout; minor inconsistencies in Momentum component counts (26 vs 25 skills, 15 vs 16 commands) and the philosophy/portability tension on what "Tier 2 support" means round out the medium-severity findings.
