---
title: Teach momentum:dev to read the verification contract Part-A header
story_key: dev-read-contract-part-a-header
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

# Teach momentum:dev to read the verification contract Part-A header

## Story

As the conduct build phase,
I want the momentum:dev agent to read the plain-language Part-A header of its story's verification contract and self-check against it before signaling done,
so that the dev agent aims at the same observable acceptance target the verifier will later check, without ever authoring the contract or choosing how it gets verified.

## Description

Today the dev agent operates under a critical rule that dev agents never access the verification material at all — it implements purely against the story's plain-English acceptance criteria and signals done with no acceptance target it can read for itself. Under the conduct rewrite, every story carries a two-part verification contract. Part A is a deliberately plain-language header: a short self-check prompt plus the observable clauses the work must satisfy. Part B (the verifier body) remains off-limits to dev.

This story teaches momentum:dev to consume **only** the Part-A header — as a self-check it runs against its own work before it signals done. The old "dev agents never access the contract" critical rule is removed and replaced with a narrow, read-only allowance scoped to Part A. The dev agent reads Part A; it never writes, edits, or influences the contract, and it never decides the verification method. It continues to implement against the story's plain-English acceptance criteria; Part A is an additional self-check layer, not a replacement for the ACs, and dev never consumes the verifier body.

Part A is intentionally a plain-language dev self-check. The stakes-routing and mid-flight-escalation machinery introduced by DEC-036 governs how *findings* are dispositioned later in the flow; it never changes what the dev agent consumes from the contract. Whether a finding is routine or stakes-class, dev's relationship to the contract is identical: read Part A, self-check, signal done. This story therefore inherits no behavioral change from DEC-036 — but the AC set below makes that invariance explicit so it can be verified.

Source decisions: DEC-035 (adopt conduct; single human end-gate; legible build phase) and DEC-036 (narrow stakes-gated mid-flight escalation tier amending DEC-035 #1). Governing spec: section 7 / decision 10 (the dev-readable verification header and dev agent contract consumption boundary — both live in "## 7. Planning → dev handoff: the verification contract (decision 10)").

## Acceptance Criteria

1. When given a story whose verification contract includes a Part-A header, the dev agent reads that Part-A header — the plain-language self-check prompt and the observable clauses — and treats those clauses as its acceptance target.

2. Before the dev agent signals that the story is done, it self-checks its own work against the Part-A observable clauses and its completion signal reflects that self-check having been performed.

3. The dev agent does not author, write, edit, append to, or otherwise alter any part of the verification contract, including Part A.

4. The dev agent does not choose, set, or change the verification method for the story; it consumes the method as already given in the Part-A header.

5. The dev agent continues to implement the story against the story's plain-English acceptance criteria; Part A is used as a self-check in addition to those ACs, not as a substitute for them.

6. The dev agent does not read, consume, or act on the verifier contract body (Part B); only the Part-A header is within its reach.

7. The dev agent's consumption of the contract is identical regardless of any stakes classification or mid-flight escalation behavior elsewhere in the flow: it reads only Part A, self-checks, and signals done. No stakes class, disposition, or escalation tier changes what dev reads from the contract or how it self-checks.

8. If a story's contract has no Part-A header available, the dev agent still implements against the story's plain-English acceptance criteria and signals done; the absence of a readable Part A does not block the dev agent from completing against the ACs.

## Tasks / Subtasks

- [ ] Remove the existing critical rule in the dev agent definition that forbids dev from accessing the verification contract / specs material (AC 1, AC 6)
- [ ] Add a narrow, read-only allowance to the dev agent definition: dev may read the Part-A header of its story's verification contract, and only Part A (AC 1, AC 6)
- [ ] In the dev workflow, add a self-check step: before emitting the completion signal, the dev agent reads the Part-A self-check prompt and observable clauses and verifies its work against them (AC 1, AC 2)
- [ ] Make the completion signal reflect that the Part-A self-check was performed (AC 2)
- [ ] State explicitly in the dev agent definition that dev does not author, edit, or alter the contract (any part), and does not choose the verification method (AC 3, AC 4)
- [ ] State explicitly that dev implements against the story's plain-English acceptance criteria, with Part A as an additional self-check, and that dev never reads the verifier body / Part B (AC 5, AC 6)
- [ ] Add a guard so that a missing or unavailable Part-A header does not block completion against the plain-English ACs (AC 8)
- [ ] Add a note in the dev agent definition that stakes classification and mid-flight escalation never change what dev consumes from the contract or how it self-checks (AC 7)
- [ ] Verify the dev agent and workflow still function for a story with a Part-A header (self-checks then signals done) and for a story without one (implements ACs, signals done)

## Dev Notes

This story touches only the dev agent definition (`skills/momentum/agents/dev.md`) and the dev workflow (`skills/momentum/skills/dev/workflow.md`). It is a consume-only change: emission of the contract is explicitly out of scope and lives elsewhere in the conduct build.

The shape of Part A (per spec section 7 / decision 10): a plain-language self-check prompt (`how_dev_self_checks`) that may explicitly reference observable clauses in the contract body. Dev's acceptance target is the prompt plus any clauses it explicitly references — these are Part-A-sanctioned (spec L607: "how_dev_self_checks + the contract body's observable clauses"). The dev agent must never reach into the verifier body beyond what the prompt references — section 7 / decision 10 governs this consumption boundary.

The previously-binding critical rule "dev agents never access specs/" is removed by this story and replaced with the Part-A-only read allowance. This is the single behavioral change; everything else (implement against the story ACs, signal done) is preserved.

**Unchanged by DEC-036.** Part A is a plain-language dev self-check, and the stakes-routing / mid-flight-escalation machinery introduced by DEC-036 never touches what the dev agent consumes from the contract. Stakes classification, dispositions, and timing tiers govern how *findings* are handled downstream — they do not change dev's read surface (Part A only) or its self-check behavior. AC 7 makes this invariance an explicit, verifiable requirement so the boundary cannot silently erode. No other DEC-036 amendment (escalation tier, dismissal rendering, anti-rubber-stamp end-gate) reaches this story, because none of them alters the dev-side contract-consumption contract.

Governing spec sections: section 7 / decision 10 (dev-readable verification header and dev agent contract consumption boundary — both are in "## 7. Planning → dev handoff: the verification contract (decision 10)"; there is no separate "section 10").

### References

- Epic: `momentum-sprint-orchestration` (from `_bmad-output/planning-artifacts/epics.json`)
- DEC-035: adopt conduct; single human end-gate; legible build phase
- DEC-036: narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 #1 (invariance asserted here — DEC-036 does not change dev's contract consumption)
