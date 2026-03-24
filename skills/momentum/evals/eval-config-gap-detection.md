# Eval: Configuration Gap Detection

## Scenario

Given a developer's project is missing required Momentum configuration — e.g., protocol mapping table is undefined, MCP provider is not configured in `.mcp.json`, or ATDD tool binding is undefined — when Impetus detects the gap at session start or when a workflow step encounters it:

The skill should:
1. Surface the gap with a clear description of what's missing and why it matters to the developer's current workflow
2. Guide the developer through resolution conversationally — ask targeted questions, receive answers, record config, confirm — never dump a raw config file
3. Correctly classify the gap as blocking or non-blocking:
   - **Blocking:** missing MCP server required for the next workflow step; missing write target that would silently skip a required output
   - **Non-blocking:** everything else — workflow continues while gap is pending resolution
4. For non-blocking gaps, continue the workflow and offer resolution when the conversational floor is open
5. For blocking gaps, explain why the workflow cannot continue and guide resolution before proceeding

## Expected Behavior

**Detection timing:**
- At session start: scan `installed.json` and protocol mapping for known gap types
- At workflow step entry: detect if required config for this specific step is present

**Gap surfacing format:**
- Description of what's missing (e.g., "No ATDD tool binding is configured for this project")
- Why it matters (e.g., "The acceptance test step will skip test generation without it")
- Conversational resolution offer (e.g., "What test runner does this project use? I'll configure the binding.")

**Resolution conversation:**
- Impetus asks targeted questions one at a time
- Developer answers naturally
- Impetus records the answer and writes the config entry (with developer confirmation)
- Never shows a raw JSON/YAML config file for the developer to edit

## NOT Expected

- Showing a raw config file (JSON, YAML, or otherwise) for manual editing
- Blocking the entire workflow for a non-blocking gap (e.g., missing ATDD binding shouldn't prevent story selection)
- Silently proceeding past a blocking gap (e.g., missing MCP server for the next step)
- Detecting a gap but not explaining why it matters
- Detecting a gap but not offering resolution
- Firing gap detection while a subagent is running or a decision is pending
