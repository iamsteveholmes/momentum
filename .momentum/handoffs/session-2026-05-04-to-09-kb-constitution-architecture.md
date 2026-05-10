---
date: '2026-05-09'
session_span: '2026-05-04 to 2026-05-09'
status: open
topics:
  - constitution-builder skill
  - KB architecture (two-store)
  - SDR-007 project organisation
  - nornspun-client frontend-dev skill
---

# Handoff — KB Architecture, Constitution-Builder, SDR-007

## What Was Accomplished

### momentum:constitution-builder skill (new)
Path: `skills/momentum/skills/constitution-builder/SKILL.md`

Three-phase workflow skill that builds the hot constitution for KB-backed agent skills:
- **Phase 2 — Permissions**: elicits what the agent owns and what it cannot touch; generates `settings.json` path-pattern snippet using Claude Code's `allow`/`deny` syntax (`Edit(/path/**)`, `Bash(git *)`, etc.)
- **Phase 3 — Standing Rules**: extracts always-on behavioral constraints from KB principle pages + developer input
- **Phase 5 — Routing Entries**: generates symptom→`wiki-query` entries from cold KB index

Key insight: three-tier architecture — Cold KB (wiki vault) → Hot Constitution (SKILL.md `## Permissions` + `## Standing Rules` + `## Quick Routing`) → Hot Selective (pages loaded on symptom fire).

Evals written: `skills/momentum/skills/constitution-builder/evals/evals.json` — 3 test cases, 6 runs. **Eval loop is incomplete** — viewer was launched but user never submitted feedback. skill-creator process is mid-flight.

### nornspun-client frontend-dev skill (new)
Path: `nornspun-client/.claude/skills/frontend-dev/SKILL.md`

Constitution for nornspun-client CMP development:
- **Standing Rules**: TDD (Red→Green→Refactor, Three Rules), MVI architecture (5 rules), Kotest spec style selection (5 rules)
- **Quick Routing**: 50 entries across 10 subsections — Compose, MVI, Nav 3, Kotest, SQLDelight, Ktor, Material3
- **Missing**: `## Permissions` section — constitution-builder was updated with the Permissions phase AFTER this skill was written. Needs to be run to generate the Permissions section.

### SDR-007 — Project Organisation + Two-Store Knowledge Architecture
Path: `nornspun/_bmad-output/planning-artifacts/decisions/sdr-007-project-org-knowledge-state-architecture-2026-05-07.md`

Six decisions formalised:
- D1: `nornspun/` is parent project owning all `docs/` and `.momentum/`
- D2: `nornspun-client/` and `nornspun-backend/` are code-only subprojects
- D3: Agents in subproject repos access knowledge via `wiki-query` only — no direct reads of `nornspun/docs/`
- D4: KB (wiki-query) and Momentum state (`.momentum/`) are separate stores, never mixed
- D5: Status-bearing documents (sprints, stories, epics, features) live only in `.momentum/`, never in KB
- D6: Knowledge documents in `docs/` → KB via workflow-triggered re-ingest (sprint planning, decision workflow, retro)

9 affected stories updated with SDR-007 constraints + AVFL checkpoint run + all fixes committed. AVFL surfaced that SDRs were misclassified as D5 (status-bearing) when they are D6 (knowledge documents).

### Two intake stories captured
- `migrate-sdrs-from-bmad-output-to-docs-decisions` — move SDRs to `docs/decisions/` per D6
- `retire-bmad-output-migrate-to-docs` *(depends on above)* — retire entire `_bmad-output/` legacy BMAD convention; migrate all knowledge docs to correct `docs/` locations; update BMAD config

### Architecture decisions clarified (conversation, not yet SDR'd)
- **wiki-ingest re-ingest mechanics**: hash-based (SHA-256), not timestamp-based. Unchanged files skipped automatically. Workflow-triggered re-ingest is the right pattern for slow-evolving docs.
- **Subagent permissions**: subagents inherit parent session permissions but can be restricted downward via `tools`/`disallowedTools`. Path-level write restrictions work natively (`Edit(/composeApp/**)`, `deny: Edit(/.momentum/**)`). MCP tool argument restrictions require a PreToolUse hook.
- **_bmad-output/ is legacy**: `docs/` is the canonical knowledge source. `_bmad-output/` should be retired.

---

## What Is Still Open

### 1. Permissions section for frontend-dev skill (HIGH)
The constitution-builder now has a Permissions phase but the frontend-dev skill predates it.

**Action:** Run `momentum:constitution-builder` against `nornspun-client/.claude/skills/frontend-dev/SKILL.md` — specifically just Phase 2 (Permissions) to generate the `## Permissions` section and `settings.json` snippet.

Key questions to answer during that session:
- What paths does the dev agent own? (source code only: `composeApp/`, `shared/src/`, `desktopApp/`)
- What can it NOT write? (`.momentum/`, `docs/`, sprint/story indexes)
- What bash commands does it need? (gradlew, git read-only, adb?)

### 2. skill-creator eval loop — incomplete (MEDIUM)
The eval viewer for constitution-builder was launched but feedback was never submitted.

**Action:** Re-open the viewer or re-run evals and complete the loop:
```bash
python3 ~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/eval-viewer/generate_review.py \
  skills/momentum/skills/constitution-builder-workspace/iteration-1 \
  --skill-name "constitution-builder" \
  --benchmark skills/momentum/skills/constitution-builder-workspace/iteration-1/benchmark.json \
  --static /tmp/constitution-builder-review.html
open /tmp/constitution-builder-review.html
```
After feedback, iterate on the skill and run description optimization.

### 3. Momentum plugin version bump (MEDIUM)
constitution-builder is a new skill added to the momentum plugin. Version hasn't been bumped.

**Action:** Bump `skills/momentum/.claude-plugin/plugin.json` — minor version (new skill added). Commit: `chore(plugin): bump version to X.Y.Z — add constitution-builder skill`.

### 4. Compose UI testing KB gap (MEDIUM)
KB has reference docs for Compose UI testing (`runComposeUiTest`, `createComposeRule`) but no synthesized concept pages. The compose+kotest skill was never built.

**Action before building skill:**
Run `wiki-research` on Compose UI testing to create synthesis pages:
- `runComposeUiTest` vs `createComposeRule` (CMP vs Android)
- Node interaction API (`onNodeWithTag`, `performClick`, etc.)
- `desktopTest` source set setup
- Compose state assertion patterns with Turbine

Then run `momentum:constitution-builder` to build the compose+kotest skill with KB-backed routing.

### 5. KB project docs ingestion (LOW)
We designed the doc taxonomy (what goes in KB vs stays live) but never ingested. Key docs in `nornspun/docs/` that should be in the KB but may not be:
- `docs/ux/patterns/`, `docs/ux/voice/`, `docs/ux/journeys/` — design system
- `docs/adr/` — ADRs
- `docs/guidelines/` — compose-ui-patterns, gradle-agp-build

**Action:** Run `wiki-ingest` on these paths (hash-based detection means it's safe to run; unchanged files are skipped automatically).

---

## Key Technical Decisions From This Session

| Decision | Summary |
|---|---|
| Two-store architecture | KB = knowledge (wiki-query); `.momentum/` = state (direct read). Never mixed. |
| Workflow-triggered re-ingest | PRD/architecture re-ingest at sprint planning; SDRs at decision workflow; general freshness at retro |
| Status-bearing docs never in KB | Sprints, stories, epics, features only in `.momentum/`, read live by orchestrator |
| `_bmad-output/` is legacy | `docs/` is canonical knowledge source; `_bmad-output/` to be retired |
| Subagent write permissions | Enforced via `Edit(/path/**)` path patterns in `settings.json` — harness-enforced, not behavioral |
| Routing entries use wiki-query | Not static file paths. Format: `**symptom** → \`wiki-query [question]\`` per DEC-018 |

---

## Files Created/Modified This Session

### In `momentum/` repo (sprint/sprint-2026-05-03)
- `skills/momentum/skills/constitution-builder/SKILL.md` — new skill
- `skills/momentum/skills/constitution-builder/evals/evals.json` — 3 eval cases
- `skills/momentum/skills/constitution-builder-workspace/` — eval run artifacts

### In `nornspun-client/` repo
- `.claude/skills/frontend-dev/SKILL.md` — new skill (missing Permissions section)

### In `nornspun/` repo (sprint/sprint-2026-05-01)
- `_bmad-output/planning-artifacts/decisions/sdr-007-*.md` — new SDR
- `_bmad-output/planning-artifacts/decisions/index.md` — updated
- `.momentum/stories/index.json` — updated (SDR-007 fields on 9 stories + 2 new intakes)
- `.momentum/stories/agent-prompt-templates-clarify-backend-client-path-split.md` — SDR-007 update (stub)
- `.momentum/stories/vendor-jetbrains-spm-reference-docs-for-greenfield-ios.md` — SDR-007 impact section
- `.momentum/stories/ios-bringup-path-decision-kotlin-2-4-vs-cocoapods.md` — SDR-007 impact section (AVFL-corrected)
- `.momentum/stories/postgres-schema-audit-against-supabase-best-practices.md` — SDR-007 impact section
- `.momentum/stories/migrate-sdrs-from-bmad-output-to-docs-decisions.md` — new intake
- `.momentum/stories/retire-bmad-output-migrate-to-docs.md` — new intake
