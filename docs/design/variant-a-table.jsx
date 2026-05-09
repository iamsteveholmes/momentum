// Variant A — Compact Table density for Level-1 Index.
// Typographic, dense, keyboard-scannable. Single accent, generous line-height.

const { T, FEATURES, SUMMARY, TYPE_ORDER, groupByType, Badge, GapFlag, StoryFraction, Breadcrumb, TERMINAL_STATES } = window;

function IndexVariantA() {
  const grouped = groupByType(FEATURES);

  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "hidden", display: "flex", flexDirection: "column",
    }}>
      <HeaderA />

      <div style={{ flex: 1, overflow: "hidden", padding: "32px 56px 48px" }}>
        {TYPE_ORDER.map(type => (
          <TypeBandA key={type} type={type} features={grouped[type] || []} />
        ))}
      </div>
    </div>
  );
}

function HeaderA() {
  return (
    <div style={{
      padding: "28px 56px 20px",
      borderBottom: `1px solid ${T.rule}`,
    }}>
      <Breadcrumb items={["Dashboard"]} />
      <div style={{
        display: "flex", alignItems: "baseline", justifyContent: "space-between",
        marginTop: 10,
      }}>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 30, lineHeight: 1.2,
          color: T.ink, letterSpacing: -0.4, fontWeight: 400,
        }}>
          Feature Status
        </div>
        <div style={{
          fontFamily: T.fontMono, fontSize: 11, color: T.inkFaint, letterSpacing: 0.3,
        }}>
          generated · {SUMMARY.generated} · hash {SUMMARY.hash}
        </div>
      </div>
      <div style={{
        fontFamily: T.fontSans, fontSize: 13, color: T.inkMuted,
        marginTop: 8, maxWidth: "68ch", lineHeight: 1.5,
      }}>
        What the product is, what it does, what's missing. Click a feature to drill into its
        value narrative, acceptance, and stories.
      </div>

      {/* Summary strip */}
      <div style={{
        display: "flex", gap: 28, marginTop: 18, alignItems: "baseline",
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
      }}>
        <SumStat n={SUMMARY.total} label="total" />
        <SumStat n={SUMMARY.working} label="working" state="working" />
        <SumStat n={SUMMARY.partial} label="partial" state="partial" />
        <SumStat n={SUMMARY.notStarted} label="not started" state="not-started" />
        <SumStat n={SUMMARY.withGaps} label="with gaps" gap />
      </div>
    </div>
  );
}

function TypeBandA({ type, features }) {
  if (!features.length) return null;
  return (
    <section style={{ marginBottom: 40 }}>
      <div style={{
        position: "sticky", top: 0,
        display: "flex", alignItems: "baseline", gap: 14,
        padding: "10px 0 12px",
        borderBottom: `1px solid ${T.ruleStrong}`,
        marginBottom: 0,
        background: T.paper,
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.5,
          color: T.accent, textTransform: "uppercase",
        }}>{type}</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 11, color: T.inkFaint, letterSpacing: 0.3,
        }}>{features.length} features</span>
      </div>

      <div>
        {features.map((f, i) => (
          <FeatureRowA key={f.key} feature={f} last={i === features.length - 1} />
        ))}
      </div>
    </section>
  );
}

function FeatureRowA({ feature, last }) {
  const isTerminal = TERMINAL_STATES.has(feature.state);
  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "minmax(0, 1fr) 110px 110px 60px",
      columnGap: 20,
      alignItems: "baseline",
      padding: "14px 0 15px",
      borderBottom: last ? "none" : `1px solid ${T.rule}`,
      opacity: isTerminal ? 0.55 : 1,
    }}>
      {/* Name + description */}
      <div style={{ minWidth: 0 }}>
        <div style={{
          fontFamily: T.fontSans, fontSize: 14, fontWeight: 500, color: T.ink,
          letterSpacing: -0.1, marginBottom: 3,
          display: "flex", alignItems: "baseline", gap: 10,
        }}>
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint,
            letterSpacing: 0.5,
          }}>→</span>
          <span style={{
            textDecoration: "underline",
            textDecorationColor: T.accentRule,
            textDecorationThickness: "1px",
            textUnderlineOffset: 3,
          }}>{feature.name}</span>
        </div>
        <div style={{
          fontFamily: T.fontSans, fontSize: 12.5, color: T.inkMuted, lineHeight: 1.5,
          paddingLeft: 20,
          maxWidth: "68ch",
          overflow: "hidden", textOverflow: "ellipsis",
          display: "-webkit-box", WebkitLineClamp: 1, WebkitBoxOrient: "vertical",
        }}>
          {feature.description}
        </div>
      </div>

      {/* State */}
      <div><Badge state={feature.state} /></div>

      {/* Stories */}
      <div>
        {feature.stories.total > 0 ? (
          <StoryFraction done={feature.stories.done} total={feature.stories.total} muted={isTerminal} />
        ) : (
          <span style={{ fontFamily: T.fontMono, fontSize: 12, color: T.inkFaint }}>—</span>
        )}
      </div>

      {/* Gap */}
      <div style={{ justifySelf: "start" }}>
        {feature.hasGap && <GapFlag note={feature.gapNote} />}
      </div>
    </div>
  );
}

window.IndexVariantA = IndexVariantA;
