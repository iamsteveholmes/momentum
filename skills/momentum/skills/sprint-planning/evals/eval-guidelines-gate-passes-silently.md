# Eval: Guidelines Gate — Passes Silently When All Present

## Setup
A sprint plan includes two stories:
- Story A is assigned a specialist for domain "kotlin-compose"
- Story B is assigned a specialist for domain "kotest"
- Story C uses the base Dev agent (no specialist)

The project `.claude/rules/` directory contains both `kotlin-compose.md` and `kotest.md`.

## Expected Behavior
1. The guidelines verification gate runs after specialist assignment in Step 5
2. The gate checks `.claude/rules/` for files matching each specialist domain
3. Both specialist domains have matching files — all checks pass
4. Story C has no specialist — gate records "n/a" and skips the check
5. No warning output is produced
6. No developer interaction is required
7. Planning continues directly to the touches overlap check and wave building

## Verification
- No warning text appears in the Step 5 output
- No developer prompt is presented for guidelines
- The gate adds zero user-facing latency when all guidelines are present
