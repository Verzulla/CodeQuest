# Выкладка CodeQuest на сервер

Нужен VPS с **Ubuntu 24.04** (от 1 ГБ RAM, лучше 2 ГБ) и домен.

## 1. Домен → сервер

В панели, где куплен домен, открой DNS и добавь две A-записи с IP сервера:

| Имя | Тип | Значение |
|---|---|---|
| `@` | A | IP сервера |
| `www` | A | IP сервера |

Обновление DNS занимает от нескольких минут до пары часов.

## 2. Установка

Подключись к серверу (IP и пароль root приходят от хостера на почту):

```bash
ssh root@IP_СЕРВЕРА
```

На сервере (вместо `example.ru` — твой домен):

```bash
curl -fsSL https://raw.githubusercontent.com/Verzulla/CodeQuest/main/deploy/install.sh -o install.sh
DOMAIN=example.ru bash install.sh
```

Скрипт ставит Docker, Python и Caddy, скачивает код в `/opt/codequest`, проверяет песочницу,
включает автозапуск, HTTPS, файрвол и ежедневный бэкап. Повторный запуск безопасен.

## 3. Перенос прогресса с компьютера (необязательно)

На своём компьютере, в папке проекта:

```bash
sqlite3 data/codequest.db ".backup data/upload.db"
scp data/upload.db root@IP_СЕРВЕРА:/tmp/codequest.db
```

На сервере:

```bash
systemctl stop codequest && install -o codequest -g codequest -m 644 /tmp/codequest.db /opt/codequest/data/codequest.db && rm -f /opt/codequest/data/codequest.db-wal /opt/codequest/data/codequest.db-shm && systemctl start codequest
```

Если база ещё из версии без аккаунтов, её прогресс получит первый зарегистрированный пользователь.

## 4. Первый вход

Открой `https://твой-домен` и **зарегистрируйся первым** — первый аккаунт становится администратором.
Других администраторов он назначает в «Настройках» → «🛡️ Администраторы».
На телефоне: Chrome → ⋮ → «Установить приложение», Safari → «Поделиться» → «На экран „Домой“».

## Дальше

| Задача | Команда (на сервере, от root) |
|---|---|
| Обновить до последней версии из GitHub | `bash /opt/codequest/deploy/update.sh` (бэкап → код → зависимости → образ песочницы → темы → перезапуск; дождись строки «Обновлено: …», синхронизация тем идёт несколько минут) |
| Логи | `journalctl -u codequest -f` |
| Перезапуск | `systemctl restart codequest` |
| Аккаунты | `sudo -u codequest -H bash -c "cd /opt/codequest && .venv/bin/python -m app.cli users"` |
| Бэкапы | `/var/backups/codequest/` (14 дней) |
