# Eval: With two pending resume cards, only the leading card's resurface_count increments

**Surface under test:** Session-start behavior in `.claude/rules/impetus.md` — multiple pending
cards, the count line, and the `resurface_count` increment rule.

**Standard:** DEC-040 D5 and `skills/momentum/skills/conductor/references/resume-card.md`.

## Scenario

**Given:** Two `resume-card.json` files with `status: "pending"` exist under different sprint
directories. Card A has the more recent `waited_since`; card B is older. Both start with a known
`resurface_count` and `waited_since`.

**When:** A fresh session starts and Impetus runs its session-start behavior.

**Then:**

1. Card A (most recent `waited_since`) leads the report with its question and options.
2. Card B is named only in a single count line (e.g. "1 more gate also waiting"), not rendered.
3. Card A's `resurface_count` is incremented by 1; its `waited_since` is unchanged.
4. Card B's file is not rewritten: `resurface_count` and `waited_since` are both unchanged.

## Pass Criteria

Exactly one card is rendered and incremented; the other appears only in the count line and its file
is byte-identical before and after the greeting.

## Fail Criteria

Both cards are incremented; card B is rewritten in any way; card B is rendered in full; the count
line is missing.

## Verification Method

Place two fixture pending cards under distinct sprint directories, start a fresh session, and
compare both card files before and after the greeting.
