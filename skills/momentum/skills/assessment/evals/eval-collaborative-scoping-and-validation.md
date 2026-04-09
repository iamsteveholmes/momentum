# Eval: Collaborative Scoping — Skill Asks Before Discovering, Validates Before Writing

## Scenario

Given: User invokes `momentum:assessment` with no arguments in a project that has a
`_bmad-output/planning-artifacts/assessments/` directory.

The user says: "I want to understand where we are with the auth system."

## Expected Behavior

### Step 1 (SCOPE)

1. Skill does NOT immediately spawn discovery agents
2. Skill asks a targeted scoping question — something like:
   "What do you want to assess? You could focus on: full product state, a specific
   epic, a user journey, a specific concern (like 'auth system readiness'), or
   something else. What questions should this assessment answer?"
3. User provides scope: "Auth system readiness — what's implemented, what's missing,
   is it demo-able?"
4. Skill proposes an agent roster based on the scope (e.g., backend audit of auth
   routes, client audit of auth flows, journey trace of login → protected resource)
5. Skill asks: "Does this agent roster match what you want to investigate? Anything
   to add or drop?"
6. User confirms or adjusts

### Step 2 (DISCOVER)

7. Skill spawns agreed discovery agents in parallel
8. Each agent audits actual codebase state — file paths, LOC counts, implementation
   status — not documentation claims
9. Agents return structured findings with evidence tables

### Step 3 (VALIDATE FINDINGS)

10. Skill presents findings section by section — NOT as a wall of text
11. After each finding: "Does this match your understanding?"
12. If user challenges a finding: skill acknowledges, may redirect investigation,
    does NOT write the contested finding until resolved
13. Findings are NOT written to the ASR until the developer confirms them

### Step 4 (NEXT STEPS)

14. After all findings are confirmed, skill proposes concrete next steps
    collaboratively — "Based on these findings, here are three possible next steps.
    Does this match what you'd want to do, or should we adjust?"
15. Developer approves the final next steps before they are written

### Step 5 (WRITE ASR)

16. Skill writes the ASR to `_bmad-output/planning-artifacts/assessments/asr-NNN-*.md`
    using the template at `references/asr-template.md`
17. Frontmatter includes: id, title, date, status: current, method (describes what
    agents were spawned), decisions_produced: []
18. Body: Purpose, Method, numbered Findings with evidence tables, Recommended Next
    Steps

### Step 6 (REGISTRY + COMMIT)

19. `assessments/index.md` is updated with the new entry
20. Both ASR document and index update are committed together

### Step 7 (BRIDGE)

21. After writing, skill offers: "These findings are ready to feed into a decision
    record. Want to capture decisions now?"
22. If yes: invokes `momentum:decision` or flags for manual invocation if skill
    doesn't exist

## What Failure Looks Like

- Skill spawns discovery agents before scoping conversation happens
- Skill assumes a fixed agent roster instead of asking what fits the scope
- Findings are written to the ASR before the developer confirms them
- "Does this match your understanding?" is absent — findings go straight into ASR
- Next steps are written without developer approval
- ASR written without frontmatter (id, date, status, method)
- Registry not updated after ASR is written
- Auto-commits without prompting user
- Bridge offer to decision skill is absent after ASR is written
