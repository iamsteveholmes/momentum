// Level 2 — Feature drill-down.
// Populated from real FEATURES data (data.jsx). Sections per brief §5.

const { T, FEATURES, Badge, GapFlag, StoryFraction, Breadcrumb, BADGE_BY_KEY } = window;

// Default feature key for the mockup. Retro+Flywheel: partial with gap, flow type,
// exercises every Level-2 section including the gap callout.
const DEFAULT_L2_KEY = "retro-and-flywheel";

function LevelTwoPage({ featureKey = DEFAULT_L2_KEY }) {
  const d = FEATURES.find(f => f.key === featureKey) || FEATURES[0];
  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "hidden", display: "flex", flexDirection: "column",
    }}>
      {/* ── Top band ─────────────────────────────────── */}
      <div style={{
        padding: "28px 64px 24px",
        borderBottom: `1px solid ${T.rule}`,
      }}>
        <Breadcrumb items={["Dashboard", d.type, d.name]} />

        <div style={{
          fontFamily: T.fontSerif, fontSize: 32, lineHeight: 1.2,
          color: T.ink, letterSpacing: -0.5, fontWeight: 400,
          marginTop: 14, maxWidth: "28ch",
        }}>
          {d.name}
        </div>

        <div style={{
          display: "flex", alignItems: "center", gap: 18, flexWrap: "wrap",
          marginTop: 16,
        }}>
          <Badge state={d.state} size="md" />
          <StoryFraction done={d.stories.done} total={d.stories.total} />
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.inkQuiet, textTransform: "uppercase",
          }}>type · {d.type}</span>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
            color: T.inkQuiet, textTransform: "uppercase",
          }}>last verified · {d.lastVerified}</span>
          {d.hasGap && <GapFlag prominent note={d.gapNote} />}
          {d.statusDrift && (
            <span style={{
              fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.5,
              color: T.inkQuiet, padding: "2px 7px",
              border: `1px dashed ${T.ruleStrong}`, borderRadius: 3,
            }}>
              all stories done · awaiting grooming
            </span>
          )}
        </div>
      </div>

      {/* ── Body ─────────────────────────────────────── */}
      <div style={{
        flex: 1, overflow: "hidden",
        padding: "40px 64px 56px",
        display: "grid",
        gridTemplateColumns: "minmax(0, 660px) 1fr",
        columnGap: 56,
        alignItems: "start",
      }}>
        {/* Left — reading column */}
        <div>
          <SectionLabel>Value</SectionLabel>
          <div style={{
            fontFamily: T.fontSerif, fontSize: 17, lineHeight: 1.65,
            color: T.ink, maxWidth: "68ch",
            marginTop: 6,
          }}>
            {d.valueNarrative.map((p, i) => (
              <p key={i} style={{ margin: "0 0 1em" }}>{p}</p>
            ))}
          </div>

          {/* Acceptance */}
          <div style={{ marginTop: 28 }}>
            <SectionLabel>Acceptance</SectionLabel>
            <div style={{
              marginTop: 10,
              padding: "18px 22px",
              borderLeft: `2px solid ${T.accent}`,
              background: T.accentSoft,
              fontFamily: T.fontSerif, fontSize: 15.5, lineHeight: 1.6,
              color: T.ink, maxWidth: "66ch",
            }}>
              {d.acceptance}
            </div>
          </div>

          {/* System context */}
          <div style={{ marginTop: 28 }}>
            <SectionLabel>System context</SectionLabel>
            <div style={{
              marginTop: 10,
              fontFamily: T.fontSans, fontSize: 13.5, lineHeight: 1.6,
              color: T.inkMuted, maxWidth: "72ch",
            }}>
              {d.systemContext}
            </div>
          </div>

          {/* Gap prose */}
          {d.hasGap && (
            <div style={{ marginTop: 32 }}>
              <div style={{
                display: "flex", alignItems: "center", gap: 10,
                marginBottom: 10,
              }}>
                <SectionLabelInline>Gap</SectionLabelInline>
                <GapFlag />
              </div>
              <div style={{
                padding: "14px 18px",
                border: `1px solid rgba(168,90,42,0.22)`,
                background: T.gapSoft,
                fontFamily: T.fontSans, fontSize: 13.5, lineHeight: 1.6,
                color: T.ink, maxWidth: "66ch",
                borderRadius: 2,
              }}>
                {d.gapNote}
              </div>
            </div>
          )}
        </div>

        {/* Right — stories + graph stub */}
        <div>
          <SectionLabel>Stories</SectionLabel>
          <div style={{
            marginTop: 10,
            border: `1px solid ${T.rule}`,
            background: T.paper,
          }}>
            {d.storiesList.map((s, i) => (
              <StoryRow key={i} idx={i + 1} story={s} last={i === d.storiesList.length - 1} />
            ))}
          </div>

          {/* Dep graph container */}
          <div style={{ marginTop: 32 }}>
            <div style={{
              display: "flex", alignItems: "baseline", justifyContent: "space-between",
              marginBottom: 10,
            }}>
              <SectionLabelInline>Dependencies</SectionLabelInline>
              <span style={{
                fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
              }}>{d.storiesList.length} stories · list mode</span>
            </div>
            <DepGraphStub feature={d} />
          </div>
        </div>
      </div>
    </div>
  );
}

function SectionLabel({ children }) {
  return (
    <div style={{
      fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.5,
      color: T.accent, textTransform: "uppercase",
      paddingBottom: 6, borderBottom: `1px solid ${T.accentRule}`,
    }}>{children}</div>
  );
}
function SectionLabelInline({ children }) {
  return (
    <span style={{
      fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.5,
      color: T.inkQuiet, textTransform: "uppercase",
    }}>{children}</span>
  );
}

function StoryRow({ story, idx, last }) {
  const b = BADGE_BY_KEY[story.status];
  return (
    <div style={{
      display: "grid", gridTemplateColumns: "auto 1fr auto", alignItems: "center",
      gap: 12,
      padding: "11px 14px",
      borderBottom: last ? "none" : `1px solid ${T.rule}`,
      cursor: "pointer",
    }}>
      <span style={{
        width: 8, height: 8, borderRadius: "50%",
        background: b.dot,
      }} />
      <div style={{ minWidth: 0 }}>
        <div style={{
          fontFamily: T.fontSans, fontSize: 13, color: T.ink,
          overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        }}>
          {story.title}
        </div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint,
          letterSpacing: 0.3, marginTop: 2,
        }}>
          {String(idx).padStart(2, "0")} · {b.label}
        </div>
      </div>
      <span style={{
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>→</span>
    </div>
  );
}

function DepGraphStub({ feature }) {
  return (
    <div style={{ border: `1px solid ${T.rule}`, background: T.paper }}>
      <div style={{
        display: "flex", alignItems: "center",
        borderBottom: `1px solid ${T.rule}`,
        padding: "8px 12px", gap: 4,
      }}>
        <ModePill label="list" active />
        <ModePill label="graph" />
        <ModePill label="direct only" />
        <span style={{ flex: 1 }} />
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
        }}>N &gt; 15 → list auto</span>
      </div>

      <div style={{ padding: "10px 14px 12px" }}>
        <DepLine from="05 cross-story-pattern" label="detects patterns" to={["04 retro-triage-handoff"]} />
        <DepLine from="06 findings-ledger" label="persists findings" to={["05 pattern detection", "infra-08 ledger store"]} external />
        <DepLine from="07 flywheel-workflow" label="explains issues" to={["06 findings-ledger", "04 retro-triage-handoff"]} />
      </div>
    </div>
  );
}

function ModePill({ label, active }) {
  return (
    <span style={{
      fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.4,
      padding: "3px 8px",
      borderRadius: 2,
      color: active ? T.accent : T.inkQuiet,
      background: active ? T.accentSoft : "transparent",
      border: `1px solid ${active ? T.accentRule : "transparent"}`,
    }}>{label}</span>
  );
}

function DepLine({ from, label, to, external }) {
  return (
    <div style={{
      padding: "6px 0",
      fontFamily: T.fontMono, fontSize: 11, lineHeight: 1.55, color: T.inkMuted,
      borderBottom: `1px dashed ${T.rule}`,
    }}>
      <span style={{ color: T.ink }}>{from}</span>
      <span style={{ color: T.inkFaint }}> · {label}</span>
      <div style={{ paddingLeft: 16, marginTop: 2 }}>
        {to.map((t, i) => (
          <div key={i} style={{ color: external ? T.gap : T.inkMuted }}>
            ↳ {t}{external && <span style={{ color: T.inkFaint, marginLeft: 6 }}>(non-feature)</span>}
          </div>
        ))}
      </div>
    </div>
  );
}

window.LevelTwoPage = LevelTwoPage;
