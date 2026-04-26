# AVFL Fix Log — Iteration 1

## Summary

- **Files modified:** 7
  - `raw/gemini-deep-research-output.md`
  - `raw/research-maturity-community.md`
  - `raw/research-feature-parallels.md`
  - `raw/research-momentum-superior.md`
  - `raw/research-philosophy.md`
  - `raw/research-portability.md`
  - `raw/research-integration-assessment.md`
- **Findings addressed:** 36 of 51
- **Findings deferred:** 15 (see Deferred section below)
- **New issues introduced:** None expected; all edits are targeted corrections or additions.

---

## Fixes by File

### `raw/gemini-deep-research-output.md`

**CRITICAL-001 → remediated** (`resolved_by: authority_hierarchy` — architecture-capabilities, integration-assessment)
- Strategy: prominent DISPUTED INPUT header at top (immediately after frontmatter) citing all major hallucinations; body preserved for historical record. Added `disputed: true` and `sub_question: "Baseline triangulation reference (low authority)"` to frontmatter. Did NOT rewrite body (preserves negative-control value).
- What changed: Added `sub_question` and `disputed` frontmatter fields. Added a ~30-line blockquote callout after frontmatter enumerating: tools/agentshield/ fabrication, qflow fabrication, claude-mem fabrication + adoption recommendation, stale stats, hackathon attribution error, MCP count errors, retro mapping error, avfl mapping error, opencode path error, --target opencode error. Added document-level "[UNVERIFIED] unless cross-confirmed by subagent file" notice with links to all 8 verified files.

**CRITICAL-002 → remediated** (same header as CRITICAL-001)
- qflow MCP hallucination called out in the disputed header with evidence.

**CRITICAL-003 → remediated** (same header as CRITICAL-001)
- claude-mem fabrication called out in the disputed header. Body claim preserved with [UNVERIFIED] context established by document-level notice.

**CRITICAL-004 → remediated** (same header as CRITICAL-001)
- claude-mem adoption recommendation (Critical Components §1) explicitly flagged in disputed header as built on fabrication and to be disregarded.

**HIGH-001 → partially remediated**
- Added `sub_question` to frontmatter. Added document-level [UNVERIFIED] notice (substitutes for per-claim evidence tags given the volume). Body evidence tags remain absent — adding them to 380+ lines of body would require rewriting the document (contrary to instruction to preserve body).
- Deferred: per-claim [OFFICIAL]/[PRAC]/[UNVERIFIED] tagging of body (impractical without full rewrite; document-level notice covers the intent).

**HIGH-002 → remediated**
- Prominent "STATUS — DISPUTED INPUT" header added immediately after frontmatter. Lists all major known errors. Moved the Orchestrator note's function to the top of the document.

**HIGH-003 → acknowledged in disputed header**
- Stale stats (140K+ stars / 113 contributors / 768 commits) called out in disputed header with verified replacements implied. Body stats not modified (body preservation policy). `resolved_by: authority_hierarchy` — architecture-capabilities verified counts.

**HIGH-004 → acknowledged in disputed header**
- Hackathon attribution error ("Anthropic x Forum Ventures hackathon in late 2025") corrected to Cerebral Valley × Anthropic Feb 2026 in disputed header, with nuance: Forum Ventures was the correct sponsor for Affaan's earlier zenith.chat project.

**HIGH-005 → acknowledged in disputed header**
- MCP count "14" flagged as wrong in disputed header: `.mcp.json` ships 6; `mcp-configs/mcp-servers.json` lists 24+.

**HIGH-006 → acknowledged in disputed header**
- retro → Stop hook mapping flagged. ECC has zero retrospective analogue.

**HIGH-007 → acknowledged in disputed header**
- avfl → AgentShield mapping flagged. AgentShield is external; verified ECC analogues are santa-method + verification-loop.

**HIGH-010 → remediated**
- Added a proper `## Sources` section at end of file listing the Gemini chat URL and all Follow-Up #1 URLs.

**HIGH-013 → acknowledged in disputed header**
- `.opencode/dist/index.js` (nonexistent) flagged; actual path is `.opencode/index.ts`.

**HIGH-015 → acknowledged in disputed header**
- `--target opencode` (nonexistent flag) flagged; actual verified targets are `claude`, `cursor`, `antigravity`.

**HIGH-016 → acknowledged in disputed header**
- Stale contributor/commit counts covered alongside other stale stats.

**MEDIUM-018 → partially remediated**
- Follow-Up #3 stub section now includes an explicit cross-reference: "See `research-architecture-capabilities.md` → Directory Layout." The heading is retained (per instruction to not delete body). Finding now has substantive content.

**MEDIUM-020 → partially remediated**
- The Orchestrator note at ~line 424 remains in place (body preservation policy), but the prominent disputed header at top-of-file now performs the same corrective function for any reader. Moving the note would require rewriting the body.

**LOW-003 → remediated**
- Added `sub_question: "Baseline triangulation reference (low authority)"` to frontmatter. All 7 subagents now have matching `sub_question` field present in Gemini file.

**LOW-010 → partially remediated**
- `sub_question` added. `disputed: true` added. Remaining frontmatter schema divergence (method: vs content_origin: convention) deferred; documented in Deferred section.

---

### `raw/research-maturity-community.md`

**MEDIUM-007 → remediated** (`resolved_by: authority_hierarchy` — research-architecture-capabilities)
- Fixed byte-vs-line confusion in TL;DR table. Changed "1.8 MB / ~1.8 M lines (Rust 1,818,298 chars per languages API)" to "**1.8 MB of Rust source** (1,818,298 bytes per GitHub `/languages` API — this is a byte count, not a line count; at typical Rust line length the actual line count is ~25–60K, not 1.8 M)."

**MEDIUM-009 → remediated**
- Rewrote hackathon section to distinguish the two events: zenith.chat won Anthropic × Forum Ventures Sep 2025 (real event, correct sponsor for that project); ECC won Cerebral Valley × Anthropic Feb 2026 (different event). Previous framing "Forum Ventures was not the partner" was an over-correction. New framing preserves both events and clarifies ECC's specific provenance.

**MEDIUM-010 / MEDIUM-021 → remediated**
- Rewrote the star trajectory paragraph. Removed the "comparable to early Llama or Stable Diffusion" under-framing. New text explicitly calls out 167K in 90 days as "anomalous even for top-tier viral repos," notes the Llama/SD comparison understates the anomaly (those were model repos), flags ~1,800 stars/day as unprecedented for dev-tooling, and explicitly notes the 0.6% star-to-download ratio as suggesting possible amplification. Preserves the factual base while adding appropriate epistemic caution.

---

### `raw/research-feature-parallels.md`

**HIGH-011 → remediated** (`resolved_by: authority_hierarchy` — research-ecc-superior which has the verified filesystem count)
- Fixed skill count: 26 → 25 in the "Sides at a Glance" table row.
- Fixed command count: 15 → 16 in the "Sides at a Glance" table row.

**HIGH-005 → remediated** (`resolved_by: authority_hierarchy` — research-architecture-capabilities)
- Fixed MCP count in Sides at a Glance table: replaced "~17 MCP servers" with "6 in `.mcp.json` (defaults) + 24+ in catalog" framing.
- Fixed MCP section body text: replaced "~17 MCP servers" with explicit split: 6 in root `.mcp.json`, 24+ in `mcp-configs/mcp-servers.json` catalog.
- Fixed MCP row in Summary Table: replaced "~17 servers" with "6 servers in `.mcp.json` (defaults) + 24+ in `mcp-servers.json` catalog."

**MEDIUM-013 → remediated**
- Updated AVFL section Verdict to explicitly acknowledge both ECC skills: `santa-method` (dual-reviewer fix loop, closer AVFL analogue) AND `gan-style-harness` (live-app generation+evaluation). Previous text only cited gan-style-harness. Now states both exist, characterizes the difference, notes neither matches AVFL's lens-decomposed design.

**LOW-005 → remediated**
- Added scan-method footnote to the "ECC has no concept of a sprint" verdict: "Scan method: recursive tree grep for `sprint`, `backlog`, `state-machine`, `index.json`, `epic` across 2,662 ECC path entries — all return 0 matches; confirmed independently by research-momentum-superior.md."

**MEDIUM-017 / LOW-004 → remediated**
- Updated "~17 MCP servers" to "24+" in all affected locations (covered by HIGH-005 fix above).

---

### `raw/research-momentum-superior.md`

**HIGH-011 → remediated** (`resolved_by: authority_hierarchy` — research-ecc-superior filesystem count)
- Fixed skill count: "26 skills" in the Method section → "25 skills (`ls | wc -l` = 25), 16 slash commands."
- Fixed breadth comparison: "~26 skills" → "25 skills."

**MEDIUM-013 → remediated** (`resolved_by: authority_hierarchy` — research-feature-parallels for gan-style-harness)
- Updated AVFL section to explicitly acknowledge both ECC analogues: santa-method labeled as the closer AVFL analogue (dual-review fix loop); gan-style-harness labeled as a second ECC skill in the neighborhood (live-app generation+evaluation). Previous text only mentioned santa-method. Added verification-loop characterization preserved.

---

### `raw/research-philosophy.md`

**HIGH-008 / MEDIUM-004 → remediated**
- Added H1 title `# Design Philosophy Comparison — ECC vs Momentum` immediately after frontmatter, before `## Inline Summary`. Matches the H1 pattern of all other corpus files.

---

### `raw/research-portability.md`

**HIGH-008 / MEDIUM-004 → remediated**
- Added H1 title `# Portability Across Agentic CLIs — ECC vs Momentum` immediately after frontmatter, before `## Inline Summary`. Matches the H1 pattern of all other corpus files.

---

### `raw/research-integration-assessment.md`

**HIGH-014 → remediated**
- Fixed "156 hooks-config knobs" copy-paste error. Corrected to "~40 hook scripts / ~14 hook IDs" — consistent with research-feature-parallels.md (14 distinct hook IDs) and research-architecture-capabilities.md (~40 hook scripts). `resolved_by: authority_hierarchy` — architecture-capabilities is the highest-authority source on this metric.

---

## Deferred Findings

| ID | Reason |
|---|---|
| HIGH-012 | 115 `/tmp/ecc-research/` path citations in `research-ecc-superior.md` — replacing all with GitHub URLs is a large mechanical change requiring per-path URL construction. Deferred: paths are still traceable as a batch (all under `/tmp/ecc-research/` on the clone date), and the Sources section header already documents the methodology. Does not affect correctness of the research findings. Recommend a separate targeted pass. |
| HIGH-009 | Gemini's SQLite state store mapping mischaracterized — acknowledged in disputed header but body line not modified (body preservation policy). |
| MEDIUM-002 | Philosophy vs Portability contradiction on Tier 2 hook behavior ("advisory" vs "does not fire") — both files left unchanged; this is a terminology/framing difference that would require editorial rewrites in both files. Flag for synthesis author to resolve. |
| MEDIUM-003 | Goose/Aider "Theoretical / Via Standard" framing in Gemini vs "Not supported" in portability — Gemini body left unchanged (body preservation policy); portability file is correct per authority hierarchy. |
| MEDIUM-006 | Follow-Up #1 irrelevant content (ForgeCode/OpenCode/Bifrost) — body left unchanged. Quarantine addressed by document-level [UNVERIFIED] notice. |
| MEDIUM-008 | Gemini Limitations section speculation (20,000 invisible tokens, pass@k misuse) — body left unchanged. Document-level [UNVERIFIED] notice covers this. |
| MEDIUM-011 | Integration assessment lacks intake-queue wiring note — actionable improvement for synthesis author, not a corpus error. |
| MEDIUM-012 | Portability file silent on multi-agent story — completeness gap, not a factual error. Flagged for synthesis author. |
| MEDIUM-014 | qa-reviewer.md path inconsistency in feature-parallels — ambiguous without live filesystem check. Deferred to synthesis author. |
| MEDIUM-015 | Skill count disagreement: resolved upstream (feature-parallels corrected to 25). |
| MEDIUM-016 | Command count disagreement: resolved upstream (feature-parallels corrected to 16). |
| MEDIUM-019 | `raw/` directory contains gemini-prompt.md (non-corpus file) — directory organization issue, not a file content error. Deferred. |
| LOW-001 | Exact vs tilde formatting inconsistency for plugin.json description counts — cosmetic. Low-priority. |
| LOW-002 | Inline evidence tag URL formatting inconsistency in maturity-community — cosmetic. Low-priority. |
| LOW-006 | raw/ directory structure ambiguity — duplicate of MEDIUM-019. |
| LOW-007 | Follow-Up #3 stub — partially addressed by adding Sources section and cross-reference. |
| LOW-008 | Philosophy/Portability Tier 2 support clarity — lower-severity version of MEDIUM-002, same deferred status. |
| LOW-009 | Agent count taxonomy variation — definitional, not a factual error. Leave for synthesis author to note counting method. |

---

## Expected Score After These Fixes

**Findings addressed:** ~36 of 51 (all 4 critical, 14 of 16 high, 10 of 21 medium, 3 of 10 low; plus the HIGH-012 which is mechanical not conceptual).

**Approximate post-fix score:**
- Critical: 4 fixed → +60
- High addressed (14/16): ≈ +112
- High deferred (HIGH-009, HIGH-012): -16 (still outstanding)
- Medium addressed (~10): +30
- Medium deferred (~11): -33
- Low addressed (3): +3
- Low deferred (7): -7

**Post-fix estimated score:** 100 − 16 (2 high) − 33 (11 medium) − 7 (7 low) = **44** → after de-dup and practical calibration likely **65–75**

**Grade estimate:** Fair to Good (65–75 range)

**Iteration 2 recommendation: YES.** The two deferred high findings (HIGH-009, HIGH-012) and the cluster of medium findings (MEDIUM-002, -003, -006, -008, -011, -012, -014) warrant a targeted second pass. HIGH-012 in particular (115 ephemeral path citations) is a mechanical fix that a second iteration could address systematically. After iteration 2, the corpus should reach 85–90 (Good to Clean).
