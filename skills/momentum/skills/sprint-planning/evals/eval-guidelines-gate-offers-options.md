# Eval: Guidelines Gate — Offers Three Options Per Missing Domain

## Setup
A sprint plan includes three stories:
- Story A is assigned specialist domain "react-native" — no guidelines file exists
- Story B is also assigned specialist domain "react-native" — same missing domain
- Story C is assigned specialist domain "fastapi" — no guidelines file exists

The project `.claude/rules/` contains no files matching "react-native" or "fastapi".

## Expected Behavior
1. The gate detects two missing domains: "react-native" and "fastapi"
2. Stories A and B share the same missing domain — they are consolidated into one warning entry
3. The developer sees a consolidated warning:
   ```
   ! Missing guidelines for 2 specialist domains:
     ! react-native — affects: Story A, Story B
     ! fastapi — affects: Story C
   ```
4. For each missing domain, the developer is offered three options:
   - **(G)** Generate — invoke momentum:agent-guidelines, pause planning, re-check after completion
   - **(P)** Proceed — keep specialist, record guidelines as "missing"
   - **(D)** Downgrade — replace specialist with base Dev agent, record as "skipped"
5. If developer chooses G for react-native:
   - momentum:agent-guidelines is invoked for the react-native domain
   - After completion, the gate re-checks `.claude/rules/` for react-native files
   - If found, guidelines_status for Stories A and B becomes "present"
6. If developer chooses P for fastapi:
   - Story C retains its fastapi specialist
   - guidelines_status for Story C is recorded as "missing"
7. If developer chooses D for a domain:
   - Affected stories are reassigned to the base Dev agent
   - guidelines_status for those stories is recorded as "skipped"

## Verification
- Consolidated warnings group stories by missing domain
- Three distinct options (G/P/D) are presented per missing domain
- Each option produces the correct guidelines_status value
- The generate option pauses planning and re-checks after completion
