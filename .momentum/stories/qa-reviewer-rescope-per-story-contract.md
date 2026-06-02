---
title: Rescope qa-reviewer to the per-story contract and add producer-side stakes tagging
story_key: qa-reviewer-rescope-per-story-contract
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - agent-definition
verification_method: skill-invoke
depends_on:
  - directed-fix-finding-schema
  - stakes-classification-rubric
touches:
  - skills/momentum/agents/qa-reviewer.md
---

# Rescope qa-reviewer to the per-story contract and add producer-side stakes tagging

## Story

As the Conductor orchestrating the conduct build phase,
I want the qa-reviewer agent rescoped to verify a single story's worktree diff against that story's own verification contract — running concurrently in stage 2 — and to tag each finding with a stakes class as it produces it,
so that per-story verification is legible and isolated, and the downstream fixer-hold and end-gate forcing functions receive a true stakes signal at the moment a finding is born rather than a structural false-negative discovered too late.

## Description

Today momentum:qa-reviewer runs **post-merge, on `main`, over the whole sprint** — it inspects everything that landed and reports against the sprint as a unit. Under conduct, the build phase verifies each story in isolation, inside its own worktree, before anything merges. This story rescopes qa-reviewer from the whole-sprint post-merge model to a **per-story** model: it verifies a single story's worktree diff against **that story's** verification contract, and it runs **concurrently in stage 2** alongside the other stage-2 reviewers.

**What changes**

1. **Scope narrows from sprint to story.** Input is one story's worktree diff plus that one story's verification contract. The reviewer classifies each acceptance criterion as VERIFIED / PARTIAL / MISSING / BLOCKED with `file:line` evidence drawn from the diff. The whole-sprint, post-merge, on-`main` behavior is removed.

2. **Cross-story integration checks leave qa-reviewer.** Anything that requires seeing more than one story at once — integration between stories, sprint-wide consistency, contract drift across stories — is **out of scope** here and migrates to AVFL (which runs once after the whole build, against the integrated result). qa-reviewer stops trying to reason about stories other than the one it was handed.

3. **Stakes tagging is added at the producer.** qa-reviewer is the agent that *produces* findings. Under DEC-036 the build phase gates certain findings differently based on a `stakes_class` (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; default routine). If the class is only inferred downstream, a structural false-negative is easy: a downstream consumer with no view of the AC text or the diff cannot reliably tell that a MISSING finding sits on a destructive operation. So qa-reviewer **tags** each finding with its `stakes_class` at the moment it writes the finding, consuming the shared stakes-classification rubric. This gives the downstream fixer-hold (DEC-036 D2) and the end-gate forcing function (DEC-036 D4) a true signal.

**Why now / pain context.** The conduct rewrite (DEC-035) replaces whole-sprint post-merge review with in-flight per-story verification under a single human end-gate, no story-count cap, and a legible auto-fix loop. DEC-036 narrowly amends DEC-035 to permit a stakes-gated mid-flight escalation tier and to make the end-gate anti-rubber-stamp — both of which depend on findings carrying a trustworthy stakes class. The natural and only correct place to set that class is at the producer, where both the AC semantics and the diff are in view. Tagging it anywhere later is guessing.

**Hard constraints carried forward (must not regress).** The existing qa-reviewer discipline stays intact: reading source is **never** a substitute for executing tests; the MISSING-vs-BLOCKED distinction is preserved (MISSING = the behavior is genuinely absent/unverified; BLOCKED = it could not be verified because something prevented execution); and when services are required to exercise the story, the reviewer **must start the services** rather than declaring the path unverifiable.

**Source decisions:** DEC-035 (adopt conduct; one end-gate; legible auto-fix loop), DEC-036 (narrow stakes-gated escalation; producer-side stakes signal feeding D2 fixer-hold and D4 end-gate forcing function). Governing spec: conduct spec section 3 (stage 2), section 4, section 10.

## Acceptance Criteria

1. When invoked, qa-reviewer verifies exactly one story's worktree diff against that same story's verification contract, and produces no findings about any other story.

2. Each acceptance criterion in the story's contract is classified as exactly one of VERIFIED, PARTIAL, MISSING, or BLOCKED, and each classification carries concrete `file:line` evidence pointing into the diff under review.

3. qa-reviewer executes the story's tests to reach its verdicts; reading or quoting source code is never accepted in place of executing the tests. A verdict that rests only on source-reading where tests were runnable is a failure of this story.

4. The MISSING-vs-BLOCKED distinction is preserved: MISSING means the behavior is genuinely absent or unverified by passing tests; BLOCKED means verification could not be performed because something prevented test execution. The two are never conflated.

5. When the story requires running services to exercise its behavior, qa-reviewer starts those services and exercises the behavior against them; it does not classify a service-backed criterion as BLOCKED merely because services were not already running.

6. qa-reviewer runs concurrently within stage 2 of the build phase (per spec section 3 stage 2), alongside the other stage-2 reviewers, scoped to its single story — not serialized after them and not waiting on a sprint-wide pass.

7. Every finding qa-reviewer emits carries a `stakes_class` drawn from the shared stakes-classification rubric, set to one of the defined classes (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; or default routine).

8. When a finding has no stakes signal, qa-reviewer tags it `routine` — `routine` is the default, applied only in the absence of a signal, never as a way to suppress a real signal.

9. When a finding touches an authentication-isolation or other security acceptance criterion, qa-reviewer tags it with the security/auth-isolation stakes class (DEC-036 D2/D4).

10. When a MISSING or PARTIAL finding touches a destructive or irreversible operation (for example a migration, a delete, a force-push, or a production deploy), qa-reviewer tags it with the irreversible/destructive stakes class (DEC-036 D2/D4).

11. The stakes class qa-reviewer assigns is determined by consulting the shared stakes-classification rubric, so that the class a finding receives is consistent with what any other producer using the same rubric would assign for the same signal.

12. Cross-story integration checks, sprint-wide consistency checks, and any reasoning that requires seeing more than the one story under review are out of scope for qa-reviewer; that coverage is owned by AVFL and qa-reviewer emits no such findings.

13. qa-reviewer no longer runs post-merge on `main` over the whole sprint; the prior whole-sprint, post-merge model is removed and does not run.

## Tasks / Subtasks

- [ ] Rescope the qa-reviewer agent definition input from "whole sprint on main, post-merge" to "single story worktree diff + that story's verification contract" (AC 1, 13)
- [ ] Define the per-AC classification output: VERIFIED / PARTIAL / MISSING / BLOCKED, each with required `file:line` evidence into the diff (AC 2)
- [ ] Carry forward the hard constraint that tests must be executed and that source-reading never substitutes for execution; state it explicitly in the agent definition (AC 3)
- [ ] Carry forward and document the MISSING-vs-BLOCKED definitions so the two are never conflated (AC 4)
- [ ] Carry forward the mandatory-service-startup constraint: when services are required, start them and exercise the behavior rather than classifying as BLOCKED (AC 5)
- [ ] Position qa-reviewer to run concurrently in stage 2 alongside the other stage-2 reviewers, scoped to its one story (AC 6); align with spec section 3 stage 2 / section 4 / section 10
- [ ] Add producer-side stakes tagging: every emitted finding gets a `stakes_class` field, populated by consulting the shared stakes-classification rubric (AC 7, 11)
- [ ] Implement the default rule: absence of any stakes signal yields `routine`; never use `routine` to mask a real signal (AC 8)
- [ ] Encode the auth-isolation / security trigger: a finding on a security or auth-isolation AC is tagged security/auth-isolation (AC 9)
- [ ] Encode the destructive-op trigger: a MISSING or PARTIAL finding touching a destructive/irreversible operation is tagged irreversible/destructive (AC 10)
- [ ] Explicitly remove cross-story / sprint-wide / integration reasoning from qa-reviewer's responsibilities and note AVFL ownership (AC 12)
- [ ] Remove the post-merge-on-main whole-sprint invocation path (AC 13)
- [ ] Self-check against the story ACs before signaling done

## Dev Notes

**Agent type and invocation.** qa-reviewer is a finding **producer** — it is a reviewer agent the Conductor spawns during stage 2, not the orchestrator itself. It writes no git mutations and merges nothing; it reads a story's worktree diff, runs that story's tests, and emits classified findings. `verification_method: skill-invoke` — the agent is exercised by invocation and its observable outputs are inspected.

**Per-story isolation is the core shift.** The whole point of the rescope is that the unit of review is one story, in its worktree, before merge. Everything cross-story is deferred to AVFL, which runs once over the integrated build. qa-reviewer that emits a finding about story B while reviewing story A is a defect, not a feature.

**Stakes tagging is producer-side on purpose.** DEC-036 introduces a `stakes_class` that the build phase uses to (a) hold the fixer on stakes-class findings instead of silently auto-fixing (D2), and (b) force the end-gate to surface them anti-rubber-stamp (D4). Those consumers act on the *signal*, but only the producer has both the AC text and the diff in front of it, which is what's needed to recognize, e.g., a MISSING finding sitting on a migration. Setting the class anywhere downstream invites a structural false-negative. Hence the tagging lives here. The shared rubric (`stakes-classification-rubric`, a dependency of this story) defines the four classes and the signals that map to them; qa-reviewer consumes that rubric so its tagging is consistent with every other producer. The finding shape that carries the class is owned by `directed-fix-finding-schema` (the other dependency).

**Vocabulary to honor exactly.** Stakes classes: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine. qa-reviewer's job here is the *tag*, not the *disposition* — dispositions (fixed | dismissed | triaged-out | escalated) and timing tiers (end-gate-expanded default | mid-flight narrow) are decided downstream by the fix loop and the Conductor, not by this producer. qa-reviewer only sets `stakes_class`.

**Hard constraints are non-negotiable.** The three carried-forward constraints (execute tests, never substitute source-reading; MISSING vs BLOCKED; mandatory service startup) are existing qa-reviewer discipline and must survive the rescope unchanged. They are the reason qa-reviewer's verdicts are trusted at all.

**Governing spec sections (cited by number from the authoring brief):**
- Section 3, stage 2 — concurrent stage-2 reviewers; qa-reviewer runs here, per story.
- Section 4 — build-phase verification structure into which the per-story review fits.
- Section 10 — qa-reviewer's role and constraints within conduct.

### References

- Epic: `momentum-sprint-orchestration` — `_bmad-output/planning-artifacts/epics.json`
- Decision: DEC-035 — adopt conduct; one human end-gate; no story-count cap; report organized by user-facing functionality; legible auto-fix loop (what it changed AND dismissed).
- Decision: DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier; stakes-class findings leave the silent auto-fix path; report renders dismissals; anti-rubber-stamp end-gate. Specifically D2 (fixer-hold on stakes-class findings) and D4 (end-gate forcing function), both of which consume the producer-side `stakes_class` set by this story.
- Dependency stories: `directed-fix-finding-schema` (finding shape carrying `stakes_class`), `stakes-classification-rubric` (shared class definitions consumed here).
