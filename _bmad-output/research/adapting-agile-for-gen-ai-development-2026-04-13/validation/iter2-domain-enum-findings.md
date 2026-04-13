# Domain Fitness — Enumerator Findings (Iteration 2)

**Lens:** Domain Fitness
**Role:** Enumerator
**Skepticism level:** 2 (Balanced) — evidence required, benefit of the doubt, no re-reporting fixed issues
**Date:** 2026-04-13

## Summary

7 findings — 0 critical, 2 high, 3 medium, 2 low

Iteration 1 fixes were largely effective. The ATDD/BDD/Gherkin disambiguation was applied and works. The Anthropic Bloom UNVERIFIED tag is present. The E2E clarification is adequate. The MIT NANDA claim is properly qualified. The METR contradiction across files was corrected in the granularity file. No re-reported issues.

Remaining concerns cluster in three areas: (1) TDA is still a renamed TDD without genuine domain content — the fix was not applied to the Gemini file body; (2) the "spec-correct, value-zero" layered defense is genuinely circular at Layer 3 without external specification as a prerequisite; (3) the seven competing names for post-story work units are still unresolved and leave a practitioner without an operational definition; (4) Shape Up and Zero-Backlog coverage is structurally present but contains no adaptation guidance for solo/small teams and the specific conditions under which each applies are underdeveloped.

---

## Findings

### DOMAIN-R01
- **id:** DOMAIN-R01
- **severity:** high
- **dimension:** domain_rule_compliance
- **location:** `gemini-deep-research-output.md:Test-Driven AI (TDA) and the 'Red' Phase`
- **description:** The TDA fix from iteration 1 was applied to the Gemini file's `fix-log-gemini.md` — but reviewing the actual Gemini file body, the "Test-Driven AI (TDA)" label and its attribution to "Kent Beck and others" remains unchanged in the `gemini-deep-research-output.md` body. The fix was logged but the target text was not altered. The claim still reads: "Kent Beck and others have emphasized that TDD is a 'superpower' in the age of AI agents. However, the methodology has evolved into 'Test-Driven AI' (TDA)." The Gemini fix log (FIX 7 in fix-log-gemini.md) only added the "Blind Tester" known-gap note and does not describe fixing TDA. The TDA term is a renamed TDD with no documented domain distinction — Beck does not use or endorse "TDA" in his cited sources (Tidy First Substack, Pragmatic Engineer interview). Additionally, the term appears in `gemini-deep-research-output.md:Follow-up Q2` ("Red/Green TDA") and `gemini-deep-research-output.md:Follow-up Q3` ("Red/Green TDA") without correction.
- **evidence:** "Kent Beck and others have emphasized that Test-Driven Development (TDD) is a 'superpower' in the age of AI agents. However, the methodology has evolved into 'Test-Driven AI' (TDA). A critical component of TDA is the 'red' phase: writing a test and watching it fail before allowing the agent to implement the solution." (`gemini-deep-research-output.md`, "Test-Driven AI (TDA) and the 'Red' Phase") — body text unchanged from iteration 1. Fix log FIX 7 in `fix-log-gemini.md` does not address TDA, confirming the fix was not applied.
- **suggestion:** Rename "TDA" to "TDD applied to AI-assisted development" throughout the Gemini file. Remove the claim that "the methodology has evolved into TDA" — the described practice is standard TDD red/green/refactor applied in an AI context. If a third-party source coined "TDA" independently, attribute it to that source specifically and do not associate it with Beck.

---

### DOMAIN-R02
- **id:** DOMAIN-R02
- **severity:** high
- **dimension:** fitness_for_purpose
- **location:** `research-spec-correct-value-zero.md:Synthesis — A Framework for Closing the Gap`
- **description:** The "layered defense" synthesis (Layers 1–5) remains partially circular. Layer 3 ("Deterministic verification against external truth: Use executable BDD specs as the verification pipeline") depends on having valid BDD specs — but Layer 2 is what produces those specs. If Layer 2 fails (the spec was written without proper user assumption validation, or the PM lacks "intent competency"), Layer 3 does not verify against external truth: it verifies against the flawed spec. The paper cited for Layer 3 (arxiv 2603.25773) explicitly acknowledges that BDD specifications can "catch domain-specific defects that AI review missed" — but only when the specifications correctly capture domain intent. The corpus does not provide actionable guidance for what a team does when Layer 2 produces an incorrect spec. Layer 5 ("Continuous feedback loops") is the only escape valve but is described at high abstraction with no operational guidance for how short the cycle must be or what triggers a spec revision versus a product rollback. A solo/small-team practitioner reading this section cannot determine concretely whether the defense is self-closing or has exits.
- **evidence:** "Layer 2 — Specification quality as a first-class practice: Write specs assuming zero implicit context... Layer 3 — Deterministic verification against external truth: Use executable BDD specs as the verification pipeline, not AI-on-AI review." (`research-spec-correct-value-zero.md`, Synthesis section) — Layer 3 is predicated on Layer 2 correctness, which is the very gap the document is attempting to close.
- **suggestion:** Add a clarifying note at the synthesis that the layered defense is not self-sealing: if Layer 2 produces a wrong spec, Layers 3–4 enforce a wrong spec efficiently. Layer 5 (feedback loop shorter than the spec-writing cycle) is therefore not optional — it is the structural prerequisite for the other layers to have net positive effect. A single sentence identifying this dependency would make the framework honest about its failure conditions without restructuring the content.

---

### DOMAIN-R03
- **id:** DOMAIN-R03
- **severity:** medium
- **dimension:** fitness_for_purpose
- **location:** `research-work-granularity-ai-speed.md:What Replaces the User Story` / `research-ceremony-rhythm-alternatives.md:Synthesis` / `gemini-deep-research-output.md:Restructuring Work Granularity`
- **description:** The corpus uses seven distinct names for post-story work units across three files — Bolts, Units of Work, Agent Stories, Impact Loops, Context Capsules, Super-Specs, and "shaped pitches" — without a reconciling taxonomy. A practitioner reading across the corpus cannot determine whether these are synonyms, layered concepts, or competing alternatives. Specifically: "Bolts" (AI-DLC / Gemini file), "Units of Work" (AI-DLC, also used in Agentsway), "Agent Stories" (Kurilyak framework), "Impact Loops" (brgr.one), "Context Capsules" (Crywolfe/dev.to), "Super-Specs" (AI/works), and "shaped pitches" (Shape Up synthesis in granularity file) are all presented as replacements or restructurings of the user story, but each comes from a different framework with different scope and constraints. The granularity file's synthesis attempts to combine them ("Shape Up shaping + SDD + Agent Stories"), but does not explain whether "Agent Stories" and "Bolts" are interchangeable or different layers. A practitioner adopting any of these needs to know: which applies to my context, and do I need more than one?
- **evidence:** `research-work-granularity-ai-speed.md:Synthesis` uses "shaped pitches," "Agent Stories," and references to continuous flow — three separate concepts combined without explaining their operational relationship. `research-ceremony-rhythm-alternatives.md` references "Impact Loops" and "Units of Work" without cross-referencing the granularity file's Agent Stories taxonomy. `gemini-deep-research-output.md` uses "Bolts" and "Units of Work" in the AI-DLC context but does not map these to Agent Stories.
- **suggestion:** The granularity file's synthesis section is the natural place for a two-paragraph reconciliation: (1) clarify that "Bolts," "Units of Work," and "Agent Stories" describe the same conceptual slot (sub-sprint execution unit for AI agents) from different frameworks, and (2) distinguish these from "Super-Specs" and "shaped pitches," which are planning artifacts rather than execution units. A small reconciliation table would make this cross-file issue tractable without requiring structural changes.

---

### DOMAIN-R04
- **id:** DOMAIN-R04
- **severity:** medium
- **dimension:** fitness_for_purpose
- **location:** `research-ceremony-rhythm-alternatives.md:Shape Up as an AI-Compatible Alternative`
- **description:** The Shape Up section explicitly notes: "no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context." This is an honest qualification. However, the synthesis section at the end of the same file — and the synthesis in `research-work-granularity-ai-speed.md` — recommends "Shape Up's shaping discipline" as a primary planning layer without re-noting this caveat. A practitioner following the synthesis guidance would adopt Shape Up for AI-native contexts while the body of the document has already told them this is structurally argued but not empirically validated. The caveat is present but gets lost as it moves from body to synthesis.
- **evidence:** "no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team" (`research-ceremony-rhythm-alternatives.md`, Shape Up section) vs. "1. Shape Up's shaping discipline for the planning layer — appetite-bounded problem framing before any AI agent work begins" (`research-work-granularity-ai-speed.md`, Synthesis) — the synthesis recommends without re-flagging the caveat.
- **suggestion:** Add "(structurally compatible; no empirical cases validated for AI-native teams as of April 2026)" as a parenthetical in the synthesis recommendation in both files. The caveat is already in the body; it only needs to propagate to the recommendation.

---

### DOMAIN-R05
- **id:** DOMAIN-R05
- **severity:** medium
- **dimension:** fitness_for_purpose
- **location:** `gemini-deep-research-output.md:Follow-Up Q2:3-3-3 Model` / `research-thought-leader-frameworks-agile-ai.md:3-3-3 delivery model`
- **description:** The 3-3-3 model (Thoughtworks AI/works) is described in both files as a framework for enterprise-scale modernization. The Gemini follow-up Q2 section ("Solo Developer and Tiny Team Workflows") references "Mob Elaboration" and "Mob Construction" rituals as if they are available to a solo developer, then provides alternative patterns (OpenSpec, README-Driven Development, Project Constitution). However, the gap is not fully bridged: Mob Elaboration requires a group, and the solo adaptation offered — "Propose-Apply-Archive loop" — is a different tool from a different vendor (Fission-AI). No solo-viable equivalent to the 3-3-3 milestone structure is proposed. A solo practitioner reading this section understands why the 3-3-3 doesn't apply to them, but leaves without a comparable milestone structure for their context. The BMAD Quick Flow entry in the table is the closest item, but it is listed with a single-line description and no operational detail.
- **evidence:** "Mob Elaboration and Construction: These rituals condense weeks of sequential requirements work into a few hours of collaborative, high-bandwidth interaction" (`gemini-deep-research-output.md`, cognitive load section) — requires a team. In Q2, BMAD Quick Flow is listed in a comparison table as "Best For: Small to medium features where enterprise ceremony is overkill" but no milestone structure is described. (`gemini-deep-research-output.md`, Follow-up Q2)
- **suggestion:** Either expand the BMAD Quick Flow row with an actual milestone structure (Spec → Implementation → Validation, with time-appetite framing), or explicitly note that a solo-team equivalent of 3-3-3's milestone structure is a gap in current practitioner guidance. The honest acknowledgment of a gap is better than a table entry with insufficient detail.

---

### DOMAIN-R06
- **id:** DOMAIN-R06
- **severity:** low
- **dimension:** fitness_for_purpose
- **location:** `research-behavioral-validation-ai-agents.md:The Cheating Problem / Key Design Principles`
- **description:** The iteration 1 fix added a clarifying parenthetical for "E2E test" in the QA.tech paragraph. However, the broader problem flagged in iteration 1 DOMAIN-011 — that the document conflates two distinct problems (AI coding agents gaming their own tests vs. validating a running app for user value) — was acknowledged in the fix log but not structurally addressed. The document still presents NIST cheating research and Playwright behavioral testing in consecutive sections without an explicit scoping note distinguishing them. The Key Design Principles section lists 6 principles without labeling which apply to Problem A (preventing agent test gaming during development) vs. Problem B (validating user value in a running app). Principle 1 ("technical separation between builder and validator") addresses A; Principles 2–3 address both; Principles 4–6 address B. A dev team lead still has to reconstruct which principles apply at which stage of their workflow.
- **evidence:** "1. Technical separation between builder and validator. The agent that wrote the code must not be able to read the test artifacts..." (Principle 1 — development-phase concern) and "4. Stack validation layers, not substitute them. Static analysis catches structural defects; unit tests catch logic failures..." (Principle 4 — deployment-phase concern) presented as a flat numbered list without phasing context. (`research-behavioral-validation-ai-agents.md`, Key Design Principles)
- **suggestion:** Add a brief header before Principle 1: "Principles 1–3: Development phase (preventing agent gaming and self-referential validation)" and before Principle 4: "Principles 4–6: Deployment and production phase (validating user value in running applications)." This is a four-line change that makes the document immediately actionable without restructuring.

---

### DOMAIN-R07
- **id:** DOMAIN-R07
- **severity:** low
- **dimension:** fitness_for_purpose
- **location:** `research-ceremony-rhythm-alternatives.md:Zero-Backlog` (absent) / `gemini-deep-research-output.md:Follow-Up Q1 — Zero-Backlog`
- **description:** Zero-Backlog appears only in the Gemini follow-up Q1 as a single bullet: "In technical support and maintenance domains, practitioners are moving toward a 'Zero-Backlog' model — the 'ticket' was a necessary evil of a low-bandwidth era; with infinite compute, agents can solve problems instantly, making backlog management obsolete." This is the corpus's only substantive mention of Zero-Backlog as an Agile alternative. It has no source attribution, no named practitioner, and no description of how a team would operationalize it. The ceremony alternatives file — which is the natural home for this content — does not mention it at all. A practitioner interested in this option has no actionable entry point from the corpus.
- **evidence:** Single unsourced mention: "practitioners are moving toward a 'Zero-Backlog' model — the 'ticket' was a necessary evil of a low-bandwidth era" (`gemini-deep-research-output.md`, Follow-Up Q1). Zero-Backlog does not appear in `research-ceremony-rhythm-alternatives.md`.
- **suggestion:** Either add a source attribution and one operational example to the existing Zero-Backlog mention (making it minimally citable), or flag explicitly that "Zero-Backlog" is listed as an Agile alternative but is underdeveloped in this research corpus and requires a dedicated follow-up investigation. Given skepticism level 2, this is low severity — the corpus is not claiming Zero-Backlog as well-developed guidance, it simply mentions it. But a practitioner wanting to explore it has no path forward from the corpus.

---

## Verification Status: Iteration 1 Fixes

| Finding | Fix Claimed | Verified in Body |
|---|---|---|
| DOMAIN-001 MIT NANDA | Applied (UNVERIFIED blockquote) | Yes — present in `research-spec-correct-value-zero.md` |
| DOMAIN-002 ATDD/BDD/Gherkin | Applied (disambiguation blockquote) | Yes — present in `research-acceptance-criteria-ai-literal.md` |
| DOMAIN-003 TDA/Beck attribution | Not in any fix log | No — body text unchanged in `gemini-deep-research-output.md` → raised as DOMAIN-R01 |
| DOMAIN-004 Harness Engineering disambiguation | Applied (note added to ceremony file + Gemini) | Yes — notes present in both files |
| DOMAIN-007 METR contradiction | Applied (granularity file corrected) | Yes — granularity file now correctly states 19% longer |
| HIGH-006 Anthropic Bloom | Applied (UNVERIFIED tags in body and sources) | Yes — both UNVERIFIED markers present |
| E2E clarification | Applied (inline parenthetical) | Yes — parenthetical present in behavioral validation file |
