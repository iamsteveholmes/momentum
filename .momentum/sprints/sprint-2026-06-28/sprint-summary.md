# Sprint Summary — sprint-2026-06-28

**Sprint completed:** 2026-07-06
**Retro date:** 2026-07-06

## Stories Completed vs. Planned

5 / 5 planned stories reached done (no force-closures):

- companion-surface-pre-sprint-plan-gate
- companion-surface-post-sprint-results-gate
- companion-surface-rule-sync-and-bulk-derivation
- manifesto-format-normative-file-pattern-ownership-field
- live-e2e-compose-register-resolve-gen-2-agent

Retro caveat: `live-e2e-compose-register-resolve-gen-2-agent` merged done with headline AC1/AC6 unmet — both driver runs failed at the first check (`agents.json` not found; missing live fixture). Carried forward as a ledger handoff and the next sprint's proof story.

## Key Decisions

No decisions recorded this sprint.

## Unresolved Issues

- Retro stubs added to backlog (3): `repair-phantom-story-file-entries-and-backfill-live-fixture-scope` (high), `harden-avfl-checkpoint-validator-mailbox-delivery` (high), `epic-fit-flag-enforcement-and-companion-surface-epic-correction` (medium)
- Retro amendments to existing stories (4): audit-engine model pinning AC, process-findings story backfill/re-prioritization, avfl namespace-typo fold, AVFL out-of-scope-file routing expansion
- Pre-existing critical stub from the end-gate incident: `conductor-endgate-viewer-hijack-and-silent-gate`
- 12 retro handoff events written to practice-ledger.jsonl for next sprint planning

## Narrative

This sprint shipped the companion decision surfaces (pre-sprint plan gate, post-sprint results gate, and rule-sync/bulk derivation), the normative File Ownership field in the manifesto format, and the gen-2 live E2E compose/register/resolve driver — released as plugin 0.31.0. The build's dominant friction was a single root cause rediscovered at least three times: the missing live nornspun fixture, which blocked 9/9 ACs on one story and 16/27 sprint E2E scenarios, and left the E2E driver unproven at merge. The retro ran the first Workflow-tool audit engine (14 agents, 33 verified findings) plus a 27-agent corpus-wide dedup, converting the findings into 3 deduplicated backlog stubs, 4 story amendments, and 12 ledger handoffs. The practice takeaway: verification must demand observed output over structured status, and index/story-file integrity now has an owning story.
