---
id: AES-002
title: Feature Schema Value Gap — Structural Definition Without Value Context
date: '2026-04-11'
status: current
method: session analysis + features.json audit + developer conversation (April 11, 2026)
decisions_produced:
  - DEC-004
supersedes: []
---

# AES-002: Feature Schema Value Gap

## Purpose

Evaluate whether the current feature schema and feature-management practice deliver on
their intent. Determine whether features, as currently defined, are functioning as units
of value delivery or as structural bookkeeping artifacts.

---

## The Problem

Sprints are completing. Stories are being done. Yet users cannot use Nornspun for anything
useful today. A user cannot initialize a session. They cannot import documents. They cannot
prepare for a game. The product has accumulated stories, epics, and features — but not value.

Momentum has a similar pattern. Many skills exist. But several of them are hard to explain
to a developer who hasn't already been working in the codebase. "Why would I use this?"
should be answerable in one sentence. For many current features, it isn't.

The root cause is not missing stories. It is that features are being defined as structural
containers rather than value delivery vehicles. A feature is supposed to be the answer to
the question "what does this product do for me?" — not a label for a cluster of related
work.

---

## Current State

### Feature Schema

The current `features.json` schema contains:
```
feature_slug (key)
name
type (flow / connection / quality)
description
acceptance_condition
status
prd_section
stories[]
stories_done
stories_remaining
last_verified
notes
```

Every field describes **what** the feature is and **how it relates to other artifacts**.
No field asks **why** a user would want it, **what value** it delivers, **how it
fits** the broader product, or **what gap exists** between current delivery and full vision.

### Evidence: Nornspun

Nornspun features do articulate user value in their `description` and `acceptance_condition`
fields — "ready to run their session in under 15 minutes," "capture doesn't get abandoned."
The intent is there. But Nornspun has 0 users experiencing this value. The features are
defined correctly in words, but the value hasn't been delivered.

The missing fields would force honest assessment: "what value is this delivering *right now*
vs. what we aspire to?" Without that, features silently drift to "technically defined but
not delivering."

### Evidence: Momentum

Momentum features describe internal process efficiency, not developer outcomes:
- "Sprint Planning — Backlog to Ready Sprint" — describes a workflow, not what the developer
  gains from running it
- "Assessment → Decision → Story Traceability" — describes a mechanism, not the knowledge
  or confidence it creates
- "Quality Gates Applied to Every Sprint" — describes enforcement, not the psychological
  safety that makes rapid development possible

A developer encountering these descriptions is told *what* the feature does, not *why
they would want it* or *how their work is different after having it*.

### Evidence: Missing Impetus Feature

Impetus — the session host and practice companion — is not represented as a feature at all.
The "session orientation" feature covers the functional sprint-state greeting. But Impetus
as a UX experience (personality, ASCII art, identity, warmth) has no feature definition.
Because it has no feature, it has no value analysis, no status, and no gap tracking. The
developer observation that Impetus currently feels like "a lifeless config dump" has no
structural home in the practice.

---

## What Is Missing

### 1. value_analysis — substantive value description

Every feature needs an honest, multi-paragraph description that covers:
- What value the feature delivers **right now**, in its current state
- The **full vision** of the value it could deliver — including new capabilities the user
  didn't know they wanted, not just removal of known pain
- Known **gaps** between current delivery and full vision

Pain removal is one valid form of value. Others include: new capabilities that expand what
is possible, knowledge that elevates judgment, experiences that make work more enjoyable
or effective. A feature's value_analysis should cover whichever dimensions apply.

Value is a **spectrum**, not a boolean. A feature can be partially delivering value and
have a clear path to delivering more. Status must reflect actual delivery, not story completion.

### 2. system_context — how this feature enhances the whole

Every feature exists in relationship to other features. A feature that delivers value
in isolation but makes the product harder to understand or use is still a liability.
The system_context field captures:
- How this feature fits the overall product
- What becomes possible or impossible without it
- How its value enhances or interacts with other features

### 3. Honest current-state status

A feature with status "working" that has 0 users is not working. Status must reflect
whether the feature is actively delivering value to someone, not just whether its
implementation stories are technically complete.

---

## Risk

Without these changes, the practice will continue to:

1. **Deliver stories without delivering value.** Stories complete; features stay at "partial"
   indefinitely; users never get anything they can use.

2. **Accumulate features that nobody uses.** A feature that nobody uses but nobody removes
   becomes permanent maintenance burden. Without a value_analysis that shows the gap between
   current and full value, there is no basis for deciding to simplify or remove.

3. **Lose the thread on why things were built.** As the codebase grows, features defined
   without value context become harder to maintain, extend, or explain. New contributors —
   human or AI — can read the schema but can't understand the purpose.

---

## Recommendation

Add `value_analysis` and `system_context` as required fields to the features.json schema.

Require feature-grooming to populate these fields for all proposed features, with the
following standards:
- `value_analysis`: minimum one substantive paragraph; must address current value, full
  vision, and known gaps; must not reduce to pain removal only
- `system_context`: one paragraph; must explain how this feature enhances the overall
  product and what depends on it

Flag existing features without these fields as incomplete at every refine run.

Create DEC-004 to formalize this decision and define the schema contract.
