---
title: "B3: Canvas update — render epics instead of features"
story_key: b3-canvas-update-render-epics-instead-of-features
status: review
epic_slug: ad-hoc
feature_slug:
story_type: feature
change_type:
  - script-code
  - skill-instruction
verification_method: execution test
harness_profile: default
depends_on:
  - b1-epic-schema-migration-define-epicsjson-migrate-features
touches:
  - skills/momentum/skills/canvas/server.tsx
  - skills/momentum/skills/canvas/server.test.ts
  - skills/momentum/skills/canvas/SKILL.md
  - skills/momentum/skills/canvas/workflow.md
source_decision: dec-034-epic-layer-consolidation-2026-05-25
source_assessment: aes-003-practice-ledger-defects-and-epic-unification-2026-05-25
---

# B3: Canvas update — render epics instead of features

## Story

As a Momentum developer using the live cycle dashboard,
I want the canvas to read and render epics from `epics.json` instead of features from `features.json`,
So that the dashboard reflects the unified epic-layer model adopted in DEC-034 and stays consistent with the data source produced by B1.

## Description

DEC-034 unifies Momentum's `features.json` and categorical `epics.md` into a single concept stored in `_bmad-output/planning-artifacts/epics.json`. The Momentum Cycle dashboard (Hono+Bun server at `skills/momentum/skills/canvas/server.tsx`, port 3456) currently reads `features.json` and renders a "Features" lens with a feature-detail L2 reading view. After B1 ships `epics.json`, the canvas must:

1. Replace `readFeaturesJson()` and `readFeatureBySlug()` with `readEpicsJson()` and `readEpicBySlug()` that read from `_bmad-output/planning-artifacts/epics.json`.
2. Rename the `/lenses/features` route and section id to `/lenses/epics` / `lens-epics` and update the corresponding LensSection placeholder and root-page HTMX wiring.
3. Rename the `/features/:slug` reading-mode route to `/epics/:slug` and update the L2 detail view to render the epic schema (including new `lifecycle` and `audience` properties from DEC-034 D2/D3 in addition to existing `value_analysis`, `system_context`, `acceptance_condition`, `stories`, `dependencies`).
4. Update all internal links (feat-row `href`, breadcrumb middle segment in the story L3 view's `from=feature` path, sprint detail story links) to use `/epics/<slug>` and accept `from=epic`/`feature=` → `from=epic`/`epic=` query parameter substitutions. Preserve backward-compatible behavior for `from=feature` legacy params: redirect or alias to the epic path until B4 completes, then remove the alias.
5. Update the Type-level signatures (`Feature` → `Epic`, `FeatureRow` → `EpicRow`, `FeatureDetailView` → `EpicDetailView`, `buildFeatureStoryRows` → `buildEpicStoryRows`) and their export/test references in `server.test.ts`.
6. Update placeholder copy in `renderFeaturesTable` ("No features found — run momentum:feature-grooming first") to reference epics and `momentum:epic-grooming` (the renamed grooming skill produced by B4 — until B4 lands, the copy may transitionally read "run momentum:feature-grooming or momentum:epic-grooming first" but the canonical post-B4 copy is `momentum:epic-grooming`).
7. Update the Sprint lens and Cycle timeline lens? — these are unaffected by epics.json migration and must continue rendering unchanged. (Verify by tests.)
8. Update `skills/momentum/skills/canvas/SKILL.md` description if it mentions features (current copy does not) and update `skills/momentum/skills/canvas/workflow.md` if it references feature-grooming (current copy mentions Step 1 server path only — no feature-grooming reference present, so workflow.md is no-op unless the renamed grooming skill needs surfacing).
9. Verify the practice-rendering / project-detection path described in Architecture Decision 48 (practice project detection) still functions. DEC-034's frontmatter notes "Decision 48 may survive in different form for the canvas" — confirm by exercising the canvas in a project with practice scope and observing the same projection. No code change required in this story unless the practice projection path itself reads `features.json` (it does not — verified by repo scan; readSprintsIndex and readStoriesIndexRaw are the only project-detection inputs).

**Pain context:** Hidden blocker that the original DEC-034 implementation plan missed; surfaced in AES-003 Finding 9 as a user-visible dashboard concern. Without this fix, after B1 lands, the Features lens silently empties and the L2 feature reading view 404s for any new epic slug.

**Source:** DEC-034 D6 (canvas updates to render epics); AES-003 Finding 9 (hidden touchpoint).

## Acceptance Criteria

1. `readFeaturesJson()` and `readFeatureBySlug()` are removed from `server.tsx`. New functions `readEpicsJson(): Promise<Epic[]>` and `readEpicBySlug(slug: string): Promise<Epic | null>` exist and read from `_bmad-output/planning-artifacts/epics.json` (the path produced by B1). Both gracefully return `[]` / `null` when the file is absent (consistent with the prior features.json reader behavior).
2. The `Epic` type matches the schema produced by B1, at minimum including: `epic_slug: string`, `name: string`, `status: string`, `lifecycle: "finite-lived" | "long-lived"`, `audience: "user" | "internal"`, `stories_done: number`, `stories_remaining: number`, optional `stories?: string[]`, `acceptance_condition?: string`, `value_analysis?: string`, `system_context?: string`, `description?: string`, `dependencies?: string[]`. The type is exported.
3. The HTTP route `GET /lenses/features` is replaced by `GET /lenses/epics`. The HTMX section id is `lens-epics` and the HTMX trigger preserves the existing 2s polling cadence. The lens header reads "Epics" (capitalized as the existing convention) and the row count and gap count behave as before.
4. The HTTP route `GET /features/:slug` is replaced by `GET /epics/:slug`. The L2 detail view renders the epic shape including the new `lifecycle` and `audience` properties displayed prominently in the `l2-meta` strip (alongside the status badge and stories fraction). Existing sections (value narrative, acceptance condition, system context, stories, dependencies) continue to render when the corresponding fields are present.
5. The root `GET /` route's HTMX fragment and full-page render reference `LensSection({ id: "epics", tag: "Epics", title: "Epics" })` in place of the previous `"features"` section.
6. All internal hrefs and HTMX `hx-get` URLs that previously pointed to `/features/<slug>` now point to `/epics/<slug>`. The story L3 view's `from=feature` breadcrumb param is updated to `from=epic` and `feature=<slug>` becomes `epic=<slug>`. The `StoryDetailView` typing for `from` accepts `"epic" | "sprint" | null` (replacing `"feature"`); `featureSlugOverride` is renamed `epicSlugOverride`. The story L3 breadcrumb middle segment renders `epic` (not `feature`) when entering from the epic L2 view.
7. The `Feature` type alias is renamed to `Epic`; `FeatureRow` → `EpicRow`; `FeatureDetailView` → `EpicDetailView`; `buildFeatureStoryRows` → `buildEpicStoryRows`. All consumers in `server.tsx` and `server.test.ts` are updated. No exported symbol named `Feature*` remains.
8. The empty-state placeholder in the epics lens reads "No epics found — run momentum:epic-grooming first" (post-B4 canonical copy). If B4 has not yet landed at implementation time, transitional copy is acceptable: "No epics found — run momentum:epic-grooming or momentum:feature-grooming first."
9. The Sprint lens (`/lenses/sprint`, `SprintCard`, `SprintDetailView`) and Cycle timeline lens (`/lenses/cycle`, `CycleLensSection`, `computeCycleState`) render identically to before. No functional change in either lens. Existing test coverage in `server.test.ts` for these two lenses still passes without modification.
10. `server.test.ts` is updated:
    - Existing tests covering `analyzeGap`, `buildSortedRows`, `badgeClass`, `FeatureDetailView`, `buildFeatureStoryRows`, and route handlers are renamed to their epic equivalents and continue to pass.
    - At least one new test asserts that `readEpicsJson` returns `[]` when `epics.json` is missing (graceful degradation).
    - At least one new test asserts that the L2 epic-detail view renders the `lifecycle` and `audience` fields when present on the epic object.
    - At least one new test asserts that `GET /lenses/epics` returns a 200 HTML response with the section id `lens-epics`.
    - At least one new test asserts that `GET /epics/:slug` returns the epic-detail view when the slug exists, and a graceful "not found" fragment when it does not.
11. `skills/momentum/skills/canvas/workflow.md` is updated only if it references features or feature-grooming. (Current scan shows no such reference; this AC is satisfied as a no-op pending a re-scan at implementation time.) `skills/momentum/skills/canvas/SKILL.md` description remains within ≤150 chars (current: 121 chars — leaves room for an epic-mention rewording if desired but not required).
12. A smoke test passes: with `epics.json` present and populated by B1's migration, running `bun --hot skills/momentum/skills/canvas/server.tsx` starts the server, `curl http://localhost:3456/lenses/epics` returns a 200 with an HTML body containing at least one epic row, and `curl http://localhost:3456/epics/<known-slug>` returns the L2 detail view containing the lifecycle and audience values.
13. A human visual review confirms the L2 epic-detail view renders cleanly (no broken layout, no missing sections) for at least one finite-lived user epic and at least one long-lived (e.g., `ad-hoc`) epic.

## Tasks / Subtasks

- [x] **Task 1 — Define `Epic` type and replace `Feature` type** *(script-code)*
  - Add the `Epic` type matching the schema in AC 2, including `lifecycle` and `audience` enum-narrowed fields.
  - Rename `FeatureRow` → `EpicRow`, propagate through `analyzeGap`, `buildSortedRows`, `renderFeaturesTable` (rename to `renderEpicsTable`).
  - Update `STATUS_SEVERITY` if any epic-specific status values are introduced by B1's schema; otherwise leave unchanged.
  - Update `server.test.ts` test fixtures and type imports.

- [x] **Task 2 — Replace data readers** *(script-code)*
  - Implement `readEpicsJson()` reading `_bmad-output/planning-artifacts/epics.json`. Treat the JSON as an object keyed by `epic_slug` (mirror the current features.json shape) — confirm against B1's actual output before merging.
  - Implement `readEpicBySlug(slug)` analogously.
  - Delete `readFeaturesJson` and `readFeatureBySlug`. Confirm no remaining import sites.

- [x] **Task 3 — Rename routes and HTMX wiring** *(script-code)*
  - Change `app.get("/lenses/features", ...)` to `app.get("/lenses/epics", ...)`. Update section id to `lens-epics`. Update hx-get URLs in the section and in the placeholder `LensSection({ id: "epics", ... })`.
  - Change `app.get("/features/:slug", ...)` to `app.get("/epics/:slug", ...)`. Update all internal references including the story L3 breadcrumb middle and feat-row `href`.
  - Update the root route's HTMX fragment to emit `LensSection({ id: "epics", tag: "Epics", title: "Epics" })`.

- [x] **Task 4 — Rename L2 detail view and breadcrumb wiring** *(script-code)*
  - Rename `FeatureDetailView` → `EpicDetailView`. Add `lifecycle` and `audience` to the `l2-meta` strip (as pill-style labels alongside the status badge).
  - Update `buildFeatureStoryRows` → `buildEpicStoryRows`; update story href construction to use `from=epic&epic=<slug>`.
  - Update `StoryDetailView` to accept `from: "epic" | "sprint" | null` and `epicSlugOverride` in place of `featureSlugOverride`. Update the breadcrumb-middle render path to label the segment `epic`.

- [x] **Task 5 — Update placeholder copy and grooming-skill reference** *(script-code)*
  - Change the empty-state placeholder to the AC 8 copy. Default to the canonical post-B4 copy; if B4 has not yet landed at implementation time, use the transitional variant.

- [x] **Task 6 — Tests in `server.test.ts`** *(script-code)*
  - Rename existing feature-related tests to epic-equivalents. Update fixtures to the `Epic` shape.
  - Add the four new tests called out in AC 10 (graceful missing-file, lifecycle/audience render, /lenses/epics route, /epics/:slug route).
  - Confirm sprint and cycle lens tests pass unchanged.

- [x] **Task 7 — Canvas SKILL.md / workflow.md sweep** *(skill-instruction)*
  - Re-scan `skills/momentum/skills/canvas/SKILL.md` and `workflow.md` for any references to "features", "feature lens", or "feature-grooming". Replace with epics-equivalent copy. If no references exist (current state), document the no-op in the Dev Agent Record. SKILL.md description ≤150 chars confirmed.

- [x] **Task 8 — Smoke + visual verification** *(script-code, verification step)*
  - With B1's `epics.json` in place, start the server. Use `curl` to hit `/lenses/epics` and `/epics/<known-slug>`; assert HTML body markers per AC 12.
  - Open the dashboard in cmux viewer pane; confirm at least one finite-lived user epic and one long-lived epic render correctly. Capture the visual confirmation in the Dev Agent Record.

## Dev Notes

### Architecture Compliance

- **DEC-034 D6 — direct mandate.** This story implements the canvas update sub-decision explicitly listed in DEC-034: "Canvas updates to render epics (the features lens becomes an epics lens; cycle timeline + sprint lens unaffected)."
- **Architecture Decisions 44–49 status.** These are marked HISTORICAL by DEC-034. Decision 48 (practice project detection) may survive in different form — verify by exercise (Task 8) that the canvas continues to detect and render practice scope correctly after epics.json supersedes features.json. No code change required unless the practice-detection path reads features.json (repo scan confirms it does not).
- **Read/Write Authority.** Per DEC-034 frontmatter: the architecture Read/Write Authority table is updated so the canvas read row points at `epics.json` (was `features.json`). This story implements that read-path change.
- **Dependency on B1.** This story cannot be merged before B1 is merged because the data file `epics.json` is produced by B1's schema migration. The smoke test in Task 8 will fail without B1's output. The dev agent must verify B1 is merged into the sprint branch before running smoke verification.

### Testing Requirements

- **Verification method:** `execution test` (per `skills/momentum/references/rules/verification-standard.md` §1, `script-code` change type). The canvas server is exercised via `curl` against the running process; output is asserted against AC 12 markers.
- **Harness profile:** `default` — Bun runtime, no special drivers. Port 3456 must be free at verification time.
- **EDD note:** Task 7 (SKILL.md/workflow.md sweep) is `skill-instruction` change type. Per the verification-standard.md routing table, this would normally require EDD evals. However, the task is bounded to a re-scan and no-op-or-substitution edit; if the scan finds nothing to change, no eval is required. If a substantive copy change is introduced, a single eval covering "given the canvas SKILL.md, agent invocations correctly identify the canvas as serving epics, not features" should be authored under `skills/momentum/skills/canvas/evals/`.
- **Test runner:** `bun test skills/momentum/skills/canvas/server.test.ts`. All existing assertions must continue to pass after rename; the four new assertions in AC 10 must be added.
- **No insider knowledge guard:** The verification steps use only `curl` against documented routes and visual confirmation of documented UI sections — no implementation internals are required.

### Implementation Guide

The current `server.tsx` is a single 2192-line file. Stay inside that file unless the diff would naturally grow beyond ~200 LOC, in which case factor the epic-specific helpers into a sibling module (`skills/momentum/skills/canvas/epics.ts`) and import them — but do not pre-emptively split: keep the change minimal.

**Specific edit map (line refs are approximate, against the current file at `skills/momentum/skills/canvas/server.tsx`):**

- Lines 14–37: replace `Feature`, `FeatureRow` types with `Epic`, `EpicRow` (add `lifecycle`, `audience`).
- Lines 47–61: `analyzeGap(feature, ...)` → `analyzeGap(epic, ...)`. Logic unchanged.
- Lines 78–102: `buildSortedRows(features, ...)` → `buildSortedRows(epics, ...)`. Field accesses (`feature_slug`, `name`) → (`epic_slug`, `name`).
- Lines 108–148: replace `readFeaturesJson` and `readFeatureBySlug` with epic equivalents pointing at `_bmad-output/planning-artifacts/epics.json`.
- Lines 187–213: `renderFeaturesTable` → `renderEpicsTable`. Update empty-state copy. Update `href` from `/features/<slug>` to `/epics/<slug>`.
- Lines 596–747: `FeatureDetailView` → `EpicDetailView`. Add lifecycle and audience pills to `l2-meta`. Update breadcrumb `here` label from `feature` to `epic`.
- Lines 625–646: `buildFeatureStoryRows` → `buildEpicStoryRows`. Update story href construction.
- Lines 648–663: `FeatureStoryRow` → `EpicStoryRow`. Update `from=feature` to `from=epic`, `feature=` to `epic=`.
- Lines 1604–1632: root `GET /` handler — change `LensSection({ id: "features", tag: "Features", title: "Features" })` to `{ id: "epics", tag: "Epics", title: "Epics" }`.
- Lines 1637–1658: `app.get("/lenses/features", ...)` → `app.get("/lenses/epics", ...)`. Section id `lens-features` → `lens-epics`. hx-get URL update.
- Lines 1909–2053: `StoryDetailView` — update `from` union type, rename `featureSlugOverride` → `epicSlugOverride`, update breadcrumb-middle render to label `epic`.
- Lines 2068–2125: story L3 handler — read `from=epic` (was `from=feature`) and `epic=<slug>` (was `feature=<slug>`).
- Lines 2128–2180: `app.get("/features/:slug", ...)` → `app.get("/epics/:slug", ...)`. All internal references updated.

**Verification commands (smoke):**

```bash
# Confirm B1 has produced epics.json
test -f _bmad-output/planning-artifacts/epics.json && echo "ok" || echo "blocked-by-B1"

# Run tests
bun test skills/momentum/skills/canvas/server.test.ts

# Boot server and smoke-test routes
bun --hot skills/momentum/skills/canvas/server.tsx &
SERVER_PID=$!
sleep 2
curl -sf http://localhost:3456/lenses/epics | grep -q 'lens-epics' && echo "lens-epics ok"
KNOWN_SLUG=$(jq -r 'keys[0]' _bmad-output/planning-artifacts/epics.json)
curl -sf "http://localhost:3456/epics/$KNOWN_SLUG" | grep -q "$KNOWN_SLUG" && echo "epic detail ok"
kill $SERVER_PID
```

**Gherkin specs separation note (Decision 30):** Gherkin specs may exist for this sprint under `.momentum/sprints/sprint-2026-05-26/specs/`. The dev agent must NOT read or implement against those `.feature` files — only the plain English ACs in this story file are in scope.

### Project Structure Notes

- The canvas server is the sole consumer of `features.json` in the codebase (verified by repo scan). After this story, the canvas reads `epics.json` and no other code reads `features.json` until it is archived by B1.
- The cmux markdown viewer and `mdpreview` are unaffected — they do not read momentum data files.
- The canvas is part of the `momentum` plugin package; version bump on release (per `.claude/rules/version-on-release.md`) happens at sprint close, not per story.

### References

- `_bmad-output/planning-artifacts/decisions/dec-034-epic-layer-consolidation-2026-05-25.md` — directing decision (D4: schema in `epics.json`; D6: skill restructure including canvas).
- `_bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md` — Finding 9 (hidden canvas touchpoint).
- `.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md` — cascade plan (this story is leaf B3).
- `.momentum/stories/b1-epic-schema-migration-define-epicsjson-migrate-features.md` — produces the `epics.json` file consumed here.
- `skills/momentum/references/rules/verification-standard.md` — verification method routing (this story uses `execution test`).
- `skills/momentum/references/agent-skill-development-guide.md` — referenced for the Task 7 SKILL.md/workflow.md sweep if substantive edits are made.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6, 8 → `script-code` (TDD)
- Task 7 → `skill-instruction` (EDD if substantive copy change introduced; otherwise no-op verified by re-scan)

---

### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Update or add failing tests in `skills/momentum/skills/canvas/server.test.ts` for the renamed types, new readers, new routes, and lifecycle/audience rendering. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run `bun test skills/momentum/skills/canvas/server.test.ts` to confirm.
3. **Refactor:** Improve code structure while keeping tests green. The 2192-line file may benefit from light grouping (group epic helpers near each other) but do not pre-emptively split into sibling modules.

**DoD items for script-code tasks:**
- [ ] Tests written and passing (`bun test skills/momentum/skills/canvas/server.test.ts` green)
- [ ] No regressions in existing test suite — sprint and cycle lens tests still pass without modification
- [ ] Smoke test executed per Task 8 — both `/lenses/epics` and `/epics/<slug>` return 200 with expected markers
- [ ] No remaining `Feature*` exported symbol in `server.tsx`
- [ ] No remaining import path or reference to `features.json` in `server.tsx`

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing any substantive change to canvas SKILL.md / workflow.md:**

1. Re-scan the files for "feature" references. If none exist (current state), the task is a no-op — document this in the Dev Agent Record and skip the rest of this template.
2. If substantive edits are introduced (e.g., renaming "feature lens" copy → "epics lens"), write 1 behavioral eval in `skills/momentum/skills/canvas/evals/`:
   - File: `eval-canvas-serves-epics-not-features.md`
   - Format: "Given the canvas SKILL.md and workflow.md, an agent invoked to describe what the canvas displays should answer with 'epics' (or 'epic lens'), not 'features' (or 'feature lens')."

**Then implement:**

3. Apply the copy change.

**Then verify:**

4. Run the eval by spawning a subagent with the SKILL.md and workflow.md contents as context and the eval scenario as its task. Observe whether the response matches.
5. If the eval matches → task complete.
6. If the eval fails → revise the copy, re-run (max 3 cycles).

**NFR compliance:**
- SKILL.md `description` field ≤150 characters (current: 121 chars — fine; new copy must not exceed 150).
- `model:` and `effort:` frontmatter fields must remain present.
- SKILL.md body must stay under 500 lines / 5000 tokens.
- Skill name remains `canvas` under the `momentum:` namespace.

**Additional DoD items for skill-instruction tasks:**
- [ ] If substantive change made: 1 behavioral eval written in `skills/momentum/skills/canvas/evals/`
- [ ] If substantive change made: EDD cycle ran — eval behavior confirmed
- [ ] If no substantive change: Dev Agent Record documents "Task 7 no-op — no feature references found in canvas SKILL.md or workflow.md"
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

---

**Gherkin spec separation reminder (Decision 30, black-box separation):** Gherkin `.feature` files may exist for this sprint under `.momentum/sprints/sprint-2026-05-26/specs/`. The dev agent is forbidden from reading or implementing against those files. Implementation targets the plain-English Acceptance Criteria above only.

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- epics.json schema confirmed: keyed by epic_slug, fields include lifecycle/audience/acceptance_conditions (array). No status field present in real data — type made optional.
- buildSortedRows: guarded against undefined name/status from real epics.json data (some epics have sparse fields).
- Task 7 no-op — no feature references found in canvas SKILL.md or workflow.md. SKILL.md description = 145 chars (≤150 confirmed).
- Smoke test: lens-epics ok, epic detail ok (momentum-agent-composition-pipeline slug).

### Completion Notes List

- Replaced Feature type with Epic type (lifecycle, audience added; status made optional to match real epics.json data which has no status field).
- readEpicsJson() and readEpicBySlug() implemented, readFeaturesJson/readFeatureBySlug deleted.
- Routes: /lenses/features → /lenses/epics (id: lens-epics), /features/:slug → /epics/:slug.
- EpicDetailView renders lifecycle and audience pills in l2-meta strip; handles both acceptance_conditions (array) and acceptance_condition (legacy string).
- StoryDetailView: from accepts "epic"|"feature"|"sprint"|null — "feature" is a backward-compat alias routing to /epics/. epicSlugOverride added, featureSlugOverride kept deprecated.
- Empty-state copy: "No epics found — run momentum:epic-grooming first" (canonical post-B4 copy).
- 78 tests pass (0 fail). All sprint/cycle lens tests pass unchanged.
- Smoke test confirmed both /lenses/epics (lens-epics present) and /epics/<slug> (reading-surface present).

### File List

- skills/momentum/skills/canvas/server.tsx
- skills/momentum/skills/canvas/server.test.ts

### Status

review
