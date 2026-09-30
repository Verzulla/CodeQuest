// Глобальное состояние игрока (XP, сердечки, streak…) и его отображение.
import { api, esc, toast, plural, ic, owl, modal } from "./util.js";
import { achIconName } from "./achievements.js";

export const store = { state: null, user: null, listeners: new Set() };

export function setState(state) {
  store.state = state;
  if (state.notice) showStreakNotice(state.notice);
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
const days = (n) => `${n} ${plural(n, "день", "дня", "дней")}`;

// Неделя серии: занимался — оранжевый, спасено заморозкой — голубой со снежинкой, сегодня — пунктир.
export function weekRow(s) {
  const todayIdx = (new Date().getDay() + 6) % 7;
  return `<div class="week">${(s.week || []).map((d, i) => d === "frz"
    ? `<i class="frz ${i === todayIdx ? "today" : ""}" title="Спасено заморозкой">${ic("snow")}</i>`
    : `<i class="${d === "on" ? "on" : ""} ${i === todayIdx ? "today" : ""}">${WEEK[i]}</i>`).join("")}</div>`;
}

// Копилка заморозок: ячейки, когда будет следующая, подсказка «?».
export function freezeBox(s) {
  const max = s.max_freezes || 2;
  const slots = Array.from({ length: max }, (_, i) => `<span class="slot ${i < s.freezes ? "on" : ""}">${i < s.freezes ? ic("snow") : ""}</span>`).join("");
  const next = s.freeze_next == null
    ? `<div class="frz-next">Копилка полна: больше ${max === 2 ? "двух" : max} заморозок не хранится</div>`
    : `<div class="frz-next">Новая заморозка через <b>${days(s.freeze_next)}</b> серии</div>
       <div class="frz-bar"><i style="width:${Math.round((100 * (7 - s.freeze_next)) / 7)}%"></i></div>`;
  return `<div class="frz-box">
    <div class="frz-row">${ic("snow", "frz-ico")}Заморозки<button class="q" type="button" data-frz-help aria-label="Как работают заморозки">?</button>
      <span class="slots">${slots}</span></div>
    ${next}
  </div>`;
}
// «?» у заморозок: на десктопе — всплывающая подсказка поверх страницы (наведение или нажатие),
// на телефоне — шторка снизу. Ничего не сдвигает в карточке.
const FRZ_RULES = (max) => [
  ["snow", "<b>Спасает серию</b>, если пропустил день. Тратится сама, когда возвращаешься: один день — одна заморозка."],
  ["flame", `Новую дают за каждые <b>7 дней</b> серии. Хранить можно до <b>${max}</b>.`],
  ["warn", "Пропустил больше дней, чем есть заморозок, — <b>серия начнётся заново</b>."],
];
const hoverDevice = () => matchMedia("(hover: hover) and (pointer: fine)").matches && window.innerWidth > 700;
let tip = null, tipBtn = null, tipTimer = null;
function closeTip() {
  clearTimeout(tipTimer);
  tip?.remove(); tip = null;
  tipBtn?.classList.remove("on"); tipBtn = null;
}
function openTip(btn) {
  if (tipBtn === btn) return;
  closeTip();
  const max = store.state?.max_freezes || 2;
  tip = document.createElement("div");
  tip.className = "frz-tip";
  tip.setAttribute("role", "tooltip");
  tip.innerHTML = `<div class="tip-h">${ic("snow")}Как работают заморозки</div>
    <ul>${FRZ_RULES(max).map(([, t]) => `<li>${t}</li>`).join("")}</ul>`;
  document.body.append(tip);
  const r = btn.getBoundingClientRect(), w = tip.offsetWidth;
  const left = Math.min(Math.max(12, r.left + r.width / 2 - w / 2), window.innerWidth - w - 12);
  tip.style.left = `${left + window.scrollX}px`;
  tip.style.top = `${r.bottom + 10 + window.scrollY}px`;
  tip.style.setProperty("--arrow", `${r.left + r.width / 2 - left}px`);
  tip.addEventListener("mouseenter", () => clearTimeout(tipTimer));
  tip.addEventListener("mouseleave", () => { tipTimer = setTimeout(closeTip, 150); });
  tipBtn = btn;
  btn.classList.add("on");
}
function openSheet() {
  const max = store.state?.max_freezes || 2;
  const wrap = document.createElement("div");
  wrap.className = "sheet-wrap";
  wrap.innerHTML = `<div class="sheet-dim"></div><div class="sheet" role="dialog" aria-label="Как работают заморозки">
      <div class="grab"></div>${owl("think", "tilt")}<h2>Как работают заморозки</h2>
      ${FRZ_RULES(max).map(([icon, t]) => `<div class="rule"><span class="ri2">${ic(icon)}</span><div>${t}</div></div>`).join("")}
      <button class="btn wide" data-close>Понятно</button></div>`;
  document.body.append(wrap);
  requestAnimationFrame(() => wrap.classList.add("open"));
  const sheet = wrap.querySelector(".sheet");
  const close = () => { wrap.classList.remove("open"); setTimeout(() => wrap.remove(), 250); };
  wrap.querySelector(".sheet-dim").onclick = close;
  wrap.querySelector("[data-close]").onclick = close;
  // свайп вниз — закрыть
  let y0 = null;
  sheet.addEventListener("touchstart", (e) => { y0 = e.touches[0].clientY; sheet.style.transition = "none"; }, { passive: true });
  sheet.addEventListener("touchmove", (e) => {
    if (y0 == null) return;
    const dy = Math.max(0, e.touches[0].clientY - y0);
    sheet.style.transform = `translateY(${dy}px)`;
  }, { passive: true });
  sheet.addEventListener("touchend", (e) => {
    const dy = e.changedTouches[0].clientY - (y0 ?? 0);
    sheet.style.transition = ""; sheet.style.transform = "";
    y0 = null;
    if (dy > 80) close();
  });
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-frz-help]");
  if (b) {
    if (hoverDevice()) { tipBtn === b ? closeTip() : openTip(b); } else openSheet();
    return;
  }
  if (tip && !e.target.closest(".frz-tip")) closeTip();
});
document.addEventListener("mouseover", (e) => {
  const b = e.target.closest?.("[data-frz-help]");
  if (b && hoverDevice()) { clearTimeout(tipTimer); openTip(b); }
});
document.addEventListener("mouseout", (e) => {
  if (e.target.closest?.("[data-frz-help]") && tip) tipTimer = setTimeout(closeTip, 150);
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeTip(); });
window.addEventListener("hashchange", closeTip);

// Окно при возвращении: заморозка спасла серию или серия сгорела. Приходит с сервера один раз.
function showStreakNotice(n) {
  setTimeout(() => {
    if (document.querySelector(".modal")) return;          // не перекрываем приветствие новичка
    // оставшиеся — слева, потраченные — справа: заморозки «сгорают» справа налево, как в копилке
    const snow = (used) => `<span class="${used ? "used" : ""}">${ic("snow")}</span>`;
    const m = n.type === "freeze_used"
      ? modal(`${owl("happy", "bob")}
        <div class="snowbig">${Array.from({ length: n.freezes }, () => snow(false)).join("")}${Array.from({ length: n.count }, () => snow(true)).join("")}</div>
        <h2>Серия спасена!</h2>
        <p class="muted">${n.count === 1 ? "Вчера ты не занимался" : `Ты пропустил ${days(n.count)}`} — ${n.count === 1 ? "заморозка сохранила" : "заморозки сохранили"} твою серию <b class="hl-streak">${days(n.streak)}</b>.</p>
        <p class="muted">${n.freezes ? `Осталось заморозок: ${n.freezes}.` : "Заморозок больше нет."}${n.next_in ? ` Новую дадут через ${days(n.next_in)} серии.` : ""}</p>
        <div class="btns"><button class="btn" data-ok>Продолжить серию</button></div>`)
      : modal(`${owl("sad", "breathe")}<h2>Серия сгорела</h2>
        <p class="muted">Ты пропустил ${days(n.missed)}, а ${n.freezes ? `заморозок было ${n.freezes}` : "заморозок не было"}.
        Серия начинается заново — рекорд <b class="hl-streak">${days(n.record)}</b> остаётся в статистике.</p>
        <div class="btns"><button class="btn" data-ok>Начать новую серию</button></div>`);
    m.root.classList.add(n.type === "freeze_used" ? "modal-frz" : "modal-lost");
    m.root.querySelector("[data-ok]").onclick = m.close;
  }, 400);
}
const heartRow = (s) => ic("heart").repeat(s.hearts) + ic("heartE").repeat(s.max_hearts - s.hearts);

// Что сова скажет на главной — по тому, как идёт день. Серия засчитывается за любой опыт,
// цель дня — отдельная планка по XP.
export function homeRemark(s = store.state) {
  const name = store.user?.username ? `, ${store.user.username}` : "";
  const left = Math.max(0, s.daily_goal - s.today_xp);
  const d = (n) => `${n} ${plural(n, "день", "дня", "дней")}`;
  if (s.today_xp >= s.daily_goal) return ["happy", `Цель дня выполнена! ${s.streak ? `${d(s.streak)} подряд — ` : ""}так держать.`];
  if (s.today_xp > 0) return ["happy", `Серия на сегодня сохранена! До цели дня ещё <b>${left} XP</b> — пара заданий.`];
  if (s.streak && s.streak_at_risk) return ["think", `Привет${name}! Серия под угрозой — <b>одно задание сегодня</b>, и она продолжится.`];
  if (s.streak) return ["wave", `Привет${name}! Реши задание, чтобы продлить серию: ${d(s.streak)} подряд.`];
  return ["wave", `Привет${name}! Реши одно задание — и огонёк серии загорится.`];
}

// Главная на телефоне и планшете (там нет правой колонки): сова с репликой и полоса серии.
export function statusStrip(s = store.state) {
  if (!s) return "";
  const [pose, text] = homeRemark(s);
  const goalPct = Math.min(100, Math.round((100 * s.today_xp) / s.daily_goal));
  return `
    <div class="hs-talk">${owl(pose, pose === "happy" ? "bob" : "tilt")}<div class="hs-bub">${text}</div></div>
    <div class="hs-sep"></div>
    <div class="hs-streak ${s.streak ? "" : "cold"}"><img src="/static/img/flames/flame-1.webp" alt="" draggable="false">
      <div><b>${s.streak} ${plural(s.streak, "день", "дня", "дней")}</b><small>серия · рекорд ${s.longest_streak}</small></div></div>
    ${weekRow(s)}
    <div class="hs-goal">${ic("target")}<div class="bar gold"><i style="width:${goalPct}%"></i></div><span>${s.today_xp} / ${s.daily_goal} XP</span></div>
    <div class="hs-foot"><span>Уровень <b class="lv">${s.level}</b> · ${s.level_xp}/${s.level_size} XP</span>
      <span class="hs-hearts">${s.hearts_enabled ? heartRow(s) : `${ic("heart")}∞`}</span></div>`;
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
      ${weekRow(s)}${freezeBox(s)}</div>
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
