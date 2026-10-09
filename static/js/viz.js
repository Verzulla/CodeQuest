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

const KINDS = { memory: memoryViz, git: gitViz };
