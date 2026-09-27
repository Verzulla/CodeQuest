// Повторение, награды, статистика, настройки.
import { api, esc, modal, soundOn, sound, plural } from "../util.js";
import { store, setState, pills } from "../store.js";
import { runSession } from "./lesson.js";

// ---------- Повторение ----------
export async function renderReview(view, start) {
  const data = await api("/review");
  if (start && data.exercises.length) {
    return runSession(view, { mode: "review", title: "Повторение", theory: "", color: "var(--blue)", exercises: data.exercises });
  }
  const s = store.state;
  const heartsNote = s.hearts_enabled && s.hearts < s.max_hearts
    ? `<p><b>❤️ Каждый правильный ответ здесь возвращает сердечко.</b></p>` : "";
  let body;
  if (!data.exercises.length) {
    body = `<div class="big">🌱</div><h2>Пока нечего повторять</h2>
      <p class="muted">Реши несколько заданий на карте — сюда попадут твои ошибки и пройденный материал.</p>
      <a class="btn" href="#/">На карту</a>`;
  } else if (data.kind === "mistakes") {
    body = `<div class="big">🩹</div><h2>Работа над ошибками</h2>
      <p class="muted">${data.exercises.length} ${plural(data.exercises.length, "задание ждёт", "задания ждут", "заданий ждут")} реванша.
      За каждую исправленную ошибку — +5 XP. Сердечки здесь не тратятся.</p>${heartsNote}
      <a class="btn blue" href="#/review/start">Начать</a>`;
  } else {
    body = `<div class="big">🏋️</div><h2>Ошибок нет — ты молодец!</h2>
      <p class="muted">Можно закрепить пройденное: ${data.exercises.length} случайных решённых заданий.</p>${heartsNote}
      <a class="btn blue" href="#/review/start">Тренировка</a>`;
  }
  view.innerHTML = `<div class="topbar path-top">${pills()}</div><div class="card empty">${body}</div>`;
}

// ---------- Награды ----------
export async function renderAwards(view) {
  const { achievements, trophies } = await api("/achievements");
  const got = achievements.filter((a) => a.unlocked_at).length;
  view.innerHTML = `
    <h1 class="section-title">🏆 Зал трофеев</h1>
    ${trophies.length ? trophies.map((t) => `
      <div class="card trophy-topic">
        <div class="row"><h2 style="margin:0">${esc(t.icon)} ${esc(t.title)}</h2><div class="spacer"></div>
          <span class="muted">${t.modules.filter((m) => m.earned_at).length} / ${t.modules.length} модулей</span></div>
        <div class="trophy-row">
          ${t.modules.map((m) => medal(m.icon, m.title, m.earned_at)).join("")}
          ${medal("🏆", `Кубок темы`, t.earned_at, "cup")}
        </div>
      </div>`).join("") : `<p class="muted">Тем пока нет.</p>`}
    <h1 class="section-title">🎖️ Достижения <small class="muted">${got} / ${achievements.length}</small></h1>
    <div class="ach-grid">${achievements.map((a) => `
      <div class="card ach ${a.unlocked_at ? "" : "off"}">
        <div class="ai">${esc(a.icon)}</div>
        <div style="flex:1;min-width:0"><b>${esc(a.title)}</b><small class="muted">${esc(a.description)}</small>
          ${a.unlocked_at ? `<div><small style="color:var(--good-text);font-weight:800">✔ ${new Date(a.unlocked_at).toLocaleDateString("ru")}</small></div>`
            : `<div class="bar" style="--c:var(--purple)"><i style="width:${Math.round(100 * a.progress / a.goal)}%"></i></div>
               <small class="muted">${a.progress} / ${a.goal}</small>`}
        </div></div>`).join("")}</div>`;
}

const medal = (icon, title, earned, extra = "") => `
  <div class="medal ${extra} ${earned ? "" : "off"}" title="${earned ? `Получено ${new Date(earned).toLocaleDateString("ru")}` : "Ещё не получено"}">
    <div class="m">${esc(icon)}</div>${esc(title)}</div>`;

// ---------- Статистика ----------
export async function renderStats(view) {
  const d = await api("/stats");
  const st = d.state;
  const max = Math.max(1, ...d.activity.map((a) => a.xp));
  const level = (xp) => (xp === 0 ? 0 : xp < max / 3 ? 1 : xp < (2 * max) / 3 ? 2 : 3);
  const last14 = d.activity.slice(-14);
  const max14 = Math.max(1, ...last14.map((a) => a.xp));
  // выравниваем heatmap так, чтобы столбцы были неделями (пн — первая строка)
  const first = new Date(d.activity[0].day);
  const pad = (first.getDay() + 6) % 7;
  view.innerHTML = `
    <h1 class="section-title">📊 Статистика</h1>
    <div class="stat-grid">
      ${stat("🔥", st.streak, "серия дней")}
      ${stat("🏅", st.longest_streak, "рекорд серии")}
      ${stat("⚡", d.xp, "всего XP")}
      ${stat("🦉", d.level, "уровень")}
      ${stat("✅", d.solved, "заданий решено")}
      ${stat("💻", d.code_solved, "программ написано")}
      ${stat("📘", d.lessons, "уроков пройдено")}
      ${stat("🎯", d.accuracy == null ? "—" : d.accuracy + "%", "точность")}
    </div>
    <div class="card" style="margin-bottom:16px">
      <h3>Активность за 20 недель</h3>
      <div class="heatmap">${"<i style='visibility:hidden'></i>".repeat(pad)}${d.activity.map((a) =>
        `<i data-l="${level(a.xp)}" class="${a.goal_met ? "goal" : ""}" title="${a.day}: ${a.xp} XP${a.goal_met ? " · цель выполнена" : ""}"></i>`).join("")}</div>
      <small class="muted">Золотая рамка — день, когда выполнена дневная цель</small>
    </div>
    <div class="card"><h3>XP за последние 14 дней</h3>
      <div class="xpbars">${last14.map((a, i) => `<div class="${i === 13 ? "today" : ""}" title="${a.day}: ${a.xp} XP">
        ${a.xp || ""}<span style="height:${Math.round((100 * a.xp) / max14)}%"></span>${new Date(a.day).getDate()}</div>`).join("")}</div>
    </div>`;
}

const stat = (icon, value, label) =>
  `<div class="card stat"><div class="si">${icon}</div><div><b>${esc(value)}</b><small>${label}</small></div></div>`;

// ---------- Настройки ----------
const GOALS = [[10, "Легко"], [20, "Нормально"], [30, "Серьёзно"], [50, "Интенсив"], [100, "Хардкор"]];

export function renderSettings(view) {
  const draw = () => {
    const s = store.state;
    view.innerHTML = `<div class="settings">
      <h1 class="section-title">⚙️ Настройки</h1>
      <div class="card"><h3>Дневная цель</h3>
        <div class="choice">${GOALS.map(([xp, name]) =>
          `<button data-goal="${xp}" class="${s.daily_goal === xp ? "on" : ""}">${name}<br><small class="muted">${xp} XP / день</small></button>`).join("")}</div></div>
      <div class="card form">
        <div class="switch"><div><b>🌙 Тёмная тема</b></div><button class="toggle ${s.theme === "dark" ? "on" : ""}" id="theme"></button></div>
        <div class="switch"><div><b>❤️ Сердечки</b><br><small class="muted">Ошибка в уроке стоит сердечко; без сердечек — только повторение. Выключи, если мешает.</small></div>
          <button class="toggle ${s.hearts_enabled ? "on" : ""}" id="hearts"></button></div>
        <div class="switch"><div><b>🔊 Звуки</b></div><button class="toggle ${soundOn() ? "on" : ""}" id="sound"></button></div>
      </div>
      <div class="card form"><h3>🗄️ Данные</h3>
        <p class="muted" style="margin:0">Весь прогресс хранится в базе <code>data/codequest.db</code> — он не пропадёт после перезапуска.
        Чтобы сделать резервную копию, просто скопируй этот файл.</p>
        <div><button class="btn red small" id="reset">Сбросить прогресс</button></div>
      </div></div>`;
    view.querySelectorAll("[data-goal]").forEach((b) => b.onclick = () => save({ daily_goal: Number(b.dataset.goal) }));
    view.querySelector("#theme").onclick = () => save({ theme: s.theme === "dark" ? "light" : "dark" });
    view.querySelector("#hearts").onclick = () => save({ hearts_enabled: !s.hearts_enabled });
    view.querySelector("#sound").onclick = () => {
      localStorage.setItem("cq-sound", soundOn() ? "off" : "on");
      sound("good");
      draw();
    };
    view.querySelector("#reset").onclick = confirmReset;
  };
  const save = async (patch) => { setState(await api("/settings", { method: "PUT", body: patch })); draw(); };
  const confirmReset = () => {
    const m = modal(`<div class="big">⚠️</div><h2>Сбросить весь прогресс?</h2>
      <p class="muted">XP, серия, награды и решённые задания будут удалены. Темы и задания останутся. Это нельзя отменить.</p>
      <input class="input" id="confirm" placeholder="Напиши RESET для подтверждения">
      <div class="btns"><button class="btn red" id="yes" disabled>Сбросить</button><button class="btn ghost" id="no">Отмена</button></div>`);
    const inp = m.root.querySelector("#confirm"), yes = m.root.querySelector("#yes");
    inp.oninput = () => { yes.disabled = inp.value !== "RESET"; };
    m.root.querySelector("#no").onclick = m.close;
    yes.onclick = async () => { setState(await api("/progress/reset", { method: "POST", body: { confirm: "RESET" } })); m.close(); draw(); };
  };
  draw();
}
