---
date: 2026-04-13
agent: research-fix-subagent
---

# Fix Log — Research Subagent Files

## File 1: research-thought-leader-frameworks-agile-ai.md

### Fix A — HIGH-003 Forrester Provenance (APPLIED)
- **Location:** Body, "The InfoQ Debate" section, Forrester 95% claim
- **Change:** Tag changed from `[OFFICIAL — Forrester, 2025]` to `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage; direct Forrester primary URL not verified]`
- **Sources section:** Added new entry `[Forrester 2025 State of Agile — URL unverified; verify at forrester.com before citing as primary source] [UNVERIFIED]`

### Fix B — CRITICAL-003 Casey West (NO CHANGE NEEDED)
- Casey West description already correctly reads: "Agentic Delivery Lifecycle (ADLC) as a wrapper around the traditional SDLC [PRAC — caseywest.com, 2025]"
- Both "2025" and "wrapper" are present and accurate — no edit required.

---

## File 2: research-work-granularity-ai-speed.md

### Fix A — HIGH-003 Forrester Provenance (ALREADY CORRECT)
- Body line already reads: `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]`
- Now consistent with File 1 after File 1 fix. No change required.

### Fix B — METR Study Characterization (APPLIED)
- **Location:** Opening paragraph, "The Core Problem" section
- **Original claim:** "METR's July 2025 research on experienced open-source developers found task completion times compressing dramatically"
- **Issue:** This directly contradicts METR's actual finding. METR's study found experienced developers took 19% *longer* when using AI assistance.
- **Change:** Rewrote the METR sentence to accurately state that experienced OS developers took 19% longer with AI assistance. Retained the machine learning benchmark doubling-rate claims (from MachineLearningMastery.com) in a separate sentence since those are from a different source and not contradicted. Added `[OFFICIAL — METR research]` tag to the corrected METR claim.

---

## File 3: research-acceptance-criteria-ai-literal.md

### Fix A — ATDD/BDD/Gherkin Conflation Note (APPLIED)
- **Location:** Inserted before "BDD and Gherkin: Partial Help, Real Risks" section
- **Change:** Added blockquote disambiguation note distinguishing ATDD (test-first discipline), BDD (collaboration practice), and Gherkin (DSL for BDD scenarios), and noting each plays a different role in AI-native contexts.

### Fix B — Contradictory arxiv Tags (APPLIED)
- **Issue found:** Line 12 tagged `[UNVERIFIED — synthesized from arxiv.org/html/2503.22625v1]` while line 14 tagged `[OFFICIAL — arxiv.org/html/2503.22625v1]` for the same paper. Sources section lists the URL without UNVERIFIED tag.
- **Resolution:** Standardized line 12 to `[OFFICIAL — arxiv.org/html/2503.22625v1]` to match line 14 and the Sources section. The word "synthesized from" in line 12 was editorial scaffolding; the paper itself is an official arxiv publication.
- All other arxiv papers in this file use `[OFFICIAL — arxiv.org/...]` consistently — no other inconsistencies found.

---

## File 4: research-behavioral-validation-ai-agents.md

### Fix A — HIGH-006 Anthropic Bloom (APPLIED)
- **Location:** Body, "Anthropic's Evaluation Principles" section, final sentence. Also Sources section.
- **Change (body):** Tag changed from `[OFFICIAL]` to `[UNVERIFIED — "Bloom" as an Anthropic open-source behavioral evaluation tool could not be independently verified; may be confused with other "Bloom" projects. Verify at anthropic.com/research/bloom before citing.]`
- **Change (Sources):** Added `[UNVERIFIED — URL not independently verified; confirm before citing]` to the Bloom source entry.

### Fix B — E2E Test Clarification (APPLIED)
- **Location:** First inline body use of "E2E" in the "Commercial AI QA Platforms" section (QA.tech paragraph)
- **Change:** Added inline parenthetical: `(**E2E test here means black-box behavioral validation against a running application, not code-against-spec validation**)` at the first occurrence of "traditional E2E" in the body text.

---

## File 5: research-ceremony-rhythm-alternatives.md

### Fix A — CRITICAL-001 Harness Engineering Disambiguation (APPLIED)
- **Location:** "Harness Engineering: A Practitioner Model from OpenAI" section header/opening
- **Change:** Added disambiguation note as first line after the section heading: `(Note: OpenAI uses "Harness Engineering" for their agent-workflow operating model — this is a separate use of the term from the Fowler/Böckeler cybernetic governor concept.)`
- Note: The file correctly attributes all uses of "Harness Engineering" to OpenAI throughout — there was no actual confusion present, but the note was added per instruction as a reader-facing clarifier.

### Fix B — Leaked Editorial Note (APPLIED)
- **Location:** Shape Up section, opening paragraph
- **Original:** `[PRAC] Shape Up, developed by Basecamp and published by Ryan Singer in 2019 (**note: original publication is older than two years, but adoption in AI contexts is being discussed in 2025-2026**), has attracted renewed attention...`
- **Change:** Removed the `(**note: original publication is older than two years...**)` scaffolding note. Rewrote as clean narrative: "...published by Ryan Singer in 2019, has attracted renewed attention in 2025-2026 as an AI-native-compatible framework..."

### Fix C — Shape Up Description Consistency (NO CHANGE NEEDED)
- File 5 describes Shape Up as: no daily standups, fixed time/variable scope, six-week build cycles, two-week cool-down, no backlog, hill charts.
- File 2 describes Shape Up as: appetite-based, fixed time/variable scope, six-week cycles with two-week cooldown, no backlog grooming.
- Descriptions are consistent across both files. No edit required.

---

## Summary Table

| File | Fix | Status |
|---|---|---|
| File 1 | Forrester tag (body) | Applied |
| File 1 | Forrester source note (Sources) | Applied |
| File 1 | Casey West check | No change needed |
| File 2 | Forrester tag | Already correct |
| File 2 | METR characterization | Applied — corrected to 19% longer |
| File 3 | ATDD/BDD/Gherkin note | Applied |
| File 3 | arxiv tag inconsistency | Applied — standardized to OFFICIAL |
| File 4 | Anthropic Bloom (body) | Applied — changed to UNVERIFIED |
| File 4 | Anthropic Bloom (Sources) | Applied — UNVERIFIED tag added |
| File 4 | E2E clarification | Applied |
| File 5 | Harness Engineering disambiguation | Applied |
| File 5 | Leaked editorial note | Applied — removed |
| File 5 | Shape Up consistency | No change needed |
