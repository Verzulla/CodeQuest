// Прохождение урока / повторения: теория → задания по одному → финальный экран.
import { api, esc, md, highlight, sound, modal, confetti, burst, toast, $ } from "../util.js";
import { createEditor } from "../editor.js";
import { bindRunnable } from "../runnable.js";
import { store, setState, announce } from "../store.js";

export async function renderLesson(view, id) {
  let lesson;
  try {
    lesson = await api(`/lessons/${id}`);
  } catch (e) {
    view.innerHTML = `<div class="empty"><div class="big">🔒</div><h2>${esc(e.message)}</h2><a class="btn" href="#/">Все темы</a></div>`;
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

export function runSession(view, opts) {
  // Пройденный урок открывается «с чистого листа» (повтор), незаконченный — с места, где остановился.
  const replay = opts.mode === "lesson" && opts.completed;
  const persist = opts.mode === "lesson" && !replay;          // черновики сохраняются на сервер
  const items = opts.exercises.map((ex) => {
    const solved = persist && ex.solved;
    return { ex, solved, answer: solved ? ex.answer : (persist ? ex.draft : ""), failed: false, redo: false };
  });
  const n = items.length;
  const s = { mistakes: 0, xp: 0, events: [], solvedNow: 0, firstTry: 0, theorySeen: false };
  // Теория урока: полный урок (theoryFull) — основной экран, краткая (theory) — шпаргалка.
  const hasCheat = opts.mode === "lesson" && !!(opts.theory || "").trim();
  const hasFull = opts.mode === "lesson" && !!(opts.theoryFull || "").trim();
  const hasTheory = hasCheat || hasFull;
  // «Проверь себя» — после всех заданий; страницы вопросов идут следом за заданиями: cur = n + k.
  const quiz = opts.mode === "lesson" ? (opts.quiz || []) : [];
  const quizAnswers = quiz.map(() => null);
  const FULL = -2;                 // полный урок, открытый из задания через 📖 (с возвратом к заданию)
  let returnTo = null;             // задание, из которого открыли полный урок
  const allSolved = () => items.every((it) => it.solved);
  const training = opts.mode === "training";   // случайные решённые задания: шпаргалка — своя у каждого задания
  const exitHash = () => (opts.mode === "review" ? "#/review" : training ? "#/training" : (opts.backHash || "#/"));
  // Сессия может идти по тому же адресу, куда выходим (тренировка — #/training): тогда hashchange не
  // случится сам, и экран нужно перерисовать явно.
  const leaveTo = (hash) => {
    if (location.hash === hash) window.dispatchEvent(new HashChangeEvent("hashchange"));
    else location.hash = hash;
  };
  const cheatOf = () => (training && cur >= 0 && cur < n ? (items[cur].ex.cheat || "").trim() : "");
  document.body.classList.add("focus");
  view.style.setProperty("--tc", opts.color || "var(--green)");

  // Где начать: первое нерешённое задание; теория — только если ещё ничего не решено.
  const firstTodo = items.findIndex((it) => !it.solved);
  const anySolved = items.some((it) => it.solved);
  let cur = hasTheory && !anySolved ? -1 : Math.max(0, firstTodo);
  let reached = firstTodo === -1 ? n - 1 : firstTodo;          // дальше этого места вперёд не прыгаем
  if (anySolved && firstTodo > 0) toast("▶️", `Продолжаем с задания ${firstTodo + 1} из ${n}`, "Прогресс урока сохранён");

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
      return `<button class="${cls.join(" ")}" data-seg="${n}" title="Проверь себя${allSolved() ? "" : " — откроется после всех заданий"}" ${allSolved() ? "" : "disabled"}></button>`;
    }
    const it = items[i];
    const cls = ["seg", it.solved ? "done" : it.failed ? "fail" : "", i === cur ? "cur" : ""];
    const open = i <= reached || it.solved;
    const title = `Задание ${i + 1}${it.solved ? " · решено" : it.failed ? " · была ошибка" : ""}`;
    return `<button class="${cls.join(" ")}" data-seg="${i}" title="${title}" ${open ? "" : "disabled"}></button>`;
  };
  const top = () => `
    <div class="lesson-top">
      <button class="close" title="Выйти" id="quit">✕</button>
      <div class="segs">${hasTheory ? segHtml(-1) : ""}${items.map((_, i) => segHtml(i)).join("")}${quiz.length ? segHtml(n) : ""}</div>
      ${hasTheory || cheatOf() ? `<button class="btn ghost small" id="theory-btn" title="Шпаргалка урока">📖</button>` : ""}
      ${store.state.hearts_enabled && opts.mode === "lesson"
        ? `<span class="pill heart">❤️ ${store.state.hearts}</span>`
        : opts.mode === "review" ? `<span class="pill heart" title="В повторении сердечки не тратятся, а восстанавливаются">❤️ +</span>`
        : training ? `<span class="pill" title="В тренировке ошибки не тратят сердечки">🏋️</span>` : ""}
    </div>`;

  const bindTop = () => {
    $("#quit", view).onclick = () => {
      flushDraft();
      const leave = () => leaveTo(exitHash());
      if (opts.mode !== "lesson") return leave();
      const m = modal(`<div class="big">👋</div><h2>Выйти из урока?</h2>
        <p class="muted">Прогресс сохранён: решённые задания и недописанные ответы останутся на месте, в следующий раз продолжишь отсюда.</p>
        <div class="btns"><button class="btn" data-a="stay">Продолжить учиться</button>
        <button class="btn ghost" data-a="leave">Выйти</button></div>`);
      m.root.querySelector('[data-a="stay"]').onclick = m.close;
      m.root.querySelector('[data-a="leave"]').onclick = () => { m.close(); leave(); };
    };
    view.querySelectorAll("[data-seg]").forEach((b) => b.onclick = () => {
      const i = Number(b.dataset.seg);
      i === n && quiz.length ? toEnd() : goTo(i);   // к вопросам — только через засчитывание урока
    });
    const tb = $("#theory-btn", view);
    if (tb) tb.onclick = () => {
      if (training) {
        const ex = items[cur].ex;
        const m = modal(`<h2 style="margin-top:0">📝 Шпаргалка</h2>
          <p class="muted" style="margin-top:-6px">${esc(ex.topic_title || "")} · ${esc(ex.lesson_title || "")}</p>
          <div class="theory md" style="text-align:left;max-height:60vh;overflow:auto">${md(cheatOf(), { runnable: true })}</div>
          <div class="btns"><button class="btn" data-a="ok">Понятно</button></div>`);
        m.root.style.maxWidth = "720px";
        bindRunnable(m.root);
        m.root.querySelector('[data-a="ok"]').onclick = m.close;
        return;
      }
      if (!hasCheat) { returnTo = cur >= 0 && cur < n ? cur : null; goTo(FULL); return; }
      const m = modal(`<h2 style="margin-top:0">📝 Шпаргалка</h2>
        <div class="theory md" style="text-align:left;max-height:60vh;overflow:auto">${md(opts.theory, { runnable: true })}</div>
        <div class="btns">${hasFull ? `<button class="btn blue" data-a="full">📚 Открыть полный урок</button>` : ""}
        <button class="btn" data-a="ok">Понятно</button></div>`);
      m.root.style.maxWidth = "720px";
      bindRunnable(m.root);
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
  // Основной экран — полный урок; шпаргалка свёрнута внизу (и доступна по 📖 во время заданий).
  const cheatBlock = () => hasFull && hasCheat
    ? `<details class="cheat"><summary>📝 Шпаргалка — коротко всё главное из урока</summary>
        <div class="theory md">${md(opts.theory, { runnable: true })}</div></details>` : "";
  function showTheory() {
    s.theorySeen = true;
    view.innerHTML = `${top()}
      <div class="lesson-body"><div class="ex-kind">📖 Урок</div><h1>${esc(opts.title)}</h1>
      <div class="theory md full">${md(hasFull ? opts.theoryFull : opts.theory, { runnable: true })}</div>
      ${cheatBlock()}</div>
      <div class="footer"><div class="inner"><div class="spacer"></div>
        <button class="btn" id="go">${anySolved || s.solvedNow ? "Дальше →" : "Поехали!"}</button></div></div>`;
    bindTop();
    bindRunnable(view);
    $("#go", view).onclick = () => goTo(0);
    $("#go", view).focus();
  }

  // ---------- Полный урок, открытый из задания ----------
  function showTheoryFull() {
    s.theorySeen = true;
    const back = returnTo;
    view.innerHTML = `${top()}
      <div class="lesson-body"><div class="ex-kind">📖 Урок</div><h1>${esc(opts.title)}</h1>
      <div class="theory md full">${md(opts.theoryFull, { runnable: true })}</div>
      ${cheatBlock()}</div>
      <div class="footer"><div class="inner"><div class="spacer"></div>
        <button class="btn" id="go">${back !== null ? `Вернуться к заданию ${back + 1} →` : anySolved || s.solvedNow ? "Дальше →" : "Поехали!"}</button></div></div>`;
    bindTop();
    bindRunnable(view);
    $("#go", view).onclick = () => { returnTo = null; goTo(back !== null ? back : 0); };
  }

  // ---------- Задание ----------
  function showExercise(i) {
    const item = items[i];
    const ex = item.ex;
    const isCode = ex.type === "code";
    const isCmd = ex.type === "command";
    const kindLabel = isCode ? "Напиши код" : isCmd ? "Терминал" : "Что выведет программа?";
    const viewSolved = item.solved && !item.redo;   // решённое задание: показываем решение, проверка выключена
    view.innerHTML = `${top()}
      <div class="lesson-body">
        <div class="ex-kind ${item.solved || ex.solved ? "" : "new"}">Задание ${i + 1} из ${n} · ${kindLabel}</div>
        ${training ? `<div class="muted" style="font-size:13px;margin:-4px 0 8px">${esc(ex.topic_title || "")} · ${esc(ex.lesson_title || "")}${ex.warmup ? ` · <b title="Урок ещё не пройден — задание не засчитывается">🆕 разминка</b>` : ""}</div>` : ""}
        ${viewSolved ? `<div class="solved-banner"><span>✅ Задание решено — это твоё решение</span>
          <button class="btn ghost small" id="redo">↺ Решить заново</button></div>` : ""}
        ${item.redo ? `<div class="solved-banner redo"><span>↺ Решаешь заново — ошибки здесь не отнимают сердечки, статус «решено» сохранится</span></div>` : ""}
        <div class="prompt md">${md(ex.prompt)}</div>
        ${isCode ? `<div id="ed"></div>`
          : isCmd ? `${ex.code ? `<pre class="code-view term">${esc(ex.code)}</pre>` : ""}
            <div class="term-input"><span class="term-prompt">$</span>
              <input class="answer code" id="answer" placeholder="команда или ответ"
                spellcheck="false" autocomplete="off" autocapitalize="off"></div>`
          : `<pre class="code-view">${highlight(ex.code)}</pre>
          <textarea class="answer code" id="answer" placeholder="Введи вывод программы — каждую строку с новой строки" spellcheck="false"></textarea>`}
        <div class="tools">
          ${isCode ? `<button class="btn blue small" id="run">▶ Запустить</button>` : ""}
          ${ex.hint && !viewSolved ? `<button class="btn ghost small" id="hint">💡 Подсказка</button>` : ""}
          <button class="btn ghost small" id="sol" ${item.failed || item.solved ? "" : "hidden"}>👀 ${item.solved ? "Эталонное решение" : "Показать решение"}</button>
          ${isCode && !viewSolved ? `<button class="btn ghost small" id="reset" title="Вернуть заготовку">↺ Сбросить</button>` : ""}
          <span class="muted" style="align-self:center;font-size:13px">${isCode && !viewSolved ? "⌘/Ctrl + Enter — проверить" : ""}</span>
        </div>
        <div id="hintbox"></div>
        <div id="console"></div>
      </div>
      <div class="footer" id="footer"></div>`;
    bindTop();

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
      if (!viewSolved) editor.focus();
      $("#run", view).onclick = async () => {
        const btn = $("#run", view);
        btn.disabled = true;
        btn.textContent = "⏳ Выполняю…";
        try { showConsole(await api("/run", { method: "POST", body: { code: editor.value } }), false); }
        finally { btn.disabled = false; btn.textContent = "▶ Запустить"; }
      };
      $("#reset", view)?.addEventListener("click", () => { editor.value = ex.starter_code; editor.focus(); });
    } else {
      answerEl = $("#answer", view);
      answerEl.value = initial;
      answerEl.readOnly = viewSolved;
      if (!viewSolved) answerEl.focus();
      answerEl.oninput = () => onEdit(answerEl.value);
      answerEl.onkeydown = (e) => {
        if (e.key === "Enter" && (isCmd || e.metaKey || e.ctrlKey)) { e.preventDefault(); $("#check", view)?.click(); }
      };
    }
    $("#hint", view)?.addEventListener("click", () => {
      $("#hintbox", view).innerHTML = `<div class="hintbox">💡 ${md(ex.hint)}</div>`;
    });
    $("#sol", view).onclick = async () => {
      const { solution } = await api(`/exercises/${ex.id}/solution`);
      $("#hintbox", view).innerHTML = `<div class="hintbox"><b>Эталонное решение:</b><pre class="code-view${isCmd ? " term" : ""}">${isCmd ? esc(solution) : highlight(solution)}</pre>
        ${item.solved ? "" : `<small class="muted">Разберись, как оно работает, и напиши своё — копипаст не прокачивает мозг 😉</small>`}</div>`;
    };
    $("#redo", view)?.addEventListener("click", () => { item.redo = true; showExercise(i); });

    const footer = $("#footer", view);
    const solvedFooter = () => {
      const last = nextTodo(i) === -1 && (i === n - 1 || items.slice(i + 1).every((it) => it.solved));
      footer.className = "footer";
      footer.innerHTML = `<div class="inner">${backBtn()}<div class="spacer"></div>
        <button class="btn" id="next">${last && opts.mode === "lesson" ? endLabel() : "Дальше →"}</button></div>`;
      bindBack();
      $("#next", view).onclick = () => {
        if (i < n - 1) return goTo(i + 1);
        const j = nextTodo(i);
        j === -1 ? toEnd() : goTo(j);
      };
    };
    const idleFooter = () => {
      footer.className = "footer";
      footer.innerHTML = `<div class="inner">${backBtn()}<div class="spacer"></div>
        ${item.redo ? `<button class="btn ghost" id="cancel-redo">Отмена</button>` : ""}
        <button class="btn" id="check">Проверить</button></div>`;
      bindBack();
      $("#cancel-redo", view)?.addEventListener("click", () => { item.redo = false; showExercise(i); });
      $("#check", view).onclick = check;
      refreshCheck();
    };
    viewSolved ? solvedFooter() : idleFooter();

    // Продолжить после верного ответа: к следующему нерешённому или к финалу.
    const proceed = () => {
      const j = nextTodo(i);
      j === -1 ? toEnd() : goTo(j);
    };

    async function check() {
      const btn = $("#check", view);
      btn.disabled = true;
      btn.textContent = isCode ? "⏳ Тестирую…" : "…";
      const mode = opts.mode === "review" ? "review" : training && ex.warmup ? "warmup" : training || item.redo ? "practice" : "lesson";
      const answer = getAnswer();
      let r;
      try {
        r = await api(`/exercises/${ex.id}/check`, { method: "POST", body: { answer, mode } });
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
          if (!item.failed) s.firstTry++;
        }
        item.solved = true;
        item.redo = false;
        item.answer = answer;
        clearTimeout(draftTimer); draftPending = null;   // сервер сам очистил черновик
        if (isCode) editor.textarea.readOnly = true; else answerEl.readOnly = true;
        footer.className = "footer good";
        footer.innerHTML = `<div class="inner"><div class="verdict"><span class="ico">✅</span>
          <div>${praise()}<div class="detail">+${gained} XP</div></div></div>
          <div class="spacer"></div><button class="btn" id="cont">${nextTodo(i) === -1 ? (opts.mode === "lesson" ? endLabel() : "Готово") : "Продолжить"}</button></div>`;
        $("#cont", view).onclick = proceed;
      } else {
        sound("bad");
        if (mode !== "practice" || training) { s.mistakes++; item.failed = true; }
        $("#sol", view).hidden = false;
        view.querySelector(".lesson-body").classList.add("shake");
        const detail = isCode
          ? (r.details.error ? "Программа упала — смотри консоль" : `Не прошло тестов: ${r.details.tests.filter((t) => !t.passed).length} из ${r.details.tests.length}`)
          : isCmd ? `Например: ${r.expected}` : `Правильный ответ:\n${r.expected}`;
        footer.className = "footer bad";
        const later = nextTodo(i);
        footer.innerHTML = `<div class="inner"><div class="verdict"><span class="ico">❌</span>
          <div>${isCode ? "Пока не то" : "Неправильно"}<div class="detail">${esc(detail)}</div></div></div>
          <div class="spacer"></div>
          ${item.redo ? `<button class="btn ghost" id="cancel-redo">Отмена</button><button class="btn red" id="retry">Исправить</button>`
            : isCode ? `${later !== -1 && later !== i ? `<button class="btn ghost" id="later">Позже</button>` : ""}<button class="btn red" id="retry">Исправить</button>`
            : `<button class="btn red" id="cont">Понятно</button>`}</div>`;
        $("#retry", view)?.addEventListener("click", () => { idleFooter(); (isCode ? editor : answerEl).focus(); });
        $("#later", view)?.addEventListener("click", () => goTo(later));
        $("#cancel-redo", view)?.addEventListener("click", () => { item.redo = false; showExercise(i); });
        // «что выведет»: правильный ответ уже показан — вернёмся к заданию позже, по кругу
        $("#cont", view)?.addEventListener("click", () => {
          const j = nextTodo(i);
          if (j === i || j === -1) { answerEl.value = ""; item.answer = ""; saveDraft(item, ""); idleFooter(); answerEl.focus(); }
          else goTo(j);
        });
        if (mode === "lesson" && store.state.hearts_enabled && store.state.hearts <= 0) {
          setTimeout(noHearts, 700);
        }
      }
      refreshTop();
      ($("#cont", view) || $("#retry", view))?.focus();
    }
  }

  function showConsole(res, withTests) {
    const box = $("#console", view);
    if (!box) return;
    const tests = withTests && res.tests.length
      ? `<ul class="tests">${res.tests.map((t) => `<li class="${t.passed ? "ok" : "fail"}">${t.passed ? "✔" : "✘"} ${esc(t.name.replace(/^test_/, "").replaceAll("_", " "))}${t.message ? ` — ${esc(t.message)}` : ""}</li>`).join("")}</ul>`
      : "";
    const out = res.stdout ? esc(res.stdout) : `<span class="muted">(программа ничего не вывела)</span>`;
    const err = res.error ? `\n<span class="err">${esc(res.error)}${res.error_line ? ` (строка ${res.error_line})` : ""}</span>` : "";
    box.innerHTML = `<div class="console"><div class="c-head">Вывод</div><pre>${out}${err}</pre>
      ${tests ? `<div class="c-head">Тесты</div>${tests}` : ""}</div>`;
  }

  function noHearts() {
    const m = modal(`<div class="big">💔</div><h2>Сердечки закончились</h2>
      <p class="muted">Потренируйся в «Повторении» — каждый правильный ответ там возвращает ❤️. Или подожди: сердечко восстанавливается каждые 30 минут.</p>
      <div class="btns"><a class="btn blue" href="#/review" data-a="r">Повторение (+❤️)</a>
      <a class="btn ghost" href="${opts.backHash || "#/"}" data-a="h">К урокам темы</a></div>`);
    m.root.querySelectorAll("a").forEach((a) => a.addEventListener("click", m.close));
  }

  // ---------- «Проверь себя» ----------
  const endLabel = () => (quiz.length ? "Дальше: проверь себя 🧠" : "Завершить урок 🏁");

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
        <div class="ex-kind">🧠 Проверь себя · вопрос ${k + 1} из ${quiz.length} · без штрафов</div>
        <div class="prompt md">${md(q.q)}</div>
        <div class="quiz-options">${q.options.map((o, j) => {
          const cls = !answered ? "" : j === q.answer ? "right" : j === chosen ? "wrong" : "dim";
          return `<button class="quiz-opt ${cls}" data-opt="${j}" ${answered ? "disabled" : ""}>
            <span class="qo-key">${"АБВГДЕ"[j]}</span><span class="md">${md(o)}</span></button>`;
        }).join("")}</div>
        ${answered ? `<div class="quiz-explain ${chosen === q.answer ? "right" : "wrong"}">
          <b>${chosen === q.answer ? "✅ Верно!" : "❌ Не совсем."}</b> ${md(q.explain || "")}</div>` : ""}
      </div>
      <div class="footer"><div class="inner">${backBtn()}<div class="spacer"></div>
        ${answered ? "" : `<button class="btn ghost" id="skip">Пропустить</button>`}
        <button class="btn" id="qnext" ${answered ? "" : "disabled"}>${last ? "Завершить урок 🏁" : "Дальше →"}</button></div></div>`;
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
      completion = await api(`/lessons/${opts.lessonId}/complete`, { method: "POST", body: { mistakes: s.mistakes } });
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
    const acc = s.solvedNow ? Math.round((100 * s.firstTry) / s.solvedNow) : 100;
    const rewards = s.events.filter((e) => ["trophy", "achievement", "level_up", "perfect"].includes(e.type));
    const hero = rewards.some((e) => e.type === "trophy" && e.kind === "topic") ? "🏆"
      : rewards.some((e) => e.type === "trophy") ? "🏅" : s.mistakes === 0 ? "💎" : "🎉";
    const title = opts.mode === "review" ? "Повторение завершено!" : training ? "Тренировка завершена!"
      : s.mistakes === 0 ? "Идеально! Без ошибок!" : "Урок пройден!";
    view.innerHTML = `<div class="finish">
      <div class="hero">${hero}</div><h1>${title}</h1>
      <div class="tiles">
        <div class="tile" style="--c:var(--gold)"><small>Опыт</small><div>⚡ ${s.xp}</div></div>
        <div class="tile" style="--c:var(--green)"><small>Точность</small><div>🎯 ${acc}%</div></div>
        <div class="tile" style="--c:var(--blue)"><small>Заданий</small><div>✅ ${n}</div></div>
      </div>
      <div class="rewards">${quizLine()}${rewards.map((e, i) => reward(e, i + 1)).join("")}</div>
      <button class="btn wide" id="done">Продолжить</button></div>`;
    sound("done");
    confetti();
    $("#done", view).onclick = () => leaveTo(exitHash());
    $("#done", view).focus();
  }

  const quizLine = () => {
    const done = quizAnswers.filter((a) => a !== null).length;
    if (!quiz.length || !done) return "";
    const right = quiz.filter((q, k) => quizAnswers[k] === q.answer).length;
    return `<div class="reward" style="animation-delay:.3s"><div class="ri">🧠</div><div><b>Проверь себя: ${right} из ${quiz.length}</b>
      <span class="muted">${right === quiz.length ? "Материал усвоен отлично" : "Загляни в подробную теорию, чтобы закрепить"}</span></div></div>`;
  };

  const reward = (e, i) => {
    const delay = `style="animation-delay:${0.3 + i * 0.15}s"`;
    if (e.type === "trophy") return `<div class="reward trophy" ${delay}><div class="ri">${esc(e.icon)}</div><div>
      <b>${e.kind === "topic" ? "Тема пройдена! 🏆" : "Модуль завершён! 🏅"}</b>${esc(e.title)} · +${e.kind === "topic" ? 50 : 20} XP</div></div>`;
    if (e.type === "achievement") return `<div class="reward" ${delay}><div class="ri">${esc(e.icon)}</div><div>
      <b>${esc(e.title)}</b><span class="muted">${esc(e.description)}</span></div></div>`;
    if (e.type === "level_up") return `<div class="reward" ${delay}><div class="ri">🆙</div><div><b>Уровень ${e.level}!</b><span class="muted">Так держать</span></div></div>`;
    return `<div class="reward" ${delay}><div class="ri">💎</div><div><b>Без ошибок</b><span class="muted">+5 XP бонус</span></div></div>`;
  };

  goTo(cur);
}

const PRAISES = ["Отлично!", "Супер!", "Великолепно!", "Так держать!", "В точку!", "Красота!"];
const praise = () => PRAISES[Math.floor(Math.random() * PRAISES.length)];

function alertError(e) {
  const m = modal(`<div class="big">⚠️</div><h2>Что-то пошло не так</h2><p class="muted">${esc(e.message)}</p>
    <div class="btns"><button class="btn">Ок</button></div>`);
  m.root.querySelector(".btn").onclick = m.close;
}
