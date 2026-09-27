// Экран входа и регистрации.
import { api, esc } from "../util.js";

export function renderAuth(view, onDone) {
  let mode = "login";
  const draw = (error = "", values = {}) => {
    const reg = mode === "register";
    view.innerHTML = `
      <div class="auth-box">
        <div class="auth-logo">🦉 <span>codequest</span></div>
        <p class="muted auth-sub">Учи Python и тестирование играючи</p>
        <div class="card">
          <div class="auth-tabs">
            <button type="button" data-mode="login" class="${reg ? "" : "on"}">Вход</button>
            <button type="button" data-mode="register" class="${reg ? "on" : ""}">Регистрация</button>
          </div>
          <form class="form" id="auth-form" novalidate>
            <label>Ник
              <input class="input" name="username" autocomplete="username" maxlength="20" required value="${esc(values.username || "")}">
              ${reg ? `<small>3–20 символов: буквы, цифры и _</small>` : ""}
            </label>
            <label>Пароль
              <input class="input" name="password" type="password" autocomplete="${reg ? "new-password" : "current-password"}" maxlength="128" required>
              ${reg ? `<small>Не меньше 6 символов</small>` : ""}
            </label>
            ${reg ? `<label>Повтори пароль
              <input class="input" name="password2" type="password" autocomplete="new-password" maxlength="128" required></label>
              <p class="muted auth-note">🔑 Восстановления пароля нет — запомни его или сохрани в менеджере паролей.</p>` : ""}
            <p class="auth-error" id="auth-error" ${error ? "" : "hidden"}>${esc(error)}</p>
            <button class="btn" type="submit" id="auth-submit">${reg ? "Создать аккаунт" : "Войти"}</button>
          </form>
        </div>
      </div>`;
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
