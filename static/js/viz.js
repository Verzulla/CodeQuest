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
  const text = [...String(spec.text || "Python")];
  const n = text.length;
  const st = { start: spec.start ?? null, stop: spec.stop ?? null, step: spec.step || 1 };
  const presets = spec.presets || ["[1:4]", "[:3]", "[-3:]", "[::2]", "[::-1]"];
  box.innerHTML = `${spec.title ? `<div class="viz-title">${esc(spec.title)}</div>` : ""}
    <div class="viz-slice-expr"></div>
    <div class="viz-slice-cells"></div>
    <div class="viz-legend"><span class="s"></span>start — откуда <span class="e"></span>stop — докуда (не входит) <em>1 2 3</em> — порядок</div>
    <div class="viz-slice-ctrl">
      ${["start", "stop", "step"].map((k) => `
        <label class="viz-slider"><span>${k}</span>
          <input type="range" data-k="${k}" min="${k === "step" ? -3 : -n}" max="${k === "step" ? 3 : n}" step="1">
          <b data-v="${k}"></b>
          ${k === "step" ? "" : `<button class="viz-chip" data-none="${k}">пусто</button>`}</label>`).join("")}
    </div>
    <div class="viz-sb-quick">${presets.map((p) => `<button class="viz-chip" data-preset="${esc(p)}">s${esc(p)}</button>`).join("")}</div>
    <div class="viz-note"></div>`;
  const parse = (p) => {
    const [a = "", b = "", c = ""] = p.replace(/^\[|\]$/g, "").split(":");
    return { start: a === "" ? null : Number(a), stop: b === "" ? null : Number(b), step: c === "" ? 1 : Number(c) };
  };
  const show = () => {
    const idx = sliceIndices(n, st.start, st.stop, st.step);
    const order = new Map(idx.map((i, k) => [i, k + 1]));
    const expr = `s[${st.start ?? ""}:${st.stop ?? ""}${st.step !== 1 ? `:${st.step}` : ""}]`;
    box.querySelector(".viz-slice-expr").innerHTML =
      `<code>s = ${esc(pyRepr(text.join("")))}</code><code class="res">${esc(expr)} → ${esc(pyRepr(idx.map((i) => text[i]).join("")))}</code>`;
    box.querySelector(".viz-slice-cells").innerHTML = text.map((ch, i) => {
      const k = order.get(i);
      const edge = (i === (st.start == null ? null : (st.start < 0 ? st.start + n : st.start)) ? " is-start" : "")
        + (i === (st.stop == null ? null : (st.stop < 0 ? st.stop + n : st.stop)) ? " is-stop" : "");
      return `<div class="viz-sc${k ? " on" : ""}${edge}"><i>${i}</i><b>${esc(ch === " " ? "␣" : ch)}</b><i>${i - n}</i>${k ? `<em>${k}</em>` : ""}</div>`;
    }).join("");
    for (const k of ["start", "stop", "step"]) {
      const input = box.querySelector(`[data-k="${k}"]`);
      input.value = st[k] ?? (k === "start" ? (st.step > 0 ? 0 : n - 1) : (st.step > 0 ? n : -n));
      input.classList.toggle("none", st[k] == null);
      box.querySelector(`[data-v="${k}"]`).textContent = st[k] ?? "пусто";
    }
    const dir = st.step > 0 ? "слева направо" : "справа налево";
    const note = !idx.length ? "Пустой срез: при таком шаге от start до stop не дойти — ошибки нет, просто пусто."
      : `Берём ${idx.length} ${plural(idx.length, "символ", "символа", "символов")} ${dir}${Math.abs(st.step) > 1 ? `, каждый ${Math.abs(st.step)}-й` : ""}. `
        + (st.step > 0 ? "`stop` не входит в срез." : "При отрицательном шаге пустой `start` — с конца, пустой `stop` — до самого начала.");
    box.querySelector(".viz-note").innerHTML = inline(note);
  };
  box.querySelectorAll("input[type=range]").forEach((inp) => (inp.oninput = () => {
    let v = Number(inp.value);
    if (inp.dataset.k === "step" && v === 0) v = st.step > 0 ? -1 : 1;
    st[inp.dataset.k] = v;
    show();
  }));
  box.querySelectorAll("[data-none]").forEach((b) => (b.onclick = () => { st[b.dataset.none] = null; show(); }));
  box.querySelectorAll("[data-preset]").forEach((b) => (b.onclick = () => { Object.assign(st, parse(b.dataset.preset)); show(); }));
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

function fixtureEvents(fixtures, tests) {
  const scope = Object.fromEntries(fixtures.map((f) => [f.name, f.scope]));
  const alive = [];
  const events = [];
  const count = {};
  const push = (e) => events.push({ ...e, alive: [...alive], count: { ...count } });
  const teardown = (pred) => {
    for (const f of [...alive].reverse()) {
      if (!pred(f)) continue;
      alive.splice(alive.indexOf(f), 1);
      push({ kind: "down", f, note: `Уборка \`${f}\` (scope=${scope[f]}).` });
    }
  };
  tests.forEach((t, k) => {
    for (const f of t.uses) {
      if (alive.includes(f)) continue;
      alive.push(f);
      count[f] = (count[f] || 0) + 1;
      push({ kind: "up", f, test: t.name, note: `Создаётся \`${f}\` (scope=${scope[f]}) — его просит \`${t.name}\`.` });
    }
    push({ kind: "test", test: t.name, module: t.module, note: `Выполняется \`${t.name}\`${t.uses.length ? `, получает ${t.uses.map((f) => `\`${f}\``).join(", ")}` : ""}.` });
    teardown((f) => scope[f] === "function");
    const next = tests[k + 1];
    if (!next || next.module !== t.module) teardown((f) => scope[f] === "module");
  });
  teardown(() => true);
  return events;
}

function fixturesViz(box, spec) {
  const fixtures = spec.fixtures.map((f) => ({ ...f }));
  const build = () => {
    const events = fixtureEvents(fixtures, spec.tests);
    const states = [{ idx: -1, alive: [], count: {}, note: "Нажимай «Шаг» и смотри, когда pytest создаёт и убирает фикстуры. Область видимости можно переключить вверху." },
      ...events.map((e, idx) => ({ ...e, idx }))];
    stepper(box, {
      title: spec.title,
      states,
      render(stage, st) {
        stage.innerHTML = `
          <div class="viz-fx-scopes">${fixtures.map((f, k) => `<label><b>${esc(f.name)}</b>
            <select data-k="${k}">${["function", "module", "session"].map((s) => `<option${s === f.scope ? " selected" : ""}>${s}</option>`).join("")}</select></label>`).join("")}</div>
          <div class="viz-fx-alive"><span>сейчас живы:</span>${st.alive.length ? st.alive.map((f) => `<i>${esc(f)}</i>`).join("") : `<em>никого</em>`}</div>
          <ol class="viz-fx-log">${events.map((e, k) => `<li class="${e.kind}${k === st.idx ? " cur" : k < st.idx ? " done" : ""}">${
            e.kind === "up" ? `▲ создать <b>${esc(e.f)}</b>` : e.kind === "down" ? `▼ убрать <b>${esc(e.f)}</b>` : `▶ <b>${esc(e.test)}</b> <small>${esc(e.module)}</small>`}</li>`).join("")}</ol>
          <div class="viz-fx-count">${fixtures.map((f) => `<span><b>${esc(f.name)}</b> создан ${st.count[f.name] || 0} ${plural(st.count[f.name] || 0, "раз", "раза", "раз")}</span>`).join("")}</div>`;
        stage.querySelectorAll("select").forEach((sel) => (sel.onchange = () => { fixtures[sel.dataset.k].scope = sel.value; build(); }));
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

const KINDS = {
  memory: memoryViz, git: gitViz, slice: sliceViz, fs: fsViz, perm: permViz,
  fixtures: fixturesViz, pipeline: pipelineViz, http: httpViz, trace: traceViz,
};
