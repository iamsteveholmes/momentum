# AVFL Fix Log — Iteration 1

**Corpus:** Gas City HITL gates and cycle orchestration research (`docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`)
**Source:** `validation/avfl-consolidated.md` (29 deduped findings, severity FAILING −18/100)
**New ground truth applied:** `raw/research-verification-probes.md` (live gc 1.4.1 probes, 2026-08-24), `raw/research-dec035-revisit-triggers.md` (new file, closes MAJ-012)
**Fixer:** AVFL Fixer pass, 2026-08-24. Fixed in severity order (critical → major → minor → low); cross-cutting adjudications A–H applied alongside individual findings where they overlapped.

Every one of the 29 findings is accounted for below as **Fixed**, **Resolved** (already addressed by new material, corpus updated to reflect it), or explicitly **Deferred**. None were dropped silently.

---

## Critical (5/5 fixed)

| ID | Change | File(s) |
|---|---|---|
| **CRIT-001** | Added `## Reliability Notice` section (untagged/untriangulated warning, refuted-claims table, citation guidance) | `raw/gemini-deep-research-output.md` |
| **CRIT-002** | Refuted-claims table entry: notify/renudge orders are 404 at every tagged release, edge-only; `gate-sweep` excludes human gates | `raw/gemini-deep-research-output.md` |
| **CRIT-003** | Refuted-claims table entry: #2311 is OPEN and unrelated (barrier bug, not data-loss); #3200 uncorroborated | `raw/gemini-deep-research-output.md` |
| **CRIT-004** | Full re-derivation per adjudication A: `GC_BEADS=file` exists and boots (Probe 1), but the entire `gc bd` verb family (`bd gate create`, `--set-metadata`) is unconditionally blocked on it (Probes 2–3). Struck the false "no GC_BEADS=file" negative in gate-mechanics; re-derived beads-coupling's Bottom Line, §2, §7 "Forced: nothing," §8; corrected the exec-step false premises this same claim fed in hitl-alternative-patterns | `raw/research-gate-mechanics-handson.md`, `raw/research-beads-coupling-dec028.md`, `raw/research-hitl-alternative-patterns.md` |
| **CRIT-005** | Corrected per adjudication C: no `exec`/`command`/`run`/`script` step key in v2 formulas. Replaced with real constructs — work-step `description_file` instructing the claiming agent to run `bd gate create`, or order-level `exec` (300s cap, no agent) — and fixed `--blocks` to resolve to the downstream step's bead id (cook-time discovery via `gc.root_bead_id`/`gc.step_ref`), not the gate-creating step's own id | `raw/research-hitl-alternative-patterns.md` (§2 practical implication, §7(b) concrete shape), `raw/research-gate-mechanics-handson.md` (Design consequence paragraph) |

## Major (15/15 fixed or resolved)

| ID | Change | File(s) |
|---|---|---|
| **MAJ-001** | Refuted-claims table: v1.4.0-as-current corrected to v1.4.1 (2026-08-15) | `raw/gemini-deep-research-output.md` |
| **MAJ-002** | Refuted-claims table: dashboard is compiled into `gc` binary, port 8372 (not React/Node/8082), no gate view — corroborated by live Probe 4 | `raw/gemini-deep-research-output.md` |
| **MAJ-003** | Refuted-claims table: #2131/#2168 attributed to v1.2.0 (2026-05-29), not v1.4.0 | `raw/gemini-deep-research-output.md` |
| **MAJ-004** | Query-method annotation added everywhere the 575 vs 1,011 figures appear: 575 = search-API `is:issue is:open` (issues only); 1,011 = `open_issues_count` repo endpoint (issues + PRs) | `raw/research-maturity-open-bugs.md`, `raw/research-notification-watcher-layer.md`, `raw/research-production-evidence.md` (Finding 7) |
| **MAJ-005** | Stripped incorrect `packs/` prefix from 4 citations (2 in Finding 1, 2 in Finding 3); underlying evidence was sound, only paths were wrong | `raw/research-production-evidence.md` |
| **MAJ-006** | Added missing Gate 2 row (`discovered-from`/intake-queue toil) to the DEC-028 re-score table, scored Neutral — Gas City adoption doesn't touch it | `raw/research-beads-coupling-dec028.md` §7 |
| **MAJ-007** | Resolved by Probe 2: FileStore.SetMetadata **is** durable (not a no-op), but moot — no CLI verb writes arbitrary metadata on a file-backed city in gc 1.4.1. Updated §8 (removed `[UNVERIFIED]` framing) and cross-referenced from the new §2 caveat | `raw/research-beads-coupling-dec028.md` §2, §8 |
| **MAJ-008** | Resolved by Probe 5: v1.2.2 (v1.4.1 tag) and v1.1.0 (`main`) are both correct for different refs — `main` deliberately downgraded BD_VERSION pending an upstream CAS-flag release. Documented both with refs | `raw/research-beads-coupling-dec028.md` §6 |
| **MAJ-009** | Corrected: the close-bypass transcript (`gt-bvw`/`gt-2zt`) is from the timer-gate probe, not the human-gate probe (`gt-b3e`/`gt-crp`). Noted the underlying claim is gate-type-agnostic and stands regardless | `raw/research-gate-mechanics-handson.md` Q2 bonus finding |
| **MAJ-010** | Downgraded `interaction_mode` from "forbids/enforces" framing to "the shipped packs' prompt convention" — it is prose read by the LLM, not a compiled control-flow gate. Noted Momentum-authored packs set their own mode prose | `raw/research-hitl-alternative-patterns.md` §4 |
| **MAJ-011** | Corrected "costs nothing" to "costs the notification path" — formula gates persist `await_type: null`, both bundled notify reflexes filter on `await_type == "human"`, so a formula-cooked human gate blocks correctly and notifies nobody | `raw/research-human-verdict-patterns.md` §5, `raw/research-maturity-open-bugs.md` |
| **MAJ-012** | **Resolved.** `raw/research-dec035-revisit-triggers.md` (new file, already written) closes the coverage gap — scores both DEC-035 revisit triggers against the corpus. Added as 9th sub-question in `scope.md` so the corpus's own index reflects it | `scope.md` |
| **MAJ-013** | Addressed per adjudication B (no wholesale rewrite): body marked as raw unstructured extraction in the Reliability Notice; the Notice + corrected Follow-Up/Sources sections are the citable parts of the file going forward | `raw/gemini-deep-research-output.md` |
| **MAJ-014** | Added rewrite-scope estimate (15–25 days, on top of the 6–9 day gate-glue estimate) to §9, sized against the five methodology packs (bmad/gascity/superpowers/gstack/pr-pipeline) that walked this path | `raw/research-cycle-orchestration-fit.md` §9 |
| **MAJ-015** | Re-derived "Forced: nothing" — the exec-order premise (`claude -p` subprocess) doesn't exist; under the actual pack/formula-step shape, Momentum's phase work becomes city beads. Combined with CRIT-004, the conclusion changes from "forced: nothing" to "forced: a scoped, city-local Dolt requirement for the gate primitive" | `raw/research-beads-coupling-dec028.md` §7 |

## Minor (7/7 fixed)

| ID | Change | File(s) |
|---|---|---|
| **MIN-001** | Refuted-claims table: beads#1467 is unrelated (closed 2026-02-03, different subject); corpus's actual tracker is gascity#4399 | `raw/gemini-deep-research-output.md` |
| **MIN-002** | Filled in `§2` for the v2 spec citation (Compilation, where gate synthesis lives); replaced the milestone ellipsis with a concrete search URL (`.../milestones?q=1.5`) rather than guess an unconfirmed numeric id, and added it to Sources | `raw/research-human-verdict-patterns.md` §5, `raw/research-maturity-open-bugs.md` |
| **MIN-003** | Refuted-claims table: split the fused "Dolt ≥2.1.0 because pre-1.86.2 lacks fixes" sentence — 2.1.0 is v1.2.1's managed-Dolt floor; pre-1.86.2 is a separate, older caveat | `raw/gemini-deep-research-output.md` |
| **MIN-004** | Standardized create-vs-check framing: added a note to the 5-row gate-type table (hitl-alternative-patterns) clarifying `bead` is check-only, not creatable; added an equivalent note to the 4-row create-side listing (human-verdict-patterns) clarifying it's a subset. `research-maturity-open-bugs.md` already drew the distinction correctly — left as-is (it's the file the others are aligned to) | `raw/research-hitl-alternative-patterns.md` §2, `raw/research-human-verdict-patterns.md` §5 |
| **MIN-005** | Added a corpus-level environment note to all 4 files that stated "gc not installed on this machine" — the original claim was true for each sub-question's *own* session (2026-08-21); a later probe session (2026-08-24) installed gc 1.4.1 globally, but each file's specific untested claim is re-scoped individually (some remain genuinely open, e.g. multi-hour session survival; others are now resolved, e.g. GC_BEADS=file existence) | `raw/research-cycle-orchestration-fit.md`, `raw/research-notification-watcher-layer.md`, `raw/research-human-verdict-patterns.md`, `raw/research-beads-coupling-dec028.md` |
| **MIN-006** | Aligned the per-fork verdict vocabulary (`adopt\|change\|reject` → `approve\|modify\|remove`) to `plan-gate-renderer.md`'s actual source vocabulary. `research-notification-watcher-layer.md`'s top-level "Approve / Modify / Re-run AVFL" already matched the renderer and needed no change | `raw/research-human-verdict-patterns.md` §8 |
| **MIN-007** | Standardized the reference-implementation line count to 222 (matching the more specific, closer-read citation) in both places it appeared | `raw/research-notification-watcher-layer.md` |

## Low (2/2 fixed)

| ID | Change | File(s) |
|---|---|---|
| **LOW-001** | Softened "no `await_type` key at all" to "persists a null `await_type`" — the shown `jq` transcript cannot distinguish key-absent from key-present-null, and the downstream argument doesn't depend on which | `raw/research-gate-mechanics-handson.md` |
| **LOW-002** | Flagged the 1,783-fork citation as secondary/gameable per the file's own stated methodology; noted the directional conclusion doesn't depend on it | `raw/research-production-evidence.md` Finding 7 |

## Resolved during validation (not scored, no action needed)

| ID | Status |
|---|---|
| **RESOLVED-001** (Q3 empty section) | Already repaired before this fix pass began, per team-lead instruction. No action taken. |

---

## Cross-cutting adjudications applied beyond the 29 scored findings

These were called out explicitly in the fix-pass brief as required alongside the findings above:

- **Adjudication D (deps.env, folded into MAJ-008):** both `v1.2.2` and `v1.1.0` are correct for different refs (v1.4.1 tag vs. current `main`, respectively) — documented with the full explanation (upstream CAS-flag capability gap) in both files that cite a `BD_VERSION`.
- **Adjudication F ([EMPIRICAL] tag):** added an "Evidence notation note" section to `scope.md` defining `[EMPIRICAL]` as the corpus's fourth evidence tag. Per the brief, did **not** edit the `momentum:research` skill itself — recorded here that a skill-level template fix (adding `[EMPIRICAL]` as a first-class tag) should be routed through Momentum's `momentum:upstream-fix` process separately.
- **Adjudication G (missing analyses):** added two new sections to `research-cycle-orchestration-fit.md` — §9a "What happens when a gate is never resolved" (DOMAIN-A-009, unresolved-gate failure mode: order-skip + no timeout + no notification = silent permanent stall; prescribes an external `bd gate list --status open` liveness sweep) and §9b "Push/merge authority under out-of-session orchestration" (DOMAIN-A-011: git-discipline's push-approval rule and version-on-release's mandatory push imply a fifth gate, or an explicit statement that the cycle terminates before push).
- **Four-vs-five provider count** (part of the adjudication H catch-all, no individual finding ID but explicitly named in the brief): corrected `research-beads-coupling-dec028.md` §1's "four implementations" to "five," matching its own 5-row table (BdStore, NativeDoltStore, FileStore, MemStore, exec.Store).

---

## Summary

- **29/29 findings accounted for** — 28 fixed by direct edit, 1 (MAJ-012) resolved by a pre-existing new file plus a scope.md index update.
- **0 findings could not be fixed.**
- **9 files edited:** all 8 `research-*.md` files, `gemini-deep-research-output.md`, and `scope.md`.
- **1 deferred item, explicitly scoped down-stream, not up to this fix pass:** the `[EMPIRICAL]` tag is corpus-documented (scope.md) but the underlying `momentum:research` skill template was not touched — that is a skill-level change requiring `momentum:upstream-fix`, out of scope for a corpus fix pass.
