# Eval: 2-Item Menu — First-Time User Orientation Unaffected

## Story

2a-3: Session-Open Menu Redesign

## Setup

- `momentum_completions = 0` (first-time user)
- Momentum freshly installed, no prior sessions

## Expected Behavior

1. Full orientation walkthrough fires (expertise-adaptive: first encounter path)
2. The 2-item menu may not appear during the walkthrough — this is acceptable
3. The first-encounter orientation path is not broken or bypassed
4. Developer does not see the 2-item menu presented without context

## Fail Conditions

- First-time user sees the 2-item menu with no orientation context
- Full walkthrough is suppressed (abbreviated orientation shown to first-time user)
- Orientation path errors out or behaves unexpectedly
