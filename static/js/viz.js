// Интерактивные схемы в теории. В markdown урока это блок
//   ```viz
//   {"type": "memory" | "git", ...}
//   ```
// md() превращает его в <div class="viz" data-viz="…">, bindViz() оживляет.
// Общий каркас — «шаг — состояние — картинка»: кнопки «Сначала / Назад / Шаг», счётчик, пояснение к шагу.
import { esc, highlight } from "./util.js";

const SVG = "http://www.w3.org/2000/svg";

export function bindViz(root) {
  root.querySelectorAll(".viz:not([data-ready])").forEach((box) => {
    box.dataset.ready = "1";
    let spec;
    try {
      spec = JSON.parse(box.dataset.viz);
    } catch {
      box.innerHTML = `<div class="viz-err">Схема не загрузилась</div>`;
      return;
    }
    const kind = KINDS[spec.type];
    if (!kind) return;
    kind(box, spec);
  });
}

// ---------- каркас шагов ----------

function stepper(box, { title, states, render, extra = "" }) {
  box.innerHTML = `
    ${title ? `<div class="viz-title">${esc(title)}</div>` : ""}
    <div class="viz-stage"></div>
    <div class="viz-note"></div>
    <div class="viz-ctrl">
      <button class="viz-btn" data-a="reset" title="Сначала">⟲</button>
      <button class="viz-btn" data-a="prev">← Назад</button>
      <span class="viz-count"></span>
      <button class="viz-btn main" data-a="next">Шаг →</button>
    </div>${extra}`;
  const stage = box.querySelector(".viz-stage");
  const note = box.querySelector(".viz-note");
  const count = box.querySelector(".viz-count");
  const prevBtn = box.querySelector('[data-a="prev"]');
  const nextBtn = box.querySelector('[data-a="next"]');
  let i = 0;
  const show = () => {
    const st = states[i];
    render(stage, st, i > 0 ? states[i - 1] : null, i);
    note.innerHTML = st.note ? inline(st.note) : "";
    note.hidden = !st.note;
    count.textContent = `${i} / ${states.length - 1}`;
    prevBtn.disabled = i === 0;
    nextBtn.disabled = i === states.length - 1;
  };
  box.querySelector('[data-a="reset"]').onclick = () => { i = 0; show(); };
  prevBtn.onclick = () => { if (i > 0) { i--; show(); } };
  nextBtn.onclick = () => { if (i < states.length - 1) { i++; show(); } };
  show();
  return {
    // песочница git дописывает новые состояния в конец и переходит к последнему
    push(st) { states.splice(i + 1); states.push(st); i = states.length - 1; show(); },
    get current() { return states[i]; },
    reset() { i = 0; show(); },
    show,
  };
}

// `код` и **жирный** в пояснениях
function inline(text) {
  return esc(text).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
}

// ---------- память: имена, объекты и стрелки ----------
// {"type": "memory", "title": "…", "code": "a = [1]\nb = a",
//  "steps": [{"line": 1, "vars": {"a": "L"}, "objs": {"L": [1]}, "note": "…", "out": "…"}, …]}
// vars и objs в шаге — изменения к прошлому шагу (null — удалить).
// Объект: список [..] (ссылка на другой объект — строка "@id"), {"t": "tuple", "v": [..]}, число или строка.

function memoryViz(box, spec) {
  const states = [{ line: 0, vars: {}, objs: {}, out: [], note: spec.intro || "" }];
  for (const step of spec.steps) {
    const prev = states.at(-1);
    const vars = { ...prev.vars };
    const objs = { ...prev.objs };
    for (const [k, v] of Object.entries(step.vars || {})) v === null ? delete vars[k] : (vars[k] = v);
    for (const [k, v] of Object.entries(step.objs || {})) v === null ? delete objs[k] : (objs[k] = v);
    const out = step.out != null ? [...prev.out, ...String(step.out).split("\n")] : prev.out;
    states.push({ line: step.line || 0, vars, objs, out, note: step.note || "" });
  }
  const codeLines = (spec.code || "").split("\n");
  // У каждого объекта — постоянный номер и цвет на всю схему. Ссылки внутри объектов показываем
  // меткой «→2» того же цвета, а не стрелкой: стрелки из ячеек перекрещиваются и путают.
  const num = {};
  for (const st of states) for (const id of Object.keys(st.objs)) num[id] ??= Object.keys(num).length + 1;
  const ro = new ResizeObserver(() => drawArrows(box));
  stepper(box, {
    title: spec.title,
    states,
    render(stage, st, prev) {
      stage.innerHTML = `
        <div class="viz-mem">
          <pre class="viz-code">${codeLines.map((l, n) =>
            `<span class="ln${n + 1 === st.line ? " cur" : n + 1 < st.line ? " done" : ""}">${highlight(l) || " "}</span>`).join("")}</pre>
          <div class="viz-mem-graph">${memoryGraph(st, prev, num)}<svg class="viz-arrows"></svg></div>
          ${st.out.length ? `<div class="viz-out"><span>Вывод</span><pre>${esc(st.out.join("\n"))}</pre></div>` : ""}
        </div>`;
      const graph = stage.querySelector(".viz-mem-graph");
      ro.disconnect();
      ro.observe(graph);
      // на узком экране схема шире окна — показываем объект, который изменился на этом шаге
      const ch = graph.querySelector(".viz-obj.changed");
      if (ch) {
        const g = graph.getBoundingClientRect(), c = ch.getBoundingClientRect();
        if (c.right > g.right) graph.scrollLeft += c.right - g.right + 8;
        else if (c.left < g.left) graph.scrollLeft -= g.left - c.left + 8;
      }
      // нажатие на метку-ссылку подсвечивает объект, на который она указывает
      graph.querySelectorAll(".viz-ref").forEach((r) => (r.onclick = () => {
        const t = graph.querySelector(`.viz-obj[data-id="${CSS.escape(r.dataset.to)}"]`);
        if (!t) return;
        t.classList.remove("ping");
        void t.offsetWidth;
        t.classList.add("ping");
      }));
      requestAnimationFrame(() => drawArrows(box));
      drawArrows(box);
    },
  });
}

// Объект схемы → {t: тип, cells: [{label, value}] | null, value}. У словаря подписи ячеек — ключи.
function objKind(o) {
  if (Array.isArray(o)) return { t: "list", cells: o.map((value, k) => ({ label: k, value })) };
  if (o && typeof o === "object") {
    if (Array.isArray(o.v)) return { t: o.t || "list", cells: o.v.map((value, k) => ({ label: k, value })) };
    if (o.v && typeof o.v === "object") return { t: o.t || "dict", cells: Object.entries(o.v).map(([k, value]) => ({ label: pyRepr(k), value })) };
    return { t: o.t || "object", cells: null, value: o.v };
  }
  return { t: typeof o === "number" ? (Number.isInteger(o) ? "int" : "float") : "str", value: o };
}

const isRef = (v) => typeof v === "string" && v.startsWith("@");
const pyRepr = (v) => (typeof v === "string" ? `'${v}'` : v === null ? "None" : v === true ? "True" : v === false ? "False" : String(v));

function memoryGraph(st, prev, num) {
  // уровни: объекты, на которые смотрят имена, — 1-й столбец; на которые ссылаются они — 2-й…
  const level = {};
  let frontier = [...new Set(Object.values(st.vars))].filter((id) => id in st.objs);
  frontier.forEach((id) => (level[id] = 1));
  for (let depth = 2; frontier.length && depth < 5; depth++) {
    const next = [];
    for (const id of frontier) {
      for (const { value: it } of objKind(st.objs[id]).cells || []) {
        const ref = isRef(it) && it.slice(1);
        if (ref && ref in st.objs && !(ref in level)) { level[ref] = depth; next.push(ref); }
      }
    }
    frontier = next;
  }
  const columns = [];
  for (const id of Object.keys(st.objs)) {
    const lv = level[id] || 1;
    (columns[lv - 1] ||= []).push(id);
  }
  columns.forEach((ids) => ids.sort((a, b) => num[a] - num[b]));
  const tag = (id) => `c${(num[id] - 1) % 6}`;
  const changed = (id) => !prev || JSON.stringify(prev.objs[id]) !== JSON.stringify(st.objs[id]);
  // имена стоят в одной строке со своим объектом — стрелка короткая и горизонтальная
  const nameChips = (id) => Object.entries(st.vars).filter(([, to]) => to === id).map(([name]) => {
    const fresh = !prev || prev.vars[name] !== id;
    return `<div class="viz-var${fresh ? " fresh" : ""}" data-to="${esc(id)}"><span>${esc(name)}</span></div>`;
  }).join("");
  const objBox = (id) => {
    const o = objKind(st.objs[id]);
    const garbage = !(id in level);
    let body;
    if (o.cells) {
      body = `<div class="viz-cells${o.t === "dict" ? " dict" : ""}">${o.cells.length ? o.cells.map(({ label, value: it }) =>
        `<div class="viz-cell"><i>${esc(label)}</i>${isRef(it)
          ? `<b class="viz-ref ${tag(it.slice(1))}" data-to="${esc(it.slice(1))}" title="ссылка на объект ${num[it.slice(1)]}">→${num[it.slice(1)]}</b>`
          : `<b>${esc(pyRepr(it))}</b>`}</div>`).join("")
        : `<div class="viz-cell empty"><b>пусто</b></div>`}</div>`;
    } else {
      body = `<div class="viz-scalar">${esc(pyRepr(o.value))}</div>`;
    }
    return `<div class="viz-obj${changed(id) ? " changed" : ""}${garbage ? " garbage" : ""}" data-id="${esc(id)}">
      <div class="viz-obj-type"><span class="viz-num ${tag(id)}">${num[id]}</span>${esc(o.t)}${garbage ? " · никто не ссылается" : ""}</div>${body}</div>`;
  };
  if (!Object.keys(st.objs).length) return `<div class="viz-empty">объектов пока нет — нажми «Шаг»</div>`;
  const [first = [], ...rest] = columns;
  return `<div class="viz-col viz-first">${first.map((id) => `<div class="viz-names">${nameChips(id)}</div>${objBox(id)}`).join("")}</div>`
    + rest.map((ids) => `<div class="viz-col">${ids.map(objBox).join("")}</div>`).join("");
}

function drawArrows(box) {
  const graph = box.querySelector(".viz-mem-graph");
  const svg = graph?.querySelector(".viz-arrows");
  if (!svg) return;
  const base = graph.getBoundingClientRect();
  svg.setAttribute("width", graph.scrollWidth);
  svg.setAttribute("height", graph.scrollHeight);
  svg.innerHTML = `<defs><marker id="vz-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" class="viz-arrow-head"/></marker></defs>`;
  const target = (id) => graph.querySelector(`.viz-obj[data-id="${CSS.escape(id)}"]`);
  const line = (from, to, cls) => {
    const a = from.getBoundingClientRect(), b = to.getBoundingClientRect();
    const x1 = a.right - base.left + graph.scrollLeft;
    const y1 = a.top + a.height / 2 - base.top + graph.scrollTop;
    const x2 = b.left - base.left + graph.scrollLeft - 2, y2 = b.top + Math.min(22, b.height / 2) - base.top + graph.scrollTop;
    const dx = Math.max(24, (x2 - x1) / 2);
    const p = document.createElementNS(SVG, "path");
    p.setAttribute("d", x2 > x1
      ? `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`
      : `M${x1},${y1} C${x1 + 60},${y1} ${x2 - 60},${y2} ${x2},${y2}`);
    p.setAttribute("class", `viz-arrow ${cls}`);
    p.setAttribute("marker-end", "url(#vz-head)");
    svg.appendChild(p);
  };
  graph.querySelectorAll(".viz-var").forEach((v) => { const t = target(v.dataset.to); if (t) line(v, t, v.classList.contains("fresh") ? "fresh" : ""); });
}

// ---------- git: граф коммитов ----------
// {"type": "git", "title": "…", "steps": ["git commit -m 'A'", {"cmd": "git switch -c feature", "note": "…"}, …],
//  "sandbox": true}  — песочница: после шагов можно вводить свои команды.

function gitInit() {
  return { commits: [{ id: "C1", label: "C1", parents: [], lane: 0 }], branches: { main: "C1" }, head: "main", lanes: { main: 0 }, n: 1, log: [] };
}

function clone(st) {
  return { ...st, commits: st.commits.map((c) => ({ ...c })), branches: { ...st.branches }, lanes: { ...st.lanes }, log: [...st.log] };
}

const byId = (st, id) => st.commits.find((c) => c.id === id);
const headCommit = (st) => st.branches[st.head];

function ancestors(st, id) {
  const seen = new Set();
  const stack = [id];
  while (stack.length) {
    const c = stack.pop();
    if (!c || seen.has(c)) continue;
    seen.add(c);
    stack.push(...byId(st, c).parents);
  }
  return seen;
}

function laneOf(st, branch) {
  if (!(branch in st.lanes)) st.lanes[branch] = Math.max(-1, ...Object.values(st.lanes)) + 1;
  return st.lanes[branch];
}

function newCommit(st, parents, msg, label) {
  st.n += 1;
  const id = `C${st.n}`;
  st.commits.push({ id, label: label || id, parents, lane: laneOf(st, st.head), msg });
  st.branches[st.head] = id;
  return id;
}

// Выполнить команду git над копией состояния. Возвращает {state, text} или {error}.
function gitRun(prev, raw) {
  const cmd = raw.trim().replace(/\s+/g, " ");
  const words = cmd.match(/'[^']*'|"[^"]*"|\S+/g) || [];
  if (words[0] !== "git") return { error: "Команда должна начинаться с git" };
  const st = clone(prev);
  const [, sub, ...rest] = words;
  const arg = rest.filter((w) => !w.startsWith("-")).at(-1);
  const has = (...flags) => rest.some((w) => flags.includes(w));
  const exists = (b) => b in st.branches;
  if (sub === "commit") {
    const m = rest.findIndex((w) => w === "-m");
    const msg = m >= 0 ? (rest[m + 1] || "").replace(/^['"]|['"]$/g, "") : "";
    const id = newCommit(st, [headCommit(st)], msg);
    return { state: st, text: `новый коммит ${id} в ветке ${st.head}` };
  }
  if (sub === "branch" && arg && !has("-d", "-D")) {
    if (exists(arg)) return { error: `Ветка ${arg} уже есть` };
    st.branches[arg] = headCommit(st);
    return { state: st, text: `ветка ${arg} создана на ${headCommit(st)}, но HEAD остался на ${st.head}` };
  }
  if ((sub === "switch" || sub === "checkout") && arg) {
    if (has("-c", "-b")) {
      if (exists(arg)) return { error: `Ветка ${arg} уже есть` };
      st.branches[arg] = headCommit(st);
    } else if (!exists(arg)) return { error: `Нет ветки ${arg}` };
    st.head = arg;
    return { state: st, text: `HEAD теперь на ветке ${arg}` };
  }
  if (sub === "merge" && arg) {
    if (!exists(arg)) return { error: `Нет ветки ${arg}` };
    if (arg === st.head) return { error: "Нельзя влить ветку саму в себя" };
    const target = st.branches[arg], head = headCommit(st);
    if (ancestors(st, head).has(target)) return { state: st, text: "Already up to date — всё из этой ветки уже есть" };
    if (ancestors(st, target).has(head)) {
      st.branches[st.head] = target;
      return { state: st, text: `fast-forward: ${st.head} просто передвинулась на ${target}` };
    }
    const id = newCommit(st, [head, target], `Merge ${arg}`);
    return { state: st, text: `коммит слияния ${id} с двумя родителями` };
  }
  if (sub === "reset") {
    const m = (arg || "").match(/^HEAD~(\d*)$/);
    if (!m) return { error: "Поддерживается git reset --hard HEAD~1" };
    let id = headCommit(st);
    for (let k = 0; k < Number(m[1] || 1); k++) {
      id = byId(st, id).parents[0];
      if (!id) return { error: "Дальше коммитов нет" };
    }
    st.branches[st.head] = id;
    return { state: st, text: `${st.head} откатилась на ${id}${has("--hard") ? ", изменения выброшены" : ""}` };
  }
  if (sub === "rebase" && arg) {
    if (!exists(arg)) return { error: `Нет ветки ${arg}` };
    const onto = st.branches[arg];
    const base = ancestors(st, onto);
    const mine = [];
    for (let id = headCommit(st); id && !base.has(id); id = byId(st, id).parents[0]) mine.unshift(byId(st, id));
    if (!mine.length) return { state: st, text: "Нечего переносить" };
    st.branches[st.head] = onto;
    for (const c of mine) newCommit(st, [headCommit(st)], c.msg, c.label.replace(/′*$/, "") + "′");
    return { state: st, text: `${mine.length} коммит(а) переписаны поверх ${arg}; старые больше не в ветке` };
  }
  return { error: "Знаю команды: commit, branch, switch, checkout, merge, rebase, reset --hard HEAD~1" };
}

function gitViz(box, spec) {
  const states = [{ ...gitInit(), note: spec.intro || "" }];
  for (const step of spec.steps || []) {
    const cmd = typeof step === "string" ? step : step.cmd;
    const r = gitRun(states.at(-1), cmd);
    const st = r.state || clone(states.at(-1));
    st.cmd = cmd;
    st.note = (typeof step === "object" && step.note) || r.text || r.error;
    states.push(st);
  }
  const sandbox = spec.sandbox ? `
    <div class="viz-sandbox">
      <div class="viz-sb-head">Попробуй сам — введи команду:</div>
      <form class="viz-sb-form"><input class="viz-sb-input" placeholder="git commit -m 'тест'" autocapitalize="off" autocomplete="off" spellcheck="false">
        <button class="viz-btn main">↵</button></form>
      <div class="viz-sb-quick"></div>
      <div class="viz-sb-msg"></div>
    </div>` : "";
  let ctl = null;   // render() вызывается уже внутри stepper(), до присваивания
  ctl = stepper(box, {
    title: spec.title,
    states,
    extra: sandbox,
    render(stage, st, prev) {
      stage.innerHTML = `${st.cmd ? `<div class="viz-cmd"><span>$</span> ${esc(st.cmd)}</div>` : `<div class="viz-cmd muted">репозиторий с одним коммитом</div>`}
        <div class="viz-git-wrap">${gitSvg(st, prev)}</div>`;
      const wrap = stage.querySelector(".viz-git-wrap");
      wrap.scrollLeft = wrap.scrollWidth;
      quick();
    },
  });
  if (!spec.sandbox) return;
  const input = box.querySelector(".viz-sb-input");
  const msg = box.querySelector(".viz-sb-msg");
  const exec = (cmd) => {
    const r = gitRun(ctl.current, cmd);
    if (r.error) { msg.className = "viz-sb-msg err"; msg.textContent = r.error; return; }
    const st = r.state;
    st.cmd = cmd;
    st.note = r.text;
    msg.className = "viz-sb-msg";
    msg.textContent = "";
    ctl.push(st);
  };
  box.querySelector(".viz-sb-form").onsubmit = (e) => {
    e.preventDefault();
    if (input.value.trim()) exec(input.value);
    input.value = "";
  };
  // быстрые кнопки — подсказки команд для текущего состояния
  function quick() {
    const st = ctl?.current || states[0];
    const others = Object.keys(st.branches).filter((b) => b !== st.head);
    const cmds = [`git commit -m '${st.head}-${st.n + 1}'`, `git switch -c feature-${Object.keys(st.branches).length}`,
      ...others.flatMap((b) => [`git switch ${b}`, `git merge ${b}`, `git rebase ${b}`]), "git reset --hard HEAD~1"];
    const holder = box.querySelector(".viz-sb-quick");
    if (!holder) return;
    holder.innerHTML = cmds.map((c) => `<button class="viz-chip" data-cmd="${esc(c)}">${esc(c.replace(/^git /, ""))}</button>`).join("");
    holder.querySelectorAll("button").forEach((b) => (b.onclick = () => exec(b.dataset.cmd)));
  }
  quick();
}

function gitSvg(st, prev) {
  const reach = new Set();
  for (const id of Object.values(st.branches)) for (const a of ancestors(st, id)) reach.add(a);
  const stepX = 62, laneH = 70, padX = 34, padY = 52;
  const lanes = Math.max(...st.commits.map((c) => c.lane)) + 1;
  const pos = {};
  st.commits.forEach((c, k) => (pos[c.id] = { x: padX + k * stepX, y: padY + c.lane * laneH }));
  const w = padX * 2 + (st.commits.length - 1) * stepX + 40;
  const h = padY + (lanes - 1) * laneH + 34;
  const fresh = new Set(prev ? st.commits.filter((c) => !prev.commits.some((p) => p.id === c.id)).map((c) => c.id) : []);
  let edges = "", nodes = "", tags = "";
  for (const c of st.commits) {
    const b = pos[c.id];
    for (const pid of c.parents) {
      const a = pos[pid];
      const d = a.y === b.y ? `M${a.x},${a.y} L${b.x},${b.y}` : `M${a.x},${a.y} C${a.x + stepX * 0.6},${a.y} ${b.x - stepX * 0.6},${b.y} ${b.x},${b.y}`;
      edges += `<path d="${d}" class="g-edge${reach.has(c.id) ? "" : " dead"}"/>`;
    }
  }
  for (const c of st.commits) {
    const { x, y } = pos[c.id];
    const cls = `g-node${reach.has(c.id) ? "" : " dead"}${fresh.has(c.id) ? " fresh" : ""}${c.parents.length > 1 ? " merge" : ""}`;
    nodes += `<g class="${cls}"><title>${esc(c.msg || c.label)}</title><circle cx="${x}" cy="${y}" r="15"/><text x="${x}" y="${y + 4}">${esc(c.label)}</text></g>`;
  }
  // ярлыки веток над коммитом; ветка, на которой HEAD, — подсвечена
  const at = {};
  for (const [name, id] of Object.entries(st.branches)) (at[id] ||= []).push(name);
  for (const [id, names] of Object.entries(at)) {
    const { x, y } = pos[id];
    names.sort((a, b) => (a === st.head ? -1 : b === st.head ? 1 : a.localeCompare(b)));
    names.forEach((name, k) => {
      const label = name === st.head ? `HEAD → ${name}` : name;
      const tw = label.length * 7 + 14;
      const ty = y - 26 - k * 20;
      const moved = prev && prev.branches[name] !== id;
      tags += `<g class="g-tag${name === st.head ? " head" : ""}${moved ? " moved" : ""}"><rect x="${x - tw / 2}" y="${ty - 13}" width="${tw}" height="18" rx="9"/><text x="${x}" y="${ty}">${esc(label)}</text></g>`;
    });
  }
  const top = Math.min(0, ...Object.entries(at).map(([id, names]) => pos[id].y - 26 - (names.length - 1) * 20 - 16));
  return `<svg class="viz-git" viewBox="${-10} ${top} ${w + 20} ${h - top}" width="${w + 20}" height="${h - top}">${edges}${nodes}${tags}</svg>`;
}


// ---------- общий кусок: код с текущей строкой ----------

// code — текст, line — текущая строка, call — строка, которая ждёт (например, next(g) пока работает генератор)
function codeView(code, line, call) {
  return `<pre class="viz-code flat">${String(code || "").split("\n").map((l, n) =>
    `<span class="ln${n + 1 === line ? " cur" : n + 1 === call ? " wait" : ""}">${highlight(l) || " "}</span>`).join("")}</pre>`;
}

// ---------- срезы: ползунки start / stop / step ----------
// {"type": "slice", "text": "Python", "start": 1, "stop": 4, "step": 1, "presets": ["[1:4]", "[::-1]"]}
// start/stop: число или null (не указан).

function sliceIndices(n, start, stop, step) {
  const norm = (v, lo, hi) => (v < 0 ? Math.max(v + n, lo) : Math.min(v, hi));
  const out = [];
  if (step > 0) {
    const a = start == null ? 0 : norm(start, 0, n), b = stop == null ? n : norm(stop, 0, n);
    for (let i = a; i < b; i += step) out.push(i);
  } else {
    const a = start == null ? n - 1 : norm(start, -1, n - 1), b = stop == null ? -1 : norm(stop, -1, n - 1);
    for (let i = a; i > b; i += step) out.push(i);
  }
  return out;
}

function sliceViz(box, spec) {
  // editable: своя строка или список; items: начать со списка
  let isList = Array.isArray(spec.items);
  let text = isList ? spec.items : [...String(spec.text || "Python")];
  let n = text.length;
  const st = { start: spec.start ?? null, stop: spec.stop ?? null, step: spec.step || 1 };
  const presets = spec.presets || ["[1:4]", "[:3]", "[-3:]", "[::2]", "[::-1]"];
  const listRaw = () => `[${text.map(pyFmt).join(", ")}]`;
  box.innerHTML = `${spec.title ? `<div class="viz-title">${esc(spec.title)}</div>` : ""}
    ${spec.editable ? `<div class="viz-slice-edit">
      <button class="viz-chip" data-mode="str">строка</button><button class="viz-chip" data-mode="list">список</button>
      <input class="viz-sb-input" autocapitalize="off" autocomplete="off" spellcheck="false"></div>` : ""}
    <div class="viz-slice-expr"></div>
    <div class="viz-slice-cells"></div>
    <div class="viz-legend"><span class="s"></span>start — откуда <span class="e"></span>stop — докуда (не входит) <em>1 2 3</em> — порядок</div>
    <div class="viz-slice-ctrl">
      ${["start", "stop", "step"].map((k) => `
        <label class="viz-slider"><span>${k}</span>
          <input type="range" data-k="${k}" step="1">
          <b data-v="${k}"></b>
          ${k === "step" ? "" : `<button class="viz-chip" data-none="${k}">пусто</button>`}</label>`).join("")}
    </div>
    <div class="viz-sb-quick">${presets.map((p) => `<button class="viz-chip" data-preset="${esc(p)}">${isList ? "nums" : "s"}${esc(p)}</button>`).join("")}</div>
    <div class="viz-note"></div>`;
  const parse = (p) => {
    const [a = "", b = "", c = ""] = p.replace(/^\[|\]$/g, "").split(":");
    return { start: a === "" ? null : Number(a), stop: b === "" ? null : Number(b), step: c === "" ? 1 : Number(c) };
  };
  const edit = box.querySelector(".viz-slice-edit input");
  const setRanges = () => {
    for (const k of ["start", "stop"]) {
      const inp = box.querySelector(`[data-k="${k}"]`);
      inp.min = -n; inp.max = n;
    }
    const sInp = box.querySelector('[data-k="step"]');
    sInp.min = -3; sInp.max = 3;
  };
  const show = () => {
    const v = isList ? "nums" : "s";
    const idx = sliceIndices(n, st.start, st.stop, st.step);
    const order = new Map(idx.map((i, k) => [i, k + 1]));
    const expr = `${v}[${st.start ?? ""}:${st.stop ?? ""}${st.step !== 1 ? `:${st.step}` : ""}]`;
    const res = isList ? pyFmt(idx.map((i) => text[i])) : pyRepr(idx.map((i) => text[i]).join(""));
    box.querySelector(".viz-slice-expr").innerHTML =
      `<code>${v} = ${esc(isList ? listRaw() : pyRepr(text.join("")))}</code><code class="res">${esc(expr)} → ${esc(res)}</code>`;
    box.querySelector(".viz-slice-cells").innerHTML = text.map((ch, i) => {
      const k = order.get(i);
      const edge = (i === (st.start == null ? null : (st.start < 0 ? st.start + n : st.start)) ? " is-start" : "")
        + (i === (st.stop == null ? null : (st.stop < 0 ? st.stop + n : st.stop)) ? " is-stop" : "");
      const shown = isList ? pyFmt(ch) : ch === " " ? "␣" : ch;
      return `<div class="viz-sc${k ? " on" : ""}${edge}"><i>${i}</i><b>${esc(shown)}</b><i>${i - n}</i>${k ? `<em>${k}</em>` : ""}</div>`;
    }).join("");
    box.querySelectorAll("[data-preset]").forEach((b) => (b.textContent = v + b.dataset.preset));
    for (const k of ["start", "stop", "step"]) {
      const input = box.querySelector(`[data-k="${k}"]`);
      input.value = st[k] ?? (k === "start" ? (st.step > 0 ? 0 : n - 1) : (st.step > 0 ? n : -n));
      input.classList.toggle("none", st[k] == null);
      box.querySelector(`[data-v="${k}"]`).textContent = st[k] ?? "пусто";
    }
    const dir = st.step > 0 ? "слева направо" : "справа налево";
    const what = isList ? ["элемент", "элемента", "элементов"] : ["символ", "символа", "символов"];
    const note = !n ? "Пусто — срезать нечего. Введи что-нибудь вверху."
      : !idx.length ? "Пустой срез: при таком шаге от start до stop не дойти — ошибки нет, просто пусто."
      : `Берём ${idx.length} ${plural(idx.length, ...what)} ${dir}${Math.abs(st.step) > 1 ? `, каждый ${Math.abs(st.step)}-й` : ""}. `
        + (st.step > 0 ? "`stop` не входит в срез." : "При отрицательном шаге пустой `start` — с конца, пустой `stop` — до самого начала.");
    box.querySelector(".viz-note").innerHTML = inline(note);
    box.querySelectorAll("[data-mode]").forEach((b) => b.classList.toggle("on", (b.dataset.mode === "list") === isList));
  };
  box.querySelectorAll("input[type=range]").forEach((inp) => (inp.oninput = () => {
    let v = Number(inp.value);
    if (inp.dataset.k === "step" && v === 0) v = st.step > 0 ? -1 : 1;
    st[inp.dataset.k] = v;
    show();
  }));
  box.querySelectorAll("[data-none]").forEach((b) => (b.onclick = () => { st[b.dataset.none] = null; show(); }));
  box.querySelectorAll("[data-preset]").forEach((b) => (b.onclick = () => { Object.assign(st, parse(b.dataset.preset)); show(); }));
  if (edit) {
    const fill = () => { edit.value = isList ? listRaw() : text.join(""); };
    edit.oninput = () => {
      if (isList) { try { text = pyParse(edit.value).slice(0, 16); } catch { return; } }
      else text = [...edit.value].slice(0, 16);
      n = text.length;
      setRanges();
      show();
    };
    box.querySelectorAll("[data-mode]").forEach((b) => (b.onclick = () => {
      const want = b.dataset.mode === "list";
      if (want === isList) return;
      isList = want;
      text = isList ? [10, 20, 30, 40, 50, 60] : [..."Python"];
      n = text.length;
      fill(); setRanges(); show();
    }));
    edit.maxLength = 60;
    fill();
  }
  setRanges();
  show();
}

function plural(n, one, few, many) {
  const m10 = n % 10, m100 = n % 100;
  return m10 === 1 && m100 !== 11 ? one : m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14) ? few : many;
}

// ---------- файловая система: cd, ls, pwd ----------
// {"type": "fs", "tree": {"home": {"anna": {"projects": {}}}, "notes.txt": null}, "home": "/home/anna",
//  "cwd": "/home/anna", "steps": ["pwd", {"cmd": "cd projects", "note": "…"}], "sandbox": true}
// В дереве папка — объект, файл — null.

function fsResolve(st, path) {
  if (path == null || path === "" || path === "~") return st.home;
  if (path === "-") return st.prev || st.cwd;
  let parts = path.startsWith("/") ? [] : (path.startsWith("~") ? st.home.split("/").filter(Boolean) : st.cwd.split("/").filter(Boolean));
  for (const p of path.replace(/^~/, "").split("/").filter(Boolean)) {
    if (p === ".") continue;
    if (p === "..") parts.pop();
    else parts.push(p);
  }
  return "/" + parts.join("/");
}

function fsNode(tree, path) {
  let node = tree;
  for (const p of path.split("/").filter(Boolean)) {
    if (!node || typeof node !== "object" || !(p in node)) return undefined;
    node = node[p];
  }
  return node;
}

function fsRun(prev, raw) {
  const st = { ...prev, tree: JSON.parse(JSON.stringify(prev.tree)) };
  const [cmd, ...args] = raw.trim().split(/\s+/);
  const arg = args.filter((a) => !a.startsWith("-") || a === "-")[0];
  if (cmd === "pwd") return { state: st, out: st.cwd };
  if (cmd === "cd") {
    const target = fsResolve(st, arg);
    const node = fsNode(st.tree, target);
    if (node === undefined) return { state: st, out: `cd: ${arg}: нет такой папки` };
    if (node === null) return { state: st, out: `cd: ${arg}: это файл, а не папка` };
    st.prev = st.cwd;
    st.cwd = target;
    return { state: st, out: arg === "-" ? target : "" };
  }
  if (cmd === "ls") {
    const target = fsResolve(st, arg ?? ".");
    const node = fsNode(st.tree, target);
    if (node === undefined) return { state: st, out: `ls: ${arg}: нет такого файла или папки` };
    if (node === null) return { state: st, out: arg };
    const all = args.includes("-a") || args.includes("-la") || args.includes("-al");
    const names = Object.keys(node).filter((k) => all || !k.startsWith(".")).sort();
    return { state: st, out: names.map((k) => (node[k] === null ? k : `${k}/`)).join("  ") };
  }
  if (cmd === "mkdir" || cmd === "touch") {
    if (!arg) return { state: st, out: `${cmd}: укажи имя` };
    const target = fsResolve(st, arg);
    const parent = fsNode(st.tree, target.split("/").slice(0, -1).join("/"));
    if (!parent || typeof parent !== "object") return { state: st, out: `${cmd}: нет папки для ${arg}` };
    const name = target.split("/").pop();
    if (!(name in parent)) parent[name] = cmd === "mkdir" ? {} : null;
    return { state: st, out: "" };
  }
  return { state: st, out: `${cmd}: в этой схеме есть pwd, cd, ls, mkdir, touch` };
}

function fsTree(st) {
  const rows = [];
  const walk = (node, path, depth) => {
    for (const name of Object.keys(node).sort((a, b) => (node[a] === null) - (node[b] === null) || a.localeCompare(b))) {
      const p = `${path}/${name}`;
      const isDir = node[name] !== null;
      const here = p === st.cwd, onPath = isDir && st.cwd.startsWith(p + "/");
      rows.push(`<div class="viz-fs-row${here ? " here" : ""}${onPath ? " path" : ""}" style="padding-left:${depth * 16 + 6}px">
        <span>${isDir ? "📁" : "📄"}</span><b>${esc(name)}${isDir ? "/" : ""}</b>${here ? `<em>ты здесь</em>` : ""}</div>`);
      if (isDir) walk(node[name], p, depth + 1);
    }
  };
  rows.push(`<div class="viz-fs-row${st.cwd === "/" ? " here" : ""}" style="padding-left:6px"><span>💾</span><b>/</b>${st.cwd === "/" ? `<em>ты здесь</em>` : ""}</div>`);
  walk(st.tree, "", 1);
  return rows.join("");
}

function fsViz(box, spec) {
  const start = { tree: spec.tree, home: spec.home || "/home/anna", cwd: spec.cwd || spec.home || "/", prev: null, log: [], note: spec.intro || "" };
  const states = [start];
  for (const step of spec.steps || []) {
    const cmd = typeof step === "string" ? step : step.cmd;
    const r = fsRun(states.at(-1), cmd);
    states.push({ ...r.state, log: [...states.at(-1).log, { cmd, out: r.out }], note: (typeof step === "object" && step.note) || "" });
  }
  const sandbox = spec.sandbox ? `
    <div class="viz-sandbox">
      <div class="viz-sb-head">Попробуй сам — введи команду:</div>
      <form class="viz-sb-form"><input class="viz-sb-input" placeholder="cd .." autocapitalize="off" autocomplete="off" spellcheck="false">
        <button class="viz-btn main">↵</button></form>
      <div class="viz-sb-quick">${["pwd", "ls", "cd ..", "cd ~", "cd -", "cd /"].map((c) => `<button class="viz-chip" data-cmd="${c}">${c}</button>`).join("")}</div>
    </div>` : "";
  let ctl = null;
  ctl = stepper(box, {
    title: spec.title,
    states,
    extra: sandbox,
    render(stage, st) {
      const log = st.log.slice(-4);
      stage.innerHTML = `<div class="viz-fs">
        <div class="viz-fs-tree">${fsTree(st)}</div>
        <div class="viz-term">${log.length ? log.map((l) => `<div><span>$</span> ${esc(l.cmd)}</div>${l.out ? `<pre>${esc(l.out)}</pre>` : ""}`).join("") : `<div class="muted">терминал пуст — нажми «Шаг»</div>`}
          <div class="viz-term-cwd">${esc(st.cwd)}</div></div></div>`;
    },
  });
  if (!spec.sandbox) return;
  const exec = (cmd) => {
    const cur = ctl.current;
    const r = fsRun(cur, cmd);
    ctl.push({ ...r.state, log: [...cur.log, { cmd, out: r.out }], note: "" });
  };
  const input = box.querySelector(".viz-sb-input");
  box.querySelector(".viz-sb-form").onsubmit = (e) => { e.preventDefault(); if (input.value.trim()) exec(input.value); input.value = ""; };
  box.querySelectorAll(".viz-sb-quick [data-cmd]").forEach((b) => (b.onclick = () => exec(b.dataset.cmd)));
}

// ---------- права доступа: галочки rwx ----------
// {"type": "perm", "file": "run_tests.sh", "value": "644"}

function permViz(box, spec) {
  const who = [["владелец", "u"], ["группа", "g"], ["остальные", "o"]];
  const bits = [["r", 4, "читать"], ["w", 2, "писать"], ["x", 1, "выполнять"]];
  let digits = String(spec.value || "644").split("").map(Number);
  box.innerHTML = `${spec.title ? `<div class="viz-title">${esc(spec.title)}</div>` : ""}
    <div class="viz-perm">
      <div class="viz-perm-grid">
        <div></div>${bits.map(([b, , t]) => `<div class="h"><b>${b}</b><i>${t}</i></div>`).join("")}<div class="h"><b>=</b></div>
        ${who.map(([w], r) => `<div class="w">${w}</div>${bits.map(([b, v]) =>
          `<button class="viz-bit" data-r="${r}" data-v="${v}">${b}</button>`).join("")}<div class="viz-digit" data-d="${r}"></div>`).join("")}
      </div>
      <div class="viz-perm-out"></div>
    </div>
    <div class="viz-sb-quick">${["755", "644", "600", "700", "777"].map((p) => `<button class="viz-chip" data-p="${p}">${p}</button>`).join("")}</div>
    <div class="viz-note"></div>`;
  const show = () => {
    box.querySelectorAll(".viz-bit").forEach((b) => b.classList.toggle("on", (digits[b.dataset.r] & b.dataset.v) > 0));
    box.querySelectorAll(".viz-digit").forEach((d) => (d.textContent = digits[d.dataset.d]));
    const str = digits.map((d) => bits.map(([b, v]) => (d & v ? b : "-")).join("")).join("");
    const oct = digits.join("");
    box.querySelector(".viz-perm-out").innerHTML =
      `<code>-${str}</code><code>chmod ${oct} ${esc(spec.file || "file")}</code>`;
    const hints = { "755": "Скрипты и папки: все могут запускать, менять — только владелец.", "644": "Обычные файлы: все читают, пишет только владелец.",
      "600": "Секреты (`.env`, ключи): только владелец, остальным ничего.", "777": "Всем всё — так делать не надо: любой может изменить файл.",
      "700": "Только владелец, зато всё." };
    box.querySelector(".viz-note").innerHTML = inline(hints[oct] || "Каждая цифра — сумма: `r`=4, `w`=2, `x`=1.");
  };
  box.querySelectorAll(".viz-bit").forEach((b) => (b.onclick = () => { digits[b.dataset.r] ^= Number(b.dataset.v); show(); }));
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => { digits = b.dataset.p.split("").map(Number); show(); }));
  show();
}

// ---------- фикстуры pytest: когда создаются и убираются ----------
// {"type": "fixtures", "fixtures": [{"name": "db", "scope": "module"}], "tests": [{"name": "test_a", "module": "test_x.py", "uses": ["db"]}]}
// Область видимости каждой фикстуры можно переключить прямо в схеме.

function fixtureEvents(fixtures, tests, failed = new Set(), afterYield = false) {
  const scope = Object.fromEntries(fixtures.map((f) => [f.name, f.scope]));
  const alive = [];
  const events = [];
  const count = {};
  const push = (e) => events.push({ ...e, alive: [...alive], count: { ...count } });
  let lastFail = false;
  const teardown = (pred) => {
    for (const f of [...alive].reverse()) {
      if (!pred(f)) continue;
      alive.splice(alive.indexOf(f), 1);
      push({ kind: "down", f, note: `Уборка \`${f}\` (scope=${scope[f]})${afterYield ? " — выполняется код после `yield`" : ""}.`
        + (lastFail ? " Тест упал, но уборка всё равно выполняется." : "") });
    }
  };
  tests.forEach((t, k) => {
    for (const f of t.uses) {
      if (alive.includes(f)) continue;
      alive.push(f);
      count[f] = (count[f] || 0) + 1;
      push({ kind: "up", f, test: t.name, note: `Создаётся \`${f}\` (scope=${scope[f]}) — его просит \`${t.name}\`.` });
    }
    lastFail = failed.has(t.name);
    push({ kind: "test", test: t.name, module: t.module, fail: lastFail,
      note: lastFail ? `\`${t.name}\` **упал** (assert не прошёл). Что будет с фикстурами?`
        : `Выполняется \`${t.name}\`${t.uses.length ? `, получает ${t.uses.map((f) => `\`${f}\``).join(", ")}` : ""}.` });
    teardown((f) => scope[f] === "function");
    const next = tests[k + 1];
    if (!next || next.module !== t.module) teardown((f) => scope[f] === "module");
  });
  teardown(() => true);
  return events;
}

function fixturesViz(box, spec) {
  const fixtures = spec.fixtures.map((f) => ({ ...f }));
  const failed = new Set(spec.fail || []);
  const build = () => {
    const events = fixtureEvents(fixtures, spec.tests, failed, !!spec.failable);
    const states = [{ idx: -1, alive: [], count: {}, note: "Нажимай «Шаг» и смотри, когда pytest создаёт и убирает фикстуры. Область видимости можно переключить вверху." },
      ...events.map((e, idx) => ({ ...e, idx }))];
    stepper(box, {
      title: spec.title,
      states,
      render(stage, st) {
        stage.innerHTML = `
          <div class="viz-fx-scopes">${fixtures.map((f, k) => `<label><b>${esc(f.name)}</b>
            <select data-k="${k}">${["function", "module", "session"].map((s) => `<option${s === f.scope ? " selected" : ""}>${s}</option>`).join("")}</select></label>`).join("")}</div>
          ${spec.failable ? `<div class="viz-fx-fail"><span>уронить тест:</span>${spec.tests.map((t) => `<button class="viz-par-val${failed.has(t.name) ? " bad" : ""}" data-fail="${esc(t.name)}">${failed.has(t.name) ? "✗" : "✓"} ${esc(t.name)}</button>`).join("")}</div>` : ""}
          <div class="viz-fx-alive"><span>сейчас живы:</span>${st.alive.length ? st.alive.map((f) => `<i>${esc(f)}</i>`).join("") : `<em>никого</em>`}</div>
          <ol class="viz-fx-log">${events.map((e, k) => `<li class="${e.kind}${e.fail ? " fail" : ""}${k === st.idx ? " cur" : k < st.idx ? " done" : ""}">${
            e.kind === "up" ? `▲ создать <b>${esc(e.f)}</b>` : e.kind === "down" ? `▼ убрать <b>${esc(e.f)}</b>` : `${e.fail ? "✗" : "▶"} <b>${esc(e.test)}</b> <small>${e.fail ? "упал" : esc(e.module)}</small>`}</li>`).join("")}</ol>
          <div class="viz-fx-count">${fixtures.map((f) => `<span><b>${esc(f.name)}</b> создан ${st.count[f.name] || 0} ${plural(st.count[f.name] || 0, "раз", "раза", "раз")}</span>`).join("")}</div>`;
        stage.querySelectorAll("select").forEach((sel) => (sel.onchange = () => { fixtures[sel.dataset.k].scope = sel.value; build(); }));
        stage.querySelectorAll("[data-fail]").forEach((b) => (b.onclick = () => { const t = b.dataset.fail; failed.has(t) ? failed.delete(t) : failed.add(t); build(); }));
        // прокрутить только сам список событий, не страницу
        const log = stage.querySelector(".viz-fx-log"), cur = log.querySelector("li.cur");
        if (cur) log.scrollTop = cur.offsetTop - log.clientHeight / 2;
      },
    });
  };
  build();
}

// ---------- CI: job-ы, needs и падения ----------
// {"type": "pipeline", "jobs": {"lint": {"needs": [], "min": 1}, "api": {"needs": ["lint"], "min": 6}}, "fail": ["api"]}
// Нажми на job — он «упадёт» (или снова пройдёт). Шаги — волны параллельного запуска.

function pipelineViz(box, spec) {
  const fail = new Set(spec.fail || []);
  const names = Object.keys(spec.jobs);
  const build = () => {
    const status = {}, finish = {}, waves = [];
    const done = new Set();
    while (done.size < names.length) {
      const wave = names.filter((j) => !done.has(j) && spec.jobs[j].needs.every((d) => done.has(d)));
      if (!wave.length) break;
      for (const j of wave) {
        const needs = spec.jobs[j].needs;
        if (needs.some((d) => status[d] !== "success")) { status[j] = "skipped"; finish[j] = Math.max(0, ...needs.map((d) => finish[d] || 0)); }
        else { status[j] = fail.has(j) ? "failure" : "success"; finish[j] = Math.max(0, ...needs.map((d) => finish[d])) + spec.jobs[j].min; }
      }
      wave.forEach((j) => done.add(j));
      waves.push(wave);
    }
    const total = Math.max(...names.map((j) => finish[j]));
    const serial = names.reduce((a, j) => a + (status[j] === "skipped" ? 0 : spec.jobs[j].min), 0);
    const states = [{ shown: 0, note: "Нажми на job, чтобы он «упал», и запусти пайплайн по шагам." }];
    const red = Object.values(status).includes("failure");
    const list = (js) => js.map((j) => `\`${j}\``).join(", ");
    waves.forEach((w, k) => {
      const ran = w.filter((j) => status[j] !== "skipped"), failed = w.filter((j) => status[j] === "failure"), skipped = w.filter((j) => status[j] === "skipped");
      let note = `Волна ${k + 1}: `;
      if (ran.length) note += `${list(ran)} ${ran.length > 1 ? "идут одновременно" : "выполняется"}.`;
      if (failed.length) note += ` ${list(failed)} ${failed.length > 1 ? "упали" : "упал"} — всё, что от ${failed.length > 1 ? "них" : "него"} зависит, будет пропущено.`;
      if (skipped.length) note += `${ran.length ? " " : ""}${list(skipped)} ${skipped.length > 1 ? "пропущены" : "пропущен"}: зависимость не прошла.`;
      if (k === waves.length - 1) {
        note += red ? " Итог: пайплайн **красный**." : ` Итог: **зелёный**, ${total} мин — job-ы без зависимостей шли параллельно (подряд было бы ${serial}).`;
      }
      states.push({ shown: k + 1, note });
    });
    stepper(box, {
      title: spec.title,
      states,
      render(stage, st) {
        stage.innerHTML = `<div class="viz-pipe">${waves.map((w, k) => `<div class="viz-wave"><span>волна ${k + 1}</span>${w.map((j) => {
          const s = k < st.shown ? status[j] : "wait";
          const icon = { success: "✓", failure: "✗", skipped: "⏭", wait: "…" }[s];
          return `<button class="viz-job ${s}${fail.has(j) ? " will-fail" : ""}" data-job="${esc(j)}">
            <b>${icon} ${esc(j)}</b><i>${spec.jobs[j].min} мин${spec.jobs[j].needs.length ? ` · после ${spec.jobs[j].needs.join(", ")}` : ""}</i></button>`;
        }).join("")}</div>`).join("")}</div>`;
        stage.querySelectorAll("[data-job]").forEach((b) => (b.onclick = () => {
          const j = b.dataset.job;
          fail.has(j) ? fail.delete(j) : fail.add(j);
          build();
        }));
      },
    });
  };
  build();
}

// ---------- HTTP: конструктор запроса к учебному API ----------
// {"type": "http", "items": [{"id": 1, "name": "Аня"}], "presets": ["GET /users", "POST /users"]}

function httpViz(box, spec) {
  let db = JSON.parse(JSON.stringify(spec.items || []));
  const presets = spec.presets || ["GET /users", "GET /users/1", "GET /users/99", "POST /users", "PATCH /users/1", "DELETE /users/2"];
  const bodies = { POST: '{"name": "Вика"}', PUT: '{"name": "Анна"}', PATCH: '{"name": "Анна"}' };
  const phrases = { 200: "OK", 201: "Created", 204: "No Content", 400: "Bad Request", 404: "Not Found", 405: "Method Not Allowed", 422: "Unprocessable Entity" };
  box.innerHTML = `${spec.title ? `<div class="viz-title">${esc(spec.title)}</div>` : ""}
    <div class="viz-http-form">
      <select class="viz-http-method">${["GET", "POST", "PUT", "PATCH", "DELETE"].map((m) => `<option>${m}</option>`).join("")}</select>
      <input class="viz-sb-input viz-http-path" value="/users/1" autocapitalize="off" spellcheck="false">
      <button class="viz-btn main viz-http-send">Отправить</button>
    </div>
    <textarea class="viz-sb-input viz-http-body" rows="2" spellcheck="false"></textarea>
    <div class="viz-sb-quick">${presets.map((p) => `<button class="viz-chip" data-p="${esc(p)}">${esc(p)}</button>`).join("")}
      <button class="viz-chip" data-reset>⟲ сбросить данные</button></div>
    <div class="viz-http-ex"></div>
    <div class="viz-note"></div>`;
  const method = box.querySelector(".viz-http-method"), path = box.querySelector(".viz-http-path"), body = box.querySelector(".viz-http-body");
  const syncBody = () => { body.hidden = !(method.value in bodies); };
  const serve = (m, p, raw) => {
    const mm = p.match(/^\/users(?:\/(\d+))?\/?$/);
    if (!mm) return [404, { detail: "Нет такого адреса" }];
    let data = null;
    if (m in bodies) {
      try { data = JSON.parse(raw || "{}"); } catch { return [400, { detail: "Тело — не JSON" }]; }
    }
    if (!mm[1]) {
      if (m === "GET") return [200, db];
      if (m === "POST") {
        if (!data.name || typeof data.name !== "string") return [422, { detail: "name: обязательное поле" }];
        const user = { id: Math.max(0, ...db.map((u) => u.id)) + 1, name: data.name };
        db.push(user);
        return [201, user, { Location: `/users/${user.id}` }];
      }
      return [405, { detail: `${m} для /users не поддерживается` }];
    }
    const id = Number(mm[1]);
    const user = db.find((u) => u.id === id);
    if (!user) return [404, { detail: `Пользователь ${id} не найден` }];
    if (m === "GET") return [200, user];
    if (m === "DELETE") { db = db.filter((u) => u.id !== id); return [204, null]; }
    if (m === "PUT") {
      if (!data.name) return [422, { detail: "name: обязательное поле" }];
      Object.keys(user).forEach((k) => k !== "id" && delete user[k]);
      Object.assign(user, data, { id });
      return [200, user];
    }
    if (m === "PATCH") { Object.assign(user, data, { id }); return [200, user]; }
    return [405, { detail: "Метод не поддерживается" }];
  };
  const send = () => {
    const m = method.value, p = path.value.trim() || "/";
    const raw = m in bodies ? body.value : "";
    const [code, data, extra = {}] = serve(m, p, raw);
    const reqHead = ["Host: api.test", "Authorization: Bearer t-123", ...(raw ? ["Content-Type: application/json"] : [])];
    const resBody = data == null ? "" : JSON.stringify(data, null, 2);
    const resHead = [...(resBody ? ["Content-Type: application/json"] : []), ...Object.entries(extra).map(([k, v]) => `${k}: ${v}`)];
    const part = (label, cls, text) => `<div class="viz-http-part ${cls}"><span>${label}</span><pre>${esc(text)}</pre></div>`;
    box.querySelector(".viz-http-ex").innerHTML = `
      <div class="viz-http-msg"><div class="viz-http-cap">Запрос</div>
        ${part("метод и путь", "line", `${m} ${p} HTTP/1.1`)}${part("заголовки", "head", reqHead.join("\n"))}${raw ? part("тело", "body", raw) : ""}</div>
      <div class="viz-http-msg"><div class="viz-http-cap">Ответ</div>
        ${part("код ответа", `line c${String(code)[0]}`, `HTTP/1.1 ${code} ${phrases[code] || ""}`)}${resHead.length ? part("заголовки", "head", resHead.join("\n")) : ""}${resBody ? part("тело", "body", resBody) : ""}</div>`;
    const notes = { 200: "Успех.", 201: "Ресурс создан — у него появился `id`, а в заголовке `Location` его адрес.", 204: "Удалено. У ответа **нет тела** — проверять нечего, кроме кода.",
      400: "Плохой запрос: тело не разобрать.", 404: "Такого ресурса нет — правильная реакция на неверный id.", 405: "Метод не подходит к этому адресу.",
      422: "Данные не прошли проверку — сервер объяснил, какое поле не так." };
    box.querySelector(".viz-note").innerHTML = inline(`**${code}**: ${notes[code] || ""}`);
  };
  method.onchange = () => { syncBody(); if (method.value in bodies && !body.value) body.value = bodies[method.value]; };
  box.querySelector(".viz-http-send").onclick = send;
  path.onkeydown = (e) => { if (e.key === "Enter") { e.preventDefault(); send(); } };
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => {
    const [m, p] = b.dataset.p.split(" ");
    method.value = m; path.value = p; body.value = bodies[m] || ""; syncBody(); send();
  }));
  box.querySelector("[data-reset]").onclick = () => { db = JSON.parse(JSON.stringify(spec.items || [])); box.querySelector(".viz-http-ex").innerHTML = ""; box.querySelector(".viz-note").innerHTML = inline("Данные вернулись к началу."); };
  syncBody();
  send();
}

// ---------- трассировка кода: строка, переменные, вывод ----------
// {"type": "trace", "code": "…", "steps": [{"line": 3, "vars": {"x": "1"}, "out": "…", "badge": "⏸ пауза на yield", "note": "…"}]}
// vars — изменения к прошлому шагу (null — удалить), значения — как их показать.

function traceViz(box, spec) {
  const states = [{ line: 0, vars: {}, out: [], badge: "", note: spec.intro || "" }];
  for (const step of spec.steps) {
    const prev = states.at(-1);
    const vars = { ...prev.vars };
    for (const [k, v] of Object.entries(step.vars || {})) v === null ? delete vars[k] : (vars[k] = v);
    const out = step.out != null ? [...prev.out, ...String(step.out).split("\n")] : prev.out;
    states.push({ line: step.line || 0, call: step.call || 0, vars, out, badge: step.badge ?? prev.badge, note: step.note || "" });
  }
  stepper(box, {
    title: spec.title,
    states,
    render(stage, st, prev) {
      const vars = Object.entries(st.vars);
      stage.innerHTML = `<div class="viz-mem">
        ${codeView(spec.code, st.line, st.call)}
        ${st.badge ? `<div class="viz-badge">${inline(st.badge)}</div>` : ""}
        <div class="viz-vars">${vars.length ? vars.map(([k, v]) =>
          `<div class="viz-kv${!prev || prev.vars[k] !== v ? " changed" : ""}"><b>${esc(k)}</b><span>${esc(String(v))}</span></div>`).join("")
          : `<div class="viz-empty">переменных пока нет</div>`}</div>
        ${st.out.length ? `<div class="viz-out"><span>Вывод</span><pre>${esc(st.out.join("\n"))}</pre></div>` : ""}</div>`;
    },
  });
}

// ---------- общие мелочи ----------

const vizHead = (spec) => (spec.title ? `<div class="viz-title">${esc(spec.title)}</div>` : "");
const tup = (...v) => ({ t: "tuple", v });
const pymod = (a, b) => ((a % b) + b) % b;
function pyFmt(v) {
  if (Array.isArray(v)) return `[${v.map(pyFmt).join(", ")}]`;
  if (v && v.t === "tuple") return `(${v.v.map(pyFmt).join(", ")}${v.v.length === 1 ? "," : ""})`;
  if (v && typeof v === "object") return `{${Object.entries(v).map(([k, x]) => `${pyRepr(k)}: ${pyFmt(x)}`).join(", ")}}`;
  return pyRepr(v);
}
const pyType = (v) => (v === null ? "NoneType" : Array.isArray(v) ? "list" : typeof v === "object" ? "dict"
  : typeof v === "boolean" ? "bool" : typeof v === "number" ? (Number.isInteger(v) ? "int" : "float") : "str");

// Python-литерал из поля ввода: [1, 2], (3,), "abc", range(5)
function pyParse(raw) {
  const s = String(raw).trim();
  if (/^(['"]).*\1$/.test(s)) return [...s.slice(1, -1)];
  const r = s.match(/^range\(\s*(-?\d+)\s*(?:,\s*(-?\d+)\s*)?(?:,\s*(-?\d+)\s*)?\)$/);
  if (r) {
    const [a, b, c] = r.slice(1).map((x) => (x == null ? null : Number(x)));
    const [st, en, sp] = b == null ? [0, a, 1] : [a, b, c ?? 1];
    const out = [];
    if (sp) for (let i = st; sp > 0 ? i < en : i > en; i += sp) { out.push(i); if (out.length > 200) break; }
    return out;
  }
  const js = s.replace(/'/g, '"').replace(/\(/g, "[").replace(/\)/g, "]")
    .replace(/\bTrue\b/g, "true").replace(/\bFalse\b/g, "false").replace(/\bNone\b/g, "null").replace(/,\s*([\]}])/g, "$1");
  const v = JSON.parse(js);
  if (!Array.isArray(v)) throw new Error("not a list");
  return v;
}

// ---------- Linux: конвейер из команд ----------
// {"type": "pipe", "files": {"app.log": "строка\nстрока"}, "cmd": "grep ERROR app.log | sort", "presets": ["…"]}
// Каждый этап можно выключить галочкой и посмотреть, что изменится.

function shTokens(cmd) {
  return (cmd.match(/'[^']*'|"[^"]*"|\S+/g) || []).map((t) => t.replace(/^(['"])(.*)\1$/, "$2"));
}

function shStage(cmd, input, files) {
  const [name, ...args] = shTokens(cmd);
  const flags = args.filter((a) => /^-[a-zA-Z]+$/.test(a)).join("").replace(/-/g, "");
  const plain = args.filter((a) => !/^-[a-zA-Z]+$/.test(a) && !/^-\d+$/.test(a));
  const optVal = (opt) => { const k = args.indexOf(opt); return k >= 0 ? args[k + 1] : null; };
  const fileOf = (rest) => rest.find((a) => a in files);
  const src = (file) => (file != null ? files[file].split("\n") : input);
  const num = (s) => { const m = String(s).trim().match(/^-?\d+(\.\d+)?/); return m ? Number(m[0]) : 0; };
  switch (name) {
    case "cat": {
      const missing = plain.find((a) => !(a in files));
      if (missing) return { err: `cat: ${missing}: нет такого файла` };
      return { out: plain.length ? plain.flatMap((f) => files[f].split("\n")) : input, file: plain[0] };
    }
    case "grep": {
      const [pat, file] = plain;
      if (pat == null) return { err: "grep: укажи, что искать" };
      let re;
      try { re = new RegExp(pat, flags.includes("i") ? "i" : ""); } catch { return { err: `grep: плохой шаблон ${pat}` }; }
      const hit = src(file).filter((l) => re.test(l) !== flags.includes("v"));
      return { out: flags.includes("c") ? [String(hit.length)] : hit, file };
    }
    case "sort": {
      const file = fileOf(plain);
      let out = [...src(file)];
      out.sort(flags.includes("n") ? (a, b) => num(a) - num(b) || (a < b ? -1 : a > b ? 1 : 0) : (a, b) => (a < b ? -1 : a > b ? 1 : 0));
      if (flags.includes("r")) out.reverse();
      if (flags.includes("u")) out = out.filter((l, k) => k === 0 || l !== out[k - 1]);
      return { out, file };
    }
    case "uniq": {
      const file = fileOf(plain);
      const groups = [];
      for (const l of src(file)) {
        if (groups.length && groups.at(-1)[0] === l) groups.at(-1)[1]++;
        else groups.push([l, 1]);
      }
      return { out: groups.map(([l, c]) => (flags.includes("c") ? `${String(c).padStart(7)} ${l}` : l)), file };
    }
    case "head": case "tail": {
      const short = args.find((a) => /^-\d+$/.test(a));
      const n = Number(optVal("-n") ?? (short ? short.slice(1) : 10));
      const file = fileOf(plain.filter((a) => a !== optVal("-n")));
      const lines = src(file);
      return { out: name === "head" ? lines.slice(0, n) : lines.slice(Math.max(0, lines.length - n)), file };
    }
    case "wc": {
      const file = fileOf(plain);
      return { out: [String(src(file).length) + (file ? ` ${file}` : "")], file };
    }
    case "cut": {
      const d = optVal("-d") ?? "\t", f = Number(optVal("-f"));
      if (!f) return { err: "cut: укажи поле: -f 2" };
      const file = fileOf(plain.filter((a) => a !== optVal("-d") && a !== optVal("-f")));
      return { out: src(file).map((l) => l.split(d)[f - 1] ?? ""), file };
    }
    case "awk": {
      const prog = plain[0] || "";
      const file = fileOf(plain.slice(1));
      const fields = (l) => l.trim().split(/\s+/);
      const pm = prog.match(/^\{\s*print\s+(.+?)\s*\}$/);
      if (pm) {
        const parts = pm[1].split(/\s*,\s*/).map((p) => p.match(/^\$(\d+)$/)?.[1]);
        if (parts.some((p) => p == null)) return { err: "awk: в схеме есть только {print $N}" };
        return { out: src(file).map((l) => parts.map((p) => (p === "0" ? l : fields(l)[p - 1] ?? "")).join(" ")), file };
      }
      return { err: "awk: в схеме есть только {print $N}" };
    }
    default:
      return { err: `${name}: в схеме есть cat, grep, sort, uniq, head, tail, wc, cut, awk` };
  }
}

const SH_NOTES = {
  cat: "выводит файл целиком",
  grep: (a) => (a.includes("-v") ? "оставляет строки **без** шаблона" : "оставляет только строки с шаблоном") + (a.includes("-c") ? " и считает их" : ""),
  sort: (a) => (/n/.test(a.join("")) ? "сортирует по числу в начале строки" : "сортирует строки") + (/-\w*r/.test(a.join(" ")) ? ", по убыванию" : ""),
  uniq: (a) => (a.join("").includes("c") ? "схлопывает **соседние** повторы и пишет, сколько их было" : "убирает **соседние** повторы"),
  head: "оставляет первые строки", tail: "оставляет последние строки",
  wc: "считает строки", cut: "вырезает столбец", awk: "берёт нужное поле (слово) из строки",
};

function pipeViz(box, spec) {
  const files = spec.files || {};
  const presets = spec.presets || [];
  let off = new Set();
  let sel = null;
  box.innerHTML = `${vizHead(spec)}
    ${Object.entries(files).map(([f, text]) => `<details class="viz-pipe-file"><summary>📄 ${esc(f)} — ${text.split("\n").length} строк</summary><pre>${esc(text)}</pre></details>`).join("")}
    <form class="viz-sb-form"><input class="viz-sb-input" value="${esc(spec.cmd || "")}" autocapitalize="off" autocomplete="off" spellcheck="false">
      <button class="viz-btn main">↵</button></form>
    ${presets.length ? `<div class="viz-sb-quick">${presets.map((p) => `<button class="viz-chip" data-p="${esc(p)}">${esc(p)}</button>`).join("")}</div>` : ""}
    <div class="viz-sh-stages"></div>
    <div class="viz-term viz-sh-out"></div>
    <div class="viz-note"></div>`;
  const input = box.querySelector(".viz-sb-input");
  const show = () => {
    const stages = input.value.split("|").map((s) => s.trim()).filter(Boolean);
    const res = [];
    let cur = [];
    let warn = "";
    stages.forEach((cmd, k) => {
      const before = cur;
      if (off.has(k)) {
        const r = shStage(cmd, cur, files);
        if (r.file) cur = files[r.file].split("\n");
        res.push({ cmd, off: true, out: cur });
        return;
      }
      const r = shStage(cmd, cur, files);
      if (r.err) { res.push({ cmd, err: r.err, out: [] }); cur = []; return; }
      if (cmd.startsWith("uniq") && !warn) {
        const src = r.file ? files[r.file].split("\n") : before;
        const sorted = src.every((l, i) => i === 0 || src[i - 1] <= l);
        if (!sorted && new Set(src).size < src.length) warn = "⚠ `uniq` получил **неотсортированные** строки: одинаковые стоят не рядом, поэтому посчитаны кусками. Вот зачем перед `uniq` ставят `sort`.";
      }
      cur = r.out;
      res.push({ cmd, out: cur });
    });
    if (sel == null || sel >= res.length) sel = res.length - 1;
    box.querySelector(".viz-sh-stages").innerHTML = res.map((r, k) => `
      <div class="viz-sh-stage${r.off ? " off" : ""}${r.err ? " err" : ""}${k === sel ? " sel" : ""}" data-k="${k}">
        <label title="включить или выключить этап"><input type="checkbox" data-t="${k}"${r.off ? "" : " checked"}></label>
        <code>${k ? "| " : ""}${esc(r.cmd)}</code>
        <span>${r.err ? "ошибка" : r.off ? "выключен" : `${r.out.length} ${plural(r.out.length, "строка", "строки", "строк")}`}</span></div>`).join("");
    const r = res[sel];
    const lines = r ? r.out : [];
    box.querySelector(".viz-sh-out").innerHTML = r
      ? `<div class="muted">после этапа ${sel + 1}: <b>${esc(r.cmd.split(" ")[0])}</b></div>${r.err ? `<pre class="err">${esc(r.err)}</pre>`
        : `<pre>${esc(lines.slice(0, 12).join("\n")) || "(пусто)"}${lines.length > 12 ? `\n… ещё ${lines.length - 12}` : ""}</pre>`}`
      : `<div class="muted">введи команду</div>`;
    let note = "";
    if (r && !r.err) {
      const [name, ...args] = shTokens(r.cmd);
      const d = SH_NOTES[name];
      note = r.off ? `Этап выключен — данные проходят мимо него без изменений.` : d ? `\`${name}\` ${typeof d === "function" ? d(args) : d}.` : "";
    }
    box.querySelector(".viz-note").innerHTML = inline([warn, note].filter(Boolean).join(" ") + " Нажми на этап, чтобы увидеть данные после него; галочка выключает этап.");
    box.querySelectorAll("[data-k]").forEach((el) => (el.onclick = (e) => { if (e.target.closest("label")) return; sel = Number(el.dataset.k); show(); }));
    box.querySelectorAll("[data-t]").forEach((cb) => (cb.onchange = () => { const k = Number(cb.dataset.t); cb.checked ? off.delete(k) : off.add(k); sel = k; show(); }));
  };
  box.querySelector(".viz-sb-form").onsubmit = (e) => { e.preventDefault(); off = new Set(); sel = null; show(); };
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => { input.value = b.dataset.p; off = new Set(); sel = null; show(); }));
  show();
}

// ---------- Linux: > и >> в файл ----------
// {"type": "redirect", "files": {"notes.txt": "привет"}, "steps": ["echo старт > progress.log", {"cmd": "cat progress.log", "note": "…"}], "sandbox": true}

function redirRun(prev, raw) {
  const files = { ...prev.files };
  const m = raw.trim().match(/^(.*?)\s*(>>|>)\s*(\S+)$/);
  const left = (m ? m[1] : raw).trim();
  // файл для > и >> создаётся (а для > ещё и очищается) до запуска команды
  if (m) files[m[3]] = m[2] === ">>" && m[3] in files ? files[m[3]] : "";
  let out = "", err = "";
  if (left) {
    const [name, ...args] = shTokens(left);
    if (name === "echo") out = args.join(" ");
    else if (name === "cat") {
      const miss = args.find((a) => !(a in files));
      if (miss) err = `cat: ${miss}: нет такого файла`;
      else out = args.map((a) => files[a]).filter((t) => t !== "").join("\n");
    } else if (name === "ls") out = Object.keys(files).sort().join("\n");
    else if (name === "wc" && args[0] === "-l") {
      if (!(args[1] in files)) err = `wc: ${args[1] || ""}: нет такого файла`;
      else out = `${files[args[1]] === "" ? 0 : files[args[1]].split("\n").length} ${args[1]}`;
    } else if (name === "rm") {
      args.forEach((a) => delete files[a]);
    } else err = `${name}: в схеме есть echo, cat, ls, wc -l, rm`;
  }
  if (!m) return { files, out: [out, err].filter(Boolean).join("\n"), changed: null };
  const [, , op, file] = m;
  const base = files[file] ?? "";
  files[file] = out === "" ? base : base === "" ? out : `${base}\n${out}`;
  return { files, out: err, changed: file, op };
}

function redirectViz(box, spec) {
  const start = { files: { ...(spec.files || {}) }, log: [], changed: null, note: spec.intro || "" };
  const states = [start];
  for (const step of spec.steps || []) {
    const cmd = typeof step === "string" ? step : step.cmd;
    const r = redirRun(states.at(-1), cmd);
    states.push({ files: r.files, changed: r.changed, op: r.op, log: [...states.at(-1).log, { cmd, out: r.out }], note: (typeof step === "object" && step.note) || "" });
  }
  const quick = spec.quick || ["echo привет > a.txt", "echo ещё >> a.txt", "cat a.txt", "ls > files.txt", "cat nope.txt > out.txt"];
  const sandbox = spec.sandbox ? `
    <div class="viz-sandbox">
      <div class="viz-sb-head">Попробуй сам:</div>
      <form class="viz-sb-form"><input class="viz-sb-input" placeholder="echo текст >> файл" autocapitalize="off" autocomplete="off" spellcheck="false">
        <button class="viz-btn main">↵</button></form>
      <div class="viz-sb-quick">${quick.map((c) => `<button class="viz-chip" data-cmd="${esc(c)}">${esc(c)}</button>`).join("")}</div>
    </div>` : "";
  let ctl = null;
  ctl = stepper(box, {
    title: spec.title,
    states,
    extra: sandbox,
    render(stage, st) {
      const log = st.log.slice(-4);
      const names = Object.keys(st.files).sort();
      stage.innerHTML = `<div class="viz-fs">
        <div class="viz-term">${log.length ? log.map((l) => `<div><span>$</span> ${esc(l.cmd)}</div>${l.out ? `<pre>${esc(l.out)}</pre>` : ""}`).join("") : `<div class="muted">терминал пуст — нажми «Шаг»</div>`}</div>
        <div class="viz-files">${names.length ? names.map((f) => `<div class="viz-file${f === st.changed ? ` changed ${st.op === ">" ? "over" : "app"}` : ""}">
          <div class="viz-file-name">📄 ${esc(f)}${f === st.changed ? `<em>${st.op === ">" ? "перезаписан" : "дописан"}</em>` : ""}</div>
          <pre>${st.files[f] === "" ? `<i>(пусто)</i>` : esc(st.files[f])}</pre></div>`).join("") : `<div class="viz-empty">файлов нет</div>`}</div></div>`;
    },
  });
  if (!spec.sandbox) return;
  const exec = (cmd) => {
    const cur = ctl.current;
    const r = redirRun(cur, cmd);
    ctl.push({ files: r.files, changed: r.changed, op: r.op, log: [...cur.log, { cmd, out: r.out }],
      note: r.changed ? (r.op === ">" ? "`>` — файл **перезаписан**: старое содержимое пропало." : "`>>` — строка **дописана** в конец.") : "" });
  };
  const input = box.querySelector(".viz-sb-input");
  box.querySelector(".viz-sb-form").onsubmit = (e) => { e.preventDefault(); if (input.value.trim()) exec(input.value); input.value = ""; };
  box.querySelectorAll(".viz-sb-quick [data-cmd]").forEach((b) => (b.onclick = () => exec(b.dataset.cmd)));
}

// ---------- pytest: отбор тестов -k и -m ----------
// {"type": "select", "tests": [{"name": "test_login", "file": "test_auth.py", "marks": ["smoke"]}], "mode": "m", "expr": "smoke",
//  "presets": {"m": ["smoke", "not slow"], "k": ["login"]}}

function boolExpr(expr, hit) {
  const toks = expr.match(/\(|\)|[^\s()]+/g) || [];
  let i = 0;
  const peek = () => toks[i];
  const atom = () => {
    const t = toks[i++];
    if (t == null) throw new Error("выражение оборвалось");
    if (t === "(") { const v = or(); if (toks[i++] !== ")") throw new Error("нет закрывающей скобки"); return v; }
    if (t === ")" || t === "and" || t === "or") throw new Error(`неожиданное «${t}»`);
    if (t === "not") return !atom();
    return hit(t);
  };
  const and = () => { let v = atom(); while (peek() === "and") { i++; const r = atom(); v = v && r; } return v; };
  const or = () => { let v = and(); while (peek() === "or") { i++; const r = and(); v = v || r; } return v; };
  if (!toks.length) return true;
  const v = or();
  if (i < toks.length) throw new Error(`лишнее «${toks[i]}»`);
  return v;
}

function selectViz(box, spec) {
  let mode = spec.mode || "m";
  const presets = spec.presets || { m: [], k: [] };
  box.innerHTML = `${vizHead(spec)}
    <div class="viz-sel-mode">${["m", "k"].map((m) => `<button class="viz-chip" data-m="${m}">-${m} ${m === "m" ? "по маркерам" : "по имени"}</button>`).join("")}</div>
    <form class="viz-sb-form"><span class="viz-sel-cmd"></span><input class="viz-sb-input" value="${esc(spec.expr || "")}" autocapitalize="off" autocomplete="off" spellcheck="false"></form>
    <div class="viz-sb-quick viz-sel-presets"></div>
    <div class="viz-sel-list"></div>
    <div class="viz-note"></div>`;
  const input = box.querySelector(".viz-sb-input");
  const show = () => {
    box.querySelectorAll("[data-m]").forEach((b) => b.classList.toggle("on", b.dataset.m === mode));
    box.querySelector(".viz-sel-cmd").textContent = `pytest -${mode}`;
    box.querySelector(".viz-sel-presets").innerHTML = (presets[mode] || []).map((p) => `<button class="viz-chip" data-p="${esc(p)}">${esc(p)}</button>`).join("");
    box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => { input.value = b.dataset.p; show(); }));
    let err = "";
    const picked = spec.tests.map((t) => {
      try {
        return boolExpr(input.value.trim(), (w) => (mode === "m" ? t.marks.includes(w)
          : `${t.file || ""}::${t.name}`.toLowerCase().includes(w.toLowerCase())));
      } catch (e) { err = e.message; return false; }
    });
    const n = picked.filter(Boolean).length;
    box.querySelector(".viz-sel-list").innerHTML = spec.tests.map((t, k) => `
      <div class="viz-sel-row${picked[k] ? " on" : ""}"><b>${picked[k] ? "✓" : "–"}</b>
        <code><small>${esc(t.file || "")}::</small>${esc(t.name)}</code>
        <span>${t.marks.map((m) => `<i>@${esc(m)}</i>`).join("")}</span></div>`).join("");
    const expr = input.value.trim();
    box.querySelector(".viz-note").innerHTML = inline(err ? `Ошибка в выражении: ${err}.`
      : !expr ? "Пустое выражение — запустятся все тесты."
      : `\`pytest -${mode} "${expr}"\`: collected ${spec.tests.length}, **${n} selected**, ${spec.tests.length - n} deselected. `
        + (mode === "m" ? "`-m` смотрит только на маркеры теста." : "`-k` ищет слово как подстроку в имени теста и файла, без учёта регистра."));
  };
  box.querySelectorAll("[data-m]").forEach((b) => (b.onclick = () => { mode = b.dataset.m; input.value = (presets[mode] || [""])[0]; show(); }));
  input.oninput = show;
  box.querySelector(".viz-sb-form").onsubmit = (e) => e.preventDefault();
  show();
}

// ---------- pytest: parametrize и id тестов ----------
// {"type": "params", "func": "test_home", "decorators": [{"name": "browser", "values": ["chrome", "firefox"]}, …]}
// Декораторы в порядке, как в коде (сверху вниз). Нажми на значение — выключить его.

function paramId(v) {
  if (Array.isArray(v)) return v.map(paramId).join("-");
  return v === null ? "None" : v === true ? "True" : v === false ? "False" : String(v);
}

function paramsViz(box, spec) {
  const decs = spec.decorators.map((d) => ({ ...d, on: d.values.map(() => true) }));
  const show = () => {
    const act = decs.map((d) => d.values.filter((_, k) => d.on[k]));
    // ближайший к функции декоратор — первый в id и меняется медленнее всех
    const order = [...act.keys()].reverse();
    let ids = [[]];
    for (const di of order) ids = ids.flatMap((pre) => act[di].map((v) => [...pre, paramId(v)]));
    const tests = act.some((a) => !a.length) ? [] : ids.map((p) => `${spec.func}[${p.join("-")}]`);
    const formula = act.map((a) => a.length).join(" × ");
    box.innerHTML = `${vizHead(spec)}
      <div class="viz-par-code">${decs.map((d, di) => `<div><span class="kw">@pytest.mark.parametrize</span>(<s>"${esc(d.name)}"</s>, [${
        d.values.map((v, k) => `<button class="viz-par-val${d.on[k] ? " on" : ""}" data-d="${di}" data-k="${k}">${esc(pyFmt(v))}</button>`).join("")}])</div>`).join("")}
        <div><span class="kw">def</span> ${esc(spec.func)}(${decs.map((d) => esc(d.name)).join(", ")}):</div></div>
      <div class="viz-par-count">${decs.length > 1 ? `${formula} = ` : ""}<b>${tests.length}</b> ${plural(tests.length, "тест", "теста", "тестов")}</div>
      <div class="viz-par-ids">${tests.map((t) => `<code>${esc(t)}</code>`).join("") || `<span class="viz-empty">ни одного набора — тест будет пропущен</span>`}</div>
      <div class="viz-note"></div>`;
    box.querySelector(".viz-note").innerHTML = inline(decs.length > 1
      ? "Нажимай на значения, чтобы выключать их. Id собирается из значений через `-`: первым идёт значение **нижнего** декоратора (ближнего к функции)."
      : "Нажимай на значения, чтобы выключать их. Каждое значение — отдельный тест со своим id в квадратных скобках.");
    box.querySelectorAll(".viz-par-val").forEach((b) => (b.onclick = () => { const d = decs[b.dataset.d]; d.on[b.dataset.k] = !d.on[b.dataset.k]; show(); }));
  };
  show();
}

// ---------- JSON-ответ: нажми на поле — получишь путь в Python ----------
// {"type": "json", "var": "body", "data": {…}}

function jsonViz(box, spec) {
  const name = spec.var || "data";
  let sel = spec.select || [];
  const rows = [];
  const lit = (v) => (v === null ? "null" : typeof v === "string" ? JSON.stringify(v) : String(v));
  const walk = (v, path, depth, key, last) => {
    const label = key == null ? "" : typeof key === "number" ? "" : `<s>${esc(JSON.stringify(key))}</s>: `;
    const comma = last ? "" : ",";
    const p = esc(JSON.stringify(path));
    if (v && typeof v === "object") {
      const arr = Array.isArray(v);
      const entries = arr ? v.map((x, k) => [k, x]) : Object.entries(v);
      rows.push(`<div class="viz-js-row" data-p="${p}" style="padding-left:${depth * 14 + 8}px">${label}${arr ? "[" : "{"}${entries.length ? "" : (arr ? "]" : "}") + comma}</div>`);
      entries.forEach(([k, x], i) => walk(x, [...path, k], depth + 1, k, i === entries.length - 1));
      if (entries.length) rows.push(`<div class="viz-js-row close" style="padding-left:${depth * 14 + 8}px">${arr ? "]" : "}"}${comma}</div>`);
    } else {
      rows.push(`<div class="viz-js-row" data-p="${p}" style="padding-left:${depth * 14 + 8}px">${label}<em class="${v === null ? "nul" : typeof v}">${esc(lit(v))}</em>${comma}</div>`);
    }
  };
  walk(spec.data, [], 0, null, true);
  box.innerHTML = `${vizHead(spec)}<div class="viz-js-tree">${rows.join("")}</div><div class="viz-js-out"></div><div class="viz-note"></div>`;
  const get = (path) => path.reduce((v, k) => v[k], spec.data);
  const show = () => {
    const key = JSON.stringify(sel);
    box.querySelectorAll(".viz-js-row[data-p]").forEach((r) => {
      const p = r.dataset.p;
      r.classList.toggle("sel", p === key);
      r.classList.toggle("in", p !== key && p.startsWith(key.slice(0, -1)) && sel.length > 0);
    });
    const v = get(sel);
    const strict = name + sel.map((k) => `[${typeof k === "number" ? k : JSON.stringify(k)}]`).join("");
    let safe = name;
    sel.forEach((k, i) => {
      const last = i === sel.length - 1;
      const parent = get(sel.slice(0, i));
      safe += typeof k === "number" ? `[${k}]` : `.get(${JSON.stringify(k)}${last ? "" : Array.isArray(parent[k]) ? ", []" : ", {}"})`;
    });
    const out = box.querySelector(".viz-js-out");
    out.innerHTML = `<div class="viz-js-expr"><code>${esc(strict)}</code><b>→</b><code class="res">${esc(pyFmt(v))}</code><i>${pyType(v)}</i></div>
      ${sel.some((k) => typeof k === "string") ? `<div class="viz-js-expr"><code>${esc(safe)}</code><small>без KeyError</small></div>` : ""}`;
    const hint = !sel.length ? "Нажми на любое поле — увидишь, как до него добраться в Python."
      : v === null ? "`null` в JSON стал `None`. Дальше по нему не пройти — подстрахуйся `or {}`."
      : typeof v === "boolean" ? "`true`/`false` в JSON — это `True`/`False` в Python."
      : Array.isArray(v) ? "Массив стал списком: дальше — индексы `[0]`, `[1]`, `len(...)`."
      : typeof v === "object" ? "Объект стал словарём: дальше — ключи в квадратных скобках."
      : "Каждый шаг пути — ключ словаря (строка) или индекс списка (число).";
    box.querySelector(".viz-note").innerHTML = inline(hint);
  };
  box.querySelectorAll(".viz-js-row[data-p]").forEach((r) => (r.onclick = () => { sel = JSON.parse(r.dataset.p); show(); }));
  show();
}

// ---------- Pydantic: проверка данных моделью ----------
// {"type": "schema", "model": "User", "fields": [{"name": "id", "type": "int"}, {"name": "active", "type": "bool", "default": true}],
//  "data": "{\"id\": \"abc\"}", "presets": {"имя": "{…}"}}

function pdField(type, v) {
  const fail = (t, msg) => ({ err: t, msg });
  if (type === "int") {
    if (typeof v === "boolean") return { val: Number(v) };
    if (typeof v === "number") return Number.isInteger(v) ? { val: v } : fail("int_from_float", "Input should be a valid integer, got a number with a fractional part");
    if (typeof v === "string") return /^\s*[-+]?\d+\s*$/.test(v) ? { val: Number(v) } : fail("int_parsing", "Input should be a valid integer, unable to parse string as an integer");
    return fail("int_type", "Input should be a valid integer");
  }
  if (type === "float") {
    if (typeof v === "number") return { val: v };
    if (typeof v === "string" && v.trim() !== "" && !isNaN(Number(v))) return { val: Number(v) };
    return typeof v === "string" ? fail("float_parsing", "Input should be a valid number, unable to parse string as a number") : fail("float_type", "Input should be a valid number");
  }
  if (type === "str") return typeof v === "string" ? { val: v } : fail("string_type", "Input should be a valid string");
  if (type === "bool") {
    if (typeof v === "boolean") return { val: v };
    if (v === 0 || v === 1) return { val: v === 1 };
    if (typeof v === "string") {
      const s = v.toLowerCase();
      if (["true", "1", "yes", "y", "on", "t"].includes(s)) return { val: true };
      if (["false", "0", "no", "n", "off", "f"].includes(s)) return { val: false };
    }
    return typeof v === "string" || typeof v === "number" ? fail("bool_parsing", "Input should be a valid boolean, unable to interpret input") : fail("bool_type", "Input should be a valid boolean");
  }
  return { val: v };
}

function schemaViz(box, spec) {
  const model = spec.model || "User";
  const presets = spec.presets || {};
  box.innerHTML = `${vizHead(spec)}
    <pre class="viz-code flat viz-sch-model"></pre>
    <label class="viz-sch-opt"><input type="checkbox" class="viz-sch-forbid"> <code>extra="forbid"</code> — лишние поля запрещены</label>
    <div class="viz-sb-head">Данные (JSON) — меняй прямо здесь:</div>
    <textarea class="viz-sb-input viz-sch-data" rows="3" spellcheck="false" autocapitalize="off">${esc(spec.data || "{}")}</textarea>
    <div class="viz-sb-quick">${Object.keys(presets).map((k) => `<button class="viz-chip" data-p="${esc(k)}">${esc(k)}</button>`).join("")}</div>
    <div class="viz-term viz-sch-out"></div>
    <div class="viz-note"></div>`;
  const forbid = box.querySelector(".viz-sch-forbid"), area = box.querySelector(".viz-sch-data");
  const show = () => {
    const code = [`class ${model}(BaseModel):`, ...(forbid.checked ? [`    model_config = ConfigDict(extra="forbid")`] : []),
      ...spec.fields.map((f) => `    ${f.name}: ${f.type}${"default" in f ? ` = ${pyFmt(f.default)}` : ""}`)].join("\n");
    box.querySelector(".viz-sch-model").innerHTML = code.split("\n").map((l) => `<span class="ln">${highlight(l)}</span>`).join("");
    const out = box.querySelector(".viz-sch-out"), note = box.querySelector(".viz-note");
    let data;
    try { data = JSON.parse(area.value); } catch {
      out.innerHTML = `<pre class="err">json.decoder.JSONDecodeError</pre>`;
      note.innerHTML = inline("Это не JSON — до Pydantic дело не дошло. Проверь кавычки (только двойные) и запятые.");
      return;
    }
    if (!data || typeof data !== "object" || Array.isArray(data)) {
      out.innerHTML = `<pre class="err">1 validation error for ${esc(model)}\n  Input should be a valid dictionary or instance of ${esc(model)} [type=model_type, input_value=${esc(pyFmt(data))}, input_type=${pyType(data)}]</pre>`;
      note.innerHTML = inline("Модель ждёт объект `{…}`.");
      return;
    }
    const errs = [], obj = {};
    for (const f of spec.fields) {
      if (!(f.name in data)) {
        if ("default" in f) obj[f.name] = f.default;
        else errs.push({ loc: f.name, type: "missing", msg: "Field required", input: data });
        continue;
      }
      const r = pdField(f.type, data[f.name]);
      if (r.err) errs.push({ loc: f.name, type: r.err, msg: r.msg, input: data[f.name] });
      else obj[f.name] = r.val;
    }
    const extra = Object.keys(data).filter((k) => !spec.fields.some((f) => f.name === k));
    if (forbid.checked) extra.forEach((k) => errs.push({ loc: k, type: "extra_forbidden", msg: "Extra inputs are not permitted", input: data[k] }));
    if (errs.length) {
      out.innerHTML = `<pre class="err">${esc(`${errs.length} validation error${errs.length > 1 ? "s" : ""} for ${model}\n` + errs.map((e) =>
        `${e.loc}\n  ${e.msg} [type=${e.type}, input_value=${pyFmt(e.input)}, input_type=${pyType(e.input)}]`).join("\n"))}</pre>`;
      note.innerHTML = inline(`\`ValidationError\`: ${errs.length} ${plural(errs.length, "ошибка", "ошибки", "ошибок")} сразу. В \`e.errors()\` — ${errs.map((e) => `\`('${e.loc}',) ${e.type}\``).join(", ")}.`);
    } else {
      const coerced = spec.fields.filter((f) => f.name in data && JSON.stringify(data[f.name]) !== JSON.stringify(obj[f.name])).map((f) => f.name);
      out.innerHTML = `<pre class="ok">${esc(`${model}(${spec.fields.map((f) => `${f.name}=${pyFmt(obj[f.name])}`).join(", ")})`)}</pre>`;
      note.innerHTML = inline("Данные прошли проверку." + (coerced.length ? ` Pydantic **привёл** ${coerced.map((c) => `\`${c}\``).join(", ")} к нужному типу.` : "")
        + (extra.length && !forbid.checked ? ` Лишнее (${extra.map((c) => `\`${c}\``).join(", ")}) молча отброшено — включи \`extra="forbid"\`, чтобы это ловить.` : ""));
    }
  };
  area.oninput = show;
  forbid.onchange = show;
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => { area.value = presets[b.dataset.p]; show(); }));
  show();
}

// ---------- CI: матрица ----------
// {"type": "matrix", "axes": {"os": ["ubuntu-latest"], "browser": ["chromium"]}, "exclude": [{…}], "include": [{…}]}

function matrixViz(box, spec) {
  const axes = Object.entries(spec.axes).map(([k, vals]) => ({ k, vals, on: vals.map(() => true) }));
  const exc = (spec.exclude || []).map((e) => ({ e, on: true }));
  const inc = (spec.include || []).map((e) => ({ e, on: true }));
  const fmt = (o) => Object.entries(o).map(([k, v]) => `${k}: ${v}`).join(", ");
  const show = () => {
    let combos = [{}];
    for (const a of axes) combos = combos.flatMap((c) => a.vals.filter((_, i) => a.on[i]).map((v) => ({ ...c, [a.k]: v })));
    const base = combos.length;
    const match = (c, e) => Object.entries(e).every(([k, v]) => c[k] === v);
    const excluded = combos.filter((c) => exc.some((x) => x.on && match(c, x.e)));
    combos = combos.filter((c) => !excluded.includes(c)).map((c) => ({ ...c, _from: "base" }));
    let added = 0;
    for (const x of inc.filter((x) => x.on)) {
      const orig = Object.entries(x.e).filter(([k]) => axes.some((a) => a.k === k));
      const hits = combos.filter((c) => c._from === "base" && orig.every(([k, v]) => c[k] === v));
      if (hits.length && orig.length) hits.forEach((c) => Object.assign(c, x.e));
      else { combos.push({ ...x.e, _from: "inc" }); added++; }
    }
    box.innerHTML = `${vizHead(spec)}
      <div class="viz-mx-axes">${axes.map((a, ai) => `<div class="viz-mx-axis"><b>${esc(a.k)}:</b>${a.vals.map((v, i) =>
        `<button class="viz-par-val${a.on[i] ? " on" : ""}" data-a="${ai}" data-i="${i}">${esc(v)}</button>`).join("")}</div>`).join("")}
        ${exc.map((x, i) => `<label class="viz-mx-rule exc"><input type="checkbox" data-x="${i}"${x.on ? " checked" : ""}> <b>exclude</b> ${esc(fmt(x.e))}</label>`).join("")}
        ${inc.map((x, i) => `<label class="viz-mx-rule inc"><input type="checkbox" data-n="${i}"${x.on ? " checked" : ""}> <b>include</b> ${esc(fmt(x.e))}</label>`).join("")}</div>
      <div class="viz-par-count">${axes.map((a) => a.on.filter(Boolean).length).join(" × ")} = ${base}${excluded.length ? ` − ${excluded.length}` : ""}${added ? ` + ${added}` : ""} = <b>${combos.length}</b> ${plural(combos.length, "запуск", "запуска", "запусков")}</div>
      <div class="viz-mx-jobs">${combos.map((c) => `<div class="viz-mx-job${c._from === "inc" ? " inc" : ""}">${Object.entries(c).filter(([k]) => k !== "_from").map(([, v]) => esc(v)).join(" · ")}</div>`).join("")}
        ${excluded.map((c) => `<div class="viz-mx-job exc">${Object.values(c).map(esc).join(" · ")}</div>`).join("")}</div>
      <div class="viz-note">${inline("Нажимай на значения и галочки. Зачёркнутое убрал `exclude`, отмеченное «+» добавил `include`.")}</div>`;
    box.querySelectorAll("[data-a]").forEach((b) => (b.onclick = () => {
      const a = axes[b.dataset.a];
      if (a.on[b.dataset.i] && a.on.filter(Boolean).length === 1) return;
      a.on[b.dataset.i] = !a.on[b.dataset.i];
      show();
    }));
    box.querySelectorAll("[data-x]").forEach((cb) => (cb.onchange = () => { exc[cb.dataset.x].on = cb.checked; show(); }));
    box.querySelectorAll("[data-n]").forEach((cb) => (cb.onchange = () => { inc[cb.dataset.n].on = cb.checked; show(); }));
  };
  show();
}

// ---------- CI: запустится ли workflow ----------
// {"type": "trigger", "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"], "paths": ["frontend/**"]}, "schedule": true},
//  "presets": [{"label": "…", "event": "push", "branch": "main", "files": "src/app.py"}]}

function globRe(g) {
  return new RegExp("^" + g.split(/(\*\*|\*|\?)/).map((p) => (p === "**" ? ".*" : p === "*" ? "[^/]*" : p === "?" ? "[^/]" : p.replace(/[.+^${}()|[\]\\]/g, "\\$&"))).join("") + "$");
}

function triggerViz(box, spec) {
  const on = spec.on;
  const yaml = ["on:", ...Object.entries(on).map(([ev, cfg]) => {
    if (cfg === true) return `  ${ev}:`;
    if (ev === "schedule") return `  schedule:\n    - cron: "${cfg}"`;
    return `  ${ev}:\n` + Object.entries(cfg).map(([k, v]) => `    ${k}: [${v.map((x) => (/[*?]/.test(x) ? `"${x}"` : x)).join(", ")}]`).join("\n");
  })].join("\n");
  const presets = spec.presets || [];
  box.innerHTML = `${vizHead(spec)}
    <pre class="viz-code flat wrap">${yaml.split("\n").map((l) => `<span class="ln">${esc(l) || " "}</span>`).join("")}</pre>
    <div class="viz-tr-form">
      <label><span>событие</span><select class="viz-http-method viz-tr-ev">${["push", "pull_request", "schedule", "workflow_dispatch"].map((e) => `<option>${e}</option>`).join("")}</select></label>
      <label class="br"><span class="viz-tr-brl">ветка</span><input class="viz-sb-input viz-tr-br" autocapitalize="off" spellcheck="false"></label>
      <label class="fl"><span>изменённые файлы (через запятую)</span><input class="viz-sb-input viz-tr-fl" autocapitalize="off" spellcheck="false"></label>
    </div>
    <div class="viz-sb-quick">${presets.map((p, i) => `<button class="viz-chip" data-p="${i}">${esc(p.label)}</button>`).join("")}</div>
    <div class="viz-tr-res"></div>`;
  const ev = box.querySelector(".viz-tr-ev"), br = box.querySelector(".viz-tr-br"), fl = box.querySelector(".viz-tr-fl");
  const show = () => {
    const e = ev.value, cfg = on[e];
    const noFiles = e === "schedule" || e === "workflow_dispatch";
    box.querySelector(".fl").hidden = noFiles;
    box.querySelector(".br").hidden = e === "schedule";
    box.querySelector(".viz-tr-brl").textContent = e === "pull_request" ? "ветка, куда PR (base)" : "ветка";
    const checks = [];
    if (cfg === undefined) checks.push([false, `события \`${e}\` нет в \`on\``]);
    else {
      checks.push([true, `событие \`${e}\` есть в \`on\``]);
      if (e === "schedule") checks.push([true, "по расписанию запускается из ветки по умолчанию"]);
      if (cfg && typeof cfg === "object") {
        const b = br.value.trim();
        if (cfg.branches) {
          const hit = cfg.branches.find((g) => globRe(g).test(b));
          checks.push([!!hit, hit ? `ветка \`${b}\` подходит под \`${hit}\`` : `ветка \`${b || "?"}\` не подходит ни под один шаблон \`branches\`${cfg.branches.some((g) => g.includes("*") && !g.includes("**")) && b.split("/").length > 2 ? " (`*` не проходит через `/`)" : ""}`]);
        }
        const files = fl.value.split(/[,\n]/).map((s) => s.trim()).filter(Boolean);
        if (cfg.paths) {
          const hit = files.find((f) => cfg.paths.some((g) => globRe(g).test(f)));
          checks.push([!!hit, hit ? `файл \`${hit}\` подходит под \`paths\`` : "ни один изменённый файл не подходит под `paths`"]);
        }
        if (cfg["paths-ignore"]) {
          const rest = files.filter((f) => !cfg["paths-ignore"].some((g) => globRe(g).test(f)));
          checks.push([rest.length > 0, rest.length ? `не всё попало в \`paths-ignore\`: \`${rest[0]}\`` : "все файлы попали в `paths-ignore`"]);
        }
      }
    }
    const run = checks.every(([ok]) => ok);
    box.querySelector(".viz-tr-res").innerHTML = `<div class="viz-tr-verdict ${run ? "ok" : "no"}">${run ? "▶ Workflow запустится" : "⏸ Не запустится"}</div>
      <ul>${checks.map(([ok, t]) => `<li class="${ok ? "ok" : "no"}">${ok ? "✓" : "✗"} ${inline(t)}</li>`).join("")}</ul>`;
  };
  [ev, br, fl].forEach((el) => (el.oninput = show));
  ev.onchange = show;
  const apply = (p) => { ev.value = p.event; br.value = p.branch || ""; fl.value = p.files || ""; show(); };
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => apply(presets[b.dataset.p])));
  apply(presets[0] || { event: "push", branch: "main" });
}

// ---------- cron: что значит расписание и когда следующие запуски ----------
// {"type": "cron", "expr": "0 3 * * *", "presets": ["0 3 * * *", "30 6 * * 1-5"]}

const DOW = ["вс", "пн", "вт", "ср", "чт", "пт", "сб"];
const DOW_PL = ["по воскресеньям", "по понедельникам", "по вторникам", "по средам", "по четвергам", "по пятницам", "по субботам"];
const MON = ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"];

function cronField(s, lo, hi, name) {
  const out = new Set();
  for (const part of s.split(",")) {
    const m = part.match(/^(\*|\d+(?:-\d+)?)(?:\/(\d+))?$/);
    if (!m) throw new Error(`${name}: не понимаю «${part}»`);
    let [a, b] = m[1] === "*" ? [lo, hi] : m[1].split("-").map(Number);
    if (b === undefined) b = m[2] ? hi : a;
    const step = m[2] ? Number(m[2]) : 1;
    if (a < lo || b > hi || a > b || step < 1) throw new Error(`${name}: допустимо ${lo}–${hi}`);
    for (let v = a; v <= b; v += step) out.add(v);
  }
  return [...out].sort((x, y) => x - y);
}

function cronDescribe(f, sets) {
  const [mi, ho, dom, mon, dow] = f;
  const pad = (n) => String(n).padStart(2, "0");
  const stepOf = (s) => s.match(/^\*\/(\d+)$/)?.[1];
  let time;
  if (sets[0].length === 1 && sets[1].length === 1) time = `в ${pad(sets[1][0])}:${pad(sets[0][0])}`;
  else if (mi === "*" && ho === "*") time = "каждую минуту";
  else if (stepOf(mi) && ho === "*") time = `каждые ${stepOf(mi)} мин`;
  else if (sets[0].length === 1 && ho === "*") time = `каждый час в :${pad(sets[0][0])}`;
  else if (sets[0].length === 1 && stepOf(ho)) time = `каждые ${stepOf(ho)} ч (в ${sets[1].map((h) => `${pad(h)}:${pad(sets[0][0])}`).slice(0, 4).join(", ")}${sets[1].length > 4 ? "…" : ""})`;
  else if (sets[0].length === 1) time = `в ${sets[1].map((h) => `${pad(h)}:${pad(sets[0][0])}`).join(", ")}`;
  else time = `в минуты ${sets[0].join(", ")} часов ${sets[1].join(", ")}`;
  const days = [];
  const dowSet = sets[4];
  if (dow !== "*") {
    days.push(dowSet.join() === "1,2,3,4,5" ? "по будням" : dowSet.join() === "0,6" ? "по выходным" : dowSet.length === 1 ? DOW_PL[dowSet[0]] : `по дням недели: ${dowSet.map((d) => DOW[d]).join(", ")}`);
  }
  if (dom !== "*") days.push(sets[2].length === 1 ? `${sets[2][0]}-го числа` : `числа: ${sets[2].join(", ")}`);
  const day = days.length ? days.join(" или ") : "каждый день";
  const month = mon === "*" ? "" : `, месяцы: ${sets[3].map((m) => MON[m - 1]).join(", ")}`;
  if (!days.length && !month && /^кажд/.test(time)) return time;
  return `${day}${month} ${time}`;
}

function cronViz(box, spec) {
  const presets = spec.presets || ["0 3 * * *", "30 6 * * 1-5", "0 */4 * * *", "*/15 * * * *", "0 9 * * 1", "0 0 1 * *"];
  const names = ["минута", "час", "день месяца", "месяц", "день недели"];
  box.innerHTML = `${vizHead(spec)}
    <form class="viz-sb-form"><input class="viz-sb-input viz-cron-in" value="${esc(spec.expr || presets[0])}" autocapitalize="off" autocomplete="off" spellcheck="false"></form>
    <div class="viz-sb-quick">${presets.map((p) => `<button class="viz-chip" data-p="${esc(p)}">${esc(p)}</button>`).join("")}</div>
    <div class="viz-cron-fields"></div>
    <div class="viz-cron-res"></div>`;
  const input = box.querySelector(".viz-cron-in");
  const show = () => {
    const f = input.value.trim().split(/\s+/);
    const fieldsBox = box.querySelector(".viz-cron-fields"), res = box.querySelector(".viz-cron-res");
    fieldsBox.innerHTML = names.map((n, i) => `<div><code>${esc(f[i] ?? "?")}</code><span>${n}</span></div>`).join("");
    let sets;
    try {
      if (f.length !== 5) throw new Error(`нужно 5 полей через пробел, а здесь ${f.length}`);
      sets = [cronField(f[0], 0, 59, "минута"), cronField(f[1], 0, 23, "час"), cronField(f[2], 1, 31, "день месяца"),
        cronField(f[3], 1, 12, "месяц"), cronField(f[4], 0, 7, "день недели").map((d) => d % 7)];
      sets[4] = [...new Set(sets[4])].sort((a, b) => a - b);
    } catch (e) {
      res.innerHTML = `<div class="viz-note">${inline(`Ошибка: ${e.message}.`)}</div>`;
      return;
    }
    const domR = f[2] !== "*", dowR = f[4] !== "*";
    const runs = [];
    const now = new Date();
    const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
    for (let day = 0; day < 800 && runs.length < 5; day++, d.setUTCDate(d.getUTCDate() + 1)) {
      if (!sets[3].includes(d.getUTCMonth() + 1)) continue;
      const a = sets[2].includes(d.getUTCDate()), b = sets[4].includes(d.getUTCDay());
      if (!(domR && dowR ? a || b : a && b)) continue;
      for (const h of sets[1]) for (const m of sets[0]) {
        const t = new Date(d.getTime() + (h * 60 + m) * 60000);
        if (t > now && runs.length < 5) runs.push(t);
      }
    }
    const pad = (n) => String(n).padStart(2, "0");
    const fmt = (t, off) => { const x = new Date(t.getTime() + off * 3600000); return `${pad(x.getUTCHours())}:${pad(x.getUTCMinutes())}`; };
    res.innerHTML = `<div class="viz-cron-say">${esc(cronDescribe(f, sets))} <small>(UTC)</small></div>
      <div class="viz-sb-head">Ближайшие запуски:</div>
      <ol class="viz-cron-runs">${runs.map((t) => `<li><b>${DOW[t.getUTCDay()]} ${t.getUTCDate()} ${MON[t.getUTCMonth()]}</b> ${fmt(t, 0)} UTC <i>= ${fmt(t, 3)} МСК</i></li>`).join("")}</ol>
      ${domR && dowR ? `<div class="viz-note">${inline("Заданы и день месяца, и день недели — cron запускает, когда подходит **любой** из них.")}</div>` : ""}`;
  };
  input.oninput = show;
  box.querySelector(".viz-sb-form").onsubmit = (e) => e.preventDefault();
  box.querySelectorAll("[data-p]").forEach((b) => (b.onclick = () => { input.value = b.dataset.p; show(); }));
  show();
}

// ---------- itertools: песочница ----------
// {"type": "itertools", "fn": "chain", "fns": ["chain", "islice", …]}

const PREDS = {
  "n % 2": [(n) => pymod(n, 2) !== 0, "нечётное"],
  "n % 2 == 0": [(n) => pymod(n, 2) === 0, "чётное"],
  "n < 5": [(n) => n < 5, "меньше 5"],
  "n > 0": [(n) => n > 0, "больше 0"],
};
const ACC = { "": [(a, b) => a + b, "сумма"], max: [Math.max, "максимум"], min: [Math.min, "минимум"], "operator.mul": [(a, b) => a * b, "произведение"] };

function combos(xs, r, perm) {
  const out = [];
  const rec = (start, used, cur) => {
    if (cur.length === r) { out.push(tup(...cur.map((i) => xs[i]))); return; }
    for (let i = perm ? 0 : start; i < xs.length; i++) {
      if (used.has(i)) continue;
      used.add(i); cur.push(i);
      rec(i + 1, used, cur);
      used.delete(i); cur.pop();
      if (out.length > 300) return;
    }
  };
  rec(0, new Set(), []);
  return out;
}

const ITF = {
  chain: { args: [["a", "list", "[1, 2]"], ["b", "list", "(3,)"], ["c", "list", '"ab"']], code: (a) => `chain(${a.a}, ${a.b}, ${a.c})`,
    run: (v) => [...v.a, ...v.b, ...v.c], note: "Перебирает последовательности одну за другой — новый общий список не создаётся." },
  islice: { args: [["it", "list", "range(10)"], ["start", "int", 2], ["stop", "int", 8], ["step", "int", 2]], code: (a) => `islice(${a.it}, ${a.start}, ${a.stop}, ${a.step})`,
    run: (v) => {
      if (v.step < 1 || v.start < 0 || v.stop < 0) throw new Error("ValueError: в islice нельзя отрицательные числа и шаг 0");
      const idx = []; for (let i = v.start; i < Math.min(v.stop, v.it.length); i += v.step) idx.push(i);
      return { out: idx.map((i) => v.it[i]), mark: idx };
    }, note: "Как срез `[start:stop:step]`, но для любого итератора — даже бесконечного. Отрицательные индексы нельзя." },
  takewhile: { args: [["pred", "pred", "n % 2"], ["nums", "list", "[1, 3, 5, 8, 9, 11]"]], code: (a) => `takewhile(lambda n: ${a.pred}, ${a.nums})`,
    run: (v) => { const k = v.nums.findIndex((n) => !PREDS[v.pred][0](n)); const end = k < 0 ? v.nums.length : k; return { out: v.nums.slice(0, end), mark: [...Array(end).keys()], stop: k }; },
    note: "Берёт, **пока** условие истинно. На первом ложном элементе — стоп, дальше даже не смотрит." },
  dropwhile: { args: [["pred", "pred", "n % 2"], ["nums", "list", "[1, 3, 5, 8, 9, 11]"]], code: (a) => `dropwhile(lambda n: ${a.pred}, ${a.nums})`,
    run: (v) => { const k = v.nums.findIndex((n) => !PREDS[v.pred][0](n)); const s = k < 0 ? v.nums.length : k; return { out: v.nums.slice(s), mark: v.nums.map((_, i) => i).filter((i) => i >= s), stop: k }; },
    note: "Пропускает, пока условие истинно, а с первого ложного отдаёт **всё** подряд — условие больше не проверяется." },
  groupby: { args: [["xs", "list", '"aaabccaa"']], code: (a) => `[(k, list(g)) for k, g in groupby(${a.xs})]`, wrap: false,
    run: (v) => { const g = []; for (const x of v.xs) { if (g.length && JSON.stringify(g.at(-1).v[0]) === JSON.stringify(x)) g.at(-1).v[1].push(x); else g.push(tup(x, [x])); } return g; },
    note: "Группирует только **подряд идущие** одинаковые элементы. Нужны общие группы — сначала `sorted`." },
  accumulate: { args: [["xs", "list", "[1, 2, 3, 4]"], ["func", "acc", ""]], code: (a) => `accumulate(${a.xs}${a.func ? `, ${a.func}` : ""})`,
    run: (v) => { const out = []; for (const x of v.xs) out.push(out.length ? ACC[v.func][0](out.at(-1), x) : x); return out; },
    note: "Накопленный итог: каждый элемент — результат для всех предыдущих. По умолчанию сумма." },
  pairwise: { args: [["xs", "list", "[10, 13, 19, 20]"]], code: (a) => `pairwise(${a.xs})`,
    run: (v) => v.xs.slice(1).map((x, i) => tup(v.xs[i], x)), note: "Пары соседей: элементов на один меньше, чем во входе." },
  batched: { args: [["xs", "list", '"abcdefg"'], ["n", "int", 3]], code: (a) => `batched(${a.xs}, ${a.n})`,
    run: (v) => { if (v.n < 1) throw new Error("ValueError: n должно быть ≥ 1"); const out = []; for (let i = 0; i < v.xs.length; i += v.n) out.push(tup(...v.xs.slice(i, i + v.n))); return out; },
    note: "Пачки по `n` штук; последняя может быть короче." },
  product: { args: [["a", "list", '["chrome", "firefox"]'], ["b", "list", '["ru", "en"]']], code: (a) => `product(${a.a}, ${a.b})`,
    run: (v) => v.a.flatMap((x) => v.b.map((y) => tup(x, y))), note: "Все пары «каждый с каждым»: длина = произведение длин." },
  combinations: { args: [["xs", "list", '"abcd"'], ["r", "int", 2]], code: (a) => `combinations(${a.xs}, ${a.r})`,
    run: (v) => combos(v.xs, v.r, false), note: "Сочетания: порядок внутри не важен, `('a', 'b')` и `('b', 'a')` — одно и то же." },
  permutations: { args: [["xs", "list", '"abc"'], ["r", "int", 2]], code: (a) => `permutations(${a.xs}, ${a.r})`,
    run: (v) => combos(v.xs, v.r, true), note: "Перестановки: порядок важен, поэтому их больше, чем сочетаний." },
};

function itertoolsViz(box, spec) {
  const fns = spec.fns || Object.keys(ITF);
  let fn = spec.fn || fns[0];
  const vals = {};
  box.innerHTML = `${vizHead(spec)}
    <div class="viz-sb-quick viz-it-fns">${fns.map((f) => `<button class="viz-chip" data-f="${f}">${f}</button>`).join("")}</div>
    <div class="viz-it-args"></div>
    <div class="viz-it-res"></div>
    <div class="viz-note"></div>`;
  const run = () => {
    const F = ITF[fn];
    const raw = Object.fromEntries(F.args.map(([k, , def]) => [k, vals[`${fn}.${k}`] ?? def]));
    const res = box.querySelector(".viz-it-res"), note = box.querySelector(".viz-note");
    const call = F.code(raw);
    let v;
    try {
      v = Object.fromEntries(F.args.map(([k, kind]) => [k, kind === "list" ? pyParse(raw[k]) : kind === "int" ? Number(raw[k]) : raw[k]]));
    } catch {
      res.innerHTML = `<pre class="viz-code flat"><span class="ln">${highlight(F.wrap === false ? call : `list(${call})`)}</span></pre>`;
      note.innerHTML = inline("Не получилось прочитать вход: пиши как в Python — `[1, 2, 3]`, `\"abc\"` или `range(10)`.");
      return;
    }
    let r;
    try { r = F.run(v); } catch (e) { res.innerHTML = `<div class="viz-sb-msg err">${esc(e.message)}</div>`; note.innerHTML = ""; return; }
    const out = Array.isArray(r) ? r : r.out;
    const listArg = F.args.find(([, kind]) => kind === "list" && r.mark);
    res.innerHTML = `<pre class="viz-code flat"><span class="ln">${highlight(F.wrap === false ? call : `list(${call})`)}</span></pre>
      ${listArg ? `<div class="viz-slice-cells">${v[listArg[0]].map((x, i) => `<div class="viz-sc${r.mark.includes(i) ? " on" : ""}${i === r.stop ? " is-stop" : ""}"><i>${i}</i><b>${esc(pyFmt(x))}</b></div>`).join("")}</div>` : ""}
      <div class="viz-it-out"><span>→</span>${out.map((x) => `<code>${esc(pyFmt(x))}</code>`).join("") || `<i>пусто</i>`}</div>
      <div class="viz-sb-head">${out.length} ${plural(out.length, "элемент", "элемента", "элементов")}</div>`;
    note.innerHTML = inline(F.note);
  };
  const show = () => {
    const F = ITF[fn];
    box.querySelectorAll("[data-f]").forEach((b) => b.classList.toggle("on", b.dataset.f === fn));
    box.querySelector(".viz-it-args").innerHTML = F.args.map(([k, kind, def]) => {
      const cur = vals[`${fn}.${k}`] ?? def;
      if (kind === "pred") return `<label><span>условие</span><select data-k="${k}">${Object.entries(PREDS).map(([p, [, t]]) => `<option value="${esc(p)}"${p === cur ? " selected" : ""}>lambda n: ${esc(p)} — ${t}</option>`).join("")}</select></label>`;
      if (kind === "acc") return `<label><span>функция</span><select data-k="${k}">${Object.entries(ACC).map(([p, [, t]]) => `<option value="${esc(p)}"${p === cur ? " selected" : ""}>${p ? esc(p) : "не указана"} — ${t}</option>`).join("")}</select></label>`;
      return `<label class="${kind}"><span>${esc(k)}</span><input class="viz-sb-input" data-k="${k}" value="${esc(String(cur))}"${kind === "int" ? ' type="number" inputmode="numeric"' : ""} autocapitalize="off" spellcheck="false"></label>`;
    }).join("");
    box.querySelectorAll(".viz-it-args [data-k]").forEach((el) => (el.oninput = el.onchange = () => { vals[`${fn}.${el.dataset.k}`] = el.value; run(); }));
    run();
  };
  box.querySelectorAll("[data-f]").forEach((b) => (b.onclick = () => { fn = b.dataset.f; show(); }));
  show();
}

const KINDS = {
  memory: memoryViz, git: gitViz, slice: sliceViz, fs: fsViz, perm: permViz,
  fixtures: fixturesViz, pipeline: pipelineViz, http: httpViz, trace: traceViz,
  pipe: pipeViz, redirect: redirectViz, select: selectViz, params: paramsViz, json: jsonViz,
  schema: schemaViz, matrix: matrixViz, trigger: triggerViz, cron: cronViz, itertools: itertoolsViz,
};
