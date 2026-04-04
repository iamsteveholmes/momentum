# Eval: Plugin Skill Spawn Names

## Setup
Read the Impetus workflow.md and all skill workflow files.

## Expected Behavior
1. All skill spawn/invoke references use `momentum:<name>` format (not `momentum-<name>`)
2. Examples: `momentum:dev`, `momentum:avfl`, `momentum:create-story`, `momentum:plan-audit`
3. No spawn reference uses the old `momentum-<name>` format
4. Sub-skill references within a skill (e.g., AVFL sub-skills) use relative paths
