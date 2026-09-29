// Глобальное состояние игрока (XP, сердечки, streak…) и его отображение.
import { api, esc, toast, plural } from "./util.js";

export const store = { state: null, user: null, listeners: new Set() };

export function setState(state) {
  store.state = state;
  document.documentElement.dataset.theme = state.theme;
  document.getElementById("theme-color")?.setAttribute("content", state.theme === "dark" ? "#131f24" : "#ffffff");
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
    ? `<a class="pill heart" href="#/review" title="Сердечки. Восстанавливаются со временем или в Повторении">❤️ ${s.hearts}</a>`
    : `<span class="pill heart" title="Сердечки выключены">❤️ ∞</span>`;
  return `
    <a class="pill fire ${s.streak ? "" : "cold"}" href="#/stats" title="Серия дней">🔥 ${s.streak}</a>
    <a class="pill gem" href="#/stats" title="Всего опыта">⚡ ${s.xp}</a>
    ${hearts}`;
}

// Компактная сводка для телефона и планшета: там боковой колонки нет (см. .status-strip в CSS).
export function statusStrip(s = store.state) {
  if (!s) return "";
  const goalPct = Math.min(100, Math.round((100 * s.today_xp) / s.daily_goal));
  const lvlPct = Math.round((100 * s.level_xp) / s.level_size);
  const streakText = !s.streak ? "Реши задание, чтобы начать"
    : s.streak_at_risk ? "Под угрозой — позанимайся!" : `${s.streak} ${plural(s.streak, "день", "дня", "дней")} подряд`;
  const hearts = s.hearts_enabled
    ? `<div class="ss-item"><b>❤️ Сердечки</b><div class="ss-hearts">${"❤️".repeat(s.hearts)}${"🤍".repeat(s.max_hearts - s.hearts)}</div>
        <small class="muted">${s.hearts < s.max_hearts ? "Вернёшь в работе над ошибками" : "Все на месте"}</small></div>`
    : `<div class="ss-item"><b>❤️ Сердечки</b><div class="ss-hearts">∞</div><small class="muted">Выключены</small></div>`;
  return `
    <div class="ss-item"><b>🎯 Цель дня</b>
      ${goalPct >= 100 ? `<div class="goal-done">Выполнено!</div>`
        : `<div class="bar" style="--c:var(--gold)"><i style="width:${goalPct}%"></i></div>`}
      <small class="muted">${s.today_xp} / ${s.daily_goal} XP</small></div>
    <div class="ss-item"><b>🦉 Уровень ${s.level}</b>
      <div class="bar" style="--c:var(--purple)"><i style="width:${lvlPct}%"></i></div>
      <small class="muted">${s.level_xp} / ${s.level_size} XP</small></div>
    <div class="ss-item"><b>🔥 Серия</b><div>${esc(streakText)}</div>
      <small class="muted">Рекорд ${s.longest_streak} · ${"🧊".repeat(s.freezes) || "без заморозок"}</small></div>
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
  const streakText = s.streak
    ? (s.streak_at_risk ? "Серия под угрозой — позанимайся сегодня!" : `${s.streak} ${plural(s.streak, "день", "дня", "дней")} подряд`)
    : "Реши задание, чтобы начать серию";
  let heartsText = "";
  if (s.hearts_enabled && s.hearts < s.max_hearts) {
    heartsText = `<small class="muted">Сердечки возвращаются в <a href="#/review">работе над ошибками</a></small>`;
  }
  rail.innerHTML = `
    <div class="statbar">${pills(s)}</div>
    <div class="card">
      <h3>Дневная цель</h3>
      ${goalPct >= 100
        ? `<div class="goal-row"><div class="icon">🎯</div><div class="goal-done">Выполнено!</div></div>`
        : `<div class="goal-row"><div class="icon">⚡</div>
            <div style="flex:1"><div class="bar" style="--c:var(--gold)"><i style="width:${goalPct}%"></i></div>
            <small class="muted">${s.today_xp} / ${s.daily_goal} XP сегодня</small></div></div>`}
    </div>
    <div class="card">
      <h3>Уровень ${s.level}</h3>
      <div class="bar" style="--c:var(--purple)"><i style="width:${lvlPct}%"></i></div>
      <small class="muted">${s.level_xp} / ${s.level_size} XP до уровня ${s.level + 1}</small>
    </div>
    <div class="card">
      <h3>🔥 Серия</h3>
      <div>${esc(streakText)}</div>
      <small class="muted">Рекорд: ${s.longest_streak} · Заморозки: ${"🧊".repeat(s.freezes) || "нет"}</small>
    </div>
    ${s.hearts_enabled ? `<div class="card"><h3>Сердечки</h3><div style="font-size:26px">${"❤️".repeat(s.hearts)}${"🤍".repeat(s.max_hearts - s.hearts)}</div>${heartsText}</div>` : ""}
  `;
}

// Показать события, пришедшие с сервера (достижения, уровень, цель…)
export function announce(events) {
  for (const e of events || []) {
    if (e.type === "achievement") toast(e.icon, `Достижение: ${e.title}`, e.description);
    else if (e.type === "level_up") toast("🆙", `Новый уровень ${e.level}!`);
    else if (e.type === "goal_met") toast("🎯", "Дневная цель выполнена!", `${e.goal} XP`);
    else if (e.type === "freeze_earned") toast("🧊", "Заморозка серии получена", "Спасёт серию, если пропустишь день");
    else if (e.type === "freeze_used") toast("🧊", "Серия спасена заморозкой!");
    else if (e.type === "heart_restored") toast("❤️", `+${e.amount || 1} ${plural(e.amount || 1, "сердечко", "сердечка", "сердечек")}`, "Ошибка исправлена");
  }
}

// Раз в 30 секунд обновляем таймер сердечек
