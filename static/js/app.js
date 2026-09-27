// Точка входа: хэш-роутер и загрузка состояния.
import { esc } from "./util.js";
import { refreshState } from "./store.js";
import { renderCatalog, renderTopic } from "./views/path.js";
import { renderLesson } from "./views/lesson.js";
import { renderReview, renderAwards, renderStats, renderSettings } from "./views/pages.js";
import { renderAdmin } from "./views/admin.js";
import { renderAbout } from "./views/about.js";

// Тема из localStorage сразу — чтобы не мигало светлым до ответа сервера.
try { document.documentElement.dataset.theme = localStorage.getItem("cq-theme") || "light"; } catch { /* ok */ }

const ROUTES = [
  [/^$/, "path", (v) => renderCatalog(v)],
  [/^topic\/(\d+)$/, "path", (v, m) => renderTopic(v, Number(m[1]))],
  [/^lesson\/(\d+)$/, null, (v, m) => renderLesson(v, Number(m[1]))],
  [/^review$/, "review", (v) => renderReview(v, false)],
  [/^review\/start$/, null, (v) => renderReview(v, true)],
  [/^awards$/, "awards", (v) => renderAwards(v)],
  [/^stats$/, "stats", (v) => renderStats(v)],
  [/^settings$/, "settings", (v) => renderSettings(v)],
  [/^admin$/, "admin", (v) => renderAdmin(v)],
  [/^about$/, "about", (v) => renderAbout(v)],
];

async function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  const view = document.getElementById("view");
  document.body.classList.remove("focus", "wide");
  document.getElementById("overlay").innerHTML = "";
  document.querySelectorAll(".confetti").forEach((c) => c.remove());
  view.onclick = null;
  view.innerHTML = "";
  window.scrollTo(0, 0);
  for (const [re, nav, render] of ROUTES) {
    const m = hash.match(re);
    if (!m) continue;
    document.querySelectorAll(".nav-link").forEach((a) => a.classList.toggle("active", a.dataset.route === nav));
    try {
      await render(view, m);
    } catch (e) {
      view.innerHTML = `<div class="empty"><div class="big">⚠️</div><h2>Не удалось загрузить</h2><p class="muted">${esc(e.message)}</p>
        <button class="btn" onclick="location.reload()">Обновить</button></div>`;
    }
    return;
  }
  location.hash = "#/";
}

window.addEventListener("hashchange", route);
refreshState().then(route, (e) => {
  document.getElementById("view").innerHTML = `<div class="empty"><div class="big">🔌</div><h2>Сервер недоступен</h2><p class="muted">${esc(e.message)}. Запусти <code>./run.sh</code>.</p></div>`;
});
