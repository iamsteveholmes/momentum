# Momentum CLI Reference

## Version
v1.0.0 | Released: 2026-03-01

## Overview
The Momentum CLI (`mo`) provides command-line access to workflow validation and quality scoring. All commands require authentication via `mo auth login` before first use.

## Installation

Install via Homebrew:
```bash
brew install momentum-cli
```

Verify installation:
```bash
mo --version
# Output: mo version 1.0.0
```

## Authentication

### mo auth login
Authenticates the CLI with your Momentum account. Opens a browser window to complete OAuth2 login. Credentials are stored in `~/.mo/credentials.json`.

```bash
mo auth login
# Output: Opening browser for authentication...
#         Authenticated as user@example.com
```

### mo auth logout
Removes stored credentials from `~/.mo/credentials.json`.

```bash
mo auth logout
# Output: Logged out successfully.
```

### mo auth status
Displays the currently authenticated user, or "Not authenticated" if no credentials are stored.

```bash
mo auth status
# Output: Authenticated as user@example.com
```

## Validation Commands

### mo validate
Runs AVFL validation on a file or directory.

**Syntax:**
```bash
mo validate <path> [options]
```

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `path` | Yes | Path to the file or directory to validate |

**Options:**

| Option | Default | Description |
|---|---|---|
| `--profile` | `full` | Validation profile: `gate`, `checkpoint`, or `full` |
| `--expert` | `auto` | Domain expert role for validation and fixing. `auto` infers from file type. |
| `--source` | none | Path to source material file for factual accuracy checks |
| `--output` | stdout | Path to write the validation report. If omitted, prints to stdout. |

**Exit codes:**

| Code | Meaning |
|---|---|
| 0 | Validation passed (CLEAN) |
| 1 | Validation failed (GATE_FAILED or MAX_ITERATIONS_REACHED) |
| 2 | Invalid arguments or missing required file |
| 3 | Authentication error — run `mo auth login` |

**Example:**
```bash
mo validate docs/architecture.md --profile full --source docs/requirements.md --output report.md
```

### mo validate --profile gate
Runs a structural-only pass. Exits immediately on failure with code 1; does not attempt fixes.

```bash
mo validate spec.json --profile gate
# Output on pass:  CLEAN (score: 98/100)
# Output on fail:  GATE_FAILED (score: 62/100) — 3 findings. See report for details.
```

## Scoring

Validation produces a score from 0 to 100, starting at 100 and deducting by finding severity:

| Severity | Deduction | Description |
|---|---|---|
| critical | −15 | Fundamentally broken — output unusable without fixing |
| high | −8 | Significant error that undermines quality |
| medium | −3 | Notable issue that degrades quality |
| low | −1 | Minor or cosmetic issue |

A score of 95 or above is considered **CLEAN** (passing). A score below 95 requires remediation.

## Configuration

The CLI reads configuration from `~/.mo/config.json` if present. All settings are optional and override CLI defaults.

```json
{
  "default_profile": "full",
  "default_expert": "auto",
  "output_format": "markdown"
}
```

**Supported `output_format` values:** `markdown` (default), `json`, `plain`

## Error Messages

| Message | Cause | Resolution |
|---|---|---|
| `Authentication required` | No credentials stored | Run `mo auth login` |
| `File not found: <path>` | Specified path does not exist | Check the path and try again |
| `Invalid profile: <value>` | `--profile` value is not `gate`, `checkpoint`, or `full` | Use one of the three valid values |
| `Source file not found: <path>` | `--source` path does not exist | Check the source path and try again |
