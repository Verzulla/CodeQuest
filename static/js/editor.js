// Лёгкий редактор кода: textarea поверх подсвеченного <pre>.
// Tab / Shift+Tab — отступ, Enter — автоотступ (после ":" +4 пробела),
// Ctrl/Cmd+Enter — onSubmit.
import { highlight } from "./util.js";

const INDENT = "    ";

export function createEditor(host, initial = "", { onSubmit, onChange } = {}) {
  host.innerHTML = `<div class="editor"><div class="gutter"></div><div class="area"><pre aria-hidden="true"></pre><textarea spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" wrap="off"></textarea><span class="ed-measure" aria-hidden="true">0000000000</span></div></div>`;
  const ta = host.querySelector("textarea");
  const pre = host.querySelector("pre");
  const gutter = host.querySelector(".gutter");
  const area = host.querySelector(".area");
  const measure = host.querySelector(".ed-measure");

  // textarea растягивается на весь текст (как подсветка под ним), а прокручивается только .area.
  // Иначе длинная строка прокручивается внутри textarea, подсветка остаётся на месте:
  // набранного текста не видно, а касание ставит курсор не туда (особенно на телефоне).
  const fit = () => {
    ta.style.width = "";
    ta.style.height = "";
    ta.style.width = `${Math.max(pre.scrollWidth, area.clientWidth)}px`;
    ta.style.height = `${Math.max(pre.scrollHeight, area.clientHeight)}px`;
    // Номера строк — ровно по высоте области кода (прокручиваются вместе с ней, см. scroll ниже).
    // Иначе колонка номеров растягивает редактор на все строки, а код виден лишь в верхнем окошке.
    gutter.style.height = `${area.offsetHeight}px`;
    gutter.scrollTop = area.scrollTop;
  };

  // Прокрутить .area так, чтобы курсор был виден (шрифт моноширинный — позицию считаем сами).
  const followCaret = () => {
    if (document.activeElement !== ta) return;
    const pos = ta.selectionEnd;
    const before = ta.value.slice(0, pos);
    const line = before.split("\n").length - 1;
    const col = pos - (before.lastIndexOf("\n") + 1);
    const cs = getComputedStyle(ta);
    const charW = measure.getBoundingClientRect().width / 10;
    const lineH = parseFloat(cs.lineHeight) || charW * 1.7;
    const x = parseFloat(cs.paddingLeft) + col * charW;
    const y = parseFloat(cs.paddingTop) + line * lineH;
    const margin = charW * 3;
    if (x - margin < area.scrollLeft) area.scrollLeft = Math.max(0, x - margin - parseFloat(cs.paddingLeft));
    else if (x + margin > area.scrollLeft + area.clientWidth) area.scrollLeft = x + margin - area.clientWidth;
    if (y < area.scrollTop) area.scrollTop = y;
    else if (y + lineH * 1.5 > area.scrollTop + area.clientHeight) area.scrollTop = y + lineH * 1.5 - area.clientHeight;
  };

  const render = () => {
    // Пробел в конце — чтобы пустая последняя строка тоже имела высоту.
    pre.innerHTML = highlight(ta.value) + " ";
    const n = ta.value.split("\n").length;
    gutter.textContent = Array.from({ length: n }, (_, i) => i + 1).join("\n");
    fit();
    onChange?.(ta.value);
  };
  area.addEventListener("scroll", () => { gutter.scrollTop = area.scrollTop; });
  // Браузер иногда всё же прокручивает саму textarea (например, к курсору) — возвращаем.
  ta.addEventListener("scroll", () => { if (ta.scrollLeft || ta.scrollTop) { ta.scrollLeft = 0; ta.scrollTop = 0; } });
  // Курсор двигается стрелками, касанием или кнопками ← → панели символов.
  const onSelection = () => {
    if (!ta.isConnected) return document.removeEventListener("selectionchange", onSelection);   // редактор уже убран со страницы
    if (document.activeElement === ta) followCaret();
  };
  document.addEventListener("selectionchange", onSelection);
  ta.addEventListener("focus", () => followCaret());
  new ResizeObserver(fit).observe(area);

  const replace = (start, end, text, selStart, selEnd) => {
    ta.setRangeText(text, start, end, "end");
    if (selStart != null) ta.setSelectionRange(selStart, selEnd ?? selStart);
    render();
    followCaret();
  };

  ta.addEventListener("input", () => { render(); followCaret(); });
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
