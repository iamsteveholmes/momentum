# Eval: Install Route — File Operations Use Bash, Not Write/Edit

## Scenario

Given a developer invokes `/momentum` and the preflight returns `route: 'first-install'`, when Impetus executes the install workflow (steps 2-5) — including copying rule files, writing installed.json, and writing global-installed.json — all file mutation operations should use Bash tool calls (cp, mkdir, python3 -c, tee) rather than Write or Edit tool calls.

## Expected Behavior

1. Step 3 (execute install actions):
   - `add` actions: copy source to target via Bash (`cp` or `python3 -c "import shutil; ..."`)
   - Parent directory creation: `mkdir -p` via Bash
   - `delete` actions: `rm` via Bash
   - `migration` actions: follow instruction file, execute mutations via Bash
2. Step 4 (write state files):
   - `global-installed.json`: written via Bash (`python3 -c` or `tee`)
   - `installed.json`: written via Bash (`python3 -c` or `tee`)
3. Step 5 (gitignore fix if needed): `.gitignore` edits via Bash (`python3 -c` or `sed`)
4. No Write tool calls anywhere in the install path
5. No Edit tool calls anywhere in the install path

## NOT Expected

- Write tool called to create or overwrite any file
- Edit tool called to modify any file
- Tool calls outside the allowed set: Read, Glob, Grep, Agent, Bash

## Why This Matters

The `allowed-tools` frontmatter restriction deterministically blocks Write and Edit. If the install
workflow relied on these tools, it would fail at runtime under the restriction. Task 0 is to refactor
all such calls to Bash equivalents before the restriction is added.
