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

// Значок-«ромб» для экрана наград.
export function achBadge(a) {
  const [icon, [c1, c2]] = LOOK[a.code] || ["star", GREEN];
  const on = !!a.unlocked_at;
  const sub = on ? new Date(a.unlocked_at).toLocaleDateString("ru") : `${a.progress} из ${a.goal}`;
  return `<div class="abadge ${on ? "" : "lock"}" title="${esc(a.description)}" style="--b1:${c1};--b2:${c2}">
    <div class="bmedal"><span>${ic(on ? icon : "lock")}</span>${a.goal > 1 ? `<i class="bnum">${short(a.goal)}</i>` : ""}</div>
    <b>${esc(a.title)}</b><small>${esc(on ? a.description : sub)}</small>
    ${on ? "" : `<div class="bar"><i style="width:${Math.round((100 * a.progress) / a.goal)}%"></i></div>`}</div>`;
}

// Маленький значок в ячейке (финал урока, уведомление).
export const achMini = (code) => {
  const [icon, [c1, c2]] = LOOK[code] || ["star", GREEN];
  return `<span class="ach-mini-ico" style="--b1:${c1};--b2:${c2}">${ic(icon)}</span>`;
};
