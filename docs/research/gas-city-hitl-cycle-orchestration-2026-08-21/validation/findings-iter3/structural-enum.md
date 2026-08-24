# iter3 Validator: structural / Enumerator — 2 findings (1 minor, 1 low)
All 27 iter2 fixes verified landed; all 7 grep sweeps independently re-run and clean; corpus completeness/index/cross-refs/headers all pass.
STRUCTURAL3-E-001 | minor | cycle-fit:173 | "fan-out hazard in the row below" points at unrelated row :174; actual hazard row is :177 (last row). (= COHERENCE3-E-001) Fix: "the table's last row".
STRUCTURAL3-E-002 | low | dec035:49 | correction-marker wording backwards: "the pre-CRIT-004 framing below is superseded" precedes the CORRECTED text, reading as if the new text is superseded. Fix: reword per gate-mechanics:64's well-formed pattern.
