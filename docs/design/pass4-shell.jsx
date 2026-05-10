// Pass 4 shell — the long-scroll pane.
// 700px wide, scroll container, sticky anchor rail on the left edge, pane header on top.
// Scroll-spy: active anchor updates as the user scrolls. Click an anchor to smooth-jump.
//
// The three lenses are direct children of the scroll container. Each has an id
// so the anchor rail can jump to it. Scroll-spy uses IntersectionObserver with
// a top-weighted rootMargin so "what's active" means "what the reader is at".

const { T, FEATURES, SUMMARY } = window;

const LENSES = [
  { id: "features", label: "Features", meta: "what we're building" },
  { id: "sprints",  label: "Sprints",  meta: "how it's shipping" },
  { id: "flywheel", label: "Flywheel", meta: "what we're learning" },
];

// ─── Pane — outer 700px frame with header, scroll area, anchor rail ───────
function Pane({ tweaks, setTweaks, children }) {
  const scrollRef = React.useRef(null);
  const [active, setActive] = React.useState("features");

  // Scroll spy: whichever lens header crosses the top zone wins.
  React.useEffect(() => {
    const root = scrollRef.current;
    if (!root) return;
    const headers = [...root.querySelectorAll("[data-lens-id]")];
    const obs = new IntersectionObserver(
      (entries) => {
        // Among entries that are in the top band, pick the one nearest the top.
        const hits = entries
          .filter(e => e.isIntersecting)
          .map(e => ({ id: e.target.getAttribute("data-lens-id"), top: e.boundingClientRect.top }))
          .sort((a, b) => a.top - b.top);
        if (hits.length) setActive(hits[0].id);
      },
      { root, rootMargin: "0px 0px -70% 0px", threshold: [0, 0.01, 0.5, 1] }
    );
    headers.forEach(h => obs.observe(h));
    return () => obs.disconnect();
  }, []);

  const jumpTo = (id) => {
    const root = scrollRef.current;
    if (!root) return;
    const el = root.querySelector(`[data-lens-id="${id}"]`);
    if (!el) return;
    // Offset a little so the sticky pane header doesn't cover the lens header.
    const top = el.offsetTop - 8;
    root.scrollTo({ top, behavior: "smooth" });
  };

  const isDark = tweaks.dark;
  const bg = isDark ? T.paperDark : T.paper;
  const ink = isDark ? T.inkOnDark : T.ink;
  const inkMuted = isDark ? T.inkOnDarkMuted : T.inkMuted;
  const rule = isDark ? T.ruleDark : T.rule;

  return (
    <div style={{
      width: 700, height: 900,
      background: bg,
      border: `1px solid ${rule}`,
      boxShadow: "0 1px 0 rgba(0,0,0,0.04), 0 20px 40px -20px rgba(30,20,10,0.12)",
      borderRadius: 4,
      overflow: "hidden",
      display: "flex", flexDirection: "column",
      fontFamily: T.fontSans, color: ink,
      position: "relative",
    }}>
      <PaneHeader active={active} tweaks={tweaks} />
      <div style={{ flex: 1, display: "flex", minHeight: 0 }}>
        <AnchorRail active={active} onJump={jumpTo} tweaks={tweaks} />
        <div
          ref={scrollRef}
          style={{
            flex: 1, overflowY: "auto", overflowX: "hidden",
            scrollBehavior: "smooth",
          }}
        >
          {children}
        </div>
      </div>
    </div>
  );
}

// ─── Pane header ───────────────────────────────────────────────────────────
// Mono, terminal-ish. Signals cmux pane. Shows current lens as a breadcrumb.
function PaneHeader({ active, tweaks }) {
  const isDark = tweaks.dark;
  const bg = isDark ? "#1e1d1a" : "#2a2824";
  const current = LENSES.find(l => l.id === active);
  return (
    <div style={{
      height: 32, flexShrink: 0,
      background: bg, color: "rgba(255,252,245,0.9)",
      display: "flex", alignItems: "center", gap: 10,
      padding: "0 14px",
      fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
      borderBottom: `1px solid rgba(0,0,0,0.3)`,
    }}>
      <span style={{ display: "flex", gap: 6 }}>
        <Dot c="#ff5f57" />
        <Dot c="#febc2e" />
        <Dot c="#28c840" />
      </span>
      <span style={{ opacity: 0.55, marginLeft: 4 }}>cmux</span>
      <span style={{ opacity: 0.35 }}>›</span>
      <span style={{ opacity: 0.55 }}>feature-status</span>
      <span style={{ opacity: 0.35 }}>›</span>
      <span style={{ color: "#e8b974" }}>{current?.label.toLowerCase()}</span>
      <span style={{ flex: 1 }} />
      <span style={{ opacity: 0.45, fontSize: 10 }}>⌘K to jump</span>
    </div>
  );
}

function Dot({ c }) {
  return <span style={{ width: 10, height: 10, borderRadius: "50%", background: c, display: "inline-block" }} />;
}

// ─── Anchor rail — sticky left column, active indicator follows scroll ─────
function AnchorRail({ active, onJump, tweaks }) {
  const isDark = tweaks.dark;
  const ruleC = isDark ? T.ruleDark : T.rule;
  const inkQuiet = isDark ? "rgba(255,252,245,0.45)" : T.inkQuiet;
  return (
    <div style={{
      width: 52, flexShrink: 0,
      borderRight: `1px solid ${ruleC}`,
      padding: "18px 0",
      display: "flex", flexDirection: "column", alignItems: "center", gap: 2,
      background: isDark ? "rgba(255,255,255,0.015)" : "rgba(0,0,0,0.015)",
    }}>
      {LENSES.map((l, i) => (
        <AnchorItem
          key={l.id}
          n={i + 1}
          label={l.label}
          active={active === l.id}
          onClick={() => onJump(l.id)}
          tweaks={tweaks}
        />
      ))}
    </div>
  );
}

function AnchorItem({ n, label, active, onClick, tweaks }) {
  const isDark = tweaks.dark;
  const activeInk = isDark ? "#f0eee9" : "#1e1d1a";
  const quietInk = isDark ? "rgba(255,252,245,0.42)" : "rgba(40,30,20,0.42)";
  const accent = "#5863a8";
  return (
    <button
      onClick={onClick}
      style={{
        all: "unset", cursor: "pointer",
        width: 44, padding: "14px 0",
        display: "flex", flexDirection: "column", alignItems: "center", gap: 6,
        position: "relative",
        transition: "color 180ms ease",
        color: active ? activeInk : quietInk,
      }}
    >
      {/* Active indicator bar */}
      <span style={{
        position: "absolute", left: -1, top: "50%", transform: "translateY(-50%)",
        width: 2, height: active ? 28 : 0,
        background: accent,
        transition: "height 220ms cubic-bezier(0.2, 0.7, 0.2, 1)",
        borderRadius: 1,
      }} />
      <span style={{
        fontFamily: T.fontMono, fontSize: 10,
        opacity: active ? 1 : 0.6, letterSpacing: 0.5,
      }}>
        0{n}
      </span>
      <span style={{
        fontFamily: T.fontSans, fontSize: 10.5, letterSpacing: 0.4,
        writingMode: "vertical-rl", transform: "rotate(180deg)",
        textTransform: "uppercase", fontWeight: active ? 600 : 500,
      }}>
        {label}
      </span>
    </button>
  );
}

Object.assign(window, { Pane, LENSES });
