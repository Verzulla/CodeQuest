// Общие утилиты: запросы к API, экранирование, markdown, подсветка, звуки, эффекты.

export async function api(path, { method = "GET", body } = {}) {
  let res;
  try {
    res = await fetch(`/api${path}`, {
      method,
      headers: body ? { "Content-Type": "application/json" } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    const err = new Error(navigator.onLine === false ? "Нет подключения к интернету" : "Сервер не отвечает");
    err.status = 0;
    throw err;
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    // Сессия истекла или завершена — показываем экран входа (сами запросы входа не в счёт).
    if (res.status === 401 && !path.startsWith("/auth/")) window.dispatchEvent(new Event("cq:unauthorized"));
    const err = new Error(typeof data.detail === "string" ? data.detail : `Ошибка ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

// SVG-иконка из спрайта в index.html: ic("flame"), ic("heart", "big").
export const ic = (name, cls = "") => `<svg class="i ${cls}" aria-hidden="true"><use href="#ic-${name}"/></svg>`;
const isIconName = (s) => /^[a-z][\w-]*$/.test(s);

// Сова-иллюстрация: owl("happy", "hop") — позы wave, happy, trophy, think, sad, sleep.
export const owl = (pose, anim = "", style = "") =>
  `<img class="owl ${anim}" src="/static/img/owls/owl-${pose}.webp" alt="" draggable="false"${style ? ` style="${style}"` : ""}>`;

// ---------- «Назад» — на предыдущий экран приложения ----------
// Свой стек адресов: переход вперёд добавляет адрес, возврат (браузером или кнопкой) снимает.
const navStack = [location.hash || "#/"];
window.addEventListener("hashchange", () => {
  const h = location.hash || "#/";
  if (navStack.length >= 2 && navStack[navStack.length - 2] === h) navStack.pop();
  else if (navStack[navStack.length - 1] !== h) navStack.push(h);
});
// Вернуться на предыдущий экран; если его нет (открыли по ссылке) — на fallback.
export function goBack(fallback = "#/") {
  if (navStack.length >= 2) history.back();
  else location.hash = fallback;
}
// Ссылки «назад» в разметке: <a data-back href="#/запасной-адрес">
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[data-back]");
  if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
  e.preventDefault();
  goBack(a.getAttribute("href"));
});

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

// ---------- Подсветка Python ----------
const KW = new Set("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case".split(" "));
const BI = new Set("print len range int str float bool list dict set tuple input type isinstance enumerate zip map filter sorted sum min max abs round open any all reversed super object Exception ValueError TypeError KeyError IndexError ZeroDivisionError".split(" "));
const TOKEN = /(#[^\n]*)|([rbfu]{0,2}("""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?))|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)/g;

export function highlight(code) {
  let out = "", last = 0, prevWord = "";
  for (const m of code.matchAll(TOKEN)) {
    out += esc(code.slice(last, m.index));
    last = m.index + m[0].length;
    const t = esc(m[0]);
    if (m[1]) out += `<span class="hl-com">${t}</span>`;
    else if (m[2]) out += `<span class="hl-str">${t}</span>`;
    else if (m[4]) out += `<span class="hl-num">${t}</span>`;
    else if (KW.has(m[0])) out += `<span class="hl-kw">${t}</span>`;
    else if (prevWord === "def" || prevWord === "class") out += `<span class="hl-fn">${t}</span>`;
    else if (BI.has(m[0])) out += `<span class="hl-bi">${t}</span>`;
    else out += t;
    if (m[5]) prevWord = m[0];
  }
  return out + esc(code.slice(last));
}

// ---------- Мини-markdown (заголовки, списки, код, жирный, курсив, `inline`) ----------
function inline(s) {
  // Код внутри `…` прячем на время разметки: звёздочки в коде (x * 2) — не курсив.
  const codes = [];
  const html = esc(s)
    .replace(/`([^`]+)`/g, (_, c) => `\u0000${codes.push(c) - 1}\u0000`)
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>");
  return html.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[i]}</code>`);
}

// Блоки кода: ```python (или без языка) — подсветка Python; ```yaml / ```bash / … — как есть.
// С опцией runnable блоки ```python получают кнопки «Запустить» / «Изменить» (см. bindRunnable).
const PY_LANGS = new Set(["", "python", "py"]);

function codeBlock(lang, code, runnable) {
  // интерактивная схема (viz.js: bindViz) — JSON внутри блока ```viz
  if (lang === "viz") return `<div class="viz" data-viz="${esc(code)}"></div>`;
  const body = PY_LANGS.has(lang) ? highlight(code) : esc(code);
  const pre = `<pre${lang && !PY_LANGS.has(lang) ? ` data-lang="${esc(lang)}"` : ""}><code>${body}</code></pre>`;
  if (!(runnable && lang === "python")) return pre;
  return `<div class="runnable" data-code="${esc(code)}">
    <div class="rb-bar"><span class="kind">Python</span><span class="spacer"></span>
      <button class="act" data-act="edit">${ic("pen")}<span>Изменить</span></button>
      <button class="act run" data-act="run">${ic("play")}<span>Запустить</span></button></div>
    <div class="rb-code">${pre}</div><div class="rb-out"></div></div>`;
}

// Строка таблицы «| a | b |» → ячейки; `|` внутри `кода` не делит ячейку.
function tableRow(line) {
  const cells = [];
  let cur = "", code = false;
  for (const ch of line.trim().replace(/^\||\|$/g, "")) {
    if (ch === "`") code = !code;
    if (ch === "|" && !code) { cells.push(cur.trim()); cur = ""; } else cur += ch;
  }
  cells.push(cur.trim());
  return cells;
}

export function md(src, { runnable = false } = {}) {
  const lines = String(src || "").replace(/\r\n/g, "\n").split("\n");
  let html = "", para = [];
  // Стек открытых списков: вложенность определяется отступом строки.
  const stack = [];
  const flushPara = () => { if (para.length) html += `<p>${inline(para.join(" "))}</p>`; para = []; };
  const closeTop = () => { html += `</li></${stack.pop().tag}>`; };
  const flushList = () => { while (stack.length) closeTop(); };
  const listItem = (indent, tag, text) => {
    while (stack.length && indent < stack.at(-1).indent) closeTop();
    const top = stack.at(-1);
    if (top && indent === top.indent && tag !== top.tag) closeTop();
    const cur = stack.at(-1);
    if (cur && indent === cur.indent) html += `</li><li>${inline(text)}`;
    else { stack.push({ indent, tag }); html += `<${tag}><li>${inline(text)}`; }
  };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith("```")) {
      flushPara(); flushList();
      const lang = line.slice(3).trim().toLowerCase();
      const buf = [];
      while (++i < lines.length && !lines[i].startsWith("```")) buf.push(lines[i]);
      html += codeBlock(lang, buf.join("\n"), runnable);
      continue;
    }
    // таблица: строка «| … |», за ней разделитель «|---|---|»
    if (line.trim().startsWith("|") && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i + 1] || "") && (lines[i + 1] || "").includes("-")) {
      flushPara(); flushList();
      const head = tableRow(line);
      const rows = [];
      i++;
      while (i + 1 < lines.length && lines[i + 1].trim().startsWith("|")) rows.push(tableRow(lines[++i]));
      html += `<div class="md-table"><table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead>`
        + `<tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
      continue;
    }
    const h = line.match(/^(#{1,3})\s+(.*)/);
    const ul = line.match(/^(\s*)[-*]\s+(.*)/);
    const ol = line.match(/^(\s*)\d+[.)]\s+(.*)/);
    if (h) { flushPara(); flushList(); html += `<h${h[1].length + 1}>${inline(h[2])}</h${h[1].length + 1}>`; }
    else if (ul || ol) {
      flushPara();
      const m = ul || ol;
      listItem(m[1].length, ul ? "ul" : "ol", m[2]);
    } else if (!line.trim()) { flushPara(); flushList(); }
    else { flushList(); para.push(line); }
  }
  flushPara(); flushList();
  return html;
}

// ---------- Звуки (WebAudio, без файлов) ----------
let audio;
export const soundOn = () => localStorage.getItem("cq-sound") !== "off";
export function sound(kind) {
  if (!soundOn()) return;
  try {
    audio ??= new AudioContext();
    if (kind === "win") return winSound();
    const notes = { good: [659, 880], bad: [220, 185], done: [523, 659, 784, 1047], click: [880] }[kind] || [440];
    notes.forEach((f, i) => {
      const o = audio.createOscillator(), g = audio.createGain();
      o.type = kind === "bad" ? "sawtooth" : "sine";
      o.frequency.value = f;
      const t = audio.currentTime + i * 0.09;
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(kind === "bad" ? 0.06 : 0.15, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.22);
      o.connect(g).connect(audio.destination);
      o.start(t); o.stop(t + 0.25);
    });
  } catch { /* звук необязателен */ }
}

// Победный звук за верный ответ — яркий «дзынь-дзынь», как в Duolingo: две быстрые
// высокие ноты вверх (до → соль), звонкий колокольчатый тембр. Колокольчик — FM-синтез:
// синусоида, частоту которой «дёргает» вторая синусоида (обертоны металла), плюс
// тихий голос на октаву выше для блеска и короткое эхо для объёма. Всего ~0.45 с.
let hall = null;
function hallReverb() {
  if (hall) return hall;
  const len = audio.sampleRate * 0.5;
  const ir = audio.createBuffer(2, len, audio.sampleRate);
  for (let ch = 0; ch < 2; ch++) {
    const d = ir.getChannelData(ch);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len) ** 4;
  }
  const conv = audio.createConvolver();
  conv.buffer = ir;
  const wet = audio.createGain();
  wet.gain.value = 0.2;
  conv.connect(wet).connect(audio.destination);
  hall = conv;
  return hall;
}

function chime(freq, t, dur, vol) {
  const out = audio.createGain();
  out.gain.setValueAtTime(0.0001, t);
  out.gain.exponentialRampToValueAtTime(vol, t + 0.008);         // мгновенный удар
  out.gain.exponentialRampToValueAtTime(0.0001, t + dur);        // звенящее затухание
  out.connect(audio.destination);
  out.connect(hallReverb());

  const carrier = audio.createOscillator();
  carrier.frequency.value = freq;
  const mod = audio.createOscillator(), modGain = audio.createGain();
  mod.frequency.value = freq * 3.5;
  modGain.gain.setValueAtTime(freq * 1.2, t);                    // яркость удара…
  modGain.gain.exponentialRampToValueAtTime(freq * 0.05, t + dur * 0.6);   // …быстро смягчается
  mod.connect(modGain).connect(carrier.frequency);
  carrier.connect(out);

  const shine = audio.createOscillator(), shineGain = audio.createGain();
  shine.frequency.value = freq * 2;
  shineGain.gain.value = 0.25;
  shine.connect(shineGain).connect(out);

  for (const o of [carrier, mod, shine]) { o.start(t); o.stop(t + dur + 0.02); }
}

function winSound() {
  const t = audio.currentTime + 0.01;
  chime(1046.5, t, 0.22, 0.16);          // «дзынь» (до)
  chime(1568, t + 0.1, 0.4, 0.18);       // «дзынь!» (соль) — выше и звонче
}

// ---------- Тосты и модалки ----------
export function toast(icon, title, sub = "") {
  const box = document.getElementById("toasts");
  const t = document.createElement("div");
  t.className = "toast";
  t.innerHTML = `<div class="ti">${isIconName(icon) ? ic(icon) : esc(icon)}</div><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</div>`;
  box.append(t);
  setTimeout(() => t.remove(), 4000);
}

export function modal(html) {
  const ov = document.getElementById("overlay");
  ov.innerHTML = `<div class="modal">${html}</div>`;
  const close = () => { ov.innerHTML = ""; };
  ov.onclick = (e) => { if (e.target === ov) close(); };
  return { root: ov.firstElementChild, close };
}

// ---------- Конфетти ----------
export function confetti() {
  const c = document.createElement("canvas");
  c.className = "confetti";
  c.width = innerWidth; c.height = innerHeight;
  document.body.append(c);
  const ctx = c.getContext("2d");
  const colors = ["#58cc02", "#1cb0f6", "#ffc800", "#ff4b4b", "#ce82ff", "#ff9600"];
  const parts = Array.from({ length: 160 }, () => ({
    x: innerWidth / 2 + (Math.random() - 0.5) * 200, y: innerHeight / 3,
    vx: (Math.random() - 0.5) * 16, vy: -Math.random() * 16 - 4,
    r: Math.random() * 6 + 4, a: Math.random() * 6, va: (Math.random() - 0.5) * 0.3,
    c: colors[Math.floor(Math.random() * colors.length)],
  }));
  let frame = 0;
  (function tick() {
    ctx.clearRect(0, 0, c.width, c.height);
    for (const p of parts) {
      p.vy += 0.4; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.a += p.va;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
      ctx.fillStyle = p.c; ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2); ctx.restore();
    }
    if (++frame < 180 && c.isConnected) requestAnimationFrame(tick); else c.remove();
  })();
}

// Маленький взрыв конфетти из элемента (например, из кнопки «Проверить»).
export function burst(el) {
  if (!el || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const rect = el.getBoundingClientRect();
  const c = document.createElement("canvas");
  c.className = "confetti";
  c.width = innerWidth; c.height = innerHeight;
  document.body.append(c);
  const ctx = c.getContext("2d");
  const colors = ["#58cc02", "#1cb0f6", "#ffc800", "#ff4b4b", "#ce82ff", "#ff9600"];
  const cx = rect.left + rect.width / 2, cy = rect.top + rect.height / 2;
  const FRAMES = 120;
  const parts = Array.from({ length: 90 }, () => {
    const angle = -Math.PI / 2 + (Math.random() - 0.5) * 2.4;   // веер вверх и в стороны
    const speed = Math.random() * 10 + 9;
    return {
      x: cx + (Math.random() - 0.5) * rect.width * 0.8, y: cy,
      vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
      w: Math.random() * 8 + 8, h: Math.random() * 4 + 5,
      a: Math.random() * 6, va: (Math.random() - 0.5) * 0.35,
      flip: Math.random() * 6, vflip: Math.random() * 0.2 + 0.1,   // «кувыркание» бумажки
      c: colors[Math.floor(Math.random() * colors.length)],
    };
  });
  let frame = 0;
  (function tick() {
    ctx.clearRect(0, 0, c.width, c.height);
    ctx.globalAlpha = Math.min(1, (FRAMES - frame) / 25);        // плавно гаснет в конце
    for (const p of parts) {
      p.vy += 0.32; p.vx *= 0.985; p.vy *= 0.99;
      p.x += p.vx; p.y += p.vy; p.a += p.va; p.flip += p.vflip;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.scale(1, Math.cos(p.flip));
      ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); ctx.restore();
    }
    if (++frame < FRAMES && c.isConnected) requestAnimationFrame(tick); else c.remove();
  })();
}

export function fmtTime(sec) {
  const m = Math.floor(sec / 60), s = sec % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function plural(n, one, few, many) {
  const m10 = n % 10, m100 = n % 100;
  if (m10 === 1 && m100 !== 11) return one;
  if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few;
  return many;
}
