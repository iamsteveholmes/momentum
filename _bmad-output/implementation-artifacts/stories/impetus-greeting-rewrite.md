---
title: Impetus Greeting Rewrite — 9-State Narrative Orientation
story_key: impetus-greeting-rewrite
status: backlog
epic_slug: greeting-redesign
depends_on:
  - sprint-lifecycle-tools
  - sprint-index-schema-migration
touches:
  - skills/momentum/skills/impetus/workflow.md
change_type: skill-instruction
---

# Impetus Greeting Rewrite — 9-State Narrative Orientation

## Description

The current Impetus session orientation uses 3 rigid modes with fill bars and a
dashboard voice. The approved greeting mockup (`.claude/momentum/greeting-mockup.md`
v8) defines 9 greeting states with narrative prose in the KITT + Optimus Prime
voice. Architecture Decisions 37 (Greeting State Detection) and 38 (Narrative
Voice Contract) are the authoritative references.

This story replaces the entire Step 7 greeting system in `workflow.md` (lines
354-586) with 9-state detection, narrative prose, adaptive menus, and
state-based dispatch.

## Acceptance Criteria (Plain English)

1. Step 7 detects exactly 9 greeting states based on sprint index data:
   first-session-ever, active-not-started, active-in-progress, active-blocked,
   active-planned-needs-work, done-retro-needed, done-no-planned,
   no-active-nothing-planned, and no-active-planned-ready. Detection logic
   correctly distinguishes each state using sprint status, story statuses, and
   planning sprint presence.

2. Fill bar rendering is completely removed — no status-to-fill mapping, no
   MODE 1/2/3 bar rendering code remains anywhere in Step 7.

3. Each of the 9 states produces a narrative greeting matching the exact prose
   from greeting-mockup.md v8. Voice follows the Optimus Prime gravitas + KITT
   loyalty tone: "Stands ready." "Carried across the line." "Let's face it
   together."

4. The 3 hard-coded menus are replaced with state-driven adaptive menus. Each
   state presents 3-4 contextually appropriate action items rather than a
   one-size-fits-all menu.

5. Dispatch routes menu selections to the correct handler: Run/Continue sprint
   dispatches to sprint-dev, Plan/Finish planning dispatches to sprint-planning,
   Activate dispatches to momentum-tools sprint activate, Run retro shows a
   placeholder message, Refine backlog dispatches to create-story, and Triage
   shows a placeholder message.

6. Stats write uses `momentum-tools session stats-update` via Bash instead of
   the Write tool. Stats update fires after menu selection, not during greeting
   display.

7. First-session-ever gets a distinct identity declaration greeting. All other
   sessions get state-appropriate narrative greetings. The "Full walkthrough or
   decision points?" expertise-adaptive question is removed.

## Dev Notes

### What to implement in workflow.md Step 7 (lines 354-586)

**1. Replace sprint mode detection (lines 363-369) with 9-state detection:**

| State | Condition |
|---|---|
| `first-session-ever` | `momentum_completions == 0` AND no sprint history |
| `active-not-started` | active sprint exists, `status=="active"`, all stories `ready-for-dev` or `backlog` |
| `active-in-progress` | active sprint exists, stories moving, none blocked |
| `active-blocked` | active sprint exists, at least one story with unmet `depends_on` |
| `active-planned-needs-work` | active sprint exists + planning sprint exists with `status=="planning"` |
| `done-retro-needed` | `active.status=="done"` AND planning sprint exists |
| `done-no-planned` | `active.status=="done"` AND no planning sprint |
| `no-active-nothing-planned` | `active==null` AND `planning==null` |
| `no-active-planned-ready` | `active==null` AND `planning.status=="ready"` |

**2. Delete fill bar rendering (lines 371-459):**

Remove entirely: status-to-fill mapping, all MODE 1/2/3 bar rendering. No
remnants should remain.

**3. Replace with narrative greeting text:**

Each of the 9 states maps to exact prose from `greeting-mockup.md` v8. Voice:
Optimus Prime's gravitas + KITT's loyalty. Phrases like "Stands ready." "Carried
across the line." "Let's face it together."

**4. Replace menus (lines 487-524):**

Delete 3 hard-coded menus. Replace with state-driven adaptive 3-4 item menus
per state. Each state's menu offers only the actions that make sense for that
state.

**5. Update dispatch (lines 530-586):**

State-based dispatch mapping:

| Menu action | Dispatch target |
|---|---|
| Run/Continue sprint | sprint-dev |
| Plan/Finish planning | sprint-planning |
| Activate | `momentum-tools sprint activate` |
| Run retro | placeholder message |
| Refine backlog | create-story |
| Triage | placeholder message |

**6. Stats write via momentum-tools:**

Replace Write-tool stats update (lines 526-528) with
`momentum-tools session stats-update` via Bash. Move to after menu selection,
not during greeting display.

**7. Simplify expertise-adaptive (lines 463-472):**

First session is distinct (identity declaration). All other sessions get
state-appropriate greeting. Remove "Full walkthrough or decision points?"
question.

### Authoritative references

- `.claude/momentum/greeting-mockup.md` v8 — approved greeting prose
- Architecture Decision 37 — Greeting State Detection
- Architecture Decision 38 — Narrative Voice Contract
