"""Теория модуля «Ветки и командная работа» темы «Git».

full — полный урок (основной экран), short — шпаргалка."""
from ._lib import q, t

T = {

# ---------- git-branch ----------
'git-branch': dict(
    full=t(r'''
## Зачем это нужно

**Ветка** позволяет работать над задачей отдельно, не ломая основной код. Разработчик делает фичу в `feature/cart`, тестировщик пишет тесты в `test/cart-e2e`, а `main` остаётся стабильной. Когда работа готова и проверена, ветку вливают обратно.

## Как устроены ветки

- Ветка — просто подвижный указатель на последний коммит своей линии.
- `HEAD` — указатель на ветку, на которой ты сейчас.
- Новая ветка начинается с текущего коммита; дальше её коммиты не влияют на другие ветки.

```viz
{"type": "git", "title": "Ветки — подвижные указатели. Нажимай «Шаг»", "intro": "Кружки — коммиты, ярлыки — ветки. Зелёный ярлык `HEAD → …` — ветка, на которой ты сейчас.", "steps": [{"cmd": "git commit -m 'login page'", "note": "Новый коммит `C2`. Ветка `main` передвинулась на него."}, {"cmd": "git switch -c feature", "note": "Новая ветка `feature` указывает на тот же коммит, и HEAD теперь на ней. Коммитов не прибавилось."}, {"cmd": "git commit -m 'login tests'", "note": "Коммит идёт в `feature`. Ярлык `main` остался на месте."}, {"cmd": "git commit -m 'more tests'"}, {"cmd": "git switch main", "note": "Вернулись на `main`: файлы стали такими, как в `C2`."}, {"cmd": "git commit -m 'hotfix'", "note": "Ветки разошлись: у каждой свои коммиты после `C2`."}], "sandbox": true}
```

## Команды

```bash
$ git branch
  main
* bugfix/timeout
  feature/cart
$ git switch -c feature/login-tests
$ git switch main
$ git branch -a
$ git branch -m feature/cart-tests
$ git branch -d feature/old
```

Что делает каждая команда:

- `git branch` — список локальных веток, `*` — текущая.
- `git switch -c имя` — **создать** ветку и перейти на неё. Старый вариант — `git checkout -b имя`.
- `git switch имя` (или `git checkout имя`) — перейти на существующую ветку. Незакоммиченные изменения переходят вместе с тобой — если они мешают, git откажет.
- `git branch -a` — все ветки, включая удалённые (`remotes/origin/...`).
- `git branch -m новое` — переименовать текущую ветку.
- `git branch -d имя` — удалить ветку, уже слитую в текущую. `-D` — удалить принудительно (несохранённая работа пропадёт).

## Именование веток

- Договорённость команды обычно такая: `тип/описание`: `feature/cart`, `bugfix/login-500`, `test/cart-e2e`, `hotfix/pay`.
- Строчные латинские буквы, цифры и дефисы, без пробелов. Часто в имя добавляют номер задачи: `test/QA-123-cart`.

## Итог

- Ветка — независимая линия коммитов; `HEAD` — где ты.
- `git switch -c` — создать и перейти, `git switch` — перейти.
- `git branch` (`-a`, `-m`, `-d`) — список, переименование, удаление.
- Имена: `тип/описание-через-дефисы`.
'''),
    short=t(r'''
```bash
git branch                 # список, * — текущая
git switch -c test/cart    # создать и перейти (checkout -b)
git switch main            # перейти (checkout main)
git branch -a              # вместе с удалёнными
git branch -m new-name     # переименовать текущую
git branch -d old          # удалить слитую (-D — принудительно)
```
'''),
    quiz=[
        q('Что делает `git switch -c test/cart`?',
            ['Удаляет ветку', 'Создаёт ветку и переключается на неё', 'Переименовывает ветку', 'Вливает ветку'],
            1, 'То же, что git checkout -b.'),
        q('Как в выводе `git branch` отмечена текущая ветка?',
            ['Жирным', 'Звёздочкой *', 'Стрелкой', 'Никак'],
            1, '* перед именем.'),
        q('Чем `git branch -D` отличается от `-d`?',
            ['Ничем', 'Удаляет даже неслитую ветку', 'Удаляет на сервере', 'Переименовывает'],
            1, 'Можно потерять работу.'),
    ],
),

# ---------- git-merge ----------
'git-merge': dict(
    full=t(r'''
## Зачем это нужно

Ветки создают, чтобы потом **соединить**: влить фичу в `main`, забрать свежий `main` в свою ветку. Обычно git делает это сам. Но если два человека изменили одни и те же строки, возникает **конфликт**, и решать его придётся тебе.

## git merge

```bash
$ git switch main
$ git merge feature/cart
Updating 1a2b3c4..9f8e7d6
Fast-forward
```

- `git merge ветка` — влить указанную ветку в **текущую**.
- **Fast-forward** — в `main` новых коммитов не было, git просто передвинул указатель.
- Если изменения были в обеих ветках, git создаст **коммит слияния** (merge commit).

```viz
{"type": "git", "title": "Fast-forward и коммит слияния", "steps": [{"cmd": "git switch -c feature", "note": "Отвели ветку."}, {"cmd": "git commit -m 'cart tests'"}, {"cmd": "git switch main"}, {"cmd": "git merge feature", "note": "В `main` новых коммитов не было — **fast-forward**: указатель `main` просто передвинулся."}, {"cmd": "git switch -c bugfix"}, {"cmd": "git commit -m 'fix timeout'"}, {"cmd": "git switch main"}, {"cmd": "git commit -m 'new page'", "note": "Теперь изменения есть в обеих ветках."}, {"cmd": "git merge bugfix", "note": "Git создал **коммит слияния** с двумя родителями (фиолетовый)."}], "sandbox": true}
```

## Конфликт

```bash
$ git merge feature/cart
Auto-merging tests/conftest.py
CONFLICT (content): Merge conflict in tests/conftest.py
Automatic merge failed; fix conflicts and then commit the result.
```

В файле появятся маркеры:

```bash
<<<<<<< HEAD
TIMEOUT = 10
=======
TIMEOUT = 30
>>>>>>> feature/cart
```

- Между `<<<<<<< HEAD` и `=======` — версия **текущей** ветки.
- Между `=======` и `>>>>>>> feature/cart` — версия **вливаемой**.
- Нужно оставить правильный вариант (или объединить оба) и **удалить все маркеры**.

## Как разрешить

```bash
$ git status
$ git diff --name-only --diff-filter=U
$ git add tests/conftest.py
$ git commit
$ git merge --abort
```

По шагам:

1. `git status` показывает файлы в конфликте (both modified). `--diff-filter=U` — только их список.
2. Открыть каждый файл, выбрать нужные строки, удалить маркеры.
3. `git add файл` — отметить конфликт как разрешённый.
4. `git commit` — завершить слияние (сообщение git подставит сам).
5. Если запутался — `git merge --abort` вернёт всё как было до слияния.

Редакторы (VS Code, PyCharm) показывают конфликты с кнопками «принять текущее / входящее / оба».

## Итог

- `git merge ветка` — влить в текущую; fast-forward или merge commit.
- Конфликт: `<<<<<<< HEAD` — наше, `>>>>>>>` — вливаемое; маркеры удалить.
- Разрешение: исправить → `git add` → `git commit`.
- `git merge --abort` — отменить слияние.
'''),
    short=t(r'''
```bash
git merge feature/cart          # влить в текущую
# <<<<<<< HEAD  … наше  ======= … их  >>>>>>> branch
git diff --name-only --diff-filter=U   # файлы в конфликте
git add file && git commit      # конфликт разрешён
git merge --abort               # отменить слияние
```
'''),
    quiz=[
        q('В какую ветку вливает `git merge feature/cart`?',
            ['В feature/cart', 'В текущую ветку', 'В main всегда', 'В origin'],
            1, 'Сначала переключись на ветку-получатель.'),
        q('Что находится между `<<<<<<< HEAD` и `=======`?',
            ['Вливаемая версия', 'Версия текущей ветки', 'Общий предок', 'Комментарий'],
            1, 'После ======= — вливаемая.'),
        q('Как отметить, что конфликт в файле разрешён?',
            ['git resolve', 'git add файл', 'git merge --done', 'git push'],
            1, 'Затем git commit.'),
    ],
),

# ---------- git-remote ----------
'git-remote': dict(
    full=t(r'''
## Зачем это нужно

Твой репозиторий на компьютере и репозиторий на GitHub/GitLab — две копии. Изменения между ними не синхронизируются сами: свои коммиты нужно **отправить** (`push`), чужие — **забрать** (`pull`/`fetch`). CI запускает тесты именно на коммитах с сервера.

## Удалённые репозитории

```bash
$ git remote -v
origin  git@github.com:acme/api-tests.git (fetch)
origin  git@github.com:acme/api-tests.git (push)
```

- `origin` — стандартное имя удалённого репозитория после `git clone`.
- Адрес бывает HTTPS (`https://github.com/...`) или SSH (`git@github.com:...`) — для SSH нужен настроенный ключ.

## push: отправить

```bash
$ git push -u origin feature/login-tests
$ git push
```

- Первый раз для новой ветки: `-u` (`--set-upstream`) связывает локальную ветку с удалённой. Потом достаточно `git push`.
- Если на сервере есть коммиты, которых у тебя нет, push будет отклонён — сначала забери их.

## fetch и pull: забрать

```bash
$ git fetch
$ git status
Your branch is behind 'origin/main' by 3 commits, and can be fast-forwarded.
$ git pull
$ git pull --rebase
```

- `git fetch` — только **скачать** информацию о новых коммитах и ветках, ничего не меняя в твоих ветках. Безопасно всегда.
- После fetch `git status` покажет, насколько ты отстаёшь (behind) или опережаешь (ahead).
- `git pull` = `fetch` + `merge`: скачать и влить в текущую ветку.
- `git pull --rebase` = `fetch` + `rebase`: твои локальные коммиты встанут поверх свежих, без лишнего коммита слияния. Многие команды используют именно его.

## Ветка коллеги

```bash
$ git fetch
$ git switch feature/payment
```

- Если ветка есть на `origin`, а локально нет, `git switch имя` создаст локальную ветку, связанную с удалённой.

## Итог

- `git remote -v` — куда отправляем; `origin` — сервер.
- `git push -u origin ветка` — первый раз, дальше `git push`.
- `git fetch` — узнать новое, `git pull` — забрать и влить, `--rebase` — без коммита слияния.
- behind — отстаёшь, ahead — опережаешь.
'''),
    short=t(r'''
```bash
git remote -v                     # удалённые репозитории
git push -u origin my-branch      # первый push ветки
git push                          # дальше
git fetch                         # скачать, ничего не вливая
git pull                          # fetch + merge
git pull --rebase                 # fetch + rebase
git switch feature/x              # ветка коллеги после fetch
```
'''),
    quiz=[
        q('Чем `git fetch` отличается от `git pull`?',
            ['Ничем', 'fetch только скачивает, pull ещё и вливает', 'fetch отправляет', 'pull только скачивает'],
            1, 'fetch безопасен всегда.'),
        q('Зачем флаг `-u` в `git push -u origin ветка`?',
            ['Удалить ветку', 'Связать локальную ветку с удалённой', 'Обновить', 'Отправить теги'],
            1, 'Дальше хватит git push.'),
        q('Что значит «Your branch is behind by 3 commits»?',
            ['У тебя 3 лишних коммита', 'На сервере 3 коммита, которых у тебя нет', 'Конфликт', 'Ветка удалена'],
            1, 'Нужно git pull.'),
    ],
),

# ---------- git-pr ----------
'git-pr': dict(
    full=t(r'''
## Зачем это нужно

В командах не пушат напрямую в `main`. Изменения предлагают через **pull request** (PR; в GitLab — merge request, MR): коллеги смотрят код, CI прогоняет тесты, и только потом ветку вливают. Тестировщик участвует дважды: присылает свои PR с тестами и проверяет PR разработчиков — локально запускает их ветку.

## Цикл работы над задачей

```bash
$ git switch main
$ git pull
$ git switch -c test/cart-e2e
$ git add . && git commit -m "test: add cart e2e"
$ git push -u origin test/cart-e2e
```

По шагам:

1. Обновить `main`, чтобы начать от свежей версии.
2. Создать ветку под задачу.
3. Писать тесты, делать осмысленные коммиты. `&&` — выполнить вторую команду, только если первая прошла успешно.
4. Отправить ветку и открыть PR на GitHub/GitLab (ссылку на создание git печатает прямо после push).

## GitHub CLI

```bash
$ gh pr create --fill
$ gh pr list
$ gh pr checkout 42
$ gh pr view 42 --web
```

- `gh` — официальная утилита GitHub для терминала.
- `gh pr create` — создать PR из текущей ветки (`--fill` — заголовок и описание из коммитов).
- `gh pr checkout 42` — скачать ветку PR №42 и переключиться на неё — так тестировщик проверяет чужую задачу локально.

## Ревью и исправления

```bash
$ git add . && git commit -m "fix: review comments" && git push
```

- Ревьюер оставляет комментарии. Ты исправляешь в той же ветке и пушишь — PR обновится сам.
- Хороший PR: понятный заголовок (часто в формате Conventional Commits), описание «что и зачем», ссылка на задачу, небольшой размер, зелёный CI.

## Что проверяет тестировщик в чужом PR

- Ветка запускается, тесты проходят локально и в CI.
- Новая функциональность покрыта тестами; изменённый код без тестов — повод спросить.
- Ручная проверка сценариев из задачи на стенде или локально.

## Итог

- Работа идёт через ветки и PR, а не прямой push в `main`.
- Цикл: `pull` → `switch -c` → коммиты → `push -u` → PR → ревью → merge.
- `gh pr create`, `gh pr checkout N` — GitHub CLI.
- Исправления после ревью — новыми коммитами в ту же ветку.
'''),
    short=t(r'''
```bash
git switch main && git pull
git switch -c test/cart-e2e
git add . && git commit -m "test: add cart e2e"
git push -u origin test/cart-e2e     # → открыть PR
gh pr create --fill                  # или через GitHub CLI
gh pr checkout 42                    # проверить чужой PR
git commit -am "fix: review" && git push   # правки после ревью
```
'''),
    quiz=[
        q('Что такое pull request?',
            ['Команда git pull', 'Предложение влить ветку, с ревью и проверкой CI', 'Скачивание репозитория', 'Удаление ветки'],
            1, 'В GitLab — merge request.'),
        q('Как тестировщику проверить PR №42 локально через GitHub CLI?',
            ['gh pr view 42', 'gh pr checkout 42', 'git pull 42', 'git merge 42'],
            1, 'Скачает ветку и переключит на неё.'),
        q('Как внести исправления после ревью?',
            ['Создать новый PR', 'Закоммитить в ту же ветку и сделать push', 'Удалить ветку', 'Переписать main'],
            1, 'PR обновится автоматически.'),
    ],
),

}
