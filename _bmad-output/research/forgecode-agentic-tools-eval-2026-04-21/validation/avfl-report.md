---
content_origin: avfl-consolidator
date: 2026-04-21
profile: checkpoint
stage: checkpoint
corpus_file_count: 7
---

# AVFL Validation Report — Research Corpus

## Summary

- **Consolidated score:** 50/100
- **Grade:** Failing — major rework needed
- **Findings by severity:** critical=2, high=8, medium=11, low=2, total=23 (21 after deduplication)
- **Lenses run:** structural, accuracy
- **Duplicates removed:** 2
- **Cross-document contradictions identified:** 5

This research corpus suffers from pervasive factual errors, missing external evidence tags, and uncorroborated claims that contradict multiple authoritative sources. The most damaging issues are the TermBench 2.0 cheating disclosure (critical) and systematic misrepresentation of tool capabilities and metrics across files. At checkpoint stage with a Failing grade, the corpus requires substantial fact-checking and restructuring before handoff.

---

## Findings (sorted by severity, then by location)

### FINDING-001
- **severity:** critical
- **confidence:** MEDIUM (single reviewer, checkpoint profile)
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:main body + research-forgecode-overview.md:TermBench 2.0 Scoring
- **description:** ForgeCode's TermBench 2.0 score of 81.8% is fundamentally misrepresented. The official DebugML paper "Finding Widespread Cheating on Popular Agent Benchmarks" (debugml.github.io/cheating-agents/) exposes that ForgeCode achieves this score via embedded answer keys in AGENTS.md files. Adjusted fair score is approximately 71.7% (14th place, not 1st). No corpus file discloses this cheating mechanism or adjusted score.
- **evidence:** gemini-deep-research-output.md claims "ForgeCode leads at 81.8%"; research-forgecode-overview.md states the same score without mentioning cheating disclosure; DebugML paper directly contradicts this ranking.
- **suggestion:** Amend both files to cite the DebugML cheating investigation and adjust ForgeCode score to 71.7% with note that 81.8% was invalidated. Add reference: debugml.github.io/cheating-agents/

### FINDING-002
- **severity:** critical
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:Hooks and Deterministic Orchestration
- **description:** Gemini claims ForgeCode and Claude Code have "native hook systems for validation and logging" — this contradicts research-forgecode-overview.md which explicitly states "Hooks are the most important explicit gap" and gemini-deep-research-output.md Follow-Up 2 Goose section which cites sanj.dev blog claiming Goose hooks are "Missing (no lifecycle hook API; MCP only)." The claim appears unsupported by other corpus files.
- **evidence:** gemini-deep-research-output.md: "Claude Code and ForgeCode provide native hook systems"; research-forgecode-overview.md: "Hooks are the most important explicit gap"; research-momentum-practice-surface.md: "Goose hooks = Missing (no lifecycle hook API; MCP only)"
- **suggestion:** Revise gemini section to acknowledge hooks are NOT native; clarify which tools support MCP-based hooks vs. lifecycle hooks. Remove claim about native hook support or cite source material proving it.

### FINDING-003
- **severity:** high
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Maturity section
- **description:** Gemini cites ForgeCode as "v0.106.0 as of August 2025" while all other corpus files (research-forgecode-overview.md, research-agentic-peers-comparison.md, research-integration-parallel-replace-paths.md) cite v2.12.0 as of April 2026. These are irreconcilable version schemes — no reasonable path explains how 0.106.0 becomes 2.12.0. Suggests Gemini drew from stale/incorrect source material.
- **evidence:** gemini-deep-research-output.md: "v0.106.0 as of August 2025"; research-forgecode-overview.md: "v2.12.0 (current, April 2026)"
- **suggestion:** Verify current ForgeCode version from official repository. Update gemini to cite v2.12.0 with April 2026 timestamp, or revise release date to match version scheme.

### FINDING-004
- **severity:** high
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:OpenCode section
- **description:** Gemini claims OpenCode has "over 95,000 GitHub stars and 2.5 million monthly developers" while research-integration-parallel-replace-paths.md and research-agentic-peers-comparison.md cite ~147K stars and 6.5M monthly developers (April 2026 snapshots). Difference is ~55% undercounting on stars and ~37% undercounting on developer count.
- **evidence:** gemini-deep-research-output.md: "95,000 stars and 2.5M monthly devs"; research-integration-parallel-replace-paths.md: "~147K stars"; research-agentic-peers-comparison.md: "6.5M monthly developers"
- **suggestion:** Update OpenCode metrics to cite current April 2026 data: 147K stars, 6.5M monthly developers. Add a note explaining the disparity (older snapshot vs. current).

### FINDING-005
- **severity:** high
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Integration Surface (Pathway C)
- **description:** Gemini claims ForgeCode has a "VS Code extension's 'never' mode" as an integration surface. In reality, the ForgeCode VS Code extension is a file-reference utility with 1,679 installs — not a coding assistant and certainly not a mode. research-forgecode-overview.md explicitly states "No VS Code extension, no JetBrains plugin" as features/capabilities. Gemini appears to have fabricated or severely misrepresented this integration vector.
- **evidence:** gemini-deep-research-output.md: "VS Code extension's 'never' mode"; research-forgecode-overview.md: "No VS Code extension, no JetBrains plugin"
- **suggestion:** Remove the claim about VS Code 'never' mode. Clarify that ForgeCode has a lightweight file-reference utility (1,679 installs), not an IDE integration. Reclassify as a non-integration surface or remove entirely from integration analysis.

### FINDING-006
- **severity:** high
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-Up 1
- **description:** Gemini cites "Claude 4.6 Opus" which is incorrect naming. Anthropic's canonical naming is "Claude Opus 4.6" (tier comes before version). The system context confirms current models are Opus 4.7, Sonnet 4.6, Haiku 4.5. This is a factual naming error that undermines credibility on model-level specifications.
- **evidence:** gemini-deep-research-output.md: "Claude 4.6 Opus"; system context: "Claude Opus 4.7"
- **suggestion:** Correct to "Claude Opus 4.6" throughout. If current, update to "Claude Opus 4.7" to match present day (2026-04-21). Add a note about model versioning convention.

### FINDING-007
- **severity:** high
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** traceability
- **location:** gemini-deep-research-output.md:Follow-Up 2 Goose section
- **description:** Gemini cites sanj.dev practitioner blog as "Primary Source" for Goose HTTP hooks capability. However, research-momentum-practice-surface.md states Goose hooks are "Missing (no lifecycle hook API; MCP only)." This is a direct contradiction on a core capability claim. Primary source status does not override corpus consensus on a factual matter.
- **evidence:** gemini-deep-research-output.md Follow-Up 2: Cites sanj.dev blog claiming Goose hooks exist; research-momentum-practice-surface.md: "Goose: Missing (no lifecycle hook API; MCP only)"
- **suggestion:** Resolve contradiction by verifying Goose's actual hook capabilities against official documentation. Update gemini and/or research-momentum-practice-surface.md to agree on whether lifecycle hooks exist. Add authoritative source citation (official Goose docs).

### FINDING-008
- **severity:** high
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** structural_validity
- **location:** gemini-deep-research-output.md:main body (lines 9-208)
- **description:** Main body contains zero evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]) and no sources section, unlike all other corpus files which systematically tag claims and provide source references. This is a structural inconsistency that violates the corpus format standard.
- **evidence:** gemini-deep-research-output.md main body: no [OFFICIAL], [PRAC], or [UNVERIFIED] tags; research-forgecode-overview.md, research-momentum-practice-surface.md: all have evidence tags and sources sections
- **suggestion:** Add evidence tags to all significant claims in gemini main body. Create a sources section at the end listing URLs and source documents. Standardize formatting to match other corpus files.

### FINDING-009
- **severity:** high
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:opencode-workflows section
- **description:** Gemini claims OpenCode supports "JSON-defined DAG workflows" via opencode-workflows plugin. research-momentum-practice-surface.md classifies OpenCode workflows as "Glue" (utility layer without a DAG DSL). This is a direct contradiction on OpenCode's workflow capabilities — either it has DAGs or it doesn't.
- **evidence:** gemini-deep-research-output.md: "OpenCode supports...JSON-defined DAG workflows"; research-momentum-practice-surface.md: "OpenCode workflows = Glue (no DAG DSL)"
- **suggestion:** Verify opencode-workflows plugin documentation. If DAG support exists, update research-momentum-practice-surface.md. If not, revise gemini to clarify that opencode-workflows is a utility layer without structured DAG definition.

### FINDING-010
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:Follow-Up 2 OpenCode
- **description:** Gemini claims oh-my-opencode plugin provides hooks but gives no URL, no evidence tag, and provides no corroboration from other corpus files. This is an uncited claim that cannot be verified against source material.
- **evidence:** gemini-deep-research-output.md Follow-Up 2: "oh-my-opencode plugin"; no URL, no [OFFICIAL] or source link provided; research-agentic-peers-comparison.md and research-momentum-practice-surface.md do not mention oh-my-opencode
- **suggestion:** Add a URL and [OFFICIAL] source tag to the oh-my-opencode claim. If the plugin is referenced elsewhere in the corpus, cite that reference. If not verifiable, remove the claim or mark as [UNVERIFIED].

### FINDING-011
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:Follow-Up 2 Goose
- **description:** Citation "aaif-goose/goose#8184" has no URL, no evidence tag, and is not corroborated elsewhere in the corpus. This is a GitHub issue reference without proper formatting or verification.
- **evidence:** gemini-deep-research-output.md Follow-Up 2 Goose: "aaif-goose/goose#8184" — no URL, unique formatting not seen in other citations
- **suggestion:** Convert to full GitHub URL (github.com/aaif-goose/goose/issues/8184) and add [OFFICIAL] tag. Verify the issue exists and is relevant to the claim being made.

### FINDING-012
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** traceability
- **location:** gemini-deep-research-output.md:ForgeCode Architecture section
- **description:** Gemini names ForgeCode components: "Tool-Call Correction Layer," "Semantic Entry-Point Discovery," and "10-message thinking budget threshold." These component names appear ONLY in gemini-deep-research-output.md and not in research-forgecode-overview.md which read the official README. This suggests elaboration or hallucination of feature names.
- **evidence:** gemini-deep-research-output.md ForgeCode Architecture: names three specific components; research-forgecode-overview.md README analysis: no mention of these exact component names
- **suggestion:** Verify these component names against official ForgeCode README/documentation. If they are not official names, replace with actual component names from source material or mark as [UNVERIFIED] elaboration. If they are correct, add source URL citation.

### FINDING-013
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Bifrost section
- **description:** Gemini writes "Maxim AI" when the correct name is "Maxim" (product at getmaxim.ai). Also cites "11 µs overhead" without noting this is t3.xlarge-specific; t3.medium shows 59 µs. Overprecision without context is misleading.
- **evidence:** gemini-deep-research-output.md: "Maxim AI...11 µs overhead"; getmaxim.ai: product is "Maxim"; overhead varies by instance type
- **suggestion:** Correct to "Maxim" with URL getmaxim.ai. Amend overhead claim to specify instance type: "11 µs on t3.xlarge (59 µs on t3.medium)." Add [PRAC] tag for performance claims.

### FINDING-014
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Risk Assessment table
- **description:** ForgeCode stars cited as "6.6K" but April 2026 snapshot shows 6.8K (2.3% drift). While not catastrophic, it indicates stale/rounded data from an earlier snapshot.
- **evidence:** gemini-deep-research-output.md Risk Assessment: "6.6K stars"; research-agentic-peers-comparison.md April 2026: "6.8K stars"
- **suggestion:** Update to 6.8K stars. Add snapshot date (April 2026) to disambiguate from earlier data. Consider including a note about version drift across files.

### FINDING-015
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** logical_soundness
- **location:** gemini-deep-research-output.md:Conclusion / Recommendation 4
- **description:** Gemini recommends opencode-workflows plugin (solo-dev, no governance) for "critical engineering paths" — yet the corpus itself identifies governance and sustainability as key risk factors in its own framework. This recommendation contradicts the corpus's own risk assessment principles.
- **evidence:** gemini-deep-research-output.md Recommendation 4: "opencode-workflows plugin for critical paths"; framework discussion of governance risk for solo-dev tools
- **suggestion:** Either revise recommendation to exclude critical paths, or reframe as a conditional recommendation with explicit governance/sustainability caveats. Align with the corpus's own risk framework.

### FINDING-016
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** research-momentum-practice-surface.md:Qwen Code section
- **description:** Claims "13 lifecycle events" but lists 14 named events in the same section. Arithmetic error.
- **evidence:** research-momentum-practice-surface.md Qwen Code: states "13 lifecycle events" then lists: [14 named events enumerated]
- **suggestion:** Either reduce count to 12, verify actual count and correct to 14, or provide clarification about which events are "lifecycle" vs. other types.

### FINDING-017
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** research-integration-parallel-replace-paths.md:Goose section
- **description:** Cites "~29K stars" for Goose; research-agentic-peers-comparison.md and other files cite 42.9K (current April 2026). This is a 48% undercount suggesting stale data.
- **evidence:** research-integration-parallel-replace-paths.md: "~29K stars"; research-agentic-peers-comparison.md: "42.9K stars"
- **suggestion:** Update to 42.9K stars. Add snapshot date to disambiguate. Check whether other metrics in research-integration-parallel-replace-paths.md are equally stale.

### FINDING-018
- **severity:** medium
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-Up 2 OpenCode hooks
- **description:** Gemini frames oh-my-opencode as a "community workaround" for missing OpenCode hooks. In fact, OpenCode has native 25+ event plugin system; oh-my-opencode adds Claude Code-format compatibility on top. Characterization is misleading.
- **evidence:** gemini-deep-research-output.md: "community workaround for missing hooks"; research-momentum-practice-surface.md: "OpenCode: 25+ plugin events (native)"
- **suggestion:** Reframe oh-my-opencode as an adapter/bridge layer, not a workaround. Clarify that OpenCode has native hooks and oh-my-opencode provides Claude Code-compatible formatting.

### FINDING-019
- **severity:** low
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** research-agentic-peers-comparison.md:ForgeCode header + research-integration-parallel-replace-paths.md
- **description:** Both research-agentic-peers-comparison.md and research-integration-parallel-replace-paths.md use tailcallhq/forgecode as ForgeCode's canonical GitHub URL. research-forgecode-overview.md identifies antinomyhq/forge as canonical. Both URLs currently resolve to the same content, but using inconsistent canonical references weakens cross-document integrity.
- **evidence:** research-agentic-peers-comparison.md: "tailcallhq/forgecode"; research-forgecode-overview.md: "antinomyhq/forge"
- **suggestion:** Standardize on antinomyhq/forge as canonical URL across all files (research-forgecode-overview.md is most authoritative on ForgeCode details). Update research-agentic-peers-comparison.md and research-integration-parallel-replace-paths.md to use antinomyhq/forge.

### FINDING-020
- **severity:** low
- **confidence:** MEDIUM
- **lens:** structural
- **dimension:** cross_reference_integrity
- **location:** gemini-deep-research-output.md:Follow-Up 1
- **description:** Gemini cites tailcallhq/forgecode as ForgeCode repository URL; research-forgecode-overview.md identifies antinomyhq/forge as canonical. Same issue as FINDING-019 but specific to gemini file.
- **evidence:** gemini-deep-research-output.md Follow-Up 1: "tailcallhq/forgecode"; research-forgecode-overview.md: "antinomyhq/forge"
- **suggestion:** Update to antinomyhq/forge URL to align with authoritative source (research-forgecode-overview.md).

### FINDING-021
- **severity:** low
- **confidence:** MEDIUM
- **lens:** accuracy
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Risk Assessment table
- **description:** ForgeCode releases cited as "334 releases" but April 2026 snapshot shows 336. Minor drift (0.6%) but indicates snapshot age mismatch.
- **evidence:** gemini-deep-research-output.md Risk Assessment: "334 releases"; research-agentic-peers-comparison.md April 2026: "336 releases"
- **suggestion:** Update to 336 releases. Standardize snapshot dates across all metrics in the Risk Assessment table.

---

## Consolidation Notes

### Merges Performed
1. **STRUCTURAL-003 merged with ACCURACY-003:** Both concern OpenCode star count (95K vs 147K). Consolidated as FINDING-004 (high severity, single location with evidence from both lenses).
2. **STRUCTURAL-008 merged with ACCURACY-011:** Both concern ForgeCode repository URL inconsistency (tailcallhq vs antinomyhq). Consolidated as FINDING-019 and FINDING-020 (separate files, but same underlying issue).

### Cross-Document Contradictions Identified
1. **Hooks capability:** Gemini claims "native hook systems" for ForgeCode; research-forgecode-overview.md says hooks are "most important explicit gap." Unresolved.
2. **ForgeCode version:** Gemini cites v0.106.0 (Aug 2025); all other files cite v2.12.0 (Apr 2026). Unresolved — requires version scheme clarification.
3. **Goose hooks:** Gemini cites sanj.dev blog supporting Goose hooks; research-momentum-practice-surface.md says "Missing (MCP only)." Unresolved.
4. **OpenCode workflows:** Gemini claims "JSON-defined DAG workflows"; research-momentum-practice-surface.md says "Glue (no DAG DSL)." Unresolved.
5. **oh-my-opencode purpose:** Gemini frames as "workaround"; research-momentum-practice-surface.md implies OpenCode has native events. Unresolved characterization issue.

### Scope Assessment
This is a **Failing** checkpoint-stage corpus suitable only for major rework, not handoff:
- Critical errors (ForgeCode TermBench cheating, hook system claims) make portions dangerous for decision-making.
- Systematic metric staleness (stars, versions, release counts) across multiple files suggests coordinated reuse of outdated snapshots.
- Missing evidence tags in gemini file violate corpus format standards.
- Five major cross-document contradictions remain unresolved.

### Recommendation for Fix Phase
If fix phase proceeds:
1. **CRITICAL findings (1–2):** Must resolve TermBench cheating disclosure and hook system claims against authoritative sources before any other work.
2. **HIGH findings (3–7):** Require factual verification against official tool repositories and documentation.
3. **MEDIUM findings (8–18):** Require consistency pass and evidence tagging.
4. **Stale data:** Consider re-running data collection for all metrics (stars, versions, developer counts) against April 2026 snapshots to ensure consistency.

### Confidence Calibration (Checkpoint Profile)
All findings tagged MEDIUM confidence per checkpoint profile rules (single reviewer per lens, no Adversary cross-check). Were this a full profile with dual reviewers, several findings (TermBench cheating, hook contradictions, version mismatch) would elevate to HIGH confidence due to independent corroboration in corpus material itself.

---

## Exit Status: CHECKPOINT_WARNING

**Fixer phase skipped deliberately.** Rationale:

- `authority_hierarchy` not set — most findings are cross-document contradictions that the fixer would mark as `unresolved_contradiction` per AVFL corpus-mode rules, leaving files unchanged anyway.
- The corpus consists of raw research artifacts whose provenance (Gemini Deep Research output, Claude-Code subagent outputs) is itself evidence about each source's reliability. Editing `gemini-deep-research-output.md` would destroy that signal.
- **Phase 5 (synthesis) incorporates these findings as direct corrections in the final document.** The final document's `derives_from` chain will reference this validation report and apply corrections in-line.
- AVFL findings are also direct input to **Phase 4 (Practitioner Q&A)** — targeted questions to the developer for the highest-stakes disputes (TermBench cheating, hook-system claims, version numbers).

Accepting CHECKPOINT_WARNING per the checkpoint profile exit rules. Score 50/100 reflects corpus reliability needs — synthesis will address.
