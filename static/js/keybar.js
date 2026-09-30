// Панель символов для кода на телефоне (вариант A): лента над клавиатурой, листается пальцем.
// Появляется, только пока поле кода в фокусе на сенсорном устройстве. Скобки и кавычки — парой,
// курсор между ними; выделенный текст оборачивается. Tab — 4 пробела.
const KEYS = [
  ["⇥", "    "], ["( )", "(", ")"], ["[ ]", "[", "]"], ["{ }", "{", "}"], ['" "', '"', '"'], ["' '", "'", "'"],
  [":", ":"], ["=", "="], [".", "."], [",", ","], ["_", "_"], ["#", "#"], ["+", "+"], ["-", "-"], ["*", "*"],
  ["/", "/"], ["%", "%"], ["<", "<"], [">", ">"], ["!", "!"], ["←", "left"], ["→", "right"],
];
const touch = () => matchMedia("(pointer: coarse)").matches;
let bar = null, target = null;

function ensureBar() {
  if (bar) return bar;
  bar = document.createElement("div");
  bar.className = "keybar";
  bar.setAttribute("aria-hidden", "true");
  bar.innerHTML = KEYS.map(([label], i) => `<button type="button" tabindex="-1" data-k="${i}" class="${i === 0 || label.length === 1 && "←→".includes(label) ? "acc" : ""}">${label}</button>`).join("");
  // pointerdown + preventDefault: фокус остаётся в поле, клавиатура не прячется
  bar.addEventListener("pointerdown", (e) => {
    const b = e.target.closest("[data-k]");
    if (!b || !target) return;
    e.preventDefault();
    press(KEYS[Number(b.dataset.k)]);
  });
  document.body.append(bar);
  const vv = window.visualViewport;
  const place = () => {
    if (!vv) return;
    bar.style.bottom = `${Math.max(0, window.innerHeight - vv.height - vv.offsetTop)}px`;
  };
  vv?.addEventListener("resize", place);
  vv?.addEventListener("scroll", place);
  place();
  return bar;
}

function press([, open, close]) {
  const el = target;
  const { selectionStart: s, selectionEnd: e, value } = el;
  if (open === "left" || open === "right") {
    const p = open === "left" ? Math.max(0, s - 1) : Math.min(value.length, e + 1);
    el.setSelectionRange(p, p);
    return;
  }
  const sel = value.slice(s, e);
  const text = close ? open + sel + close : open;
  el.setRangeText(text, s, e, "end");
  if (close && !sel) el.setSelectionRange(s + open.length, s + open.length);   // курсор внутрь пары
  el.dispatchEvent(new Event("input", { bubbles: true }));                    // редактор перерисует подсветку
}

// Подключить панель к полю ввода (textarea редактора, поле ответа, строка терминала).
export function attachKeybar(el) {
  if (!el || !touch()) return;
  el.addEventListener("focus", () => {
    if (el.readOnly) return;
    target = el;
    ensureBar().classList.add("show");
    document.body.classList.add("has-keybar");
  });
  el.addEventListener("blur", () => {
    setTimeout(() => {
      if (document.activeElement === el) return;
      if (target === el) target = null;
      bar?.classList.remove("show");
      document.body.classList.remove("has-keybar");
    }, 50);
  });
}
