# Skill Benchmark Analysis
**Date:** 2026-05-07
**Author:** Steve Holmes (with Claude Code)

---

## Overview

A systematic benchmark comparing four agent configurations across two implementation scenarios, with AVFL 3-lens quality validation on all eight outputs. The goal was to answer: **which skills produce measurably better code, and under what conditions?**

---

## Agents Tested

| Agent | Type | Description |
|---|---|---|
| **no-skill** | Baseline | Raw model, no skill active |
| **compose-expert** | Knowledge skill | Jetpack Compose / CMP patterns, reference files, source code receipts from androidx/JetBrains |
| **frontend-dev v2** | Process skill | Project-specific: MVI, Kotest/Turbine, TDD mandate, completion gate (spec cross-check + scope constraint + DoD gate) |
| **bmad-dev-story** | Methodology skill | BMAD implementation workflow: story-driven, red-green-refactor, DoD validation gates |

---

## Scenarios

### Scenario A — Favorites Screen (narrative prompt)
Open-ended task with no formal acceptance criteria:
> "Implement a Favorites screen for a CMP app targeting Android and Desktop. SQLDelight-backed list, tap to remove, filter input at top. Stub the database."

Validated against: `kotlin-testing.md` + `kotlin-kmp.md` (standards compliance, no story spec).

### Scenario B — Campaign-Init Story (full story ACs)
Structured task with 11 formal acceptance criteria from a real Momentum story:
> `/nornspun/.momentum/stories/campaign-init-screen-integration.md`

Five-phase ViewModel state machine, hero loop, readback message construction, sentiment parser, DataStore persistence, in-voice error handling, Kotest FunSpec test suite mandated.

Validated against: story spec + `kotlin-testing.md` + `kotlin-kmp.md` + `architecture.md`.

---

## Results

### Performance

**Scenario A — Favorites**

| Agent | Time | Tokens | Tools |
|---|---|---|---|
| compose-expert | 3m 30s | 67,695 | 16 |
| frontend-dev v2 | 3m 48s | 42,533 | 14 |
| bmad-dev-story | 4m 16s | 49,490 | 18 |
| no-skill | 5m 36s | 83,678 | 39 |

**Scenario B — Campaign-Init**

| Agent | Time | Tokens | Tools |
|---|---|---|---|
| no-skill | 5m 23s | 55,145 | 9 |
| compose-expert | 5m 26s | 79,548 | 18 |
| bmad-dev-story | 5m 35s | 66,066 | 13 |
| frontend-dev v2 | 6m 7s | 65,896 | 16 |

### Quality (AVFL 3-Lens — score out of 100, higher is better)

**Scenario A — Favorites**

| Agent | Score | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|---|
| **compose-expert** | **82/100** | 0 | 1 | 2 | 4 | 7 |
| frontend-dev v2 | 66/100 | 0 | 3 | 1 | 7 | 11 |
| bmad-dev-story | 50/100 | 1 | 4 | 1 | 0 | 6 |
| no-skill | 29/100 | 2 | 4 | 2 | 3 | 11 |

**Scenario B — Campaign-Init**

| Agent | Score | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|---|
| **frontend-dev v2** | **78/100** | 0 | 1 | 3 | 5 | 9 |
| bmad-dev-story | 64/100 | 0 | 3 | 4 | 0 | 7 |
| no-skill | 57/100 | 2 | 4 | 3 | 2 | 11 |
| compose-expert | 51/100 | 1 | 3 | 2 | 4 | 10 |

---

## Key Findings

### 1. The ordering reverses between scenarios

compose-expert leads on the narrative task (82) but finishes last on the full story (51 — worse than no-skill). frontend-dev goes the opposite direction: second on narrative (66), first on the full story (78).

This is the most important result. **The right skill depends entirely on the task structure.**

### 2. Any skill beats no-skill on a narrative task by a wide margin

| | Narrative score |
|---|---|
| Best skilled agent | 82 |
| Worst skilled agent | 50 |
| No-skill baseline | 29 |

The gap between the worst skill (50) and no skill (29) is larger than the gap between the best and worst skilled agents (82 vs 50). On open-ended work, having any Compose-aware skill active dramatically improves output quality.

### 3. On a well-specified story, the skill gap narrows

| | Story score |
|---|---|
| Best skilled agent | 78 |
| Worst skilled agent | 51 |
| No-skill baseline | 57 |

No-skill actually beats compose-expert on the full story. The story's AC11 explicitly mandated Kotest FunSpec, the Dev Notes contained architectural guidance, and the Dev Agent Record documented known bugs. A well-written story provides enough structure that the base model can navigate it reasonably well — and a knowledge-only skill (compose-expert) that doesn't prioritize spec compliance can fall below the baseline.

### 4. compose-expert is a UI excellence skill, not a spec compliance skill

On the Favorites narrative, compose-expert produced the best code: `@Immutable` annotations, correct `stateIn(WhileSubscribed)` semantics, atomic design hierarchy, stateless/stateful composable split, and Compose UI tests. It read 4 reference files before writing a line of code. It scored 82/100.

On Campaign-Init, it completely missed AC10 (retry/backoff — `IN_VOICE_ERROR_MESSAGE` was defined but never wired into any retry context), left `clearPersistedJourneyState` as a no-op, and introduced `@Composable` in `commonMain`. It scored 51/100.

compose-expert knows how to build correct Compose UI. It is not designed to track spec compliance across 11 ACs.

### 5. frontend-dev's process discipline is what wins on stories

frontend-dev's 78/100 on Campaign-Init came down to three things:

- **TDD**: tests written before production code, forcing behavioral contracts to be explicit
- **Completion gate**: spec cross-check after TDD (does the output match the AC word-for-word?), scope constraint (never add files not in the story tasks), DoD gate (verify tests cover the right behaviors)
- **Project standards**: Kotest FunSpec, Channel-based effects, MVI standing rules — applied regardless of whether the story mandated them

Its one high finding (InMemoryAppPrefs in commonMain instead of commonTest) is a structural placement issue, not a functional correctness issue. The core logic was correct across all 11 ACs.

### 6. The "level" prefix bug is a recurring failure mode across all agents

Every agent (narrative and story) that implemented the readback message either:
- Typed `startingLevel` as `String` instead of `Int`, masking the missing `"level "` prefix
- Embedded `"level one"` in the test value so the test passed without testing the format

This is a class of bug that TDD cannot prevent if the test is written incorrectly in the same way as the implementation. The completion gate's spec fidelity check ("read the AC word-for-word") is the right defense — but even with the gate, the frontend-dev agent in the initial run missed it. A dedicated assertion like `readback shouldContain "level $startingLevel"` (using a bare integer) would catch it reliably.

### 7. bmad-dev-story is consistently middle-of-the-pack

bmad-dev-story scored 50/100 on Favorites and 64/100 on Campaign-Init. It follows TDD when the story mandates it, picks up Kotest from explicit AC requirements, and fixes known bugs (parser order, `\bno\b` regex) when they're documented in the story's Dev Notes. But without project-specific standing rules, it defaults to patterns that violate project standards: `androidx.lifecycle.ViewModel` base class in commonMain, InMemoryAppPrefs in production code.

Its strongest area is consistently the core logic (sentiment parser, Oxford comma, state machine) — it rarely gets the domain logic wrong. Its weakness is architecture boundary awareness.

---

## Skill-Specific Assessment

### compose-expert (aldefy/compose-skill v2.3.1)
**Strengths:**
- Highest quality on open-ended Compose work
- Reads reference files before writing code — routes symptom to specific doc
- Produces Compose UI tests (other agents often skip these)
- Correct `@Immutable`, `stateIn(WhileSubscribed)`, atomic design hierarchy
- Properly avoids `collectAsStateWithLifecycle()` in CMP commonMain

**Weaknesses:**
- No spec compliance mechanism — does not track ACs
- Drops entire ACs when they don't fit its pattern focus (AC10 retry logic)
- JUnit4 runner instead of Kotest (doesn't know project testing stack)
- Introduces `androidx.*` annotations in commonMain when it shouldn't

**Best used for:** Any Compose/CMP implementation task without a formal story spec. UI design-to-code, performance optimization, animation work, component library development.

### frontend-dev v2 (nornspun-client project skill)
**Strengths:**
- Best AVFL score on a full story (78/100)
- TDD mandate produces tests before code, forcing correct behavioral contracts
- Completion gate catches scope violations and spec-format issues
- Consistent Kotest FunSpec + Turbine regardless of story mandate
- Channel-based effects, MVI standing rules applied uniformly
- Reads actual project codebase for context (discovers existing AppPrefs, NornRadii conventions)

**Weaknesses:**
- Second on narrative tasks (66/100) — knowledge skills outperform it without a spec
- Completion gate adds overhead (~6m on Campaign-Init vs ~5m for others)
- InMemoryAppPrefs placement (commonMain vs commonTest) is a recurring miss
- Cannot prevent tests that are wrong in the same way as the implementation

**Best used for:** Any nornspun-client story with formal acceptance criteria. The skill has diminishing returns on narrative work but is the right choice for the dev wave.

**Improvement opportunity:** The `startingLevel` / `"level "` prefix bug recurred even with the completion gate. A stronger spec fidelity instruction — "derive the expected output from the spec alone before checking if the test matches" — would close this class of bug.

### bmad-dev-story
**Strengths:**
- Strong validation gates: "never mark task complete until tests exist and pass"
- Scope constraint: "never implement anything not in the story tasks"
- AC10 retry logic implemented correctly when story documents it
- Catches subtle implementation bugs (Phase 3 injection guard for duplicate hero canvases)
- Consistent across different story types

**Weaknesses:**
- Uses `androidx.lifecycle.ViewModel` base class in commonMain without project-specific guidance
- InMemoryAppPrefs in production code (ARCH-PREFS2 violation)
- journeyComplete emission value (UUID vs human-readable string)
- No project-specific testing stack knowledge (Kotest only when story mandates it)

**Best used for:** General story implementation when frontend-dev skill is unavailable. The story itself must contain all testing and architecture guidance, as bmad-dev-story does not carry project conventions.

---

## Architecture Observations

### The `androidx.*` in commonMain problem is universal

Every agent (including the baseline) violated the `kotlin-kmp.md` prohibition on `androidx.*` imports in commonMain at least once. The most common trigger is the `ChatActions` interface declaring a `@Composable` lambda parameter. This is a genuine ambiguity: Compose Multiplatform does use `androidx.compose.*` at runtime, but the project rule is written as a blanket prohibition.

**Recommendation:** Either add an explicit exception to `kotlin-kmp.md` for `androidx.compose.runtime.*` (which CMP ships cross-platform), or document an `expect/actual` pattern for the `@Composable` lambda in `ChatActions` that avoids the `androidx.*` namespace.

### InMemoryAppPrefs placement is a recurring miss

All agents that created `InMemoryAppPrefs` placed it in `commonMain` rather than `commonTest` (ARCH-PREFS2 violation). This puts a test double in production code.

**Recommendation:** Add this explicitly to the frontend-dev skill's Standing Rules or to a `.claude/rules/kotlin-kmp.md` addendum: "Test doubles (`InMemoryAppPrefs`, `FakeX`) live in `commonTest`, never `commonMain`."

### The `LaunchedEffect(currentPhase)` hero loop bug

The no-skill baseline and one other agent used `LaunchedEffect(currentPhase)` for Phase 3 hero canvas injection. This only fires once for the entire hero loop because `currentPhase` stays `PHASE_3_HEROES` for all N heroes. Correct key: `LaunchedEffect(currentPhase, heroesRemaining)`.

**Recommendation:** Add this pattern to the campaign-init architecture notes or as a `wiki-query`-able KB entry: "Phase 3 hero loop requires `LaunchedEffect(currentPhase, heroesRemaining)` — keying on phase alone silently drops heroes 2+."

---

## Benchmark Integrity Notes

1. **No-skill read the Dev Agent Record**: The no-skill baseline on Campaign-Init read the story's Dev Agent Record section, which documents post-implementation bug fixes from a prior agent (parser order, DataStore workaround). This gave the no-skill baseline knowledge of known bugs, making its Campaign-Init score (57/100) slightly inflated relative to a truly cold run.

2. **Favorites has no formal spec**: AVFL Factual Accuracy was weaker on Favorites because there are no ACs to check against. Scores are dominated by Structural Integrity and Coherence & Craft.

3. **All agents were instructed not to read existing nornspun-client source files** on Campaign-Init. This makes the comparison fair but means no agent could discover existing interfaces (AppPrefs, ChatActions) that would have resolved structural violations.

---

## Recommendations

### For the dev wave
1. **Use frontend-dev skill for all nornspun-client story work** — it produces the best AVFL scores on formal stories and enforces project standards automatically.
2. **Copy frontend-dev to nornspun/.claude/skills/** so it auto-discovers when orchestrator agents spawn dev subagents from the nornspun project.
3. **Consider compose-expert as a supplementary skill** for UI-heavy tasks (animations, component design, adaptive layouts) where spec compliance is less important than Compose pattern quality.

### For skill improvements
1. **Frontend-dev — strengthen spec fidelity check**: add instruction to "derive expected output from the spec independently before comparing to tests — do not check if test matches code, check if both match the spec."
2. **Add InMemoryAppPrefs placement rule** to frontend-dev standing rules: "Test doubles live in commonTest, never commonMain."
3. **Document the `@Composable` in ChatActions exception** in `kotlin-kmp.md` to stop the universal false positive.
4. **Add LaunchedEffect hero loop pattern** to wiki KB for the campaign-init story family.

### For process
1. **AVFL is non-optional** — no agent scored above 82/100, meaning all outputs had meaningful issues. The AVFL fix pass is the quality gate, not a nice-to-have.
2. **A well-written story is worth more than the right skill** — the story's AC11, Dev Notes, and architecture references substantially lifted the no-skill baseline. Investing in story quality (especially testing requirements and architecture references) has compounding returns across all agents.
3. **Skills and stories are complementary** — frontend-dev's process discipline combined with a well-specified story is the highest-quality combination we tested. Neither alone is sufficient.
