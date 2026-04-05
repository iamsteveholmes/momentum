# Eval: Guidelines Gate — Detects Missing Guidelines

## Setup
A sprint plan includes two stories:
- Story A is assigned a specialist for domain "kotlin-compose"
- Story B is assigned a specialist for domain "kotest"

The project `.claude/rules/` directory contains `kotlin-compose.md` but does NOT contain `kotest.md`, `kotest-5.md`, or any other file matching the "kotest" domain.

## Expected Behavior
1. The guidelines verification gate runs after specialist assignment in Step 5
2. The gate checks `.claude/rules/` for files matching each specialist domain
3. Story A's domain ("kotlin-compose") is found — no warning for that domain
4. Story B's domain ("kotest") is NOT found — a warning is surfaced:
   `! Missing guidelines for kotest — affects: Story B`
5. The consolidated warning lists only domains that are missing, not domains that are present

## Verification
- Gate produces a warning for "kotest" domain listing Story B
- Gate does NOT produce a warning for "kotlin-compose" domain
- Warning uses Impetus `!` symbol for the warning prefix
