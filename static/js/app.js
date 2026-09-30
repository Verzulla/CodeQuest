// Точка входа: хэш-роутер и загрузка состояния.
import { api, esc, modal, toast, owl } from "./util.js";
import { store, refreshState } from "./store.js";
import { renderAuth } from "./views/auth.js";
import { renderCatalog, renderTopic, renderTopicTheory } from "./views/path.js";
import { renderLesson } from "./views/lesson.js";
import { renderReview, renderTraining, renderAwards, renderStats, renderSettings, renderNavAvatar } from "./views/pages.js";
import { renderAdmin } from "./views/admin.js";
import { renderAbout } from "./views/about.js";

// Тема из localStorage сразу — чтобы не мигало светлым до ответа сервера.
try { document.documentElement.dataset.theme = localStorage.getItem("cq-theme") || "dark"; } catch { /* ok */ }

const ROUTES = [
  [/^$/, "path", (v) => renderCatalog(v)],
  [/^topic\/(\d+)$/, "path", (v, m) => renderTopic(v, Number(m[1]))],
  [/^topic\/(\d+)\/theory$/, "path", (v, m) => renderTopicTheory(v, Number(m[1]))],
  [/^lesson\/(\d+)$/, null, (v, m) => renderLesson(v, Number(m[1]))],
  [/^review$/, "review", (v) => renderReview(v, false)],
  [/^review\/start$/, null, (v) => renderReview(v, true)],
  [/^training$/, "review", (v) => renderTraining(v)],
  [/^awards$/, "awards", (v) => renderAwards(v)],
  [/^stats$/, "stats", (v) => renderStats(v)],
  [/^settings$/, "settings", (v) => renderSettings(v)],
  [/^admin$/, "admin", (v) => (store.user.is_admin ? renderAdmin(v) : (location.hash = "#/"))],
  [/^about$/, "about", (v) => renderAbout(v)],
];

async function route() {
  if (!store.user) return;
  const hash = location.hash.replace(/^#\/?/, "");
  const view = document.getElementById("view");
  document.body.classList.remove("focus", "wide", "celebrate");
  document.getElementById("overlay").innerHTML = "";
  document.querySelectorAll(".confetti").forEach((c) => c.remove());
  view.onclick = null;
  view.innerHTML = "";
  window.scrollTo(0, 0);
  for (const [re, nav, render] of ROUTES) {
    const m = hash.match(re);
    if (!m) continue;
    document.querySelectorAll(".nav-link").forEach((a) => a.classList.toggle("active", a.dataset.route === nav));
    document.body.dataset.route = nav || "";   // для стилей конкретного раздела (например, фон без свечения)
    document.body.dataset.page = hash.split("/")[0] || "home";   // home / topic / awards / …
    try {
      await render(view, m);
    } catch (e) {
      view.innerHTML = `<div class="empty">${owl("sad", "breathe")}<h2>Не удалось загрузить</h2><p class="muted">${esc(e.message)}</p>
        <button class="btn" onclick="location.reload()">Обновить</button></div>`;
    }
    return;
  }
  location.hash = "#/";
}

// ---------- Аккаунт ----------
function showAuth() {
  store.user = null;
  store.state = null;
  document.body.classList.remove("focus", "wide", "celebrate");
  document.body.classList.add("auth");
  document.getElementById("overlay").innerHTML = "";
  document.getElementById("rail").innerHTML = "";
  const view = document.getElementById("view");
  view.onclick = null;
  renderAuth(view, (user) => {
    if (user.claimed_progress) toast("chest", "Прогресс перенесён", "Всё, что было решено раньше, теперь в твоём аккаунте");
    enter(user);
  });
}

async function enter(user) {
  store.user = user;
  document.body.classList.remove("auth");
  document.getElementById("nav-admin").hidden = !user.is_admin;
  renderNavAvatar();
  await refreshState();
  route();
  if (store.state && store.state.onboarded === false) showWelcome();
}

// Приветствие нового пользователя: один раз сразу после регистрации (флаг хранится на сервере).
function showWelcome() {
  const m = modal(`${owl("wave", "hop")}<h2>Добро пожаловать в CodeQuest!</h2>
    <p class="muted">Хочешь за пару минут узнать, как всё устроено: уроки и задания, опыт и уровни,
    серия дней, сердечки и награды?</p>
    <div class="btns"><button class="btn" id="welcome-yes">Посмотреть, как всё устроено</button>
      <button class="btn ghost" id="welcome-later">Позже</button></div>
    <p class="muted" style="margin:14px 0 0;font-size:13px">Раздел «О приложении» всегда есть в меню, а на телефоне — в профиле.</p>`);
  const done = (goAbout) => {
    m.close();
    store.state.onboarded = true;
    api("/onboarding/done", { method: "POST" }).catch(() => {});
    if (goAbout) location.hash = "#/about";
  };
  m.root.querySelector("#welcome-yes").onclick = () => done(true);
  m.root.querySelector("#welcome-later").onclick = () => done(false);
  document.getElementById("overlay").onclick = (e) => { if (e.target.id === "overlay") done(false); };
}

function serverDown(e) {
  document.body.classList.add("auth");   // без меню: без сервера оно всё равно бесполезно
  document.getElementById("view").innerHTML = `<div class="empty">${owl("sleep", "breathe")}<h2>${esc(e.message)}</h2>
    <p class="muted">Прогресс хранится на сервере, поэтому без связи учиться не получится. Проверь интернет и попробуй снова.</p>
    <button class="btn" onclick="location.reload()">Повторить</button></div>`;
}

// ---------- PWA ----------
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}));
}
// Chrome/Android: запоминаем предложение установки, кнопку покажем в настройках.
window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  window.cqInstallPrompt = e;
  window.dispatchEvent(new Event("cq:installable"));
});
window.addEventListener("appinstalled", () => { window.cqInstallPrompt = null; });

window.addEventListener("hashchange", route);
window.addEventListener("cq:unauthorized", () => { if (store.user) showAuth(); });
api("/auth/me").then(enter, (e) => (e.status === 401 ? showAuth() : serverDown(e))).catch(serverDown);
