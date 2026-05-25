# Features → Epics: The Direction (As I Understand It)

**Date:** 2026-05-23
**Purpose:** Capture the restated direction for cascade B before locking it into Decision 2. Read, correct, approve.

---

## Today: Three Overlapping Layers

Right now Momentum has three layers that all carry "what work is being done":

| Layer | File | What it is | Lifecycle |
|---|---|---|---|
| **Categorical epics** | `epics.md` (18 entries) | Long-lived thematic groupings — Foundation, Stay Oriented with Impetus, Quality Enforcement, etc. | Effectively immortal — never "done" because they're categories |
| **Features** | `features.json` (23 entries) | User-observable capabilities with closure semantics (acceptance conditions, value analysis) | Finite — each one has a definition of "done" |
| **Stories** | `stories/index.json` (410 entries) | Individual work units | Finite — each one ships and is done |

The friction: developers think about what they're delivering in terms of "what will be done when this body of work is finished." That's not the categorical-epic shape — those are categories that just keep going. So we introduced features to capture the deliverable shape. Now we maintain two parallel layers of grouping above stories, with different semantics, different write surfaces, and 269 stories that don't fit any feature.

---

## The Direction You Want

**Get rid of categorical epics. Promote features into the unified epic concept.**

| Layer | File | What it is | Lifecycle |
|---|---|---|---|
| **Epics (unified)** | (new shape, possibly still `epics.md`) | Finite-lived deliverables. Each one has acceptance conditions, value narrative, system context, and a story list. Some are user-facing capabilities; others are internal/infrastructure deliverables not visible to end users. | Finite — done means done |
| **Stories** | `stories/index.json` | Individual work units (unchanged) | Finite — each ships |

**Key shifts:**

1. **One concept, not two.** No more "is this a feature or an epic?" question. Everything that groups stories into a deliverable is an epic.
2. **Beads alignment falls out for free.** Beads' epic model is exactly the finite-lived deliverable shape — no translation needed.
3. **User-facing vs. infrastructure is a property of the epic, not a separate layer.** The flow/connection/quality taxonomy from features.json may survive as one property; some epics will simply not be user-visible at all (e.g., "Practice-ledger event-log redesign" is an internal deliverable).
4. **The "category" question gets answered differently.** If you want to ask "what's the state of UI work?" you do it by tagging or filtering across the unified epic set, not by maintaining a separate categorical layer.
5. **Done means done.** When an epic's stories are all merged and the acceptance conditions are met, the epic closes. No long-lived "Stay Oriented with Impetus" epic that's always partly in progress.

---

## Migration Shape (rough)

1. **Each of the 23 current features → becomes an epic.** Their schema (`value_analysis`, `system_context`, `acceptance_conditions`, story arrays) carries forward.
2. **The 18 categorical epics → most are dissolved.** Their stories get re-homed to either an existing (former-feature) epic or a new finite-lived epic created for that body of work.
3. **The 269 unhomed stories → each gets an epic.** New finite-lived epics may need to be created for groups of these that share a deliverable shape; some land in `ad-hoc`.
4. **`features.json` → either renamed (`epics.json`?) or its contents migrate to a restructured `epics.md`.** TBD which artifact survives — both have pros (JSON queryable, markdown human-readable).
5. **Skills that were features-aware become epic-aware.** `feature-grooming` → `epic-grooming` (the existing categorical epic-grooming gets retired; the role moves to maintain the unified epic taxonomy). `feature-breakdown` → `epic-breakdown`. Canvas's "features lens" becomes an "epics lens."
6. **`stories/index.json`'s `epic_slug` field stays.** Just points at the new unified epic concept.

---

## What Could Go Wrong (worth deciding before the cascade)

1. **Some current categorical epics may not decompose cleanly into finite-lived form.** E.g., "Stay Oriented with Impetus" is genuinely an ongoing concern, not a deliverable. The honest answer: that's a category we're choosing not to maintain explicitly anymore. If we want to know "how is the orientation experience trending?" we ask via tags or queries, not via a long-lived epic.
2. **The `ad-hoc` epic stays as a category-shaped catch-all.** Quick-fixes and one-offs don't fit the finite-lived deliverable shape. `ad-hoc` survives as the explicit "this isn't part of a planned deliverable" bucket. Fine to keep.
3. **The 269 unhomed stories need triage.** Most are probably small enough to re-home easily; some may reveal that we have planned work that was never named as a deliverable.
4. **`feature_slug` field on stories needs to become `epic_slug` (already exists).** And the existing `epic_slug` values for categorical epics need migration to their new finite-lived replacements.

---

## What Decision 2 Becomes

Decision 2's new framing:

- **D2-1: Unify the epic concept.** Drop categorical (long-lived) epics. Adopt finite-lived deliverable as the only epic shape going forward.
- **D2-2: Promote features into the unified epic concept.** Migrate features.json contents into the new epic shape; features.json archives.
- **D2-3: Migrate categorical epic contents.** Each current categorical epic's stories get re-homed to either an existing (former-feature) epic or a newly-created finite-lived epic.
- **D2-4: Skill renames.** `feature-grooming` → `epic-grooming` (replaces the categorical one). `feature-breakdown` → `epic-breakdown`. Canvas updates accordingly.
- **D2-5: Schema decision.** Whether the unified epic concept lives in `epics.md` (markdown), `epics.json` (structured), or both. Decide based on canvas/skill ergonomics.
- **D2-6: Property — user-facing vs. infrastructure.** Add an `audience: user | internal` field (or similar) to epic schema so we can distinguish without a separate layer.

---

## Implementation Cost (rough)

This is a bigger cascade than originally framed. Discovery agent E estimated 24–46 hours just for the original "retire features.json" framing. The new direction is bigger because we're also migrating 18 categorical epics + re-homing 269 stories. Plausibly 60–100 hours of focused work, parallelizable across 4–6 stories (epics? deliverables?).

The good news: the cascade halves the conceptual complexity of the practice going forward. After it lands, there's one concept where there were two.

---

## Where I Need You to Push Back

- Does "drop categorical epics entirely" feel right, or do you want some categorical residue (a small set of always-on themes for orientation)?
- Is `audience: user | internal` the right way to capture user-facing vs. infrastructure, or do you want the type taxonomy (flow/connection/quality) to do that work, or both?
- For the 269 unhomed stories: do you want to take this on as part of this cascade (slow, careful re-homing) or accept that some land in `ad-hoc` for now?
- For the schema decision (JSON vs. markdown for unified epics): preference?
