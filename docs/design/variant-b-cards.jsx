// Variant B — Card Grid density for Level-1 Index.
// More breathing room, feature description gets its own block, meta line at bottom.

const { T, FEATURES, SUMMARY, TYPE_ORDER, groupByType, Badge, GapFlag, StoryFraction, Breadcrumb, TERMINAL_STATES } = window;

function IndexVariantB() {
  const grouped = groupByType(FEATURES);

  return (
    <div style={{
      fontFamily: T.fontSans, color: T.ink, background: T.paper,
      width: "100%", height: "100%", boxSizing: "border-box",
      overflow: "hidden", display: "flex", flexDirection: "column",
    }}>
      <HeaderB />

      <div style={{ flex: 1, overflow: "hidden", padding: "28px 40px 48px" }}>
        {TYPE_ORDER.map(type => (
          <TypeBandB key={type} type={type} features={grouped[type] || []} />
        ))}
      </div>
    </div>
  );
}

function HeaderB() {
  return (
    <div style={{
      padding: "28px 40px 20px",
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

function TypeBandB({ type, features }) {
  if (!features.length) return null;
  return (
    <section style={{ marginBottom: 36 }}>
      <div style={{
        display: "flex", alignItems: "baseline", gap: 14,
        padding: "8px 4px 16px",
      }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.5,
          color: T.accent, textTransform: "uppercase",
        }}>{type}</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 11, color: T.inkFaint, letterSpacing: 0.3,
        }}>{features.length}</span>
        <div style={{ flex: 1, height: 1, background: T.rule, marginLeft: 8 }} />
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
        gap: 1,
        background: T.rule,
        border: `1px solid ${T.rule}`,
      }}>
        {features.map(f => <FeatureCardB key={f.key} feature={f} />)}
      </div>
    </section>
  );
}

function FeatureCardB({ feature }) {
  const isTerminal = TERMINAL_STATES.has(feature.state);
  return (
    <div style={{
      background: T.paper,
      padding: "18px 20px 16px",
      opacity: isTerminal ? 0.55 : 1,
      display: "flex", flexDirection: "column", gap: 10,
      cursor: "pointer",
      minHeight: 124,
    }}>
      {/* Top row: state + gap */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        gap: 10,
      }}>
        <Badge state={feature.state} />
        {feature.hasGap && <GapFlag note={feature.gapNote} />}
      </div>

      {/* Name */}
      <div style={{
        fontFamily: T.fontSans, fontSize: 14.5, fontWeight: 500,
        color: T.ink, lineHeight: 1.35, letterSpacing: -0.1,
      }}>
        {feature.name}
      </div>

      {/* Description */}
      <div style={{
        fontFamily: T.fontSans, fontSize: 12.5, color: T.inkMuted,
        lineHeight: 1.55,
        display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
        overflow: "hidden",
      }}>
        {feature.description}
      </div>

      {/* Meta */}
      <div style={{
        marginTop: "auto", paddingTop: 8,
        borderTop: `1px dashed ${T.rule}`,
        display: "flex", alignItems: "center", justifyContent: "space-between",
      }}>
        {feature.stories.total > 0 ? (
          <StoryFraction done={feature.stories.done} total={feature.stories.total} muted={isTerminal} />
        ) : (
          <span style={{ fontFamily: T.fontMono, fontSize: 11, color: T.inkFaint, letterSpacing: 0.3 }}>
            no stories
          </span>
        )}
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.5,
          color: T.inkFaint,
        }}>open →</span>
      </div>
    </div>
  );
}

window.IndexVariantB = IndexVariantB;
