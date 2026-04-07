# Eval: Refine Skill — No Dependency Analysis, No Logging Calls

## Setup
Invoke `/momentum:refine` on a project where `stories/index.json` contains stories
with `depends_on` fields — including circular dependencies, missing targets, and
satisfied dependencies. Run the workflow through to completion (approve or reject
all findings).

## Expected Behavior

### No Dependency Analysis
1. The workflow does NOT detect circular dependency chains
2. The workflow does NOT flag missing dependency targets (depends_on references to
   slugs not in stories/index.json)
3. The workflow does NOT flag satisfied dependencies (depends_on entries where the
   dependency status is `done`)
4. No findings are generated in a "dependency issues" category
5. The consolidated findings report has no dependency-related section or entries

### No Logging Calls
6. The workflow does NOT call `momentum-tools log` at any point — not at workflow
   start, not after backlog presentation, not after discovery, not after findings
   review, not after applying changes, and not in the summary
7. No Bash invocations contain `momentum-tools` with the `log` subcommand
8. The workflow uses TaskCreate/TaskUpdate for progress tracking instead of logging

## Verification
- Search all Bash tool invocations during the workflow execution for any containing
  `momentum-tools` with `log` — there must be zero
- Search all findings presented to the developer for any in a "dependency" category
  — there must be zero
- Confirm the workflow proceeds through stories with dependency fields without
  analyzing or reporting on them
