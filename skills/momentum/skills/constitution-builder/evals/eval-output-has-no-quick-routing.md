# Eval: No ## Quick Routing section in output under any write mode

## Scenario

Given: The constitution-builder skill is invoked with any valid `write_mode` value
(`in_place_skill`, `composed_agent_file`, or `standalone_constitution`) and a target project
with at least one domain and one knowledge base configured.

The skill completes its full workflow and writes or displays the generated constitution content.

## Expected outcome

The generated and written constitution contains:
- An embedded-facts section (project identity, stack, conventions)
- A KB-sourced context section (populated via wiki-query lookups)
- The wiki-query interface block (DEC-018 canonical form)

The generated and written constitution does NOT contain:
- Any `## Quick Routing` section
- Any symptom→`wiki-query` routing table entries
- Any per-agent diagnostic table
- Any agent-specific `## Permissions` section
- Any agent-specific `## Standing Rules` section

## Pass criteria

- The written/displayed output contains none of the prohibited sections
- No `## Quick Routing` heading appears at any level
- No symptom → wiki-query routing rows appear under any heading
- Embedded facts, KB-sourced context, and wiki-query interface block ARE present
- The completion message does NOT reference "routing entries" as something generated

## Fail criteria

- A `## Quick Routing` section appears in the output
- Any symptom→`wiki-query` routing rows appear under any heading in the output
- The embedded-facts section is absent
- The wiki-query interface block is absent
- The skill's completion message says routing entries were generated
