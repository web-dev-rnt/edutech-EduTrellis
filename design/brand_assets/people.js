// Illustrated students and study props. Every student is drawn front-facing in a
// 240x320 local frame (head centred at 120,92) and placed with translate/scale.

const SKIN = {
  light: { base: '#F1C3A0', shade: '#DDA47E' },
  wheat: { base: '#DDA27A', shade: '#C4865E' },
  brown: { base: '#B57A52', shade: '#99613D' },
  deep:  { base: '#8A5636', shade: '#6F4127' },
};
const HAIR = '#1C1515';

function hairBack(o) {
  const h = o.hairColor || HAIR;
  switch (o.hair) {
    case 'long':
      return `<path d="M76 74 C72 40 96 30 120 30 C146 30 170 40 166 76 L176 196 C150 214 92 214 64 196 Z" fill="${h}"/>`;
    case 'ponytail':
      return `<path d="M150 56 C196 58 204 126 182 168 C176 180 164 184 160 176 C176 140 172 100 146 82 Z" fill="${h}"/>
        <circle cx="156" cy="62" r="9" fill="${C.accent}"/>`;
    case 'bun':
      return `<circle cx="120" cy="30" r="22" fill="${h}"/><rect x="104" y="44" width="32" height="7" rx="3.5" fill="${C.accent}"/>`;
    case 'braid':
      return `<path d="M84 70 C70 110 78 150 70 196 C80 204 92 200 96 192 C96 150 92 110 96 76 Z" fill="${h}"/>
        <circle cx="80" cy="200" r="7" fill="${C.accent}"/>`;
    default:
      return '';
  }
}

function hairFront(o) {
  const h = o.hairColor || HAIR;
  switch (o.hair) {
    case 'short':
      return `<path d="M78 96 C70 48 96 30 124 30 C154 30 172 50 164 96 C162 82 158 72 152 66 C138 76 106 80 90 68 C84 76 80 86 78 96 Z" fill="${h}"/>
        <path d="M96 42 C110 30 140 30 150 46 C134 40 112 40 96 42 Z" fill="#fff" opacity=".08"/>`;
    case 'curly':
      return `<g fill="${h}"><circle cx="88" cy="66" r="16"/><circle cx="104" cy="50" r="18"/><circle cx="126" cy="44" r="19"/>
        <circle cx="148" cy="54" r="17"/><circle cx="160" cy="72" r="13"/><circle cx="80" cy="84" r="9"/><circle cx="162" cy="88" r="8"/></g>`;
    default: // girls' styles share a side-parted fringe
      return `<path d="M78 104 C68 52 96 32 122 32 C154 32 174 54 164 106 C162 86 154 70 142 62 C128 76 102 82 84 78 C80 86 79 96 78 104 Z" fill="${h}"/>
        <path d="M100 44 C116 36 140 38 152 52 C136 46 116 46 100 44 Z" fill="#fff" opacity=".08"/>` +
        (o.hair === 'long' ? `<path d="M82 82 C74 120 78 156 72 190 L88 192 C90 156 86 118 90 86 Z" fill="${h}"/>
          <path d="M158 82 C166 120 162 156 168 190 L152 192 C150 156 154 118 150 86 Z" fill="${h}"/>` : '');
  }
}

function face(o) {
  const s = SKIN[o.skin];
  const ink = '#1C1515';
  const eyes = o.eyes === 'down'
    ? `<path d="M97 100 Q104 105 111 100" stroke="${ink}" stroke-width="3.4" fill="none" stroke-linecap="round"/>
       <path d="M129 100 Q136 105 143 100" stroke="${ink}" stroke-width="3.4" fill="none" stroke-linecap="round"/>`
    : `<ellipse cx="104" cy="99" rx="4.6" ry="5.6" fill="${ink}"/><ellipse cx="136" cy="99" rx="4.6" ry="5.6" fill="${ink}"/>
       <circle cx="105.6" cy="97" r="1.6" fill="#fff"/><circle cx="137.6" cy="97" r="1.6" fill="#fff"/>`;
  const brow = o.hair === 'short' || o.hair === 'curly' ? 3.6 : 2.8;
  const mouth = o.mouth === 'open'
    ? `<path d="M110 118 Q120 132 130 118 Z" fill="#7B2D2D"/><path d="M112 119 L128 119 L127 122 L113 122 Z" fill="#fff"/>`
    : `<path d="M111 119 Q120 126 129 119" stroke="#7B2D2D" stroke-width="3" fill="none" stroke-linecap="round"/>`;
  return `
    <ellipse cx="80" cy="100" rx="8" ry="11" fill="${s.shade}"/><ellipse cx="160" cy="100" rx="8" ry="11" fill="${s.shade}"/>
    <path d="M82 86 C82 56 98 44 120 44 C142 44 158 56 158 86 L158 100 C158 126 140 140 120 140 C100 140 82 126 82 100 Z" fill="${s.base}"/>
    <path d="M150 64 C160 80 160 108 152 124 C146 134 136 139 126 140 C142 128 152 104 150 64 Z" fill="${s.shade}" opacity=".45"/>
    <path d="M95 87 Q104 82 113 86" stroke="${HAIR}" stroke-width="${brow}" fill="none" stroke-linecap="round"/>
    <path d="M127 86 Q136 82 145 87" stroke="${HAIR}" stroke-width="${brow}" fill="none" stroke-linecap="round"/>
    ${eyes}
    <path d="M120 103 Q116 112 121 114" stroke="${s.shade}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
    <circle cx="97" cy="113" r="7" fill="#F0806E" opacity=".22"/><circle cx="143" cy="113" r="7" fill="#F0806E" opacity=".22"/>
    ${mouth}
    ${o.glasses ? `<g fill="none" stroke="${C.ink}" stroke-width="3"><rect x="91" y="88" width="26" height="22" rx="9"/><rect x="123" y="88" width="26" height="22" rx="9"/><path d="M117 97 Q120 94 123 97"/></g>
      <path d="M94 92 L100 92" stroke="#fff" stroke-width="2" opacity=".6" stroke-linecap="round"/>` : ''}
    ${o.earring ? `<circle cx="80" cy="113" r="3" fill="${C.accent}"/><circle cx="160" cy="113" r="3" fill="${C.accent}"/>` : ''}`;
}

function torso(o) {
  const s = SKIN[o.skin];
  const top = o.top || C.navy, shade = o.topShade || 'rgba(0,0,0,.14)';
  let collar = '';
  if (o.collar === 'shirt') {
    collar = `<path d="M108 160 L120 186 L132 160 Z" fill="${s.base}"/>
      <path d="M104 156 L120 184 L108 192 L94 166 Z" fill="#fff"/><path d="M136 156 L120 184 L132 192 L146 166 Z" fill="#fff"/>`;
  } else if (o.collar === 'hoodie') {
    collar = `<path d="M92 164 C100 188 140 188 148 164" stroke="${shade}" stroke-width="10" fill="none"/>
      <path d="M112 182 L110 214 M128 182 L130 214" stroke="#fff" stroke-width="3" stroke-linecap="round"/>`;
  } else if (o.collar === 'gown') {
    collar = `<path d="M100 162 L120 196 L140 162 Z" fill="#fff"/>
      <path d="M94 162 L120 214 L108 320 L84 320 L80 176 Z" fill="url(#gBrand)"/><path d="M146 162 L120 214 L132 320 L156 320 L160 176 Z" fill="url(#gBrand)"/>`;
  } else {
    collar = `<path d="M104 162 Q120 180 136 162" stroke="${shade}" stroke-width="7" fill="none" stroke-linecap="round"/>`;
  }
  return `
    <path d="M106 126 L106 158 Q120 168 134 158 L134 126 Z" fill="${s.shade}"/>
    <path d="M36 320 C36 222 66 168 120 164 C174 168 204 222 204 320 Z" fill="${top}"/>
    <path d="M150 172 C182 186 200 230 204 320 L172 320 C176 250 168 200 150 172 Z" fill="${shade}"/>
    ${collar}
    ${o.badge ? `<circle cx="160" cy="214" r="9" fill="${C.accent}"/><path d="M155 214 l3.5 3.5 6-7" stroke="${C.ink}" stroke-width="2.4" fill="none" stroke-linecap="round"/>` : ''}`;
}

function limb(d, color, w = 30) {
  return `<path d="${d}" stroke="${color}" stroke-width="${w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
}
const hand = (x, y, s, r = 13) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${s.base}"/><path d="M${x + r * 0.2} ${y - r * 0.85} A${r} ${r} 0 0 1 ${x + r * 0.85} ${y + r * 0.2}" stroke="${s.shade}" stroke-width="${r * 0.35}" fill="none" opacity=".6"/>`;

function book(x, y, w, h, color, opts = {}) {
  const spine = opts.spine || 'rgba(0,0,0,.18)';
  return `<g transform="rotate(${opts.rot || 0} ${x + w / 2} ${y + h / 2})">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${Math.min(5, h / 4)}" fill="${color}"/>
    <rect x="${x + w * 0.06}" y="${y + h * 0.22}" width="${w * 0.9}" height="${h * 0.5}" rx="${h * 0.12}" fill="#FFFDF6"/>
    <path d="M${x + w * 0.06} ${y + h * 0.36} H${x + w * 0.96} M${x + w * 0.06} ${y + h * 0.56} H${x + w * 0.96}" stroke="#EFDDE0" stroke-width="1.4"/>
    <rect x="${x}" y="${y}" width="${w * 0.07}" height="${h}" fill="${spine}"/>
    ${opts.label ? `<rect x="${x + w * 0.62}" y="${y + h * 0.05}" width="${w * 0.2}" height="${h * 0.12}" fill="${C.accent}"/>` : ''}
  </g>`;
}

// Student holding a stack of books against the chest.
function poseBooks(o) {
  const s = SKIN[o.skin], top = o.top || C.navy;
  return limb('M64 212 Q48 272 96 280', top) + limb('M176 212 Q192 272 144 280', top) +
    book(70, 238, 100, 22, C.ink, { rot: -5 }) + book(74, 258, 94, 22, C.accent, { rot: -2, label: true }) + book(66, 276, 106, 22, C.navyL, { rot: 3 }) +
    hand(78, 276, s) + hand(162, 276, s);
}

// Thinking pose: pencil at the chin, notebook in the other arm.
function poseThink(o) {
  const s = SKIN[o.skin], top = o.top || C.navy;
  return `<rect x="40" y="226" width="54" height="80" rx="6" fill="${C.accent}" transform="rotate(-8 67 266)"/>
    <rect x="46" y="232" width="42" height="68" rx="4" fill="#fff" opacity=".35" transform="rotate(-8 67 266)"/>` +
    limb('M64 212 Q54 262 78 288', top) + hand(80, 290, s) +
    limb('M176 212 L192 278 L150 170', top, 28) +
    `<g transform="rotate(28 150 160)"><rect x="144" y="104" width="10" height="62" rx="3" fill="${C.accent}"/><path d="M144 104 L149 90 L154 104 Z" fill="#F3D9B0"/><path d="M147.5 94 L149 90 L150.5 94 Z" fill="${C.ink}"/><rect x="144" y="160" width="10" height="8" fill="${C.coral}"/></g>` +
    hand(148, 162, s, 14);
}

// Arms reaching forward onto a desk (desk drawn by the scene over the lower body).
function poseDesk(o) {
  const s = SKIN[o.skin], top = o.top || C.navy;
  return limb('M66 214 Q56 262 92 296', top) + limb('M174 214 Q184 262 148 296', top) + hand(96, 298, s) + hand(144, 298, s);
}

// Graduate holding a rolled diploma.
function poseGrad(o) {
  const s = SKIN[o.skin];
  return limb('M64 212 Q50 270 100 272', C.ink) + limb('M176 212 Q190 270 140 272', C.ink) +
    `<g transform="rotate(-12 120 268)"><rect x="70" y="258" width="104" height="22" rx="11" fill="#FFFDF6"/><circle cx="174" cy="269" r="11" fill="#F3E2E4"/>
     <rect x="112" y="256" width="12" height="26" fill="${C.coral}"/><path d="M118 282 l-8 18 l8 -5 l8 5 z" fill="${C.coral}"/></g>` +
    hand(96, 274, s) + hand(146, 266, s);
}

// Waving / hello pose with a book tucked in the other arm.
function poseWave(o) {
  const s = SKIN[o.skin], top = o.top || C.navy;
  return limb('M176 210 L206 190 L214 120', top, 28) + hand(214, 112, s, 14) +
    book(46, 230, 26, 84, C.accent, { rot: -8 }) +
    limb('M64 212 Q50 262 76 292', top) + hand(78, 292, s);
}

function gradCap(cx, y, w) {
  const k = w / 120;
  return `<g transform="translate(${cx - 60 * k} ${y}) scale(${k})">
    <path d="M22 28 L22 46 Q60 62 98 46 L98 28 Z" fill="${C.ink2}"/>
    <path d="M0 22 L60 0 L120 22 L60 44 Z" fill="${C.ink}"/>
    <path d="M60 22 L104 30 L104 58" stroke="${C.accent}" stroke-width="3.4" fill="none" stroke-linecap="round"/>
    <path d="M100 56 L104 74 L108 56 Z" fill="${C.accent}"/><circle cx="60" cy="22" r="4" fill="${C.accent}"/></g>`;
}

const POSES = { books: poseBooks, think: poseThink, desk: poseDesk, grad: poseGrad, wave: poseWave };

// Place a student. o: {skin, hair, top, collar, glasses, eyes, mouth, pose, cap}
function student(x, y, scale, o) {
  const pose = POSES[o.pose || 'books'](o);
  const behind = o.pose === 'think' ? '' : '';
  return `<g transform="translate(${x} ${y}) scale(${scale})">
    ${hairBack(o)}${torso(o)}${behind}${face(o)}${hairFront(o)}
    ${o.cap ? gradCap(120, 4, 132) : ''}
    ${pose}
  </g>`;
}

/* ---------- props ---------- */

function bookStack(x, y, w, colors = [C.navyL, C.accent, C.ink, C.coral]) {
  const h = w * 0.2;
  return colors.map((c, i) => book(x + (i % 2 ? w * 0.05 : -w * 0.03) , y - (i + 1) * h, w * (1 - i * 0.04), h, c, { rot: i % 2 ? 2 : -1.5, label: i === 1 })).join('');
}

function openBook(cx, cy, w, color = C.accent) {
  const h = w * 0.42;
  return `<g transform="translate(${cx - w / 2} ${cy - h / 2})">
    <path d="M${w / 2} ${h * 0.14} C${w * 0.34} ${-h * 0.02} ${w * 0.12} ${-h * 0.02} 0 ${h * 0.06} L0 ${h} C${w * 0.14} ${h * 0.92} ${w * 0.34} ${h * 0.92} ${w / 2} ${h * 1.06} Z" fill="${color}"/>
    <path d="M${w / 2} ${h * 0.14} C${w * 0.66} ${-h * 0.02} ${w * 0.88} ${-h * 0.02} ${w} ${h * 0.06} L${w} ${h} C${w * 0.86} ${h * 0.92} ${w * 0.66} ${h * 0.92} ${w / 2} ${h * 1.06} Z" fill="${color}"/>
    <path d="M${w / 2} ${h * 0.08} C${w * 0.36} ${-h * 0.08} ${w * 0.14} ${-h * 0.08} ${w * 0.04} 0 L${w * 0.04} ${h * 0.9} C${w * 0.16} ${h * 0.82} ${w * 0.36} ${h * 0.84} ${w / 2} ${h * 0.98} Z" fill="#FFFDF6"/>
    <path d="M${w / 2} ${h * 0.08} C${w * 0.64} ${-h * 0.08} ${w * 0.86} ${-h * 0.08} ${w * 0.96} 0 L${w * 0.96} ${h * 0.9} C${w * 0.84} ${h * 0.82} ${w * 0.64} ${h * 0.84} ${w / 2} ${h * 0.98} Z" fill="#EEF1F8"/>
    <g stroke="#ECD6DA" stroke-width="${w / 120}" stroke-linecap="round">
      ${[0.22, 0.36, 0.5, 0.64].map(t => `<path d="M${w * 0.12} ${h * t} H${w * 0.42}"/><path d="M${w * 0.58} ${h * t} H${w * 0.88}"/>`).join('')}</g>
  </g>`;
}

// Laptop seen from behind on a desk, brand monogram on the lid.
function laptopBack(cx, bottom, w, light = false) {
  const h = w * 0.66;
  return `<g transform="translate(${cx - w / 2} ${bottom - h})">
    <rect x="0" y="0" width="${w}" height="${h}" rx="${w * 0.05}" fill="${light ? '#E3E7EF' : C.ink2}"/>
    <rect x="${w * 0.02}" y="${w * 0.02}" width="${w * 0.96}" height="${h - w * 0.04}" rx="${w * 0.04}" fill="${light ? '#F1F3F8' : C.ink3}" opacity=".5"/>
    ${monogram(w / 2 - h * 0.15, h * 0.35, h * 0.3)}
  </g>`;
}

// Laptop open towards the viewer (screen showing a lesson).
function laptopFront(cx, bottom, w) {
  const h = w * 0.62;
  return `<g transform="translate(${cx - w / 2} ${bottom - h})">
    <rect x="${w * 0.06}" y="0" width="${w * 0.88}" height="${h * 0.86}" rx="${w * 0.03}" fill="${C.ink}"/>
    <rect x="${w * 0.09}" y="${h * 0.05}" width="${w * 0.82}" height="${h * 0.72}" rx="${w * 0.015}" fill="#FFF9F8"/>
    <rect x="${w * 0.09}" y="${h * 0.05}" width="${w * 0.82}" height="${h * 0.12}" fill="${C.accent}"/>
    <circle cx="${w * 0.5}" cy="${h * 0.43}" r="${h * 0.14}" fill="${C.ink}"/><path d="M${w * 0.485} ${h * 0.36} L${w * 0.54} ${h * 0.43} L${w * 0.485} ${h * 0.5} Z" fill="${C.accent}"/>
    <rect x="${w * 0.16}" y="${h * 0.64}" width="${w * 0.68}" height="${h * 0.035}" rx="${h * 0.02}" fill="#EFDFE1"/>
    <rect x="${w * 0.16}" y="${h * 0.64}" width="${w * 0.4}" height="${h * 0.035}" rx="${h * 0.02}" fill="${C.accent}"/>
    <path d="M0 ${h * 0.86} H${w} L${w * 0.96} ${h} H${w * 0.04} Z" fill="#C3C8D4"/>
    <rect x="${w * 0.42}" y="${h * 0.86}" width="${w * 0.16}" height="${h * 0.04}" rx="${h * 0.02}" fill="#9EA5B4"/>
  </g>`;
}

function deskLamp(x, bottom, h, glow = true) {
  const k = h / 200;
  return `<g transform="translate(${x} ${bottom - h}) scale(${k})">
    ${glow ? `<path d="M118 70 L20 210 L210 210 Z" fill="url(#gGlow)" opacity=".7"/>` : ''}
    <ellipse cx="60" cy="196" rx="38" ry="8" fill="${C.ink}"/>
    <path d="M60 192 L44 110 L118 54" stroke="${C.ink}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="44" cy="110" r="8" fill="${C.accent}"/>
    <path d="M96 30 L150 52 L132 92 L78 70 Z" fill="${C.accent}" transform="rotate(8 114 60)"/>
    <ellipse cx="128" cy="86" rx="12" ry="7" fill="#FFF3C4" transform="rotate(28 128 86)"/>
  </g>`;
}

function plant(x, bottom, h) {
  const k = h / 160;
  return `<g transform="translate(${x} ${bottom - h}) scale(${k})">
    <path d="M60 100 C30 70 20 30 34 10 C52 40 62 70 60 100 Z" fill="${C.green}"/>
    <path d="M62 100 C70 60 96 30 116 26 C110 60 90 88 62 100 Z" fill="${C.greenD}"/>
    <path d="M58 104 C40 92 10 88 0 66 C30 64 50 80 58 104 Z" fill="${C.greenD}"/>
    <path d="M62 104 C80 94 110 96 124 80 C100 70 74 82 62 104 Z" fill="${C.green}"/>
    <path d="M30 100 H94 L86 160 H38 Z" fill="${C.white}"/><path d="M30 100 H94 L92 116 H32 Z" fill="${C.accent}"/>
  </g>`;
}

function mug(x, bottom, h) {
  const k = h / 80;
  return `<g transform="translate(${x} ${bottom - h}) scale(${k})">
    <path d="M14 0 C8 -12 22 -18 16 -30 M30 0 C24 -12 38 -18 32 -30" stroke="#C9BFA8" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>
    <path d="M56 22 C76 22 76 54 54 54" stroke="${C.ink}" stroke-width="7" fill="none"/>
    <rect x="0" y="8" width="60" height="72" rx="10" fill="${C.ink}"/><rect x="0" y="34" width="60" height="12" fill="${C.accent}"/>
  </g>`;
}

function sparkle(x, y, r, color = C.accent) {
  return `<path d="M${x} ${y - r} C${x + r * 0.16} ${y - r * 0.16} ${x + r * 0.16} ${y - r * 0.16} ${x + r} ${y} C${x + r * 0.16} ${y + r * 0.16} ${x + r * 0.16} ${y + r * 0.16} ${x} ${y + r} C${x - r * 0.16} ${y + r * 0.16} ${x - r * 0.16} ${y + r * 0.16} ${x - r} ${y} C${x - r * 0.16} ${y - r * 0.16} ${x - r * 0.16} ${y - r * 0.16} ${x} ${y - r} Z" fill="${color}"/>`;
}

// Echo of the emblem: concentric gold arcs used as background ornament.
function rings(cx, cy, r, n = 4, color = C.accent, opacity = 0.35, sw = 3) {
  let out = '';
  for (let i = 0; i < n; i++) {
    const rr = r * (1 - i * 0.2);
    out += `<ellipse cx="${cx + i * r * 0.12}" cy="${cy}" rx="${rr * 0.78}" ry="${rr}" fill="none" stroke="${color}" stroke-width="${sw}" opacity="${opacity * (1 - i * 0.15)}"/>`;
  }
  return out;
}

/* ---------- UI chips used inside illustrations ---------- */

const ICONS = {
  phone: (c) => `<path d="M-6 -9 C-8 -9 -10 -7 -9 -4 C-7 3 -3 7 4 9 C7 10 9 8 9 6 L9 3 L4 1 L2 3 C-1 2 -2 1 -3 -2 L-1 -4 L-3 -9 Z" fill="${c}"/>`,
  globe: (c) => `<g fill="none" stroke="${c}" stroke-width="2.2"><circle r="9"/><ellipse rx="4" ry="9"/><path d="M-9 0 H9 M-7.5 -4.8 H7.5 M-7.5 4.8 H7.5"/></g>`,
  mail: (c) => `<g fill="none" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"><rect x="-10" y="-7" width="20" height="14" rx="2"/><path d="M-9 -6 L0 1 L9 -6"/></g>`,
  whatsapp: (c) => `<path d="M0 -10 A10 10 0 1 1 -8.2 5.7 L-10 10 L-5.4 8.4 A10 10 0 0 0 0 -10 Z" fill="none" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="M-3.6 -4.2 C-4.4 -1 -1 4 3.6 4.6 L5 2.6 L2.6 1.4 L1.6 2.4 C0 1.6 -1.4 0.2 -2 -1.4 L-1 -2.4 L-2.2 -4.8 Z" fill="${c}"/>`,
  play: (c) => `<path d="M-4 -7 L8 0 L-4 7 Z" fill="${c}"/>`,
  check: (c) => `<path d="M-6 0 L-2 4.5 L7 -5" stroke="${c}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,
  star: (c) => `<path d="M0 -9 L2.6 -3 L9 -2.6 L4 1.6 L5.6 8.2 L0 4.6 L-5.6 8.2 L-4 1.6 L-9 -2.6 L-2.6 -3 Z" fill="${c}"/>`,
  live: (c) => `<circle r="4" fill="${c}"/><path d="M-8 -6 A10 10 0 0 0 -8 6 M8 -6 A10 10 0 0 1 8 6" stroke="${c}" stroke-width="2.2" fill="none" stroke-linecap="round"/>`,
  book: (c) => `<path d="M0 -6 C-4 -9 -8 -9 -10 -8 L-10 7 C-8 6 -4 6 0 8 C4 6 8 6 10 7 L10 -8 C8 -9 4 -9 0 -6 Z M0 -6 V8" fill="none" stroke="${c}" stroke-width="2.2" stroke-linejoin="round"/>`,
  users: (c) => `<g fill="${c}"><circle cx="-4" cy="-4" r="4"/><path d="M-12 8 C-12 1 4 1 4 8 Z"/><circle cx="6" cy="-3" r="3.2" opacity=".7"/><path d="M3 2 C8 1 12 3 12 8 L6 8 Z" opacity=".7"/></g>`,
  trophy: (c) => `<g fill="${c}"><path d="M-7 -9 H7 V-2 A7 7 0 0 1 -7 -2 Z"/><rect x="-1.6" y="4" width="3.2" height="4"/><rect x="-6" y="8" width="12" height="3" rx="1"/></g>
    <path d="M-7 -6 H-10 C-10 -1 -8 1 -6 1 M7 -6 H10 C10 -1 8 1 6 1" stroke="${c}" stroke-width="2" fill="none"/>`,
  clock: (c) => `<g fill="none" stroke="${c}" stroke-width="2.2" stroke-linecap="round"><circle r="9"/><path d="M0 -5 V0 L4 3"/></g>`,
};

function icon(name, x, y, size, color) {
  return `<g transform="translate(${x} ${y}) scale(${size / 20})">${ICONS[name](color)}</g>`;
}

// Floating white card: icon disc + title + subtitle. Width auto-ish via w.
function infoCard(x, y, w, h, iconName, title, sub, opts = {}) {
  const r = h * 0.22, d = h * 0.62;
  const dark = opts.dark;
  return `<g filter="url(#fShadow)">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${dark ? C.ink : '#FFFFFF'}"/>
    <circle cx="${x + h * 0.5}" cy="${y + h / 2}" r="${d / 2}" fill="${opts.iconBg || C.accent}"/>
    ${icon(iconName, x + h * 0.5, y + h / 2, d * 0.5, opts.iconColor || C.ink)}
    <text x="${x + h * 0.95}" y="${y + h * 0.47}" font-family="${SANS}" font-weight="800" font-size="${h * 0.26}" fill="${dark ? '#fff' : C.ink}">${title}</text>
    <text x="${x + h * 0.95}" y="${y + h * 0.76}" font-family="${SANS}" font-weight="600" font-size="${h * 0.19}" fill="${dark ? '#EBC3C9' : C.mute}">${sub}</text>
    ${opts.bar ? `<rect x="${x + h * 0.95}" y="${y + h * 0.84}" width="${w - h * 1.25}" height="${h * 0.05}" rx="${h * 0.025}" fill="${dark ? '#6B2635' : '#F3E5E7'}"/>
      <rect x="${x + h * 0.95}" y="${y + h * 0.84}" width="${(w - h * 1.25) * opts.bar}" height="${h * 0.05}" rx="${h * 0.025}" fill="${C.accent}"/>` : ''}
  </g>`;
}

const pillWidth = (h, text) => h * 1.02 + textW(text, h * 0.42, SANS, 700) + h * 0.46;

// Pill with icon + text (contact details); pillWidth() gives its width.
function pill(x, y, h, iconName, text, opts = {}) {
  const fs = h * 0.42, w = opts.w || pillWidth(h, text);
  const bg = opts.bg || C.ink, fg = opts.fg || '#fff';
  return `<g ${opts.shadow === false ? '' : 'filter="url(#fShadowS)"'}>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h / 2}" fill="${bg}" ${opts.stroke ? `stroke="${opts.stroke}" stroke-width="2"` : ''}/>
    <circle cx="${x + h / 2}" cy="${y + h / 2}" r="${h * 0.36}" fill="${opts.iconBg || C.accent}"/>
    ${icon(iconName, x + h / 2, y + h / 2, h * 0.4, opts.iconColor || C.ink)}
    <text x="${x + h * 1.02}" y="${y + h * 0.64}" font-family="${SANS}" font-weight="700" font-size="${fs}" fill="${fg}">${text}</text>
  </g>`;
}

function formulaChip(x, y, text, size = 26, rot = 0, dark = false) {
  const w = textW(text, size, SERIF, 700) + size * 1.2, h = size * 1.7;
  return `<g transform="rotate(${rot} ${x + w / 2} ${y + h / 2})" filter="url(#fShadowS)">
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h * 0.3}" fill="${dark ? C.ink2 : '#fff'}"/>
    <text x="${x + w / 2}" y="${y + h * 0.66}" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-weight="700" font-size="${size}" fill="${dark ? C.accentL : C.ink}">${text}</text></g>`;
}
