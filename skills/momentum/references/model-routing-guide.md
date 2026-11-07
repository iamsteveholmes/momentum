# Momentum Model Routing Guide

**Principle: nothing in Momentum hard-codes a model.** Skills, agents, workflows, and `framework.json` carry no model pins. The orchestrator chooses a model per task at spawn time. A skill or agent with no `model:` runs on the session model unless the orchestrator passes one.

## How to choose (at spawn time)

| Work type | Choice |
|---|---|
| Judgment work: planning, retro, assessment, review synthesis, decisions, adversarial validation | Session model (do not pass `model`) |
| Mechanical, extraction, audit scans, or high-volume worker steps where cost matters | Sonnet 5.5 or Haiku 5.5 (pass a family alias, e.g. `sonnet`, `haiku`) |

Effort is separate from model. Skills still declare `effort:` in frontmatter and workflows may state an effort level per step.

## Rules

- Never pin versioned model IDs anywhere in skills, agents, workflows, or generated agent files; they go stale silently.
- Do not add `model:` to frontmatter. Generated agents (agent-builder, build-guidelines) omit it too.
- Tier hints in workflows (for example AVFL's "mid-tier worker" / "strongest judgment model") are guidance for the orchestrator, not pins.
- **Caveat, `[1m]` sessions:** if the session model is a `[1m]` long-context variant, pass an explicit model on subagent spawns. Inheriting `[1m]` can fail with an entitlement error.

## Superseded

The earlier per-component assignment table (opus/sonnet/haiku per skill) is historical and superseded by this guide.
