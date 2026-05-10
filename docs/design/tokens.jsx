// Design tokens — Linear/Figma-adjacent, serif for narrative, mono for meta.
// Muted indigo/slate-blue accent; status color family is separate (see data.jsx BADGES).

const T = {
  // Typography stacks
  fontSans: '"Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  fontSerif: '"Source Serif 4", "Source Serif Pro", "Iowan Old Style", Georgia, serif',
  fontMono: '"JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace',

  // Paper / ink — warm neutral, not pure white
  paper: '#fbfaf7',
  paperAlt: '#f5f3ed',
  rule: '#e7e3d9',
  ruleStrong: '#d4cfc2',

  // Ink — soft black, not #000
  ink: '#1e1d1a',
  inkMuted: '#5a574f',
  inkQuiet: '#8a8678',
  inkFaint: '#b5b0a2',

  // Accent — muted indigo/slate-blue. Intentional thinking, not SaaS brand.
  accent: '#5863a8',
  accentSoft: 'rgba(88,99,168,0.08)',
  accentRule: 'rgba(88,99,168,0.22)',

  // Gap flag — warm, quiet, not alarming
  gap: '#a85a2a',
  gapSoft: 'rgba(168,90,42,0.09)',

  // Dark-mode paper/ink — warm dark, not black.
  paperDark: '#16140f',
  paperDarkAlt: '#1e1b15',
  ruleDark: 'rgba(255,252,245,0.10)',
  ruleDarkStrong: 'rgba(255,252,245,0.18)',
  inkOnDark: '#f0eee9',
  inkOnDarkMuted: 'rgba(240,238,233,0.70)',
  inkOnDarkQuiet: 'rgba(240,238,233,0.48)',

  // Scale
  reading: '72ch',
};

Object.assign(window, { T });
