// Nav chrome comparison — three candidates at the 700px half-width target.
// Each variant renders the same Features-snippet inside so chrome weight is
// the only axis of variation. Not full-populated; that's on purpose.

const { T, FEATURES, Badge, GapFlag, StoryFraction, TERMINAL_STATES, SUMMARY } = window;

// Small shared snippet — a tight version of the Features view.
function FeaturesSnippet({ rows = 4 }) {
  const items = FEATURES.slice(0, rows);
  return (
    <div style={{ padding: "18px 20px 8px" }}>
      <div style={{
        fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
        color: T.accent, textTransform: "uppercase",
        paddingBottom: 8, borderBottom: `1px solid ${T.accentRule}`,
        display: "flex", alignItems: "baseline", justifyContent: "space-between",
      }}>
        <span>flow · 9</span>
        <span style={{ color: T.inkFaint, letterSpacing: 0.3 }}>{SUMMARY.withGaps} with gaps</span>
      </div>
      <div>
        {items.map(f => (
          <div key={f.key} style={{
            display: "grid", gridTemplateColumns: "1fr auto",
            alignItems: "center", gap: 10,
            padding: "10px 0", borderBottom: `1px solid ${T.rule}`,
            opacity: TERMINAL_STATES.has(f.state) ? 0.65 : 1,
          }}>
            <div style={{ minWidth: 0 }}>
              <div style={{
                fontFamily: T.fontSans, fontSize: 13.5, color: T.ink, fontWeight: 500,
                lineHeight: 1.35,
                overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
              }}>
                {f.name}
              </div>
              <div style={{
                fontFamily: T.fontSans, fontSize: 12, color: T.inkMuted,
                marginTop: 3, lineHeight: 1.4,
                overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
              }}>
                {f.description}
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {f.hasGap && <GapFlag />}
              <Badge state={f.state} />
              <StoryFraction done={f.stories.done} total={f.stories.total} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── A · Tabs ─────────────────────────────────────────────────────────────
function NavTabs() {
  return (
    <div style={{
      width: "100%", height: "100%",
      background: T.paper, boxSizing: "border-box",
      display: "flex", flexDirection: "column",
      fontFamily: T.fontSans, color: T.ink,
    }}>
      {/* Title strip */}
      <div style={{
        padding: "16px 20px 10px",
        borderBottom: `1px solid ${T.rule}`,
      }}>
        <div style={{
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
        }}>
          <div style={{
            fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.3, fontWeight: 400,
          }}>
            Momentum · canvas
          </div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>
            generated · {SUMMARY.generated}
          </div>
        </div>
      </div>

      {/* Tab row */}
      <div style={{
        display: "flex", alignItems: "stretch",
        borderBottom: `1px solid ${T.rule}`,
        padding: "0 16px",
        background: T.paper,
      }}>
        <Tab label="features" active meta="19" />
        <Tab label="sprints"  meta="sprint-04-22" />
        <Tab label="flywheel" meta="6 findings" />
        <div style={{ flex: 1 }} />
      </div>

      <div style={{ flex: 1, overflow: "hidden" }}>
        <FeaturesSnippet />
      </div>
    </div>
  );
}

function Tab({ label, meta, active }) {
  return (
    <div style={{
      padding: "12px 16px 10px",
      borderBottom: active ? `2px solid ${T.accent}` : "2px solid transparent",
      marginBottom: -1,
      display: "flex", alignItems: "baseline", gap: 8,
      cursor: "pointer",
    }}>
      <span style={{
        fontFamily: T.fontMono, fontSize: 12, fontWeight: 500,
        letterSpacing: 0.3,
        color: active ? T.accent : T.inkMuted,
      }}>{label}</span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>{meta}</span>
    </div>
  );
}

// ─── B · Sidebar ──────────────────────────────────────────────────────────
function NavSidebar() {
  return (
    <div style={{
      width: "100%", height: "100%",
      background: T.paper, boxSizing: "border-box",
      display: "grid", gridTemplateColumns: "168px 1fr",
      fontFamily: T.fontSans, color: T.ink,
    }}>
      {/* Sidebar */}
      <aside style={{
        background: T.paperAlt,
        borderRight: `1px solid ${T.rule}`,
        padding: "16px 14px",
        display: "flex", flexDirection: "column", gap: 4,
      }}>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 17, fontWeight: 400,
          letterSpacing: -0.2, marginBottom: 14,
        }}>
          Momentum
        </div>
        <SideItem label="features" meta="19" active />
        <SideItem label="sprints" meta="04-22" />
        <SideItem label="flywheel" meta="6" />

        {/* Persistent current-sprint banner — the sidebar's main argument */}
        <div style={{
          marginTop: "auto", paddingTop: 14,
          borderTop: `1px solid ${T.rule}`,
        }}>
          <div style={{
            fontFamily: T.fontMono, fontSize: 9, letterSpacing: 1.3,
            color: T.inkQuiet, textTransform: "uppercase", marginBottom: 6,
          }}>
            in flight
          </div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 11, color: T.ink, fontWeight: 500,
            letterSpacing: 0.2,
          }}>
            sprint-04-22
          </div>
          <div style={{
            fontFamily: T.fontSans, fontSize: 11, color: T.inkMuted,
            marginTop: 2, lineHeight: 1.4,
          }}>
            3 in wave · 2 merged · 1 blocked
          </div>
        </div>
      </aside>

      {/* Main — Features snippet */}
      <div style={{ overflow: "hidden" }}>
        <div style={{
          padding: "14px 20px 10px",
          borderBottom: `1px solid ${T.rule}`,
          display: "flex", alignItems: "baseline", justifyContent: "space-between",
        }}>
          <div style={{
            fontFamily: T.fontSerif, fontSize: 18, letterSpacing: -0.2, fontWeight: 400,
          }}>
            Features
          </div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>
            hash {SUMMARY.hash}
          </div>
        </div>
        <FeaturesSnippet rows={3} />
      </div>
    </div>
  );
}

function SideItem({ label, meta, active }) {
  return (
    <div style={{
      display: "flex", alignItems: "baseline", justifyContent: "space-between",
      padding: "7px 10px",
      background: active ? T.accentSoft : "transparent",
      borderLeft: active ? `2px solid ${T.accent}` : "2px solid transparent",
      cursor: "pointer",
    }}>
      <span style={{
        fontFamily: T.fontMono, fontSize: 12, fontWeight: 500, letterSpacing: 0.3,
        color: active ? T.accent : T.ink,
      }}>{label}</span>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>{meta}</span>
    </div>
  );
}

// ─── C · Long-scroll ──────────────────────────────────────────────────────
function NavLongScroll() {
  return (
    <div style={{
      width: "100%", height: "100%",
      background: T.paper, boxSizing: "border-box",
      display: "flex", flexDirection: "column",
      fontFamily: T.fontSans, color: T.ink,
    }}>
      {/* Sticky index rail */}
      <div style={{
        position: "sticky", top: 0, zIndex: 2,
        padding: "10px 20px",
        background: T.paper,
        borderBottom: `1px solid ${T.rule}`,
        display: "flex", alignItems: "center", gap: 14,
      }}>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 16, letterSpacing: -0.2, fontWeight: 400,
          flexShrink: 0,
        }}>
          Momentum
        </div>
        <div style={{ flex: 1, height: 1, background: T.rule }} />
        <Anchor n="01" label="features" active />
        <Anchor n="02" label="sprints" />
        <Anchor n="03" label="flywheel" />
      </div>

      <div style={{ flex: 1, overflow: "hidden" }}>
        {/* Section header — anchor target style */}
        <div style={{
          padding: "20px 20px 2px",
          display: "flex", alignItems: "baseline", gap: 12,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.accent, textTransform: "uppercase",
          }}>01</span>
          <div style={{
            fontFamily: T.fontSerif, fontSize: 22, letterSpacing: -0.3, fontWeight: 400,
          }}>
            Features
          </div>
          <span style={{ flex: 1 }} />
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
          }}>{SUMMARY.total} total · {SUMMARY.withGaps} with gaps</span>
        </div>
        <FeaturesSnippet rows={3} />

        {/* Hint that more sections live below */}
        <div style={{
          padding: "18px 20px 0",
          display: "flex", alignItems: "center", gap: 12,
          opacity: 0.55,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.inkQuiet, textTransform: "uppercase",
          }}>02</span>
          <span style={{
            fontFamily: T.fontSerif, fontSize: 17, letterSpacing: -0.2, fontWeight: 400,
            color: T.inkMuted,
          }}>
            Sprints
          </span>
          <span style={{
            fontFamily: T.fontSans, fontSize: 12, color: T.inkQuiet,
          }}>· scroll down ↓</span>
        </div>
      </div>
    </div>
  );
}

function Anchor({ n, label, active }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "baseline", gap: 6,
      fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
      color: active ? T.accent : T.inkQuiet,
      fontWeight: active ? 500 : 400,
      cursor: "pointer",
    }}>
      <span style={{ color: active ? T.accent : T.inkFaint, fontSize: 9 }}>{n}</span>
      {label}
    </span>
  );
}

Object.assign(window, { NavTabs, NavSidebar, NavLongScroll });
