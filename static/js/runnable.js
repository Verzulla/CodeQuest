// Живые примеры в теории: «Запустить» выполняет код в песочнице,
// «Изменить» превращает пример в редактор, «Вернуть» — исходный код.
import { api, esc, ic } from "./util.js";
import { createEditor } from "./editor.js";

export function bindRunnable(root) {
  root.querySelectorAll(".runnable").forEach((box) => {
    const original = box.dataset.code;
    const codeHost = box.querySelector(".rb-code");
    const out = box.querySelector(".rb-out");
    const editBtn = box.querySelector('[data-act="edit"]');
    const runBtn = box.querySelector('[data-act="run"]');
    const staticHtml = codeHost.innerHTML;
    let editor = null;

    const run = async () => {
      if (runBtn.dataset.running) return;   // вид кнопки не меняется — повторные нажатия игнорируем
      runBtn.dataset.running = "1";
      try {
        const r = await api("/run", { method: "POST", body: { code: editor ? editor.value : original } });
        const text = r.stdout ? esc(r.stdout) : `<span class="muted">(программа ничего не вывела)</span>`;
        const err = r.error ? `\n<span class="err">${esc(r.error)}${r.error_line ? ` (строка ${r.error_line})` : ""}</span>` : "";
        out.innerHTML = `<div class="console"><div class="c-head">Вывод</div><pre>${text}${err}</pre></div>`;
      } catch (e) {
        out.innerHTML = `<div class="console"><pre class="err">${esc(e.message)}</pre></div>`;
      } finally {
        delete runBtn.dataset.running;
      }
    };

    runBtn.onclick = run;
    editBtn.onclick = () => {
      if (editor) {                      // «↺ Вернуть»: назад к исходному примеру
        editor = null;
        codeHost.innerHTML = staticHtml;
        editBtn.innerHTML = `${ic("pen")}<span>Изменить</span>`;
        out.innerHTML = "";
        return;
      }
      codeHost.innerHTML = "";
      editor = createEditor(codeHost, original, { onSubmit: run });
      editor.focus();
      editBtn.innerHTML = `${ic("refresh")}<span>Вернуть</span>`;
    };
  });
}
