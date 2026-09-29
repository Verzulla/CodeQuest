"""pwfake — учебная реализация синхронного API Playwright без браузера.

Страницы — HTML, который отдаёт учебное веб-приложение App (обычный Python). pwfake
разбирает HTML в дерево, ищет элементы локаторами Playwright и выполняет действия:
клики по ссылкам и кнопкам, заполнение и отправку форм, переходы. Время — фейковое:
элементы с data-appear-after="мс" появляются не сразу, а expect() и действия ждут их
автоматически (как настоящий Playwright), продвигая часы страницы.

В реальном проекте импорт такой:  from playwright.sync_api import Page, expect
Здесь:                            from pwfake.sync_api import Page, expect
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import parse_qsl, urljoin, urlsplit

__all__ = ["App", "Redirect", "Response", "Page", "Locator", "expect", "sync_playwright",
           "set_app", "Error", "TimeoutError"]

DEFAULT_TIMEOUT = 5000   # мс, как у Playwright
TICK = 100               # шаг фейковых часов при ожидании

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FAKE_PNG = b"\x89PNG\r\n\x1a\n" + bytes(24)


class Error(Exception):
    """Ошибка Playwright (например, нарушение строгости локатора)."""


class TimeoutError(Error):  # noqa: A001 — как в Playwright
    """Не дождались элемента или условия."""


# ---------------------------------------------------------------- приложение

class Redirect:
    def __init__(self, path):
        self.path = path


class Response:
    def __init__(self, html, status=200):
        self.html = html
        self.status = status


class Request:
    def __init__(self, method, path, query, form):
        self.method = method
        self.path = path
        self.query = query
        self.form = form


class App:
    """Учебное веб-приложение: маршруты «путь → функция, возвращающая HTML».

        app = App()

        @app.route("/login")
        def login(request):
            return "<form method='post'>…</form>"

        @app.route("/login", method="POST")
        def do_login(request):
            return Redirect("/dashboard") if request.form["user"] == "anna" else "<p>Ошибка</p>"
    """

    def __init__(self):
        self.routes = {}
        self.state = {}      # общее состояние приложения (например, корзина)
        self.requests = []   # журнал запросов — удобно для проверок

    def route(self, path, method="GET"):
        def decorator(func):
            self.routes[(method.upper(), path)] = func
            return func
        return decorator

    def handle(self, method, path, query=None, form=None):
        request = Request(method, path, query or {}, form or {})
        self.requests.append(request)
        handler = self.routes.get((method, path))
        if handler is None:
            return Response("<html><head><title>404</title></head><body><h1>Страница не найдена</h1></body></html>", 404)
        result = handler(request)
        if isinstance(result, str):
            return Response(result)
        return result


_DEFAULT_APP = None


def set_app(app):
    """Приложение для browser.new_page() без явного app (так делают проверки заданий)."""
    global _DEFAULT_APP
    _DEFAULT_APP = app


# ---------------------------------------------------------------- DOM

class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []   # Node или str

    # --- обход
    def elements(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.elements()

    def ancestors(self):
        node = self.parent
        while node is not None and node.tag != "#root":
            yield node
            node = node.parent

    # --- текст
    def raw_text(self):
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            elif child.tag not in ("script", "style"):
                parts.append(child.raw_text())
        return "".join(parts)

    def text(self):
        return " ".join(self.raw_text().split())

    def classes(self):
        return self.attrs.get("class", "").split()

    def __repr__(self):
        attrs = "".join(f' {k}="{v}"' for k, v in self.attrs.items() if v is not None)
        return f"<{self.tag}{attrs}>"


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {})
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, [(k, "" if v is None else v) for k, v in attrs], self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, [(k, "" if v is None else v) for k, v in attrs], self.current)
        self.current.children.append(node)

    def handle_endtag(self, tag):
        node = self.current
        while node is not None and node.tag != tag:
            node = node.parent
        if node is not None and node.parent is not None:
            self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse_html(html):
    parser = _Parser()
    parser.feed(html)
    parser.close()
    return parser.root


# ---------------------------------------------------------------- CSS-селекторы (подмножество)

_COMPOUND = re.compile(
    r"""(?P<tag>[a-zA-Z][\w-]*|\*)?
        (?P<rest>(?:\#[\w-]+|\.[\w-]+|\[[^\]]+\]|:has-text\((?:"[^"]*"|'[^']*')\)|:visible|:checked|:disabled|:enabled)*)""",
    re.X,
)
_PART = re.compile(r"""\#[\w-]+|\.[\w-]+|\[[^\]]+\]|:has-text\((?:"[^"]*"|'[^']*')\)|:visible|:checked|:disabled|:enabled""")
_ATTR = re.compile(r"""\[\s*([\w-]+)\s*(?:([*^$~]?=)\s*(?:"([^"]*)"|'([^']*)'|([^\]\s]*)))?\s*\]""")


def _split_selector(selector):
    """'form > input.x' → [('', 'form'), ('>', 'input.x')]."""
    tokens = []
    buf = ""
    depth = 0
    quote = None
    for ch in selector.strip():
        if quote:
            buf += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf += ch
        elif ch in "[(":
            depth += 1
            buf += ch
        elif ch in "])":
            depth -= 1
            buf += ch
        elif depth == 0 and ch in " >":
            if buf:
                tokens.append(buf)
                buf = ""
            if ch == ">":
                tokens.append(">")
        else:
            buf += ch
    if buf:
        tokens.append(buf)
    parts = []
    combinator = ""
    for tok in tokens:
        if tok == ">":
            combinator = ">"
        else:
            parts.append((combinator, tok))
            combinator = ""
    return parts


def _match_compound(node, compound, page):
    m = _COMPOUND.fullmatch(compound)
    if not m or not compound:
        raise Error(f"Неподдерживаемый селектор: {compound!r}")
    tag = m.group("tag")
    if tag and tag != "*" and node.tag != tag.lower():
        return False
    for part in _PART.findall(m.group("rest") or ""):
        if part.startswith("#"):
            if node.attrs.get("id") != part[1:]:
                return False
        elif part.startswith("."):
            if part[1:] not in node.classes():
                return False
        elif part.startswith("["):
            am = _ATTR.fullmatch(part)
            if not am:
                raise Error(f"Неподдерживаемый селектор атрибута: {part!r}")
            name, op, v1, v2, v3 = am.groups()
            if name not in node.attrs:
                return False
            if op:
                value = v1 if v1 is not None else v2 if v2 is not None else v3
                actual = node.attrs.get(name) or ""
                ok = {"=": actual == value, "*=": value in actual, "^=": actual.startswith(value),
                      "$=": actual.endswith(value), "~=": value in actual.split()}[op]
                if not ok:
                    return False
        elif part.startswith(":has-text("):
            text = part[len(":has-text("):-1][1:-1]
            if text.lower() not in node.text().lower():
                return False
        elif part == ":visible":
            if not page._visible(node):
                return False
        elif part == ":checked":
            if "checked" not in node.attrs:
                return False
        elif part == ":disabled":
            if "disabled" not in node.attrs:
                return False
        elif part == ":enabled":
            if "disabled" in node.attrs:
                return False
    return True


def _css_select(roots, selector, page):
    parts = _split_selector(selector)
    if not parts:
        raise Error("Пустой селектор")
    result = []
    for root in roots:
        for node in root.elements():
            if node in result:
                continue
            if _matches_chain(node, parts, page, root):
                result.append(node)
    return result


def _matches_chain(node, parts, page, root=None):
    # Как querySelectorAll: результат — потомки корня, а предки в селекторе могут быть где угодно.
    combinator, compound = parts[-1]
    if not _match_compound(node, compound, page):
        return False
    if len(parts) == 1:
        return True
    rest = parts[:-1]
    if combinator == ">":
        parent = node.parent
        return parent is not None and parent.tag != "#root" and _matches_chain(parent, rest, page)
    return any(_matches_chain(a, rest, page) for a in node.ancestors())


# ---------------------------------------------------------------- роли и доступные имена

_HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_TEXTBOX_TYPES = {"", "text", "email", "search", "tel", "url"}


def _role(node):
    if "role" in node.attrs:
        return node.attrs["role"]
    tag, typ = node.tag, node.attrs.get("type", "").lower()
    if tag == "button":
        return "button"
    if tag == "input":
        if typ in ("submit", "button", "reset", "image"):
            return "button"
        if typ == "checkbox":
            return "checkbox"
        if typ == "radio":
            return "radio"
        if typ == "number":
            return "spinbutton"
        if typ in _TEXTBOX_TYPES:
            return "textbox"
        return None
    if tag == "textarea":
        return "textbox"
    if tag == "select":
        return "combobox"
    if tag == "a" and "href" in node.attrs:
        return "link"
    if tag in _HEADINGS:
        return "heading"
    if tag == "img":
        return "img"
    if tag in ("ul", "ol"):
        return "list"
    if tag == "li":
        return "listitem"
    if tag == "table":
        return "table"
    if tag == "tr":
        return "row"
    if tag in ("td",):
        return "cell"
    if tag == "th":
        return "columnheader"
    if tag == "nav":
        return "navigation"
    if tag == "form":
        return "form"
    if tag == "dialog":
        return "dialog"
    return None


def _label_text(node, root):
    node_id = node.attrs.get("id")
    if node_id:
        for label in root.elements():
            if label.tag == "label" and label.attrs.get("for") == node_id:
                return label.text()
    for ancestor in node.ancestors():
        if ancestor.tag == "label":
            return ancestor.text()
    return None


def _accessible_name(node, root):
    if node.attrs.get("aria-label"):
        return " ".join(node.attrs["aria-label"].split())
    if node.tag in ("input", "textarea", "select"):
        if node.attrs.get("type", "").lower() in ("submit", "button", "reset"):
            return node.attrs.get("value", "")
        label = _label_text(node, root)
        if label:
            return label
        return node.attrs.get("title") or node.attrs.get("placeholder") or ""
    if node.tag == "img":
        return node.attrs.get("alt", "")
    return node.text() or node.attrs.get("title", "")


def _text_matches(actual, expected, exact):
    actual = " ".join((actual or "").split())
    if isinstance(expected, re.Pattern):
        return expected.search(actual) is not None
    expected = " ".join(str(expected).split())
    if exact:
        return actual == expected
    return expected.lower() in actual.lower()


# ---------------------------------------------------------------- страница

class Page:
    def __init__(self, app=None, base_url="http://app.test"):
        self.app = app or _DEFAULT_APP
        if self.app is None:
            raise Error("pwfake: у страницы нет приложения (App)")
        self.base_url = base_url.rstrip("/")
        self.clock = 0           # фейковое время, мс
        self.default_timeout = DEFAULT_TIMEOUT
        self._root = parse_html("<html><head><title></title></head><body></body></html>")
        self._url = "about:blank"
        self._history = []
        self.status = None
        self._loaded_at = 0

    # --- навигация
    @property
    def url(self):
        return self._url

    def _resolve(self, url):
        if url.startswith("/"):
            return self.base_url + url
        if url.startswith("http"):
            return url
        return urljoin(self._url if self._url != "about:blank" else self.base_url + "/", url)

    def _load(self, method, url, form=None, remember=True):
        full = self._resolve(url)
        parts = urlsplit(full)
        response = self.app.handle(method, parts.path or "/", dict(parse_qsl(parts.query)), form)
        hops = 0
        while isinstance(response, Redirect):
            hops += 1
            if hops > 10:
                raise Error("Слишком много перенаправлений")
            full = self._resolve(response.path)
            parts = urlsplit(full)
            response = self.app.handle("GET", parts.path or "/", dict(parse_qsl(parts.query)))
        if remember and self._url != "about:blank":
            self._history.append(self._url)
        self._url = full
        self.status = response.status
        self._root = parse_html(response.html)
        self._loaded_at = self.clock
        return response

    def goto(self, url, **_):
        return self._load("GET", url)

    def reload(self, **_):
        return self._load("GET", self._url, remember=False)

    def go_back(self, **_):
        if self._history:
            url = self._history.pop()
            self._load("GET", url, remember=False)

    def title(self):
        for node in self._root.elements():
            if node.tag == "title":
                return node.text()
        return ""

    def content(self):
        return self._serialize(self._root)

    def _serialize(self, node):
        out = []
        for child in node.children:
            if isinstance(child, str):
                out.append(child)
            else:
                attrs = "".join(f' {k}="{v}"' for k, v in child.attrs.items())
                inner = "" if child.tag in VOID else self._serialize(child) + f"</{child.tag}>"
                out.append(f"<{child.tag}{attrs}>{inner}")
        return "".join(out)

    # --- время
    def wait_for_timeout(self, timeout):
        self.clock += int(timeout)

    def set_default_timeout(self, timeout):
        self.default_timeout = int(timeout)

    def _present(self, node):
        appear = node.attrs.get("data-appear-after")
        if appear is not None and self.clock - self._loaded_at < int(appear):
            return False
        gone = node.attrs.get("data-disappear-after")
        if gone is not None and self.clock - self._loaded_at >= int(gone):
            return False
        return all(self._present(a) for a in node.ancestors()) if node.parent and node.parent.tag != "#root" else True

    def _visible(self, node):
        if not self._present(node):
            return False
        for n in [node, *node.ancestors()]:
            if "hidden" in n.attrs:
                return False
            style = n.attrs.get("style", "").replace(" ", "").lower()
            if "display:none" in style or "visibility:hidden" in style:
                return False
            if n.tag in ("head", "script", "style", "title", "template"):
                return False
            if n.tag == "input" and n.attrs.get("type", "").lower() == "hidden":
                return False
        return True

    # --- локаторы
    def locator(self, selector):
        return Locator(self, [("css", selector)])

    def get_by_role(self, role, name=None, exact=False, **_):
        return Locator(self, [("role", (role, name, exact))])

    def get_by_text(self, text, exact=False):
        return Locator(self, [("text", (text, exact))])

    def get_by_label(self, text, exact=False):
        return Locator(self, [("label", (text, exact))])

    def get_by_placeholder(self, text, exact=False):
        return Locator(self, [("attr", ("placeholder", text, exact))])

    def get_by_test_id(self, test_id):
        return Locator(self, [("attr", ("data-testid", test_id, True))])

    def get_by_alt_text(self, text, exact=False):
        return Locator(self, [("attr", ("alt", text, exact))])

    def get_by_title(self, text, exact=False):
        return Locator(self, [("attr", ("title", text, exact))])

    # --- сокращения, как у Playwright
    def click(self, selector, **kw):
        self.locator(selector).click(**kw)

    def fill(self, selector, value, **kw):
        self.locator(selector).fill(value, **kw)

    def text_content(self, selector, **kw):
        return self.locator(selector).text_content(**kw)

    def is_visible(self, selector):
        return self.locator(selector).is_visible()

    def screenshot(self, path=None, **_):
        if path:
            with open(path, "wb") as f:
                f.write(FAKE_PNG)
        return FAKE_PNG

    def close(self):
        pass

    # --- поиск элементов (внутреннее)
    def _all(self):
        return [n for n in self._root.elements() if self._present(n)]

    def _query(self, steps):
        nodes = [self._root]
        for kind, arg in steps:
            nodes = self._apply(nodes, kind, arg)
        return nodes

    def _apply(self, roots, kind, arg):
        if kind == "nth":
            return [roots[arg]] if -len(roots) <= arg < len(roots) else []
        if kind == "filter":
            has_text, has_not_text = arg
            out = []
            for n in roots:
                t = n.text()
                if has_text is not None and not _text_matches(t, has_text, False):
                    continue
                if has_not_text is not None and _text_matches(t, has_not_text, False):
                    continue
                out.append(n)
            return out
        candidates = []
        for root in roots:
            for n in root.elements():
                if n not in candidates and self._present(n):
                    candidates.append(n)
        if kind == "css":
            selector = arg
            if selector.startswith("text="):
                value = selector[5:]
                exact = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
                return self._by_text(candidates, value.strip("\"'"), exact)
            if selector.startswith(("xpath=", "//")):
                raise Error("XPath в pwfake не поддерживается — используй CSS или get_by_*")
            return [n for n in _css_select(roots, selector, self) if self._present(n)]
        if kind == "role":
            role, name, exact = arg
            out = [n for n in candidates if _role(n) == role and self._visible(n)]
            if name is not None:
                out = [n for n in out if _text_matches(_accessible_name(n, self._root), name, exact)]
            return out
        if kind == "text":
            text, exact = arg
            return self._by_text(candidates, text, exact)
        if kind == "label":
            text, exact = arg
            out = []
            for n in candidates:
                if n.tag not in ("input", "textarea", "select"):
                    continue
                label = _label_text(n, self._root) or n.attrs.get("aria-label")
                if label is not None and _text_matches(label, text, exact):
                    out.append(n)
            return out
        if kind == "attr":
            name, value, exact = arg
            return [n for n in candidates if name in n.attrs and _text_matches(n.attrs[name], value, exact)]
        raise Error(f"Неизвестный тип локатора: {kind}")

    def _by_text(self, candidates, text, exact):
        matching = [n for n in candidates if n.tag not in ("html", "head", "body", "script", "style", "title")
                    and _text_matches(n.text(), text, exact)]
        # как в Playwright: самый «глубокий» элемент с этим текстом
        return [n for n in matching if not any(c in matching for c in n.elements())]

    # --- действия (внутреннее)
    def _wait(self, predicate, timeout, what):
        timeout = self.default_timeout if timeout is None else timeout
        waited = 0
        while True:
            result = predicate()
            if result:
                return result
            if waited >= timeout:
                raise TimeoutError(f"Timeout {timeout}ms exceeded: {what}")
            self.clock += TICK
            waited += TICK

    def _submit(self, form, extra=None):
        values = {}
        for n in form.elements():
            name = n.attrs.get("name")
            if not name or "disabled" in n.attrs:
                continue
            if n.tag == "input":
                typ = n.attrs.get("type", "text").lower()
                if typ in ("checkbox", "radio"):
                    if "checked" in n.attrs:
                        values[name] = n.attrs.get("value", "on")
                elif typ in ("submit", "button", "reset", "image"):
                    continue
                else:
                    values[name] = n.attrs.get("value", "")
            elif n.tag == "textarea":
                values[name] = n.attrs.get("value", n.raw_text())
            elif n.tag == "select":
                chosen = [o for o in n.elements() if o.tag == "option" and "selected" in o.attrs]
                options = [o for o in n.elements() if o.tag == "option"]
                opt = chosen[0] if chosen else (options[0] if options else None)
                if opt is not None:
                    values[name] = opt.attrs.get("value", opt.text())
        if extra:
            values.update(extra)
        method = form.attrs.get("method", "GET").upper()
        action = form.attrs.get("action") or urlsplit(self._url).path or "/"
        if method == "GET":
            query = "&".join(f"{k}={v}" for k, v in values.items())
            self._load("GET", action + ("?" + query if query else ""))
        else:
            self._load("POST", action, form=values)

    def _click(self, node):
        if "disabled" in node.attrs:
            raise Error(f"Элемент {node!r} недоступен (disabled)")
        toggle = node.attrs.get("data-toggle")
        if toggle:
            for target in _css_select([self._root], toggle, self):
                if "hidden" in target.attrs:
                    del target.attrs["hidden"]
                else:
                    target.attrs["hidden"] = ""
            return
        link = node if node.tag == "a" else next((a for a in node.ancestors() if a.tag == "a"), None)
        if link is not None and "href" in link.attrs:
            self._load("GET", link.attrs["href"])
            return
        if node.tag == "input" and node.attrs.get("type", "").lower() in ("checkbox", "radio"):
            self._set_checked(node, not ("checked" in node.attrs) if node.attrs.get("type").lower() == "checkbox" else True)
            return
        is_submit = (node.tag == "button" and node.attrs.get("type", "submit").lower() == "submit") or \
                    (node.tag == "input" and node.attrs.get("type", "").lower() in ("submit", "image"))
        if is_submit:
            form = next((a for a in node.ancestors() if a.tag == "form"), None)
            if form is not None:
                extra = {node.attrs["name"]: node.attrs.get("value", "")} if node.attrs.get("name") else None
                self._submit(form, extra)
            return
        href = node.attrs.get("data-href")
        if href:
            self._load("GET", href)

    def _set_checked(self, node, checked):
        if node.attrs.get("type", "").lower() == "radio" and checked:
            name = node.attrs.get("name")
            for other in self._root.elements():
                if other.tag == "input" and other.attrs.get("type", "").lower() == "radio" and other.attrs.get("name") == name:
                    other.attrs.pop("checked", None)
        if checked:
            node.attrs["checked"] = ""
        else:
            node.attrs.pop("checked", None)


# ---------------------------------------------------------------- локатор

class Locator:
    def __init__(self, page, steps):
        self.page = page
        self._steps = steps

    def __repr__(self):
        return f"<Locator {self._describe()}>"

    def _describe(self):
        return " >> ".join(f"{k}={a!r}" for k, a in self._steps)

    def _resolve(self):
        return self.page._query(self._steps)

    # --- построение
    def locator(self, selector):
        return Locator(self.page, self._steps + [("css", selector)])

    def get_by_role(self, role, name=None, exact=False, **_):
        return Locator(self.page, self._steps + [("role", (role, name, exact))])

    def get_by_text(self, text, exact=False):
        return Locator(self.page, self._steps + [("text", (text, exact))])

    def get_by_label(self, text, exact=False):
        return Locator(self.page, self._steps + [("label", (text, exact))])

    def get_by_placeholder(self, text, exact=False):
        return Locator(self.page, self._steps + [("attr", ("placeholder", text, exact))])

    def get_by_test_id(self, test_id):
        return Locator(self.page, self._steps + [("attr", ("data-testid", test_id, True))])

    def nth(self, index):
        return Locator(self.page, self._steps + [("nth", index)])

    @property
    def first(self):
        return self.nth(0)

    @property
    def last(self):
        return self.nth(-1)

    def filter(self, has_text=None, has_not_text=None, **_):
        return Locator(self.page, self._steps + [("filter", (has_text, has_not_text))])

    def all(self):
        return [self.nth(i) for i in range(self.count())]

    # --- чтение (без ожидания, как в Playwright для count/is_*)
    def count(self):
        return len(self._resolve())

    def _one(self, timeout=None, need_visible=True, action="действие"):
        def find():
            nodes = self._resolve()
            if len(nodes) > 1:
                raise Error(f"strict mode violation: {self._describe()} resolved to {len(nodes)} elements")
            if not nodes:
                return None
            if need_visible and not self.page._visible(nodes[0]):
                return None
            return nodes[0]
        return self.page._wait(find, timeout, f"waiting for {self._describe()} ({action})")

    def text_content(self, timeout=None):
        return self._one(timeout, need_visible=False, action="text_content").raw_text()

    def inner_text(self, timeout=None):
        return self._one(timeout, action="inner_text").text()

    def all_text_contents(self):
        return [n.raw_text() for n in self._resolve()]

    def all_inner_texts(self):
        return [n.text() for n in self._resolve()]

    def input_value(self, timeout=None):
        node = self._one(timeout, need_visible=False, action="input_value")
        if node.tag == "select":
            chosen = [o for o in node.elements() if o.tag == "option" and "selected" in o.attrs]
            return chosen[0].attrs.get("value", chosen[0].text()) if chosen else ""
        return node.attrs.get("value", "")

    def get_attribute(self, name, timeout=None):
        return self._one(timeout, need_visible=False, action="get_attribute").attrs.get(name)

    def is_visible(self):
        nodes = self._resolve()
        if len(nodes) > 1:
            raise Error(f"strict mode violation: {self._describe()} resolved to {len(nodes)} elements")
        return bool(nodes) and self.page._visible(nodes[0])

    def is_hidden(self):
        return not self.is_visible()

    def is_enabled(self):
        return "disabled" not in self._one(action="is_enabled", need_visible=False).attrs

    def is_disabled(self):
        return not self.is_enabled()

    def is_checked(self):
        return "checked" in self._one(action="is_checked", need_visible=False).attrs

    # --- действия
    def click(self, timeout=None, **_):
        self.page._click(self._one(timeout, action="click"))

    def fill(self, value, timeout=None, **_):
        node = self._one(timeout, action="fill")
        if node.tag not in ("input", "textarea") or node.attrs.get("type", "").lower() in ("checkbox", "radio", "submit", "button"):
            raise Error(f"Элемент {node!r} нельзя заполнить: это не поле ввода")
        if "disabled" in node.attrs or "readonly" in node.attrs:
            raise Error(f"Поле {node!r} недоступно для ввода")
        node.attrs["value"] = str(value)

    def clear(self, timeout=None):
        self.fill("", timeout=timeout)

    def press_sequentially(self, text, timeout=None, **_):
        node = self._one(timeout, action="press_sequentially")
        node.attrs["value"] = node.attrs.get("value", "") + str(text)

    def press(self, key, timeout=None, **_):
        node = self._one(timeout, action="press")
        if key == "Enter" and node.tag == "input":
            form = next((a for a in node.ancestors() if a.tag == "form"), None)
            if form is not None:
                self.page._submit(form)

    def check(self, timeout=None, **_):
        self.page._set_checked(self._one(timeout, action="check"), True)

    def uncheck(self, timeout=None, **_):
        self.page._set_checked(self._one(timeout, action="uncheck"), False)

    def set_checked(self, checked, timeout=None, **_):
        self.page._set_checked(self._one(timeout, action="set_checked"), checked)

    def select_option(self, value=None, label=None, timeout=None, **_):
        node = self._one(timeout, action="select_option")
        options = [o for o in node.elements() if o.tag == "option"]
        target = None
        for o in options:
            if (value is not None and o.attrs.get("value", o.text()) == value) or \
               (label is not None and o.text() == label) or \
               (value is not None and label is None and o.text() == value):
                target = o
                break
        if target is None:
            raise Error(f"Нет варианта {value or label!r} в {node!r}")
        for o in options:
            o.attrs.pop("selected", None)
        target.attrs["selected"] = ""
        return [target.attrs.get("value", target.text())]

    def hover(self, timeout=None, **_):
        self._one(timeout, action="hover")

    def wait_for(self, state="visible", timeout=None):
        if state in ("visible", "attached"):
            self.page._wait(lambda: self.count() > 0 and (state == "attached" or self.is_visible()), timeout,
                            f"waiting for {self._describe()} to be {state}")
        else:
            self.page._wait(lambda: self.count() == 0 or (state == "hidden" and not self.is_visible()), timeout,
                            f"waiting for {self._describe()} to be {state}")

    def screenshot(self, path=None, **_):
        return self.page.screenshot(path=path)


# ---------------------------------------------------------------- expect

class _Expect:
    def __init__(self, target, negate=False):
        self.target = target
        self.negate = negate

    def __getattr__(self, name):
        if name.startswith("not_to_"):
            positive = getattr(_Expect(self.target, not self.negate), "to_" + name[len("not_to_"):])
            return positive
        raise AttributeError(name)

    def _check(self, predicate, describe, timeout=None):
        page = self.target.page if isinstance(self.target, Locator) else self.target
        timeout = page.default_timeout if timeout is None else timeout
        waited = 0
        last = None
        while True:
            try:
                ok, last = predicate()
            except Error:
                ok, last = False, None
            if ok != self.negate:
                return
            if waited >= timeout:
                prefix = "не ожидалось" if self.negate else "ожидалось"
                raise AssertionError(f"{prefix}: {describe}; фактически: {last!r} (ждали {timeout} мс)")
            page.clock += TICK
            waited += TICK

    # --- страница
    def to_have_url(self, url, timeout=None):
        page = self.target
        self._check(lambda: (_text_matches(page.url, url, True) if not isinstance(url, re.Pattern)
                             else url.search(page.url) is not None, page.url), f"URL {url!r}", timeout)

    def to_have_title(self, title, timeout=None):
        page = self.target
        self._check(lambda: (_text_matches(page.title(), title, True), page.title()), f"заголовок {title!r}", timeout)

    # --- локатор
    def _nodes(self):
        return self.target._resolve()

    def to_be_visible(self, timeout=None):
        loc = self.target
        self._check(lambda: (loc.is_visible(), "виден" if loc.is_visible() else "не виден"), f"{loc._describe()} виден", timeout)

    def to_be_hidden(self, timeout=None):
        loc = self.target
        self._check(lambda: (not loc.is_visible(), "скрыт" if not loc.is_visible() else "виден"), f"{loc._describe()} скрыт", timeout)

    def to_be_attached(self, timeout=None):
        self._check(lambda: (bool(self._nodes()), len(self._nodes())), f"{self.target._describe()} есть в DOM", timeout)

    def to_have_count(self, count, timeout=None):
        self._check(lambda: (len(self._nodes()) == count, len(self._nodes())), f"{self.target._describe()}: {count} элементов", timeout)

    def to_have_text(self, expected, timeout=None, use_inner_text=False):
        def pred():
            nodes = self._nodes()
            texts = [n.text() for n in nodes]
            if isinstance(expected, (list, tuple)):
                return len(texts) == len(expected) and all(_text_matches(t, e, True) for t, e in zip(texts, expected)), texts
            if len(nodes) != 1:
                return False, texts
            return _text_matches(texts[0], expected, True), texts[0]
        self._check(pred, f"текст {expected!r}", timeout)

    def to_contain_text(self, expected, timeout=None):
        def pred():
            texts = [n.text() for n in self._nodes()]
            if isinstance(expected, (list, tuple)):
                return all(any(_text_matches(t, e, False) for t in texts) for e in expected), texts
            return any(_text_matches(t, expected, False) for t in texts), texts
        self._check(pred, f"содержит {expected!r}", timeout)

    def to_have_value(self, value, timeout=None):
        loc = self.target
        self._check(lambda: (_text_matches(loc.input_value(timeout=0), value, True), loc.input_value(timeout=0)), f"значение {value!r}", timeout)

    def to_be_enabled(self, timeout=None):
        loc = self.target
        self._check(lambda: (loc.is_enabled(), "enabled" if loc.is_enabled() else "disabled"), "элемент доступен", timeout)

    def to_be_disabled(self, timeout=None):
        loc = self.target
        self._check(lambda: (not loc.is_enabled(), "disabled" if not loc.is_enabled() else "enabled"), "элемент недоступен", timeout)

    def to_be_checked(self, timeout=None, checked=True):
        loc = self.target
        self._check(lambda: (loc.is_checked() == checked, loc.is_checked()), f"checked={checked}", timeout)

    def to_have_attribute(self, name, value, timeout=None):
        loc = self.target
        self._check(lambda: (_text_matches(loc.get_attribute(name, timeout=0) or "", value, True), loc.get_attribute(name, timeout=0)),
                    f"атрибут {name}={value!r}", timeout)

    def to_have_class(self, expected, timeout=None):
        def pred():
            nodes = self._nodes()
            cls = nodes[0].attrs.get("class", "") if len(nodes) == 1 else None
            return (cls is not None and _text_matches(cls, expected, True)), cls
        self._check(pred, f"класс {expected!r}", timeout)


def expect(target):
    """expect(locator).to_be_visible() / expect(page).to_have_url(...) — с автоожиданием."""
    if not isinstance(target, (Locator, Page)):
        raise Error("expect() принимает Locator или Page")
    return _Expect(target)


# ---------------------------------------------------------------- sync_playwright

class _Browser:
    def __init__(self, name):
        self.name = name
        self.pages = []

    def new_page(self, app=None, base_url="http://app.test", **_):
        page = Page(app, base_url=base_url)
        self.pages.append(page)
        return page

    def new_context(self, **kwargs):
        return self

    def close(self):
        self.pages.clear()


class _BrowserType:
    def __init__(self, name):
        self.name = name

    def launch(self, headless=True, **_):
        return _Browser(self.name)


class _Playwright:
    def __init__(self):
        self.chromium = _BrowserType("chromium")
        self.firefox = _BrowserType("firefox")
        self.webkit = _BrowserType("webkit")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def stop(self):
        pass


def sync_playwright():
    return _Playwright()
