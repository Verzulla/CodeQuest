// «Учиться»: каталог тем (сгруппированный) → страница темы с дорожкой уроков.
import { api, esc, sound, plural } from "../util.js";
import { pills } from "../store.js";

const OFFSETS = [0, 44, 70, 44, 0, -44, -70, -44]; // зигзаг дорожки
const NO_GROUP = "Другие темы";

const emptyContent = `<div class="empty"><div class="big">📭</div><h2>Пока нет ни одной темы</h2>
  <p class="muted">Создай тему в разделе «Контент» или попроси Claude сгенерировать пакет заданий.</p>
  <a class="btn" href="#/admin">Открыть контент</a></div>`;

// ---------- Каталог тем ----------
export async function renderCatalog(view) {
  const [topics, cont] = await Promise.all([api("/path"), api("/continue")]);
  if (!topics.length) { view.innerHTML = emptyContent; return; }

  // Группы — в порядке первой темы каждой группы; темы без группы — в конце.
  const groups = new Map();
  for (const t of topics) {
    const g = t.group || NO_GROUP;
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(t);
  }
  if (groups.has(NO_GROUP)) { const rest = groups.get(NO_GROUP); groups.delete(NO_GROUP); groups.set(NO_GROUP, rest); }

  view.innerHTML = `
    <div class="topbar path-top">${pills()}</div>
    ${cont ? continueBanner(cont) : ""}
    ${[...groups].map(([name, list]) => `
      <section class="topic-group">
        <h2 class="group-title">${esc(name)} <small class="muted">${list.filter((t) => t.trophy).length} / ${list.length} пройдено</small></h2>
        <div class="topic-grid">${list.map(topicCard).join("")}</div>
      </section>`).join("")}`;
}

function continueBanner(c) {
  const pct = c.lesson.exercises ? Math.round((100 * c.lesson.solved) / c.lesson.exercises) : 0;
  return `<a class="continue" href="#/lesson/${c.lesson.id}" style="--tc:${esc(c.topic.color)}">
    <div class="c-icon">${esc(c.topic.icon)}</div>
    <div class="c-body">
      <small>${c.started ? "Продолжить" : "Начни отсюда"}</small>
      <b>${esc(c.topic.title)} → ${esc(c.lesson.title)}</b>
      <div class="c-meta"><div class="bar"><i style="width:${pct}%"></i></div>
        <span>${c.lesson.solved}/${c.lesson.exercises} ${plural(c.lesson.exercises, "задание", "задания", "заданий")}</span></div>
    </div>
    <span class="btn c-btn">${c.started && c.lesson.solved ? "Продолжить" : "Начать"} ▶</span>
  </a>`;
}

function topicCard(t) {
  const pct = t.total ? Math.round((100 * t.completed) / t.total) : 0;
  const action = t.trophy ? "Повторить" : t.completed ? "Продолжить" : "Начать";
  return `<a class="topic-card ${t.trophy ? "finished" : ""}" href="#/topic/${t.id}" style="--tc:${esc(t.color)}">
    <div class="tc-head"><span class="tc-icon">${esc(t.icon)}</span>${t.trophy ? `<span class="tc-cup" title="Тема пройдена">🏆</span>` : ""}</div>
    <h3>${esc(t.title)}</h3>
    <p>${esc(t.description)}</p>
    <div class="tc-foot">
      <div class="bar"><i style="width:${pct}%"></i></div>
      <small>${t.completed} / ${t.total} ${plural(t.total, "урок", "урока", "уроков")} · ${t.modules.length} ${plural(t.modules.length, "модуль", "модуля", "модулей")}</small>
      <span class="tc-action">${action} →</span>
    </div>
  </a>`;
}

// ---------- Страница темы ----------
export async function renderTopic(view, topicId) {
  const topics = await api("/path");
  const t = topics.find((x) => x.id === topicId);
  if (!t) {
    view.innerHTML = `<div class="empty"><div class="big">🤷</div><h2>Такой темы нет</h2><a class="btn" href="#/">Все темы</a></div>`;
    return;
  }
  const pct = t.total ? Math.round((100 * t.completed) / t.total) : 0;
  view.innerHTML = `
    <div class="topbar path-top">${pills()}</div>
    <div class="topic-head" style="--tc:${esc(t.color)}">
      <a class="btn ghost small" href="#/">← Все темы</a>
      <div class="th-title"><span>${esc(t.icon)}</span><div><h1>${esc(t.title)}</h1>
        <div class="th-meta"><div class="bar"><i style="width:${pct}%"></i></div><small class="muted">${t.completed} / ${t.total} ${plural(t.total, "урок", "урока", "уроков")}${t.trophy ? " · 🏆 тема пройдена" : ""}</small></div></div></div>
    </div>
    <div style="--tc:${esc(t.color)}">${t.modules.map((m, mi) => unit(m, mi)).join("") ||
      `<div class="empty"><div class="big">🧱</div><p class="muted">В этой теме пока нет модулей.</p></div>`}</div>`;

  view.querySelectorAll(".node").forEach((n) => n.onclick = (e) => {
    e.stopPropagation();
    sound("click");
    togglePopover(n.closest(".node-wrap"));
  });
  view.onclick = () => view.querySelectorAll(".popover").forEach((p) => p.remove());
  view.querySelector(".node-wrap.current .node")?.scrollIntoView({ block: "center", behavior: "smooth" });
}

function unit(m, mi) {
  let i = 0;
  const nodes = m.lessons.map((l) => {
    const off = OFFSETS[i++ % OFFSETS.length];
    const icon = l.status === "done" ? "✓" : l.status === "locked" ? "🔒" : "★";
    return `<div class="node-wrap ${l.status}" style="transform:translateX(${off}px)"
        data-id="${l.id}" data-status="${l.status}" data-title="${esc(l.title)}"
        data-info="${l.exercises} ${plural(l.exercises, "задание", "задания", "заданий")}">
      ${l.status === "current" ? `<div class="start-tip">${l.solved ? "Продолжить" : "Начать"}</div>` : ""}
      <button class="node ${l.status}" aria-label="${esc(l.title)}">${icon}${l.perfect ? `<span class="crown">👑</span>` : ""}</button>
      <div class="node-label ${off > 0 ? "left" : "right"}">
        <b>${esc(l.title)}</b>
        <small>${l.status === "locked" ? "🔒 " : ""}${l.solved}/${l.exercises} ${plural(l.exercises, "задание", "задания", "заданий")}</small>
      </div>
    </div>`;
  }).join("");
  return `<section class="unit">
    <div class="unit-head"><div class="u-icon">${esc(m.icon)}</div>
      <div><small>Модуль ${mi + 1}</small><h2>${esc(m.title)}</h2>${m.description ? `<p>${esc(m.description)}</p>` : ""}</div></div>
    <div class="nodes">${nodes}
      <div class="chest ${m.trophy ? "earned" : ""}" title="${m.trophy ? "Награда за модуль получена!" : "Пройди все уроки модуля, чтобы получить награду"}">${m.trophy ? "🏅" : "🎁"}</div>
    </div></section>`;
}

function togglePopover(wrap) {
  const had = wrap.querySelector(".popover");
  document.querySelectorAll(".popover").forEach((p) => p.remove());
  if (had) return;
  const { id, status, title, info } = wrap.dataset;
  const pop = document.createElement("div");
  pop.className = `popover ${status === "locked" ? "locked" : ""}`;
  pop.style.transform = `translateX(-50%)`;
  pop.innerHTML = status === "locked"
    ? `<h3>${esc(title)}</h3><p>Пройди предыдущие уроки, чтобы открыть этот.</p><button class="btn" disabled>Закрыто</button>`
    : `<h3>${esc(title)}</h3><p>${esc(info)}</p><a class="btn" href="#/lesson/${id}">${status === "done" ? "Повторить +XP" : "Начать +XP"}</a>`;
  pop.onclick = (e) => e.stopPropagation();
  wrap.append(pop);
}
