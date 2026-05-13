# Feature Grooming Report — Composable Specialist Agents

**Feature:** `momentum-composable-specialist-agents` — Composable Specialist Agents — Project-Conditioned Agent Bodies
**Pass date:** 2026-05-12
**Driver:** Steve (manual grooming pass; pattern intended to be encoded into a future `/momentum:feature-grooming` skill)
**Scope:** Stories tagged `feature_slug: momentum-composable-specialist-agents` plus stories under `epic_slug: agent-team-model` that the dashboard renders as part of this feature.

## Context for the Pass

Three drivers triggered this grooming pass:

1. **DEC-018 (2026-05-03)** — adopted the installed Obsidian wiki skill suite (`Ar9av/obsidian-wiki` + `kepano/obsidian-skills`) as the cold KB layer, superseding the planned `kb-init`, `kb-ingest`, and vault-schema stories.
2. **`momentum:constitution-builder` shipped** — generates `## Permissions` + `## Standing Rules` + `## Quick Routing` for any KB-backed agent skill, with the same KB-synthesis logic `build-guidelines-skill` was designed to implement. The planned skill needs to become an orchestrator over `constitution-builder`, not a duplicate.
3. **Benchmark validation of project-local prototype** — `nornspun-client/.claude/skills/frontend-dev/SKILL.md` was hand-rolled with the wiki-query preflight pattern and validated by two benchmark runs (2026-05-09 to 2026-05-10). The prototype proves the pattern works but creates parallel-implementation drift risk that the existing backlog did not address.

Additionally, several stories had stale `ready-for-dev` / `review` frontmatter despite their deliverables having shipped in completed sprints (`sprint-2026-04-04-3`, `sprint-2026-04-08`).

## Actions Applied

### A. Status flips — deliverables verified on disk

| Story | Old | New | Evidence |
|---|---|---|---|
| `dev-agent-definition-files` | ready-for-dev | done | `skills/momentum/agents/{dev,dev-build,dev-frontend,dev-skills}.md` exist |
| `guidelines-verification-gate` | ready-for-dev | done | `skills/momentum/skills/sprint-planning/workflow.md` lines 538–585 implement the gate |
| `architecture-guard-implementation` | ready-for-dev | done (partial) | SKILL exists at `skills/momentum/skills/architecture-guard/`; AC1 (standalone `agents/architecture-guard.md` body) NOT delivered — moved to `architect-guard-agent-definition` per DEC-013. Annotated in story body. |
| `agent-prompt-large-file-guidance` | review | done | Large-File Handling section present in agent definitions (`grep -l "Large File Handling" skills/momentum/agents/*.md` returns 5 files) |

### B. Dropped — superseded per DEC-018

The wiki-* skill suite from `Ar9av/obsidian-wiki` and `kepano/obsidian-skills` covers the work these stories planned. DEC-018 D1 explicitly lists these as superseded.

| Story file dropped | Replaced by |
|---|---|
| `.momentum/stories/kb-init.md` | `wiki-setup` |
| `.momentum/stories/kb-ingest.md` | `wiki-ingest`, `wiki-history-ingest` |
| `.momentum/stories/kb-raw-ingest-spike.md` | `wiki-ingest` already handles multi-source ingestion |
| `.momentum/stories/vault-claudemd-navigation-contract-spec.md` | Obsidian-skills `obsidian-cli`, `obsidian-markdown` |
| `.momentum/stories/vault-indexmd-registry-format-and-update-protocol.md` | Obsidian-skills index handling |
| `.momentum/stories/wiki-page-schema-and-frontmatter-formalization.md` | Wiki-* skills enforce their own schema |

Total dropped: **6 stories** via `git rm`. The chore story `drop-superseded-kb-stories-dec-018` (which exists in the backlog and is the formal driver of these drops) can now itself be marked done — its work is complete.

### C. Rewritten — `build-guidelines-skill`

The story was designed pre-`constitution-builder`. With `constitution-builder` shipped and performing the KB-synthesis work, `build-guidelines-skill` is reframed from "new KB-synthesis skill" to "orchestrator that drives `constitution-builder` for each role × domain pair plus the universal Tier 1 constitution."

Changes applied to `.momentum/stories/build-guidelines-skill.md`:
- Added `feature_slug: momentum-composable-specialist-agents` (was missing — this is why the dashboard count for the feature was unreliable)
- Updated `depends_on: kb-init` → `depends_on: constitution-builder-write-mode-parameterization`
- Rewrote `## What This Is` and `## Why This Matters` to reflect the orchestrator pattern
- Rewrote `## Workflow Phases` from generator-style ("Distill → Generate") to orchestrator-style ("Fan out to constitution-builder → Generate Tier 1 → Wire")
- Removed mention of internal KB synthesis (that work now lives in `constitution-builder`)

### D. New intake stubs created

| New story | Role |
|---|---|
| `constitution-builder-write-mode-parameterization` | Adds `write_mode` parameter to `constitution-builder` supporting `in_place_skill` (current), `composed_agent_file` (new — for sprint-dev subagents), `standalone_constitution` (new — for Tier 1). Unblocks `build-guidelines-skill` as orchestrator. |
| `project-local-skill-md-migration-to-gen-2` | Documents the procedure for retiring hand-rolled SKILL.md prototypes (starting with `nornspun-client/.claude/skills/frontend-dev/SKILL.md`) once `build-guidelines` can produce equivalent composed bodies. Prevents parallel-implementation drift. |

Both are tagged to this feature (`feature_slug: momentum-composable-specialist-agents`).

### E. Annotations — naming reconciliation

| Story | Annotation |
|---|---|
| `architect-guard-agent-definition` | Added `> Grooming note` explaining the deliberate filename split: `agents/architect-guard.md` (the agent base body, this story) vs `skills/momentum/skills/architecture-guard/` (the SKILL, shipped by `architecture-guard-implementation`). The disambiguation is intentional. |
| `architecture-guard-implementation` | Added `> Grooming note` explaining that AC1 (standalone agent body file) was not delivered and the work moved to `architect-guard-agent-definition` per DEC-013. The SKILL shipped; the agent base body did not. |

## Net Effect on the Feature

| Metric | Before | After |
|---|---|---|
| Stories tagged `feature_slug: momentum-composable-specialist-agents` | 26 | 28 (+2 new, build-guidelines now tagged) |
| Stories on this feature's dashboard view (epic + feature) | ~60 | 54 (–6 dropped) |
| Stories with status `done` in this feature/epic | 1 | 5 |
| Stories with stale `ready-for-dev` / `review` status | 4 | 0 |
| Stories awaiting `create-story` enrichment in feature scope | ~25 | ~25 (unchanged — grooming surfaces structure; create-story enriches content) |

## Out of Scope for This Pass

The following grooming opportunities exist but are tagged to other features and were deliberately not touched. They warrant their own grooming passes.

### `momentum-practice-knowledge-base` feature

DEC-018 affects several KB-feature stories that should be reviewed:

- `build-guidelines-soft-stop-ux-for-missing-vault` — still valid (soft-stop UX is consumer-side, not infrastructure)
- `citation-integrity-validation-in-build-guidelines-avfl` — still valid
- `drop-superseded-kb-stories-dec-018` — can be marked done; this pass executed its work
- `staleness-detection-mechanism-for-raw-sources` — likely covered by `wiki-status` / `wiki-history-ingest`; needs review
- The KB infrastructure stories were dropped above; their `momentum-practice-knowledge-base` feature now has 6 fewer stories. The feature dashboard should be re-rendered.

### `agent-team-model` epic — agent-behavior-quality stories

These are still valid backlog work and were not touched. Each is a discrete behavioral fix to spawned agents (separate from the topology architecture):

- `dev-agent-executor-not-decider`
- `agent-spawn-preflight-check`
- `agent-spawn-observability-metric`
- `agent-state-verification-hook`
- `read-only-investigation-agents`
- `e2e-validator-black-box-hardening`
- `e2e-client-side-coverage`
- `e2e-and-qa-validator-prompts-branch-standalone-vs-team`
- `validator-targeted-recheck-pattern`
- `explore-agent-directory-hints`
- `fan-out-agent-prompt-fix`
- `enforce-parallel-spawning-for-independent-subagents`
- `context-aware-explanations`
- `verify-shell-before-fix`
- `maestro-ux-spec-sync-guidance`

These could be split into their own feature (perhaps `momentum-agent-behavior-quality`) to clarify dashboard views.

## Recommendations for Follow-up

1. **Run `momentum:create-story`** on the four critical-path stories in feature scope:
   - `agents-md-manifest-format`
   - `project-manifest-format-specification`
   - `constitution-builder-write-mode-parameterization` (new)
   - `build-guidelines-skill` (now reframed)

   Once these are dev-ready, a sprint can be planned with the critical path.

2. **Schedule a `momentum-practice-knowledge-base` grooming pass** to apply DEC-018 supersession to its stories.

3. **Encode this grooming workflow into `/momentum:feature-grooming`** — the phases used in this pass (Scope → Inventory → Decision cross-reference → Implementation cross-reference → Duplication detection → Report+apply) are reusable. The handoff report format here can serve as the skill's output template.

4. **Re-tag stories** that should belong to this feature but currently have empty `feature_slug:` — sweep the `agent-team-model` epic and assign accurate feature slugs so the dashboard view reflects reality.

## Audit Trail

All file changes from this pass:

**Modified (status flips + annotations):**
- `.momentum/stories/dev-agent-definition-files.md`
- `.momentum/stories/guidelines-verification-gate.md`
- `.momentum/stories/architecture-guard-implementation.md`
- `.momentum/stories/agent-prompt-large-file-guidance.md`
- `.momentum/stories/architect-guard-agent-definition.md`
- `.momentum/stories/build-guidelines-skill.md`

**Deleted:**
- `.momentum/stories/kb-init.md`
- `.momentum/stories/kb-ingest.md`
- `.momentum/stories/kb-raw-ingest-spike.md`
- `.momentum/stories/vault-claudemd-navigation-contract-spec.md`
- `.momentum/stories/vault-indexmd-registry-format-and-update-protocol.md`
- `.momentum/stories/wiki-page-schema-and-frontmatter-formalization.md`

**Created:**
- `.momentum/stories/constitution-builder-write-mode-parameterization.md`
- `.momentum/stories/project-local-skill-md-migration-to-gen-2.md`
- `.momentum/handoffs/feature-grooming-composable-specialist-agents-2026-05-12.md` (this report)

All changes are reversible via git revert.
