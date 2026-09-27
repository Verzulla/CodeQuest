// Общие утилиты: запросы к API, экранирование, markdown, подсветка, звуки, эффекты.

export async function api(path, { method = "GET", body } = {}) {
  const res = await fetch(`/api${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(typeof data.detail === "string" ? data.detail : `Ошибка ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

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
  const body = PY_LANGS.has(lang) ? highlight(code) : esc(code);
  const pre = `<pre${lang && !PY_LANGS.has(lang) ? ` data-lang="${esc(lang)}"` : ""}><code>${body}</code></pre>`;
  if (!(runnable && lang === "python")) return pre;
  return `<div class="runnable" data-code="${esc(code)}">
    <div class="rb-bar"><span>🐍 Пример</span><span class="spacer"></span>
      <button class="btn ghost small" data-act="edit">✏️ Изменить</button>
      <button class="btn blue small" data-act="run">▶ Запустить</button></div>
    <div class="rb-code">${pre}</div><div class="rb-out"></div></div>`;
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

// ---------- Тосты и модалки ----------
export function toast(icon, title, sub = "") {
  const box = document.getElementById("toasts");
  const t = document.createElement("div");
  t.className = "toast";
  t.innerHTML = `<div class="ti">${esc(icon)}</div><div><b>${esc(title)}</b>${sub ? `<small>${esc(sub)}</small>` : ""}</div>`;
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
