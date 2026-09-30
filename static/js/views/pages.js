// Повторение, награды, статистика, настройки.
import { api, esc, modal, soundOn, sound, plural, toast, ic, owl } from "../util.js";
import { store, setState, pills, weekRow, freezeBox } from "../store.js";
import { runSession } from "./lesson.js";
import { glyph } from "../glyphs.js";
import { achBadge } from "../achievements.js";

// ---------- Повторение ----------
const KIND = { code: ["code", "Напиши код"], command: ["term", "Терминал"], output: ["eye", "Что выведет"] };
// Заголовок задания — первая строка условия без markdown.
const promptTitle = (p) => {
  const line = String(p || "").split("\n").find((x) => x.trim()) || "Задание";
  const t = line.replace(/^#+\s*/, "").replace(/[*_`]/g, "").trim();
  return t.length > 70 ? `${t.slice(0, 68)}…` : t;
};

export async function renderReview(view, start) {
  const data = await api("/review");
  const mistakes = data.kind === "mistakes" ? data.exercises : [];
  if (start && mistakes.length) {
    return runSession(view, { mode: "review", title: "Повторение", theory: "", color: "var(--red)", exercises: mistakes });
  }
  if (start) { location.hash = "#/review"; return; }
  const s = store.state;
  const items = data.items || [];
  const total = items.length;
  const lost = items.reduce((a, it) => a + (it.hearts_lost || 0), 0);
  const back = s.hearts_enabled ? Math.min(lost, s.max_hearts - s.hearts) : 0;
  const heart = ic("heart");
  const mistakesCard = total
    ? `<div class="card rv-card bad">${owl("sad", "breathe")}
        <div class="kind">Работа над ошибками</div>
        <div class="rv-big">${total} ${plural(total, "задание", "задания", "заданий")}</div>
        <div class="muted rv-sub">ждут реванша${back ? ` · вернёшь до <b class="hl">${back} ${heart}</b>` : ""} и +${data.fix_xp * total} XP</div>
        ${total > mistakes.length ? `<div class="muted rv-note">За один подход — до ${mistakes.length} заданий</div>` : ""}
        <a class="btn" href="#/review/start">Исправить</a></div>`
    : `<div class="card rv-card good">${owl("happy", "bob")}
        <div class="kind">Работа над ошибками</div>
        <div class="rv-big">Ошибок нет</div>
        <div class="muted rv-sub">Задания, в которых ошибёшься, попадут сюда — чтобы вернуться и исправить. Исправленное возвращает сердечки.</div></div>`;
  const trainingCard = `<div class="card rv-card">${owl("think", "tilt")}
      <div class="kind">Тренировка</div>
      <div class="rv-mid">Закрепи пройденное</div>
      <div class="muted rv-sub">Случайные задания из выбранных тем — пройденных и новых (разминка). Ошибки не тратят сердечки.</div>
      <a class="btn ghost" href="#/training">Настроить</a></div>`;
  const hearts = s.hearts_enabled
    ? `<div class="card rv-chip"><span class="muted">Сердечки</span>${ic("heart").repeat(s.hearts)}${ic("heartE").repeat(s.max_hearts - s.hearts)}</div>` : "";
  const list = total ? `<h3 class="rv-sec">Ошибки</h3>
    <div class="card rv-list">${items.map((it) => {
      const [icon, label] = KIND[it.type] || KIND.output;
      const gain = s.hearts_enabled && it.hearts_lost
        ? `<span class="rv-gain hearts">+${it.hearts_lost}${heart}</span>` : `<span class="rv-gain">+${data.fix_xp} XP</span>`;
      return `<div class="rv-row"><span class="rv-ico ${it.type}">${ic(icon)}</span>
        <div class="rv-body"><b>${esc(promptTitle(it.prompt))}</b><small class="muted">${esc(it.topic_title)} · ${esc(it.lesson_title)}</small></div>
        <span class="muted rv-type">${label}</span><span class="rv-count" title="Ошибок">${it.mistakes}×</span>${gain}</div>`;
    }).join("")}</div>` : "";
  view.innerHTML = `<div class="topbar path-top">${pills()}</div>
    <div class="rv-head"><h1 class="section-title">Повторение</h1><div class="spacer"></div>${hearts}
      <div class="card rv-chip"><span class="muted">Исправлено</span><b>${data.fixed}</b></div></div>
    <div class="rv-grid">${mistakesCard}${trainingCard}</div>${list}`;
}

// ---------- Тренировка: случайные задания из пройденных уроков выбранных тем ----------
const TRAIN_KEY = "cq-training";       // выбор тем и размер сессии — удобство конкретного браузера
const TRAIN_SIZES = [10, 20, 30];
const TRAIN_MAX = 100;

export async function renderTraining(view) {
  const topics = await api("/training/topics");
  const passed = topics.filter((t) => t.passed);
  const fresh = topics.filter((t) => !t.passed);
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(TRAIN_KEY) || "{}"); } catch { /* пусто */ }
  const known = new Set(topics.map((t) => t.slug));
  const selected = new Set((saved.topics || []).filter((slug) => known.has(slug)));
  if (!selected.size) passed.forEach((t) => selected.add(t.slug));   // по умолчанию — все пройденные
  let unfinished = saved.include_unfinished === true;
  let count = Number.isInteger(saved.count) && saved.count >= 1 ? Math.min(saved.count, TRAIN_MAX) : 10;
  let custom = !TRAIN_SIZES.includes(count);

  // Сколько заданий даст тема при текущих настройках и сколько из них — разминка (не засчитывается).
  const tasksOf = (t) => (!t.passed || unfinished ? t.total : t.available);
  const warmupOf = (t) => (!t.passed ? t.total : unfinished ? t.total - t.available : 0);
  const n = (k) => `${k} ${plural(k, "задание", "задания", "заданий")}`;
  const topicBtn = (t) => `<button data-topic="${esc(t.slug)}" class="topic-pick ${selected.has(t.slug) ? "on" : ""}">
      ${glyph(t, 34)}<span><b>${esc(t.title)}</b><small class="muted">${n(tasksOf(t))}</small></span>${selected.has(t.slug) ? ic("okc", "tick") : ""}</button>`;
  const allBtn = (list, id) => list.length
    ? `<button class="btn ghost small" id="${id}">${list.every((t) => selected.has(t.slug)) ? "Снять все" : "Выбрать все"}</button>` : "";

  const draw = () => {
    // Экран перерисовывается целиком — сохраняем прокрутку списка тем и страницы, чтобы клик не сбивал её.
    const listScroll = view.querySelector(".train-scroll")?.scrollTop || 0;
    const pageScroll = window.scrollY;
    const chosen = topics.filter((t) => selected.has(t.slug));
    const available = chosen.reduce((a, t) => a + tasksOf(t), 0);
    const warmup = chosen.reduce((a, t) => a + warmupOf(t), 0);
    const will = Math.min(count, available);
    view.innerHTML = `<div class="topbar path-top">${pills()}</div>
      <div class="settings">
        <div class="rv-head"><a class="icon-btn" href="#/review" title="К повторению">${ic("back")}</a><h1 class="section-title">Тренировка</h1></div>
        <div class="card"><h3 style="margin-top:0">Темы</h3>
          <div class="row"><b>Пройденные</b><div class="spacer"></div>${allBtn(passed, "all-passed")}</div>
          <p class="muted" style="margin:6px 0 12px">Темы, где пройден хотя бы один урок. Задания — из пройденных уроков.</p>
          ${passed.length ? `<div class="choice topic-choice">${passed.map(topicBtn).join("")}</div>
            <label class="check-row"><input type="checkbox" id="unfinished" ${unfinished ? "checked" : ""}>
              <span><b>Включать непройденные уроки этих тем</b><br><small class="muted">Их задания — разминка: не засчитываются</small></span></label>`
            : `<p class="muted" style="margin:0">Пока нет — пройди хотя бы один урок.</p>`}
          <div class="train-sep"></div>
          <div class="row"><b>Ещё не пройденные</b><div class="spacer"></div>${allBtn(fresh, "all-fresh")}</div>
          <p class="muted" style="margin:6px 0 12px">Разминка на новом материале: задания из любых уроков темы. Не засчитываются — прогресс уроков не меняется.</p>
          ${fresh.length ? `<div class="choice topic-choice train-scroll">${fresh.map(topicBtn).join("")}</div>` : `<p class="muted" style="margin:0">Все темы уже начаты.</p>`}
        </div>
        <div class="card"><h3>Сколько заданий</h3>
          <p class="muted" style="margin:-4px 0 12px">В выбранных темах доступно <b>${available}</b> ${plural(available, "задание", "задания", "заданий")}.</p>
          <div class="choice">${TRAIN_SIZES.map((k) => `<button data-size="${k}" class="${!custom && count === k ? "on" : ""} ${k > available ? "dim" : ""}"
            ${k > available ? `title="Сейчас доступно только ${available}"` : ""}>${k}</button>`).join("")}
            <button data-size="custom" class="${custom ? "on" : ""}">Своё</button></div>
          ${custom ? `<label style="display:block;margin-top:12px">Количество (1–${TRAIN_MAX})
            <input class="input" id="custom" type="number" min="1" max="${TRAIN_MAX}" value="${count}" inputmode="numeric"></label>` : ""}
        </div>
        <div class="card empty">
          <p class="muted" style="margin:0 0 12px">${available
            ? `${will < count
                ? `Выбрано ${count}, а заданий в этих темах пока ${available} — тренировка будет из ${will}. Добавь темы или пройди больше уроков, и выбор вырастет.<br>`
                : `Будет ${n(will)} вперемешку. `}${warmup ? `Из них могут попасться задания разминки — они не засчитываются. ` : ""}Ошибки не тратят сердечки, правильный ответ — +2 XP. Книжка вверху — шпаргалка урока.`
            : "Выбери хотя бы одну тему."}</p>
          <button class="btn blue wide" id="start" ${available ? "" : "disabled"}>Начать тренировку</button>
        </div>
      </div>`;
    view.querySelectorAll("[data-topic]").forEach((b) => b.onclick = () => {
      const slug = b.dataset.topic;
      selected.has(slug) ? selected.delete(slug) : selected.add(slug);
      draw();
    });
    const toggleAll = (list) => {
      if (list.every((t) => selected.has(t.slug))) list.forEach((t) => selected.delete(t.slug));
      else list.forEach((t) => selected.add(t.slug));
      draw();
    };
    view.querySelector("#all-passed")?.addEventListener("click", () => toggleAll(passed));
    view.querySelector("#all-fresh")?.addEventListener("click", () => toggleAll(fresh));
    view.querySelector("#unfinished")?.addEventListener("change", (e) => { unfinished = e.target.checked; draw(); });
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
    const list = view.querySelector(".train-scroll");
    if (list) list.scrollTop = listScroll;
    window.scrollTo(0, pageScroll);
  };

  const start = async () => {
    const input = view.querySelector("#custom");
    if (input) count = Math.min(TRAIN_MAX, Math.max(1, Math.round(Number(input.value)) || 10));
    try {
      localStorage.setItem(TRAIN_KEY, JSON.stringify({ topics: [...selected], count, include_unfinished: unfinished }));
    } catch { /* ок */ }
    const btn = view.querySelector("#start");
    btn.disabled = true;
    try {
      const r = await api("/training/start", { method: "POST", body: { topics: [...selected], count, include_unfinished: unfinished } });
      runSession(view, { mode: "training", title: "Тренировка", color: "var(--purple)", exercises: r.exercises });
    } catch (e) {
      btn.disabled = false;
      toast("warn", "Не удалось начать", e.message);
    }
  };
  draw();
}

// ---------- Награды (вариант B: зал трофеев по темам) ----------
export async function renderAwards(view) {
  const { achievements, trophies } = await api("/achievements");
  const got = achievements.filter((a) => a.unlocked_at).length;
  const cups = trophies.filter((t) => t.earned_at).length;
  const medals = trophies.reduce((n, t) => n + t.modules.filter((m) => m.earned_at).length, 0);
  const medalChip = (m) => `<span class="medal-chip ${m.earned_at ? "" : "off"}" title="${m.earned_at ? `Получено ${new Date(m.earned_at).toLocaleDateString("ru")}` : "Ещё не получено"}">${m.earned_at ? ic("medalI") : ""}${esc(m.title)}</span>`;
  const topicCard = (t) => {
    const n = t.modules.filter((m) => m.earned_at).length;
    const state = t.earned_at ? "done" : n ? "going" : "new";
    const head = t.earned_at ? `<span class="aw-cup">${ic("cup")}</span>` : glyph(t, 40);
    const sub = t.earned_at ? "тема пройдена" : n ? `${n} из ${t.modules.length} ${plural(t.modules.length, "модуля", "модулей", "модулей")}` : "ещё нет медалей";
    return `<a class="card aw-topic ${state}" href="#/topic/${t.id}" style="--tc:${esc(t.color)}">
      <div class="aw-row">${head}<div class="aw-name"><b>${esc(t.title)}</b><small class="muted">${sub}</small></div></div>
      ${state === "new" ? "" : `<div class="aw-medals">${t.modules.map(medalChip).join("")}</div>`}</a>`;
  };
  const started = trophies.filter((t) => t.earned_at || t.modules.some((m) => m.earned_at));
  const ahead = trophies.filter((t) => !started.includes(t));
  view.innerHTML = `<div class="topbar path-top">${pills()}</div>
    <div class="card aw-hero">${owl("trophy", "hop")}
      <div class="kind">Зал трофеев</div>
      <div class="aw-nums">
        <div><b>${cups}</b><small>${plural(cups, "кубок", "кубка", "кубков")} за темы</small></div>
        <div><b>${medals}</b><small>${plural(medals, "медаль", "медали", "медалей")} за модули</small></div>
        <div><b>${got}<span> / ${achievements.length}</span></b><small>достижений</small></div>
      </div></div>
    <h3 class="rv-sec">Темы</h3>
    ${started.length ? `<div class="aw-grid">${started.map(topicCard).join("")}</div>`
      : `<p class="muted">Медали выдаются за пройденные модули, кубок — за всю тему. Пройди все уроки первого модуля — и здесь появится первая медаль.</p>`}
    <h3 class="rv-sec">Достижения <small class="muted">${got} / ${achievements.length}</small></h3>
    <div class="badges">${[...achievements].sort((x, y) => !!y.unlocked_at - !!x.unlocked_at).map(achBadge).join("")}</div>
    ${ahead.length ? `<h3 class="rv-sec">Впереди <small class="muted">${ahead.length} ${plural(ahead.length, "тема", "темы", "тем")} без медалей</small></h3>
      <div class="aw-ahead">${ahead.map((t) => `<a href="#/topic/${t.id}" title="${esc(t.title)}">${glyph(t, 38)}<span>${esc(t.title)}</span></a>`).join("")}</div>` : ""}`;
}

// ---------- Статистика ----------
const ACTIVITY_PERIODS = [[30, "Месяц"], [91, "3 месяца"], [182, "Полгода"], [365, "Год"]];
const ACTIVITY_KEY = "cq-activity-period";

export async function renderStats(view) {
  const d = await api("/stats");
  const st = d.state;
  let period = 91;
  try { period = Number(localStorage.getItem(ACTIVITY_KEY)) || 91; } catch { /* ок */ }
  if (!ACTIVITY_PERIODS.some(([days]) => days === period)) period = 91;
  const last14 = d.activity.slice(-14);
  const max14 = Math.max(1, ...last14.map((a) => a.xp));

  // Календарь за выбранный период: столбец — неделя (пн — первая строка), яркость — относительно максимума периода.
  const heatmap = () => {
    const days = d.activity.slice(-period);
    const max = Math.max(1, ...days.map((a) => a.xp));
    const level = (xp) => (xp === 0 ? 0 : xp < max / 3 ? 1 : xp < (2 * max) / 3 ? 2 : 3);
    const pad = (new Date(days[0].day).getDay() + 6) % 7;
    const active = days.filter((a) => a.xp > 0).length;
    const goals = days.filter((a) => a.goal_met).length;
    const frozen = days.filter((a) => a.frozen).length;
    const cell = period <= 30 ? 32 : period <= 91 ? 24 : 14;   // короткий период — клетки крупнее
    return `<div class="heatmap" style="--cell:${cell}px">${"<i style='visibility:hidden'></i>".repeat(pad)}${days.map((a) =>
      a.frozen ? `<i class="fz" title="${a.day}: спасено заморозкой"></i>`
        : `<i data-l="${level(a.xp)}" class="${a.goal_met ? "goal" : ""}" title="${a.day}: ${a.xp} XP${a.goal_met ? " · цель выполнена" : ""}"></i>`).join("")}</div>
      <div class="hm-legend"><span><i class="l3"></i>занимался</span><span><i class="goal"></i>цель выполнена</span><span><i class="fz"></i>спасено заморозкой</span><span><i></i>пропуск</span></div>
      <small class="muted">Активных дней: <b>${active}</b> из ${days.length} · цель выполнена: <b>${goals}</b>${frozen ? ` · спасено заморозкой: <b>${frozen}</b>` : ""}.</small>`;
  };

  const avg14 = Math.round(last14.reduce((n, a) => n + a.xp, 0) / 14);
  const num = (n) => Number(n).toLocaleString("ru-RU");
  view.innerHTML = `<div class="topbar path-top">${pills()}</div>
    <h1 class="section-title">Статистика</h1>
    <div class="st-top">
      <div class="card st-streak ${st.streak ? "" : "cold"}">
        <svg class="i st-flame ${st.streak ? "glowP" : ""}"><use href="#ic-flame"/></svg>
        <div class="st-days">${st.streak}</div>
        <div class="st-days-l">${plural(st.streak, "день", "дня", "дней")} подряд</div>
        ${weekRow(st)}
        <div class="muted st-rec">Рекорд ${st.longest_streak} ${plural(st.longest_streak, "день", "дня", "дней")}</div>
        ${freezeBox(st)}
      </div>
      <div class="st-grid">
        ${rec("Всего XP", num(d.xp), "#ffd54a")}${rec("Уровень", d.level, "#c68bff")}
        ${rec("Точность", d.accuracy == null ? "—" : d.accuracy + "%", "#9be84a")}${rec("Заданий решено", num(d.solved))}
        ${rec("Программ написано", num(d.code_solved))}${rec("Уроков пройдено", num(d.lessons))}
      </div>
    </div>
    <div class="card st-card">
      <div class="row st-head"><b>Активность</b><div class="spacer"></div>
        <div class="seg-switch">${ACTIVITY_PERIODS.map(([days, label]) =>
          `<button data-period="${days}" class="${days === period ? "on" : ""}">${label}</button>`).join("")}</div></div>
      <div id="heat">${heatmap()}</div>
    </div>
    <div class="card st-card"><div class="row st-head"><b>XP за 14 дней</b><div class="spacer"></div><span class="muted" style="font-size:12.5px">в среднем ${avg14} в день</span></div>
      <div class="xpbars">${last14.map((a, i) => `<div class="${i === 13 ? "today" : ""}" title="${a.day}: ${a.xp} XP">
        ${a.xp || ""}<span style="height:${Math.round((100 * a.xp) / max14)}%"></span>${new Date(a.day).getDate()}</div>`).join("")}</div>
    </div>`;
  view.querySelectorAll("[data-period]").forEach((b) => b.onclick = () => {
    period = Number(b.dataset.period);
    try { localStorage.setItem(ACTIVITY_KEY, String(period)); } catch { /* ок */ }
    view.querySelectorAll("[data-period]").forEach((x) => x.classList.toggle("on", x === b));
    view.querySelector("#heat").innerHTML = heatmap();
    const hm = view.querySelector(".heatmap");
    hm.scrollLeft = hm.scrollWidth;          // длинный календарь — сразу к свежим неделям
  });
  const hm = view.querySelector(".heatmap");
  hm.scrollLeft = hm.scrollWidth;
}

const rec = (label, value, color = "") =>
  `<div class="card st-rec-card"><small>${label}</small><b${color ? ` style="color:${color}"` : ""}>${esc(value)}</b></div>`;

// ---------- Установка на телефон (PWA) ----------
const isStandalone = () => matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
const isIOS = () => !/android/i.test(navigator.userAgent)
  && (/iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1));  // iPadOS притворяется Mac

function installCard() {
  let body;
  if (isStandalone()) {
    body = `<small class="muted">CodeQuest уже открыт как приложение</small>`;
  } else if (window.cqInstallPrompt) {
    body = `<small class="muted">Иконка на главном экране, запуск без адресной строки</small>`;
  } else if (isIOS()) {
    body = `<small class="muted">В Safari: «Поделиться» → «На экран „Домой“». Войти нужно будет один раз заново</small>`;
  } else {
    body = `<small class="muted">На телефоне в Chrome: меню ⋮ → «Установить приложение»</small>`;
  }
  return `<div class="card set-row">${ic("phone", "si")}<div class="grow"><b>Приложение на телефоне</b>${body}</div>
    ${window.cqInstallPrompt && !isStandalone() ? `<button class="btn small" id="install">Установить</button>` : ""}</div>`;
}

// ---------- Настройки: администраторы (видно только администратору) ----------
function bindAdmins(root) {
  const form = root.querySelector("#admins-form");
  const list = root.querySelector("#admins-list");
  const err = root.querySelector("#admins-error");
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
      toast("shield", r.username, isAdmin ? "Теперь администратор" : "Права администратора сняты");
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

// ---------- Настройки (вариант B: визуальные карточки) ----------
const GOALS = [[10, "легко"], [20, "норм"], [30, "серьёзно"], [50, "интенсив"], [100, "хардкор"]];
const toggle = (id, on) => `<button class="toggle ${on ? "on" : ""}" id="${id}" role="switch" aria-checked="${on}"></button>`;
const setRow = (icon, title, sub, right, cls = "") =>
  `<div class="card set-row ${cls}">${icon}<div class="grow"><b>${title}</b>${sub ? `<small class="muted">${sub}</small>` : ""}</div>${right}</div>`;
const ZIG = `<svg viewBox="0 0 160 80" class="pv-svg"><path d="M80 8 C 120 20, 120 34, 94 42 S 40 60, 74 74" stroke="currentColor" stroke-opacity=".25" stroke-width="3" fill="none" stroke-dasharray="1 7" stroke-linecap="round"/><circle cx="80" cy="10" r="9" class="pv-on"/><circle cx="102" cy="38" r="9" class="pv-on"/><circle cx="70" cy="66" r="9" class="pv-off"/></svg>`;
const LST = `<svg viewBox="0 0 160 80" class="pv-svg"><rect x="10" y="6" width="140" height="18" rx="6" class="pv-on" opacity=".6"/><rect x="10" y="30" width="140" height="18" rx="6" class="pv-off"/><rect x="10" y="54" width="140" height="18" rx="6" class="pv-off" opacity=".6"/></svg>`;

export function renderSettings(view) {
  const draw = () => {
    const s = store.state, u = store.user;
    const chev = ic("arrowR", "chev");
    view.innerHTML = `<div class="topbar path-top">${pills()}</div>
      <h1 class="section-title">Настройки</h1>
      <div class="settings set-grid">
      <div class="set-col">
        <div class="card set-profile"><div class="avatar">${esc(u.username[0].toUpperCase())}</div>
          <div class="grow"><b>${esc(u.username)}</b><small class="muted">${u.is_admin ? "администратор · " : ""}уровень ${s.level}</small></div>
          <button class="btn ghost small" id="logout">${ic("logout")}Выйти</button></div>
        <div class="card mob-links">
          <a href="#/about">${ic("i-info")}<span>О приложении</span>${chev}</a>
          ${u.is_admin ? `<a href="#/admin">${ic("wrench")}<span>Контент</span>${chev}</a>` : ""}
        </div>
        <h3 class="set-sec">Дневная цель</h3>
        <div class="goal-tiles">${GOALS.map(([xp, name]) =>
          `<button data-goal="${xp}" class="card ${s.daily_goal === xp ? "on" : ""}"><b>${xp}</b><small>${name}</small></button>`).join("")}</div>
        <small class="muted set-note">XP в день — столько нужно набрать, чтобы засчитать день и продлить серию</small>
        <h3 class="set-sec">Вид дорожки</h3>
        <div class="pv-tiles">
          <button data-view="zigzag" class="card ${s.path_view !== "list" ? "on" : ""}">${ZIG}<b>Зигзаг</b></button>
          <button data-view="list" class="card ${s.path_view === "list" ? "on" : ""}">${LST}<b>Список</b></button></div>
      </div>
      <div class="set-col">
        <h3 class="set-sec">Режимы</h3>
        ${setRow(ic("heart", "si"), "Сердечки", "Ошибка в уроке стоит сердечко, вернуть — в работе над ошибками", toggle("hearts", s.hearts_enabled))}
        ${setRow(ic("unlock", "si ok"), "Открыть все уроки", "Любой урок доступен сразу, без прохождения предыдущих", toggle("sequential", !s.sequential_lessons))}
        ${setRow(ic(s.theme === "dark" ? "moon" : "sun", "si blue"), "Тёмная тема", "", toggle("theme", s.theme === "dark"))}
        ${setRow(ic("sound", "si ok"), "Звуки", "", toggle("sound", soundOn()))}
        ${installCard()}
        <h3 class="set-sec">Аккаунт</h3>
        <button class="card set-row link-row" id="pw-open">${ic("key", "si")}<div class="grow"><b>Сменить пароль</b></div>${chev}</button>
        ${u.is_admin ? `<button class="card set-row link-row" id="admins-open">${ic("shield", "si ok")}<div class="grow"><b>Администраторы</b><small class="muted">назначить или снять по нику</small></div>${chev}</button>` : ""}
        <button class="card set-row link-row danger" id="danger-open">${ic("warn", "si")}<div class="grow"><b>Сбросить прогресс или удалить аккаунт</b></div>${chev}</button>
      </div></div>`;
    view.querySelectorAll("[data-goal]").forEach((b) => b.onclick = () => save({ daily_goal: Number(b.dataset.goal) }));
    view.querySelector("#theme").onclick = () => save({ theme: s.theme === "dark" ? "light" : "dark" });
    view.querySelector("#hearts").onclick = () => save({ hearts_enabled: !s.hearts_enabled });
    view.querySelectorAll("[data-view]").forEach((b) => b.onclick = () => save({ path_view: b.dataset.view }));
    view.querySelector("#sequential").onclick = () => save({ sequential_lessons: !s.sequential_lessons });
    view.querySelector("#sound").onclick = () => {
      localStorage.setItem("cq-sound", soundOn() ? "off" : "on");
      sound("good");
      draw();
    };
    view.querySelector("#danger-open").onclick = openDanger;
    view.querySelector("#pw-open").onclick = openPassword;
    view.querySelector("#admins-open")?.addEventListener("click", openAdmins);
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
  };
  const openPassword = () => {
    const m = modal(`<h2 class="cheat-title">${ic("key")}Смена пароля</h2>
      <form class="form" id="pw-form" novalidate style="text-align:left">
        <label>Текущий пароль<input class="input" type="password" name="current" autocomplete="current-password" maxlength="128"></label>
        <label>Новый пароль<small>Не меньше 6 символов. На других устройствах придётся войти заново.</small>
          <input class="input" type="password" name="next" autocomplete="new-password" maxlength="128"></label>
        <label>Повтори новый пароль<input class="input" type="password" name="next2" autocomplete="new-password" maxlength="128"></label>
        <p class="auth-error" id="pw-error" hidden></p>
        <div class="btns"><button class="btn" type="submit">Сменить пароль</button><button class="btn ghost" type="button" id="pw-cancel">Отмена</button></div>
      </form>`);
    const pw = m.root.querySelector("#pw-form");
    m.root.querySelector("#pw-cancel").onclick = m.close;
    pw.current.focus();
    pw.onsubmit = async (e) => {
      e.preventDefault();
      const err = m.root.querySelector("#pw-error");
      const fail = (msg) => { err.textContent = msg; err.hidden = false; };
      if (!pw.current.value || !pw.next.value) return fail("Заполни текущий и новый пароль");
      if (pw.next.value !== pw.next2.value) return fail("Новые пароли не совпадают");
      try {
        await api("/account/password", { method: "PUT", body: { current_password: pw.current.value, new_password: pw.next.value } });
        m.close();
        toast("key", "Пароль изменён", "Другие устройства вышли из аккаунта");
      } catch (e2) { fail(e2.message); }
    };
  };
  const openAdmins = () => {
    const m = modal(`<h2 class="cheat-title">${ic("shield")}Администраторы</h2>
      <form class="form" id="admins-form" novalidate style="text-align:left">
        <p class="muted" style="margin:0">Администратор может менять контент в разделе «Контент» и назначать других администраторов.</p>
        <div class="row" style="gap:10px">
          <input class="input" name="username" placeholder="Ник пользователя" maxlength="64" autocomplete="off" style="flex:1;min-width:140px">
          <button class="btn small" type="submit">Назначить</button></div>
        <p class="auth-error" id="admins-error" hidden></p>
        <div id="admins-list" class="muted">Загрузка…</div>
        <div class="btns"><button class="btn ghost" type="button" id="adm-close">Готово</button></div>
      </form>`);
    m.root.querySelector("#adm-close").onclick = m.close;
    bindAdmins(m.root);
  };
  const openDanger = () => {
    const m = modal(`${owl("sad", "breathe")}<h2>Опасная зона</h2>
      <p class="muted">Сброс прогресса обнулит XP, серию, награды и решённые задания. Удаление аккаунта сотрёт аккаунт вместе со всем прогрессом.</p>
      <div class="btns"><button class="btn red" id="d-reset">Сбросить прогресс</button><button class="btn red" id="d-delete">Удалить аккаунт</button>
        <button class="btn ghost" id="d-cancel">Отмена</button></div>`);
    m.root.querySelector("#d-cancel").onclick = m.close;
    m.root.querySelector("#d-reset").onclick = confirmReset;
    m.root.querySelector("#d-delete").onclick = confirmDelete;
  };
  const save = async (patch) => { setState(await api("/settings", { method: "PUT", body: patch })); draw(); };
  const confirmReset = () => {
    const m = modal(`${owl("sad", "breathe")}<h2>Сбросить весь прогресс?</h2>
      <p class="muted">XP, серия, награды и решённые задания будут удалены. Темы и задания останутся. Это нельзя отменить.</p>
      <input class="input" id="confirm" placeholder="Напиши RESET для подтверждения">
      <div class="btns"><button class="btn red" id="yes" disabled>Сбросить</button><button class="btn ghost" id="no">Отмена</button></div>`);
    const inp = m.root.querySelector("#confirm"), yes = m.root.querySelector("#yes");
    inp.oninput = () => { yes.disabled = inp.value !== "RESET"; };
    m.root.querySelector("#no").onclick = m.close;
    yes.onclick = async () => { setState(await api("/progress/reset", { method: "POST", body: { confirm: "RESET" } })); m.close(); draw(); };
  };
  const confirmDelete = () => {
    const m = modal(`${owl("sad", "breathe")}<h2>Удалить аккаунт «${esc(store.user.username)}»?</h2>
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
