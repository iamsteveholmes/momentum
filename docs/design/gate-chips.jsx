// Gate-chip primitive — new for Pass 3.
//
// Why a new primitive:
//   State badges answer "what's the condition of this thing?" (one value per thing).
//   Gates answer "did this thing pass three independent checks?" (three values, same thing).
//   A single state badge can't carry three booleans without distortion. A gate trio
//   makes the three checks visible at glance without inventing a combined badge.
//
// Family resemblance (inherited from badge system):
//   - JetBrains Mono, lowercase, 10–11px — same voice
//   - Same muted greens/reds from the state family (matched chroma)
//   - Same terminal-opacity pattern: pending / n/a reads at ~55%
//   - Dot or bar, 6px-ish, same visual mass as state-badge dot
//
// Distinct from state badges so you can tell at a glance:
//   - Three cells in a row, not one capsule
//   - Labels are the GATE name (avfl/cr/e2e), not a state word
//   - No pill background; just the row of cells, on its own baseline

const { T } = window;

const GATE_COLORS = {
  // Pull from the existing state palette so chroma is matched.
  pass:    { fg: "#2a5a42", dot: "#3e7a5a", bg: "rgba(62,122,90,0.10)",  bd: "rgba(62,122,90,0.25)" },
  fail:    { fg: "#7a3a3a", dot: "#a85252", bg: "rgba(168,82,82,0.10)",  bd: "rgba(168,82,82,0.25)" },
  pending: { fg: "#5a5a5a", dot: "#8a8a8a", bg: "rgba(138,138,138,0.08)", bd: "rgba(138,138,138,0.20)" },
  "n/a":   { fg: "#8a8678", dot: "#b5b0a2", bg: "rgba(138,134,120,0.06)", bd: "rgba(138,134,120,0.14)" },
};

function GateChip({ gate, state }) {
  const c = GATE_COLORS[state] || GATE_COLORS.pending;
  const terminal = state === "pending" || state === "n/a";
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 5,
      padding: "2px 6px 2px 5px",
      fontFamily: T.fontMono, fontSize: 10, fontWeight: 500,
      letterSpacing: 0.3,
      color: c.fg,
      background: c.bg,
      border: `1px solid ${c.bd}`,
      borderRadius: 2,
      opacity: terminal ? 0.75 : 1,
      whiteSpace: "nowrap",
    }}>
      <span style={{
        width: 5, height: 5, borderRadius: "50%",
        background: c.dot,
        opacity: terminal ? 0.7 : 1,
      }} />
      {gate}
    </span>
  );
}

function GateTrio({ gates, compact = false }) {
  // gates: { avfl, cr, e2e }
  return (
    <span style={{
      display: "inline-flex", alignItems: "center",
      gap: compact ? 4 : 5,
      fontFamily: T.fontMono,
    }}>
      <GateChip gate="avfl" state={gates.avfl} />
      <GateChip gate="cr"   state={gates.cr}   />
      <GateChip gate="e2e"  state={gates.e2e}  />
    </span>
  );
}

// Minimal dot-only variant — for when a row already has a story-title column
// and you want the gates to read as a tiny signature at the right edge.
function GateDots({ gates, title }) {
  const entries = [
    ["avfl", gates.avfl], ["cr", gates.cr], ["e2e", gates.e2e],
  ];
  return (
    <span title={title || entries.map(([g, s]) => `${g}:${s}`).join(" · ")}
          style={{ display: "inline-flex", gap: 3 }}>
      {entries.map(([g, s]) => {
        const c = GATE_COLORS[s] || GATE_COLORS.pending;
        return (
          <span key={g} style={{
            width: 6, height: 6, borderRadius: "50%",
            background: c.dot,
            opacity: (s === "pending" || s === "n/a") ? 0.55 : 1,
            boxShadow: `0 0 0 1px ${c.bd}`,
          }} />
        );
      })}
    </span>
  );
}

// Gate-health summary for a whole sprint (header strip).
// Visual mass: three small bars, labeled beneath. Honest about pending.
function GateHealthBar({ counts }) {
  // counts: { avfl: {pass, fail, pending}, cr: {...}, e2e: {...} }
  const row = ["avfl", "cr", "e2e"];
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
      gap: 10,
      fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.3,
      color: T.inkQuiet,
    }}>
      {row.map(g => {
        const c = counts[g] || { pass: 0, fail: 0, pending: 0 };
        const total = c.pass + c.fail + c.pending || 1;
        const passW = (c.pass / total) * 100;
        const failW = (c.fail / total) * 100;
        const penW  = (c.pending / total) * 100;
        return (
          <div key={g}>
            <div style={{
              display: "flex", alignItems: "baseline", justifyContent: "space-between",
              marginBottom: 4,
            }}>
              <span>{g}</span>
              <span style={{ color: T.inkFaint }}>
                {c.pass}<span style={{ margin: "0 2px" }}>/</span>{total}
              </span>
            </div>
            <div style={{
              height: 4, display: "flex",
              border: `1px solid ${T.rule}`, background: T.paperAlt,
            }}>
              <div style={{ width: `${passW}%`, background: GATE_COLORS.pass.dot }} />
              <div style={{ width: `${failW}%`, background: GATE_COLORS.fail.dot }} />
              <div style={{ width: `${penW}%`,  background: GATE_COLORS.pending.dot, opacity: 0.5 }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

Object.assign(window, { GateChip, GateTrio, GateDots, GateHealthBar, GATE_COLORS });
