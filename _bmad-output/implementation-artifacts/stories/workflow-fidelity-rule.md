---
title: Workflow Fidelity Rule — Delegation Steps Are Binding
story_key: workflow-fidelity-rule
status: done
epic_slug: quality-enforcement
depends_on: []
touches:
  - skills/momentum/references/rules/workflow-fidelity.md
  - .claude/rules/workflow-fidelity.md
change_type: rule-hook
---

# Workflow Fidelity Rule — Delegation Steps Are Binding

## Description

When executing Momentum workflows, delegation steps (spawn X, invoke X)
were being bypassed as "efficiency shortcuts." This breaks separation of
concerns, consistent quality, and auditability.

This story adds a `workflow-fidelity.md` rule to the Momentum plugin's
bundled rules that enforces: delegation is not optional, parallelism is
expected, and missing skills must be flagged rather than silently replaced.

## Acceptance Criteria (Plain English)

1. A rule file exists at `skills/momentum/references/rules/workflow-fidelity.md`
   that ships with the Momentum plugin.

2. The rule states that workflow delegation steps are binding — spawning
   the specified skill/agent is required, not optional.

3. The rule covers three scenarios: delegation is mandatory, parallelism
   is expected for independent items, and missing skills must be flagged.

4. The rule is deployed to `.claude/rules/` for the current project
   and `~/.claude/rules/` globally.

## Dev Notes

Single rule file — no code changes needed. Impetus deploys it to project
and global rules directories on install, same as existing rules.
