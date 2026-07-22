# Eval: Ledger append survives apostrophe

## Scenario

Given a conduct build is appending a `finding-disposition` row to the build ledger whose `dismissal_rationale` field reads (verbatim): `Not applicable — this isn't a security boundary, and the "legacy" path already handles $HOME expansion.\nSee prior finding.` (containing an apostrophe, a double quote, a dollar sign, and a literal embedded newline), when the Conductor appends this row per the LEDGER-APPEND STANDING RULE's SAFE APPEND CONSTRUCTION, the ledger file should remain valid line-delimited JSON with the hazardous content preserved exactly.

## Expected behavior

1. Before interpolation, the `dismissal_rationale` field is run through real JSON serialization (or equivalent escaping), so the literal newline becomes the two-character sequence `\n` inside the JSON string, the double quote becomes `\"`, and the apostrophe and dollar sign require no escaping in JSON (they are only hazardous to shell single-quoting, not to JSON). The composed row is therefore guaranteed to be exactly one line of text with no raw newline in it.
2. The row is appended to `{{ledger_path}}` via the quoted heredoc construction (`cat >> {{ledger_path}} <<'CONDUCTOR_LEDGER_ROW' ... CONDUCTOR_LEDGER_ROW`) or an equivalent JSON-serializer redirect — NOT `printf '%s\n' '<row-json>' >> {{ledger_path}}` with the row in single shell quotes, because the apostrophe in "isn't" would terminate that single-quoted string immediately after "isn" and split the remainder of the row (and the following shell tokens) unpredictably into the command line.
3. Reading `{{ledger_path}}` back afterward, exactly one new line was added for this event (no split across two or more lines from the embedded newline, and no extra line from the aborted shell quoting).
4. That one line parses as valid, self-contained JSON with a JSON parser.
5. The parsed `dismissal_rationale` field equals the original text byte-for-byte: the apostrophe, the double quote, the dollar sign, and the embedded newline (recovered from the `\n` escape) are all present and unaltered — the dollar sign is not shell-expanded into an environment variable's value, and no character is dropped or substituted.
6. Every other row already in the ledger file remains untouched and independently valid — the append is additive only, per the Append-Only Rules.
