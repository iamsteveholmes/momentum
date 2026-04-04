# Eval: Proactive Offer, Never Block

## Scenario

Given Impetus detects an information gap or a step the developer is about to skip — e.g., developer is about to implement without an accepted spec, or a configuration gap is detected mid-workflow — when the conversational floor is open (no subagent running, no pending decision):

The skill should:
1. Surface the offer using `?` symbol and proactive-offer framing — present options without blocking on a response
2. Allow the developer to decline and continue without the workflow stalling
3. Retain developer agency: the offer is an option, not a gate

## Expected Behavior

**Offer format:**
```
?  I notice [gap description]. Want me to [resolution action]? Or continue as planned?
```

The developer can:
- Accept the offer → Impetus guides resolution
- Decline the offer → workflow continues immediately, no follow-up about this offer
- Ignore the offer and ask about something else → Impetus follows the developer's lead

**Floor-open gate:**
Proactive offers only fire when:
- No subagent is currently running
- No pending decision awaits the developer's response
- The workflow is at a natural pause point or transition

## NOT Expected

- Blocking the workflow to wait for a response to the proactive offer
- Firing a proactive offer while a subagent is running or while the developer has a pending decision
- Using mandatory question framing ("You must configure X before continuing") for non-blocking gaps
- Repeating the offer if the developer declines (see eval-no-re-offer-after-decline)
- Omitting the `?` symbol from proactive offer framing
- Presenting the offer as a requirement rather than an option
