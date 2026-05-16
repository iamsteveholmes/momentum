---
id: DEC-024
title: Read-Only Skill Constraint — Context:Fork Replaces Separate Role Bodies
date: '2026-05-16'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-16'
prior_decisions_reviewed:
  - DEC-008 D4 (Fallback behavior when composed file missing)
  - DEC-013 (Universal Agent Model — No Bucket Distinction, Ask Not Fallback, Sprint Planning as Type Discovery)
  - DEC-020 (Universal Agent Role Taxonomy — BMAD-Aligned Base Bodies)
architecture_decisions_affected:
  - DEC-008 D4 — extends no-fallback posture to read-only constraint pattern
  - DEC-020 D2 — implements the mechanism that closes code-reviewer and architect-guard base body stories
stories_affected:
  - code-reviewer-agent-definition (closed)
  - architect-guard-agent-definition (closed)
  - code-review SKILL.md (update — implement constraint pattern)
  - architecture-guard SKILL.md (update — implement constraint pattern)
---

# DEC-024: Read-Only Skill Constraint — Context:Fork Replaces Separate Role Bodies

## Summary

Read-only agent invocations (code review, architecture guard) are achieved by spawning the appropriate base role with `context:fork` + `allowed-tools: Read` applied by the calling skill. No separate base body files are needed for read-only variants. This generalizes to a universal principle: any role can be invoked read-only by any skill, eliminating the combinatorial explosion of "reviewer" role variants.

The code-review skill spawns the project's dev agent(s) from the routing table with the read-only constraint and an adversarial prompt framing. The architecture-guard skill spawns the architect agent similarly. Both skills need SKILL.md updates to implement the constraint pattern; no new base body files are created.

## Decisions

### D1: code-review skill invokes dev with Read-only constraint — ADOPTED

**Developer framing:** How should the code-review skill spawn its review agent without requiring a separate code-reviewer base body?

**Decision:** The code-review skill spawns the project's dev agent(s) resolved from the routing table, but passes `context:fork` and `allowed-tools: Read`. The agent performs adversarial code review with an adversarial prompt framing. It cannot write regardless of what it intends.

**Rationale:** The adversarial constraint is caller-provided; the dev base body already has the domain knowledge needed for code review. Maintaining a separate code-reviewer base body would duplicate dev's domain knowledge while providing no additional capability.

---

### D2: architecture-guard skill invokes architect with Read-only constraint — ADOPTED

**Developer framing:** How should the architecture-guard skill spawn its review agent without requiring a separate architect-guard base body?

**Decision:** Same pattern. The architecture-guard skill spawns the architect agent with `context:fork` + `allowed-tools: Read, Grep, Bash(git *)`. The git read access allows the agent to inspect commit history and diffs relevant to the architectural pattern being checked.

**Rationale:** Same reasoning as D1; architect already knows architecture.md and the relevant architectural decisions. The guard constraint is caller-provided.

---

### D3: Generalization — any role can be invoked read-only — ADOPTED

**Developer framing:** Is this pattern limited to code review and architecture guard, or does it apply broadly?

**Decision:** Any skill can invoke any role read-only for review/audit purposes. pm invoked read-only can audit PRD drift. analyst invoked read-only can audit an assessment. The permission constraint is always a caller concern, never a role concern.

**Rationale:** Eliminates the combinatorial explosion of "reviewer" role variants (code-reviewer, prd-reviewer, architecture-reviewer, etc.). The pattern is: role identity provides domain knowledge; caller provides constraint. These are orthogonal concerns and should be composed at the call site.

---

### D4: Closes code-reviewer-agent-definition and architect-guard-agent-definition — ADOPTED

**Developer framing:** What story closures follow from this decision?

**Decision:** The code-reviewer-agent-definition and architect-guard-agent-definition stories are closed. The SKILL.md files for code-review and architecture-guard need to be updated to implement the constraint pattern, but no new base body files are created.

**Rationale:** The stories were created under the assumption that read-only agents required dedicated base bodies. D1-D3 show this assumption is incorrect; the constraint pattern achieves the same capability with less file overhead and no role duplication.
