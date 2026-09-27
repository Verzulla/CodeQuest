// Лёгкий редактор кода: textarea поверх подсвеченного <pre>.
// Tab / Shift+Tab — отступ, Enter — автоотступ (после ":" +4 пробела),
// Ctrl/Cmd+Enter — onSubmit.
import { highlight } from "./util.js";

const INDENT = "    ";

export function createEditor(host, initial = "", { onSubmit, onChange } = {}) {
  host.innerHTML = `<div class="editor"><div class="gutter"></div><div class="area"><pre aria-hidden="true"></pre><textarea spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"></textarea></div></div>`;
  const ta = host.querySelector("textarea");
  const pre = host.querySelector("pre");
  const gutter = host.querySelector(".gutter");
  const area = host.querySelector(".area");

  const render = () => {
    // Пробел в конце — чтобы пустая последняя строка тоже имела высоту.
    pre.innerHTML = highlight(ta.value) + " ";
    const n = ta.value.split("\n").length;
    gutter.textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n");
    onChange?.(ta.value);
  };
  area.addEventListener("scroll", () => { gutter.style.transform = `translateY(${-area.scrollTop}px)`; });

  const replace = (start, end, text, selStart, selEnd) => {
    ta.setRangeText(text, start, end, "end");
    if (selStart != null) ta.setSelectionRange(selStart, selEnd ?? selStart);
    render();
  };

  ta.addEventListener("input", render);
  ta.addEventListener("keydown", (e) => {
    const { selectionStart: s, selectionEnd: en, value: v } = ta;
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      onSubmit?.();
      return;
    }
    if (e.key === "Tab") {
      e.preventDefault();
      const lineStart = v.lastIndexOf("\n", s - 1) + 1;
      if (s === en && !e.shiftKey) return replace(s, en, INDENT);
      // Отступ / снятие отступа для всех выделенных строк
      const block = v.slice(lineStart, en);
      const lines = block.split("\n");
      const changed = e.shiftKey
        ? lines.map((l) => l.replace(/^ {1,4}/, ""))
        : lines.map((l) => INDENT + l);
      const text = changed.join("\n");
      const delta0 = changed[0].length - lines[0].length;
      replace(lineStart, en, text, Math.max(lineStart, s + delta0), lineStart + text.length);
      return;
    }
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const lineStart = v.lastIndexOf("\n", s - 1) + 1;
      const line = v.slice(lineStart, s);
      let indent = line.match(/^\s*/)[0];
      if (/:\s*(#.*)?$/.test(line)) indent += INDENT;
      replace(s, en, "\n" + indent);
      return;
    }
    if (e.key === "Backspace" && s === en && s > 0) {
      const lineStart = v.lastIndexOf("\n", s - 1) + 1;
      const before = v.slice(lineStart, s);
      if (before.length && /^ +$/.test(before)) {
        e.preventDefault();
        const cut = before.length % 4 || 4;
        replace(s - cut, s, "");
      }
    }
  });

  ta.value = initial;
  render();
  return {
    get value() { return ta.value; },
    set value(v) { ta.value = v; render(); },
    focus() { ta.focus(); },
    textarea: ta,
  };
}
