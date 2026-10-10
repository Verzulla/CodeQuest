// Service worker CodeQuest. Отдаётся сервером с корня (/sw.js), который подставляет
// VERSION (хеш файлов фронтенда) и SHELL (список этих файлов).
//
// Стратегия: оболочка приложения — «сначала сеть, при её отсутствии кэш», чтобы после
// обновления сервера сразу грузилась новая версия, а без интернета приложение всё равно
// открывалось. Запросы к /api/ не кэшируются никогда: прогресс и данные аккаунта — только живые.
const VERSION = "__VERSION__";
const SHELL = __SHELL__;
const CACHE = `cq-shell-${VERSION}`;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith("cq-shell-") && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin || url.pathname.startsWith("/api/")) return;
  if (url.pathname.startsWith("/static/stories/")) return;   // 3D-истории: модели тяжёлые, кэшем браузера обходимся
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      })
      .catch(() => caches.match(req).then((hit) => hit || (req.mode === "navigate" ? caches.match("/") : Response.error()))),
  );
});
