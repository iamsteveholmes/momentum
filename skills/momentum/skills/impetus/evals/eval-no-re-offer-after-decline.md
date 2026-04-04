# Eval: No Re-Offer After Explicit Decline

## Scenario

Given a developer has explicitly declined a proactive offer — e.g., Impetus offered to walk through quick-spec and the developer said "No, continue as planned" — when the same or similar gap recurs later in the session or in a subsequent session:

The skill should:
1. NOT re-surface the same offer
2. Record the declination in journal thread state so it persists across session boundaries
3. Only re-surface if context has materially changed (e.g., the spec that triggered the offer was updated, the story changed, a new workflow step introduces a different aspect of the same gap)

## Expected Behavior

**Declination recording:**
- When a developer declines a proactive offer, Impetus records in journal thread state:
  - What was offered (gap type + specific context)
  - That it was declined
  - The context at time of decline (so material change can be detected later)

**Material change detection:**
A re-offer is justified only when:
- The underlying spec or config that triggered the original offer has been modified since the decline
- A different story or workflow step surfaces a genuinely new aspect of the gap
- The developer explicitly asks Impetus to revisit the topic

**Same-session behavior:**
If the developer declines an offer in step 3 of a workflow and the same gap is relevant in step 7, Impetus does not re-offer. The gap was acknowledged and declined.

**Cross-session behavior:**
If the developer declined in a previous session and the context has not changed, Impetus does not re-offer when the same gap appears in the next session.

## NOT Expected

- Re-surfacing the same offer after explicit decline with no context change
- Re-surfacing because a different workflow step encounters the same gap (same gap, same context = no re-offer)
- Treating "ignore" the same as "decline" — only explicit decline ("No", "Skip", "Continue as planned") triggers the no-re-offer rule
- Failing to re-offer when context has materially changed (the rule is no-re-offer without change, not no-re-offer ever)
- Storing declination data outside of journal thread state
