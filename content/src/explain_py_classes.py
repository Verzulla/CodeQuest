"""Тема «Классы и ООП» — ручные разборы решений (кнопка «Показать решение»).

EXPLAIN = {slug задания: x(...)}; задания без разбора получают автоматический (app/explain.py)."""
from ._lib import x

P = "oop"

EXPLAIN = {

# ===== Модуль 1. Первый класс =====

f"{P}-m1-l1-e1": x(
    idea="Класс — шаблон, объект — конкретный экземпляр. `__init__` заполняет атрибуты нового объекта, `self` — это сам объект.",
    lines=[
        ("self.name = name", "У каждой собаки своё имя."),
        ('a = Dog("Рекс")\nb = Dog("Шарик")', "Два независимых объекта."),
        ("print(a.bark())", "`self` внутри метода — это `a`."),
    ],
    mistake="Думать, что второй объект перезапишет имя первого."),

f"{P}-m1-l1-e2": x(
    idea="Метод меняет состояние объекта через `self`.",
    lines=[
        ("self.value += step", "Меняется атрибут объекта."),
        ("c.inc()\nc.inc(5)", "1 + 5 = 6."),
    ],
    mistake="Ожидать 0 — изменения сохраняются в объекте."),

f"{P}-m1-l1-e3": x(
    idea="`b = a` — не копия объекта, а второе имя. Изменения через `b` видны и через `a`.",
    lines=[
        ("b = a", "Один объект."),
        ("b.items.append(2)", "Меняется общий список."),
        ("print(a is b)", "`True`."),
    ],
    mistake="Думать, что присваивание копирует объект."),

f"{P}-m1-l1-e4": x(
    idea="Конструктор принимает значения и раскладывает их по атрибутам `self`.",
    lines=[
        ("def __init__(self, name, email):", "`self` — первый параметр всегда."),
        ("self.name = name\n        self.email = email", "Атрибуты объекта."),
    ],
    mistake="Забыть `self.` — получатся локальные переменные, которые исчезнут после `__init__`."),

f"{P}-m1-l1-e5": x(
    idea="Методы используют атрибуты, сохранённые конструктором.",
    lines=[
        ("return self.width * self.height", "3 · 4 = 12."),
        ("return 2 * (self.width + self.height)", "2 · 7 = 14."),
    ],
    mistake="Писать `width` без `self.` — `NameError`."),

f"{P}-m1-l1-e6": x(
    idea="Объект хранит состояние (баланс), методы его меняют и охраняют правила.",
    lines=[
        ("def __init__(self, owner, balance=0):", "Баланс по умолчанию."),
        ("self.balance += amount", "Пополнение."),
        ('if amount > self.balance:\n            raise ValueError("Недостаточно средств")', "Правило."),
    ],
    mistake="Проверять после вычитания — баланс уже уйдёт в минус."),

f"{P}-m1-l1-e7": x(
    idea="Три действия с одним атрибутом: задать, увеличить, обнулить.",
    lines=[
        ("self.seconds += 1", "`tick`."),
        ("self.seconds = 0", "`reset`."),
    ],
    mistake="`seconds = 0` без `self.` — изменится локальная переменная."),

f"{P}-m1-l1-e8": x(
    idea="Класс-обёртка над списком: каждый объект получает свой список в `__init__`.",
    lines=[
        ("self.items = []", "Свой список у каждого стека."),
        ("if not self.items:\n            return None", "Пустой — `None` вместо ошибки."),
        ("return self.items[-1]", "`peek` не снимает."),
    ],
    mistake="Объявить `items = []` на уровне класса — стеки будут делить один список."),

# ===== __init__ и значения по умолчанию =====

f"{P}-init-e1": x(
    idea="Параметры по умолчанию работают в `__init__` как в обычной функции. `vars(obj)` — словарь атрибутов.",
    lines=[
        ("self.active = True", "Атрибут без параметра."),
        ("print(a.role, vars(a))", "Все атрибуты Бори."),
    ],
    mistake="Ожидать, что `active` не попадёт в `vars`."),

f"{P}-init-e2": x(
    idea="Недостающий аргумент конструктора — `TypeError`. Атрибуты можно добавить объекту и позже.",
    lines=[
        ("Point(1)", "Нет `y`."),
        ("p.z = 3", "Новый атрибут только у этого объекта."),
    ],
    mistake="Ожидать ошибку на `p.z = 3`."),

f"{P}-init-e3": x(
    idea="`None` по умолчанию и новый список внутри — у каждого заказа свой.",
    lines=[("self.items = items if items is not None else []", "Новый `[]` на каждый вызов.")],
    mistake="`def __init__(self, items=[])` — общий список на все заказы."),

f"{P}-init-e4": x(
    idea="Три атрибута, у одного значение по умолчанию.",
    lines=[("def __init__(self, name, price, qty=1):", "`qty` — последним.")],
    mistake="Поставить `qty=1` раньше обязательных — `SyntaxError`."),

f"{P}-init-e5": x(
    idea="Все параметры необязательны — объект можно создать без аргументов.",
    lines=[('def __init__(self, host="localhost", port=8080, debug=False):', "`Config()` работает.")],
    mistake="Забыть сохранить какой-то параметр в `self`."),

f"{P}-init-e6": x(
    idea="Изменяемое значение по умолчанию — ловушка. `None` и новый список внутри.",
    lines=[("if items is None:\n            items = []", "Свой список.")],
    mistake="`items=[]` — заказы будут делить список."),

f"{P}-init-e7": x(
    idea="Конструктор может проверять данные и не давать создать некорректный объект.",
    lines=[('if celsius < -273.15:\n            raise ValueError("ниже абсолютного нуля")', "Проверка до сохранения.")],
    mistake="Сохранить значение, а потом проверять — объект с плохими данными уже создан."),

f"{P}-init-e8": x(
    idea="В конструкторе можно вычислить производные атрибуты.",
    lines=[("self.distance = round((x * x + y * y) ** 0.5, 2)", "(3, 4) → 5.0.")],
    mistake="Если потом изменить `x`, `distance` не пересчитается — это стоит помнить."),

# ===== Методы и self =====

f"{P}-methods-e1": x(
    idea="Метод, который возвращает `self`, позволяет цеплять вызовы.",
    lines=[
        ("return self", "Тот же объект."),
        ("c.inc().inc().inc()", "Три увеличения."),
    ],
    mistake="Без `return self` второй `.inc()` вызовется у `None`."),

f"{P}-methods-e2": x(
    idea="Метод может вызывать другой метод того же объекта через `self`.",
    lines=[
        ("return sum(price for _, price in self.items)", "800."),
        ('return f"{len(self.items)} товара на {self.total()} ₽"', "`self.total()`."),
    ],
    mistake="Писать `total()` без `self.` — `NameError`."),

f"{P}-methods-e3": x(
    idea="`g.hello()` — то же, что `Greeter.hello(g)`: объект передаётся как `self`. Метод можно сохранить в переменную — он помнит свой объект.",
    lines=[
        ("print(g.hello(), Greeter.hello(g))", "Одинаковый результат."),
        ("m = g.hello", "Связанный метод."),
    ],
    mistake="Думать, что `self` — магия. Это просто первый аргумент."),

f"{P}-methods-e4": x(
    idea="Список пар в объекте, методы считают по нему.",
    lines=[
        ("self.items.append((name, price))", "Кортеж — один элемент."),
        ("return len(self.items)", "Количество."),
    ],
    mistake="`append(name, price)` — два аргумента нельзя."),

f"{P}-methods-e5": x(
    idea="Методы меняют баланс и возвращают новое значение.",
    lines=[
        ("self.balance += amount\n        return self.balance", "Пополнение и новый баланс."),
        ('if amount > self.balance:\n            raise ValueError("недостаточно средств")', "Проверка до изменения."),
    ],
    mistake="Не вернуть баланс — вызов даст `None`."),

f"{P}-methods-e6": x(
    idea="Словарь «задача → выполнена» хранит порядок добавления и статус.",
    lines=[
        ("self.tasks[task] = False", "Новая задача."),
        ("return [task for task, finished in self.tasks.items() if not finished]", "Невыполненные."),
    ],
    mistake="Два списка — сложнее держать в согласии."),

f"{P}-methods-e7": x(
    idea="Оба метода возвращают `self` — цепочки работают.",
    lines=[
        ("self.value += step\n        return self", "`inc`."),
        ("self.value = 0\n        return self", "`reset` тоже возвращает объект."),
    ],
    mistake="Забыть `return self` в `reset`."),

f"{P}-methods-e8": x(
    idea="Объект хранит текст, методы считают разное.",
    lines=[
        ("return len(self.text.split())", "Слова."),
        ('return len(self.text.replace(" ", ""))', "Символы без пробелов."),
        ("return max(words, key=words.count)", "При равенстве — первое."),
    ],
    mistake="Не опускать регистр — `Тест` и `тест` станут разными."),

# ===== Атрибуты класса и __str__ =====

f"{P}-m1-l2-e1": x(
    idea="Атрибут класса общий для всех объектов. Через `Test.count` его меняют все экземпляры.",
    lines=[
        ("count = 0", "Один на класс."),
        ("Test.count += 1", "Каждый новый объект увеличивает."),
    ],
    mistake="`self.count += 1` — создаст атрибут объекта, общий счётчик не изменится."),

f"{P}-m1-l2-e2": x(
    idea="`__str__` — вид для людей (`print`), `__repr__` — для разработчика, в том числе внутри списков.",
    lines=[
        ("print(p)", "Использует `__str__`."),
        ("print([p])", "Внутри списка — `__repr__`."),
    ],
    mistake="Ожидать `[(1, 2)]`."),

f"{P}-m1-l2-e3": x(
    idea="Изменяемый атрибут класса — общий для всех объектов. Добавление в одну корзину видно во всех.",
    lines=[
        ("items = []", "Один список на класс."),
        ("print(b.items)", "Яблоко и у `b`."),
    ],
    mistake="Ожидать `[]`."),

f"{P}-m1-l2-e4": x(
    idea="`__str__` возвращает строку, которую покажет `print`.",
    lines=[('return f"«{self.title}» — {self.author}"', "Ёлочки и длинное тире.")],
    mistake="`print` внутри `__str__` — метод должен **вернуть** строку."),

f"{P}-m1-l2-e5": x(
    idea="Счётчик номеров — атрибут класса. Объект берёт текущий номер и увеличивает счётчик.",
    lines=[
        ("next_id = 1", "Общий."),
        ("self.id = Bug.next_id\n        Bug.next_id += 1", "Сначала взять, потом увеличить."),
    ],
    mistake="`self.next_id += 1` — у каждого объекта своя копия, номера повторятся."),

f"{P}-m1-l2-e6": x(
    idea="Список, объявленный в теле класса, общий. Свой список создают в `__init__`.",
    lines=[("self.items = []", "В конструкторе — у каждой корзины свой.")],
    mistake="Оставить `items = []` в теле класса."),

f"{P}-m1-l2-e7": x(
    idea="`!r` в f-строке даёт вид «как в коде» — строку в кавычках.",
    lines=[
        ("return self.name", "`__str__`."),
        ('return f"User({self.name!r})"', "`User('Аня')`."),
    ],
    mistake="`f\"User({self.name})\"` — без кавычек."),

f"{P}-m1-l2-e8": x(
    idea="Общий счётчик в классе и флаг `closed` у каждой сессии — повторный `close` ничего не меняет.",
    lines=[
        ("Session.active += 1", "Открыли."),
        ("if not self.closed:\n            self.closed = True\n            Session.active -= 1", "Закрываем один раз."),
    ],
    mistake="Уменьшать без флага — повторный `close` уведёт счётчик в минус."),

# ===== Объекты, ссылки и копии =====

f"{P}-identity-e1": x(
    idea="Без своего `__eq__` объекты сравниваются по тому, один ли это объект. `c = a` — тот же объект.",
    lines=[
        ("print(a == b, a is b, a is c)", "Разные объекты с одинаковым значением не равны."),
        ("c.value = 99", "Меняется `a`."),
    ],
    mistake="Ожидать `a == b` — `True`."),

f"{P}-identity-e2": x(
    idea="В функцию передаётся сам объект — изменение его атрибута видно снаружи.",
    lines=[("user.name = user.name.upper()", "Меняется атрибут объекта `u`.")],
    mistake="Ожидать `аня`."),

f"{P}-identity-e3": x(
    idea="`copy.copy` — мелкая копия: новый объект, но список внутри общий. `deepcopy` копирует и вложенное.",
    lines=[
        ("t2 = copy.copy(t1)", "Делит список с `t1`."),
        ("t3 = copy.deepcopy(t1)", "Свой список."),
    ],
    mistake="Ожидать, что `copy` защитит список."),

f"{P}-identity-e4": x(
    idea="Новый объект со своей копией списка.",
    lines=[("return User(user.name, list(user.tags))", "`list(...)` — новый список.")],
    mistake="`User(user.name, user.tags)` — теги будут общими."),

f"{P}-identity-e5": x(
    idea="Независимая копия матрицы — копия каждой строки.",
    lines=[("return Matrix([list(row) for row in self.rows])", "Копия каждой строки.")],
    mistake="`Matrix(list(self.rows))` — строки останутся общими."),

f"{P}-identity-e6": x(
    idea="`id(obj)` — уникальный номер объекта. Множество id считает разные объекты.",
    lines=[("return len({id(o) for o in objs})", "`b` дважды — один id.")],
    mistake="Считать по `value` — два разных Box(1) сольются."),

f"{P}-identity-e7": x(
    idea="Метод возвращает **новый** объект, не меняя текущий.",
    lines=[("return Settings({**self.values, key: value})", "Новый словарь, новый объект.")],
    mistake="`self.values[key] = value` — изменит исходный."),

f"{P}-identity-e8": x(
    idea="Конструктор копирует переданный список — внешние изменения не затронут команду.",
    lines=[("self.members = list(members)", "Своя копия.")],
    mistake="`self.members = members` — общий список."),

# ===== Модуль 2. Наследование и super() =====

f"{P}-m2-l1-e1": x(
    idea="Наследник может переопределить метод; унаследованные методы, вызывающие его через `self`, используют версию наследника.",
    lines=[
        ('return "Я говорю: " + self.speak()', "Метод родителя."),
        ('return "Мяу"', "Переопределение у `Cat`."),
    ],
    mistake="Ожидать `...` для кошки."),

f"{P}-m2-l1-e2": x(
    idea="`super()` вызывает метод родителя. Цепочка: C → B → A, результат собирается обратно.",
    lines=[("return super().hello() + \"C\"", "`\"AB\" + \"C\"`.")],
    mistake="Ожидать `CBA` — сначала получаем результат родителя, потом дописываем."),

f"{P}-m2-l1-e3": x(
    idea="`isinstance` учитывает наследование: кошка — это и `Cat`, и `Animal`.",
    lines=[
        ("print(isinstance(c, Cat), isinstance(c, Animal), isinstance(c, Dog))", "Кошка — не собака."),
        ("print(issubclass(Dog, Animal))", "Класс — подкласс."),
    ],
    mistake="Ожидать `False` для `Animal`."),

f"{P}-m2-l1-e4": x(
    idea="Наследник вызывает конструктор родителя через `super().__init__`, а потом добавляет своё.",
    lines=[
        ("class Admin(User):", "Наследование."),
        ("super().__init__(name)", "Имя и роль — от родителя."),
        ("self.permissions = permissions", "Своё поле."),
    ],
    mistake="Не вызвать `super().__init__` — у админа не будет `name`."),

f"{P}-m2-l1-e5": x(
    idea="Сначала родитель ставит `role = \"user\"`, потом наследник перезаписывает. Порядок важен.",
    lines=[
        ("super().__init__(name)", "Роль user."),
        ('self.role = "admin"', "Перезапись после."),
        ("return action in self.permissions", "Проверка права."),
    ],
    mistake="Поставить `self.role = \"admin\"` до `super().__init__` — родитель вернёт `user`."),

f"{P}-m2-l1-e6": x(
    idea="Каждая фигура по-своему считает площадь, а общая функция просто вызывает `area()` — полиморфизм.",
    lines=[
        ("class Square(Shape):", "Наследник."),
        ("return 3.14 * self.r * self.r", "Площадь круга."),
        ("return sum(s.area() for s in shapes)", "Не важно, какая фигура."),
    ],
    mistake="Проверять тип фигуры через `isinstance` в `total_area` — теряется смысл наследования."),

f"{P}-m2-l1-e7": x(
    idea="Переопределённый метод может использовать результат родителя через `super()`.",
    lines=[
        ("super().__init__(name, salary)", "Общие поля."),
        ("return super().yearly() + self.bonus", "Годовой доход плюс бонус."),
    ],
    mistake="Копировать формулу `salary * 12` в наследника — дублирование."),

f"{P}-m2-l1-e8": x(
    idea="Наследник меняет сообщение и передаёт его в метод родителя — логика хранения остаётся в одном месте.",
    lines=[
        ("super().__init__()", "Родитель создаёт `self.lines`."),
        ('super().log(f"[{self.prefix}] {msg}")', "Добавляем префикс и сохраняем родительским методом."),
    ],
    mistake="`self.log(...)` внутри `log` — бесконечная рекурсия."),

# ===== Переопределение и MRO =====

f"{P}-override-e1": x(
    idea="Метод родителя, вызывающий `self.hello()`, использует переопределённую версию наследника.",
    lines=[
        ('return "run: " + self.hello()', "`self` — реальный объект."),
        ("print(Child().run())", "`hello` у ребёнка своя."),
    ],
    mistake="Ожидать `run: Base` во второй строке."),

f"{P}-override-e2": x(
    idea="Метод ищется по цепочке классов (MRO): сначала сам класс, потом родители, в конце `object`.",
    lines=[
        ("print(C().who())", "В C и B нет — найдено в A."),
        ("print([cls.__name__ for cls in C.__mro__])", "Порядок поиска."),
    ],
    mistake="Ожидать ошибку — метод наследуется через несколько уровней."),

f"{P}-override-e3": x(
    idea="При множественном наследовании родители проверяются слева направо.",
    lines=[
        ("class Report(Loggable, Savable):", "Сначала Loggable."),
        ("print(r.info(), r.save())", "`info` из Loggable, `save` — только в Savable."),
    ],
    mistake="Ожидать `save` для `info`."),

f"{P}-override-e4": x(
    idea="Общий метод `describe` в базе, наследники задают своё имя (атрибут класса) и свою площадь.",
    lines=[
        ('name = "квадрат"', "Атрибут класса наследника перекрывает базовый."),
        ("return self.side ** 2", "Своя площадь."),
    ],
    mistake="Переписывать `describe` в каждом наследнике."),

f"{P}-override-e5": x(
    idea="Наследник берёт результат родителя и дополняет его.",
    lines=[
        ("h = super().headers()", "Базовые заголовки."),
        ('h["Authorization"] = f"Bearer {self.token}"', "Добавка."),
    ],
    mistake="Писать заголовки заново — `Accept` можно потерять."),

f"{P}-override-e6": x(
    idea="Наследник добавляет проверку и делегирует основную работу родителю.",
    lines=[
        ('if len(self.items) >= self.limit:\n            raise OverflowError("стек полон")', "Проверка."),
        ("super().push(x)", "Добавление — у родителя."),
    ],
    mistake="`self.push(x)` — бесконечная рекурсия."),

f"{P}-override-e7": x(
    idea="`__mro__` — кортеж классов в порядке поиска. `object` в конце — отфильтровываем.",
    lines=[("return [c.__name__ for c in cls.__mro__ if c is not object]", "B, A.")],
    mistake="Сравнивать по имени `\"object\"` — работает, но `is object` точнее."),

f"{P}-override-e8": x(
    idea="Миксин — маленький класс с полезным поведением, который подмешивают к другим. `vars(self)` работает для любого объекта.",
    lines=[
        ("return dict(vars(self))", "Копия атрибутов."),
        ("class User(JsonMixin):", "Подмешали."),
    ],
    mistake="`return vars(self)` — изменение словаря изменит объект."),

# ===== Полиморфизм и ABC =====

f"{P}-m2-l2-e1": x(
    idea="Полиморфизм: разные классы с одинаковым методом — один и тот же вызов работает для любого.",
    lines=[("print(driver.open(\"/login\"))", "Не важно, какой браузер.")],
    mistake="Думать, что нужен общий родитель — хватает одинакового метода."),

f"{P}-m2-l2-e2": x(
    idea="Абстрактный класс нельзя создать напрямую; наследник обязан реализовать абстрактные методы.",
    lines=[
        ("@abstractmethod", "Метод без реализации."),
        ("Base()", "`TypeError`."),
        ("print(Impl().run())", "Наследник реализовал — работает."),
    ],
    mistake="Ожидать, что `Base()` создастся."),

f"{P}-m2-l2-e3": x(
    idea="Абстрактный класс задаёт интерфейс, наследники — реализацию.",
    lines=[
        ("class Notifier(ABC):", "Наследник ABC."),
        ("@abstractmethod\n    def send(self, text): ...", "Обязательный метод."),
        ('return f"email: {text}"', "Реализация."),
    ],
    mistake="Забыть `ABC` — `@abstractmethod` не запретит создание."),

f"{P}-m2-l2-e4": x(
    idea="Функции всё равно, какой класс у объекта — важно, что есть `send`.",
    lines=[("return [n.send(text) for n in notifiers]", "Результаты по порядку.")],
    mistake="Проверять тип каждого объекта — лишнее."),

f"{P}-m2-l2-e5": x(
    idea="Шаблонный метод: общий алгоритм в базе (`run`), изменяемый шаг — в наследниках (`check`).",
    lines=[
        ('return "PASS" if self.check(value) else "FAIL"', "Общее для всех проверок."),
        ('return value != ""', "`NotEmpty`."),
        ("return value > 0", "`IsPositive`."),
    ],
    mistake="Дублировать `run` в каждом наследнике."),

f"{P}-m2-l2-e6": x(
    idea="Один вызов `send` — три разных поведения.",
    lines=[
        ('return f"sms: {text[:5]}"', "Первые 5 символов: `тест ` с пробелом."),
        ('return f"push: {text.upper()}"', "Заглавными."),
    ],
    mistake="Забыть пробел в `тест `."),

f"{P}-m2-l2-e7": x(
    idea="Интерфейс хранилища задан абстрактно, реализация на словаре — одна из возможных.",
    lines=[
        ("@abstractmethod\n    def save(self, key, value):", "Обязательные методы."),
        ("return self.data.get(key)", "Нет ключа — `None`."),
    ],
    mistake="`self.data[key]` — `KeyError`."),

f"{P}-m2-l2-e8": x(
    idea="Утиная типизация: «если крякает как утка — это утка». Общий родитель не нужен.",
    lines=[("return sum(s.area() for s in shapes)", "Любой объект с `area()`.")],
    mistake="`isinstance` в `total_area` — ограничит набор фигур."),

# ===== isinstance и type =====

f"{P}-isinstance-e1": x(
    idea="`isinstance` учитывает наследование, `type(x) is` — нет. Любой объект — это `object`.",
    lines=[
        ("print(type(d) is Dog, type(d) is Animal)", "Точный тип — только Dog."),
        ("print(issubclass(Dog, Animal), issubclass(Animal, Dog))", "Наследование в одну сторону."),
    ],
    mistake="Ожидать `True` для `type(d) is Animal`."),

f"{P}-isinstance-e2": x(
    idea="`bool` — подкласс `int`, поэтому `True` проходит проверку на число.",
    lines=[("print(type(v).__name__, isinstance(v, (int, float)))", "`bool True`.")],
    mistake="Ожидать `False` для `True`."),

f"{P}-isinstance-e3": x(
    idea="Имя класса — `type(e).__name__` или `e.__class__.__name__`; родители — в `__bases__`.",
    lines=[
        ("print(NotFound.__bases__[0].__name__)", "Прямой родитель."),
        ("print(isinstance(e, Exception))", "Через цепочку наследования."),
    ],
    mistake="Ожидать `Exception` как прямого родителя."),

f"{P}-isinstance-e4": x(
    idea="Число, но не `bool` — две проверки.",
    lines=[("return [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]", "`[1, 3.5]`.")],
    mistake="Без второй проверки `True` попадёт в результат."),

f"{P}-isinstance-e5": x(
    idea="Цепочка проверок типа; в конце — имя типа.",
    lines=[
        ('if isinstance(value, str):\n        return f"строка из {len(value)} символов"', "Строки — первыми."),
        ("if isinstance(value, (list, tuple)):", "Коллекции."),
        ("return type(value).__name__", "Остальное."),
    ],
    mistake="Проверять `len` у всего подряд — у чисел длины нет."),

f"{P}-isinstance-e6": x(
    idea="Счётчик по имени типа.",
    lines=[
        ("name = type(o).__name__", "`int`, `str`, `NoneType`."),
        ("result[name] = result.get(name, 0) + 1", "Подсчёт."),
    ],
    mistake="Использовать сам тип ключом — задание просит имена."),

f"{P}-isinstance-e7": x(
    idea="`isinstance` с базовым классом ловит всех наследников: `Timeout` — это `ServerError`.",
    lines=[
        ('if isinstance(error, ServerError):\n        return "critical"', "`Timeout` тоже сюда."),
        ('if isinstance(error, ClientError):\n        return "warning"', "`NotFound` — сюда."),
    ],
    mistake="`type(error) is ServerError` — `Timeout` не пройдёт."),

f"{P}-isinstance-e8": x(
    idea="Рекурсивно разворачиваем списки и кортежи; строки — нет, хотя их тоже можно перебирать.",
    lines=[
        ("if isinstance(item, (list, tuple)):\n            result.extend(flatten(item))", "Спуск."),
        ("else:\n            result.append(item)", "`\"ab\"` целиком."),
    ],
    mistake="Проверять «можно ли перебрать» — строка развалится на буквы."),

# ===== Композиция =====

f"{P}-composition-e1": x(
    idea="Композиция: объект содержит другой объект и делегирует ему работу. «Машина имеет двигатель».",
    lines=[
        ("self.engine = Engine(power)", "Объект внутри объекта."),
        ('return f"{self.model}: {self.engine.start()}"', "Делегирование."),
    ],
    mistake="Наследовать `Car` от `Engine` — машина не является двигателем."),

f"{P}-composition-e2": x(
    idea="Объект-контейнер хранит список других объектов и работает с их атрибутами.",
    lines=[("return max(self.students, key=lambda s: s.score).name", "Боря — 95.")],
    mistake="Сравнивать объекты без ключа — `TypeError`."),

f"{P}-composition-e3": x(
    idea="Зависимость передаётся снаружи — её легко подменить фейком в тестах.",
    lines=[
        ("self.api = api", "Сервис не создаёт API сам."),
        ("print(Service(FakeApi()).report())", "Тест с подменой."),
    ],
    mistake="Создавать `RealApi()` внутри `Service` — подменить не получится."),

f"{P}-composition-e4": x(
    idea="Заказ хранит позиции и суммирует их `cost()`.",
    lines=[
        ("return self.price * self.qty", "Стоимость позиции."),
        ("return sum(item.cost() for item in self.items)", "Итого."),
    ],
    mistake="Хранить в заказе только цены — потеряется количество."),

f"{P}-composition-e5": x(
    idea="Сервис работает с любым хранилищем, у которого есть `save` и `load`.",
    lines=[
        ('if self.storage.load(name) is not None:\n            raise ValueError("занято")', "Проверка."),
        ("self.storage.save(name, True)", "Регистрация."),
    ],
    mistake="`if self.storage.load(name):` — значение `0` или `False` сломает проверку."),

f"{P}-composition-e6": x(
    idea="Библиотека хранит объекты книг и отвечает на вопросы о них.",
    lines=[
        ("return [b.title for b in self.books if b.author == author]", "Порядок добавления."),
        ("return sorted({b.author for b in self.books})", "Уникальные авторы."),
    ],
    mistake="Хранить книги словарём по автору — теряется порядок добавления."),

f"{P}-composition-e7": x(
    idea="Каналы приходят как `*channels`, хранятся списком.",
    lines=[
        ("self.channels = list(channels)", "Кортеж → список."),
        ("return [ch.send(text) for ch in self.channels]", "Во все каналы."),
    ],
    mistake="Ожидать, что `channels` — список, передаваемый одним аргументом."),

f"{P}-composition-e8": x(
    idea="Раннер получает отчётчик снаружи и сообщает ему результаты. Вывод можно менять, не трогая раннер.",
    lines=[
        ("except AssertionError:\n                failed += 1\n                self.reporter.failed(name)", "Провал."),
        ("else:\n                self.reporter.passed(name)", "Успех."),
    ],
    mistake="Вызывать `passed` внутри `try` — при ошибке после него запишутся оба результата."),

# ===== Модуль 3. Dunder-методы =====

f"{P}-m3-l1-e1": x(
    idea="Без `__eq__` объекты равны, только если это один и тот же объект. `__eq__` задаёт сравнение по смыслу.",
    lines=[
        ("print(P(1) == P(1))", "Два разных объекта — `False`."),
        ("return self.x == other.x", "Сравнение по значению."),
    ],
    mistake="Ожидать `True` в первой строке."),

f"{P}-m3-l1-e2": x(
    idea="Магические методы делают объект похожим на встроенную коллекцию: `len`, `in`, индексы.",
    lines=[
        ("def __len__(self):", "`len(p)`."),
        ("def __contains__(self, song):", "`\"B\" in p`."),
        ("def __getitem__(self, i):", "`p[-1]`."),
    ],
    mistake="Ожидать ошибку от `p[-1]` — индекс передаётся в список."),

f"{P}-m3-l1-e3": x(
    idea="`__add__` вызывается при `+`, `__eq__` — при `==`. `+` возвращает **новый** объект.",
    lines=[
        ("return Money(self.amount + other.amount)", "Новый объект."),
        ("return self.amount == other.amount", "Сравнение сумм."),
    ],
    mistake="`self.amount += other.amount; return self` — испортит левый операнд."),

f"{P}-m3-l1-e4": x(
    idea="`__lt__` — сравнение `<`. Кортежи чисел сравниваются поэлементно — как версии.",
    lines=[("return self.parts < other.parts", "(1, 9, 2) < (1, 10, 0).")],
    mistake="Сравнивать `self.text` — строки дадут неверный порядок."),

f"{P}-m3-l1-e5": x(
    idea="Три метода делают набор похожим на коллекцию: длина, проверка `in`, перебор.",
    lines=[
        ("return len(self.tests)", "`__len__`."),
        ("return item in self.tests", "`__contains__`."),
        ("return iter(self.tests)", "`__iter__` возвращает итератор."),
    ],
    mistake="`return self.tests` в `__iter__` — нужен именно итератор."),

f"{P}-m3-l1-e6": x(
    idea="Истинность объекта: `__bool__`, а если его нет — `__len__` (длина 0 — ложь).",
    lines=[
        ("print(bool(Queue([])), bool(Queue([1])))", "Через `__len__`."),
        ("if Flag(False):", "Через `__bool__`."),
    ],
    mistake="Считать любой объект истинным — это так только без этих методов."),

f"{P}-m3-l1-e7": x(
    idea="`__iter__` с `yield` — генератор значений; `__contains__` проверяет диапазон арифметикой, без перебора.",
    lines=[
        ("while current < self.stop:\n            yield current\n            current += 1", "Значения по одному."),
        ("return max(0, self.stop - self.start)", "Пустой диапазон — 0, не минус."),
        ("return self.start <= x < self.stop", "Мгновенно."),
    ],
    mistake="`stop` включительно — у `range` конец не входит."),

f"{P}-m3-l1-e8": x(
    idea="`__call__` делает объект вызываемым, как функцию, — при этом он может хранить состояние.",
    lines=[
        ("def __call__(self, x):", "`double(21)` вызывает этот метод."),
        ("self.calls += 1", "Счётчик вызовов в объекте."),
    ],
    mistake="Назвать метод `call` — объект не станет вызываемым."),

# ===== Сравнение, сортировка, хеш =====

f"{P}-compare-e1": x(
    idea="`__lt__` задаёт порядок — после этого работают `sorted`, `max` и `<`.",
    lines=[
        ("return self.priority < other.priority", "Сравнение по приоритету."),
        ("print(max(tasks).name, Task(\"a\", 1) < Task(\"b\", 2))", "`max` тоже использует `<`."),
    ],
    mistake="Ожидать ошибку от `max` — хватает `__lt__`."),

f"{P}-compare-e2": x(
    idea="Если определить `__eq__`, но не `__hash__`, объект становится нехешируемым — его нельзя положить в множество.",
    lines=[
        ("print(Point(1, 2) == Point(1, 2), Point(1, 2) != Point(3, 4))", "`!=` работает через `__eq__`."),
        ("{Point(1, 2)}", "`unhashable type`."),
    ],
    mistake="Ожидать, что множество создастся."),

f"{P}-compare-e3": x(
    idea="`@total_ordering` достраивает `<=`, `>`, `>=` из `__eq__` и `__lt__`.",
    lines=[
        ("@total_ordering", "Декоратор класса."),
        ("print(a < b, a <= b, a > b, a >= Grade(4), a != b)", "Все операторы работают."),
    ],
    mistake="Ожидать `TypeError` на `<=`."),

f"{P}-compare-e4": x(
    idea="Для множеств и ключей нужны оба: `__eq__` и согласованный с ним `__hash__`.",
    lines=[
        ("return (self.x, self.y) == (other.x, other.y)", "Равенство."),
        ("return hash((self.x, self.y))", "Хеш кортежа тех же полей."),
    ],
    mistake="Хешировать другие поля, чем сравниваешь, — равные объекты окажутся «разными»."),

f"{P}-compare-e5": x(
    idea="Место серьёзности в списке — число для сравнения. `@total_ordering` даёт остальные операторы.",
    lines=[
        ("return LEVELS.index(self.severity)", "low → 0, critical → 3."),
        ("return self.rank() < other.rank()", "`__lt__`."),
    ],
    mistake="Сравнивать строки severity — алфавитный порядок неверен."),

f"{P}-compare-e6": x(
    idea="Если класс менять нельзя — порядок задают ключом `sorted`.",
    lines=[("return [u.name for u in sorted(users, key=lambda u: (-u.age, u.name))]", "Возраст по убыванию, имя по алфавиту.")],
    mistake="`sorted(users)` — `TypeError`: объекты не сравниваются."),

f"{P}-compare-e7": x(
    idea="`NotImplemented` — сигнал «не умею сравнивать с этим типом»; Python тогда вернёт `False` для `==`.",
    lines=[
        ("if not isinstance(other, Money):\n            return NotImplemented", "Сравнение с чужим типом."),
        ('if self.currency != other.currency:\n            raise ValueError("разные валюты")', "Рубли с долларами не сравнить."),
    ],
    mistake="`return False` вместо `NotImplemented` — работает, но Python не сможет попробовать сравнение с другой стороны."),

f"{P}-compare-e8": x(
    idea="Равенство и хеш по email в нижнем регистре — множество само определит дубли.",
    lines=[
        ("return hash(self.email.lower())", "Согласовано с `__eq__`."),
        ("if u not in seen:", "Использует `__hash__` и `__eq__`."),
    ],
    mistake="Хеш от email без `lower()` — одинаковые адреса попадут в разные «корзины»."),

# ===== property, classmethod, staticmethod =====

f"{P}-m3-l2-e1": x(
    idea="`@property` — метод, который читается как атрибут и каждый раз пересчитывается.",
    lines=[
        ("@property\n    def fahrenheit(self):", "Без скобок при вызове."),
        ("t.celsius = 0", "После изменения — новое значение."),
    ],
    mistake="Писать `t.fahrenheit()` — это уже не метод, а свойство."),

f"{P}-m3-l2-e3": x(
    idea="`@classmethod` получает класс (`cls`) и служит альтернативным конструктором. `@staticmethod` — обычная функция внутри класса.",
    lines=[
        ('name, email = text.split(",")', "Разбор строки."),
        ("return cls(name, email)", "Новый объект через `cls`."),
        ('return "@" in email', "Ни `self`, ни `cls` не нужны."),
    ],
    mistake="`return User(...)` вместо `cls(...)` — наследники получат не свой класс."),

f"{P}-m3-l2-e4": x(
    idea="Свойство с setter перехватывает присваивание — и в конструкторе тоже, потому что там стоит `self.price = price`.",
    lines=[
        ("return self._price", "Настоящее значение — в «скрытом» атрибуте."),
        ('if value < 0:\n            raise ValueError("Цена не может быть отрицательной")', "Проверка при записи."),
    ],
    mistake="В setter писать `self.price = value` — бесконечная рекурсия."),

f"{P}-m3-l2-e6": x(
    idea="Свойство без setter — только для чтения, но значение пересчитывается при изменении исходных данных.",
    lines=[
        ("c.r = 10", "Диаметр станет 20."),
        ("c.diameter = 1", "Присвоить нельзя — `AttributeError`."),
    ],
    mistake="Ожидать, что `diameter` запомнил 10."),

f"{P}-m3-l2-e7": x(
    idea="`classmethod` создаёт объект через `cls` — счётчик в `__init__` сработал. `staticmethod` вызывается и через класс, и через объект.",
    lines=[
        ("return cls([\"сыр\", \"томаты\"])", "Альтернативный конструктор."),
        ('print(Pizza.is_valid("ананас"), p.is_valid("сыр"))', "`False True`."),
    ],
    mistake="Ожидать `count` = 0 — объект создан через `__init__`."),

f"{P}-m3-l2-e8": x(
    idea="Getter скрывает пароль, setter проверяет длину, а настоящее значение лежит в `_value`.",
    lines=[
        ('return "*" * len(self._value)', "Наружу — только звёздочки."),
        ('if len(new) < 8:\n            raise ValueError("слишком короткий")', "Проверка и в конструкторе."),
        ("return guess == self._value", "Сравнение с настоящим."),
    ],
    mistake="В `check` сравнивать с `self.value` — это звёздочки."),

f"{P}-m3-l2-e9": x(
    idea="Два альтернативных конструктора через `cls` и `staticmethod` для зажима значений.",
    lines=[
        ('code = code.lstrip("#")', "Убираем решётку."),
        ("return cls(int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16))", "Пары шестнадцатеричных цифр."),
        ("return max(0, min(255, x))", "Диапазон 0–255."),
    ],
    mistake="`int(code[0:2])` без основания 16 — `ff` не разберётся."),

f"{P}-m3-l2-e10": x(
    idea="Вычисляемые свойства не хранятся, а считаются из актуальных данных.",
    lines=[
        ('if value < 0:\n            raise ValueError("отрицательная ширина")', "Setter ширины."),
        ("return self.width * self.height", "`area`."),
        ("return self.width == self.height", "`is_square`."),
    ],
    mistake="Сохранить `area` в `__init__` — после изменения ширины станет устаревшим."),

# ===== dataclass =====

f"{P}-m3-l2-e2": x(
    idea="`@dataclass` по аннотациям полей сам пишет `__init__`, `__repr__` и `__eq__`.",
    lines=[
        ("y: int = 0", "Значение по умолчанию."),
        ("print(p == Point(3, 0))", "Сравнение по полям."),
    ],
    mistake="Ожидать `False` — `__eq__` сгенерирован."),

f"{P}-m3-l2-e5": x(
    idea="Поля — аннотациями, методы — как обычно.",
    lines=[
        ("duration: float = 0.0", "Поле с умолчанием — после обязательных."),
        ("""return f"{'✅' if self.passed else '❌'} {self.name}\"""", "Иконка по результату."),
    ],
    mistake="Поставить поле с умолчанием раньше обязательного — `TypeError`."),

f"{P}-dataclass-e1": x(
    idea="Изменяемое значение по умолчанию задают через `field(default_factory=list)` — у каждого объекта свой список.",
    lines=[
        ("items: list = field(default_factory=list)", "Новый список на каждый объект."),
        ('a.items.append("чай")', "У `b` пусто."),
    ],
    mistake="`items: list = []` — dataclass не даст так сделать (`ValueError`)."),

f"{P}-dataclass-e2": x(
    idea="`order=True` добавляет сравнение по полям в порядке объявления, `frozen=True` запрещает изменения и делает объект хешируемым.",
    lines=[
        ("print(sorted(vs)[0], max(vs))", "(0, 9) — минимум, (1, 10) — максимум."),
        ("vs[0].major = 2", "`FrozenInstanceError`."),
        ("print(len({Version(1, 0), Version(1, 0)}))", "Равные — одна запись."),
    ],
    mistake="Ожидать `Version(1, 2)` максимумом — 10 > 2."),

f"{P}-dataclass-e3": x(
    idea="`asdict` — объект в словарь, `replace` — копия с изменёнными полями.",
    lines=[
        ("u2 = replace(u, age=31)", "Исходный не меняется."),
        ("print(u == User(\"Аня\", 30), u == u2)", "Сравнение по полям."),
    ],
    mistake="Ожидать, что `u` стал 31."),

f"{P}-dataclass-e5": x(
    idea="`__post_init__` вызывается после сгенерированного `__init__` — место для проверок.",
    lines=[
        ('if self.start > self.stop:\n            raise ValueError("start > stop")', "Проверка после создания."),
        ("return self.stop - self.start", "Свойство `length`."),
    ],
    mistake="Писать свой `__init__` — dataclass его перезапишет или придётся дублировать поля."),

f"{P}-dataclass-e6": x(
    idea="Замороженный dataclass хешируемый — его можно класть в множество.",
    lines=[
        ("@dataclass(frozen=True)", "Неизменяемый и хешируемый."),
        ("return len(set(coords))", "Одинаковые координаты сольются."),
    ],
    mistake="Без `frozen` — `unhashable type`."),

f"{P}-dataclass-e7": x(
    idea="`order=True` сравнивает поля по порядку объявления: сначала `priority`, потом `title`.",
    lines=[
        ("priority: int\n    title: str", "Порядок полей важен."),
        ("return [t.title for t in sorted(tasks)]", "Без `key=`."),
    ],
    mistake="Объявить `title` первым — сортировка пойдёт по алфавиту."),

f"{P}-dataclass-e8": x(
    idea="Из словаря берём только нужные поля, обратно — `asdict`.",
    lines=[
        ('return [User(d["name"], d["age"]) for d in data]', "Лишние ключи игнорируются."),
        ("return [asdict(u) for u in users]", "Обратно в словари."),
    ],
    mistake="`User(**d)` — упадёт на лишних ключах."),

# ===== Практика: классы в автотестах =====

f"{P}-pom-e1": x(
    idea="Page Object: селекторы и действия страницы собраны в классе, тест вызывает понятный метод `login`. Драйвер можно подменить фейком.",
    lines=[
        ('LOGIN = "#login"', "Селекторы — в одном месте."),
        ("self.driver.type(self.LOGIN, user)", "Действия через драйвер."),
    ],
    mistake="Писать селекторы прямо в тестах — при изменении вёрстки придётся править все тесты."),

f"{P}-pom-e2": x(
    idea="API-клиент прячет склейку адресов и заголовки авторизации.",
    lines=[
        ('self.base_url = base_url.rstrip("/")', "Без слэша в конце."),
        ("""return f"{self.base_url}/{path.lstrip('/')}\"""", "Ровно один слэш."),
        ("if self.token:", "Токена нет — без Authorization."),
    ],
    mistake="Склеивать как есть — получится `//users`."),

f"{P}-pom-e3": x(
    idea="Наследники базовой страницы меняют только `url`, а при необходимости дополняют поведение через `super()`.",
    lines=[
        ('url = "/cart"', "Своё значение атрибута класса."),
        ('return super().open() + " (нужен вход)"', "Дополнение."),
    ],
    mistake="Ожидать `/` у CartPage."),

f"{P}-pom-e4": x(
    idea="Методы Page Object возвращают `self`, чтобы шаги можно было цеплять.",
    lines=[
        ("self.driver.type(self.INPUT, text)\n        self.driver.click(self.BUTTON)\n        return self", "Ввод, клик, объект для цепочки."),
        ('return self.driver.find_all(".result")', "Результаты."),
    ],
    mistake="Использовать `INPUT` без `self.` внутри метода — `NameError`."),

f"{P}-pom-e5": x(
    idea="Клиент получает сессию снаружи — в тестах её легко заменить фейком.",
    lines=[
        ('return self.session.request("GET", self.base_url + path)', "Полный адрес."),
        ('return self.session.request("POST", self.base_url + path, json=data)', "Тело — по имени."),
        ('return self.get(f"/users/{user_id}")', "Удобный метод поверх `get`."),
    ],
    mistake="Создавать сессию внутри клиента — подменить не выйдет."),

f"{P}-pom-e6": x(
    idea="Фабрика тестовых данных: счётчик у каждого объекта фабрики свой, поля можно переопределить.",
    lines=[
        ("self.counter += 1", "Следующий номер."),
        ("user.update(overrides)", "Переопределения важнее."),
        ("return [self.create() for _ in range(n)]", "Пачка пользователей."),
    ],
    mistake="Счётчик атрибутом класса — фабрики будут делить номера."),

f"{P}-pom-e7": x(
    idea="Методы проверок возвращают `self` — `response.assert_status(200).assert_has(\"id\")` читается как фраза.",
    lines=[
        ("return 200 <= self.status < 300", "`ok` — свойство."),
        ('raise AssertionError(f"ожидали {expected}, получили {self.status}")', "Понятное сообщение."),
        ("return self", "Для цепочек."),
    ],
    mistake="Возвращать `True` из проверок — цепочка сломается."),

f"{P}-pom-e8": x(
    idea="Фейковый API на словаре: быстро, предсказуемо, без сети.",
    lines=[
        ('if not name:\n            raise ValueError("пустое имя")', "Проверка."),
        ("self.users[self.next_id] = user\n        self.next_id += 1", "Хранение и следующий id."),
        ("return self.users.pop(user_id, None) is not None", "Удалили — `True`."),
    ],
    mistake="Использовать `len(self.users) + 1` как id — после удаления id повторятся."),
}
