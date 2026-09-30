// «Учиться»: каталог тем (сгруппированный) → страница темы с дорожкой уроков (зигзаг или список).
import { api, esc, md, sound, plural, toast, ic, owl } from "../util.js";
import { bindRunnable } from "../runnable.js";
import { store, pills, statusStrip } from "../store.js";
import { glyph } from "../glyphs.js";

const OFFSETS = [0, 44, 70, 44, 0, -44, -70, -44]; // зигзаг дорожки (у нечётных модулей — зеркально)
const NO_GROUP = "Другие темы";
// Цвета плашек модулей — по кругу
const MOD_COLORS = [["#4f9e1c", "#1f4a0c"], ["#8a4fd6", "#3d1d6e"], ["#2e8fd6", "#0f3150"], ["#d6802e", "#5a2e0c"], ["#d64f8f", "#5e1a3a"], ["#1fa89a", "#0b4640"]];
// Сова у модуля: поза и анимация меняются от модуля к модулю
const OWLS = [["think", "tilt"], ["wave", "bob"], ["happy", "breathe"], ["think", "bob"], ["wave", "tilt"]];

const emptyContent = `<div class="empty">${owl("sleep", "breathe")}<h2>Пока нет ни одной темы</h2>
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
    <div class="card status-strip" id="status-strip">${statusStrip()}</div>
    ${cont ? continueBanner(cont) : ""}
    ${[...groups].map(([name, list]) => `
      <section class="topic-group">
        <h2 class="group-title">${esc(name)} <small class="muted">${list.filter((t) => t.trophy).length} / ${list.length} пройдено</small></h2>
        <div class="topic-grid">${list.map(topicCard).join("")}</div>
      </section>`).join("")}`;
}

function continueBanner(c) {
  const pct = c.lesson.exercises ? Math.round((100 * c.lesson.solved) / c.lesson.exercises) : 0;
  return `<a class="continue" href="#/lesson/${c.lesson.id}">
    ${glyph(c.topic, 60)}
    <div class="c-body">
      <div class="kind">${c.started ? "Продолжить" : "Начни отсюда"}</div>
      <b>${esc(c.lesson.title)}</b>
      <div class="muted c-topic">${esc(c.topic.title)} · ${esc(c.module)}</div>
      <div class="c-meta"><div class="bar"><i style="width:${pct}%"></i></div>
        <span>${c.lesson.solved} / ${c.lesson.exercises}</span></div>
    </div>
    <span class="btn c-btn">${c.started && c.lesson.solved ? "Продолжить" : "Начать"}${ic("play")}</span>
  </a>`;
}

function topicCard(t) {
  const pct = t.total ? Math.round((100 * t.completed) / t.total) : 0;
  const action = t.trophy ? "Повторить" : t.completed ? "Продолжить" : "Начать";
  return `<a class="topic-card card ${t.trophy ? "finished" : ""}" href="#/topic/${t.id}" style="--tc:${esc(t.color)}">
    <div class="tc-head">${glyph(t)}${t.trophy ? `<span class="tc-cup" title="Тема пройдена">${ic("cup")}</span>` : ""}</div>
    <h3>${esc(t.title)}</h3>
    <p>${esc(t.description)}</p>
    <div class="tc-foot">
      <div class="bar"><i style="width:${pct}%"></i></div>
      <small>${t.completed} / ${t.total} ${plural(t.total, "урок", "урока", "уроков")} · ${t.modules.length} ${plural(t.modules.length, "модуль", "модуля", "модулей")}</small>
      <span class="tc-action">${action}${ic("arrowR")}</span>
    </div>
  </a>`;
}

// ---------- Страница темы ----------
export async function renderTopic(view, topicId) {
  const topics = await api("/path");
  const t = topics.find((x) => x.id === topicId);
  if (!t) {
    view.innerHTML = `<div class="empty">${owl("think", "tilt")}<h2>Такой темы нет</h2><a class="btn" href="#/">Все темы</a></div>`;
    return;
  }
  const pct = t.total ? Math.round((100 * t.completed) / t.total) : 0;
  const asList = store.state?.path_view === "list";
  view.innerHTML = `
    <div class="topic-head" style="--tc:${esc(t.color)}">
      <a class="icon-btn" href="#/" title="Все темы">${ic("back")}</a>
      ${glyph(t, 46)}
      <div class="th-name"><h1>${esc(t.title)}</h1>
        <div class="muted">${t.completed} из ${t.total} ${plural(t.total, "урока", "уроков", "уроков")} · ${pct}%${t.trophy ? " · тема пройдена" : ""}</div></div>
      <a class="act cheat" href="#/topic/${t.id}/theory">${ic("book")}<span>Теория</span></a>
    </div>
    <div class="th-bar bar"><i style="width:${pct}%"></i></div>
    <div class="${asList ? "lesson-list" : "trail"}">${t.modules.map((m, mi) => (asList ? listUnit : unit)(m, mi, t)).join("") ||
      `<div class="empty">${owl("sleep", "breathe")}<p class="muted">В этой теме пока нет модулей.</p></div>`}</div>
    ${t.modules.length ? `<div class="topic-cup ${t.trophy ? "earned" : ""}">${ic("cup")}<b>${t.trophy ? "Тема пройдена!" : "Кубок темы"}</b>
      <small class="muted">${t.trophy ? "Кубок уже в «Наградах»" : "Пройди все уроки темы"}</small></div>` : ""}`;

  view.querySelectorAll("[data-open]").forEach((n) => n.onclick = () => openLesson(n));
  if (!asList) {
    drawTrails(view);
    const redraw = () => (view.isConnected ? drawTrails(view) : window.removeEventListener("resize", redraw));
    window.addEventListener("resize", redraw);
  }
  view.querySelector(".node-wrap.current, .ll-item.current")?.scrollIntoView({ block: "center", behavior: "smooth" });
}

// ---------- Теория темы: все уроки подряд, как учебник ----------
const THEORY_KEY = "cq-theory-view";   // «full» или «short» — удобство конкретного браузера

export async function renderTopicTheory(view, topicId) {
  const [data, topics] = await Promise.all([api(`/topics/${topicId}/theory`), api("/path")]);
  const status = {};                   // для ссылок «к заданиям»: закрытый урок открыть нельзя
  for (const t of topics) for (const m of t.modules) for (const l of m.lessons) status[l.id] = l.status;
  let mode = "full";
  try { if (localStorage.getItem(THEORY_KEY) === "short") mode = "short"; } catch { /* ок */ }
  let num = 0;
  const lessons = data.modules.flatMap((m) => m.lessons.map((l) => ({ ...l, n: ++num })));

  const draw = () => {
    const toc = data.modules.map((m, mi) => `<div class="toc-mod"><b>${esc(m.icon)} Модуль ${mi + 1}. ${esc(m.title)}</b>
      <ol>${m.lessons.map((l) => {
        const n = lessons.find((x) => x.id === l.id).n;
        return `<li value="${n}"><button class="link" data-goto="${l.id}">${esc(l.title)}</button>${status[l.id] === "done" ? " ✓" : ""}</li>`;
      }).join("")}</ol></div>`).join("");
    const body = data.modules.map((m, mi) => `<h2 class="theory-mod">${esc(m.icon)} Модуль ${mi + 1}. ${esc(m.title)}</h2>
      ${m.lessons.map((l) => {
        const n = lessons.find((x) => x.id === l.id).n;
        const text = mode === "short" ? (l.theory || l.theory_full) : (l.theory_full || l.theory);
        const go = status[l.id] === "locked"
          ? `<span class="muted">🔒 Задания откроются после предыдущего урока</span>`
          : `<a class="btn small" href="#/lesson/${l.id}">Перейти к заданиям →</a>`;
        return `<article class="card theory-lesson" id="theory-${l.id}">
          <div class="ex-kind">Урок ${n}${status[l.id] === "done" ? " · ✓ пройден" : ""}</div>
          <h2 style="margin-top:4px">${esc(l.title)}</h2>
          <div class="theory md ${mode === "full" ? "full" : ""}">${md(text || "_Теории пока нет._", { runnable: true })}</div>
          <div class="theory-foot"><button class="btn ghost small" data-toc>↑ К содержанию</button><div class="spacer"></div>${go}</div></article>`;
      }).join("")}`).join("");
    view.innerHTML = `<div class="topbar path-top">${pills()}</div>
      <div class="topic-theory" style="--tc:${esc(data.color)}">
        <div class="th-actions"><a class="btn ghost small" href="#/topic/${data.id}">← К урокам</a></div>
        <h1 class="section-title">📚 ${esc(data.icon)} ${esc(data.title)}</h1>
        <div class="choice theory-mode">
          <button data-mode="full" class="${mode === "full" ? "on" : ""}">📖 Полная теория</button>
          <button data-mode="short" class="${mode === "short" ? "on" : ""}">📝 Только шпаргалки</button></div>
        <div class="card theory-toc"><h3 style="margin-top:0">Содержание</h3>${toc}</div>
        ${body}
      </div>`;
    bindRunnable(view);
    view.querySelectorAll("[data-mode]").forEach((b) => b.onclick = () => {
      mode = b.dataset.mode;
      try { localStorage.setItem(THEORY_KEY, mode); } catch { /* ок */ }
      const y = window.scrollY;
      draw();
      window.scrollTo(0, y);
    });
    view.querySelectorAll("[data-toc]").forEach((b) => b.onclick = () =>
      view.querySelector(".theory-toc").scrollIntoView({ behavior: "smooth", block: "start" }));
    view.querySelectorAll("[data-goto]").forEach((b) => b.onclick = () =>
      document.getElementById(`theory-${b.dataset.goto}`)?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };
  draw();
}

const modHead = (m, mi) => {
  const [c1, c2] = MOD_COLORS[mi % MOD_COLORS.length];
  return `<div class="mod" style="--m1:${c1};--m2:${c2}"><small>Модуль ${mi + 1}</small><b>${esc(m.title)}</b>
    ${m.description ? `<p>${esc(m.description)}</p>` : ""}</div>`;
};
const exercisesText = (l) => l.status === "done" || l.solved
  ? `${l.solved} / ${l.exercises}${l.perfect ? " · без ошибок" : ""}`
  : `${l.exercises} ${plural(l.exercises, "задание", "задания", "заданий")}`;
const nodeIcon = (l) => ic(l.status === "done" ? "check" : l.status === "locked" ? "lock" : "star");

// Зигзаг: узлы уроков, пунктирная тропинка (рисуется после вёрстки), сова и награда в конце модуля.
function unit(m, mi) {
  const mirror = mi % 2 ? -1 : 1;
  const nodes = m.lessons.map((l, i) => {
    const off = OFFSETS[i % OFFSETS.length] * mirror;
    return `<div class="node-wrap ${l.status}" style="--off:${off}" data-open data-id="${l.id}" data-status="${l.status}">
      ${l.status === "current" ? `<div class="start-tip">${l.solved ? "Продолжить" : "Начать"}</div>` : ""}
      <button class="node ${l.status}" aria-label="${esc(l.title)}">${nodeIcon(l)}${l.perfect ? `<span class="crown" title="Без ошибок">${ic("star")}</span>` : ""}</button>
      <div class="node-label ${off > 0 ? "left" : "right"}"><b>${esc(l.title)}</b><small>${exercisesText(l)}</small></div>
    </div>`;
  }).join("");
  const allLocked = m.lessons.length && m.lessons.every((l) => l.status === "locked");
  const allDone = m.lessons.length && m.lessons.every((l) => l.status === "done");
  const [pose, anim] = allLocked ? ["sleep", "breathe"] : allDone ? ["happy", "hop"] : OWLS[mi % OWLS.length];
  const owlSide = mirror > 0 ? "left" : "right";
  return `<section class="unit">
    ${modHead(m, mi)}
    <div class="nodes"><svg class="trail-line" aria-hidden="true"><path/></svg>${nodes}</div>
    <div class="unit-end ${owlSide}">
      <div class="unit-owl">${owl(pose, anim)}</div>
      <div class="reward-chest ${m.trophy ? "earned" : ""}" title="${m.trophy ? "Награда за модуль получена!" : "Пройди все уроки модуля, чтобы получить награду"}">
        ${ic(m.trophy ? "medalI" : "chest")}<small>${m.trophy ? "Награда получена" : "Награда модуля"}</small></div>
    </div></section>`;
}

// Пунктир через центры узлов каждого модуля — по реальным координатам после вёрстки.
function drawTrails(view) {
  view.querySelectorAll(".unit .nodes").forEach((box) => {
    const svg = box.querySelector(".trail-line");
    const r0 = box.getBoundingClientRect();
    const pts = [...box.querySelectorAll(".node")].map((n) => {
      const r = n.getBoundingClientRect();
      return [r.left + r.width / 2 - r0.left, r.top + r.height / 2 - r0.top];
    });
    svg.setAttribute("width", r0.width);
    svg.setAttribute("height", r0.height);
    if (pts.length < 2) { svg.querySelector("path").setAttribute("d", ""); return; }
    let d = `M${pts[0][0]} ${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
      const my = (y0 + y1) / 2;
      d += ` C${x0} ${my}, ${x1} ${my}, ${x1} ${y1}`;
    }
    svg.querySelector("path").setAttribute("d", d);
  });
}

// Список: карточка на урок, в конце модуля — награда.
function listUnit(m, mi) {
  const [c1] = MOD_COLORS[mi % MOD_COLORS.length];
  const items = m.lessons.map((l) => {
    const pct = l.exercises ? Math.round((100 * l.solved) / l.exercises) : 0;
    const active = l.status === "current" || l.status === "open";
    return `<div class="ll-item card ${l.status}" data-open data-id="${l.id}" data-status="${l.status}" role="button" tabindex="0">
      <span class="ll-ico">${nodeIcon(l)}</span>
      <div class="ll-body"><b>${esc(l.title)}</b><small class="muted">${exercisesText(l)}</small>
        ${active && l.solved ? `<div class="bar"><i style="width:${pct}%"></i></div>` : ""}</div>
      ${l.status === "current" ? `<span class="btn small">${l.solved ? "Дальше" : "Начать"}</span>` : ""}
    </div>`;
  }).join("");
  return `<section class="ll-unit">
    <div class="kind" style="color:${c1}">Модуль ${mi + 1} · ${esc(m.title)}</div>
    ${items}
    <div class="ll-reward ${m.trophy ? "earned" : ""}">${ic(m.trophy ? "medalI" : "chest")}
      <div><b>${m.trophy ? "Награда получена" : "Награда модуля"}</b>
      <small class="muted">${m.trophy ? "Все уроки модуля пройдены" : `Пройди ${m.lessons.length === 1 ? "урок" : `все ${m.lessons.length} ${plural(m.lessons.length, "урок", "урока", "уроков")}`}`}</small></div></div>
  </section>`;
}

// Нажатие на урок сразу открывает его; закрытый — короткая подсказка вместо перехода.
function openLesson(el) {
  const { id, status } = el.dataset;
  if (status === "locked") {
    toast("lock", "Урок пока закрыт", "Пройди предыдущие уроки или включи «Открыть все уроки» в настройках.");
    return;
  }
  sound("click");
  location.hash = `#/lesson/${id}`;
}
