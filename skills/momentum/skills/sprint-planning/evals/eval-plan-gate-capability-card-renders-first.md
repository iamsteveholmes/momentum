# Eval: Capability Sign-Off Card Renders First, Even With Zero Other Forks

**ID:** eval-plan-gate-capability-card-renders-first
**Change-type:** skill-instruction
**Phase:** Developer review (Step 7) — plan gate rendering

## Scenario A: Zero other genuine forks

Given a sprint plan where AVFL returned CLEAN, coherence checks found no open mismatches, and no
other fork-detection rule fired (all stories are `✓ batch`) — historically this would render zero
decision cards

When Step 7 (Phase A synthesis + Phase B render) builds the plan gate

Then:

1. `{{genuine_forks}}` is NOT empty — it contains exactly one entry: the capability sign-off
   fork, built from the declared `{{goal_conditions}}` / `{{goal}}`.
2. The rendered gate's decision-cards section shows exactly one `.card`, and it is the capability
   card — not the "no forks found, clean-plan path" message that would have appeared before this
   story.
3. The capability card is the FIRST card in the section, positioned ahead of where any coherence
   or other fork would appear.
4. The card's title asks, in the developer's own declared plain language, "After this sprint a GM
   will be able to ___" — filled from `{{goal}}` / `{{goal_conditions}}`, not a generic template
   string with no substance.
5. The card carries all five ForkItem fields inline: What, Why it matters, Evidence,
   Recommendation, Options — and Options lists exactly "approve", "change", "reject" (or
   equivalent plain-language phrasing of those three).
6. `FORK_COUNT` in the gate's JavaScript equals 1 (not 0) — the anti-rubber-stamp verdict input
   for this fork is rendered and required.

## Scenario B: Six other genuine forks already present

Given a sprint plan with 6 other genuine forks detected (below the 7-cap)

When Step 7 builds the gate

Then:

1. The capability fork is prepended — it is fork position 1, and the other 6 forks follow it in
   their existing order.
2. The total card count is 7 (1 capability + 6 other) — the capability fork is exempt from the
   7-fork cap and sits alongside, not counted against, the other detected forks' budget.

## Scenario C: Seven other genuine forks already present (at the cap)

Given a sprint plan with 7 other genuine forks detected (at the 7-cap)

When Step 7 builds the gate

Then:

1. The capability fork is never dropped by the 7-fork cap even though the other forks already
   fill all 7 slots — it still renders as an 8th card, exempt from the cap like a coherence fork.
2. The total card count is 8 (1 capability + 7 other) — none of the 7 other forks is displaced to
   make room for it.

## Pass Criteria

- The capability card renders even when every other fork-detection rule finds nothing.
- It is always the first decision card, before coherence and other forks.
- It carries all five required fields, worded from the actual declared capability (no bare
  placeholder text).
- `FORK_COUNT` includes it in all cases.

## Fail Criteria

- Zero other forks renders the pre-existing "clean-plan, no forks" message instead of the
  capability card.
- The capability card renders after other forks, or is folded into the coherence-fork block.
- The capability card is dropped when 7 other forks already fill the cap.
- The card's title or What field is generic ("Review the sprint capability") rather than the
  developer's own declared plain-language statement.
