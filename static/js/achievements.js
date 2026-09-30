// Значки достижений вместо эмодзи: SVG-иконка на «медали» своего цвета (код достижения → вид).
import { ic, esc } from "./util.js";

const GREEN = ["#8fe03e", "#2f7d0c"], BLUE = ["#6cc4ff", "#1d5f99"], PURPLE = ["#c68bff", "#5b2a9c"],
  CYAN = ["#5fe0d0", "#12706a"], GOLD = ["#ffd54a", "#b77800"], ORANGE = ["#ffb03a", "#c2410c"],
  RED = ["#ff8a8a", "#b8263a"], INDIGO = ["#8f9bff", "#2f3a9c"];

const LOOK = {
  first_step: ["star", GREEN], solver_25: ["target2", GREEN], solver_100: ["spark", GREEN],
  coder_10: ["code", BLUE], coder_50: ["term", BLUE],
  lesson_1: ["book", PURPLE], lesson_10: ["map", PURPLE],
  perfect_1: ["sparkle", CYAN], perfect_10: ["shield", CYAN],
  module_1: ["medalI", GOLD], module_5: ["medalI", GOLD], topic_1: ["cup", GOLD],
  streak_3: ["flame", ORANGE], streak_7: ["flame", ORANGE], streak_30: ["flame", RED],
  goal_1: ["target", ORANGE], goal_7: ["target", ORANGE],
  xp_500: ["bolt", GOLD], xp_2000: ["bolt", GOLD],
  level_5: ["star", PURPLE], review_10: ["heart", RED], night_owl: ["moon", INDIGO],
};

export const achIconName = (code) => (LOOK[code] || ["star", GREEN])[0];

// Короткая подпись на значке: 25, 1k…
const short = (n) => (n >= 1000 ? `${n / 1000}k` : String(n));

// Что значит достижение простыми словами — в подсказке по нажатию на значок.
const HOW = {
  first_step: "Засчитывается за первое правильно решённое задание в любом уроке.",
  solver_25: "Считаются все задания, решённые впервые, — в уроках, повторении и тренировке.",
  solver_100: "Считаются все задания, решённые впервые, — в уроках, повторении и тренировке.",
  coder_10: "Засчитываются задания «Напиши код», где твоя программа прошла все автотесты.",
  coder_50: "Засчитываются задания «Напиши код», где твоя программа прошла все автотесты.",
  lesson_1: "Урок засчитан, когда все его задания решены (или попробованы и ты нажал «Завершить урок»).",
  lesson_10: "Считаются разные пройденные уроки; повторное прохождение того же урока не добавляет.",
  perfect_1: "Пройди урок так, чтобы ни одна проверка не была ошибочной. «Запустить» ошибкой не считается.",
  perfect_10: "Десять уроков, в каждом из которых не было ни одной ошибочной проверки.",
  module_1: "Пройди все уроки одного модуля — получишь медаль модуля.",
  module_5: "Медали за пять разных модулей в любых темах.",
  topic_1: "Пройди все уроки всех модулей одной темы — получишь кубок темы.",
  streak_3: "Занимайся 3 дня подряд: день засчитывается за любой полученный опыт.",
  streak_7: "Неделя без пропусков. Заморозка, спасшая день, серию не прерывает.",
  streak_30: "Месяц без пропусков. Заморозка, спасшая день, серию не прерывает.",
  goal_1: "Набери за день столько XP, сколько выбрано в «Настройках» → «Дневная цель».",
  goal_7: "Дни не обязательно подряд: считаются все дни с выполненной целью.",
  xp_500: "Опыт за задания, уроки, модули и исправленные ошибки.",
  xp_2000: "Опыт за задания, уроки, модули и исправленные ошибки.",
  level_5: "Уровень растёт от опыта: каждый следующий требует больше XP.",
  review_10: "Исправь задания, где ошибся, в «Повторении» → «Работа над ошибками».",
  night_owl: "Реши любое задание ночью — между 00:00 и 05:00.",
};
let tip = null, tipFor = null;
function closeTip() { tip?.remove(); tip = null; tipFor?.classList.remove("open"); tipFor = null; }
function openTip(el) {
  closeTip();
  const d = el.dataset;
  tip = document.createElement("div");
  tip.className = "frz-tip ach-tip";
  tip.innerHTML = `<div class="tip-h">${esc(d.title)}</div><div class="ach-goal">${esc(d.desc)}</div>
    <div class="ach-how">${esc(HOW[d.code] || "")}</div>
    <div class="ach-state ${d.done ? "done" : ""}">${d.done ? `Получено ${esc(d.done)}` : `Прогресс: ${esc(d.prog)}`}</div>`;
  document.body.append(tip);
  const r = el.getBoundingClientRect(), w = tip.offsetWidth;
  const left = Math.min(Math.max(12, r.left + r.width / 2 - w / 2), window.innerWidth - w - 12);
  tip.style.left = `${left + window.scrollX}px`;
  tip.style.top = `${r.bottom + 8 + window.scrollY}px`;
  tip.style.setProperty("--arrow", `${r.left + r.width / 2 - left}px`);
  tipFor = el; el.classList.add("open");
}
document.addEventListener("click", (e) => {
  const b = e.target.closest(".abadge");
  if (b) { tipFor === b ? closeTip() : openTip(b); return; }
  if (tip && !e.target.closest(".ach-tip")) closeTip();
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeTip(); });
window.addEventListener("hashchange", closeTip);

// Значок-«ромб» для экрана наград.
export function achBadge(a) {
  const [icon, [c1, c2]] = LOOK[a.code] || ["star", GREEN];
  const on = !!a.unlocked_at;
  const sub = on ? new Date(a.unlocked_at).toLocaleDateString("ru") : `${a.progress} из ${a.goal}`;
  return `<div class="abadge ${on ? "" : "lock"}" role="button" tabindex="0" style="--b1:${c1};--b2:${c2}"
    data-code="${esc(a.code)}" data-title="${esc(a.title)}" data-desc="${esc(a.description)}"
    data-prog="${a.progress} из ${a.goal}" data-done="${on ? new Date(a.unlocked_at).toLocaleDateString("ru") : ""}">
    <div class="bmedal"><span>${ic(on ? icon : "lock")}</span>${a.goal > 1 ? `<i class="bnum">${short(a.goal)}</i>` : ""}</div>
    <b>${esc(a.title)}</b><small>${esc(on ? a.description : sub)}</small>
    ${on ? "" : `<div class="bar"><i style="width:${Math.round((100 * a.progress) / a.goal)}%"></i></div>`}</div>`;
}

// Маленький значок в ячейке (финал урока, уведомление).
export const achMini = (code) => {
  const [icon, [c1, c2]] = LOOK[code] || ["star", GREEN];
  return `<span class="ach-mini-ico" style="--b1:${c1};--b2:${c2}">${ic(icon)}</span>`;
};
