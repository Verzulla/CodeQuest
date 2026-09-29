"""Демо-сайт «Шоп» для UI-заданий: вход, каталог с поиском и сортировкой, корзина, оформление заказа.

    from pwfake.demo import shop_app
    app = shop_app()              # исправный сайт
    app = shop_app(bug="...")     # сайт с багом — так задания проверяют, что тест его ловит

Пользователи: anna / secret, boris / qwerty123; blocked — заблокирован.
Товары каталога появляются через 800 мс (пока виден «Загрузка…») — учимся ждать правильно.
"""
from html import escape
import re

from .sync_api import App, Redirect

USERS = {"anna": "secret", "boris": "qwerty123", "blocked": "blocked"}

PRODUCTS = [
    {"id": 1, "name": "Клавиатура", "price": 3500, "stock": True},
    {"id": 2, "name": "Мышь", "price": 1200, "stock": True},
    {"id": 3, "name": "Монитор", "price": 15000, "stock": True},
    {"id": 4, "name": "Наушники", "price": 4200, "stock": False},
    {"id": 5, "name": "Коврик", "price": 600, "stock": True},
]

BUGS = {
    "login_no_redirect": "после верного входа остаётся на /login",
    "login_no_error": "при неверном пароле не показывает ошибку",
    "wrong_username": "в шапке имя другого пользователя",
    "search_broken": "поиск игнорирует запрос",
    "sort_broken": "сортировка не работает",
    "cart_count": "счётчик корзины в шапке не меняется",
    "total_wrong": "«Итого» не учитывает количество",
    "remove_broken": "«Удалить» ничего не удаляет",
    "checkout_no_validation": "заказ оформляется без имени",
    "slow": "каталог грузится 3 секунды",
    "too_slow": "каталог грузится 8 секунд",
}

SORTS = [("", "По умолчанию"), ("price", "Сначала дешёвые"), ("price_desc", "Сначала дорогие"), ("name", "По названию")]


def shop_app(bug=None):
    if bug is not None and bug not in BUGS:
        raise ValueError(f"Нет такого бага: {bug}. Есть: {', '.join(BUGS)}")
    app = App()
    app.state.update(user=None, cart={}, orders=[], remember=False)
    by_id = {p["id"]: p for p in PRODUCTS}

    def cart_count():
        return 0 if bug == "cart_count" else sum(app.state["cart"].values())

    def layout(title, body):
        user = app.state["user"]
        if user:
            shown = "boris" if bug == "wrong_username" and user != "boris" else user
            who = f'<span data-testid="username">{shown}</span> <a href="/logout">Выйти</a>'
        else:
            who = '<a href="/login">Войти</a>'
        return (f"<html><head><title>{title}</title></head><body>"
                f'<nav><a href="/catalog">Каталог</a> <a href="/cart" data-testid="cart-link">Корзина ({cart_count()})</a> {who}</nav>'
                f"<main>{body}</main></body></html>")

    def error_box(message):
        return f'<div class="error" role="alert">{message}</div>' if message else ""

    @app.route("/")
    def home(request):
        return Redirect("/catalog")

    def login_page(error="", user=""):
        return layout("Вход", f"""
<h1>Вход</h1>
<form method="post" action="/login">
  <label for="user">Логин</label> <input id="user" name="user" value="{escape(user)}">
  <label for="password">Пароль</label> <input id="password" name="password" type="password">
  <label><input type="checkbox" name="remember"> Запомнить меня</label>
  <button type="submit">Войти</button>
</form>
{error_box(error)}""")

    @app.route("/login")
    def login(request):
        return login_page()

    @app.route("/login", method="POST")
    def do_login(request):
        user = request.form.get("user", "").strip()
        password = request.form.get("password", "")
        if not user or not password:
            return login_page("Введите логин и пароль", user)
        if USERS.get(user) != password:
            return login_page("" if bug == "login_no_error" else "Неверный логин или пароль", user)
        if user == "blocked":
            return login_page("Пользователь заблокирован", user)
        app.state["user"] = user
        app.state["remember"] = "remember" in request.form
        if bug == "login_no_redirect":
            return login_page()
        return Redirect("/catalog")

    @app.route("/logout")
    def logout(request):
        app.state["user"] = None
        return Redirect("/login")

    @app.route("/catalog")
    def catalog(request):
        q = request.query.get("q", "").strip()
        sort = request.query.get("sort", "")
        items = list(PRODUCTS)
        if q and bug != "search_broken":
            items = [p for p in items if q.lower() in p["name"].lower()]
        if bug != "sort_broken":
            if sort == "price":
                items.sort(key=lambda p: p["price"])
            elif sort == "price_desc":
                items.sort(key=lambda p: -p["price"])
            elif sort == "name":
                items.sort(key=lambda p: p["name"])
        cards = []
        for p in items:
            if p["stock"]:
                buy = (f'<form method="post" action="/cart/add"><input type="hidden" name="id" value="{p["id"]}">'
                       f'<button type="submit">В корзину</button></form>')
            else:
                buy = '<button disabled>Нет в наличии</button>'
            cards.append(f'<div class="card" data-testid="product"><h3>{p["name"]}</h3> '
                         f'<span class="price">{p["price"]} ₽</span> {buy}</div>')
        options = "".join(f'<option value="{v}"{" selected" if v == sort else ""}>{label}</option>' for v, label in SORTS)
        delay = {"slow": 3000, "too_slow": 8000}.get(bug, 800)
        return layout("Каталог", f"""
<h1>Каталог</h1>
<form method="get" action="/catalog" role="search">
  <input name="q" placeholder="Поиск" value="{escape(q)}">
  <select name="sort" aria-label="Сортировка">{options}</select>
  <button type="submit">Найти</button>
</form>
<div id="spinner" data-disappear-after="{delay}">Загрузка…</div>
<div id="products" data-appear-after="{delay}">{"".join(cards) or '<p class="empty">Ничего не найдено</p>'}</div>""")

    @app.route("/cart/add", method="POST")
    def cart_add(request):
        pid = int(request.form["id"])
        app.state["cart"][pid] = app.state["cart"].get(pid, 0) + 1
        return Redirect("/catalog")

    @app.route("/cart/remove", method="POST")
    def cart_remove(request):
        if bug != "remove_broken":
            app.state["cart"].pop(int(request.form["id"]), None)
        return Redirect("/cart")

    @app.route("/cart")
    def cart(request):
        rows, total = [], 0
        for pid, qty in app.state["cart"].items():
            p = by_id[pid]
            total += p["price"] * (1 if bug == "total_wrong" else qty)
            rows.append(f'<tr data-testid="cart-row"><td class="name">{p["name"]}</td> <td class="qty">{qty}</td> '
                        f'<td class="sum">{p["price"] * qty} ₽</td> <td><form method="post" action="/cart/remove">'
                        f'<input type="hidden" name="id" value="{pid}"><button type="submit">Удалить</button></form></td></tr>')
        if not rows:
            return layout("Корзина", '<h1>Корзина</h1><p class="empty">Корзина пуста</p>')
        return layout("Корзина", f"""
<h1>Корзина</h1>
<table><tr><th>Товар</th> <th>Кол-во</th> <th>Сумма</th> <th></th></tr>{"".join(rows)}</table>
<p id="total">Итого: {total} ₽</p>
<a href="/checkout">Оформить заказ</a>""")

    def checkout_page(error="", form=None):
        form = form or {}
        options = "".join(f'<option value="{v}"{" selected" if form.get("delivery") == v else ""}>{label}</option>'
                          for v, label in [("courier", "Курьер"), ("pickup", "Самовывоз")])
        return layout("Оформление заказа", f"""
<h1>Оформление заказа</h1>
<form method="post" action="/checkout">
  <label for="name">Имя</label> <input id="name" name="name" value="{escape(form.get("name", ""))}">
  <label for="phone">Телефон</label> <input id="phone" name="phone" placeholder="+79991234567" value="{escape(form.get("phone", ""))}">
  <label for="delivery">Доставка</label> <select id="delivery" name="delivery">{options}</select>
  <label><input type="checkbox" name="agree"> Согласен с условиями</label>
  <button type="submit">Подтвердить</button>
</form>
{error_box(error)}""")

    @app.route("/checkout")
    def checkout(request):
        if not app.state["user"]:
            return Redirect("/login")
        if not app.state["cart"]:
            return Redirect("/cart")
        return checkout_page()

    @app.route("/checkout", method="POST")
    def do_checkout(request):
        form = request.form
        if not app.state["user"]:
            return Redirect("/login")
        if not form.get("name", "").strip() and bug != "checkout_no_validation":
            return checkout_page("Укажите имя", form)
        if not re.fullmatch(r"\+7\d{10}", form.get("phone", "").strip()):
            return checkout_page("Неверный телефон", form)
        if "agree" not in form:
            return checkout_page("Нужно согласие с условиями", form)
        number = 1001 + len(app.state["orders"])
        app.state["orders"].append({"number": number, "user": app.state["user"], "items": dict(app.state["cart"]),
                                    "name": form["name"], "phone": form["phone"], "delivery": form.get("delivery")})
        app.state["cart"] = {}
        return Redirect(f"/order?id={number}")

    @app.route("/order")
    def order(request):
        number = int(request.query.get("id", 0))
        found = next((o for o in app.state["orders"] if o["number"] == number), None)
        if found is None:
            return layout("Заказ не найден", "<h1>Заказ не найден</h1>")
        delivery = {"courier": "Курьер", "pickup": "Самовывоз"}.get(found["delivery"], "")
        return layout("Заказ оформлен", f"""
<h1>Заказ оформлен</h1>
<p data-testid="order-number">Номер заказа: {number}</p>
<p>Доставка: {delivery}</p>""")

    return app
