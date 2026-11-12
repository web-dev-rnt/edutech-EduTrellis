// Asset catalogue: each entry is { w, h, draw() } and renders to out/<name>.png.

const ASSETS = {};

/* ---------- logos & icons ---------- */

ASSETS.logo_horizontal = { w: 1800, h: 340, trim: true, draw: () => logoHorizontal(20, 40, 240) };
ASSETS.logo_horizontal_light = { w: 1800, h: 340, trim: true, draw: () => logoHorizontal(20, 40, 240, true) };
ASSETS.logo_inline = { w: 1700, h: 260, trim: true, draw: () => logoInline(20, 30, 160) };
ASSETS.logo_compact = { w: 1400, h: 340, trim: true, draw: () => logoCompact(20, 40, 240) };
ASSETS.logo_compact_light = { w: 1400, h: 340, trim: true, draw: () => logoCompact(20, 40, 240, true) };
ASSETS.logo_stacked = { w: 1300, h: 900, trim: true, draw: () => logoStacked(650, 40, 1100) };
ASSETS.logo_stacked_light = { w: 1300, h: 900, trim: true, draw: () => logoStacked(650, 40, 1100, true) };
ASSETS.logo_badge = {
  w: 512, h: 512,
  draw: () => `<circle cx="256" cy="256" r="250" fill="#fff"/><circle cx="256" cy="256" r="236" fill="none" stroke="url(#gBrandH)" stroke-width="6"/>
    ${emblem(256 - 190 * EMBLEM_W / 2, 256 - 95, 190)}`,
};
ASSETS.icon_512 = { w: 512, h: 512, draw: () => appIcon(512) };
// Maskable PWA icon: full-bleed square, emblem inside the 80% safe zone.
ASSETS.icon_maskable_512 = { w: 512, h: 512, draw: () => appIcon(512, 0.24, 0) };

/* ---------- text helpers ---------- */

function T(x, y, size, content, o = {}) {
  return `<text x="${x}" y="${y}" font-family="${o.family || SANS}" font-weight="${o.weight || 800}" font-size="${size}"
    fill="${o.color || C.ink}" text-anchor="${o.anchor || 'start'}" letter-spacing="${o.ls || 0}" opacity="${o.opacity || 1}">${content}</text>`;
}

// One headline line where `hl` is painted in the brand spectrum (light bg) or warm amber (dark bg).
// The highlighted words get their own <text> so the gradient spans just those words.
function markLine(x, y, size, before, hl, after = '', dark = false, weight = 800, hlFill = null) {
  const wb = before ? textW(before + ' ', size, SANS, weight) : 0;
  const wh = hl ? textW(hl, size, SANS, weight) : 0;
  const base = dark ? '#fff' : C.ink;
  const fill = hlFill || (dark ? C.accentL : 'url(#gBrandH)');
  const font = `font-family="${SANS}" font-weight="${weight}" font-size="${size}"`;
  return (before ? `<text x="${x}" y="${y}" ${font} fill="${base}">${before}</text>` : '') +
    (hl ? `<text x="${x + wb}" y="${y}" ${font} fill="${fill}">${hl}</text>` : '') +
    // Leading spaces collapse in SVG text, so offset the tail by their width instead.
    (after ? `<text x="${x + wb + wh + textW(after.match(/^ */)[0], size, SANS, weight)}" y="${y}" ${font} fill="${base}">${after.trimStart()}</text>` : '');
}

// Contact pills laid out in a row starting at x; returns svg.
function contactRow(x, y, h, items, opts = {}) {
  let out = '', cx = x;
  for (const [ic, text] of items) {
    out += pill(cx, y, h, ic, text, opts);
    cx += pillWidth(h, text) + h * 0.3;
  }
  return out;
}

/* ---------- desktop banners 1920x300 (keep key content inside x 300..1620) ---------- */

function bannerBgLight() {
  return `<rect width="1920" height="300" fill="${C.paper}"/>
    <rect width="1920" height="300" fill="url(#bgWarm)"/>
    <defs><linearGradient id="bgWarm" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E6EDFF"/><stop offset=".45" stop-color="#F8FAFF"/><stop offset="1" stop-color="#F1E8FF"/></linearGradient></defs>
    <path d="M0 0 H210 C150 90 170 210 90 300 H0 Z" fill="url(#gWarm)"/>
    <path d="M0 0 H150 C100 80 110 200 40 300 H0 Z" fill="${C.ink}"/>
    ${rings(250, 30, 120, 3, C.violet, 0.3, 3)}
    <rect x="1700" y="20" width="200" height="130" fill="url(#pDots)" opacity=".45"/>
    <path d="M1920 300 H1700 C1760 240 1780 140 1860 90 C1890 70 1910 60 1920 58 Z" fill="${C.ink}"/>
    <path d="M1920 300 H1790 C1830 250 1850 180 1920 150 Z" fill="url(#gCool)"/>`;
}

ASSETS.banner_1_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgLight() +
    markLine(320, 92, 50, 'Learn Smarter,', '') +
    markLine(320, 148, 50, '', 'Score Higher.') +
    T(320, 184, 20, 'Live classes, video courses &amp; test series by expert faculty.', { weight: 600, color: C.mute }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    // illustration
    `<circle cx="1180" cy="330" r="250" fill="url(#gBrand)"/>
     ${rings(1180, 330, 300, 3, C.ink, 0.12, 2.5)}
     <rect x="1310" y="40" width="130" height="90" fill="url(#pDotsInk)"/>` +
    student(1060, 70, 0.78, { skin: 'wheat', hair: 'bun', top: C.ink, pose: 'desk', eyes: 'down', earring: true }) +
    `<rect x="930" y="282" width="520" height="18" rx="4" fill="${C.ink}"/>` +
    laptopBack(1154, 284, 150) +
    deskLamp(950, 284, 150) + bookStack(1300, 282, 110) + mug(1420, 282, 40) +
    infoCard(870, 46, 250, 70, 'live', 'Live Class', 'Physics · 6:00 PM', {}) +
    infoCard(1420, 140, 230, 70, 'trophy', 'Score 98%', 'Mock Test #12', { bar: 0.98 }) +
    sparkle(1270, 40, 14) + sparkle(1480, 110, 9, C.ink) + sparkle(890, 160, 10) +
    formulaChip(1700, 190, 'a² + b² = c²', 22, -6),
};

ASSETS.banner_2_desktop = {
  w: 1920, h: 300,
  draw: () => `<rect width="1920" height="300" fill="url(#gInk)"/>
    <rect width="1920" height="300" fill="url(#pDotsW)" opacity=".5"/>
    <circle cx="1220" cy="150" r="300" fill="url(#gGlow)" opacity=".55"/>
    ${rings(120, 150, 170, 4, C.accent, 0.5, 3)}
    ${rings(1840, 160, 150, 4, C.accent, 0.4, 3)}` +
    markLine(320, 92, 50, 'Boost Your', 'Score', '', true) +
    markLine(320, 148, 50, 'with', 'Smart Tests', '', true) +
    T(320, 184, 20, 'Mock tests · PYQs · All-India rank · Detailed analysis', { weight: 600, color: '#C3C9E6' }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]], { bg: '#1E2550', stroke: '#323B70' }) +
    // test paper card
    `<g filter="url(#fShadow)" transform="rotate(-4 1000 160)">
      <rect x="880" y="40" width="240" height="250" rx="18" fill="#F8FAFF"/>
      <rect x="880" y="40" width="240" height="50" rx="18" fill="${C.accent}"/><rect x="880" y="70" width="240" height="20" fill="${C.accent}"/>
      ${T(904, 74, 20, 'MOCK TEST 12', { color: C.ink })}
      ${[0, 1, 2, 3].map(i => `<circle cx="912" cy="${122 + i * 38}" r="12" fill="${i === 2 ? '#E2E8F5' : C.ink}"/>
        ${i === 2 ? '' : icon('check', 912, 122 + i * 38, 14, C.accent)}
        <rect x="934" y="${114 + i * 38}" width="${150 - i * 14}" height="8" rx="4" fill="#DCE2EF"/>
        <rect x="934" y="${128 + i * 38}" width="${100 - i * 10}" height="6" rx="3" fill="#E8ECF5"/>`).join('')}
    </g>` +
    student(1130, 60, 0.8, { skin: 'light', hair: 'ponytail', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'shirt', pose: 'think', glasses: true }) +
    // score ring
    `<g filter="url(#fShadow)"><circle cx="1470" cy="110" r="64" fill="#fff"/>
      <circle cx="1470" cy="110" r="48" fill="none" stroke="#E6EAF4" stroke-width="12"/>
      <circle cx="1470" cy="110" r="48" fill="none" stroke="${C.accent}" stroke-width="12" stroke-linecap="round"
        stroke-dasharray="${2 * Math.PI * 48 * 0.92} 999" transform="rotate(-90 1470 110)"/>
      ${T(1470, 118, 26, '92%', { anchor: 'middle' })}</g>` +
    infoCard(1380, 200, 250, 70, 'star', 'All-India Rank', 'Compare with toppers', { dark: false }) +
    sparkle(860, 40, 12) + sparkle(1560, 40, 10, '#fff') + sparkle(1100, 270, 9) +
    formulaChip(1680, 50, 'π r²', 24, 8, true),
};

ASSETS.banner_3_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgLight() +
    markLine(320, 90, 40, 'Knowledge That Costs Nothing,', '') +
    markLine(320, 144, 40, '', 'Empowers Everything.') +
    T(320, 180, 20, 'Join 900+ students preparing smarter with Infinite360.', { weight: 600, color: C.mute }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    `<path d="M980 300 C1030 170 1470 170 1520 300 Z" fill="url(#gBrand)"/>
     ${rings(1250, 300, 260, 3, C.ink, 0.1, 2.5)}` +
    student(1010, 92, 0.7, { skin: 'brown', hair: 'braid', top: C.navy, pose: 'books', mouth: 'open' }) +
    student(1340, 92, 0.7, { skin: 'wheat', hair: 'short', top: C.ink, collar: 'shirt', pose: 'wave', mouth: 'open' }) +
    student(1158, 66, 0.8, { skin: 'light', hair: 'long', pose: 'grad', collar: 'gown', top: C.ink, cap: true, mouth: 'open' }) +
    infoCard(975, 22, 200, 64, 'users', '900+', 'Happy students') +
    infoCard(1500, 60, 230, 66, 'book', 'E-Library', 'Notes &amp; e-books') +
    sparkle(1290, 40, 14) + sparkle(1510, 170, 9, C.ink) + sparkle(950, 160, 10) +
    formulaChip(1700, 190, 'E = mc²', 22, -6),
};

/* ---------- mobile banners 750x400 ---------- */

function bannerBgMobile(dark = false) {
  return dark
    ? `<rect width="750" height="400" fill="url(#gInk)"/><rect width="750" height="400" fill="url(#pDotsW)" opacity=".5"/>
       <circle cx="560" cy="230" r="250" fill="url(#gGlow)" opacity=".55"/>${rings(700, 60, 120, 3, C.accent, 0.45, 3)}`
    : `<rect width="750" height="400" fill="url(#bgWarmM)"/>
       <defs><linearGradient id="bgWarmM" x1="0" y1="0" x2="1" y2="1">
         <stop offset="0" stop-color="#F8FAFF"/><stop offset="1" stop-color="#E4ECFF"/></linearGradient></defs>
       <rect x="600" y="16" width="140" height="90" fill="url(#pDots)" opacity=".45"/>
       <path d="M0 400 V330 C40 350 60 380 120 400 Z" fill="${C.accent}"/>`;
}

ASSETS.banner_1_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgMobile() +
    `<circle cx="590" cy="420" r="210" fill="url(#gBrand)"/>${rings(590, 420, 250, 3, C.ink, 0.12, 2.5)}` +
    student(486, 186, 0.74, { skin: 'wheat', hair: 'bun', top: C.ink, pose: 'desk', eyes: 'down', earring: true }) +
    `<rect x="400" y="384" width="350" height="16" fill="${C.ink}"/>` + laptopBack(575, 386, 140) + deskLamp(410, 386, 120) + bookStack(660, 384, 80) +
    infoCard(486, 80, 220, 64, 'live', 'Live Class', 'Physics · 6:00 PM') +
    markLine(30, 100, 44, 'Learn Smarter,', '') +
    markLine(30, 154, 44, '', 'Score Higher.') +
    T(30, 194, 21, 'Live classes · Videos · Test series', { weight: 600, color: C.mute }) +
    pill(30, 228, 46, 'phone', BRAND.phone) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#DCE4F7' }) +
    sparkle(720, 150, 10, C.ink),
};

ASSETS.banner_2_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgMobile(true) +
    `<g filter="url(#fShadow)" transform="rotate(-5 470 250)">
      <rect x="400" y="160" width="170" height="190" rx="16" fill="#F8FAFF"/>
      <rect x="400" y="160" width="170" height="40" rx="16" fill="${C.accent}"/><rect x="400" y="184" width="170" height="16" fill="${C.accent}"/>
      ${T(418, 187, 16, 'MOCK TEST 12', { color: C.ink })}
      ${[0, 1, 2].map(i => `<circle cx="424" cy="${226 + i * 36}" r="11" fill="${C.ink}"/>${icon('check', 424, 226 + i * 36, 13, C.accent)}
        <rect x="444" y="${219 + i * 36}" width="${100 - i * 12}" height="7" rx="3.5" fill="#DCE2EF"/>
        <rect x="444" y="${231 + i * 36}" width="${70 - i * 8}" height="5" rx="2.5" fill="#E8ECF5"/>`).join('')}
    </g>` +
    student(520, 176, 0.75, { skin: 'light', hair: 'ponytail', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'shirt', pose: 'think', glasses: true }) +
    `<g filter="url(#fShadow)"><circle cx="672" cy="196" r="48" fill="#fff"/>
      <circle cx="672" cy="196" r="35" fill="none" stroke="#E6EAF4" stroke-width="9"/>
      <circle cx="672" cy="196" r="35" fill="none" stroke="${C.accent}" stroke-width="9" stroke-linecap="round"
        stroke-dasharray="${2 * Math.PI * 35 * 0.92} 999" transform="rotate(-90 672 196)"/>
      ${T(672, 203, 20, '92%', { anchor: 'middle' })}</g>` +
    markLine(30, 100, 44, 'Boost Your', 'Score', '', true) +
    markLine(30, 154, 44, 'with', 'Smart Tests', '', true) +
    T(30, 194, 21, 'Mock tests · PYQs · All-India rank', { weight: 600, color: '#C3C9E6' }) +
    pill(30, 228, 46, 'phone', BRAND.phone, { bg: '#1E2550', stroke: '#323B70' }) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#1E2550', stroke: '#323B70' }) +
    sparkle(470, 120, 10) + sparkle(720, 300, 8, '#fff'),
};

ASSETS.banner_3_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgMobile() +
    `<path d="M410 400 C440 260 730 260 760 400 Z" fill="url(#gBrand)"/>` +
    student(420, 220, 0.6, { skin: 'brown', hair: 'braid', top: C.navy, pose: 'books', mouth: 'open' }) +
    student(600, 220, 0.6, { skin: 'wheat', hair: 'short', top: C.ink, collar: 'shirt', pose: 'wave', mouth: 'open' }) +
    student(506, 186, 0.7, { skin: 'light', hair: 'long', pose: 'grad', collar: 'gown', top: C.ink, cap: true, mouth: 'open' }) +
    infoCard(470, 90, 200, 62, 'users', '900+', 'Happy students') +
    markLine(30, 96, 36, 'Knowledge That', '') +
    markLine(30, 142, 36, 'Costs Nothing,', '') +
    markLine(30, 188, 36, '', 'Empowers Everything.') +
    pill(30, 228, 46, 'phone', BRAND.phone) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#DCE4F7' }) +
    sparkle(700, 140, 10, C.ink) + sparkle(440, 120, 8),
};

/* ---------- banner 4: brand spectrum background (blue -> violet -> magenta) ---------- */

function bannerBgBrand(w, h) {
  return `<defs><linearGradient id="bgBrand${w}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${C.blueD}"/><stop offset=".45" stop-color="${C.blue}"/><stop offset=".78" stop-color="${C.violet}"/><stop offset="1" stop-color="${C.magenta}"/></linearGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#bgBrand${w})"/>
    <rect width="${w}" height="${h}" fill="url(#pDotsW)" opacity=".55"/>`;
}

ASSETS.banner_4_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgBrand(1920, 300) +
    `<path d="M0 0 H210 C150 90 170 210 90 300 H0 Z" fill="url(#gWarm)"/>
     <path d="M0 0 H150 C100 80 110 200 40 300 H0 Z" fill="${C.ink}"/>
     <path d="M1920 300 H1700 C1760 240 1780 140 1860 90 C1890 70 1910 60 1920 58 Z" fill="${C.ink}"/>
     <path d="M1920 300 H1790 C1830 250 1850 180 1920 150 Z" fill="url(#gWarm)"/>
     ${rings(1180, 330, 300, 3, '#fff', 0.2, 2.5)}
     <circle cx="1180" cy="330" r="240" fill="#fff" opacity=".14"/>` +
    markLine(320, 92, 50, 'Learn Anytime,', '', '', true) +
    markLine(320, 148, 50, '', 'Anywhere.', '', true) +
    T(320, 184, 20, 'HD video lectures, notes &amp; e-books. Study at your own pace.', { weight: 600, color: 'rgba(255,255,255,.86)' }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    student(1150, 66, 0.78, { skin: 'brown', hair: 'long', top: C.accent, topShade: 'rgba(160,70,0,.25)', pose: 'wave', mouth: 'open', earring: true }) +
    `<rect x="930" y="282" width="360" height="18" rx="4" fill="${C.ink}"/>` +
    laptopFront(1080, 284, 250) +
    openBook(1450, 230, 130, C.ink) +
    infoCard(880, 36, 240, 70, 'play', 'Video Courses', 'Watch anytime') +
    infoCard(1400, 90, 230, 70, 'book', 'E-Library', 'Notes &amp; e-books') +
    sparkle(1300, 40, 14, '#fff') + sparkle(900, 272, 10, C.accentL) + sparkle(1560, 200, 9, '#fff') +
    formulaChip(1690, 50, 'H₂O', 24, 8),
};

ASSETS.banner_4_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgBrand(750, 400) +
    `<circle cx="590" cy="420" r="210" fill="#fff" opacity=".14"/>${rings(590, 420, 250, 3, '#fff', 0.2, 2.5)}` +
    student(510, 190, 0.7, { skin: 'brown', hair: 'long', top: C.accent, topShade: 'rgba(160,70,0,.25)', pose: 'wave', mouth: 'open', earring: true }) +
    `<rect x="400" y="384" width="350" height="16" fill="${C.ink}"/>` + laptopFront(500, 386, 190) +
    infoCard(470, 70, 220, 64, 'play', 'Video Courses', 'Watch anytime') +
    markLine(30, 100, 44, 'Learn Anytime,', '', '', true) +
    markLine(30, 154, 44, '', 'Anywhere.', '', true) +
    T(30, 194, 21, 'Videos · Notes · E-books', { weight: 600, color: 'rgba(255,255,255,.86)' }) +
    pill(30, 228, 46, 'phone', BRAND.phone) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#DCE4F7' }) +
    sparkle(720, 160, 10, '#fff'),
};

/* ---------- banners 5-7: colourful campaign banners (same layout, warm amber + ink accents) ---------- */

const HUES = {
  violet: { a: '#8B5CF6', b: '#5B2EE0', c: '#2A1078', glow: '#C4B5FD' },
  magenta: { a: '#F0529C', b: '#B5247A', c: '#4A0D47', glow: '#F9A8D4' },
  blue:   { a: '#3B82F6', b: '#1D4ED8', c: '#0F1E5C', glow: '#93C5FD' },
};
const CONFETTI = ['#FFB21E', '#FF6B8A', '#4ADE80', '#FFFFFF', '#38BDF8', '#FB923C'];

// Seeded scatter so every render is identical.
function seeded(seed) {
  let s = seed;
  return () => ((s = (s * 9301 + 49297) % 233280) / 233280);
}

function confetti(x0, y0, x1, y1, n, seed = 7, size = 1) {
  const r = seeded(seed);
  let out = '';
  for (let i = 0; i < n; i++) {
    const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0), c = CONFETTI[i % CONFETTI.length], k = r(), rot = Math.round(r() * 180);
    out += k < 0.45
      ? `<rect x="${x}" y="${y}" width="${10 * size}" height="${5 * size}" rx="${1.5 * size}" fill="${c}" transform="rotate(${rot} ${x} ${y})" opacity=".9"/>`
      : k < 0.8 ? `<circle cx="${x}" cy="${y}" r="${3.4 * size}" fill="${c}" opacity=".9"/>`
        : `<path d="M${x} ${y} q${5 * size} ${-6 * size} ${10 * size} 0 t${10 * size} 0" stroke="${c}" stroke-width="${2.6 * size}" fill="none" stroke-linecap="round" transform="rotate(${rot} ${x} ${y})"/>`;
  }
  return out;
}

function bannerBgHue(hue, w, h) {
  const p = HUES[hue], id = `bgHue${hue}${w}`;
  const wide = w > h * 3;
  return `<defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${p.a}"/><stop offset=".5" stop-color="${p.b}"/><stop offset="1" stop-color="${p.c}"/></linearGradient>
      <radialGradient id="${id}g" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="${p.glow}" stop-opacity=".6"/><stop offset="1" stop-color="${p.glow}" stop-opacity="0"/></radialGradient></defs>
    <rect width="${w}" height="${h}" fill="url(#${id})"/>
    <rect width="${w}" height="${h}" fill="url(#pDotsW)" opacity=".55"/>
    <circle cx="${wide ? 1200 : 570}" cy="${wide ? 170 : 250}" r="${wide ? 320 : 240}" fill="url(#${id}g)"/>` +
    (wide
      ? `<path d="M0 0 H210 C150 90 170 210 90 300 H0 Z" fill="${C.accent}"/>
         <path d="M0 0 H150 C100 80 110 200 40 300 H0 Z" fill="${C.ink}"/>
         ${rings(250, 30, 120, 3, '#fff', 0.25, 3)}
         <path d="M1920 300 H1700 C1760 240 1780 140 1860 90 C1890 70 1910 60 1920 58 Z" fill="${C.ink}"/>
         <path d="M1920 300 H1790 C1830 250 1850 180 1920 150 Z" fill="${C.accent}"/>`
      : `${rings(700, 60, 120, 3, '#fff', 0.3, 3)}<path d="M0 400 V330 C40 350 60 380 120 400 Z" fill="${C.accent}"/>`);
}

const SUB_ON_HUE = 'rgba(255,255,255,.86)';

// Coupon ticket with notches: big stub figure on the left, offer on the right.
function ticket(x, y, w, h, rot, stubBig, stubSmall, main, mainSub) {
  const id = uid('tk'), stub = w * 0.34, r = h * 0.13;
  return `<g transform="rotate(${rot} ${x + w / 2} ${y + h / 2})" filter="url(#fShadow)">
    <defs><mask id="${id}" maskUnits="userSpaceOnUse" x="${x - 5}" y="${y - 5}" width="${w + 10}" height="${h + 10}">
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h * 0.12}" fill="#fff"/>
      <circle cx="${x + stub}" cy="${y}" r="${r}" fill="#000"/><circle cx="${x + stub}" cy="${y + h}" r="${r}" fill="#000"/>
      <circle cx="${x}" cy="${y + h / 2}" r="${r * 0.8}" fill="#000"/><circle cx="${x + w}" cy="${y + h / 2}" r="${r * 0.8}" fill="#000"/></mask></defs>
    <g mask="url(#${id})">
      <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#gBrand)"/>
      <rect x="${x}" y="${y}" width="${stub}" height="${h}" fill="${C.ink}"/>
      <rect x="${x + stub}" y="${y}" width="${w - stub}" height="${h}" fill="url(#pDotsInk)" opacity=".35"/>
    </g>
    <path d="M${x + stub} ${y + r + 6} V${y + h - r - 6}" stroke="${C.ink}" stroke-width="3" stroke-dasharray="8 7" opacity=".55"/>
    ${T(x + stub / 2, y + h * 0.6, h * 0.52, stubBig, { anchor: 'middle', color: C.accent })}
    ${T(x + stub / 2, y + h * 0.8, h * 0.11, stubSmall, { anchor: 'middle', color: '#fff', ls: h * 0.012 })}
    ${T(x + stub + (w - stub) / 2, y + h * 0.56, h * 0.36, main, { anchor: 'middle', color: C.ink })}
    ${T(x + stub + (w - stub) / 2, y + h * 0.76, h * 0.1, mainSub, { anchor: 'middle', color: C.ink, weight: 700, ls: h * 0.01 })}
  </g>`;
}

function giftBox(x, bottom, w, color = '#FF6B8A') {
  const h = w * 0.78, lid = w * 0.24, y = bottom - h;
  return `<g filter="url(#fShadowS)">
    <rect x="${x + w * 0.06}" y="${y + lid}" width="${w * 0.88}" height="${h - lid}" rx="${w * 0.05}" fill="${color}"/>
    <rect x="${x}" y="${y}" width="${w}" height="${lid}" rx="${w * 0.05}" fill="${color}"/>
    <rect x="${x}" y="${y + lid * 0.72}" width="${w}" height="${lid * 0.28}" fill="rgba(0,0,0,.12)"/>
    <rect x="${x + w * 0.43}" y="${y}" width="${w * 0.14}" height="${h}" fill="${C.accent}"/>
    <path d="M${x + w / 2} ${y} C${x + w * 0.2} ${y - w * 0.32} ${x + w * 0.06} ${y - w * 0.02} ${x + w / 2} ${y}
             C${x + w * 0.8} ${y - w * 0.32} ${x + w * 0.94} ${y - w * 0.02} ${x + w / 2} ${y} Z" fill="${C.accent}" stroke="${C.accentD}" stroke-width="2"/>
  </g>`;
}

// White sticker chip with a coloured dot (board / exam names).
function tagChip(x, y, h, text, color, rot = 0, solid = false) {
  const fs = h * 0.44, w = textW(text, fs, SANS, 800) + h * 1.15;
  return `<g transform="rotate(${rot} ${x + w / 2} ${y + h / 2})" filter="url(#fShadowS)">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="${solid ? color : '#fff'}"/>
    <circle cx="${x + h * 0.48}" cy="${y + h / 2}" r="${h * 0.17}" fill="${solid ? '#fff' : color}"/>
    <text x="${x + h * 0.8}" y="${y + h * 0.65}" font-family="${SANS}" font-weight="800" font-size="${fs}" fill="${solid ? '#fff' : C.ink}">${text}</text></g>`;
}

function reportCard(x, y, w, rot, accent) {
  const h = w * 1.05, rows = [['Maths', 'A+', 0.96, '#3B82F6'], ['Science', 'A+', 0.92, '#22C55E'], ['English', 'A', 0.86, '#F97316'], ['SST', 'A+', 0.9, '#EC4899']];
  return `<g transform="rotate(${rot} ${x + w / 2} ${y + h / 2})" filter="url(#fShadow)">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${w * 0.08}" fill="#F8FAFF"/>
    <rect x="${x}" y="${y}" width="${w}" height="${h * 0.2}" rx="${w * 0.08}" fill="${accent}"/><rect x="${x}" y="${y + h * 0.12}" width="${w}" height="${h * 0.08}" fill="${accent}"/>
    ${T(x + w * 0.08, y + h * 0.135, w * 0.085, 'REPORT CARD', { color: '#fff', ls: 1 })}
    ${rows.map(([s, g, v, c], i) => {
      const ry = y + h * (0.32 + i * 0.165);
      return `${T(x + w * 0.08, ry, w * 0.07, s, { weight: 700, color: C.ink2 })}
        <rect x="${x + w * 0.08}" y="${ry + w * 0.03}" width="${w * 0.62}" height="${w * 0.035}" rx="${w * 0.018}" fill="#E6EAF4"/>
        <rect x="${x + w * 0.08}" y="${ry + w * 0.03}" width="${w * 0.62 * v}" height="${w * 0.035}" rx="${w * 0.018}" fill="${c}"/>
        ${T(x + w * 0.9, ry + w * 0.06, w * 0.1, g, { anchor: 'end', color: c })}`;
    }).join('')}
  </g>`;
}

// Bullseye with an arrow in the centre.
function target(cx, cy, r) {
  return `<g filter="url(#fShadow)">
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff"/><circle cx="${cx}" cy="${cy}" r="${r * 0.76}" fill="#FF6B8A"/>
    <circle cx="${cx}" cy="${cy}" r="${r * 0.54}" fill="#fff"/><circle cx="${cx}" cy="${cy}" r="${r * 0.32}" fill="${C.accent}"/>
    <circle cx="${cx}" cy="${cy}" r="${r * 0.12}" fill="${C.ink}"/></g>
    <path d="M${cx} ${cy} L${cx + r * 1.1} ${cy - r * 1.1}" stroke="${C.ink}" stroke-width="${r * 0.08}" stroke-linecap="round"/>
    <path d="M${cx + r * 1.1} ${cy - r * 1.1} l${r * 0.06} ${-r * 0.3} l${r * 0.2} ${r * 0.1} Z M${cx + r * 1.1} ${cy - r * 1.1} l${r * 0.3} ${-r * 0.06} l${-r * 0.1} ${r * 0.2} Z" fill="${C.accent}"/>`;
}

// Banner 5: free test series offer (violet).
ASSETS.banner_5_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgHue('violet', 1920, 300) +
    confetti(860, 14, 1660, 120, 34, 11) + confetti(1480, 150, 1680, 290, 10, 5) +
    tagChip(320, 22, 34, 'LIMITED-TIME OFFER', C.accent, 0, true) +
    markLine(320, 110, 50, '', 'FREE', ' Test Series', true) +
    markLine(320, 164, 50, 'for', '3 Months!', '', true) +
    T(320, 196, 20, 'All mock tests unlocked · Instant results · Solutions', { weight: 600, color: SUB_ON_HUE }) +
    contactRow(320, 214, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    `<circle cx="1225" cy="330" r="200" fill="#fff" opacity=".14"/>${rings(1225, 330, 250, 3, '#fff', 0.22, 2.5)}` +
    ticket(905, 66, 280, 146, -7, '3', 'MONTHS', 'FREE', 'TEST SERIES PASS') +
    student(1190, 66, 0.78, { skin: 'wheat', hair: 'ponytail', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'shirt', pose: 'wave', mouth: 'open' }) +
    giftBox(1376, 296, 84) +
    infoCard(1440, 34, 240, 70, 'check', 'All Tests Unlocked', 'Boards + 100+ exams') +
    infoCard(1470, 150, 220, 66, 'clock', '₹0 for 90 days', 'Start today', { iconBg: '#FF6B8A', iconColor: '#fff' }) +
    sparkle(1170, 40, 14) + sparkle(880, 250, 10, '#fff') + sparkle(1400, 130, 9, C.accent),
};

ASSETS.banner_5_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgHue('violet', 750, 400) +
    confetti(400, 20, 740, 160, 22, 11, 1.1) +
    `<circle cx="600" cy="430" r="190" fill="#fff" opacity=".14"/>` +
    ticket(430, 44, 250, 128, -8, '3', 'MONTHS', 'FREE', 'TEST SERIES PASS') +
    student(500, 196, 0.68, { skin: 'wheat', hair: 'ponytail', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'shirt', pose: 'wave', mouth: 'open' }) +
    giftBox(660, 398, 70) +
    tagChip(30, 34, 32, 'LIMITED-TIME OFFER', C.accent, 0, true) +
    markLine(30, 118, 46, '', 'FREE', ' Test Series', true) +
    markLine(30, 170, 46, 'for', '3 Months!', '', true) +
    T(30, 206, 21, 'All mock tests unlocked · ₹0', { weight: 600, color: SUB_ON_HUE }) +
    pill(30, 232, 46, 'phone', BRAND.phone) +
    pill(30, 290, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#E9E3FF' }) +
    sparkle(720, 220, 9, '#fff') + sparkle(420, 210, 8, C.accent),
};

// Banner 6: school boards (magenta).
const BOARD_CHIPS = [['CBSE', '#2563EB'], ['ICSE', '#EA580C'], ['UP Board', '#16A34A'], ['NIOS', '#0D9488'], ['+20 State Boards', '#DB2777']];

ASSETS.banner_6_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgHue('magenta', 1920, 300) +
    markLine(320, 92, 50, 'Ace Your', 'Board Exams', '', true) +
    markLine(320, 148, 50, 'Class', '1 to 12.', '', true) +
    T(320, 184, 20, 'Chapter-wise tests &amp; board mocks for every major board.', { weight: 600, color: SUB_ON_HUE }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    `<path d="M1010 300 C1050 150 1330 150 1370 300 Z" fill="#fff" opacity=".16"/>${rings(1190, 300, 240, 3, '#fff', 0.2, 2.5)}` +
    tagChip(940, 40, 44, BOARD_CHIPS[0][0], BOARD_CHIPS[0][1], -6) +
    tagChip(925, 112, 44, BOARD_CHIPS[1][0], BOARD_CHIPS[1][1], 4) +
    tagChip(945, 190, 44, BOARD_CHIPS[2][0], BOARD_CHIPS[2][1], -3) +
    tagChip(1290, 26, 40, BOARD_CHIPS[3][0], BOARD_CHIPS[3][1], 6) +
    student(1100, 70, 0.76, { skin: 'brown', hair: 'braid', top: C.ink, collar: 'shirt', pose: 'books', mouth: 'open', glasses: true }) +
    reportCard(1380, 54, 190, 5, '#B5247A') +
    tagChip(1580, 240, 40, BOARD_CHIPS[4][0], BOARD_CHIPS[4][1], -4, true) +
    sparkle(1300, 110, 13, C.accent) + sparkle(1610, 60, 10, '#fff') + sparkle(880, 268, 9, C.accent) +
    formulaChip(1700, 186, 'H₂SO₄', 22, -6),
};

ASSETS.banner_6_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgHue('magenta', 750, 400) +
    `<path d="M440 400 C470 270 720 270 750 400 Z" fill="#fff" opacity=".16"/>` +
    tagChip(460, 40, 36, 'CBSE', '#2563EB', -6) + tagChip(590, 30, 36, 'ICSE', '#EA580C', 5) +
    tagChip(450, 100, 36, 'UP Board', '#16A34A', 3) + tagChip(610, 92, 36, 'NIOS', '#0D9488', -4) +
    student(500, 186, 0.68, { skin: 'brown', hair: 'braid', top: C.ink, collar: 'shirt', pose: 'books', mouth: 'open', glasses: true }) +
    tagChip(560, 160, 32, '+20 State Boards', '#DB2777', -3, true) +
    markLine(30, 100, 46, 'Ace Your', '', '', true) +
    markLine(30, 152, 46, '', 'Board Exams', '', true) +
    T(30, 194, 21, 'Class 1 to 12 · Chapter-wise tests', { weight: 600, color: SUB_ON_HUE }) +
    pill(30, 228, 46, 'phone', BRAND.phone) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#FBD5E8' }) +
    sparkle(720, 250, 9, '#fff') + sparkle(440, 180, 8, C.accent),
};

// Banner 7: competitive exams (blue).
const EXAM_CHIPS = [['JEE', '#F97316'], ['NEET', '#22C55E'], ['UPSC', '#EC4899'], ['SSC', '#8B5CF6'], ['Banking', '#0EA5E9'], ['CUET', '#EAB308'], ['GATE', '#EF4444'], ['NDA', '#14B8A6']];

ASSETS.banner_7_desktop = {
  w: 1920, h: 300,
  draw: () => bannerBgHue('blue', 1920, 300) +
    markLine(320, 92, 46, 'Crack Your', 'Dream Exam', '', true) +
    markLine(320, 148, 46, 'with', 'Real Mocks.', '', true) +
    T(320, 184, 20, 'Full mocks · PYQ papers · Topic tests · 100+ exams', { weight: 600, color: SUB_ON_HUE }) +
    contactRow(320, 206, 44, [['phone', BRAND.phone], ['mail', BRAND.email]]) +
    `<circle cx="1180" cy="330" r="220" fill="#fff" opacity=".13"/>${rings(1180, 330, 270, 3, '#fff', 0.2, 2.5)}` +
    tagChip(915, 34, 42, 'JEE', EXAM_CHIPS[0][1], -5) + tagChip(1030, 24, 42, 'NEET', EXAM_CHIPS[1][1], 4) +
    tagChip(905, 104, 42, 'UPSC', EXAM_CHIPS[2][1], 3) + tagChip(915, 176, 42, 'SSC', EXAM_CHIPS[3][1], -4) +
    tagChip(1300, 28, 42, 'Banking', EXAM_CHIPS[4][1], 5) + tagChip(1290, 102, 42, 'CUET', EXAM_CHIPS[5][1], -3) +
    tagChip(1310, 176, 42, 'GATE', EXAM_CHIPS[6][1], 4) + tagChip(1000, 236, 40, 'NDA', EXAM_CHIPS[7][1], -2) +
    student(1095, 68, 0.78, { skin: 'light', hair: 'short', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'hoodie', pose: 'think', glasses: true }) +
    target(1500, 196, 54) +
    infoCard(1450, 34, 240, 70, 'trophy', 'Rank Booster', 'All-India comparison') +
    sparkle(1240, 250, 12, C.accent) + sparkle(1630, 140, 10, '#fff') + sparkle(860, 270, 9, '#fff') +
    formulaChip(1700, 196, '∫ x dx', 22, -6),
};

ASSETS.banner_7_mobile = {
  w: 750, h: 400, scale: 2,
  draw: () => bannerBgHue('blue', 750, 400) +
    `<circle cx="590" cy="430" r="200" fill="#fff" opacity=".13"/>` +
    tagChip(440, 36, 34, 'JEE', '#F97316', -5) + tagChip(540, 26, 34, 'NEET', '#22C55E', 4) +
    tagChip(650, 40, 34, 'UPSC', '#EC4899', -3) + tagChip(430, 104, 34, 'SSC', '#8B5CF6', 3) +
    tagChip(630, 104, 34, 'Banking', '#0EA5E9', -4) +
    student(490, 190, 0.68, { skin: 'light', hair: 'short', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'hoodie', pose: 'think', glasses: true }) +
    target(690, 300, 36) +
    markLine(30, 100, 46, 'Crack Your', '', '', true) +
    markLine(30, 152, 46, '', 'Dream Exam', '', true) +
    T(30, 194, 21, 'Mocks · PYQs · 100+ exams', { weight: 600, color: SUB_ON_HUE }) +
    pill(30, 228, 46, 'phone', BRAND.phone) +
    pill(30, 286, 46, 'mail', BRAND.email, { bg: '#fff', fg: C.ink, stroke: '#DCE8FF' }) +
    sparkle(420, 200, 8, C.accent),
};

/* ---------- login / signup: desktop 1000x1400 (safe x 190..810, keep y > 1270 quiet) ---------- */

// Centered line with an optional tail painted in the brand spectrum (light) or amber (dark).
function centerLine(cx, y, size, plain, tail = '', dark = false) {
  const font = `font-family="${SANS}" font-weight="800" font-size="${size}"`;
  if (!tail) return `<text x="${cx}" y="${y}" text-anchor="middle" ${font} fill="${dark ? '#fff' : C.ink}">${plain}</text>`;
  const wp = plain ? textW(plain, size, SANS, 800) : 0, wt = textW(tail, size, SANS, 800), x = cx - (wp + wt) / 2;
  return (plain ? `<text x="${x}" y="${y}" ${font} fill="${dark ? '#fff' : C.ink}">${plain}</text>` : '') +
    `<text x="${x + wp}" y="${y}" ${font} fill="${dark ? C.accentL : 'url(#gBrandH)'}">${tail}</text>`;
}

function centeredPill(cx, y, h, ic, text, opts) {
  return pill(cx - pillWidth(h, text) / 2, y, h, ic, text, opts);
}

function deskScene(cx, top, k, person, dark) {
  const deskY = top + 296 * k;
  return `<circle cx="${cx}" cy="${top + 190 * k}" r="${170 * k}" fill="url(#gBrand)"/>
    ${rings(cx, top + 190 * k, 210 * k, 3, dark ? C.accent : C.ink, dark ? 0.35 : 0.12, 3)}` +
    deskLamp(cx - 205 * k, deskY, 160 * k, dark) +
    student(cx - 120 * k, top, k, person) +
    `<rect x="${cx - 215 * k}" y="${deskY - 2}" width="${430 * k}" height="${22 * k}" rx="${6 * k}" fill="${dark ? '#252C5C' : C.ink}"/>
     <rect x="${cx - 190 * k}" y="${deskY + 20 * k}" width="${12 * k}" height="${70 * k}" fill="${dark ? '#252C5C' : C.ink}"/>
     <rect x="${cx + 178 * k}" y="${deskY + 20 * k}" width="${12 * k}" height="${70 * k}" fill="${dark ? '#252C5C' : C.ink}"/>` +
    laptopBack(cx, deskY, 190 * k, dark) +
    bookStack(cx + 110 * k, deskY, 80 * k) + mug(cx + 128 * k, deskY - 64 * k, 30 * k) +
    plant(cx - 165 * k, deskY, 60 * k);
}

ASSETS.auth_login_desktop = {
  w: 1000, h: 1400,
  draw: () => `<rect width="1000" height="1400" fill="url(#gInk)"/>
    <rect width="1000" height="1400" fill="url(#pDotsW)" opacity=".6"/>
    <circle cx="500" cy="860" r="460" fill="url(#gGlow)" opacity=".5"/>
    ${rings(-40, 200, 260, 4, C.violet, 0.45, 3)}${rings(1060, 1180, 260, 4, C.accent, 0.3, 3)}` +
    logoStacked(500, 110, 440, true) +
    centerLine(500, 418, 56, 'Your success story', '', true) +
    centerLine(500, 484, 56, '', 'continues here.', true) +
    T(500, 538, 26, 'Pick up right where you left off.', { anchor: 'middle', weight: 600, color: '#B8BFE0' }) +
    deskScene(500, 640, 1.45, { skin: 'wheat', hair: 'bun', top: C.navyL, pose: 'desk', eyes: 'down', earring: true }, true) +
    infoCard(185, 640, 250, 76, 'clock', 'Live at 6 PM', 'Physics · Chapter 4', {}) +
    infoCard(565, 780, 250, 76, 'trophy', 'Score 98%', 'Mock Test #12', { bar: 0.98 }) +
    sparkle(250, 790, 16) + sparkle(770, 660, 12, '#fff') + sparkle(820, 980, 9) +
    centeredPill(500, 1150, 56, 'phone', BRAND.phone, { bg: '#1E2550', stroke: '#323B70' }) +
    centeredPill(500, 1218, 50, 'mail', BRAND.email, { bg: 'transparent', shadow: false, iconBg: '#1E2550', iconColor: C.accent, fg: '#D4D9F0' }),
};

ASSETS.auth_signup_desktop = {
  w: 1000, h: 1400,
  draw: () => `<rect width="1000" height="1400" fill="url(#bgSign)"/>
    <defs><linearGradient id="bgSign" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F8FAFF"/><stop offset=".6" stop-color="#EEF2FF"/><stop offset="1" stop-color="#DDE5FF"/></linearGradient></defs>
    <rect x="60" y="560" width="200" height="160" fill="url(#pDots)" opacity=".45"/>
    <rect x="760" y="380" width="180" height="140" fill="url(#pDots)" opacity=".45"/>
    ${rings(1040, 160, 240, 4, C.accent, 0.4, 3)}` +
    logoStacked(500, 100, 440) +
    centerLine(500, 404, 54, 'Start your journey') +
    markLine(500 - textW('to success today.', 54, SANS, 800) / 2, 470, 54, '', 'to success today.') +
    T(500, 524, 25, 'Create a free account in under a minute.', { anchor: 'middle', weight: 600, color: C.mute }) +
    `<path d="M150 990 C210 720 790 720 850 990 Z" fill="url(#gBrand)"/>
     ${rings(500, 990, 360, 3, C.ink, 0.1, 3)}` +
    student(196, 640, 1.2, { skin: 'brown', hair: 'braid', top: C.navy, pose: 'books', mouth: 'open' }) +
    student(516, 640, 1.2, { skin: 'deep', hair: 'curly', top: C.coral, collar: 'hoodie', pose: 'wave', mouth: 'open' }) +
    student(340, 590, 1.33, { skin: 'light', hair: 'long', pose: 'grad', collar: 'gown', top: C.ink, cap: true, mouth: 'open' }) +
    `<rect x="0" y="990" width="1000" height="410" fill="${C.ink}"/>
     <rect x="0" y="990" width="1000" height="410" fill="url(#pDotsW)" opacity=".5"/>` +
    [['play', 'Video Courses'], ['live', 'Live Classes'], ['check', 'Test Series'], ['book', 'E-Library']].map(([ic, label], i) => {
      const x = 196 + (i % 2) * 312, y = 1030 + Math.floor(i / 2) * 70;
      return `<rect x="${x}" y="${y}" width="296" height="56" rx="28" fill="#1A2048" stroke="#2C3566" stroke-width="2"/>
        <circle cx="${x + 28}" cy="${y + 28}" r="19" fill="${C.accent}"/>${icon(ic, x + 28, y + 28, 18, C.ink)}
        ${T(x + 58, y + 36, 22, label, { color: '#fff', weight: 700 })}`;
    }).join('') +
    centeredPill(500, 1180, 52, 'phone', BRAND.phone, { bg: C.accent, fg: C.ink, iconBg: C.ink, iconColor: C.accent }),
};

/* ---------- login / signup: mobile 1200x480 (shown as a short strip above the form) ---------- */

ASSETS.auth_login_mobile = {
  w: 1200, h: 480,
  draw: () => `<rect width="1200" height="480" fill="url(#gInk)"/>
    <rect width="1200" height="480" fill="url(#pDotsW)" opacity=".6"/>
    <circle cx="880" cy="300" r="330" fill="url(#gGlow)" opacity=".5"/>
    ${rings(1180, 40, 160, 3, C.accent, 0.35, 3)}` +
    logoHorizontal(90, 60, 74, true) +
    T(90, 250, 66, 'Welcome back!', { color: '#fff' }) +
    `<text x="90" y="312" font-family="${SANS}" font-weight="700" font-size="34" fill="#C3C9E6">Your success story <tspan fill="${C.accentL}">continues here.</tspan></text>` +
    pill(90, 352, 62, 'phone', BRAND.phone, { bg: '#1E2550', stroke: '#323B70' }) +
    deskScene(890, 150, 1.05, { skin: 'wheat', hair: 'bun', top: C.navyL, pose: 'desk', eyes: 'down', earring: true }, true),
};

ASSETS.auth_signup_mobile = {
  w: 1200, h: 480,
  draw: () => `<rect width="1200" height="480" fill="url(#bgSignM)"/>
    <defs><linearGradient id="bgSignM" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F8FAFF"/><stop offset="1" stop-color="#E2E9FF"/></linearGradient></defs>
    <rect x="620" y="30" width="160" height="110" fill="url(#pDots)" opacity=".45"/>` +
    logoHorizontal(90, 60, 74) +
    T(90, 250, 62, 'Start your journey', {}) +
    markLine(90, 318, 62, '', 'to success today.') +
    T(90, 396, 30, 'Live Classes · Test Series · E-Library', { weight: 700, color: C.mute }) +
    `<path d="M700 480 C740 280 1160 280 1200 480 Z" fill="url(#gBrand)"/>` +
    student(700, 230, 0.95, { skin: 'brown', hair: 'braid', top: C.navy, pose: 'books', mouth: 'open' }) +
    student(950, 230, 0.95, { skin: 'deep', hair: 'curly', top: C.coral, collar: 'hoodie', pose: 'wave', mouth: 'open' }) +
    student(820, 180, 1.05, { skin: 'light', hair: 'long', pose: 'grad', collar: 'gown', top: C.ink, cap: true, mouth: 'open' }),
};

/* ---------- course thumbnail placeholder 800x450 ---------- */

ASSETS.default_thumb = {
  w: 800, h: 450,
  draw: () => `<rect width="800" height="450" fill="url(#bgThumb)"/>
    <defs><linearGradient id="bgThumb" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F8FAFF"/><stop offset="1" stop-color="#E5EBFF"/></linearGradient></defs>
    <rect x="40" y="40" width="160" height="110" fill="url(#pDots)" opacity=".45"/>
    <circle cx="420" cy="250" r="170" fill="url(#gBrand)"/>${rings(420, 250, 210, 3, C.ink, 0.12, 3)}
    <rect x="160" y="356" width="520" height="18" rx="6" fill="${C.ink}"/>` +
    laptopFront(410, 358, 260) + bookStack(560, 356, 120) + plant(200, 358, 110) +
    `<g transform="rotate(-12 620 150)">${gradCap(620, 120, 120)}</g>` +
    formulaChip(90, 230, 'E = mc²', 24, -8) + sparkle(560, 80, 16) + sparkle(250, 120, 10, C.ink) +
    logoHorizontal(40, 394, 40),
};

/* ---------- character test sheet (dev only) ---------- */

ASSETS._sheet = {
  w: 1600, h: 420,
  draw: () => `<rect width="1600" height="420" fill="${C.cream}"/>` +
    student(0, 60, 1, { skin: 'wheat', hair: 'ponytail', top: C.navy, pose: 'books', glasses: true }) +
    student(260, 60, 1, { skin: 'brown', hair: 'short', top: C.accent, topShade: 'rgba(160,70,0,.25)', collar: 'shirt', pose: 'think' }) +
    student(520, 60, 1, { skin: 'light', hair: 'long', top: C.ink, pose: 'grad', collar: 'gown', cap: true, mouth: 'open' }) +
    student(780, 60, 1, { skin: 'deep', hair: 'curly', top: C.coral, collar: 'hoodie', pose: 'wave', mouth: 'open' }) +
    student(1040, 60, 1, { skin: 'wheat', hair: 'bun', top: C.navyL, pose: 'desk', eyes: 'down', earring: true }) +
    `<rect x="1040" y="350" width="260" height="70" fill="${C.ink}"/>` + laptopBack(1170, 356, 150) +
    student(1300, 60, 1, { skin: 'brown', hair: 'braid', top: C.green, pose: 'books', mouth: 'open' }),
};

ASSETS._props = {
  w: 1600, h: 300,
  draw: () => `<rect width="1600" height="300" fill="#fff"/>` + bookStack(40, 260, 160) + openBook(330, 200, 200) +
    laptopFront(560, 260, 200) + deskLamp(700, 260, 200) + plant(900, 260, 160) + mug(1060, 260, 70) +
    sparkle(1180, 80, 24) + infoCard(1220, 40, 330, 96, 'trophy', 'Score 98%', 'Mock Test #12', { bar: 0.98 }) +
    pill(1220, 170, 64, 'phone', BRAND.phone) + formulaChip(1220, 240, 'E = mc²', 22),
};
