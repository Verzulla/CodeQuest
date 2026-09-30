// Экран входа и регистрации.
import { api, esc, ic, owl } from "../util.js";

export function renderAuth(view, onDone) {
  let mode = "login";
  const draw = (error = "", values = {}) => {
    const reg = mode === "register";
    view.innerHTML = `
      <div class="auth-box">
        ${owl("wave", "bob")}
        <div class="auth-logo"><svg class="i"><use href="#ic-logo"/></svg><span>CodeQuest</span></div>
        <p class="muted auth-sub">Python и тестирование — играючи</p>
        <div class="auth-tabs">
          <button type="button" data-mode="login" class="${reg ? "" : "on"}">Вход</button>
          <button type="button" data-mode="register" class="${reg ? "on" : ""}">Регистрация</button>
        </div>
        <form class="form" id="auth-form" novalidate>
          <label>Ник
            <span class="fld">${ic("user")}<input class="input" name="username" autocomplete="username" maxlength="20" required value="${esc(values.username || "")}"></span>
            ${reg ? `<small>3–20 символов: буквы, цифры и _</small>` : ""}
          </label>
          <label>Пароль
            <span class="fld">${ic("lockO")}<input class="input" name="password" type="password" autocomplete="${reg ? "new-password" : "current-password"}" maxlength="128" required>
              <button type="button" class="eye" data-eye title="Показать пароль">${ic("eye")}</button></span>
            ${reg ? `<small>Не меньше 6 символов</small>` : ""}
          </label>
          ${reg ? `<label>Повтори пароль
            <span class="fld">${ic("lockO")}<input class="input" name="password2" type="password" autocomplete="new-password" maxlength="128" required></span></label>
            <p class="muted auth-note">${ic("key")}Восстановления пароля нет — запомни его или сохрани в менеджере паролей.</p>` : ""}
          <p class="auth-error" id="auth-error" ${error ? "" : "hidden"}>${esc(error)}</p>
          <button class="btn" type="submit" id="auth-submit">${reg ? "Создать аккаунт" : "Войти"}</button>
        </form>
        <p class="muted auth-foot">Прогресс хранится в аккаунте — входи с любого устройства</p>
      </div>`;
    view.querySelector("[data-eye]").onclick = () => {
      const f = view.querySelector("[name=password]");
      f.type = f.type === "password" ? "text" : "password";
    };
    view.querySelectorAll("[data-mode]").forEach((b) => b.onclick = () => {
      mode = b.dataset.mode;
      draw("", { username: view.querySelector("[name=username]").value });
    });
    const form = view.querySelector("#auth-form");
    (values.username ? form.password : form.username).focus();
    form.onsubmit = async (e) => {
      e.preventDefault();
      const username = form.username.value.trim();
      const password = form.password.value;
      const fail = (msg) => {
        const el = view.querySelector("#auth-error");
        el.textContent = msg;
        el.hidden = false;
      };
      if (!username || !password) return fail("Заполни ник и пароль");
      if (reg && password !== form.password2.value) return fail("Пароли не совпадают");
      const btn = view.querySelector("#auth-submit");
      btn.disabled = true;
      try {
        const user = await api(`/auth/${reg ? "register" : "login"}`, { method: "POST", body: { username, password } });
        onDone(user);
      } catch (err) {
        btn.disabled = false;
        fail(err.message);
      }
    };
  };
  draw();
}
