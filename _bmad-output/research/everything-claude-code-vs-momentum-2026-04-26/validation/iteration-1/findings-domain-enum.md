---
validator: avfl-domain-enum
lens: domain
framing: enumerator
skepticism: 3
stage: final
date: 2026-04-26
corpus_file_count: 9
---

# AVFL Domain Fitness Findings — Enumerator
## Corpus: everything-claude-code vs Momentum comparative research

### Enumeration Approach

Domain expectations derived from the Enumerator framing: systematically enumerate every domain rule and convention that applies to this corpus type (comparative tech research, agentic-engineering domain, Momentum research conventions), then verify each in order against each file.

**Checks enumerated:**

1. Frontmatter discipline — each subagent file has required fields (`content_origin`, `date`, `sub_question`, `topic`); Gemini file has its own provenance fields.
2. Evidence tag application — `[OFFICIAL]`, `[PRAC]`, `[UNVERIFIED]` applied per claim; untagged factual claims flagged.
3. Source citation — URLs present and properly formatted; `## Sources` section at end of each file.
4. Sub-question coverage — each file answers the assigned sub-question from `scope.md` without drift.
5. Comparative research convention — equal scrutiny applied to both sides.
6. Agentic-CLI domain accuracy — terminology (MCP, hooks, skills, agents, AVFL, AGENTS.md, plugin marketplace) used correctly; no technical errors.
7. Decision fitness — corpus gives Steve enough to decide adopt/cherry-pick/independent with concrete file paths and effort estimates.
8. Honesty about uncertainty — file-verified facts distinguished from inference; no false confidence.
9. Authority hierarchy alignment — Gemini output appropriately downgraded; subagents not repeating Gemini's uncorrected claims.

---

## Findings

---

### DOMAIN-001

- **id:** DOMAIN-001
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Technical Architecture and Repository Composition`
- **description:** Gemini's output presents a `tools/agentshield/` directory entry in its table of ECC's structure, claiming AgentShield is a component inside ECC with "over 1,282 automated tests" under `TypeScript, Python`. This is factually wrong. All three subagent reports that inspected ECC's file tree confirm AgentShield is a separate sibling repository (`affaan-m/agentshield`), not a directory inside ECC. The claim that it ships at `tools/agentshield/` with TypeScript+Python tests is a fabrication.
- **evidence:** `gemini-deep-research-output.md` table row: `tools/agentshield/ | Proprietary security scanning engine with over 1,282 automated tests. | TypeScript, Python`. Against: `research-integration-assessment.md:What Was Verified Live`: "the-security-guide.md references `affaan-m/agentshield` as a **separate** repository. AgentShield is **not** part of ECC — it is a sibling project. The '1,282 tests in AgentShield' claim from the prior report cannot be verified from inside ECC. [UNVERIFIED]"
- **suggestion:** Synthesis must not reproduce the `tools/agentshield/` path or the 1,282-tests claim as ECC-internal facts. Add a strong authority-downgrade header to `gemini-deep-research-output.md` and mark all untagged claims `[UNVERIFIED]`.

---

### DOMAIN-002

- **id:** DOMAIN-002
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Maturity and Community Traction Analysis`
- **description:** Gemini attributes the hackathon win to "Anthropic x Forum Ventures hackathon in late 2025." Both verification subagents establish the actual event was the Cerebral Valley × Anthropic "Built with Opus 4.6" hackathon, Feb 10–16, 2026 — wrong sponsor (Cerebral Valley not Forum Ventures) and wrong date (early 2026 not late 2025). The Gemini file contains the uncorrected error and would corrupt any synthesis that quotes it.
- **evidence:** `gemini-deep-research-output.md`: "Since its inception as a winner of the Anthropic x Forum Ventures hackathon in late 2025..." Versus `research-maturity-community.md:Hackathon`: "ECC was a winner at **Cerebral Valley × Anthropic 'Built with Opus 4.6' hackathon**, Feb 10-16, 2026. [PRAC: cerebralvalley.ai/e/claude-code-hackathon]" and "`Forum Ventures was not the partner` — Cerebral Valley was. [OFFICIAL]"
- **suggestion:** Gemini file needs a provenance downgrade note. Any synthesis citing hackathon facts must use `research-maturity-community.md` as authoritative.

---

### DOMAIN-003

- **id:** DOMAIN-003
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Workflow and State Management feature comparison table`
- **description:** Gemini invents an ECC component called "qflow MCP server" with a "7-state machine and dependency DAG for task management" as the analogue to Momentum's `create-story` command. No subagent — including the architecture subagent that scanned all 2,662 ECC tree entries — found any `qflow` reference in the ECC repository. This is a hallucinated ECC component presented as a concrete architectural mapping.
- **evidence:** `gemini-deep-research-output.md` table: `create-story command | qflow MCP server | 7-state machine and dependency DAG for task management`. Against: `research-momentum-superior.md:Sprint State Machine`: "ECC [OFFICIAL]: Tree scan — `sprint: 0 matches`, `backlog: 0 matches`, `epic: 0 matches`, `state-machine: 0 matches`, `index.json: 0 matches`." The architecture subagent's complete MCP catalog lists 6 root `.mcp.json` servers and ~24 catalog entries — no `qflow` appears in either.
- **suggestion:** Synthesis must exclude the `qflow` entry and use `research-feature-parallels.md` as authoritative for ECC–Momentum feature mapping.

---

### DOMAIN-004

- **id:** DOMAIN-004
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Workflow and State Management feature comparison table`
- **description:** Gemini maps Momentum's `retro` skill to ECC's "`Stop` hook pattern — Auto-summarization of successes/failures at session end." This is technically incorrect. The ECC `Stop` hook (session-end.js) captures session state — it does not run an auditor team, execute DuckDB transcript analysis, verify story completeness, emit findings to `intake-queue.jsonl`, or close a sprint. Two independent subagent tree scans confirm ECC has no retrospective analogue at all. Conflating a session-end hook with a full retrospective workflow mischaracterizes both systems for the integration decision.
- **evidence:** `gemini-deep-research-output.md` table: `retro skill | Stop hook pattern | Auto-summarization of successes/failures at session end`. Against: `research-feature-parallels.md:Retrospectives (ECC section)`: "No analogue [OFFICIAL]. Searched `commands/`, `skills/`, and README for 'retro' / 'retrospective' / 'post-mortem' — nothing." And `research-momentum-superior.md:Sprint Review with Auditor Team`: "ECC [OFFICIAL]: Tree scan — `retro: 0 matches`."
- **suggestion:** Synthesis must not repeat the Stop-hook-as-retro mapping. Verified finding: ECC has no retrospective analogue.

---

### DOMAIN-005

- **id:** DOMAIN-005
- **severity:** medium
- **dimension:** convention_adherence
- **location:** `gemini-deep-research-output.md:frontmatter`
- **description:** The Gemini output file lacks the `sub_question` field required by corpus convention. All 7 subagent files include `sub_question: "..."` in frontmatter, each answering exactly one sub-question per `scope.md`. The Gemini file uses `method:` and `source_url:` instead and covers all 8 sub-questions in a single document. This structural non-conformance makes authority-hierarchy reasoning harder for a synthesis agent: there is no slug anchor to match the Gemini output against specific sub-questions.
- **evidence:** All 7 subagent files: `sub_question: "Architecture & capabilities..."`, `sub_question: "Maturity & community signals..."`, etc. `gemini-deep-research-output.md` frontmatter: `method: cmux-browser + chrome-mcp (DOM walker markdown reconstruction)` and `source_url: https://gemini.google.com/app/86668a7bd7fdd717` — no `sub_question` field present.
- **suggestion:** Annotate the Gemini file frontmatter with `sub_question: "all (bulk output — multi-question; treat as low-authority supplement)"` so synthesis tooling can correctly tier it.

---

### DOMAIN-006

- **id:** DOMAIN-006
- **severity:** medium
- **dimension:** convention_adherence
- **location:** `gemini-deep-research-output.md` (throughout body)
- **description:** The Gemini output uses no evidence tags (`[OFFICIAL]`, `[PRAC]`, `[UNVERIFIED]`) anywhere in the document body. All 7 subagent files apply these tags per claim. The Gemini file contains dozens of factual claims — including at least 4 confirmed hallucinations (DOMAIN-001 through DOMAIN-004, DOMAIN-007) — with zero provenance discipline. A synthesis agent reading this file without cross-checking the subagent corpus has no mechanism to distinguish verified file contents from confabulations.
- **evidence:** Sample untagged claims in `gemini-deep-research-output.md`: "The ECC repository employs a sophisticated directory structure...", "the project...currently boasting 113 contributors and over 768 commits" (verified by subagents as 159 contributors and ~1,465 commits). Compare `research-maturity-community.md`: "Total contributors:** 159 (computed from Link header on `/contributors?per_page=1` showing 159 pages of 1). [OFFICIAL]"
- **suggestion:** Add a document-level notice: "All claims in this file are [UNVERIFIED] unless cross-confirmed by a subagent file. Do not cite as primary source."

---

### DOMAIN-007

- **id:** DOMAIN-007
- **severity:** medium
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Workflow and State Management feature comparison table`
- **description:** Gemini maps Momentum's `avfl` to "`AgentShield` / Red-Blue Team" as the ECC analogue. This is wrong on two counts: (1) AgentShield is a separate repository not part of ECC (DOMAIN-001); (2) the verified subagent work identifies ECC's actual AVFL analogue as `skills/santa-method/SKILL.md` (dual reviewer, fix loop, binary verdict) — with `skills/verification-loop/SKILL.md` as a thinner peer. The AgentShield mapping misleads the decision-maker about ECC's built-in validation capability and the degree of AVFL superiority.
- **evidence:** `gemini-deep-research-output.md` table: `avfl (Adversarial Loop) | AgentShield / Red-Blue Team | Multi-agent pipeline for adversarial analysis of configurations.` Against: `research-momentum-superior.md:AVFL`: "ECC [OFFICIAL]: Two relevant analogues exist. `skills/santa-method/SKILL.md`... `skills/verification-loop/SKILL.md`" — no AgentShield mention as AVFL analogue. `research-integration-assessment.md`: "AgentShield is **not** part of ECC — it is a sibling project."
- **suggestion:** Synthesis must use santa-method + verification-loop as ECC's AVFL analogue framing.

---

### DOMAIN-008

- **id:** DOMAIN-008
- **severity:** medium
- **dimension:** fitness_for_purpose
- **location:** `research-integration-assessment.md:Adopt-as-Is`
- **description:** The integration assessment recommends adopting `silent-failure-hunter.md` and `skills/repo-scan/SKILL.md` with effort estimates and commit messages, but neither recommendation connects to Momentum's own intake-queue workflow. The assessment says "commit as `feat(skills): avfl — add silent-failure-hunter adversary`" but doesn't note that adoption ideas in Momentum flow through `momentum:intake` → `intake-queue.jsonl` → `stories/index.json`. For a maintainer who relies on the intake queue as the canonical source of backlog work, the integration recommendations are actionable as prose but not yet wired to the practice's own tracking primitives.
- **evidence:** `research-integration-assessment.md:Adopt-as-Is:silent-failure-hunter`: "Integration cost. ~30 minutes... commit as `feat(skills): avfl — add silent-failure-hunter adversary`. [PRAC]" — no intake queue reference. Compare `_bmad-output/implementation-artifacts/intake-queue.jsonl` (confirmed present with structured `id`, `status: open`, `title`, `description` fields per `research-momentum-superior.md:Intake Queue Event Log`).
- **suggestion:** Note in the synthesis or integration-assessment that the three "Adopt now" items should be queued through `momentum:intake` before sprint-planning picks them up. Low-impact but aligns research output to Momentum's practice.

---

### DOMAIN-009

- **id:** DOMAIN-009
- **severity:** medium
- **dimension:** fitness_for_purpose
- **location:** `research-portability.md` (multi-agent story gap)
- **description:** `scope.md` sub-question 6 explicitly asks "What is the multi-agent story?" as part of the portability question. The portability file covers the abstraction-layer question thoroughly but is silent on whether ECC's cross-harness agents support multi-agent spawning patterns (TeamCreate, Fan-Out) comparable to Momentum's Agent-tool-based parallelism. For a decision about whether to stay Claude-Code-exclusive, knowing whether ECC's multi-agent orchestration translates across harnesses is material.
- **evidence:** `scope.md:sub_questions` item 6: "Is there an abstraction layer? **What is the multi-agent story?**" The phrase "multi-agent story" does not appear in `research-portability.md`. The file covers hook portability, MCP portability, manifest portability, and AGENTS.md, but does not address whether Fan-Out/TeamCreate/worktree patterns are portable or how ECC's `dmux-workflows` (which orchestrates agents across Claude Code, Codex, OpenCode, Gemini, Qwen) interacts with cross-harness multi-agent support.
- **suggestion:** Synthesis should explicitly flag this as an open question: "ECC's per-harness multi-agent story was not assessed — the portability sub-question's multi-agent dimension remains unanswered."

---

### DOMAIN-010

- **id:** DOMAIN-010
- **severity:** low
- **dimension:** domain_rule_compliance
- **location:** `research-feature-parallels.md:Sides at a Glance table (Agent count row)` and `Code review section`
- **description:** Minor path-citation inconsistency. The table lists `qa-reviewer.md` in the agent count row alongside `agents/dev*.md` and `e2e-validator.md`, implying it is under `agents/`. But in the Code review section it is cited as `skills/momentum/skills/qa-reviewer.md (in agents/)` — a `skills/` path with an `(in agents/)` parenthetical that is internally inconsistent.
- **evidence:** `research-feature-parallels.md:Sides at a Glance`: "7 agent .md files (`agents/dev*.md`, `e2e-validator.md`, `qa-reviewer.md`) + `agents/evals/`". `research-feature-parallels.md:Code review section`: "`skills/momentum/skills/qa-reviewer.md` (in `agents/`) — agent persona invoked during sprint-dev review."
- **suggestion:** Verify the actual path. Use the correct path consistently throughout; drop the contradictory parenthetical.

---

### DOMAIN-011

- **id:** DOMAIN-011
- **severity:** low
- **dimension:** convention_adherence
- **location:** `research-maturity-community.md:Star & Fork Growth section (inline evidence tags)`
- **description:** Inline evidence tags in the Star & Fork Growth section use bare text URL format (`[PRAC: medium.com/@tentenco]`, `[PRAC: bridgers.agency]`) rather than the Markdown hyperlink format `([Name](URL))` used in the `## Sources` section at the end. Minor formatting inconsistency that does not affect content validity.
- **evidence:** `research-maturity-community.md:Star & Fork Growth`: "[PRAC: medium.com/@tentenco]" and "[PRAC: bridgers.agency]" as bare text. The Sources section lists: "https://medium.com/@tentenco/everything-claude-code-inside..." as a full URL, properly formatted.
- **suggestion:** Normalize inline tags to use clickable links where the URL is known. Low priority.

---

## Authority-Hierarchy Alignment Check (Dimension 9)

**Result: PASS for the 7 subagent files; FAIL for the Gemini file itself.**

The 7 subagent files correctly downgrade Gemini's claims:
- `research-architecture-capabilities.md` includes a "Verification of Suspect Numeric Claims" table that contradicts every key Gemini number (stars, forks, contributors, commits, tests) and marks discrepancies DISPUTED or UNVERIFIED.
- `research-maturity-community.md` verifies/corrects the hackathon facts with primary sources.
- `research-ecc-superior.md` explicitly marks "1,282 tests" as [UNVERIFIED].
- `research-integration-assessment.md` explicitly confirms AgentShield is external.
- `research-momentum-superior.md` derives entirely from independent tree scan, does not cite Gemini.

The problem is that `gemini-deep-research-output.md` itself carries no authority-downgrade notice. A synthesis agent reading it cold would see confident claims about `tools/agentshield/`, `qflow`, and Forum Ventures with no flags. The correction work has been done by subagents but is not persisted into the source file.

---

## Corpus Completeness Check

All 8 sub-questions from `scope.md` are covered by dedicated subagent files. DOMAIN-009 flags a partial gap within sub-question 6 (multi-agent portability story unanswered).

---

## Score

| Severity | Count | Weight | Points |
|---|---|---|---|
| Critical | 0 | -15 | 0 |
| High | 4 | -8 | -32 |
| Medium | 4 | -3 | -12 |
| Low | 2 | -1 | -2 |

**Score: 100 − 46 = 54 / 100**
**Grade: Poor — significant problems**

The score is dominated by 4 high-severity findings, all in `gemini-deep-research-output.md`. The 7 subagent files are high quality and would score clean in isolation. The corpus fails primarily because the Gemini output file lacks provenance warnings and contains at least 4 hallucinated ECC architectural claims that would corrupt any synthesis reading it without cross-checking.

---

## Summary

The 7 subagent files are excellent — well-sourced, evidence-tagged, with `## Sources` sections and concrete file paths + effort estimates sufficient for the integration-vs-stay-independent decision. The corpus's domain fitness problem is concentrated in `gemini-deep-research-output.md`: it has no provenance downgrade header, no `[OFFICIAL]`/`[PRAC]`/`[UNVERIFIED]` tags, and contains at least 4 hallucinated ECC facts (nonexistent `tools/agentshield/` directory, nonexistent `qflow` MCP server, wrong hackathon sponsor/date, wrong retro analogue). The primary fix is to add an authority-downgrade notice to the Gemini file and ensure synthesis tooling treats its claims as `[UNVERIFIED]` unless cross-confirmed by a subagent. Two medium findings (DOMAIN-008, DOMAIN-009) flag a gap in the integration assessment's connection to Momentum's intake workflow and an unanswered slice of the portability sub-question.
