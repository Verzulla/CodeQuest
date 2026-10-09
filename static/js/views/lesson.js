// Прохождение урока / повторения: теория → задания по одному → финальный экран.
import { api, esc, md, highlight, sound, modal, confetti, burst, toast, fmtTime, ic, owl, plural, goBack, $ } from "../util.js";
import { createEditor } from "../editor.js";
import { achMini } from "../achievements.js";
import { keybarHtml, bindKeybar } from "../keybar.js";
import { bindRunnable } from "../runnable.js";
import { bindViz } from "../viz.js";
import { store, setState, announce } from "../store.js";

export async function renderLesson(view, id) {
  let lesson;
  try {
    lesson = await api(`/lessons/${id}`);
  } catch (e) {
    view.innerHTML = `<div class="empty">${owl("sleep", "breathe")}<h2>${esc(e.message)}</h2><a class="btn" href="#/">Все темы</a></div>`;
    return;
  }
  runSession(view, {
    mode: "lesson",
    lessonId: lesson.id,
    title: lesson.title,
    theory: lesson.theory,
    theoryFull: lesson.theory_full,
    quiz: lesson.quiz,
    color: lesson.topic.color,
    backHash: `#/topic/${lesson.topic.id}`,
    completed: lesson.completed,
    exercises: lesson.exercises,
  });
}

const THEORY_MODE_KEY = "cq-theory-mode";   // «steps» или «page» — удобство конкретного браузера

export function runSession(view, opts) {
  // Пройденный урок открывается «с чистого листа» (повтор), незаконченный — с места, где остановился.
  const replay = opts.mode === "lesson" && opts.completed;
  const persist = opts.mode === "lesson" && !replay;          // черновики сохраняются на сервер
  const items = opts.exercises.map((ex) => {
    const solved = persist && ex.solved;
    // failed — на задании уже была ошибка (в том числе в прошлый заход): оно в работе над ошибками
    return { ex, solved, answer: solved ? ex.answer : (persist ? ex.draft : ""), failed: persist && !!ex.in_review, redo: false };
  });
  const n = items.length;
  const s = { mistakes: items.filter((it) => it.failed).length, xp: 0, events: [], solvedNow: 0, firstTry: 0, theorySeen: false, started: Date.now() };
  // Теория урока: полный урок (theoryFull) — основной экран, краткая (theory) — шпаргалка.
  const hasCheat = opts.mode === "lesson" && !!(opts.theory || "").trim();
  const hasFull = opts.mode === "lesson" && !!(opts.theoryFull || "").trim();
  const hasTheory = hasCheat || hasFull;
  // Шаги теории: разделы «## …» полного урока (текст раздела — без изменений) + шпаргалка последним шагом.
  const steps = [];
  if (hasFull) {
    let head = "";
    for (const part of opts.theoryFull.replace(/\r\n/g, "\n").split(/^(?=## )/m)) {
      const m = part.match(/^## (.+)\n?([\s\S]*)$/);
      if (!m) { head += part; continue; }
      steps.push({ title: m[1].trim(), body: (steps.length ? "" : head) + m[2] });
    }
    if (!steps.length) steps.push({ title: opts.title, body: opts.theoryFull });
  }
  if (hasCheat) steps.push({ title: "Шпаргалка", body: opts.theory, cheat: true });
  let theoryStep = 0;
  const theoryMode = () => {
    let m = null;
    try { m = localStorage.getItem(THEORY_MODE_KEY); } catch { /* ок */ }
    return m === "steps" || m === "page" ? m : window.innerWidth <= 700 ? "steps" : "page";
  };
  // «Проверь себя» — после всех заданий; страницы вопросов идут следом за заданиями: cur = n + k.
  const quiz = opts.mode === "lesson" ? (opts.quiz || []) : [];
  const quizAnswers = quiz.map(() => null);
  const FULL = -2;                 // полный урок, открытый из задания через книжку (с возвратом к заданию)
  let returnTo = null;             // задание, из которого открыли полный урок
  const allSolved = () => items.every((it) => it.solved);
  // Каждое задание решено или уже с ошибкой: урок можно завершить, нерешённые — в работе над ошибками.
  const allTried = () => items.every((it) => it.solved || it.failed);
  const training = opts.mode === "training";   // случайные решённые задания: шпаргалка — своя у каждого задания
  const exitHash = () => (opts.mode === "review" ? "#/review" : training ? "#/training" : (opts.backHash || "#/"));
  // Сессия может идти по тому же адресу, куда выходим (тренировка — #/training): тогда hashchange не
  // случится сам, и экран нужно перерисовать явно.
  const leaveTo = (hash) => {
    if (location.hash === hash) window.dispatchEvent(new HashChangeEvent("hashchange"));
    else location.hash = hash;
  };
  // Выход из урока и повторения — на экран, откуда пришли; тренировка — к её настройке (тот же адрес).
  const leave = () => (training ? leaveTo(exitHash()) : goBack(exitHash()));
  const cheatOf = () => (training && cur >= 0 && cur < n ? (items[cur].ex.cheat || "").trim() : "");
  document.body.classList.add("focus");
  view.style.setProperty("--tc", opts.color || "var(--green)");

  // Где начать: первое нерешённое задание; теория — только если ещё ничего не решено.
  const firstTodo = items.findIndex((it) => !it.solved);
  const anySolved = items.some((it) => it.solved);
  let cur = hasTheory && !anySolved ? -1 : Math.max(0, firstTodo);
  let reached = firstTodo === -1 ? n - 1 : firstTodo;          // дальше этого места вперёд не прыгаем
  if (anySolved && firstTodo > 0) toast("play", `Продолжаем с задания ${firstTodo + 1} из ${n}`, "Прогресс урока сохранён");

  // Следующее задание, которое ещё не пробовали (без ошибки и не решено), по кругу. -1 — таких нет.
  const nextFresh = (from) => {
    for (let k = 1; k <= n; k++) {
      const j = (((from + k) % n) + n) % n;
      if (!items[j].solved && !items[j].failed) return j;
    }
    return -1;
  };
  // Дальше после задания i. В уроке: к непробованному; если все попробованы — финал
  // или выбор «завершить / вернуться к нерешённым». В повторении и тренировке — по кругу до решения.
  const advanceFrom = (i) => {
    if (opts.mode !== "lesson") {
      const j = nextTodo(i);
      return j === -1 ? toEnd() : goTo(j);
    }
    const j = nextFresh(i);
    if (j !== -1) return goTo(j);
    return allSolved() ? toEnd() : offerFinish(i);
  };

  // Следующее нерешённое после from (по кругу). -1 — все решены.
  const nextTodo = (from) => {
    for (let k = 1; k <= n; k++) {
      const j = (((from + k) % n) + n) % n;
      if (!items[j].solved) return j;
    }
    return -1;
  };

  // ---------- Черновики ----------
  let draftTimer = null, draftPending = null;
  const flushDraft = () => {
    clearTimeout(draftTimer);
    if (!draftPending) return;
    const { id, text } = draftPending;
    draftPending = null;
    // keepalive — запрос доживёт, даже если вкладку закрывают прямо сейчас
    fetch(`/api/exercises/${id}/draft`, {
      method: "PUT", keepalive: true,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ draft: text }),
    }).catch(() => {});
  };
  // Уход со страницы (кнопка «назад», закрытие вкладки) не должен терять последние символы.
  window.addEventListener("hashchange", flushDraft, { once: true });
  window.addEventListener("pagehide", flushDraft, { once: true });
  const saveDraft = (item, text) => {
    if (!persist || item.solved) return;
    draftPending = { id: item.ex.id, text };
    clearTimeout(draftTimer);
    draftTimer = setTimeout(flushDraft, 700);
  };

  // ---------- Верхняя панель: сегменты по страницам урока ----------
  const segHtml = (i) => {
    if (i === -1) {
      const cls = ["seg", "theory", s.theorySeen || anySolved || cur !== -1 ? "done" : "", cur === -1 || cur === FULL ? "cur" : ""];
      return `<button class="${cls.join(" ")}" data-seg="-1" title="Теория"></button>`;
    }
    if (i === n) {
      const cls = ["seg", "quiz", quizAnswers.every((a) => a !== null) ? "done" : "", cur >= n ? "cur" : ""];
      return `<button class="${cls.join(" ")}" data-seg="${n}" title="Проверь себя${allTried() ? "" : " — откроется после всех заданий"}" ${allTried() ? "" : "disabled"}></button>`;
    }
    const it = items[i];
    const cls = ["seg", it.solved ? "done" : it.failed ? "fail" : "", i === cur ? "cur" : ""];
    const open = i <= reached || it.solved;
    const title = `Задание ${i + 1}${it.solved ? " · решено" : it.failed ? " · была ошибка" : ""}`;
    return `<button class="${cls.join(" ")}" data-seg="${i}" title="${title}" ${open ? "" : "disabled"}></button>`;
  };
  const top = () => `
    <div class="lesson-top">
      <button class="close" title="Выйти" id="quit">${ic("xmark")}</button>
      <div class="segs">${hasTheory ? segHtml(-1) : ""}${items.map((_, i) => segHtml(i)).join("")}${quiz.length ? segHtml(n) : ""}</div>
      ${cur === -1 && steps.length > 1 ? `<button class="tb" id="mode-btn" title="${theoryMode() === "steps" ? "Одной страницей" : "Шагами"}">${ic(theoryMode() === "steps" ? "pageI" : "stepsI")}</button>` : ""}
      ${hasTheory || cheatOf() ? `<button class="tb" id="theory-btn" title="Шпаргалка урока">${ic("book")}</button>` : ""}
      ${store.state.hearts_enabled && opts.mode === "lesson"
        ? `<span class="hp">${ic("heart")}${store.state.hearts}</span>`
        : opts.mode === "review" ? `<span class="hp" title="В повторении сердечки не тратятся; исправленное задание возвращает сердечки, потерянные на нём">${ic("heart")}+</span>`
        : training ? `<span class="hp train" title="В тренировке ошибки не тратят сердечки">${ic("i-dumb")}</span>` : ""}
    </div>`;

  const bindTop = () => {
    $("#quit", view).onclick = () => {
      flushDraft();
      if (opts.mode !== "lesson") return leave();
      const m = modal(`${owl("wave")}<h2>Выйти из урока?</h2>
        <p class="muted">Прогресс сохранён: решённые задания и недописанные ответы останутся на месте, в следующий раз продолжишь отсюда.</p>
        <div class="btns"><button class="btn" data-a="stay">Продолжить учиться</button>
        <button class="btn ghost" data-a="leave">Выйти</button></div>`);
      m.root.querySelector('[data-a="stay"]').onclick = m.close;
      m.root.querySelector('[data-a="leave"]').onclick = () => { m.close(); leave(); };
    };
    view.querySelectorAll("[data-seg]").forEach((b) => b.onclick = () => {
      const i = Number(b.dataset.seg);
      if (i === n && quiz.length) return allSolved() ? toEnd() : offerFinish(cur);   // к вопросам — только через засчитывание урока
      goTo(i);
    });
    const tb = $("#theory-btn", view);
    if (tb) tb.onclick = () => {
      if (training) {
        const ex = items[cur].ex;
        const m = modal(`<h2 class="cheat-title">${ic("book")}Шпаргалка</h2>
          <p class="muted" style="margin-top:-6px">${esc(ex.topic_title || "")} · ${esc(ex.lesson_title || "")}</p>
          <div class="theory md" style="text-align:left;max-height:60vh;overflow:auto">${md(cheatOf(), { runnable: true })}</div>
          <div class="btns"><button class="btn" data-a="ok">Понятно</button></div>`);
        m.root.style.maxWidth = "720px";
        bindRunnable(m.root);
        bindViz(m.root);
        m.root.querySelector('[data-a="ok"]').onclick = m.close;
        return;
      }
      if (!hasCheat) { returnTo = cur >= 0 && cur < n ? cur : null; goTo(FULL); return; }
      const m = modal(`<h2 class="cheat-title">${ic("book")}Шпаргалка</h2>
        <div class="theory md" style="text-align:left;max-height:60vh;overflow:auto">${md(opts.theory, { runnable: true })}</div>
        <div class="btns">${hasFull ? `<button class="btn ghost" data-a="full">Открыть полный урок</button>` : ""}
        <button class="btn" data-a="ok">Понятно</button></div>`);
      m.root.style.maxWidth = "720px";
      bindRunnable(m.root);
      bindViz(m.root);
      m.root.querySelector('[data-a="ok"]').onclick = m.close;
      m.root.querySelector('[data-a="full"]')?.addEventListener("click", () => {
        m.close();
        returnTo = cur >= 0 && cur < n ? cur : null;
        goTo(FULL);
      });
    };
  };
  const refreshTop = () => { $(".lesson-top", view).outerHTML = top(); bindTop(); };

  function goTo(i) {
    flushDraft();
    if (i === -1) theoryStep = cur >= 0 && cur < n ? steps.length - 1 : cur === -1 ? theoryStep : 0;
    cur = i;
    if (i >= 0 && i < n) reached = Math.max(reached, i);
    window.scrollTo(0, 0);
    if (i === -1) showTheory();
    else if (i === FULL) showTheoryFull();
    else if (i >= n) showQuiz(i - n);
    else showExercise(i);
  }
  const backTarget = () => {
    if (cur === FULL) return -1;
    if (cur > 0) return cur - 1;                // в том числе с первого вопроса — к последнему заданию
    if (cur === 0 && hasTheory) return -1;
    return null;
  };
  const backBtn = () => backTarget() === null ? "" : `<button class="btn ghost" id="back" title="Предыдущая страница">← Назад</button>`;
  const bindBack = () => { const b = $("#back", view); if (b) b.onclick = () => goTo(backTarget()); };

  // ---------- Урок (теория) ----------
  // Основной экран — полный урок; шпаргалка свёрнута внизу (и доступна по книжке во время заданий).
  const cheatBlock = () => hasFull && hasCheat
    ? `<details class="cheat"><summary>${ic("book")}Шпаргалка — коротко всё главное из урока</summary>
        <div class="theory md">${md(opts.theory, { runnable: true })}</div></details>` : "";
  // Теория шагами: один раздел «## …» полного урока = один шаг, текст без правок; последний шаг — шпаргалка.
  // Или одной страницей (статья с оглавлением разделов). Выбор запоминается в браузере.
  function showTheory() {
    s.theorySeen = true;
    theoryMode() === "steps" && steps.length > 1 ? showTheoryStep() : showTheoryPage();
  }
  const bindMode = () => {
    const b = $("#mode-btn", view);
    if (b) b.onclick = () => {
      try { localStorage.setItem(THEORY_MODE_KEY, theoryMode() === "steps" ? "page" : "steps"); } catch { /* ок */ }
      window.scrollTo(0, 0);
      showTheory();
    };
  };
  const goLabel = () => (anySolved || s.solvedNow ? "К заданиям →" : "Поехали!");

  function showTheoryPage() {
    const secs = hasFull ? steps.filter((st) => !st.cheat) : [];
    const toc = secs.length > 1 ? `<aside class="th-toc card"><b>Разделы урока</b>${secs.map((st, k) =>
      `<button class="toc-link" data-sec="${k}"><i>${k + 1}</i>${esc(st.title)}</button>`).join("")}
      ${hasCheat && hasFull ? `<button class="toc-link cheat-link" data-sec="cheat">${ic("book")}Шпаргалка</button>` : ""}</aside>` : "";
    view.innerHTML = `${top()}
      <div class="lesson-body th-page ${toc ? "with-toc" : ""}"><div class="th-article">
        <div class="th-first">${owl("think", "tilt")}</div>
        <div class="kind">Урок</div><h1>${esc(opts.title)}</h1>
        <div class="theory md full">${md(hasFull ? opts.theoryFull : opts.theory, { runnable: true })}</div>
        ${cheatBlock()}</div>${toc}</div>
      <div class="footer"><div class="inner"><div class="spacer"></div>
        <button class="btn main" id="go">${goLabel()}</button></div></div>`;
    bindTop();
    bindMode();
    bindRunnable(view);
    bindViz(view);
    const heads = [...view.querySelectorAll(".theory.full > h3")];
    view.querySelectorAll("[data-sec]").forEach((b) => b.onclick = () => {
      const el = b.dataset.sec === "cheat" ? view.querySelector("details.cheat") : heads[Number(b.dataset.sec)];
      if (el?.tagName === "DETAILS") el.open = true;
      el?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    $("#go", view).onclick = () => goTo(0);
  }

  function showTheoryStep() {
    const k = Math.min(theoryStep, steps.length - 1);
    const st = steps[k];
    const last = k === steps.length - 1;
    view.innerHTML = `${top()}
      <div class="lesson-body th-step">
        <div class="kind">${esc(opts.title)} · шаг ${k + 1} из ${steps.length}</div>
        <div class="step-dots">${steps.map((_, j) => `<button class="${j < k ? "done" : j === k ? "cur" : ""}" data-step="${j}" title="Шаг ${j + 1}"></button>`).join("")}</div>
        ${k === 0 ? `<div class="th-first">${owl("think", "tilt")}</div>` : ""}
        <h1 class="step-title">${st.cheat ? `${ic("book")}` : ""}${esc(st.title)}</h1>
        <div class="theory md full">${md(st.body, { runnable: true })}</div>
      </div>
      <div class="footer"><div class="inner">
        ${k > 0 ? `<button class="btn ghost" id="step-back">← Назад</button>` : ""}<div class="spacer"></div>
        <button class="btn main" id="go">${last ? goLabel() : "Дальше →"}</button></div></div>`;
    bindTop();
    bindMode();
    bindRunnable(view);
    bindViz(view);
    const to = (j) => { theoryStep = j; window.scrollTo(0, 0); showTheoryStep(); };
    $("#step-back", view)?.addEventListener("click", () => to(k - 1));
    view.querySelectorAll("[data-step]").forEach((b) => b.onclick = () => to(Number(b.dataset.step)));
    $("#go", view).onclick = () => (last ? goTo(0) : to(k + 1));
  }

  // ---------- Полный урок, открытый из задания ----------
  function showTheoryFull() {
    s.theorySeen = true;
    const back = returnTo;
    view.innerHTML = `${top()}
      <div class="lesson-body"><div class="kind">Урок</div><h1>${esc(opts.title)}</h1>
      <div class="theory md full">${md(opts.theoryFull, { runnable: true })}</div>
      ${cheatBlock()}</div>
      <div class="footer"><div class="inner"><div class="spacer"></div>
        <button class="btn" id="go">${back !== null ? `Вернуться к заданию ${back + 1} →` : anySolved || s.solvedNow ? "Дальше →" : "Поехали!"}</button></div></div>`;
    bindTop();
    bindRunnable(view);
    bindViz(view);
    $("#go", view).onclick = () => { returnTo = null; goTo(back !== null ? back : 0); };
  }

  // ---------- Задание ----------
  function showExercise(i) {
    const item = items[i];
    const ex = item.ex;
    const isCode = ex.type === "code";
    // ошиблись в коде и остались на задании («Исправить»): верное решение простит ошибку (game.record_answer)
    let fixNow = false;
    const isCmd = ex.type === "command";
    const kindLabel = isCode ? "Напиши код" : isCmd ? "Терминал" : "Что выведет программа?";
    const viewSolved = item.solved && !item.redo;   // решённое задание: показываем решение, проверка выключена
    const fileName = isCode ? "solution.py" : isCmd ? "терминал" : "program.py";
    const dots = `<span class="dots"><i></i><i></i><i></i></span>`;
    const work = isCode
      ? `<div class="code-card"><div class="cc-head">${dots}<span class="cc-name">${fileName}</span><span class="spacer"></span>
          <button class="act run" id="run">${ic("play")}Запустить</button></div><div id="ed"></div><div class="ed-grip" data-grip="ed" title="Потяни, чтобы изменить высоту поля"><i></i></div>${viewSolved ? "" : keybarHtml()}</div>`
      : isCmd
      ? `<div class="code-card term">${ex.code ? `<div class="cc-head">${dots}<span class="cc-name">${fileName}</span></div><pre class="code-view term">${esc(ex.code)}</pre>` : ""}
          <div class="term-input"><span class="term-prompt">$</span>
            <input class="answer code" id="answer" placeholder="команда или ответ"
              spellcheck="false" autocomplete="off" autocapitalize="off"></div>${viewSolved ? "" : keybarHtml()}</div>`
      : `<div class="code-card"><div class="cc-head">${dots}<span class="cc-name">${fileName}</span></div><pre class="code-view">${highlight(ex.code)}</pre></div>
        <div class="kind out-label">Твой ответ — что появится на экране</div>
        <div class="answer-card"><textarea class="answer code" id="answer" placeholder="Каждую строку вывода — с новой строки" spellcheck="false"></textarea><div class="ed-grip" data-grip="ans" title="Потяни, чтобы изменить высоту поля"><i></i></div>${viewSolved ? "" : keybarHtml()}</div>`;
    view.innerHTML = `${top()}
      <div class="lesson-body ex-layout${isCode ? " split" : ""}">
        <div class="ex-left">
          <div class="kind ${item.solved || ex.solved ? "" : "new"}">Задание ${i + 1} из ${n} · ${kindLabel}</div>
          ${training ? `<div class="muted ex-src">${esc(ex.topic_title || "")} · ${esc(ex.lesson_title || "")}${ex.warmup ? ` · <b title="Урок ещё не пройден — задание не засчитывается">разминка</b>` : ""}</div>` : ""}
          ${viewSolved ? `<div class="solved-banner"><span>${ic("okc")}Задание решено — это твоё решение</span>
            <button class="btn ghost small" id="redo">${ic("refresh")}Решить заново</button></div>` : ""}
          ${item.redo ? `<div class="solved-banner redo"><span>${ic("refresh")}Решаешь заново — ошибки здесь не отнимают сердечки, статус «решено» сохранится</span></div>` : ""}
          <div class="prompt md">${md(ex.prompt)}</div>
          <div class="tools">
            ${ex.hint && !viewSolved ? `<button class="act hint" id="hint">${ic("bulb")}Подсказка</button>` : ""}
            ${hasTheory || cheatOf() ? `<button class="act cheat" id="cheat-chip">${ic("book")}Шпаргалка</button>` : ""}
            <button class="act" id="sol">${ic("eye")}${item.solved ? "Эталонное решение" : "Показать решение"}</button>
            ${isCode && !viewSolved ? `<button class="act" id="reset" title="Вернуть заготовку">${ic("refresh")}Сбросить</button>` : ""}
          </div>
          <div id="hintbox"></div>
          ${isCode ? `<div class="ex-owl">${owl("think", "tilt")}</div>` : ""}
        </div>
        <div class="ex-right">
          ${work}
          <div id="console"></div>
          ${isCode && !viewSolved ? `<div class="kbd-tip muted"><kbd>⌘</kbd>/<kbd>Ctrl</kbd> + <kbd>Enter</kbd> — проверить</div>` : ""}
        </div>
      </div>
      <div class="footer" id="footer"></div>`;
    bindTop();
    $("#cheat-chip", view)?.addEventListener("click", () => $("#theory-btn", view)?.click());

    let editor, answerEl;
    const getAnswer = () => (isCode ? editor.value : answerEl.value);
    const refreshCheck = () => { const b = $("#check", view); if (b) b.disabled = !getAnswer().trim(); };
    const onEdit = (v) => {
      if (viewSolved) return;
      if (!item.redo) { item.answer = v; saveDraft(item, v); }
      refreshCheck();
    };
    const initial = viewSolved ? item.answer : item.redo ? (isCode ? ex.starter_code : "") : (item.answer || (isCode ? ex.starter_code : ""));

    if (isCode) {
      editor = createEditor($("#ed", view), initial, { onSubmit: () => $("#check", view)?.click(), onChange: onEdit });
      editor.textarea.readOnly = viewSolved;
      bindKeybar(view.querySelector(".ex-right"), editor.textarea);
      bindGrip(view.querySelector('[data-grip="ed"]'), view.querySelector(".editor .area"), "cq-ed-h");
      if (!viewSolved) editor.focus();
      $("#run", view).onclick = async () => {
        const btn = $("#run", view);
        if (btn.dataset.running) return;   // вид кнопки во время запуска не меняется — повторные нажатия просто игнорируем
        btn.dataset.running = "1";
        try { showConsole(await api("/run", { method: "POST", body: { code: editor.value } }), false); }
        finally { delete btn.dataset.running; }
      };
      $("#reset", view)?.addEventListener("click", () => { editor.value = ex.starter_code; editor.focus(); });
    } else {
      answerEl = $("#answer", view);
      answerEl.value = initial;
      answerEl.readOnly = viewSolved;
      bindKeybar(view.querySelector(".ex-right"), answerEl);
      if (!isCmd) bindGrip(view.querySelector('[data-grip="ans"]'), answerEl, "cq-ans-h");
      if (!viewSolved) answerEl.focus();
      answerEl.oninput = () => onEdit(answerEl.value);
      answerEl.onkeydown = (e) => {
        if (e.key === "Enter" && (isCmd || e.metaKey || e.ctrlKey)) { e.preventDefault(); $("#check", view)?.click(); }
      };
    }
    $("#hint", view)?.addEventListener("click", () => {
      $("#hintbox", view).innerHTML = `<div class="hintbox"><div class="kind">${ic("bulb")}Подсказка</div>${md(ex.hint)}</div>`;
    });
    // До первой попытки решение показываем не сразу — сначала предупреждение
    $("#sol", view).onclick = () => {
      if (item.failed || item.solved || item.peeked) return showSolution();
      $("#hintbox", view).innerHTML = `<div class="hintbox warn-sol"><div class="kind">${ic("warn")}Точно подсмотреть?</div>
        Попробуй сначала сам — даже неверная попытка покажет, где застрял, а решение без попытки забывается быстрее.
        Если подсмотришь, задание не засчитается «с первой попытки».
        <div class="row"><button class="btn main small" id="try-self">Попробую сам</button>
        <button class="btn ghost small" id="peek">${ic("eye")}Всё равно показать</button></div></div>`;
      $("#try-self", view).onclick = () => { $("#hintbox", view).innerHTML = ""; (isCode ? editor.textarea : answerEl)?.focus(); };
      $("#peek", view).onclick = () => { item.peeked = true; showSolution(); };
    };
    const showSolution = async () => {
      const { solution, explain } = await api(`/exercises/${ex.id}/solution`);
      // Разбор по строкам: код строки, под ним — что она делает; `…` в тексте — как код.
      const inl = (t) => esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>").replace(/\n/g, "<br>");
      const lines = (explain?.lines || []).map((l) => `<div class="ex-line"><div class="c">${isCmd ? esc(l.code) : highlight(l.code)}</div>
        <div class="t">${inl(l.text)}${(l.notes || []).map((n) => `<div class="n">${inl(n)}</div>`).join("")}</div></div>`).join("");
      const title = ex.type === "output" ? "Разбор программы по строкам" : isCmd && !explain?.lines?.length ? "" : "Разбор по строкам";
      $("#hintbox", view).innerHTML = `<div class="hintbox sol"><div class="kind">${ic("eye")}${ex.type === "output" ? "Правильный ответ" : "Эталонное решение"}</div><pre class="code-view${isCmd ? " term" : ""}">${isCmd || ex.type === "output" ? esc(solution) : highlight(solution)}</pre>
        ${explain?.idea ? `<div class="ex-idea"><div class="k">${ic("bulb")}Главная идея</div>${inl(explain.idea)}</div>` : ""}
        ${lines ? `<div class="expl"><div class="h">${title}</div>${lines}${explain.summary ? `<div class="ex-sum">${inl(explain.summary)}</div>` : ""}</div>` : ""}
        ${explain?.trace?.length ? `<div class="expl ex-trace"><div class="h">Выполнение по шагам</div>
          <div class="ex-row head"><span>Строка</span><span>Значения</span><span>На экране</span></div>
          ${explain.trace.map(([c, v, o]) => `<div class="ex-row"><span class="c">${highlight(c)}</span><span>${inl(v || "")}</span><span class="o">${esc(o || "")}</span></div>`).join("")}</div>` : ""}
        ${explain?.mistake ? `<div class="ex-miss"><div class="k">${ic("warn")}Частая ошибка</div>${inl(explain.mistake)}</div>` : ""}
        ${item.solved ? "" : `<small class="muted">Разберись, как оно работает, и напиши своё — копипаст не прокачивает мозг</small>`}</div>`;
    };
    $("#redo", view)?.addEventListener("click", () => { item.redo = true; showExercise(i); });

    const footer = $("#footer", view);
    const solvedFooter = () => {
      const last = nextTodo(i) === -1 && (i === n - 1 || items.slice(i + 1).every((it) => it.solved));
      footer.className = "footer";
      footer.innerHTML = `<div class="inner">${backBtn()}<div class="spacer"></div>
        <button class="btn main" id="next">${last && opts.mode === "lesson" ? endLabel() : "Дальше →"}</button></div>`;
      bindBack();
      $("#next", view).onclick = () => (i < n - 1 ? goTo(i + 1) : advanceFrom(i));
    };
    const idleFooter = () => {
      footer.className = "footer";
      footer.innerHTML = `<div class="inner">${backBtn()}<div class="spacer"></div>
        ${item.redo ? `<button class="btn ghost" id="cancel-redo">Отмена</button>` : ""}
        <button class="btn main" id="check">Проверить</button></div>`;
      bindBack();
      $("#cancel-redo", view)?.addEventListener("click", () => { item.redo = false; showExercise(i); });
      $("#check", view).onclick = check;
      refreshCheck();
    };
    viewSolved ? solvedFooter() : idleFooter();

    // Продолжить после верного ответа: к следующему заданию или к финалу.
    const proceed = () => advanceFrom(i);

    async function check() {
      const btn = $("#check", view);
      btn.disabled = true;
      btn.textContent = isCode ? "Тестирую…" : "Проверяю…";
      const mode = opts.mode === "review" ? "review" : training && ex.warmup ? "warmup" : training || item.redo ? "practice" : "lesson";
      const answer = getAnswer();
      let r;
      try {
        r = await api(`/exercises/${ex.id}/check`, { method: "POST", body: { answer, mode, fix: fixNow } });
      } catch (e) {
        if (e.status === 409) return noHearts();
        btn.disabled = false;
        btn.textContent = "Проверить";
        return alertError(e);
      }
      setState(r.state);
      announce(r.events);
      s.events.push(...r.events);
      const gained = r.events.filter((e) => e.type === "xp").reduce((a, e) => a + e.amount, 0);
      s.xp += gained;
      if (r.details) showConsole(r.details, true);

      if (r.correct) {
        sound("win");
        burst(btn);
        if (!item.solved) {
          s.solvedNow++;
          if (!item.failed && !item.peeked) s.firstTry++;
        }
        const fixed = r.events.find((e) => e.type === "fixed_now");
        if (fixed && !fixed.in_review) { item.failed = false; item.fixedNow = true; }   // не ждёт в работе над ошибками
        fixNow = false;
        item.solved = true;
        item.redo = false;
        item.answer = answer;
        clearTimeout(draftTimer); draftPending = null;   // сервер сам очистил черновик
        if (isCode) editor.textarea.readOnly = true; else answerEl.readOnly = true;
        footer.className = "footer good";
        const firstTry = !item.failed && !item.fixedNow && !item.peeked && !(item.redo);
        footer.innerHTML = `<div class="inner">${owl("happy", "hop", "")}<div class="verdict">
          <div>${praise()}<div class="detail">${gained ? `+${gained} XP` : "Решено"}${firstTry && gained ? " · с первой попытки" : ""}${fixed && !fixed.in_review ? " · исправлено сразу — в работу над ошибками не попадёт" : ""}</div></div></div>
          <div class="spacer"></div><button class="btn main" id="cont">${nextTodo(i) === -1 ? (opts.mode === "lesson" ? endLabel() : "Готово") : "Продолжить"}</button></div>`;
        $("#cont", view).onclick = proceed;
      } else {
        sound("bad");
        if (mode !== "practice" || training) { s.mistakes++; item.failed = true; }
        if (mode === "lesson" && isCode) fixNow = true;
        const outOfHearts = mode === "lesson" && store.state.hearts_enabled && store.state.hearts <= 0;
        $("#sol", view).hidden = false;
        view.querySelector(".lesson-body").classList.add("shake");
        const detail = isCode
          ? (r.details.error ? "Программа упала — смотри консоль" : `Пройдено тестов: ${r.details.tests.filter((t) => t.passed).length} из ${r.details.tests.length}`)
          : isCmd ? `Например: ${r.expected}` : `Правильный ответ:\n${r.expected}`;
        footer.className = "footer bad";
        const later = nextTodo(i);
        const lessonFlow = opts.mode === "lesson" && !item.redo;   // в уроке можно идти дальше и вернуться позже
        footer.innerHTML = `<div class="inner">${owl("think", "tilt")}<div class="verdict">
          <div>${isCode ? "Пока не то" : "Неправильно"}<div class="detail">${esc(detail)}</div></div></div>
          <div class="spacer"></div>
          ${item.redo ? `<button class="btn ghost" id="cancel-redo">Отмена</button><button class="btn red main" id="retry">Исправить</button>`
            : isCode ? `${lessonFlow || (later !== -1 && later !== i) ? `<button class="btn ghost" id="later">Позже</button>` : ""}<button class="btn red main" id="retry">Исправить</button>`
            : `<button class="btn red main" id="cont">Понятно</button>`}</div>`;
        $("#retry", view)?.addEventListener("click", () => { idleFooter(); (isCode ? editor : answerEl).focus(); });
        $("#later", view)?.addEventListener("click", () => {
          if (outOfHearts) return noHearts();   // исправить сразу можно и без сердечек, а дальше — нет
          lessonFlow ? advanceFrom(i) : goTo(later);
        });
        $("#cancel-redo", view)?.addEventListener("click", () => { item.redo = false; showExercise(i); });
        // «что выведет»: правильный ответ уже показан — вернёмся к заданию позже, по кругу
        $("#cont", view)?.addEventListener("click", () => {
          if (lessonFlow) return advanceFrom(i);
          const j = nextTodo(i);
          if (j === i || j === -1) { answerEl.value = ""; item.answer = ""; saveDraft(item, ""); idleFooter(); answerEl.focus(); }
          else goTo(j);
        });
        if (outOfHearts && !fixNow) setTimeout(noHearts, 700);
      }
      refreshTop();
      ($("#cont", view) || $("#retry", view))?.focus();
    }
  }

  function showConsole(res, withTests) {
    const box = $("#console", view);
    if (!box) return;
    const tests = withTests && res.tests.length
      ? `<ul class="tests">${res.tests.map((t) => `<li class="${t.passed ? "ok" : "fail"}">${ic(t.passed ? "okc" : "badc")}${esc(t.name.replace(/^test_/, "").replaceAll("_", " "))}${t.message ? ` — ${esc(t.message)}` : ""}</li>`).join("")}</ul>`
      : "";
    const out = res.stdout ? esc(res.stdout) : `<span class="muted">(программа ничего не вывела)</span>`;
    const err = res.error ? `\n<span class="err">${esc(res.error)}${res.error_line ? ` (строка ${res.error_line})` : ""}</span>` : "";
    const passed = withTests ? res.tests.filter((t) => t.passed).length : 0;
    const testHead = !tests ? "" : `<div class="c-head tests-head ${passed === res.tests.length ? "ok" : "fail"}">${ic("term")}Тесты: ${passed} из ${res.tests.length}</div>`;
    box.innerHTML = `<div class="console"><div class="c-head">Вывод</div><pre>${out}${err}</pre>${testHead}${tests}</div>`;
  }

  // Все задания попробованы, но не все решены: завершить урок или вернуться к нерешённым.
  function offerFinish(from) {
    const left = items.filter((it) => !it.solved).length;
    const m = modal(`${owl("think")}<h2>Остались нерешённые задания</h2>
      <p class="muted">${left === 1 ? "Одно задание пока не решено" : `Пока не решено ${left} ${plural(left, "задание", "задания", "заданий")}`}.
      ${left === 1 ? "Оно уже ждёт" : "Они уже ждут"} в «Работе над ошибками»: там ошибки не стоят сердечек, а исправление возвращает потерянные.</p>
      <div class="btns"><button class="btn" data-a="back">Вернуться к нерешённым</button>
      <button class="btn ghost" data-a="end">Завершить урок</button></div>`);
    m.root.querySelector('[data-a="back"]').onclick = () => {
      m.close();
      const j = nextTodo(from);
      goTo(j === -1 ? from : j);
    };
    m.root.querySelector('[data-a="end"]').onclick = () => { m.close(); toEnd(); };
  }

  function noHearts() {
    const rc = store.state.review_count;
    const m = modal(`${owl("sad", "breathe")}<div class="hearts-out">${ic("heartE").repeat(store.state.max_hearts)}</div>
      <h2>Сердечки закончились</h2>
      <p class="muted">Со временем они не восстанавливаются. Исправь ошибки — каждое исправленное задание вернёт сердечки, потерянные на нём.</p>
      ${rc ? `<div class="card revenge">${ic("heart")}<div><b>${rc} ${plural(rc, "задание ждёт", "задания ждут", "заданий ждут")} реванша</b>
        <div class="muted">можно вернуть до ${store.state.max_hearts} сердечек</div></div></div>` : ""}
      <div class="btns"><a class="btn" href="#/review" data-a="r">Работа над ошибками</a>
      <a class="btn ghost" href="${opts.backHash || "#/"}" data-a="h">К урокам темы</a></div>`);
    m.root.classList.add("modal-sad");
    m.root.querySelectorAll("a").forEach((a) => a.addEventListener("click", m.close));
  }

  // ---------- «Проверь себя» ----------
  const endLabel = () => (quiz.length ? "Дальше: проверь себя" : "Завершить урок");

  // Все задания решены. Урок засчитываем сразу — уход с вопросов «Проверь себя» ничего не отнимет.
  async function toEnd() {
    if (!(await completeLesson())) return;
    quiz.length ? goTo(n) : finish();
  }

  function showQuiz(k) {
    const q = quiz[k];
    const chosen = quizAnswers[k];
    const answered = chosen !== null;
    const last = k === quiz.length - 1;
    view.innerHTML = `${top()}
      <div class="lesson-body">
        <div class="kind">Проверь себя · вопрос ${k + 1} из ${quiz.length} · без штрафов</div>
        <div class="prompt md">${md(q.q)}</div>
        <div class="quiz-options">${q.options.map((o, j) => {
          const cls = !answered ? "" : j === q.answer ? "right" : j === chosen ? "wrong" : "dim";
          return `<button class="quiz-opt ${cls}" data-opt="${j}" ${answered ? "disabled" : ""}>
            <span class="qo-key">${"АБВГДЕ"[j]}</span><span class="md">${md(o)}</span></button>`;
        }).join("")}</div>
        ${answered ? `<div class="quiz-explain ${chosen === q.answer ? "right" : "wrong"}">
          <b>${chosen === q.answer ? "Верно!" : "Не совсем."}</b> ${md(q.explain || "")}</div>` : ""}
      </div>
      <div class="footer"><div class="inner">${backBtn()}<div class="spacer"></div>
        ${answered ? "" : `<button class="btn ghost" id="skip">Пропустить</button>`}
        <button class="btn main" id="qnext" ${answered ? "" : "disabled"}>${last ? "Завершить урок" : "Дальше →"}</button></div></div>`;
    bindTop();
    bindBack();
    view.querySelectorAll("[data-opt]").forEach((b) => b.onclick = () => {
      quizAnswers[k] = Number(b.dataset.opt);
      if (quizAnswers[k] === q.answer) {
        sound("win");
        burst(b);
      } else {
        sound("bad");
      }
      showQuiz(k);
      $("#qnext", view).focus();
    });
    $("#skip", view)?.addEventListener("click", finish);
    $("#qnext", view).onclick = () => (last ? finish() : goTo(n + k + 1));
  }

  // ---------- Финал ----------
  let completion = null;           // ответ /complete — вызываем ровно один раз за сессию
  async function completeLesson() {
    if (opts.mode !== "lesson" || completion) return true;
    try {
      completion = await api(`/lessons/${opts.lessonId}/complete`, { method: "POST", body: { mistakes: s.mistakes, seconds: Math.round((Date.now() - s.started) / 1000) } });
    } catch (e) { alertError(e); return false; }
    setState(completion.state);
    announce(completion.events.filter((e) => e.type !== "achievement")); // достижения покажем на финале
    s.events.push(...completion.events);
    s.xp += completion.events.filter((e) => e.type === "xp").reduce((a, e) => a + e.amount, 0);
    return true;
  }

  async function finish() {
    if (!(await completeLesson())) return;
    flushDraft();
    // Точность урока — доля заданий, решённых без единой ошибки (с учётом прошлых заходов);
    // в повторении и тренировке — по ответам этой сессии.
    const acc = opts.mode === "lesson" ? Math.round((100 * items.filter((it) => it.solved && !it.failed && !it.fixedNow).length) / n)
      : s.solvedNow ? Math.round((100 * s.firstTry) / s.solvedNow) : 100;
    const rewards = s.events.filter((e) => ["trophy", "achievement", "level_up", "perfect"].includes(e.type));
    const quizWrong = quiz.filter((q, k) => quizAnswers[k] !== null && quizAnswers[k] !== q.answer).length;
    const perfect = s.mistakes === 0 && allSolved() && quizWrong === 0;
    const title = opts.mode === "review" ? "Повторение завершено!" : training ? "Тренировка завершена!"
      : perfect ? "Урок пройден без ошибок!" : "Урок пройден!";
    const toFix = opts.mode === "lesson" ? items.filter((it) => it.failed).length : 0;
    const fixLine = toFix ? `<a class="reward card to-fix" href="#/review" style="animation-delay:.2s"><div class="ri">${ic("i-dumb")}</div><div>
      <b>${toFix} ${plural(toFix, "задание ждёт", "задания ждут", "заданий ждут")} работы над ошибками</b>
      <span class="muted">${allSolved() ? "Повтори их позже, чтобы закрепить" : "Там их можно дорешать"}${store.state.hearts_enabled ? " — исправленные вернут потерянные сердечки" : ""}</span></div>${ic("arrowR", "go")}</a>` : "";
    const secs = Math.round((Date.now() - s.started) / 1000);
    document.body.classList.add("celebrate");
    view.innerHTML = `<div class="finish">
      ${owl("trophy", "hop")}
      <div class="big-xp">+${s.xp} XP</div>
      <h1>${title}</h1>
      ${opts.mode === "lesson" ? `<p class="muted">${esc(opts.title)}</p>` : ""}
      <div class="tiles">
        <div class="tile" style="--c:#ffd54a"><small>Опыт</small><b>${ic("bolt")}${s.xp}</b></div>
        <div class="tile" style="--c:#9be84a"><small>Точность</small><b>${ic("target")}${acc}%</b></div>
        <div class="tile" style="--c:#6cc8ff"><small>Время</small><b>${ic("clock")}${fmtTime(secs)}</b></div>
      </div>
      <div class="rewards">${fixLine}${quizLine()}${rewards.map((e, i) => reward(e, i + 1)).join("")}</div>
      <button class="btn wide" id="done">Продолжить</button></div>`;
    sound("done");
    confetti();
    $("#done", view).onclick = () => { document.body.classList.remove("celebrate"); leave(); };
    view.querySelector(".to-fix")?.addEventListener("click", () => document.body.classList.remove("celebrate"));
    $("#done", view).focus();
  }

  const quizLine = () => {
    const done = quizAnswers.filter((a) => a !== null).length;
    if (!quiz.length || !done) return "";
    const right = quiz.filter((q, k) => quizAnswers[k] === q.answer).length;
    return `<div class="reward card" style="animation-delay:.3s"><div class="ri">${ic("target2")}</div><div><b>Проверь себя: ${right} из ${quiz.length}</b>
      <span class="muted">${right === quiz.length ? "Материал усвоен отлично" : "Загляни в подробную теорию, чтобы закрепить"}</span></div></div>`;
  };

  const reward = (e, i) => {
    const delay = `style="animation-delay:${0.3 + i * 0.15}s"`;
    if (e.type === "trophy") return `<div class="reward card trophy" ${delay}><div class="ri">${ic(e.kind === "topic" ? "cup" : "medalI")}</div><div>
      <b>${e.kind === "topic" ? "Тема пройдена!" : "Модуль завершён!"}</b><span class="muted">${esc(e.title)} · +${e.kind === "topic" ? 50 : 20} XP</span></div></div>`;
    if (e.type === "achievement") return `<div class="reward card" ${delay}><div class="ri">${achMini(e.code)}</div><div>
      <b>${esc(e.title)}</b><span class="muted">${esc(e.description)}</span></div></div>`;
    if (e.type === "level_up") return `<div class="reward card" ${delay}><div class="ri">${ic("star")}</div><div><b>Уровень ${e.level}!</b><span class="muted">Так держать</span></div></div>`;
    return `<div class="reward card" ${delay}><div class="ri">${ic("sparkle")}</div><div><b>Без ошибок</b><span class="muted">+5 XP бонус</span></div></div>`;
  };

  goTo(cur);
}

// Ручка под полем: тянешь — меняется высота поля; размер запоминается для следующих заданий.
function bindGrip(grip, box, key) {
  if (!grip || !box) return;
  const apply = (h) => { box.style.height = `${h}px`; box.style.maxHeight = "none"; box.style.minHeight = "100px"; };
  try { const h = Number(localStorage.getItem(key)); if (h >= 100) apply(h); } catch { /* ок */ }
  grip.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    const y0 = e.clientY, h0 = box.getBoundingClientRect().height;
    grip.setPointerCapture(e.pointerId);
    grip.classList.add("drag");
    const move = (ev) => apply(Math.round(Math.min(window.innerHeight * 0.9, Math.max(100, h0 + ev.clientY - y0))));
    const up = () => {
      grip.classList.remove("drag");
      grip.removeEventListener("pointermove", move);
      try { localStorage.setItem(key, String(Math.round(box.getBoundingClientRect().height))); } catch { /* ок */ }
    };
    grip.addEventListener("pointermove", move);
    grip.addEventListener("pointerup", up, { once: true });
    grip.addEventListener("pointercancel", up, { once: true });
  });
}

const PRAISES = ["Отлично!", "Супер!", "Великолепно!", "Так держать!", "В точку!", "Красота!"];
const praise = () => PRAISES[Math.floor(Math.random() * PRAISES.length)];

function alertError(e) {
  const m = modal(`${owl("sad", "breathe")}<h2>Что-то пошло не так</h2><p class="muted">${esc(e.message)}</p>
    <div class="btns"><button class="btn">Ок</button></div>`);
  m.root.querySelector(".btn").onclick = m.close;
}
