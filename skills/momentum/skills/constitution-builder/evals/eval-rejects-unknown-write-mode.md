# Eval: Unknown write_mode value is rejected and names all three valid values

## Scenario

Given: The constitution-builder skill is invoked with a `write_mode` argument that is not one
of the three accepted values. Example invalid values: `"full_agent"`, `"hot"`, `"inline"`, or
any string not in `{in_place_skill, composed_agent_file, standalone_constitution}`.

## Expected outcome

The skill immediately rejects the invocation without generating or writing any constitution
content. The rejection message explicitly names all three accepted values:
- `in_place_skill`
- `composed_agent_file`
- `standalone_constitution`

The skill does not proceed to Phase 2 or any content-generation step.

## Pass criteria

- Skill halts at the write_mode validation step
- No constitution content is generated or written to disk
- The developer-facing message names exactly the three valid values
- All three valid values appear in the rejection message (none omitted)
- No fourth or alternative value is listed as accepted

## Fail criteria

- Skill proceeds to generate or write content despite the invalid write_mode
- Rejection message omits any of the three valid values
- Rejection message includes a value outside the accepted set as valid
- Skill asks clarifying questions and continues rather than rejecting
