// Shared small components — badges, meta fields, section headers.

const { T, BADGE_BY_KEY, TERMINAL_STATES } = window;

function Badge({ state, size = "sm" }) {
  const b = BADGE_BY_KEY[state];
  if (!b) return null;
  const isTerminal = TERMINAL_STATES.has(state);
  const px = size === "sm" ? "2px 8px 2px 6px" : "3px 10px 3px 8px";
  const fz = size === "sm" ? 11 : 12;
  const dotSize = size === "sm" ? 6 : 7;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: px,
      fontFamily: T.fontMono,
      fontSize: fz, fontWeight: 500,
      letterSpacing: 0.2,
      color: b.fg,
      background: b.bg,
      border: `1px solid ${isTerminal ? "transparent" : "rgba(0,0,0,0.04)"}`,
      borderRadius: 3,
      whiteSpace: "nowrap",
      opacity: isTerminal ? 0.75 : 1,
    }}>
      <span style={{
        width: dotSize, height: dotSize, borderRadius: "50%",
        background: b.dot,
        boxShadow: isTerminal ? "none" : `0 0 0 2px ${b.bg}`,
        opacity: isTerminal ? 0.7 : 1,
      }} />
      {b.label}
    </span>
  );
}

function GapFlag({ prominent = false, note }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: "2px 7px 2px 6px",
      fontFamily: T.fontMono,
      fontSize: 11, fontWeight: 500,
      color: T.gap,
      background: prominent ? T.gapSoft : "transparent",
      border: `1px solid ${prominent ? "rgba(168,90,42,0.18)" : "transparent"}`,
      borderRadius: 3,
      whiteSpace: "nowrap",
    }} title={note}>
      <svg width="10" height="10" viewBox="0 0 10 10" fill="none" aria-hidden>
        <path d="M5 1.2L9 8.4H1L5 1.2z" stroke={T.gap} strokeWidth="1.1" strokeLinejoin="round" />
        <circle cx="5" cy="6.6" r="0.6" fill={T.gap} />
      </svg>
      gap
    </span>
  );
}

function StoryFraction({ done, total, muted = false }) {
  return (
    <span style={{
      fontFamily: T.fontMono,
      fontSize: 12,
      color: muted ? T.inkFaint : T.inkMuted,
      letterSpacing: 0.3,
      whiteSpace: "nowrap",
    }}>
      {done}<span style={{ color: T.inkFaint, margin: "0 1px" }}>/</span>{total}
      <span style={{ color: T.inkFaint, marginLeft: 4 }}>stories</span>
    </span>
  );
}

function TypeTag({ type }) {
  return (
    <span style={{
      fontFamily: T.fontMono,
      fontSize: 10,
      letterSpacing: 1.2,
      color: T.inkQuiet,
      textTransform: "uppercase",
    }}>{type}</span>
  );
}

function Breadcrumb({ items }) {
  return (
    <nav style={{
      fontFamily: T.fontMono,
      fontSize: 12,
      color: T.inkQuiet,
      letterSpacing: 0.2,
    }}>
      {items.map((item, i) => (
        <span key={i}>
          {i > 0 && <span style={{ margin: "0 8px", color: T.inkFaint }}>›</span>}
          <span style={{
            color: i === items.length - 1 ? T.inkMuted : T.inkQuiet,
          }}>{item}</span>
        </span>
      ))}
    </nav>
  );
}

function SumStat({ n, label, state, gap }) {
  const b = state ? (window.BADGE_BY_KEY[state]) : null;
  const dot = gap ? T.gap : (b ? b.dot : T.inkQuiet);
  return (
    <span style={{
      display: "inline-flex", alignItems: "baseline", gap: 7,
      color: T.inkMuted,
    }}>
      <span style={{
        display: "inline-block",
        width: 6, height: 6, borderRadius: "50%",
        background: dot, transform: "translateY(-1px)",
      }} />
      <span style={{ color: T.ink, fontWeight: 500 }}>{n}</span>
      <span style={{ color: T.inkQuiet }}>{label}</span>
    </span>
  );
}

Object.assign(window, { Badge, GapFlag, StoryFraction, TypeTag, Breadcrumb, SumStat });
