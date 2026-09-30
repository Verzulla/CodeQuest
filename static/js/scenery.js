// Фон дорожки (зигзаг): пейзаж из приглушённых силуэтов — лес, домики, скворечники, горы, река, пруд, мельница.
// Сцена собирается из групп по «зерну» модуля: у каждого модуля своя, при перерисовке — та же самая.
// Предметы стоят на холмиках и ставятся на ту сторону, где нет кружков уроков.

const DEFS = `
<linearGradient id="sc-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd65a"/><stop offset=".45" stop-color="#4fae3c" stop-opacity=".6"/><stop offset="1" stop-color="#4fae3c" stop-opacity="0"/></linearGradient>
<linearGradient id="sc-ground2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#45b58a"/><stop offset="1" stop-color="#45b58a" stop-opacity="0"/></linearGradient>
<linearGradient id="sc-far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8f7a"/><stop offset="1" stop-color="#3f8f7a" stop-opacity="0"/></linearGradient>
<linearGradient id="sc-mount" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a39ce8"/><stop offset="1" stop-color="#6e67b8" stop-opacity=".15"/></linearGradient>
<linearGradient id="sc-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6cc4ff"/><stop offset="1" stop-color="#3f8fe0"/></linearGradient>
<symbol id="sc-pine" viewBox="0 0 40 70"><rect x="17" y="54" width="6" height="16" rx="2" fill="#9a7250"/><path d="M20 0 34 24h-7l11 18h-9l10 16H1l10-16H2l11-18H6Z" fill="#3fae7a"/><path d="M20 0 34 24h-7l11 18h-9l10 16H20Z" fill="#35966a"/></symbol>
<symbol id="sc-tree" viewBox="0 0 60 80"><rect x="26" y="44" width="8" height="36" rx="3" fill="#9a7250"/><circle cx="30" cy="26" r="22" fill="#5fbf55"/><circle cx="14" cy="38" r="13" fill="#52ad4a"/><circle cx="46" cy="38" r="13" fill="#52ad4a"/><circle cx="24" cy="18" r="8" fill="#7dd46d"/></symbol>
<symbol id="sc-birch" viewBox="0 0 40 80"><rect x="17" y="30" width="6" height="50" rx="2" fill="#eeeade"/><path d="M17 44h3M20 56h3M17 66h3" stroke="#555" stroke-width="2"/><ellipse cx="20" cy="26" rx="16" ry="24" fill="#9bd65a"/><ellipse cx="15" cy="20" rx="6" ry="9" fill="#b6e47a"/></symbol>
<symbol id="sc-birdtree" viewBox="0 0 70 96"><rect x="30" y="48" width="9" height="48" rx="3" fill="#9a7250"/><circle cx="34" cy="28" r="24" fill="#5fbf55"/><circle cx="16" cy="42" r="14" fill="#52ad4a"/><circle cx="52" cy="42" r="14" fill="#52ad4a"/><circle cx="27" cy="19" r="9" fill="#7dd46d"/><rect x="42" y="60" width="16" height="15" rx="2" fill="#f0c98a"/><path d="M39 62 50 52l11 10Z" fill="#e0714f"/><circle cx="50" cy="67" r="3" fill="#4a3322"/><rect x="48" y="75" width="4" height="7" fill="#9a7250"/></symbol>
<symbol id="sc-house" viewBox="0 0 80 72"><rect x="54" y="6" width="9" height="18" fill="#b8563d"/><rect x="52" y="4" width="13" height="4" rx="1" fill="#c96a4f"/><rect x="12" y="32" width="56" height="40" fill="#f2dcb4"/><path d="M2 36 40 6l38 30Z" fill="#e0714f"/><path d="M2 36 40 6l38 30h-6L40 12 8 36Z" fill="#c95a3c"/><rect x="34" y="48" width="13" height="24" rx="6" fill="#9b6a45"/><circle cx="44" cy="61" r="1.4" fill="#f2dcb4"/><rect x="17" y="44" width="12" height="11" rx="1.5" fill="#ffd76a"/><path d="M23 44v11M17 49.5h12" stroke="#c9975a" stroke-width="1.6"/><rect x="52" y="44" width="12" height="11" rx="1.5" fill="#ffd76a"/><path d="M58 44v11M52 49.5h12" stroke="#c9975a" stroke-width="1.6"/><circle cx="40" cy="26" r="4" fill="#ffd76a"/></symbol>
<symbol id="sc-house2" viewBox="0 0 64 60"><rect x="8" y="26" width="48" height="34" fill="#d6e6f5"/><path d="M0 30 32 4l32 26Z" fill="#5a8fd8"/><path d="M0 30 32 4l32 26h-5L32 9 5 30Z" fill="#4a78c0"/><rect x="26" y="40" width="12" height="20" rx="1" fill="#7a5a44"/><rect x="13" y="36" width="9" height="9" fill="#ffd76a"/><rect x="42" y="36" width="9" height="9" fill="#ffd76a"/><rect x="22" y="58" width="20" height="2" fill="#b89a7a"/></symbol>
<symbol id="sc-house3" viewBox="0 0 60 70"><rect x="10" y="30" width="40" height="40" fill="#f5e3c3"/><path d="M4 34 30 2l26 32Z" fill="#7a9a4a"/><path d="M4 34 30 2l26 32h-5L30 8 9 34Z" fill="#65853c"/><rect x="24" y="48" width="12" height="22" rx="6" fill="#8a5a3a"/><circle cx="30" cy="22" r="4.5" fill="#ffd76a"/><rect x="14" y="38" width="8" height="8" fill="#ffd76a"/><rect x="38" y="38" width="8" height="8" fill="#ffd76a"/></symbol>
<symbol id="sc-windmill" viewBox="0 0 70 100"><path d="M26 40h18l6 60H20Z" fill="#e8d2b0"/><path d="M24 42 35 26l11 16Z" fill="#c95a3c"/><rect x="31" y="80" width="8" height="20" rx="4" fill="#8a5a3a"/><g transform="rotate(20 35 34)" fill="#f4eee2"><rect x="33" y="0" width="4" height="34"/><rect x="33" y="34" width="4" height="34"/><rect x="1" y="32" width="34" height="4"/><rect x="35" y="32" width="34" height="4"/></g><circle cx="35" cy="34" r="4" fill="#9a7250"/></symbol>
<symbol id="sc-fence" viewBox="0 0 90 26"><path d="M3 8l4-6 4 6v18H3Z M23 8l4-6 4 6v18h-8Z M43 8l4-6 4 6v18h-8Z M63 8l4-6 4 6v18h-8Z M83 8l4-6 3 6v18h-7Z" fill="#dcc49c"/><rect y="11" width="90" height="3" fill="#c9ae84"/><rect y="19" width="90" height="3" fill="#c9ae84"/></symbol>
<symbol id="sc-bush" viewBox="0 0 50 24"><path d="M0 24a12 12 0 0 1 13-15 14 14 0 0 1 24 0 12 12 0 0 1 13 15Z" fill="#4fb86a"/><circle cx="14" cy="14" r="2" fill="#ff8fb1"/><circle cx="30" cy="10" r="2" fill="#ffd54a"/><circle cx="38" cy="16" r="2" fill="#ff8fb1"/></symbol>
<symbol id="sc-flowers" viewBox="0 0 40 10"><circle cx="4" cy="6" r="2.2" fill="#ff8fb1"/><circle cx="14" cy="4" r="2.2" fill="#ffd54a"/><circle cx="24" cy="7" r="2.2" fill="#fff"/><circle cx="34" cy="5" r="2.2" fill="#ff8fb1"/></symbol>
<symbol id="sc-mush" viewBox="0 0 20 20"><rect x="8" y="10" width="4" height="10" rx="2" fill="#f2e6d0"/><path d="M1 11a9 9 0 0 1 18 0Z" fill="#e0564f"/><circle cx="7" cy="7" r="1.5" fill="#fff"/><circle cx="13" cy="6" r="1.3" fill="#fff"/></symbol>
<symbol id="sc-rocks" viewBox="0 0 50 24"><path d="M2 24 8 10l10-4 8 8 2 10Z" fill="#9aa3b2"/><path d="M22 24l6-12 10-3 9 8 3 7Z" fill="#b6bdc9"/><path d="M8 10l10-4 3 6-9 2Z" fill="#c9cfd8"/></symbol>
<symbol id="sc-reeds" viewBox="0 0 30 30"><path d="M6 30C6 18 4 10 3 4M13 30c0-12 1-18 3-26M21 30c0-10-2-16-4-22" stroke="#6fae5a" stroke-width="2" fill="none"/><rect x="1.5" y="2" width="3" height="9" rx="1.5" fill="#8a5a3a"/><rect x="14.5" y="1" width="3" height="9" rx="1.5" fill="#8a5a3a"/></symbol>
<symbol id="sc-duck" viewBox="0 0 24 14"><path d="M2 8c0 4 18 5 20 0-2-2-6-1-8-2 1-4-4-6-6-2-1 2 0 3-2 3Z" fill="#f4eee2"/><path d="M5 4 1 5l4 1Z" fill="#ffb03a"/></symbol>
<symbol id="sc-cloud" viewBox="0 0 100 44"><path d="M20 44a18 18 0 0 1 2-36 24 24 0 0 1 44-2 17 17 0 0 1 16 20 12 12 0 0 1-2 18Z" fill="#e8f0ff"/></symbol>
<symbol id="sc-sun" viewBox="0 0 60 60"><circle cx="30" cy="30" r="13" fill="#ffd54a"/><path d="M30 3v8M30 49v8M3 30h8M49 30h8M11 11l5.5 5.5M43.5 43.5 49 49M11 49l5.5-5.5M43.5 16.5 49 11" stroke="#ffd54a" stroke-width="4" stroke-linecap="round"/></symbol>
<symbol id="sc-moon" viewBox="0 0 40 40"><path d="M26 4a16 16 0 1 0 10 26A14 14 0 0 1 26 4Z" fill="#f4eecb"/></symbol>
<symbol id="sc-bird" viewBox="0 0 30 12"><path d="M0 8Q7 0 15 8Q23 0 30 8" fill="none" stroke="#e8f0ff" stroke-width="2.5" stroke-linecap="round"/></symbol>
<symbol id="sc-bridge" viewBox="0 0 80 30"><path d="M0 26Q40 0 80 26" fill="none" stroke="#b58a5e" stroke-width="6"/><path d="M8 20v10M24 12v14M40 9v14M56 12v14M72 20v10" stroke="#9a7250" stroke-width="3"/></symbol>`;

let defsReady = false;
function ensureDefs() {
  if (defsReady) return;
  defsReady = true;
  document.body.insertAdjacentHTML("afterbegin", `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${DEFS}</defs></svg>`);
}

// Детерминированный генератор: одна и та же сцена для одного и того же модуля.
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Предмет: центр cx, стоит на линии bottom; flip — зеркально.
const put = (id, cx, bottom, w, h, flip = false) => flip
  ? `<use href="#sc-${id}" x="${-cx - w / 2}" y="${bottom - h}" width="${w}" height="${h}" transform="scale(-1 1)"/>`
  : `<use href="#sc-${id}" x="${cx - w / 2}" y="${bottom - h}" width="${w}" height="${h}"/>`;
// Холмик под группой: склоны плавно уходят в прозрачность.
const mound = (cx, top, w) => `<path d="M${cx - w / 2 - 30} ${top + 70} C${cx - w / 2 + 10} ${top + 20}, ${cx - w / 4} ${top - 4}, ${cx} ${top - 4} S${cx + w / 2 - 10} ${top + 20}, ${cx + w / 2 + 30} ${top + 70} Z" fill="url(#sc-ground)"/>`;

// Группы предметов на холмике. dir: 1 — группа у левого края (растёт вправо), -1 — у правого.
const GROUPS = {
  forest: (x, y, s, r, dir) => mound(x, y, 150 * s) + put("pine", x - 34 * s * dir, y, 30 * s, 52 * s) + put("pine", x - 6 * s * dir, y - 4 * s, 40 * s, 70 * s)
    + put(r() < .5 ? "tree" : "birch", x + 30 * s * dir, y, 40 * s, 56 * s) + (r() < .6 ? put("mush", x + 12 * s * dir, y + 2, 12 * s, 12 * s) : ""),
  grove: (x, y, s, r, dir) => mound(x, y, 140 * s) + put("tree", x - 24 * s * dir, y, 50 * s, 66 * s, r() < .5) + put("birch", x + 16 * s * dir, y - 2, 30 * s, 60 * s)
    + put("bush", x + 44 * s * dir, y + 3, 34 * s, 17 * s),
  birdhouse: (x, y, s, r, dir) => mound(x, y, 130 * s) + put("birdtree", x, y, 60 * s, 82 * s, dir < 0) + put("flowers", x + 40 * s * dir, y + 4, 30 * s, 8 * s)
    + (r() < .5 ? put("mush", x - 34 * s * dir, y + 3, 12 * s, 12 * s) : ""),
  house: (x, y, s, r, dir) => mound(x, y, 150 * s) + put(r() < .6 ? "house" : "house3", x, y, 70 * s, 62 * s, r() < .5)
    + put("fence", x + 50 * s * dir, y + 4, 36 * s, 11 * s) + (r() < .6 ? put("tree", x - 48 * s * dir, y, 32 * s, 44 * s) : put("bush", x - 44 * s * dir, y + 3, 32 * s, 16 * s)),
  cottage: (x, y, s, r, dir) => mound(x, y, 130 * s) + put("house2", x, y, 58 * s, 54 * s, dir < 0) + put("flowers", x - 38 * s * dir, y + 4, 30 * s, 8 * s)
    + put("pine", x + 40 * s * dir, y, 26 * s, 44 * s),
  windmill: (x, y, s, r, dir) => mound(x, y, 130 * s) + put("windmill", x, y, 60 * s, 86 * s) + put("bush", x + 40 * s * dir, y + 3, 30 * s, 15 * s)
    + put("flowers", x - 36 * s * dir, y + 4, 28 * s, 8 * s),
  pond: (x, y, s, r, dir) => mound(x, y, 150 * s) + `<ellipse cx="${x + 4 * dir}" cy="${y + 14 * s}" rx="${46 * s}" ry="${11 * s}" fill="url(#sc-water)"/>`
    + put("reeds", x - 40 * s * dir, y + 12 * s, 22 * s, 24 * s) + put("duck", x + 10 * dir, y + 12 * s, 18 * s, 10 * s, dir < 0) + put("rocks", x + 42 * s * dir, y + 8, 30 * s, 14 * s),
  rocks: (x, y, s, r, dir) => mound(x, y, 120 * s) + put("rocks", x - 8 * dir, y + 2, 46 * s, 22 * s) + put("pine", x + 32 * s * dir, y, 28 * s, 48 * s)
    + put("bush", x - 40 * s * dir, y + 3, 30 * s, 15 * s),
};
// Наборы-«настроения»: основа сцены + немного чужих групп для разнообразия.
const MOODS = [
  { groups: ["forest", "grove", "birdhouse", "rocks"], extra: ["house", "pond"] },                 // лесная опушка
  { groups: ["house", "cottage", "birdhouse", "windmill"], extra: ["grove", "pond"] },              // деревня
  { groups: ["forest", "rocks", "pond"], extra: ["cottage"], mountains: true, river: true },        // горы и река
  { groups: ["forest", "house", "birdhouse", "windmill", "pond"], extra: ["grove"], sun: true, river: true }, // пейзаж
  { groups: ["grove", "pond", "windmill", "birdhouse"], extra: ["cottage", "rocks"], sun: true },   // луг у пруда
];

// Рисует сцену в svg.scenery внутри box (.nodes). pts — центры кружков, locked — модуль ещё закрыт (ночь).
export function drawScenery(box, seed, pts, locked) {
  ensureDefs();
  const svg = box.querySelector(".scenery");
  if (!svg) return;
  // Пейзаж занимает всю область контента: от бокового меню до правой колонки (на телефоне — весь экран),
  // а не только колонку дорожки. Края на десктопе растворяются маской в CSS.
  const br = box.getBoundingClientRect();
  const desk = window.innerWidth > 700;
  const side = document.querySelector(".sidebar"), rail = document.getElementById("rail");
  const L = desk && side ? side.getBoundingClientRect().right : 0;
  const R = desk && rail && rail.offsetParent ? rail.getBoundingClientRect().left : document.documentElement.clientWidth;
  const ox = L - br.left;
  const W = Math.max(1, R - L), H = box.clientHeight;
  svg.style.left = `${ox}px`;
  pts = pts.map(([x, y]) => [x - ox, y]);
  svg.setAttribute("width", W);
  svg.setAttribute("height", H);
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  if (!pts.length) { svg.innerHTML = ""; return; }
  const r = rng(seed * 2654435761 + 12345);
  const pick = (arr) => arr[Math.floor(r() * arr.length)];
  const mood = MOODS[seed % MOODS.length];
  const wide = W > 520;
  const s0 = wide ? 1.15 : 0.92;
  const mid = W / 2;
  let out = "";

  // Небо и дальний план
  if (mood.mountains) {
    const p = (f) => (W * f).toFixed(0);
    out += `<path d="M-60 ${160} L${p(.16)} 64 ${p(.28)} 108 ${p(.47)} 30 ${p(.66)} 118 ${p(.78)} 84 ${W + 60} ${160} V210 H-60Z" fill="url(#sc-mount)"/>`
      + `<path d="M${p(.47)} 30 ${+p(.47) + 16} 52 ${+p(.47) + 6} 48 ${+p(.47) - 2} 58 ${+p(.47) - 10} 50 ${+p(.47) - 18} 56Z" fill="#f4f6ff"/>`;
  }
  const farY = 110 + r() * 40;
  out += `<path d="M-60 ${farY + 34} C${W * .2} ${farY - 5} ${W * .35} ${farY + 5} ${W * .5} ${farY + 22} S${W * .8} ${farY + 8} ${W + 60} ${farY - 12} V${farY + 110} H-60Z" fill="url(#sc-far)" opacity=".7"/>`;
  const skySide = r() < .5 ? 1 : -1;
  const skyX = skySide > 0 ? W - 40 - r() * 30 : 40 + r() * 30;
  if (locked) out += put("moon", skyX, 70, 30, 30);
  else if (mood.sun || r() < .3) out += put("sun", skyX, 84, 44, 44);
  else out += put("cloud", skyX, 70, 64 + r() * 20, 30);
  if (r() < .7) out += put("cloud", mid - skySide * (60 + r() * 60), 50 + r() * 20, 50 + r() * 20, 24);
  if (r() < .6) { const bx = mid + skySide * (40 + r() * 40); out += put("bird", bx, 96, 20, 8) + put("bird", bx + 24, 110, 14, 6); }

  // Река: широкая лента через всю высоту по одной стороне
  if (mood.river) {
    const side = r() < .5 ? -1 : 1;
    const ex = (f) => (side < 0 ? W * f : W * (1 - f)).toFixed(0);
    const d = `M${ex(-.05)} ${H * .3} C${ex(.3)} ${H * .28}, ${ex(.35)} ${H * .45}, ${ex(.18)} ${H * .55} S${ex(.1)} ${H * .8}, ${ex(.45)} ${H * .88} S${ex(.95)} ${H * .95}, ${ex(1.1)} ${H + 20}`;
    out += `<path d="${d}" fill="none" stroke="url(#sc-water)" stroke-width="${wide ? 34 : 26}" stroke-linecap="round" opacity=".85"/>`
      + `<path d="${d}" fill="none" stroke="#bfe6ff" stroke-width="2" stroke-dasharray="10 18" opacity=".55"/>`;
  }

  // Группы на холмиках: по полосам сверху вниз, на сторону без кружков
  const pool = [...mood.groups, ...mood.extra];
  let last = "";
  const nodeXat = (y) => pts.reduce((best, p) => (Math.abs(p[1] - y) < Math.abs(best[1] - y) ? p : best))[0];
  for (let y = 190 + r() * 40; y < H - 30; y += 150 + r() * 60) {
    const nx = nodeXat(y);
    const left = nx > mid + 8 ? true : nx < mid - 8 ? false : r() < .5;
    const dir = left ? 1 : -1;
    const edge = wide ? 70 + r() * Math.max(0, (W - 520) / 3) : 46 + r() * 14;
    const x = left ? edge : W - edge;
    let g = r() < .8 ? pick(mood.groups) : pick(mood.extra);
    if (g === last) g = pick(pool.filter((k) => k !== last));
    last = g;
    out += GROUPS[g](x, y, s0 * (0.9 + r() * 0.25), r, dir);
  }
  // Земля внизу
  out += `<path d="M-60 ${H - 46} C${W * .25} ${H - 80} ${W * .45} ${H - 64} ${W * .6} ${H - 52} S${W * .9} ${H - 62} ${W + 60} ${H - 84} V${H + 30} H-60Z" fill="url(#sc-ground2)"/>`;
  svg.innerHTML = out;
}
