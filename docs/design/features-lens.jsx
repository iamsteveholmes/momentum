// Pass 4 · Features lens @ 700px pane.
// Single-column rows (648px content), type-banded, DNA from Variant B.

const {
  T, FEATURES, SUMMARY, TYPE_ORDER, groupByType,
  Badge, GapFlag, StoryFraction, TERMINAL_STATES,
} = window;

function FeaturesLens({ tweaks, onOpenFeature }) {
  const dark = tweaks.dark;
  const grouped = groupByType(FEATURES);
  const terminalHidden = tweaks.hideTerminal;

  return (
    <section data-lens-id="features" style={{
      padding: "32px 24px 56px",
      background: dark ? T.paperDark : T.paper,
      color: dark ? T.inkOnDark : T.ink,
      fontFamily: T.fontSans,
    }}>
      <LensHeader n="01" label="Features" tweaks={tweaks} />

      <div style={{
        fontFamily: T.fontSerif, fontSize: 22, lineHeight: 1.35,
        letterSpacing: -0.2, fontWeight: 400, marginTop: 8, maxWidth: "34ch",
      }}>
        What the product is, what it does, what's missing.
      </div>

      <div style={{
        display: "flex", flexWrap: "wrap", gap: "10px 22px",
        marginTop: 18, alignItems: "baseline",
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 0.3,
      }}>
        <Stat n={SUMMARY.total} label="total" tweaks={tweaks} />
        <Stat n={SUMMARY.working} label="working" color="#3e7a5a" tweaks={tweaks} />
        <Stat n={SUMMARY.partial} label="partial" color="#c28b3e" tweaks={tweaks} />
        <Stat n={SUMMARY.notStarted} label="not started" color={dark ? T.inkOnDarkQuiet : T.inkQuiet} tweaks={tweaks} />
        <Stat n={SUMMARY.withGaps} label="with gaps" color={T.gap} tweaks={tweaks} />
      </div>

      <div style={{ marginTop: 28 }}>
        {TYPE_ORDER.map(type => {
          let feats = grouped[type] || [];
          if (terminalHidden) feats = feats.filter(f => !TERMINAL_STATES.has(f.state));
          if (!feats.length) return null;
          return <TypeBand key={type} type={type} features={feats} tweaks={tweaks} onOpenFeature={onOpenFeature} />;
        })}
      </div>
    </section>
  );
}

function LensHeader({ n, label, tweaks }) {
  const rule = tweaks.dark ? T.ruleDark : T.rule;
  const c = tweaks.dark ? "rgba(240,238,233,0.48)" : "rgba(40,30,20,0.45)";
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 4 }}>
      <span style={{
        fontFamily: T.fontMono, fontSize: 11, letterSpacing: 1.4,
        color: c, textTransform: "uppercase",
      }}>{n} · {label}</span>
      <span style={{ flex: 1, height: 1, background: rule }} />
    </div>
  );
}

function Stat({ n, label, color, tweaks }) {
  const labelC = tweaks.dark ? T.inkOnDarkMuted : T.inkMuted;
  const ink = tweaks.dark ? T.inkOnDark : T.ink;
  return (
    <span style={{ display: "inline-flex", alignItems: "baseline", gap: 6 }}>
      {color && <span style={{ width: 6, height: 6, borderRadius: "50%", background: color }} />}
      <span style={{ color: ink, fontWeight: 500 }}>{n}</span>
      <span style={{ color: labelC }}>{label}</span>
    </span>
  );
}

function TypeBand({ type, features, tweaks, onOpenFeature }) {
  const rule = tweaks.dark ? T.ruleDark : T.rule;
  const ruleS = tweaks.dark ? T.ruleDarkStrong : T.ruleStrong;
  const inkFaint = tweaks.dark ? "rgba(240,238,233,0.38)" : T.inkFaint;
  return (
    <section style={{ marginBottom: 32 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, padding: "6px 0 12px" }}>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.5,
          color: T.accent, textTransform: "uppercase",
        }}>{type}</span>
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, color: inkFaint, letterSpacing: 0.3,
        }}>{features.length}</span>
        <div style={{ flex: 1, height: 1, background: rule, marginLeft: 4 }} />
      </div>
      <div style={{ borderTop: `1px solid ${rule}` }}>
        {features.map(f => (
          <FeatureRow key={f.key} feature={f} tweaks={tweaks} onOpenFeature={onOpenFeature} />
        ))}
      </div>
    </section>
  );
}

function FeatureRow({ feature, tweaks, onOpenFeature }) {
  const terminal = TERMINAL_STATES.has(feature.state);
  const dark = tweaks.dark;
  const rule = dark ? T.ruleDark : T.rule;
  const ink = dark ? T.inkOnDark : T.ink;
  const muted = dark ? T.inkOnDarkMuted : T.inkMuted;

  return (
    <div
      onClick={() => onOpenFeature && onOpenFeature(feature)}
      style={{
        padding: "14px 0 13px",
        borderBottom: `1px solid ${rule}`,
        opacity: terminal ? 0.58 : 1,
        cursor: "pointer",
        display: "grid",
        gridTemplateColumns: "1fr auto",
        alignItems: "baseline", columnGap: 14,
      }}>
      {/* Left block */}
      <div style={{ minWidth: 0 }}>
        <div style={{
          display: "flex", alignItems: "center", gap: 10, marginBottom: 5,
        }}>
          <Badge state={feature.state} />
          {feature.hasGap && <GapFlag />}
          <span style={{
            fontFamily: T.fontSans, fontSize: 14, fontWeight: 500,
            color: ink, lineHeight: 1.3, letterSpacing: -0.1,
            overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
            minWidth: 0,
          }}>
            {feature.name}
          </span>
        </div>
        <div style={{
          fontFamily: T.fontSans, fontSize: 12.5, color: muted, lineHeight: 1.5,
          display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}>
          {feature.description}
        </div>
      </div>
      {/* Right meta */}
      <div style={{
        display: "flex", flexDirection: "column", alignItems: "flex-end",
        gap: 6, minWidth: 60,
      }}>
        {feature.stories.total > 0 ? (
          <StoryFraction done={feature.stories.done} total={feature.stories.total} muted={terminal} />
        ) : (
          <span style={{
            fontFamily: T.fontMono, fontSize: 10, color: dark ? "rgba(240,238,233,0.36)" : T.inkFaint,
            letterSpacing: 0.3,
          }}>—</span>
        )}
        <span style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 0.4,
          color: dark ? "rgba(240,238,233,0.36)" : T.inkFaint,
        }}>open →</span>
      </div>
    </div>
  );
}

window.FeaturesLens = FeaturesLens;
