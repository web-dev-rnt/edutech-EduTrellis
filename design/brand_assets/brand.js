// Infinite360 Tech Academy brand kit: palette, contact details, emblem and logo lockups.
// Rendered to PNG by render.py; edit BRAND below and re-run to refresh every asset.

const BRAND = {
  name1: 'INFINITE',
  name2: '360',
  tagline: 'TECH ACADEMY',
  phone: '82968 93895',
  email: 'businessconsulting@gmail.com',
};

// Palette taken from the logo: the infinity runs warm (amber/orange) on the left into
// magenta, violet and blue on the right. `accent` is the warm amber used for small pops;
// `blue` is the primary UI color the website uses for buttons and links.
const C = {
  accent: '#FF9A1F', accentL: '#FFC24A', accentD: '#F07800', accentDD: '#A84E00',
  blue: '#2459E0', blueL: '#5B8CFF', blueD: '#1A3FB0',
  violet: '#7B3FF2', magenta: '#E2338C', cyan: '#19B5FE',
  ink: '#10142E', ink2: '#1E2448', ink3: '#343B66', mute: '#5F6687',
  cream: '#EEF2FF', paper: '#F8FAFF', white: '#FFFFFF', line: '#DCE4F7',
  navy: '#22307A', navyL: '#4C63D2', green: '#2F9E74', greenD: '#21765A',
  coral: '#F2617A', sky: '#DCE8F7',
};

// The signature gradient, left to right as in the logo.
const SPECTRUM = [
  [0, '#FFC21A'], [0.24, '#FF7A1A'], [0.5, '#E2338C'], [0.74, '#7B3FF2'], [1, '#2F6BFF'],
];
const stops = (list) => list.map(([o, c]) => `<stop offset="${o}" stop-color="${c}"/>`).join('');

const SERIF = "Georgia, 'Times New Roman', serif";
const SANS = "'Plus Jakarta Sans', 'Manrope', Arial, sans-serif";

let _uid = 0;
const uid = (p = 'u') => `${p}${++_uid}`;

// Measure rendered text width with the same fonts the SVG uses.
const _ctx = document.createElement('canvas').getContext('2d');
function textW(text, size, family = SANS, weight = 700, spacing = 0) {
  _ctx.font = `${weight} ${size}px ${family}`;
  return _ctx.measureText(text).width + spacing * text.length;
}

// Shared gradients/filters; every scene SVG includes this once.
function defs() {
  return `<defs>
    <linearGradient id="gBrand" x1="0" y1="0" x2="1" y2="1">${stops(SPECTRUM)}</linearGradient>
    <linearGradient id="gBrandH" x1="0" y1="0" x2="1" y2="0">${stops(SPECTRUM)}</linearGradient>
    <linearGradient id="gCool" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#1E7BFF"/><stop offset="1" stop-color="#7B3FF2"/></linearGradient>
    <linearGradient id="gWarm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFC21A"/><stop offset="1" stop-color="#FF7A1A"/></linearGradient>
    <linearGradient id="gInk" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#18205A"/><stop offset=".55" stop-color="#0F1438"/><stop offset="1" stop-color="#080B22"/></linearGradient>
    <radialGradient id="gGlow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="${C.violet}" stop-opacity=".6"/><stop offset="1" stop-color="${C.violet}" stop-opacity="0"/></radialGradient>
    <radialGradient id="gGlowW" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <filter id="fShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0b1030" flood-opacity=".18"/></filter>
    <filter id="fShadowS" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0b1030" flood-opacity=".2"/></filter>
    <pattern id="pDots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.4" fill="${C.blueL}"/></pattern>
    <pattern id="pDotsInk" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.2" fill="${C.ink}" opacity=".18"/></pattern>
    <pattern id="pDotsW" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.2" fill="#fff" opacity=".14"/></pattern>
  </defs>`;
}

// Brand emblem: a thick infinity loop in the spectrum gradient, its upper-right edge
// breaking into "pixels". Drawn in a 440x220 box; works on light and dark backgrounds.
const EMBLEM_W = 2; // width per unit of height

function infinityPath(cx, cy, a, b) {
  return `M${cx} ${cy} C${cx + a * 0.42} ${cy - b} ${cx + a} ${cy - b} ${cx + a} ${cy}
    C${cx + a} ${cy + b} ${cx + a * 0.42} ${cy + b} ${cx} ${cy}
    C${cx - a * 0.42} ${cy - b} ${cx - a} ${cy - b} ${cx - a} ${cy}
    C${cx - a} ${cy + b} ${cx - a * 0.42} ${cy + b} ${cx} ${cy} Z`;
}

// Pixel squares trailing off the right loop: [x, y, size, color].
const PIXELS = [
  [372, 22, 20, '#2F6BFF'], [398, 8, 15, '#3F8CFF'], [400, 36, 13, '#7B3FF2'],
  [420, 22, 11, '#19B5FE'], [425, 0, 8, '#2F6BFF'], [384, 0, 9, '#7B3FF2'], [430, 44, 7, '#3F8CFF'],
];

function emblem(x, y, h, light = false) {
  const s = h / 220, id = uid('em');
  return `<g transform="translate(${x} ${y}) scale(${s})">
    <defs>
      <linearGradient id="${id}g" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="410" y2="0">${stops(SPECTRUM)}</linearGradient>
      <linearGradient id="${id}s" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
    </defs>
    <path d="${infinityPath(216, 116, 168, 118)}" fill="none" stroke="url(#${id}g)" stroke-width="44" stroke-linejoin="round"/>
    <path d="${infinityPath(216, 116, 168, 118)}" fill="none" stroke="url(#${id}s)" stroke-width="44" stroke-linejoin="round" opacity="${light ? 0.5 : 0.8}"/>
    ${PIXELS.map(([px, py, ps, c]) => `<rect x="${px}" y="${py}" width="${ps}" height="${ps}" rx="${ps * 0.18}" fill="${c}"/>`).join('')}
  </g>`;
}

// Wordmark "INFINITE360°" (360 in the cool gradient) with "TECH ACADEMY" under it,
// left-aligned at x with its baseline at y. wordmarkWidth(size) gives the rendered width.
function wordmarkParts(size) {
  const ls = size * 0.01;
  const w1 = textW(BRAND.name1, size, SANS, 800, ls);
  const w2 = textW(BRAND.name2, size, SANS, 800, ls);
  return { ls, w1, w2, w: w1 + w2 + size * 0.3 };
}
const wordmarkWidth = (size) => wordmarkParts(size).w;

function wordmark(x, y, size, light = false, tagline = true) {
  const p = wordmarkParts(size);
  const tcol = light ? '#FFFFFF' : C.ink;
  const font = `font-family="${SANS}" font-weight="800" font-size="${size}" letter-spacing="${p.ls}"`;
  let out = `<text x="${x}" y="${y}" ${font} fill="${tcol}">${BRAND.name1}</text>
    <text x="${x + p.w1}" y="${y}" ${font} fill="url(#gCool)">${BRAND.name2}</text>
    <circle cx="${x + p.w1 + p.w2 + size * 0.13}" cy="${y - size * 0.62}" r="${size * 0.075}" fill="none" stroke="${C.violet}" stroke-width="${size * 0.04}"/>`;
  if (tagline) {
    const ty = y + size * 0.5, ts = size * 0.22;
    const textW = p.w * 0.6, gap = size * 0.16, rule = (p.w - textW) / 2 - gap;
    out += `<rect x="${x}" y="${ty - ts * 0.42}" width="${rule}" height="${ts * 0.16}" rx="${ts * 0.08}" fill="url(#gWarm)"/>
      <rect x="${x + p.w - rule}" y="${ty - ts * 0.42}" width="${rule}" height="${ts * 0.16}" rx="${ts * 0.08}" fill="url(#gCool)"/>
      <text x="${x + p.w / 2}" y="${ty}" text-anchor="middle" font-family="${SANS}" font-weight="700" font-size="${ts}" fill="${light ? '#C9CFEA' : C.mute}" textLength="${textW}" lengthAdjust="spacing">${BRAND.tagline}</text>`;
  }
  return out;
}

// Horizontal lockup: emblem + wordmark with tagline. Height ~ h.
function logoHorizontal(x, y, h, light = false) {
  const eh = h * 0.6, size = h * 0.4;
  return emblem(x, y + h * 0.12, eh, light) + wordmark(x + eh * EMBLEM_W + h * 0.12, y + h * 0.52, size, light);
}

function logoHorizontalWidth(h) {
  return h * 0.6 * EMBLEM_W + h * 0.12 + wordmarkWidth(h * 0.4);
}

// Compact lockup: same as horizontal, sized for tight spaces.
function logoCompact(x, y, h, light = false) {
  return logoHorizontal(x, y, h, light);
}

// Single-line lockup for the navbar: emblem + "INFINITE360°" on one line (no tagline,
// so it stays legible at small heights). `size` is the wordmark font-size.
function logoInline(x, y, size, light = false) {
  const eh = size * 0.92;
  return emblem(x, y + size * 0.02, eh, light) +
    wordmark(x + eh * EMBLEM_W + size * 0.22, y + size * 0.82, size, light, false);
}

// Stacked lockup (as in the original logo): emblem centered above wordmark.
function logoStacked(cx, y, w, light = false) {
  const size = w / wordmarkWidth(1), eh = size * 1.25;
  return emblem(cx - eh * EMBLEM_W / 2, y, eh, light) + wordmark(cx - w / 2, y + eh + size * 0.95, size, light);
}

// Rounded app-icon tile with the emblem: used for favicons and PWA icons.
function appIcon(size, pad = 0.14, radius = 0.22) {
  const r = size * radius, ew = size * (1 - pad * 2), eh = ew / EMBLEM_W;
  return `<rect width="${size}" height="${size}" rx="${r}" fill="url(#gInk)"/>
    <circle cx="${size * 0.5}" cy="${size * 0.5}" r="${size * 0.46}" fill="url(#gGlow)" opacity=".55"/>
    ${emblem(size * pad, (size - eh) / 2, eh, true)}`;
}
