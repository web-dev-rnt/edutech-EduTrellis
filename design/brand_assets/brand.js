// Edutrellis brand kit: palette, contact details, emblem and logo lockups.
// Rendered to PNG by render.py; edit BRAND below and re-run to refresh every asset.

const BRAND = {
  name1: 'Edu',
  name2: 'Trellis',
  tagline: ['LEARN', 'BUILD', 'GROW'],
  phone: '91941 30645',
  email: 'support@edutrellis.in',
};

// Red theme. `blue` keeps its old key name but is now the primary brand red the website uses
// for buttons and links; `accent` is a warm amber used for small pops against the red.
const C = {
  accent: '#FF9A1F', accentL: '#FFC24A', accentD: '#F07800', accentDD: '#A84E00',
  blue: '#D7263D', blueL: '#F45B6E', blueD: '#9E1428',
  violet: '#9E1428', magenta: '#F0506E', cyan: '#FF8A5B',
  ink: '#1F0B12', ink2: '#3A1520', ink3: '#5A2A36', mute: '#7A5A62',
  cream: '#FFF1F2', paper: '#FFF9F8', white: '#FFFFFF', line: '#F6D8DC',
  navy: '#8E1A2B', navyL: '#E25A6B', green: '#2F9E74', greenD: '#21765A',
  coral: '#FF8A4C', sky: '#FBE3E6',
  // Logo colours: "Edu" in signal red, "Trellis" in deep navy.
  logoRed: '#E8192F', logoNavy: '#0C1E45',
  saffron: '#FF9933', indiaGreen: '#138808',
};

// The signature gradient: amber into brand red into deep crimson.
const SPECTRUM = [
  [0, '#FFB21A'], [0.3, '#FF6B2B'], [0.62, '#E8283F'], [1, '#B0102A'],
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
      <stop offset="0" stop-color="#EE3349"/><stop offset="1" stop-color="#A8102C"/></linearGradient>
    <linearGradient id="gWarm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFC21A"/><stop offset="1" stop-color="#FF7A1A"/></linearGradient>
    <linearGradient id="gInk" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4E0F1F"/><stop offset=".55" stop-color="#2A0812"/><stop offset="1" stop-color="#15040A"/></linearGradient>
    <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF2E43"/><stop offset="1" stop-color="#D0102A"/></linearGradient>
    <linearGradient id="gRedLight" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF5466"/><stop offset="1" stop-color="#F0283E"/></linearGradient>
    <linearGradient id="gNavy" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#16306A"/><stop offset="1" stop-color="#0A1A3D"/></linearGradient>
    <linearGradient id="gRuleL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E8192F" stop-opacity="0"/><stop offset=".45" stop-color="#E8192F"/><stop offset="1" stop-color="#E8192F"/></linearGradient>
    <linearGradient id="gRuleR" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E8192F"/><stop offset=".55" stop-color="#E8192F"/><stop offset="1" stop-color="#E8192F" stop-opacity="0"/></linearGradient>
    <radialGradient id="gGlow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="${C.violet}" stop-opacity=".6"/><stop offset="1" stop-color="${C.violet}" stop-opacity="0"/></radialGradient>
    <radialGradient id="gGlowW" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <filter id="fShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#2a0610" flood-opacity=".18"/></filter>
    <filter id="fShadowS" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#2a0610" flood-opacity=".2"/></filter>
    <pattern id="pDots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.4" fill="${C.blueL}"/></pattern>
    <pattern id="pDotsInk" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.2" fill="${C.ink}" opacity=".18"/></pattern>
    <pattern id="pDotsW" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="3" cy="3" r="2.2" fill="#fff" opacity=".14"/></pattern>
  </defs>`;
}

// ---------------------------------------------------------------------------------------------
// Logo: the wordmark "EduTrellis" ("Edu" upright in red, "Trellis" in heavy navy italic with a red
// dot on its i), the tagline "LEARN • BUILD • GROW" between two red rules, and an optional
// "Made in India" seal. Pass light=true for dark backgrounds ("Trellis" turns white).
// ---------------------------------------------------------------------------------------------

const SKEW = 12; // italic slant of "Trellis", degrees
const SLANT = Math.tan(SKEW * Math.PI / 180);

function glyphBox(text, size, weight = 800) {
  _ctx.font = `${weight} ${size}px ${SANS}`;
  return _ctx.measureText(text);
}

// Heavy text: the 800 weight plus a same-colour outline, for a bolder, poster-like wordmark.
function heavy(x, y, size, text, fill, extra = '') {
  return `<text x="${x}" y="${y}" font-family="${SANS}" font-weight="800" font-size="${size}"
    letter-spacing="${-size * 0.012}" fill="${fill}" stroke="${fill}" stroke-width="${size * 0.034}"
    stroke-linejoin="round" paint-order="stroke" ${extra}>${text}</text>`;
}

function wordmarkParts(size) {
  const ls = -size * 0.012;
  const w1 = textW(BRAND.name1, size, SANS, 800, ls);
  const gap = -size * 0.045;
  const w2 = textW(BRAND.name2, size, SANS, 800, ls);
  const capH = glyphBox('T', size).actualBoundingBoxAscent;
  // The slanted "Trellis" leans right by about half its cap-height times the slant.
  return { ls, w1, gap, w2, capH, w: w1 + gap + w2 + capH * SLANT * 0.55 };
}
const wordmarkWidth = (size) => wordmarkParts(size).w;

function tagline(x, y, w, ts, light) {
  const tls = ts * 0.16, gap = ts * 0.85, dot = ts * 0.2;
  const widths = BRAND.tagline.map(t => textW(t, ts, SANS, 800, tls) - tls);
  const inner = widths.reduce((a, b) => a + b, 0) + gap * 2 * (BRAND.tagline.length - 1);
  const rule = (w - inner) / 2 - gap * 1.1, ry = y - ts * 0.36, rh = Math.max(ts * 0.13, 2);
  const ink = light ? '#FFFFFF' : C.logoNavy, red = light ? '#FF4D5E' : C.logoRed;
  let cx = x + (w - inner) / 2, out = '';
  if (rule > ts) {
    out += `<rect x="${x}" y="${ry - rh / 2}" width="${rule}" height="${rh}" rx="${rh / 2}" fill="url(#gRuleL)"/>
      <rect x="${x + w - rule}" y="${ry - rh / 2}" width="${rule}" height="${rh}" rx="${rh / 2}" fill="url(#gRuleR)"/>`;
  }
  BRAND.tagline.forEach((word, i) => {
    out += `<text x="${cx}" y="${y}" font-family="${SANS}" font-weight="800" font-size="${ts}" letter-spacing="${tls}" fill="${ink}">${word}</text>`;
    cx += widths[i];
    if (i < BRAND.tagline.length - 1) {
      out += `<circle cx="${cx + gap}" cy="${ry}" r="${dot}" fill="${red}"/>`;
      cx += gap * 2;
    }
  });
  return out;
}

// Wordmark with its baseline at y, starting at x. `tag` adds the tagline underneath.
function wordmark(x, y, size, light = false, tag = true) {
  const p = wordmarkParts(size), id = uid('wm');
  const red = light ? 'url(#gRedLight)' : 'url(#gRed)';
  const navy = light ? '#FFFFFF' : 'url(#gNavy)';
  const x2 = x + p.w1 + p.gap;
  // Position of the last "i" inside "Trellis", and the x-height, for the red dot.
  const iX = textW(BRAND.name2.slice(0, -2), size, SANS, 800, p.ls);
  const iW = textW('i', size, SANS, 800, 0);
  const xH = glyphBox('x', size).actualBoundingBoxAscent;
  let out = heavy(x, y, size, BRAND.name1, red) +
    `<g transform="translate(${x2} ${y}) skewX(${-SKEW})">
      <defs><clipPath id="${id}"><rect x="${iX - size * 0.06}" y="${-size * 1.2}" width="${iW + size * 0.12}" height="${size * 1.2 - xH - size * 0.025}"/></clipPath></defs>
      ${heavy(0, 0, size, BRAND.name2, navy)}
      ${heavy(iX, 0, size, 'i', light ? '#FF4D5E' : C.logoRed, `clip-path="url(#${id})"`)}
    </g>`;
  if (tag) out += tagline(x, y + size * 0.43, p.w, size * 0.17, light);
  return out;
}

// "Made in India" seal: a waving tricolour ribbon between "MADE IN INDIA" and "100% INDIAN OWNED".
// Centred on cx, top at y, w wide; about w * INDIA_SEAL_H tall.
function indiaSeal(cx, y, w, light = false) {
  const ink = light ? '#FFFFFF' : C.logoNavy, red = light ? '#FF4D5E' : C.logoRed;
  const s1 = w * 0.072, l1 = s1 * 0.2;
  const t1 = 'MADE IN INDIA', w1 = textW(t1, s1, SANS, 800, l1) - l1;
  const rule = (w - w1) / 2 - s1 * 0.9, ry = y + s1 * 0.62, rh = Math.max(s1 * 0.12, 2);
  // Ribbon: three stripes following the same gentle wave.
  const rw = w * 0.5, rx = cx - rw / 2, rt = y + s1 * 1.75, band = w * 0.038, amp = w * 0.018;
  const edge = (off) => {
    const pts = [];
    for (let i = 0; i <= 24; i++) {
      const u = i / 24;
      // Centre line waves gently; the ribbon tapers to points at both ends, like a flying pennant.
      const t = 0.18 + 0.82 * Math.sin(Math.PI * u);
      const mid = rt + band * 1.5 + amp * Math.sin(u * Math.PI * 2 + 0.6);
      pts.push([rx + u * rw, mid + (off - 1.5) * band * t]);
    }
    return pts;
  };
  const stripe = (k, fill) => {
    const top = edge(k), bot = edge(k + 1).reverse();
    return `<path d="M${top.map(p => p.join(' ')).join(' L')} L${bot.map(p => p.join(' ')).join(' L')} Z" fill="${fill}"/>`;
  };
  const s2 = w * 0.07, l2 = s2 * 0.12;
  const a = '100% ', b = 'INDIAN', c = ' OWNED';
  const wa = textW(a, s2, SANS, 800, l2), wb = textW(b, s2, SANS, 800, l2), wc = textW(c, s2, SANS, 800, l2) - l2;
  const ly = rt + band * 3 + amp + s2 * 1.15;
  const lx = cx - (wa + wb + wc) / 2;
  const font = `font-family="${SANS}" font-weight="800" font-size="${s2}" letter-spacing="${l2}"`;
  return `<rect x="${cx - w / 2}" y="${ry - rh / 2}" width="${rule}" height="${rh}" rx="${rh / 2}" fill="url(#gRuleL)"/>
    <rect x="${cx + w / 2 - rule}" y="${ry - rh / 2}" width="${rule}" height="${rh}" rx="${rh / 2}" fill="url(#gRuleR)"/>
    <text x="${cx}" y="${y + s1}" text-anchor="middle" font-family="${SANS}" font-weight="800" font-size="${s1}" letter-spacing="${l1}" fill="${ink}">${t1}</text>
    ${stripe(0, C.saffron)}${stripe(1, light ? '#FFFFFF' : '#F4F5F8')}${stripe(2, C.indiaGreen)}
    <text x="${lx}" y="${ly}" ${font} fill="${ink}">${a}<tspan fill="${red}">${b}</tspan>${c}</text>`;
}
const INDIA_SEAL_H = 0.36; // seal height per unit of width

// Horizontal lockup: wordmark + tagline, about h tall from y.
function logoHorizontal(x, y, h, light = false) {
  const size = h * 0.72;
  return wordmark(x, y + size * 0.76, size, light);
}
function logoHorizontalWidth(h) {
  return wordmarkWidth(h * 0.72);
}
const logoCompact = logoHorizontal;

// Single-line wordmark for the navbar (no tagline, so it stays legible at small heights).
function logoInline(x, y, size, light = false) {
  return wordmark(x, y + size * 0.78, size, light, false);
}

// Stacked lockup: wordmark + tagline centred on cx, w wide, with the Made in India seal below.
function logoStacked(cx, y, w, light = false, seal = true) {
  const size = w / wordmarkWidth(1);
  let out = wordmark(cx - w / 2, y + size * 0.76, size, light);
  if (seal) out += indiaSeal(cx, y + size * 1.55, w * 0.62, light);
  return out;
}

// Monogram "ET" ("E" in red, "T" in white italic) on a navy tile: app icon, favicon, badge.
// `tile` false draws only the letters (for the maskable icon, which supplies its own background).
function monogram(x, y, s, tile = true) {
  const f = s * 0.6, ls = -f * 0.012;
  const wE = textW('E', f, SANS, 800, ls), wT = textW('T', f, SANS, 800, ls);
  const capH = glyphBox('E', f).actualBoundingBoxAscent;
  const overlap = f * 0.04, total = wE + wT - overlap + capH * SLANT * 0.5;
  const bx = x + (s - total) / 2, by = y + s / 2 + capH / 2;
  const id = uid('mg');
  return `${tile ? `<defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#1B3A7E"/><stop offset="1" stop-color="#081634"/></linearGradient></defs>
    <rect x="${x}" y="${y}" width="${s}" height="${s}" rx="${s * 0.22}" fill="url(#${id})"/>
    <rect x="${x + s * 0.18}" y="${y + s * 0.8}" width="${s * 0.64}" height="${s * 0.045}" rx="${s * 0.0225}" fill="${C.logoRed}"/>` : ''}
    ${heavy(bx, by - s * 0.03, f, 'E', 'url(#gRedLight)')}
    <g transform="translate(${bx + wE - overlap} ${by - s * 0.03}) skewX(${-SKEW})">${heavy(0, 0, f, 'T', '#FFFFFF')}</g>`;
}

// App icon: the monogram tile. radius=0 gives the maskable variant, a full-bleed navy square
// with the letters inside the 80% safe zone.
function appIcon(size, pad = 0.14, radius = 0.22) {
  if (radius) return monogram(0, 0, size);
  const m = size * pad;
  return `<rect width="${size}" height="${size}" fill="url(#gNavy)"/>${monogram(m, m, size - m * 2, false)}`;
}
