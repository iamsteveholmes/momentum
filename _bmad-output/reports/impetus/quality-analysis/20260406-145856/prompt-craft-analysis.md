# Prompt Craft Analysis: Impetus

**Scanner:** PromptCraftBot
**Skill:** `/skills/momentum/skills/impetus/`
**Agent type:** Stateless workflow facilitator / orchestrator
**Date:** 2026-04-06

---

## Assessment

**Skill type:** Workflow facilitator agent with strong persona — the scanner protocol recommends "Outcome + rationale + selective HOW" for this category.

**Overview quality:** SKILL.md has no `## Overview` section (pre-pass confirms `overview_lines: 0`). The file jumps directly into `## Startup` procedural routing. However, SKILL.md does carry persona context in its `## Voice & Input` section (lines 60-78), which provides identity, voice rules, input interpretation, and symbol vocabulary. The Overview's traditional role — mission framing, domain vocabulary, theory of mind — is partially fulfilled by the `## Identity` block inside workflow.md (lines 9-16). The gap is that SKILL.md itself, which is the always-loaded foundation, lacks a mission statement or domain framing paragraph at the top level.

**Persona context quality:** Strong. The persona is well-differentiated: servant-partner in the KITT sense, dry/confident, genuine satisfaction in clean state, never performs enthusiasm. Voice rules are concrete and actionable (banned phrases, symbol vocabulary, input interpretation categories). The session-greeting.md reference elevates the persona further with evocative voice guidelines ("Optimus Prime's gravitas + KITT's loyalty", "a fifty-foot robot who kneels to listen"). This is high-craft persona work — load-bearing, not waste.

**Progressive disclosure:** Good architectural split. SKILL.md (84 lines, ~1036 tokens) handles routing and persona. workflow.md (634 lines, ~9873 tokens) carries the full execution logic. workflow-runtime.md (139 lines, ~1994 tokens) handles completion signals, productive waiting, review dispatch, and subagent synthesis — loaded on demand. Six shared reference files handle session-greeting, completion-signals, progress-indicator, spec-contextualization, configuration-gap-detection, and journal-schema. The total agent footprint across all files is ~12,903 tokens (pre-pass aggregate), but on the happy path SKILL.md renders the greeting without loading workflow.md at all, which is a deliberate latency optimization.

**Synthesis:** Impetus is a well-crafted orchestrator with a distinctive, load-bearing persona and intelligent progressive disclosure. The primary craft gap is the missing Overview in SKILL.md — the agent's mission and domain framing exist but are scattered across workflow.md's Identity section and the session-greeting reference. The happy-path optimization in SKILL.md (lines 29-56) is clever engineering that avoids loading workflow.md for the most common invocation. Voice rules are repeated across SKILL.md, workflow.md, and workflow-runtime.md — this is a deliberate self-containment strategy (context compaction survival), not waste, though one instance could be trimmed. The 634-line workflow.md is large but structurally sound with well-tagged steps and clear GOTO routing.

---

## Prompt Health Summary

| Metric | Value | Notes |
|---|---|---|
| Total prompt files | 2 | workflow.md, workflow-runtime.md |
| Config headers | 0 / 2 | Neither prompt has a config header with `{communication_language}` |
| Progression conditions | 2 / 2 | Both have clear step progression and check/goto logic |
| Self-contained | Yes | Voice rules repeated in each file; workflow-runtime.md includes a voice reminder at line 8 |
| Waste patterns detected | 0 | Pre-pass found zero defensive padding or meta-explanation patterns |
| Back-references detected | 0 | No fragile "as described above" cross-references |
| Suggestive loading | 2 | SKILL.md line 30 (false positive — HTML comment), workflow.md line 34 ("read the relevant artifact") |
| Wall of text | 2 | workflow.md lines 416-433 (18 lines) and 444-459 (16 lines) |

---

## Per-Capability Craft

### SKILL.md (84 lines, ~1036 tokens)

**Role:** Startup router + persona anchor. This is the always-loaded file.

**Strengths:**
- Happy-path optimization (lines 29-56) avoids loading workflow.md entirely for the greeting route — excellent latency engineering
- Preflight script returns pre-rendered greeting fields, minimizing agent reasoning for the common case
- Voice & Input section (lines 60-78) is crisp and actionable: concrete banned phrases, symbol vocabulary, input interpretation categories with clear rules
- Routing logic uses semantic check tags that map directly to preflight output states

**Concerns:**
- No Overview section. The agent's mission framing ("handles engineering discipline — sprint tracking, quality gates, story lifecycle") exists only inside workflow.md line 11 and the SKILL.md frontmatter description. If context compaction drops workflow.md, the agent loses its mission understanding.
- The happy-path block (lines 29-56) embeds a significant amount of dispatch logic inline — menu dispatch table, stats-update call, placeholder messages for unbuilt features. This is acceptable given the optimization goal (avoid loading workflow.md) but creates a maintenance duplication with Step 7 in workflow.md which has the same dispatch logic.

### workflow.md (634 lines, ~9873 tokens)

**Role:** Primary execution workflow — install, upgrade, hash drift, session orientation, journal management.

**Strengths:**
- Identity section (lines 9-16) is excellent persona DNA — concise, evocative, and actionable. "Servant-partner in the KITT sense" establishes the entire behavioral framework in one phrase.
- Behavioral patterns section (lines 19-101) is well-structured with named patterns (Spec Contextualization, Follow-Up Question Handling, Configuration Gap Detection, Proactive Offer, No-Re-Offer, Expertise-Adaptive Orientation, Voice Rules, Input Interpretation). Each pattern is outcome-focused with clear triggers and rules.
- Install/upgrade flow (steps 2-6, 9) uses clean consent UX: show what will happen, ask before acting, respect decline.
- Step tagging (e.g., `tag="invoked-at-completion"`, `tag="invoked-at-review-dispatch"`) enables precise cross-referencing from workflow-runtime.md.
- Journal thread management (steps 11-13) handles complex state (dormant detection, dependency satisfaction, no-re-offer suppression, unwieldy triage) with clear conditional logic.

**Concerns:**
- Voice rules appear at lines 79-89 AND in SKILL.md lines 64-71 AND in workflow-runtime.md line 8. Three locations. SKILL.md and workflow-runtime.md repetition is justified for self-containment (context compaction survival). The workflow.md copy is also justified since it's the primary execution context. All three are consistent.
- The Input Interpretation structural gate (lines 97-100) is a 4-line dense paragraph. The content is important (preventing natural language from bypassing confirmation) but the run-on formatting hurts scannability.
- Wall of text at lines 416-433 (dormant thread hygiene) and 444-459 (unwieldy journal triage) — these are dense conditional logic blocks where the nested `<check>` and `<note>` elements are packed without visual breaks. The content is necessary but could benefit from tighter structural formatting.
- Dispatch logic at lines 377-384 duplicates SKILL.md lines 49-55 — same menu-to-skill mapping. Maintenance risk if dispatch targets change.

### workflow-runtime.md (139 lines, ~1994 tokens)

**Role:** On-demand behaviors loaded during mid-session workflows (completion signals, review dispatch, productive waiting, subagent synthesis).

**Strengths:**
- Voice reminder at line 8 ensures persona consistency even when loaded without SKILL.md context — proper self-containment
- Steps 15-18 are well-structured with clear goals, output templates, and edge case handling
- Subagent synthesis (step 18) implements the hub-and-spoke contract with concrete voice rules ("never: subagent names, tool names") and tiered review depth
- Flywheel integration (lines 110-119) gracefully handles the case where upstream-fix skill isn't available yet — future-proof degradation
- Confidence-directed language guidance (lines 104-107) uses varied phrasing examples to prevent robotic repetition

**Concerns:**
- No config header (no `{communication_language}` variable)
- No frontmatter (pre-pass flags missing name, description, menu-code) — this is a workflow fragment loaded on demand, so frontmatter absence is architecturally expected, but worth noting

### Shared References Assessment

**session-greeting.md:** Excellent craft. 9 greeting states with evocative templates, menu tables, dispatch tables, and closers. The voice guidelines section ("Optimus Prime's gravitas + KITT's loyalty") is some of the strongest persona writing in the system. Load-bearing.

**completion-signals.md:** Well-structured with canonical templates, examples for edge cases (no output, partial, many files), anti-patterns, and tiered review depth. Good progressive disclosure target — substantial detail that doesn't need to be in the workflow.

**progress-indicator.md:** Clean reference with collapse rules, boundary rules, symbol vocabulary, terminal rendering constraints, and journal integration. The anti-patterns section reinforces voice rules without redundancy.

**spec-contextualization.md:** Focused on the JIT surfacing pattern with motivated disclosure (why it matters before what it says). Good/bad examples make the pattern concrete. Properly outcome-focused.

**configuration-gap-detection.md:** Thorough gap inventory with blocking/non-blocking classification, detection timing, surfacing format, and resolution conversation pattern. The "ask one targeted question" flow is well-designed UX.

**journal-schema.md:** Complete schema reference with field definitions, examples, write/read semantics, declined-offers mechanics, material-change heuristic, and session stats. Dense but necessarily so — this is a data contract.

---

## Key Findings

### HIGH: Missing Overview in SKILL.md

**Affected file:** `SKILL.md` (entire file — no Overview section)
**Line:** 1-8 (jumps from frontmatter to `## Startup`)

SKILL.md lacks an `## Overview` section. For a stateless orchestrator agent with a strong persona, the Overview serves as the mission anchor — who the agent is, what "good" looks like, and why it exists. The mission framing ("handles engineering discipline — sprint tracking, quality gates, story lifecycle") currently lives only in workflow.md line 11, which is not loaded on the happy path. If context compaction drops workflow.md during a non-greeting session, the agent loses its mission understanding and reverts to mechanical step execution.

**Impact:** Agent operates without mission context on the happy path (greeting route never loads workflow.md). On non-happy paths, the agent has Identity context from workflow.md, but SKILL.md alone gives no domain framing.

**Fix:** Add a 3-5 sentence Overview section between the frontmatter and `## Startup`. Pull from workflow.md's Identity section: mission, domain vocabulary (sprint, story lifecycle, quality gates), theory of mind (the developer leads, Impetus handles machinery), and what "good" looks like (momentum — out of the way when flowing, stepping in when needed). This does not need to duplicate the full Identity — just the seed.

### MEDIUM: Dispatch logic duplication between SKILL.md and workflow.md

**Affected files:**
- `SKILL.md` lines 49-55
- `workflow.md` lines 377-384

The menu-to-skill dispatch mapping (Run sprint -> sprint-dev, Plan sprint -> sprint-planning, Activate -> sprint activate + sprint-dev, etc.) appears in both files with identical content. SKILL.md embeds it for the happy-path optimization; workflow.md Step 7 has it for the non-happy path. If a dispatch target changes, both locations must be updated.

**Impact:** Maintenance risk. A dispatch target change that updates one but not the other would route to the wrong skill on one code path.

**Fix:** This is an acceptable trade-off for the happy-path optimization. Document the coupling with a comment in both locations: `<!-- dispatch table — must match SKILL.md / workflow.md Step 7 -->`. Alternatively, extract the dispatch table to a shared reference, but that would add a file load to the happy path, defeating the optimization.

### MEDIUM: Dense paragraph blocks in workflow.md

**Affected file:** `workflow.md`
- Lines 97-100 (Input Interpretation structural gate — 4 lines of dense prose)
- Lines 416-433 (dormant thread hygiene — 18 lines, flagged by pre-pass)
- Lines 444-459 (unwieldy journal triage — 16 lines, flagged by pre-pass)

These blocks contain important conditional logic but are formatted as dense paragraphs or tightly packed XML elements without visual breathing room. The structural gate paragraph at line 97-100 is a single run-on block covering: extraction, confirmation, wait, dispatch, re-trigger prevention, and "are you sure" prohibition.

**Impact:** Scannability. An executing agent processing these blocks is more likely to miss a conditional clause in a dense paragraph than in a broken-out list.

**Fix:** Break the structural gate (lines 97-100) into a numbered list. For the wall-of-text blocks, add blank lines between the `<check>` blocks in steps 11's dormant and unwieldy sections. The content is correct — only the formatting needs improvement.

### LOW: No config headers on prompt files

**Affected files:**
- `workflow.md` — no config header
- `workflow-runtime.md` — no config header

Neither prompt file has a `{communication_language}` config header. For a practice orchestrator that always communicates in English with a specific persona voice, this is low-impact — the voice rules effectively hardcode the communication style. However, if Momentum were ever localized, these files would need config headers.

**Impact:** Low. The voice rules and persona context effectively serve as the communication configuration. No current functional gap.

**Fix:** Consider adding a minimal config header if Momentum plans to support non-English communication. Otherwise, acceptable as-is.

### LOW: Suggestive loading at workflow.md line 34

**Affected file:** `workflow.md` line 34
**Context:** "identify and read the relevant artifact before answering"

The pre-pass flagged this as suggestive loading ("read relevant/necessary"). In context, this is within the Follow-Up Question Handling behavioral pattern and says "identify and read the relevant artifact before answering" — this is a mandatory directive ("before answering"), not a suggestion ("if needed"). The pattern continues with "Never 'Generally speaking...'" reinforcing that artifact reading is required.

**Impact:** None — this is a false positive. The instruction is mandatory, not suggestive.

**Fix:** No change needed.

### NOTE: SKILL.md suggestive loading at line 30

**Affected file:** `SKILL.md` line 30
**Context:** `<!-- HAPPY PATH — no workflow.md load, no reference file load needed -->`

Pre-pass flagged this HTML comment as suggestive loading. It's an internal design comment explaining why no file load occurs on the happy path — not an instruction to the agent. False positive.

---

## Strengths

**Happy-path latency optimization.** The SKILL.md happy path (greeting route) avoids loading workflow.md entirely by using pre-rendered greeting fields from the preflight script. This is sophisticated prompt engineering — the most common invocation path pays minimal token cost.

**Self-containment across context compaction boundaries.** Voice rules appear in SKILL.md, workflow.md, and workflow-runtime.md. Each file can function independently if the others are compacted away. This is deliberate defensive engineering, not redundancy.

**Distinctive, load-bearing persona.** The KITT/Optimus Prime persona framework is evocative and actionable. Voice rules are concrete (banned phrases, symbol vocabulary, input interpretation rules). The session-greeting templates demonstrate the persona in practice ("I hold the line", "Give the word", "The work is done"). This is the kind of persona investment that changes output quality.

**Outcome-focused behavioral patterns.** The behavioral patterns section (workflow.md lines 19-101) defines named patterns with clear triggers, not step-by-step procedures. Spec Contextualization says "surface inline: motivated disclosure + file reference + key decision" — it tells the agent WHAT to achieve, not HOW to format each character.

**Clean consent UX in install/upgrade flows.** Steps 2, 6, and 9 show what will happen, ask before acting, respect decline, and handle partial upgrade. The decline path (step 6) explicitly does not write state files and explains degraded mode. This is thoughtful orchestrator UX.

**Intelligent reference decomposition.** Six shared references handle domain-specific concerns (session greeting states, completion signal formats, progress indicator rules, spec contextualization patterns, gap detection, journal schema). Each is self-contained with its own examples and anti-patterns. The workflow steps reference them with mandatory loading directives, not suggestive "see if needed" phrasing.

**No waste detected.** Pre-pass found zero defensive padding patterns, zero back-references, and zero meta-explanation patterns across all three files. The prompt writing is clean and direct throughout.
