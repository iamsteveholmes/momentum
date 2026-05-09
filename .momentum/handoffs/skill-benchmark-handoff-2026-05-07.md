# Skill Benchmark Handoff
**Date:** 2026-05-07
**Session:** Steve Holmes + Claude Code (Sonnet 4.6 1M)
**Repo:** momentum (sprint/sprint-2026-05-03)

---

## What This Session Was

A full-day benchmarking session comparing four agent configurations across two implementation scenarios, with AVFL 3-lens quality validation on all outputs. The goal was to understand which skills produce measurably better code and under what conditions, to inform the nornspun-client dev wave.

Full analysis: `docs/analysis/skill-benchmark-analysis-2026-05-07.md`

---

## What We Learned

### The headline result

The ranking of agents reverses completely between task types:

| Agent | Narrative (Favorites) | Story (Campaign-Init) |
|---|---|---|
| compose-expert | **82/100** — best | 51/100 — worst |
| frontend-dev v2 | 66/100 | **78/100** — best |
| bmad-dev-story | 50/100 | 64/100 |
| no-skill | 29/100 — worst | 57/100 |

**compose-expert** is a knowledge/patterns skill. It excels at open-ended Compose work because it reads reference files and applies correct patterns autonomously. It fails on multi-AC stories because it doesn't track spec compliance — it missed AC10 (retry logic) entirely on Campaign-Init.

**frontend-dev** is a process skill. TDD + completion gate + project standards produce the most spec-faithful output on formal stories. On narrative work it's second because knowledge skills outperform it when there's no spec to comply with.

**bmad-dev-story** is consistently middle-of-the-pack. It follows the story well when the story tells it what to do, but has no project-specific standing knowledge (testing stack, KMP rules).

**No-skill** scores 29/100 on narrative (catastrophic structural failures) but 57/100 on story (the story itself provides enough structure). This means a well-written story is worth more than a weak skill.

### Skill scoping discovery

Skills are working-directory scoped. A skill in `nornspun-client/.claude/skills/` is only available when the working directory is nornspun-client. When orchestrating from `nornspun`, subagents see `nornspun/.claude/skills/` — not nornspun-client's.

**Confirmed via live test:** copying `frontend-dev` to `momentum/.claude/skills/` made it auto-trigger in subagents spawned from momentum. The skill was discovered and named itself in APPROACH.md without being explicitly referenced.

**For the dev wave:** `frontend-dev` needs to be in `nornspun/.claude/skills/` so orchestrator-spawned agents see it. Dev agents in worktrees see it from `nornspun-client/.claude/skills/` (already there). Both locations are needed for full coverage.

### The completion gate (frontend-dev v2)

We added three checks to the frontend-dev skill between AC-by-AC spec fidelity, scope constraint, and DoD gate. The improvement was marginal (54→52 in one comparison, 78 in the full clean run). The gate prevented the NornRadii.kt scope violation and enforced voice line constants placement. It did NOT fix the `"level"` prefix bug because the agent still verified "does test match code" rather than "does code match spec independently."

The gate is worth keeping but is not a silver bullet.

---

## What We Changed

### frontend-dev skill updated
Added `## Completion Gate` section to `nornspun-client/.claude/skills/frontend-dev/SKILL.md`:
- Scope check: never create files not listed in story tasks
- Spec fidelity check: read the AC word-for-word after tests go green
- Test coverage check: verify assertions test what the code produces, not what the test set up

The momentum copy at `momentum/.claude/skills/frontend-dev/SKILL.md` was also updated but was a temporary copy for this session's tests (see below).

### compose-expert updated
Removed the old git-cloned `compose-skill` from `~/.claude/skills/compose-skill/` and installed the proper plugin via marketplace. Now lives at `compose-expert:compose-expert` (v2.3.1).

### docs/analysis/ created
New directory for analysis documents. First resident: `skill-benchmark-analysis-2026-05-07.md`.

---

## What Was Decided

1. **Use frontend-dev for all nornspun-client story work.** It produces the best AVFL scores (78/100) on formal stories and enforces Kotest/Turbine/MVI/Channel-effects regardless of what the story says.

2. **AVFL is non-optional.** No agent scored above 82/100 on any run. Every output had meaningful issues. The AVFL fix pass is the quality gate.

3. **A well-written story matters as much as the right skill.** The story's AC11 mandate, Dev Notes, and architecture references substantially lifted even the no-skill baseline. Invest in story quality.

4. **compose-expert is best for open-ended Compose/CMP work.** Use it for UI design-to-code, animation, component library work — tasks without 11 formal ACs.

---

## What Is Unresolved

### The `"level"` prefix bug — a recurring failure class
Every agent that implemented the readback message embedded `"level"` into the test input value so the test passed without testing the format. The completion gate's fidelity check didn't catch it because the agent verified "test matches code" not "code independently matches spec." A stronger fidelity instruction — "derive the expected output from the spec alone before checking the test" — may help. Not yet validated.

### InMemoryAppPrefs placement rule missing from frontend-dev
Every agent placed `InMemoryAppPrefs` in `commonMain` instead of `commonTest` (ARCH-PREFS2 violation). The frontend-dev skill should explicitly state: "Test doubles live in `commonTest`, never `commonMain`." Not yet added.

### `@Composable` in `commonMain` interface ambiguity
`kotlin-kmp.md` prohibits all `androidx.*` imports in `commonMain`. But CMP projects legitimately use `androidx.compose.runtime.Composable` cross-platform via the CMP runtime artifact. The `ChatActions` interface pattern (using `@Composable` lambdas in commonMain) triggered a critical AVFL finding on every agent. The rule needs a documented exception or the `ChatActions` interface needs a different design.

### frontend-dev v1 vs v2 — was the completion gate worth it?
We saw mixed results: 54→52 in one comparison, but 78/100 in the clean run. The clean run was not a direct v1/v2 comparison on the same conditions — we ran v2 only. A true A/B test (same conditions, same story, v1 vs v2) was not completed. The gate is in the skill but its net effect on AVFL scores is unconfirmed.

### frontend-dev in nornspun project
The momentum copy at `momentum/.claude/skills/frontend-dev/SKILL.md` was left from testing. It should either be removed (if momentum is not the orchestrator for nornspun-client work) or kept intentionally. The canonical copy is `nornspun-client/.claude/skills/frontend-dev/SKILL.md`.

---

## What To Do Next

### Immediate
1. **Copy frontend-dev to `nornspun/.claude/skills/`** — so it auto-discovers when orchestrating from nornspun.
2. **Add InMemoryAppPrefs rule to frontend-dev** — "Test doubles live in `commonTest`, never `commonMain`."
3. **Document `@Composable` exception in `kotlin-kmp.md`** — or design the `ChatActions` interface to avoid it.
4. **Clean up `momentum/.claude/skills/frontend-dev/`** — decide whether to keep or remove.

### Follow-up
5. **Write a proper handoff doc for nornspun** — equivalent of this but oriented toward the nornspun-client dev wave.
6. **True A/B test of completion gate** — same story, v1 vs v2, same conditions, AVFL both.
7. **Strengthen spec fidelity instruction** — test the "derive from spec independently" framing and AVFL the result.

---

## Key Files Changed This Session

| File | Change |
|---|---|
| `nornspun-client/.claude/skills/frontend-dev/SKILL.md` | Added `## Completion Gate` section |
| `docs/analysis/skill-benchmark-analysis-2026-05-07.md` | New — full benchmark analysis |
| `docs/analysis/` | New directory |
| `docs/research/` | Removed 3 stale handoff docs |
| `~/.claude/skills/compose-skill/` | Deleted (replaced by compose-expert plugin) |

---

## Context for Next Session

The nornspun-client dev wave has not started yet. This session was entirely preparation and benchmarking — no production code was written to nornspun-client. The benchmark outputs are in `/tmp/benchmark/` (ephemeral — gone on next reboot).

The sprint is `sprint/sprint-2026-05-03` in the momentum repo. The nornspun sprint state is in `nornspun/.momentum/`. Campaign-init stories (`campaign-init-screen-integration`, `campaign-init-tokens-and-primitives`, etc.) are marked `done` — they were used as benchmark fixtures, not re-implemented into the actual project.
