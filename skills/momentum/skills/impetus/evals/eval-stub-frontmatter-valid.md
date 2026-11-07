# Eval: Stub SKILL.md Has Valid Frontmatter

## Scenario

Given the `skills/momentum/SKILL.md` file is read by an Agent Skills loader, the SKILL.md should:

- Have a valid `name` field equal to `momentum`
- Have a `description` field of ≤150 characters
- Have an `effort` frontmatter field present and no `model` pin
- Pass YAML frontmatter parsing without error

## Expected Behavior

An Agent Skills installer or validator that reads the SKILL.md frontmatter block should:
1. Extract `name: momentum` successfully
2. Confirm `description` character count ≤ 150
3. Confirm the `effort:` field is present and no `model:` pin is declared
4. Not produce any parse or validation errors
