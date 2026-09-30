// Управление контентом: дерево тем/модулей/уроков/заданий, формы, импорт/экспорт JSON.
import { api, esc, modal, toast, md } from "../util.js";
import { createEditor } from "../editor.js";
import { glyph } from "../glyphs.js";

const LABEL = { topics: "тему", modules: "модуль", lessons: "урок", exercises: "задание" };
const CHILD = { topics: "modules", modules: "lessons", lessons: "exercises" };
const NEW_TITLE = { topics: "Новая тема", modules: "Новый модуль", lessons: "Новый урок", exercises: "Новое задание" };
const PARENT_FIELD = { modules: "topic_id", lessons: "module_id", exercises: "lesson_id" };

let sel = null; // { kind, id } | { kind, parent, isNew: true }
const open = new Set(JSON.parse(sessionStorage.getItem("cq-admin-open") || "[]"));

export async function renderAdmin(view) {
  document.body.classList.add("wide");
  view.innerHTML = `<h1 class="section-title">Контент</h1>
    <div class="admin"><div class="card tree" id="tree"></div><div id="form"></div></div>`;
  await refresh(view);
}

async function refresh(view) {
  const tree = await api("/admin/tree");
  drawTree(view, tree);
  drawForm(view, tree);
}

function find(tree, kind, id) {
  for (const t of tree) {
    if (kind === "topics" && t.id === id) return t;
    for (const m of t.modules) {
      if (kind === "modules" && m.id === id) return m;
      for (const l of m.lessons) {
        if (kind === "lessons" && l.id === id) return l;
        for (const e of l.exercises) if (kind === "exercises" && e.id === id) return e;
      }
    }
  }
  return null;
}

function drawTree(view, tree) {
  const item = (kind, it, label, children = "") => {
    const key = `${kind}:${it.id}`;
    const hasKids = kind !== "exercises";
    const isOpen = open.has(key);
    const isSel = sel && !sel.isNew && sel.kind === kind && sel.id === it.id;
    return `<li><div class="t-item ${isSel ? "sel" : ""}" data-kind="${kind}" data-id="${it.id}">
        ${hasKids ? `<span data-toggle="${key}" style="width:14px">${isOpen ? "▾" : "▸"}</span>` : `<span style="width:14px"></span>`}
        <span class="lbl">${label}</span></div>
      ${hasKids && isOpen ? `<ul>${children}<li class="add" data-add="${CHILD[kind]}" data-parent="${it.id}">+ ${LABEL[CHILD[kind]]}</li></ul>` : ""}</li>`;
  };
  const html = tree.map((t) => item("topics", t, `${glyph(t, 22)} ${esc(t.title)}`,
    t.modules.map((m) => item("modules", m, `${esc(m.title)}`,
      m.lessons.map((l) => item("lessons", l, `${esc(l.title)}`,
        l.exercises.map((e, i) => item("exercises", e,
          `<span class="kind">${e.type === "code" ? "код" : e.type === "command" ? "$" : "вывод"} ${i + 1}.</span> ${esc(e.prompt.replace(/[`*#]/g, "").slice(0, 60))}`)).join(""))).join(""))).join(""))).join("");
  const box = view.querySelector("#tree");
  box.innerHTML = `
    <div class="row" style="margin-bottom:10px">
      <button class="btn small blue" id="imp">⬇ Импорт JSON</button>
      <button class="btn small ghost" id="exp">⬆ Экспорт</button>
    </div>
    <ul>${html}<li class="add" data-add="topics">+ новую тему</li></ul>`;

  box.querySelectorAll("[data-toggle]").forEach((t) => t.onclick = (e) => {
    e.stopPropagation();
    const k = t.dataset.toggle;
    open.has(k) ? open.delete(k) : open.add(k);
    sessionStorage.setItem("cq-admin-open", JSON.stringify([...open]));
    drawTree(view, tree);
  });
  box.querySelectorAll(".t-item").forEach((t) => t.onclick = () => {
    sel = { kind: t.dataset.kind, id: Number(t.dataset.id) };
    const key = `${sel.kind}:${sel.id}`;
    if (sel.kind !== "exercises") open.add(key);
    drawTree(view, tree);
    drawForm(view, tree);
  });
  box.querySelectorAll("[data-add]").forEach((a) => a.onclick = () => {
    sel = { kind: a.dataset.add, parent: Number(a.dataset.parent) || null, isNew: true };
    drawTree(view, tree);
    drawForm(view, tree);
  });
  box.querySelector("#imp").onclick = () => importDialog(view);
  box.querySelector("#exp").onclick = exportContent;
}

// ---------- Формы ----------
function drawForm(view, tree) {
  const box = view.querySelector("#form");
  if (!sel) {
    box.innerHTML = `<div class="card md">${HELP}</div>`;
    return;
  }
  const it = sel.isNew ? defaults(sel.kind) : find(tree, sel.kind, sel.id);
  if (!it) { sel = null; return drawForm(view, tree); }
  const k = sel.kind;
  const f = (name, label, input, hint = "") =>
    `<label data-f="${name}">${label}${hint ? ` <small>${hint}</small>` : ""}${input}</label>`;
  const text = (name) => `<input class="input" name="${name}" value="${esc(it[name])}">`;
  const area = (name, cls = "") => `<textarea class="input ${cls}" name="${name}">${esc(it[name])}</textarea>`;
  const code = (name) => `<div data-editor="${name}"></div>`;

  let fields = "";
  if (k === "topics") fields = f("title", "Название", text("title")) + f("description", "Описание", area("description", "prose"))
    + f("group_name", "Группа", text("group_name"), "раздел в каталоге тем, например «Python»; пусто — «Другие темы»")
    + `<div class="row">${f("icon", "Иконка (эмодзи)", text("icon"))}${f("color", "Цвет", `<input class="input" type="color" name="color" value="${esc(it.color)}" style="height:44px;width:90px;padding:4px">`)}</div>`;
  if (k === "modules") fields = f("title", "Название", text("title")) + f("description", "Описание", area("description", "prose"))
    + f("icon", "Иконка награды (эмодзи)", text("icon"), "её получишь, завершив модуль");
  if (k === "lessons") fields = f("title", "Название", text("title"))
    + f("theory_full", "Урок (markdown)", `<textarea class="input" name="theory_full" style="min-height:360px">${esc(it.theory_full || "")}</textarea>`,
      "основной экран теории перед заданиями; # заголовки, **жирный**, `код`, списки; блоки ```python получают кнопки «Запустить» и «Изменить», ```yaml / ```bash — просто подсветка")
    + f("theory", "Шпаргалка (markdown)", `<textarea class="input" name="theory" style="min-height:220px">${esc(it.theory)}</textarea>`,
      "коротко главное: свёрнута под уроком и открывается кнопкой с книжкой во время заданий (если урока нет — показывается вместо него)")
    + f("quiz", "Проверь себя (JSON)", `<textarea class="input" name="quiz" style="min-height:200px">${esc(prettyQuiz(it.quiz))}</textarea>`,
      'после всех заданий, без штрафов. Формат: [{"q": "вопрос", "options": ["А", "Б"], "answer": 0, "explain": "почему"}]');
  if (k === "exercises") fields = `
    <div class="row">${f("type", "Тип", `<select class="input" name="type">
        <option value="code" ${it.type === "code" ? "selected" : ""}>Написать код (проверка тестами)</option>
        <option value="output" ${it.type === "output" ? "selected" : ""}>Что выведет код?</option>
        <option value="command" ${it.type === "command" ? "selected" : ""}>Терминал (команда)</option></select>`)}
      ${f("xp", "XP", `<input class="input" type="number" min="1" max="100" name="xp" value="${it.xp}" style="width:90px">`)}</div>
    ${f("prompt", "Условие (markdown)", area("prompt", "prose"))}
    <div data-for="code">
      ${f("starter_code", "Заготовка кода", code("starter_code"), "то, что увидит ученик в редакторе")}
      ${f("tests", "Тесты", code("tests"), "функции test_*; доступны имена из кода ученика, OUTPUT и capture(f, *args)")}
      ${f("solution", "Эталонное решение", code("solution"), "показывается по кнопке «Показать решение»")}
      <div><button class="btn small blue" type="button" id="validate">Прогнать эталон через тесты</button></div>
    </div>
    <div data-for="output">
      ${f("code", "Код программы", code("code"))}
      ${f("expected_output", "Ожидаемый вывод", area("expected_output"))}
      <div><button class="btn small blue" type="button" id="compute">Вычислить вывод из кода</button></div>
    </div>
    <div data-for="command"><p class="muted">Задания «Терминал» (варианты ответа, контекст, эталон) описываются в файлах контента <code>content/src</code> через <code>cmd(...)</code> и загружаются командой sync.</p></div>
    <div id="vres"></div>
    ${f("hint", "Подсказка", area("hint", "prose"), "необязательно")}`;

  box.innerHTML = `<div class="card form">
    <h2>${sel.isNew ? NEW_TITLE[k] : "Редактирование"}</h2>
    ${fields}
    <div class="admin-actions">
      <div class="row"><button class="btn" id="save">Сохранить</button>
        ${!sel.isNew ? `<button class="btn ghost small" id="up" title="Выше">↑</button><button class="btn ghost small" id="down" title="Ниже">↓</button>` : ""}</div>
      ${!sel.isNew ? `<button class="btn red small" id="del">Удалить</button>` : ""}
    </div>
    ${!sel.isNew ? `<small class="muted">slug: ${esc(it.slug)}</small>` : ""}
  </div>`;

  const editors = {};
  box.querySelectorAll("[data-editor]").forEach((h) => { editors[h.dataset.editor] = createEditor(h, it[h.dataset.editor] || ""); });
  const syncType = () => {
    const t = box.querySelector('[name="type"]')?.value;
    box.querySelectorAll("[data-for]").forEach((d) => { d.hidden = d.dataset.for !== t; });
  };
  box.querySelector('[name="type"]')?.addEventListener("change", syncType);
  syncType();

  const collect = () => {
    const data = {};
    box.querySelectorAll("[name]").forEach((i) => { data[i.name] = i.type === "number" ? Number(i.value) : i.value; });
    for (const [n, ed] of Object.entries(editors)) data[n] = ed.value;
    return data;
  };

  box.querySelector("#save").onclick = async () => {
    const data = collect();
    try {
      if (sel.isNew) {
        if (PARENT_FIELD[k]) data[PARENT_FIELD[k]] = sel.parent;
        const created = await api(`/admin/${k}`, { method: "POST", body: data });
        if (PARENT_FIELD[k]) open.add(`${Object.keys(CHILD).find((p) => CHILD[p] === k)}:${sel.parent}`);
        sel = { kind: k, id: created.id };
      } else {
        await api(`/admin/${k}/${sel.id}`, { method: "PUT", body: data });
      }
      toast("check", "Сохранено");
      refresh(view);
    } catch (e) { toast("warn", "Не сохранилось", e.message); }
  };
  box.querySelector("#del")?.addEventListener("click", () => {
    const m = modal(`<h2>Удалить ${LABEL[k]}?</h2>
      <p class="muted">${k !== "exercises" ? "Всё вложенное тоже будет удалено. " : ""}Прогресс по удалённым заданиям перестанет учитываться.</p>
      <div class="btns"><button class="btn red" id="y">Удалить</button><button class="btn ghost" id="n">Отмена</button></div>`);
    m.root.querySelector("#n").onclick = m.close;
    m.root.querySelector("#y").onclick = async () => {
      await api(`/admin/${k}/${sel.id}`, { method: "DELETE" });
      m.close(); sel = null; refresh(view);
    };
  });
  for (const [btn, dir] of [["#up", -1], ["#down", 1]]) {
    box.querySelector(btn)?.addEventListener("click", async () => {
      await api(`/admin/${k}/${sel.id}/move`, { method: "POST", body: { direction: dir } });
      refresh(view);
    });
  }
  box.querySelector("#validate")?.addEventListener("click", async () => {
    const d = collect();
    const r = await api("/admin/validate", { method: "POST", body: { type: "code", tests: d.tests, solution: d.solution } });
    const lines = r.tests.map((t) => `${t.passed ? "✓" : "×"} ${t.name}${t.message ? " — " + t.message : ""}`);
    if (r.error) lines.unshift("Ошибка: " + r.error);
    if (!r.tests.length && !r.error) lines.push("Не найдено ни одной функции test_*");
    box.querySelector("#vres").innerHTML = `<div class="result-box ${r.passed ? "ok" : "fail"}">${r.passed ? "Эталон проходит все тесты\n" : "Эталон НЕ проходит тесты\n"}${esc(lines.join("\n"))}</div>`;
  });
  box.querySelector("#compute")?.addEventListener("click", async () => {
    const r = await api("/admin/validate", { method: "POST", body: { type: "output", code: editors.code.value } });
    if (r.error) {
      box.querySelector("#vres").innerHTML = `<div class="result-box fail">${esc(r.error)}</div>`;
      return;
    }
    box.querySelector('[name="expected_output"]').value = r.stdout.replace(/\n$/, "");
    box.querySelector("#vres").innerHTML = `<div class="result-box ok">Вывод вычислен и подставлен</div>`;
  });
}

function prettyQuiz(raw) {
  try { return JSON.stringify(typeof raw === "string" ? JSON.parse(raw || "[]") : raw || [], null, 2); }
  catch { return raw || "[]"; }
}

function defaults(kind) {
  return {
    topics: { title: "", description: "", icon: "🐍", color: "#58cc02", group_name: "" },
    modules: { title: "", description: "", icon: "⭐" },
    lessons: { title: "", theory: "", theory_full: "", quiz: "[]" },
    exercises: { type: "code", prompt: "", code: "", starter_code: "", tests: "def test_example():\n    assert ...\n",
      expected_output: "", solution: "", hint: "", xp: 10 },
  }[kind];
}

// ---------- Импорт / экспорт ----------
function importDialog(view) {
  const m = modal(`<h2>⬆ Импорт контента</h2>
    <p class="muted" style="text-align:left">Вставь JSON-пакет (например, сгенерированный Claude) или выбери файл.
    Элементы с уже существующим <code>slug</code> обновятся, новые — добавятся. Прогресс не теряется.</p>
    <input type="file" accept=".json,application/json" id="file" class="input">
    <textarea class="input" id="json" style="min-height:200px;margin-top:10px" placeholder='{"topics": [...]}'></textarea>
    <div class="btns"><button class="btn" id="go">Импортировать</button><button class="btn ghost" id="cancel">Отмена</button></div>`);
  m.root.style.maxWidth = "640px";
  const ta = m.root.querySelector("#json");
  m.root.querySelector("#file").onchange = async (e) => { ta.value = await e.target.files[0].text(); };
  m.root.querySelector("#cancel").onclick = m.close;
  m.root.querySelector("#go").onclick = async () => {
    let pkg;
    try { pkg = JSON.parse(ta.value); } catch { return toast("warn", "Это не JSON", "Проверь скобки и кавычки"); }
    try {
      const r = await api("/admin/import", { method: "POST", body: pkg });
      m.close();
      toast("okc", "Импорт завершён", `создано ${r.created}, обновлено ${r.updated}`);
      refresh(view);
    } catch (e) {
      const detail = Array.isArray(e.data?.detail) ? e.data.detail.slice(0, 3).map((d) => `${d.loc.join(".")}: ${d.msg}`).join("; ") : e.message;
      toast("warn", "Ошибка импорта", detail);
    }
  };
}

async function exportContent() {
  const data = await api("/admin/export");
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `codequest-content-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
}

const HELP = md(`## Как наполнять приложение

**Способ 1 — вручную.** Слева дерево: тема → модуль → урок → задание. Нажми «+», заполни форму, сохрани.

**Способ 2 — через Claude.** Попроси: *«сгенерируй тему про словари в Python»*. Claude создаст JSON-пакет
в папке \`content/\`, проверит каждое задание и загрузит его. Можно и вручную: «Импорт JSON».

### Типы заданий
- **Написать код** — ученик пишет программу, она запускается и проверяется тестами.
- **Что выведет код?** — ученик читает программу и вводит её вывод.
- $ **Терминал** — ученик вводит команду одной строкой; допустимые варианты — по одному на строку, \`re:…\` — регулярное выражение.

### Как писать тесты
\`\`\`
def test_sum_small():
    assert add(2, 3) == 5, "add(2, 3) должно вернуть 5"

def test_prints_hello():
    assert OUTPUT.strip() == "Hello"
\`\`\`
В тестах доступны все функции и переменные из кода ученика, \`OUTPUT\` (всё напечатанное)
и \`capture(f, *args)\` — вызвать функцию и получить то, что она напечатала.
Текст после запятой в \`assert\` ученик увидит как подсказку.`);
