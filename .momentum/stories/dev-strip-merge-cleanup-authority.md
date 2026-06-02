---
title: Strip merge, worktree-cleanup, lock, and crash-ask authority from momentum:dev
story_key: dev-strip-merge-cleanup-authority
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - agent-definition
verification_method: skill-invoke
depends_on: []
touches:
  - skills/momentum/agents/dev.md
  - skills/momentum/skills/dev/workflow.md
---

# Strip merge, worktree-cleanup, lock, and crash-ask authority from momentum:dev

## Story

As the maintainer of the Momentum build pipeline,
I want the `momentum:dev` agent stripped of all merge, worktree-cleanup, lockfile-handling, and crash-recovery-ask authority,
so that the Conductor becomes the single owner of git mutation and the human end-gate, which is the precondition for the Conductor to own mid-flight escalation.

## Description

Today `momentum:dev` does more than implement a story. After it finishes coding it also proposes (and waits for) a merge, performs the worktree merge and conflict resolution, runs worktree cleanup, manipulates a lockfile, and — on a crashed or interrupted run — asks the human how to recover. That spreads git-mutation authority across every per-story dev agent and makes it impossible for a single orchestrator to own the build phase, the git history, and the one human gate.

The `conduct` rewrite (the in-session, per-story, autonomous-build, single-end-gate replacement for `momentum:sprint-dev`) puts the Conductor in charge of the build phase. Per spec section 3 (build-phase ownership), section 6 (git mutation / merge), and section 12 (worktree lifecycle, lock, and crash recovery), all of that authority moves out of `dev` and into the Conductor. The dev agent is reduced to a pure implementer: it produces the change and reports what it touched, and it stops there.

This narrowing is not cosmetic. Per DEC-036 (D1), relocating git-mutation authority from `dev` to the Conductor is an explicit **precondition** for the Conductor to own the narrow, stakes-gated mid-flight escalation tier. As long as `dev` can merge, the Conductor cannot be the single point that decides whether a stakes-class finding pauses the run irreversibly or waits for the end-gate. So this story removes:

- the merge proposal/await in the dev agent,
- the worktree merge and conflict resolution,
- the worktree cleanup,
- the lockfile handling,
- the crash-recovery ask,
- and the `dev.md` "no-auto-merge" critical rule (deleted outright, since the agent no longer touches merge at all).

Pain context: with merge authority living in `dev`, every story-level agent is a place where the git history can diverge, a lock can be left stale, or a human can be asked an ad-hoc recovery question outside the single end-gate. Consolidating that authority in the Conductor is what makes the single-end-gate model (DEC-035) and the narrow mid-flight escalation tier (DEC-036) coherent.

Source decisions: DEC-035 (adopt conduct; one human gate at the end; Conductor owns the build phase and all git mutation), DEC-036 (narrow mid-flight escalation tier owned by the Conductor; D1 names this relocation as a precondition).

## Acceptance Criteria

1. When `momentum:dev` is invoked on a story and finishes implementing, its terminal output reports implementation-complete plus a list of the files it changed (the `file_list`), and nothing more — it does not propose a merge and does not wait for a merge to be approved.

2. `momentum:dev` performs no worktree merge: it never merges its branch/worktree into any target branch.

3. `momentum:dev` performs no merge-conflict resolution: it never resolves, or attempts to resolve, a merge conflict.

4. `momentum:dev` performs no worktree cleanup: it never removes, prunes, or tears down a worktree.

5. `momentum:dev` performs no lockfile handling: it never creates, acquires, releases, or clears a build/merge lock.

6. `momentum:dev` performs no crash-recovery ask: on an interrupted or failed run it does not prompt the human for a recovery decision (recovery is the Conductor's responsibility, surfaced only at the single end-gate).

7. Running `momentum:dev` on a story creates no merge artifacts and removes no merge/worktree artifacts — no merge commit, no worktree teardown, no lock file change is attributable to the dev agent. The Conductor owns all such artifacts.

8. The "no-auto-merge" critical rule is no longer present anywhere in the dev agent definition: because the dev agent no longer touches merge at all, the rule that forbade auto-merge is deleted rather than retained.

9. The behavior changes in ACs 1–8 are observable purely from invoking `momentum:dev` and inspecting its terminal output and the repository state afterward — no claim depends on inspecting the dev agent's internal source.

## Tasks / Subtasks

- [ ] Remove the merge proposal/await step from the dev agent so that, after implementation, the agent reports completion and the `file_list` and then stops (AC 1).
- [ ] Remove the worktree merge step from the dev agent definition and its workflow (AC 2).
- [ ] Remove the merge-conflict-resolution behavior from the dev agent definition and its workflow (AC 3).
- [ ] Remove the worktree-cleanup step from the dev agent definition and its workflow (AC 4).
- [ ] Remove the lockfile-handling behavior (acquire/release/clear) from the dev agent definition and its workflow (AC 5).
- [ ] Remove the crash-recovery ask from the dev agent definition and its workflow; the dev agent no longer prompts the human on interruption/failure (AC 6).
- [ ] Delete the "no-auto-merge" critical rule from `skills/momentum/agents/dev.md` (AC 8).
- [ ] Confirm the dev agent's terminal output schema is now exactly implementation-complete + `file_list` (AC 1).
- [ ] Update `skills/momentum/skills/dev/workflow.md` so the workflow ends at implementation-complete + `file_list` and contains no merge/worktree/lock/crash-ask steps (ACs 2–6).
- [ ] Add a Dev Notes pointer noting that merge / worktree-cleanup / lock / crash recovery now belong to the Conductor (spec sections 3, 6, 12) so a future reader does not re-add them to `dev`.
- [ ] Self-check the deltas by invoking `momentum:dev` on a representative story and confirming no merge/worktree/lock artifact and no recovery prompt result from the dev agent (ACs 1–9).

## Dev Notes

This is an `agent-definition` change verified by `skill-invoke`. The two surfaces are the agent definition (`skills/momentum/agents/dev.md`) and its workflow (`skills/momentum/skills/dev/workflow.md`). The end state: `momentum:dev` is a pure implementer whose terminal contract is implementation-complete + `file_list`, with zero git-mutation, lock, or human-recovery behavior.

Governing spec sections (cited by number from the authoring brief — not opened):
- Section 3 — build-phase ownership moves to the Conductor; the dev agent is a per-story implementer only.
- Section 6 — git mutation / merge (including conflict resolution) is the Conductor's, not `dev`'s.
- Section 12 — worktree lifecycle, lockfile handling, and crash recovery are the Conductor's, not `dev`'s.
- The `dev.md` "no-auto-merge" critical rule is deleted (the agent no longer touches merge, so a rule forbidding auto-merge is moot).

DEC-036 endorsement to record: per DEC-036 (D1), relocating git-mutation authority from `dev` to the Conductor is a confirmed **precondition** for the Conductor to own the narrow, stakes-gated mid-flight escalation tier. This story is therefore an enabling step for the mid-flight escalation work, not an isolated cleanup. The Conductor — not `dev` — is the single point that decides whether a finding (a) is silently auto-fixed (routine, always auto-fixed), (b) leaves the silent path because it is a stakes-class finding (security/auth-isolation; irreversible/destructive such as migration, delete, force-push, prod deploy; or high-blast-radius/architecture), and (c) within stakes-class findings, whether it is raised mid-flight under the NARROW bar (irreversible-and-imminent OR build-invalidating ONLY) or deferred to the end-gate-expanded tier (the default safety net). Because `dev` can no longer merge or otherwise mutate git, the Conductor can hold the irreversible operations and gate them — which is precisely why this relocation is the precondition. Disposition vocabulary that the Conductor (not `dev`) owns: fixed | dismissed (non-empty rationale required) | triaged-out | escalated (raised, not silently fixed).

Black-box separation: this story does not assume the dev agent's internals beyond the observable contract. Reviewers verify by invoking `momentum:dev` and observing output and repository state.

### References

- Epic `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json` (the conduct core-build epic; the Conductor as top-level session orchestrator that owns the build phase, all git mutation, and the single human end-gate).
- DEC-035 — adopt conduct; one human gate at the end; no story-count cap; Conductor owns the build phase and all git mutation; report organized by user-facing functionality; legible auto-fix loop.
- DEC-036 — narrowly amends DEC-035 #1: a narrow, high-bar, stakes-gated mid-flight escalation tier owned by the Conductor; D1 confirms relocating git-mutation authority from `dev` to the Conductor as a precondition for that ownership.
