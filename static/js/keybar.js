// Панель символов для кода на телефоне (вариант C): под полем ввода, внутри карточки, шириной с неё,
// листается пальцем; наборы «Символы / Операторы / Python». Только на сенсорных устройствах.
// Скобки и кавычки — парой, курсор между ними (выделенное оборачивается); «|» в заготовке — где встанет курсор.
const SETS = {
  "Символы": [["⇥", "    "], ["( )", "(", ")"], ["[ ]", "[", "]"], ["{ }", "{", "}"], ['" "', '"', '"'], ["' '", "'", "'"],
    [":", ":"], ["=", "="], [".", "."], [",", ","], ["_", "_"], ["#", "# "], ["←", "left"], ["→", "right"]],
  "Операторы": [["+", " + "], ["-", " - "], ["*", " * "], ["/", " / "], ["//", " // "], ["%", " % "], ["**", " ** "],
    ["==", " == "], ["!=", " != "], ["<", " < "], [">", " > "], ["<=", " <= "], [">=", " >= "], ["+=", " += "],
    ["and", " and "], ["or", " or "], ["not", "not "], ["in", " in "]],
  "Python": [["print()", "print(|)"], ["for", "for | in :"], ["range()", "range(|)"], ["if", "if |:"], ["elif", "elif |:"],
    ["else:", "else:"], ["def", "def |():"], ["return", "return "], ["len()", "len(|)"], ["True", "True"], ["False", "False"],
    ["None", "None"], ["self", "self"], ["import", "import "]],
};
const NAMES = Object.keys(SETS);
export const touchDevice = () => matchMedia("(pointer: coarse)").matches;

// Разметка панели (вставляется под полем). На компьютере — пустая строка.
export function keybarHtml() {
  if (!touchDevice()) return "";
  return `<div class="keybar2"><div class="kb-tabs">${NAMES.map((n, i) => `<button type="button" tabindex="-1" data-set="${n}" class="${i ? "" : "on"}">${n}</button>`).join("")}</div>
    <div class="kb-keys">${keysHtml(NAMES[0])}</div></div>`;
}
const keysHtml = (set) => SETS[set].map(([label], i) => `<button type="button" tabindex="-1" data-k="${i}" class="${label === "⇥" || label === "←" || label === "→" ? "acc" : ""}">${label}</button>`).join("");

function press(el, [, open, close]) {
  const { selectionStart: s, selectionEnd: e, value } = el;
  if (open === "left" || open === "right") {
    const p = open === "left" ? Math.max(0, s - 1) : Math.min(value.length, e + 1);
    el.setSelectionRange(p, p);
    return;
  }
  const sel = value.slice(s, e);
  if (close) {
    el.setRangeText(open + sel + close, s, e, "end");
    if (!sel) el.setSelectionRange(s + open.length, s + open.length);
  } else {
    const caret = open.indexOf("|");
    const text = open.replace("|", "");
    el.setRangeText(text, s, e, "end");
    if (caret >= 0) el.setSelectionRange(s + caret, s + caret);
  }
  el.dispatchEvent(new Event("input", { bubbles: true }));   // редактор перерисует подсветку и сохранит черновик
}

// Подключить панель внутри root к полю el.
export function bindKeybar(root, el) {
  const bar = root?.querySelector(".keybar2");
  if (!bar || !el) return;
  let set = NAMES[0];
  // pointerdown + preventDefault: фокус остаётся в поле, клавиатура телефона не прячется
  bar.addEventListener("pointerdown", (ev) => {
    const tab = ev.target.closest("[data-set]");
    const key = ev.target.closest("[data-k]");
    if (!tab && !key) return;
    ev.preventDefault();
    if (tab) {
      set = tab.dataset.set;
      bar.querySelectorAll("[data-set]").forEach((b) => b.classList.toggle("on", b === tab));
      bar.querySelector(".kb-keys").innerHTML = keysHtml(set);
      bar.querySelector(".kb-keys").scrollLeft = 0;
      return;
    }
    if (el.readOnly) return;
    if (document.activeElement !== el) el.focus();
    press(el, SETS[set][Number(key.dataset.k)]);
  });
}
