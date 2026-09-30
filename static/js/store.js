// Глобальное состояние игрока (XP, сердечки, streak…) и его отображение.
import { api, esc, toast, plural, ic, owl } from "./util.js";
import { achIconName } from "./achievements.js";

export const store = { state: null, user: null, listeners: new Set() };

export function setState(state) {
  store.state = state;
  document.documentElement.dataset.theme = state.theme;
  document.getElementById("theme-color")?.setAttribute("content", state.theme === "dark" ? "#0b0f0d" : "#f3f6f0");
  try { localStorage.setItem("cq-theme", state.theme); } catch { /* ok */ }
  const badge = document.getElementById("review-badge");
  badge.hidden = !state.review_count;
  badge.textContent = state.review_count;
  renderRail();
  store.listeners.forEach((fn) => fn(state));
}

export async function refreshState() {
  setState(await api("/state"));
  return store.state;
}

export function onState(fn) {
  store.listeners.add(fn);
  return () => store.listeners.delete(fn);
}

export function pills(s = store.state) {
  if (!s) return "";
  const hearts = s.hearts_enabled
    ? `<a class="pill heart" href="#/review" title="Сердечки. Возвращаются в работе над ошибками">${ic("heart")}${s.hearts}</a>`
    : `<span class="pill heart" title="Сердечки выключены">${ic("heart")}∞</span>`;
  return `
    <a class="pill fire ${s.streak ? "" : "cold"}" href="#/stats" title="Серия дней">${ic("flame")}${s.streak}</a>
    <a class="pill gem" href="#/stats" title="Всего опыта">${ic("bolt")}${fmtNum(s.xp)}</a>
    ${hearts}`;
}

const fmtNum = (n) => n.toLocaleString("ru-RU");
const WEEK = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
const heartRow = (s) => ic("heart").repeat(s.hearts) + ic("heartE").repeat(s.max_hearts - s.hearts);

// Компактная сводка для телефона и планшета: там боковой колонки нет (см. .status-strip в CSS).
export function statusStrip(s = store.state) {
  if (!s) return "";
  const goalPct = Math.min(100, Math.round((100 * s.today_xp) / s.daily_goal));
  const lvlPct = Math.round((100 * s.level_xp) / s.level_size);
  const streakText = !s.streak ? "Реши задание, чтобы начать"
    : s.streak_at_risk ? "Под угрозой — позанимайся!" : `${s.streak} ${plural(s.streak, "день", "дня", "дней")} подряд`;
  const hearts = s.hearts_enabled
    ? `<div class="ss-item"><b>Сердечки</b><div class="ss-hearts">${heartRow(s)}</div>
        <small class="muted">${s.hearts < s.max_hearts ? "Вернёшь в работе над ошибками" : "Все на месте"}</small></div>`
    : `<div class="ss-item"><b>Сердечки</b><div class="ss-hearts">∞</div><small class="muted">Выключены</small></div>`;
  return `
    <div class="ss-item"><b>Цель дня</b>
      ${goalPct >= 100 ? `<div class="goal-done">Выполнено!</div>`
        : `<div class="bar gold"><i style="width:${goalPct}%"></i></div>`}
      <small class="muted">${s.today_xp} / ${s.daily_goal} XP</small></div>
    <div class="ss-item"><b>Уровень ${s.level}</b>
      <div class="bar purple"><i style="width:${lvlPct}%"></i></div>
      <small class="muted">${s.level_xp} / ${s.level_size} XP</small></div>
    <div class="ss-item"><b>Серия</b><div>${esc(streakText)}</div>
      <small class="muted">Рекорд ${s.longest_streak} · заморозок: ${s.freezes}</small></div>
    ${hearts}`;
}

function renderRail() {
  const strip = document.getElementById("status-strip");
  if (strip) strip.innerHTML = statusStrip();
  const rail = document.getElementById("rail");
  const s = store.state;
  if (!rail || !s) return;
  const goalPct = Math.min(100, Math.round((100 * s.today_xp) / s.daily_goal));
  const lvlPct = Math.round((100 * s.level_xp) / s.level_size);
  const streakSub = s.streak
    ? (s.streak_at_risk ? "под угрозой — позанимайся сегодня!" : `серия · рекорд ${s.longest_streak}`)
    : "реши задание, чтобы начать серию";
  const week = (s.week || []).map((on, i) => `<i class="${on ? "on" : ""}">${WEEK[i]}</i>`).join("");
  const freezes = s.freezes ? `<small class="muted rail-freeze">${ic("snow")}Заморозки: ${s.freezes} — спасут серию при пропуске</small>` : "";
  const hearts = s.hearts_enabled
    ? `<div class="card rcard"><div class="rc-head"><b>Сердечки</b><span class="muted">${s.hearts} / ${s.max_hearts}</span></div>
        <div class="rail-hearts">${heartRow(s)}</div>
        ${s.hearts < s.max_hearts ? `<small class="muted">Возвращаются в <a class="link" href="#/review">работе над ошибками</a></small>` : ""}</div>`
    : "";
  const reviewNote = s.review_count
    ? `<a class="card rcard rail-owl" href="#/review">${owl("wave", "bob")}<div><b>${s.review_count} ${plural(s.review_count, "ошибка ждёт", "ошибки ждут", "ошибок ждут")} реванша</b>
        <div class="muted">Исправь — вернёшь сердечки</div></div></a>`
    : "";
  rail.innerHTML = `
    <div class="statbar">${pills(s)}</div>
    <div class="card rcard"><div class="rc-head"><b>Цель дня</b><span class="muted">${s.today_xp} / ${s.daily_goal} XP</span></div>
      ${goalPct >= 100 ? `<div class="goal-done">${ic("target")}Выполнено!</div>` : `<div class="bar gold"><i style="width:${goalPct}%"></i></div>`}</div>
    <div class="card rcard"><div class="rail-streak"><svg class="i ${s.streak ? "glowP" : "cold"}"><use href="#ic-flame"/></svg>
      <div><b>${s.streak} ${plural(s.streak, "день", "дня", "дней")}</b><div class="muted">${esc(streakSub)}</div></div></div>
      <div class="week">${week}</div>${freezes}</div>
    <div class="card rcard"><div class="rc-head"><b>Уровень ${s.level}</b><span class="muted">${s.level_xp} / ${s.level_size} XP</span></div>
      <div class="bar purple"><i style="width:${lvlPct}%"></i></div></div>
    ${hearts}
    ${reviewNote}
  `;
}

// Показать события, пришедшие с сервера (достижения, уровень, цель…)
export function announce(events) {
  for (const e of events || []) {
    if (e.type === "achievement") toast(achIconName(e.code), `Достижение: ${e.title}`, e.description);
    else if (e.type === "level_up") toast("star", `Новый уровень ${e.level}!`);
    else if (e.type === "goal_met") toast("target", "Дневная цель выполнена!", `${e.goal} XP`);
    else if (e.type === "freeze_earned") toast("snow", "Заморозка серии получена", "Спасёт серию, если пропустишь день");
    else if (e.type === "freeze_used") toast("snow", "Серия спасена заморозкой!");
    else if (e.type === "heart_restored") toast("heart", `+${e.amount || 1} ${plural(e.amount || 1, "сердечко", "сердечка", "сердечек")}`, "Ошибка исправлена");
  }
}
