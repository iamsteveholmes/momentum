# Phase 6 Summary: Real-World Artifact Testing

**Date:** 2026-03-20
**Artifact:** `_bmad-output/planning-artifacts/prd.md` (pre-VFL-fix state, commit `9310b44`)
**Profile:** full (4 lenses × dual framing = 8 parallel validators)
**Iterations:** 2 (iter1: 8 parallel validators; iter2: inline — see Known Failure Mode below)
**Iter1 score:** 39/100 (20 findings: 0C, 3H, 10M, 7L)
**Iter2 result:** CLEAN (inline validation, no parallel agents)
**Total tokens:** 72,842
**Total time:** 2,378s (~39.6 minutes)

---

## Purpose

Phase 6 is the first AVFL run against a real artifact — a genuine PRD with genuine issues, not a synthetic fixture with seeded problems. The ground truth was captured by extracting the pre-fix state from git history (`git show 9310b44:file`) and diffing against the completed VFL fix commits (`git diff 9310b44..3bcbeeb`). This enables a precision/recall analysis: what did AVFL find that humans also fixed, what did AVFL miss, and what did AVFL find that humans left unfixed?

---

## Ground Truth Comparison

### What humans fixed (from `prd-ground-truth-fixes.diff`)

The human VFL pass was an **architecture-driven targeted pass** — most changes relate to a single large decision: pivoting from Claude Code plugin deployment to skills-only deployment via `npx skills add`. The specific fix categories were:

| Fix Category | Description |
|---|---|
| Install command | `npx skills add momentum` → `npx skills add momentum/momentum -a claude-code` throughout |
| FR2/FR3 decomposition | FR2 split into FR2/FR2b/FR2c; FR3 split into FR3a/FR3b/FR3c |
| FR5 clarification | Team-member joining flow disambiguated from solo first-install |
| NFR1 correction | ≤100 tokens → ≤150 characters (unit change and value change) |
| NFR4 resolution | "Blocking architecture decision" → resolved as flat-skills deployment |
| NFR7 Tier 3 validation | Incomplete validation method → explicit README documentation test |
| NFR9/10/11 | Removed "Claude Code plugin API" from ecosystem dependencies |
| J1 coverage | Global install detection marked ✓ in Journey 1 (was blank) |
| Installation Architecture diagram | Completely rewritten — ide/ → skills-only peer layout, package.json → version.md |
| Repository Structure diagram | Updated to match new peer layout |
| Deployment table | Updated to new install methods including -g global option |
| Implementation Considerations | Added installed.json commit policy; version.md version management |
| Risk table | "Plugin ecosystem" → "Agent Skills ecosystem" |
| Post-PRD Actions | Removed stale README update action |

### AVFL findings vs. ground truth

| Finding | Severity | Humans fixed? | Notes |
|---|---|---|---|
| CONSOLIDATED-001: Unsourced statistics (67.3%, 1.7x, etc.) | HIGH | No | Real issue — not in human pass scope |
| CONSOLIDATED-002: Unsourced Innovation claims (11-95%, IBM DOORS) | HIGH | No | Real issue — not in human pass scope |
| CONSOLIDATED-003: No phase tags on FRs | HIGH | No | Real issue — not in human pass scope |
| CONSOLIDATED-004: Missing derives_from for process-backlog.md | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-005: Signal=Target duplicate in Outcomes table | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-006: "Four debt types" undefined | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-007: Journey 3 web-fullstack validator not in MVP | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-008: "flywheel" undefined on first use | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-009: FR13 bundles 4-5 behaviors | MEDIUM | No | Real issue; FR3 was split by humans, not FR13 |
| CONSOLIDATED-010: FR23 bundles multiple concerns | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-011: Confidence metric has no FR for collection | MEDIUM | No | Real issue — not in human pass scope |
| CONSOLIDATED-012: NFR4 "blocking decision" unresolved | MEDIUM | **Yes** | Humans resolved NFR4 to flat-skills architecture |
| CONSOLIDATED-013: Two repo diagrams with no reconciling note | MEDIUM | **Yes** | Both diagrams completely rewritten |
| CONSOLIDATED-014: Opaque "F-06" reference | LOW | **Yes** | F-06 reference removed during NFR4 rewrite |
| CONSOLIDATED-015: Spec-driven development attribution unclear | LOW | No | Real issue — not in human pass scope |
| CONSOLIDATED-016: Journey 2 "retrospective" not in table | LOW | No | Real issue — not in human pass scope |
| CONSOLIDATED-017: Post-PRD action "original seven" assumption | LOW | **Yes** | README update action removed entirely |
| CONSOLIDATED-018: FR29 cross-story detection lacks threshold | LOW | No | Real issue — not in human pass scope |
| CONSOLIDATED-019: FR11 "may improve" — untestable | LOW | No | Real issue — not in human pass scope |
| CONSOLIDATED-020: FRs embed implementation mechanisms | LOW | No | FR20 partially rewritten, but for different reason |

**AVFL findings also fixed by humans: 4/20 (20%)**
**AVFL findings where humans and AVFL agree it's an issue:** 4

### What humans fixed that AVFL missed

| Human Fix | Why AVFL Missed It |
|---|---|
| Install command `momentum` → `momentum/momentum -a claude-code` throughout | AVFL validators don't have canonical install command knowledge; treated both as plausible |
| FR2/FR5 disambiguation (solo vs team first-install) | AVFL noted FR13/FR23 as over-bundled; didn't flag FR2 |
| FR3 decomposed into FR3a/b/c | AVFL didn't flag FR3 as bundled |
| NFR1: tokens → characters, 100 → 150 | Factual accuracy lens can't verify unit claims without ground truth |
| NFR7 Tier 3 validation underspecified | AVFL didn't flag NFR7 specifically |
| J1 global install detection coverage | AVFL didn't check Journey Requirements Summary table coverage |
| NFR9/10/11: "plugin API" dependency terminology | Requires architectural context AVFL doesn't have |
| Deployment table and Installation Architecture consistency | AVFL-013 caught the two-diagram gap but not the underlying architectural staleness |

---

## Key Findings

### 1. AVFL and human reviewers have complementary blind spots

The human VFL pass was a **targeted architectural correction** — find every place the plugin model was described and update it to skills-only. AVFL was doing a **quality audit** — find every place where evidence is missing, claims are untestable, or structure is incomplete. These are nearly orthogonal passes.

Only 4 findings overlapped. That's not a failure of either approach — it's a signal that AVFL and a focused human architectural review are additive, not substitutes.

### 2. AVFL finds real issues the human pass ignores

16 of 20 AVFL findings were real issues that humans simply didn't address in the architectural pass:
- Unsourced high-precision statistics (67.3%, 1.7x, 19%, 20%, 98%)
- Undefined load-bearing concepts (four debt types, flywheel)
- Untestable requirements (FR11, FR29, FR23)
- Missing provenance (derives_from for process-backlog.md)

These aren't false positives. They're legitimate quality gaps the human VFL didn't focus on.

### 3. AVFL misses architectural consistency issues

The install command error (`npx skills add momentum` → `npx skills add momentum/momentum -a claude-code`) appeared throughout the document. AVFL's Factual Accuracy lens didn't catch this because it requires knowing the canonical form of the command — ground truth knowledge the validators don't have unless source material explicitly provides it.

This is the key gap: **AVFL is excellent at internal consistency and structural completeness; it's poor at external correctness claims it can't verify**.

### 4. Iter2 collapsed to inline validation — known failure mode

The orchestrator correctly ran 8 parallel subagents for iteration 1, but collapsed to inline (self) validation for iteration 2. This is the second time this failure mode has been observed (Phase 5 also had iter2 inline on one run). The inline iter2 returned NO FINDINGS = CLEAN, which may be less reliable than a proper parallel run.

**Root cause hypothesis:** The orchestrator treats iter2 as "verify the fixer's work" and reasons that it can do this inline since it has the full fixer output in context. The SKILL.md instruction to "loop back to Phase 1" is not forceful enough to prevent this shortcut.

**Mitigation:** Add explicit instruction in SKILL.md: "Phase 1 in every iteration — including iteration 2+ — MUST spawn subagents. Do NOT validate inline even if the fixed document is in context."

### 5. Git history as ground truth source is viable

Extracting pre-fix artifacts via `git show <commit>:file` and capturing human fixes via `git diff <before>..<after>` produces a clean ground truth. This methodology is reusable across all planned artifact types (architecture doc, epics, brief).

---

## AVFL Precision/Recall on This Artifact

This framing requires care: the human VFL pass was not comprehensive — it was scoped to architectural corrections. A finding AVFL made that humans didn't fix is not necessarily a false positive; it may be a real issue outside the human pass scope.

With that caveat:

| Metric | Value | Note |
|---|---|---|
| AVFL findings | 20 | 3H, 10M, 7L |
| Confirmed by human fix | 4 | 20% |
| Likely real issues (not false positives) | 16+ | Humans had different scope |
| Human fixes AVFL matched | 4 of ~14 fix categories | 29% recall on human-scoped fixes |
| False positives | 0 confirmed | No finding shown to be wrong |

**AVFL generated zero confirmed false positives on a real artifact.** The calibration rules (evidence required, conservative flagging) held.

---

## Cost Profile

| Metric | Value |
|---|---|
| Total tokens | 72,842 |
| Total time | 2,378s (~39.6 min) |
| vs Phase 5 synthetic fixture | +9% tokens, +319% time |

The time inflation is anomalous — iter2 ran inline (fast) but iter1 with the full 8-agent parallel pass took significantly longer than Phase 5. Likely cause: the real PRD (578 lines) is longer than the synthetic fixture (~300 lines), and the 4-lens pass each process the full document.

---

## Next Steps

1. **Fix SKILL.md iter2 collapse:** Add explicit instruction that Phase 1 runs as subagents in all iterations
2. **More real artifacts:** Architecture doc, epics, brief — same git-history methodology
3. **Source material test:** Retry this artifact with the source documents (brief, research) as `source_material` — tests whether Factual Accuracy lens catches the unsourced statistics when citations are checkable
4. **Ground truth completeness:** A future comparison where the "human fix" is a comprehensive quality pass (not just an architectural pass) would give cleaner precision/recall
