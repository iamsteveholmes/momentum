// Badge system artboard — active + terminal states, with tokens called out.

const { T, BADGES, Badge, GapFlag } = window;

function BadgeSystemArtboard() {
  return (
    <div style={{
      padding: "44px 48px",
      fontFamily: T.fontSans,
      color: T.ink,
      background: T.paper,
      width: "100%", height: "100%",
      boxSizing: "border-box",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 10,
        }}>
          Badge System · Status Semantics
        </div>
        <div style={{
          fontFamily: T.fontSerif, fontSize: 26, lineHeight: 1.25,
          color: T.ink, letterSpacing: -0.3, fontWeight: 400,
          maxWidth: "56ch",
        }}>
          Active states attract attention. Terminal states feel settled.
        </div>
        <div style={{
          fontFamily: T.fontSans, fontSize: 13, lineHeight: 1.55,
          color: T.inkMuted, marginTop: 12, maxWidth: "64ch",
        }}>
          One color family for state, separate from the indigo primary accent — so navigation
          and status never compete. Dot-first, monospace label, 6px filled disc.
        </div>
      </div>

      {/* Two columns: active vs terminal */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 40, marginBottom: 40 }}>
        {/* Active */}
        <div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.2,
            color: T.accent, textTransform: "uppercase", marginBottom: 14,
            paddingBottom: 8, borderBottom: `1px solid ${T.accentRule}`,
          }}>
            Active · draws attention
          </div>
          <BadgeRows group={BADGES.active} />
        </div>

        {/* Terminal */}
        <div>
          <div style={{
            fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.2,
            color: T.inkQuiet, textTransform: "uppercase", marginBottom: 14,
            paddingBottom: 8, borderBottom: `1px solid ${T.rule}`,
          }}>
            Terminal · de-emphasized
          </div>
          <BadgeRows group={BADGES.terminal} />
        </div>
      </div>

      {/* Gap flag specimen */}
      <div style={{
        paddingTop: 28, borderTop: `1px solid ${T.rule}`,
      }}>
        <div style={{
          fontFamily: T.fontMono, fontSize: 10, letterSpacing: 1.4,
          color: T.inkQuiet, textTransform: "uppercase", marginBottom: 14,
        }}>
          Gap Flag · two levels of emphasis
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 28 }}>
          <div>
            <div style={{ fontFamily: T.fontSans, fontSize: 11, color: T.inkQuiet, marginBottom: 6 }}>subtle</div>
            <GapFlag />
          </div>
          <div>
            <div style={{ fontFamily: T.fontSans, fontSize: 11, color: T.inkQuiet, marginBottom: 6 }}>prominent</div>
            <GapFlag prominent />
          </div>
          <div style={{
            marginLeft: "auto", maxWidth: "38ch",
            fontFamily: T.fontSans, fontSize: 12, lineHeight: 1.55, color: T.inkMuted,
          }}>
            Warm terracotta so it's distinct from `not-working` red — advises, doesn't alarm.
            Subtle by default; prominent only when the user opts in via Tweaks.
          </div>
        </div>
      </div>

      {/* Footnote */}
      <div style={{
        position: "absolute", bottom: 28, left: 48, right: 48,
        display: "flex", gap: 32,
        fontFamily: T.fontMono, fontSize: 10, color: T.inkFaint, letterSpacing: 0.3,
      }}>
        <span>hue · muted</span>
        <span>chroma · matched across states</span>
        <span>label · lowercase, mono</span>
        <span>dot · 6px filled</span>
      </div>
    </div>
  );
}

function BadgeRows({ group }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      {group.map(b => (
        <div key={b.key} style={{
          display: "grid", gridTemplateColumns: "120px 1fr", alignItems: "center",
          gap: 16,
        }}>
          <Badge state={b.key} />
          <div style={{
            fontFamily: T.fontSans, fontSize: 12, color: T.inkMuted, lineHeight: 1.4,
          }}>
            {descriptions[b.key]}
          </div>
        </div>
      ))}
    </div>
  );
}

const descriptions = {
  "working": "Acceptance met. Stories complete. Nothing pending.",
  "partial": "Works, but acceptance not fully met. Some coverage.",
  "not-working": "Stories assigned, acceptance violated. Needs attention.",
  "not-started": "No stories in flight. Quiet on the dashboard.",
  "done": "Complete and sealed. Filed below active work.",
  "shelved": "Paused intentionally. Kept for provenance.",
  "abandoned": "Work stopped mid-flight. Left as-is.",
  "rejected": "Evaluated and declined. Non-goal.",
};

window.BadgeSystemArtboard = BadgeSystemArtboard;
