# directed-fix-invocation-contract — Document Review Contract

```yaml
story_slug: directed-fix-invocation-contract
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-02-conduct-core/specs/directed-fix-invocation-contract.review.md
how_dev_self_checks: |
  Before you signal done, open the produced reference document and confirm — by reading it,
  not by inspecting code — that every Required Claim below is plainly stated. In particular:
  the document defines the contract shape (findings in -> {applied fixes, per-finding
  dispositions} out); names the four disposition values; states the routine path
  (routine finding -> fixed + committed, unchanged); states the escalate-do-not-fix path
  (stakes-class finding -> escalated + inline payload, with NO fix applied and NO fix commit);
  enumerates the stakes classes and the default routine class; requires the inline what/why/
  evidence payload floor; requires a timing-tier flag (mid-flight | end-gate-expanded) with
  the narrow mid-flight bar (irreversible-and-imminent OR build-invalidating ONLY); requires
  a non-empty rationale on any dismissed finding; and explicitly disclaims ownership of the
  mid-flight pause mechanism. If any one of these is missing or ambiguous, the document fails.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/directed-fix-invocation-contract.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

`skills/momentum/references/directed-fix-invocation-contract.md`

The reviewer reads this single produced artifact and confirms each Required Claim below by
its written content alone. No code execution, no inspection of internal function or variable
names — every claim must be visible as plain prose or a documented field in the artifact.

## Required Claims

- [ ] The document specifies an invocation contract for the directed `momentum:dev` fix-mode
      (the fix-mode invoked by the Conductor during the conduct build phase).
- [ ] The document states the contract shape in one place: findings in → {applied fixes,
      per-finding dispositions} out.
- [ ] The document states that every inbound finding returns with exactly one disposition.
- [ ] The document defines the disposition vocabulary as exactly: `fixed`, `dismissed`,
      `triaged-out`, `escalated` — each with a written one-line meaning.
- [ ] The document states the routine path: a routine / default-class legitimate finding returns
      `disposition = fixed` with the fix applied and committed, and describes this path as
      unchanged and the always-on default.
- [ ] The document states the escalate-do-not-fix path: a stakes-class finding returns
      `disposition = escalated` plus an escalation payload INSTEAD of a fix, and explicitly
      states that no fix is applied and no fix commit is produced for an escalated finding.
- [ ] The document enumerates the stakes classes that trigger escalation: security/auth-isolation;
      irreversible/destructive (migration, delete, force-push, prod deploy);
      high-blast-radius/architecture — and names `routine` as the default class.
- [ ] The document requires the escalation payload to be carried INLINE in the return and to
      contain, at minimum, the what / why / evidence a human decision card needs (not a pointer
      or external reference to be fetched).
- [ ] The document requires the escalation payload to carry a timing-tier flag with only the
      values `mid-flight` and `end-gate-expanded`, names `end-gate-expanded` as the default,
      and states the mid-flight bar is restricted to irreversible-and-imminent OR
      build-invalidating findings ONLY (the bar must stay narrow).
- [ ] The document states that any `dismissed` finding MUST carry a non-empty rationale, and
      that an empty or missing rationale is invalid.
- [ ] The document explicitly states that this contract does NOT own or implement the mid-flight
      pause mechanism — it emits disposition + timing-tier only so the Conductor can route, and
      the fix-mode never pauses, blocks, or prompts the human.
- [ ] The document describes itself as a specification artifact that introduces no executable
      behavior of its own.

## Required Sections

- [ ] A purpose / overview statement naming the directed `momentum:dev` fix-mode and the Conductor.
- [ ] A contract-shape statement (findings in → {applied fixes, per-finding dispositions} out).
- [ ] A disposition vocabulary section listing `fixed | dismissed | triaged-out | escalated`.
- [ ] A routine-path description (routine finding → fixed + committed; unchanged default).
- [ ] An escalate-do-not-fix path description (stakes-class → escalated + inline payload, no fix,
      no fix commit) including the stakes-class enumeration and default `routine`.
- [ ] An escalation-payload section covering the inline what/why/evidence floor and the
      timing-tier flag (`mid-flight | end-gate-expanded`, default end-gate-expanded, narrow
      mid-flight bar).
- [ ] A dismissed-rationale requirement (non-empty rationale required).
- [ ] An explicit pause-ownership boundary statement (contract does not implement the pause).

## Pass Criteria

- Every Required Claim checkbox is confirmed true by the written content of the document under review.
- Every Required Section is present and substantive.
- The escalate-do-not-fix behavior, the inline-payload floor, the timing-tier flag with its narrow
  mid-flight bar, the non-empty dismissed rationale, and the pause-ownership disclaimer are all
  stated unambiguously (these are the DEC-036 amendments and must be explicit, not implied).

## Fail Criteria

- Any Required Claim is absent, contradicted, or stated so ambiguously a reviewer cannot confirm it.
- The document conflates escalation with fixing (e.g., describes a stakes-class finding as fixed/committed)
  or permits a fix commit on an escalated finding.
- The mid-flight bar is described broadly (anything beyond irreversible-and-imminent OR
  build-invalidating), or the timing-tier flag is missing or allows values other than
  `mid-flight` / `end-gate-expanded`.
- The escalation payload is described as a pointer/reference rather than inline what/why/evidence.
- `dismissed` is allowed without a non-empty rationale.
- The document claims to implement, own, or trigger the mid-flight pause mechanism.
- The document specifies executable behavior rather than a specification of the contract.
