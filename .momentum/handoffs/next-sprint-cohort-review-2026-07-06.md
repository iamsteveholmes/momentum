# Handoff: Next-Sprint Cohort Review — refine inputs + sprint-planning shortlist

**Date:** 2026-07-06
**From:** end-gate pickup session (f9aa0ebe) — 12-agent workflow review of 22 cohort-relevant backlog stories + ground-truth verification of the composition pipeline.
**Sequence:** retro (handoff: `sprint-2026-06-28-retro-handoff-2026-07-06.md`) → **momentum:refine** (this doc §2–3) → **momentum:sprint-planning** (this doc §4).
**Developer's stated focus:** actually USE composed subagents — base body + manifesto + hot constitution + KB — in real conduct builds.

---

## 1. Ground truth (verified on disk 2026-07-06)

The composition machinery is **100% built and 0% used**:

- `momentum/agents.json` project block is `[]` — zero composed agents registered; defaults route 6 roles to gen-1 bodies; every `agent resolve --touches` falls through to generic `dev.md` (verified by live resolve).
- Zero composed agent files exist — `.claude/guidelines/agents/` absent in momentum AND nornspun.
- Zero manifesto instances — `.claude/manifests/` absent everywhere; format spec has the new normative File Ownership field but the only exemplar (docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md) predates it.
- No Momentum KB vault — only nornspun's exists (`~/projects/nornspun-agentic-kb`, real and populated). Multi-KB wiki-query (FR142) is "planned, not yet implemented" per build-guidelines workflow.md:60.
- No Momentum constitution — the one live instance is nornspun's (`.claude/guidelines/constitution.md`, Tier-1, shipped sprint-2026-06-18).
- `momentum-tools agent resolve` works, is multi-result, supports gen-2 paths, hard-fails on missing files. Conductor already resolves via routing table (workflow.md:550/:2047). **Resolve/spawn wiring is NOT a gap.**
- 9 base-body files exist (dev, dev-build, dev-frontend, dev-skills, qa-reviewer, e2e-validator, analyst, researcher, ux). Canonical-9 roles still backlog: architect-guard, constitution-builder, agent-builder (per architecture.md:3008 ARCH-3 — NOT architect/pm/sm as older notes assumed).

## 2. Refine: batch-DROP these 7 superseded stories (evidence inline)

| Story | Superseded by |
|---|---|
| `specialist-classify-update-for-gen-2-paths` (high) | `momentum-tools agent resolve` already returns project-scoped gen-2 paths from agents.json (momentum-tools.py:1972–2090) |
| `specialist-classify-multi-result` (med) | `agent resolve` is already multi-result (`results: [{slug, agent_path, file_scope}]`) |
| `sprint-dev-composed-file-spawn-wiring` (high) | Conductor (primary path) already spawns via routing table; target skill sprint-dev is being retired |
| `nornspun-agent-constitution-wiki-query-block` (med) | constitution-builder emits the canonical wiki-query block unconditionally (SKILL.md:46–69) |
| `drop-superseded-kb-stories-dec-018` (high) | Its 6 target slugs no longer exist anywhere in stories/index.json (grep: zero hits) |
| `constitution-builder-evals-phases-2-and-3` (med) | DEC-038 restructure removed the phases it tests; current skill has a 7-eval suite covering the new shape |
| `agents-md-manifest-format` (low) | agents.json (routing) + manifesto-format.md (spec) deliver the discoverability via a different design |

## 3. Refine: hygiene fixes

1. `conduct-live-run-against-fixture-sprint` — index says `story_file: true` but **no story file exists on disk** (index entry ~line 5628 is the only record). Flag so create-story authors it fresh at planning.
2. `researcher-base-body` — status `ready-for-dev` but `researcher.md` shipped 2026-05-16. Close done.
3. Quick-fix workflow.md:196 still calls legacy `specialist-classify` — last live call site; add a one-line migration to `agent resolve` (or note it) so the classify drops don't orphan it.

## 4. Sprint-planning shortlist — "cohort goes live" (6 stories, 2 waves)

**Wave 1 (independent):**
1. `momentum-knowledge-base-buildout` (L, feature) — Momentum's own vault + multi-KB wiki-query (FR142). The KB leg; without it every manifesto symptom→wiki-query entry dangles. Consider splitting (vault init/seed vs. FR142 multi-KB) if sizing balks.
2. `manifesto-builder-skill-generate-then-curate` (M, feature) — the missing producer. Manifestos were the unset input that blocked the live E2E run. Spec is a stale intake stub — needs create-story re-enrichment against manifesto-format.md incl. File Ownership.
3. `base-body-collapse-rollback` (M, maintenance) — remove pre-shipped dev-frontend/build/skills bodies so routing-table resolution is the ONLY specialist spawn path. Coordinate with sprint-dev references (grep shows references have grown since capture).
4. `conductor-endgate-viewer-hijack-and-silent-gate` (critical defect, S–M ride-along) — fix before this sprint's own end-gate. Stub already carries full evidence.
5. `conduct-adoption-retire-sprint-dev` — **Phase 0 only** (S ride-along): conductor never calls `momentum-tools sprint complete` (zero grep hits in conductor/workflow.md; had to run manually at the 06-28 gate). Take the port; defer the full retirement phases.

**Wave 2 (depends on 1+2 for fixture inputs):**
6. `conduct-live-run-against-fixture-sprint` (M/high) — set the nornspun fixture (agents.json project entries, .claude/manifests/, composed agents via build-guidelines) and execute the shipped E2E driver live. THE proof story; discharges last sprint's escalated residual.

**Deferred with reasons** (do not select): architect/pm/sm base bodies (planning-side roles — never flow through conduct resolve); `sprint-planning-composed-file-preference-update` + `build-guidelines-invocation-surface-in-sprint-planning` (merge into ONE small story next time — half already shipped in sprint-planning workflow.md:842–866, and the invocation story still names the pre-rename `/momentum:build-agents`); `dev-block-on-missing-dependency-contract` (hardens composed devs, not needed for the proof); `skills-kb-query-injection-audit` (audit target list is pre-conductor); `build-guidelines-soft-stop-ux-for-missing-vault` (failure-path UX; moot here once the vault exists); `citation-integrity-validation-in-build-guidelines-avfl` (quality gate, not critical path); `inject-constitution-md-path-into-create-story-flesh-out-prompts` (needs constitutions to exist first).

## 5. Depth-on-demand

Full 22-story assessment + 8 ground-truth facts: workflow output at
`/private/tmp/claude-501/-Users-steve-projects-momentum/f9aa0ebe-39e4-470d-a386-9889bbc9245c/tasks/wbxz3x2he.output`
(per-agent detail in the sibling `subagents/workflows/wf_7acca998-2b2/journal.jsonl`). Note: /tmp is volatile — this handoff carries everything decision-relevant inline.
