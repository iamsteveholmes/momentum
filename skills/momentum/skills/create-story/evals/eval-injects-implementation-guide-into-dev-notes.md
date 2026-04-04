# Eval: Injects Momentum Implementation Guide into story Dev Notes

## Scenario

Given a Momentum story file that has been produced by bmad-create-story, classified as having 2 tasks:
- Task 1: Create `skills/momentum/skills/validate/SKILL.md` → `skill-instruction`
- Task 2: Update `.claude/settings.json` hooks → `rule-hook`

The story file has a `## Dev Notes` section followed by `## Dev Agent Record`. The skill is now in Step 4.

## Expected behavior

The skill should:
1. Compose a `## Momentum Implementation Guide` section containing:
   - A header with `**Change Types in This Story:**` listing Task 1 → skill-instruction (EDD) and Task 2 → rule-hook (functional verification)
   - A `### skill-instruction Tasks: Eval-Driven Development (EDD)` section with EDD steps 1-5, NFR compliance requirements (NFR1, FR23, NFR3, NFR12), and DoD checklist items with {{SKILL_DIR}} substituted as `validate`
   - A `### rule-hook Tasks: Functional Verification` section with functional verification steps and DoD checklist items
   - NO `### script-code Tasks` section (not present in this story)
   - NO `### config-structure Tasks` section (not present in this story)
2. Inject the composed section at the END of the `## Dev Notes` section, immediately before `## Dev Agent Record`
3. Save the story file with the injected section
4. Output: "Momentum Implementation Guide injected into [story file path]"

The skill should NOT include templates for absent change types. It should NOT prompt the user during injection.
