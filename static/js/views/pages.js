// Повторение, награды, статистика, настройки.
import { api, esc, modal, soundOn, sound, plural, toast } from "../util.js";
import { store, setState, pills } from "../store.js";
import { runSession } from "./lesson.js";

// ---------- Повторение ----------
export async function renderReview(view, start) {
  const data = await api("/review");
  const mistakes = data.kind === "mistakes" ? data.exercises : [];
  if (start && mistakes.length) {
    return runSession(view, { mode: "review", title: "Повторение", theory: "", color: "var(--blue)", exercises: mistakes });
  }
  if (start) { location.hash = "#/review"; return; }
  const s = store.state;
  const heartsNote = s.hearts_enabled && s.hearts < s.max_hearts
    ? `<p><b>❤️ Каждый правильный ответ здесь возвращает сердечко.</b></p>` : "";
  const mistakesCard = mistakes.length
    ? `<div class="card empty"><div class="big">🩹</div><h2>Работа над ошибками</h2>
      <p class="muted">${mistakes.length} ${plural(mistakes.length, "задание ждёт", "задания ждут", "заданий ждут")} реванша.
      За каждую исправленную ошибку — +5 XP. Сердечки здесь не тратятся.</p>${heartsNote}
      <a class="btn blue" href="#/review/start">Начать</a></div>`
    : `<div class="card empty"><div class="big">🩹</div><h2>Ошибок нет — ты молодец!</h2>
      <p class="muted">Задания, в которых ты ошибёшься, попадут сюда — чтобы вернуться к ним и исправить.</p></div>`;
  const trainingCard = `<div class="card empty"><div class="big">🏋️</div><h2>Тренировка</h2>
      <p class="muted">Случайные задания из уроков, которые ты уже прошёл, — чтобы закрепить материал.
      Выбираешь темы и сколько заданий решить. Ошибки не тратят сердечки.</p>
      <a class="btn" href="#/training">Настроить тренировку</a></div>`;
  view.innerHTML = `<div class="topbar path-top">${pills()}</div><div style="display:grid;gap:16px">${mistakesCard}${trainingCard}</div>`;
}

// ---------- Тренировка: случайные задания из пройденных уроков выбранных тем ----------
const TRAIN_KEY = "cq-training";       // выбор тем и размер сессии — удобство конкретного браузера
const TRAIN_SIZES = [10, 20, 30];
const TRAIN_MAX = 100;

export async function renderTraining(view) {
  const topics = await api("/training/topics");
  if (!topics.length) {
    view.innerHTML = `<div class="topbar path-top">${pills()}</div><div class="card empty"><div class="big">🌱</div>
      <h2>Пока нечего тренировать</h2><p class="muted">Пройди хотя бы один урок — его задания появятся в тренировке.</p>
      <a class="btn" href="#/">На карту</a></div>`;
    return;
  }
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(TRAIN_KEY) || "{}"); } catch { /* пусто */ }
  const known = new Set(topics.map((t) => t.slug));
  const selected = new Set((saved.topics || []).filter((slug) => known.has(slug)));
  if (!selected.size) topics.forEach((t) => selected.add(t.slug));
  let count = Number.isInteger(saved.count) && saved.count >= 1 ? Math.min(saved.count, TRAIN_MAX) : 10;
  let custom = !TRAIN_SIZES.includes(count);

  const draw = () => {
    const available = topics.filter((t) => selected.has(t.slug)).reduce((a, t) => a + t.available, 0);
    const will = Math.min(count, available);
    view.innerHTML = `<div class="topbar path-top">${pills()}</div>
      <div class="settings">
        <h1 class="section-title">🏋️ Тренировка</h1>
        <div class="card"><div class="row"><h3 style="margin:0">Темы</h3><div class="spacer"></div>
          <button class="btn ghost small" id="all">${selected.size === topics.length ? "Снять все" : "Выбрать все"}</button></div>
          <p class="muted" style="margin:8px 0 12px">Только темы, где пройден хотя бы один урок. Задания берутся из пройденных уроков.</p>
          <div class="choice">${topics.map((t) => `<button data-topic="${esc(t.slug)}" class="${selected.has(t.slug) ? "on" : ""}">
            ${esc(t.icon)} ${esc(t.title)}<br><small class="muted">${t.available} ${plural(t.available, "задание", "задания", "заданий")}</small></button>`).join("")}</div></div>
        <div class="card"><h3>Сколько заданий</h3>
          <div class="choice">${TRAIN_SIZES.map((n) => `<button data-size="${n}" class="${!custom && count === n ? "on" : ""}">${n}</button>`).join("")}
            <button data-size="custom" class="${custom ? "on" : ""}">Своё</button></div>
          ${custom ? `<label style="display:block;margin-top:12px">Количество (1–${TRAIN_MAX})
            <input class="input" id="custom" type="number" min="1" max="${TRAIN_MAX}" value="${count}" inputmode="numeric"></label>` : ""}
        </div>
        <div class="card empty">
          <p class="muted" style="margin:0 0 12px">${available
            ? `Будет ${will} ${plural(will, "задание", "задания", "заданий")} вперемешку${will < count ? ` — в выбранных темах пока столько решённых` : ""}. Ошибки не тратят сердечки, правильный ответ — +2 XP. Кнопка 📖 — шпаргалка урока.`
            : "Выбери хотя бы одну тему."}</p>
          <button class="btn blue wide" id="start" ${available ? "" : "disabled"}>Начать тренировку</button>
        </div>
      </div>`;
    view.querySelectorAll("[data-topic]").forEach((b) => b.onclick = () => {
      const slug = b.dataset.topic;
      selected.has(slug) ? selected.delete(slug) : selected.add(slug);
      draw();
    });
    view.querySelector("#all").onclick = () => {
      if (selected.size === topics.length) selected.clear(); else topics.forEach((t) => selected.add(t.slug));
      draw();
    };
    view.querySelectorAll("[data-size]").forEach((b) => b.onclick = () => {
      if (b.dataset.size === "custom") { custom = true; draw(); view.querySelector("#custom").focus(); return; }
      custom = false; count = Number(b.dataset.size); draw();
    });
    const input = view.querySelector("#custom");
    if (input) input.onchange = () => {
      const v = Math.round(Number(input.value));
      count = Number.isFinite(v) ? Math.min(TRAIN_MAX, Math.max(1, v)) : 10;
      draw();
    };
    view.querySelector("#start").onclick = start;
  };

  const start = async () => {
    const input = view.querySelector("#custom");
    if (input) count = Math.min(TRAIN_MAX, Math.max(1, Math.round(Number(input.value)) || 10));
    try { localStorage.setItem(TRAIN_KEY, JSON.stringify({ topics: [...selected], count })); } catch { /* ок */ }
    const btn = view.querySelector("#start");
    btn.disabled = true;
    try {
      const r = await api("/training/start", { method: "POST", body: { topics: [...selected], count } });
      runSession(view, { mode: "training", title: "Тренировка", color: "var(--purple)", exercises: r.exercises });
    } catch (e) {
      btn.disabled = false;
      toast("⚠️", "Не удалось начать", e.message);
    }
  };
  draw();
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

// ---------- Установка на телефон (PWA) ----------
const isStandalone = () => matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
const isIOS = () => !/android/i.test(navigator.userAgent)
  && (/iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1));  // iPadOS притворяется Mac

function installCard() {
  let body;
  if (isStandalone()) {
    body = `<p style="margin:0">✅ CodeQuest открыт как приложение.</p>`;
  } else if (window.cqInstallPrompt) {
    body = `<p class="muted" style="margin:0">Иконка на главном экране, запуск без адресной строки — как обычное приложение.</p>
      <div><button class="btn small" id="install">Установить приложение</button></div>`;
  } else if (isIOS()) {
    body = `<p class="muted" style="margin:0">Открой сайт в <b>Safari</b>, нажми <b>«Поделиться»</b> (квадрат со стрелкой вверх) и выбери
      <b>«На экран „Домой“»</b>. CodeQuest появится среди приложений. Войти в аккаунт нужно будет один раз заново.</p>`;
  } else {
    body = `<p class="muted" style="margin:0">На телефоне открой сайт в <b>Chrome</b> и выбери в меню <b>⋮ → «Установить приложение»</b>
      (или «Добавить на главный экран»).</p>`;
  }
  return `<div class="card form"><h3>📱 Приложение на телефоне</h3>${body}</div>`;
}

// ---------- Настройки: администраторы (видно только администратору) ----------
function bindAdmins(view) {
  const form = view.querySelector("#admins-form");
  const list = view.querySelector("#admins-list");
  const err = view.querySelector("#admins-error");
  const fail = (msg) => { err.textContent = msg; err.hidden = false; };
  const load = async () => {
    try {
      const admins = (await api("/admin/users")).filter((x) => x.is_admin);
      list.innerHTML = admins.map((a) => `<div class="account-row" style="padding:4px 0">
          <div style="flex:1;min-width:0"><b>${esc(a.username)}</b>${a.username === store.user.username ? ` <small class="muted">(это ты)</small>` : ""}</div>
          ${a.username === store.user.username ? "" : `<button class="btn ghost small" type="button" data-revoke="${esc(a.username)}">Снять права</button>`}
        </div>`).join("");
      list.querySelectorAll("[data-revoke]").forEach((b) => b.onclick = () => setRole(b.dataset.revoke, false));
    } catch (e) { list.textContent = e.message; }
  };
  const setRole = async (username, isAdmin) => {
    err.hidden = true;
    try {
      const r = await api("/admin/users/role", { method: "POST", body: { username, is_admin: isAdmin } });
      toast("🛡️", r.username, isAdmin ? "Теперь администратор" : "Права администратора сняты");
      form.username.value = "";
      load();
    } catch (e) { fail(e.message); }
  };
  form.onsubmit = (e) => {
    e.preventDefault();
    const name = form.username.value.trim();
    if (!name) return fail("Введи ник пользователя");
    setRole(name, true);
  };
  load();
}

// ---------- Настройки ----------
const GOALS = [[10, "Легко"], [20, "Нормально"], [30, "Серьёзно"], [50, "Интенсив"], [100, "Хардкор"]];

export function renderSettings(view) {
  const draw = () => {
    const s = store.state, u = store.user;
    view.innerHTML = `<div class="settings">
      <h1 class="section-title">⚙️ Настройки</h1>
      <div class="card"><h3>Дневная цель</h3>
        <div class="choice">${GOALS.map(([xp, name]) =>
          `<button data-goal="${xp}" class="${s.daily_goal === xp ? "on" : ""}">${name}<br><small class="muted">${xp} XP / день</small></button>`).join("")}</div></div>
      <div class="card form">
        <div class="switch"><div><b>🌙 Тёмная тема</b></div><button class="toggle ${s.theme === "dark" ? "on" : ""}" id="theme"></button></div>
        <div class="switch"><div><b>❤️ Сердечки</b><br><small class="muted">Ошибка в уроке стоит сердечко; без сердечек — только повторение. Выключи, если мешает.</small></div>
          <button class="toggle ${s.hearts_enabled ? "on" : ""}" id="hearts"></button></div>
        <div class="switch"><div><b>🔒 Уроки по порядку</b><br><small class="muted">Следующий урок темы открывается после прохождения предыдущего. Выключи, чтобы открывать любой урок сразу.</small></div>
          <button class="toggle ${s.sequential_lessons ? "on" : ""}" id="sequential"></button></div>
        <div class="switch"><div><b>🔊 Звуки</b></div><button class="toggle ${soundOn() ? "on" : ""}" id="sound"></button></div>
      </div>
      ${installCard()}
      <div class="card form"><h3>👤 Аккаунт</h3>
        <div class="account-row">
          <div class="avatar">${esc(u.username[0].toUpperCase())}</div>
          <div style="flex:1;min-width:0"><b>${esc(u.username)}</b>${u.is_admin ? ` <span class="chip">администратор</span>` : ""}
            <br><small class="muted">Прогресс хранится на сервере в твоём аккаунте — войди с любого устройства.</small></div>
          <button class="btn ghost small" id="logout">Выйти</button>
        </div>
      </div>
      ${u.is_admin ? `<form class="card form" id="admins-form" novalidate><h3>🛡️ Администраторы</h3>
        <p class="muted" style="margin:0">Администратор может менять контент в разделе «Контент» и назначать других администраторов.</p>
        <div class="row" style="gap:10px;flex-wrap:wrap">
          <input class="input" name="username" placeholder="Ник пользователя" maxlength="64" autocomplete="off" style="flex:1;min-width:160px">
          <button class="btn blue small" type="submit">Сделать администратором</button></div>
        <p class="auth-error" id="admins-error" hidden></p>
        <div id="admins-list" class="muted">Загрузка…</div>
      </form>` : ""}
      <form class="card form" id="pw-form" novalidate><h3>🔑 Смена пароля</h3>
        <label>Текущий пароль<input class="input" type="password" name="current" autocomplete="current-password" maxlength="128"></label>
        <label>Новый пароль<small>Не меньше 6 символов. На других устройствах придётся войти заново.</small>
          <input class="input" type="password" name="next" autocomplete="new-password" maxlength="128"></label>
        <label>Повтори новый пароль<input class="input" type="password" name="next2" autocomplete="new-password" maxlength="128"></label>
        <p class="auth-error" id="pw-error" hidden></p>
        <div><button class="btn blue small" type="submit">Сменить пароль</button></div>
      </form>
      <div class="card form"><h3>⚠️ Опасная зона</h3>
        <p class="muted" style="margin:0">Сброс прогресса обнулит XP, серию, награды и решённые задания. Удаление аккаунта сотрёт аккаунт вместе со всем прогрессом.</p>
        <div class="row" style="gap:10px;flex-wrap:wrap"><button class="btn red small" id="reset">Сбросить прогресс</button>
          <button class="btn red small" id="delete">Удалить аккаунт</button></div>
      </div></div>`;
    view.querySelectorAll("[data-goal]").forEach((b) => b.onclick = () => save({ daily_goal: Number(b.dataset.goal) }));
    view.querySelector("#theme").onclick = () => save({ theme: s.theme === "dark" ? "light" : "dark" });
    view.querySelector("#hearts").onclick = () => save({ hearts_enabled: !s.hearts_enabled });
    view.querySelector("#sequential").onclick = () => save({ sequential_lessons: !s.sequential_lessons });
    view.querySelector("#sound").onclick = () => {
      localStorage.setItem("cq-sound", soundOn() ? "off" : "on");
      sound("good");
      draw();
    };
    view.querySelector("#reset").onclick = confirmReset;
    view.querySelector("#delete").onclick = confirmDelete;
    const install = view.querySelector("#install");
    if (install) install.onclick = async () => {
      const prompt = window.cqInstallPrompt;
      if (!prompt) return;
      prompt.prompt();
      await prompt.userChoice.catch(() => {});
      window.cqInstallPrompt = null;
      draw();
    };
    view.querySelector("#logout").onclick = async () => {
      await api("/auth/logout", { method: "POST" }).catch(() => {});
      window.dispatchEvent(new Event("cq:unauthorized"));
    };
    if (u.is_admin) bindAdmins(view);
    const pw = view.querySelector("#pw-form");
    pw.onsubmit = async (e) => {
      e.preventDefault();
      const err = view.querySelector("#pw-error");
      const fail = (msg) => { err.textContent = msg; err.hidden = false; };
      if (!pw.current.value || !pw.next.value) return fail("Заполни текущий и новый пароль");
      if (pw.next.value !== pw.next2.value) return fail("Новые пароли не совпадают");
      try {
        await api("/account/password", { method: "PUT", body: { current_password: pw.current.value, new_password: pw.next.value } });
        pw.reset();
        err.hidden = true;
        toast("🔑", "Пароль изменён", "Другие устройства вышли из аккаунта");
      } catch (e2) { fail(e2.message); }
    };
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
  const confirmDelete = () => {
    const m = modal(`<div class="big">🗑️</div><h2>Удалить аккаунт «${esc(store.user.username)}»?</h2>
      <p class="muted">Аккаунт и весь прогресс будут стёрты безвозвратно. Ник освободится.</p>
      <input class="input" id="pwd" type="password" placeholder="Введи пароль для подтверждения" autocomplete="current-password">
      <p class="auth-error" id="del-error" hidden></p>
      <div class="btns"><button class="btn red" id="yes" disabled>Удалить навсегда</button><button class="btn ghost" id="no">Отмена</button></div>`);
    const inp = m.root.querySelector("#pwd"), yes = m.root.querySelector("#yes"), err = m.root.querySelector("#del-error");
    inp.focus();
    inp.oninput = () => { yes.disabled = !inp.value; };
    m.root.querySelector("#no").onclick = m.close;
    yes.onclick = async () => {
      yes.disabled = true;
      try {
        await api("/account/delete", { method: "POST", body: { password: inp.value } });
        m.close();
        window.dispatchEvent(new Event("cq:unauthorized"));
      } catch (e) { err.textContent = e.message; err.hidden = false; yes.disabled = false; }
    };
  };
  // предложение установки может прийти уже после открытия настроек
  const onInstallable = () => { if (document.body.contains(view.firstElementChild)) draw(); };
  window.addEventListener("cq:installable", onInstallable, { once: true });
  draw();
}
