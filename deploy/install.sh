#!/usr/bin/env bash
# Установка CodeQuest на чистый сервер Ubuntu 24.04. Запускать от root:
#
#   curl -fsSL https://raw.githubusercontent.com/Verzulla/CodeQuest/main/deploy/install.sh -o install.sh
#   DOMAIN=example.ru bash install.sh
#
# Что делает: ставит Docker, Python, Caddy (HTTPS-сертификат получает сам), создаёт
# пользователя codequest, скачивает код в /opt/codequest, проверяет песочницу, включает
# автозапуск, файрвол и ежедневный бэкап базы. Повторный запуск безопасен.
set -euo pipefail

DOMAIN="${DOMAIN:?Укажи домен: DOMAIN=example.ru bash install.sh}"
REPO="${REPO:-https://github.com/Verzulla/CodeQuest.git}"
APP=/opt/codequest
say() { printf '\n\033[1;32m==> %s\033[0m\n' "$*"; }

[ "$(id -u)" -eq 0 ] || { echo "Запусти от root (sudo -i)"; exit 1; }
. /etc/os-release
[ "$ID" = ubuntu ] || echo "Внимание: скрипт проверен на Ubuntu 24.04, у тебя $PRETTY_NAME"

say "Обновляю систему и ставлю пакеты"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get upgrade -yq
apt-get install -yq git python3 python3-venv sqlite3 docker.io caddy ufw unattended-upgrades

# Меньше 2 ГБ памяти — добавим подкачку, чтобы сервер не падал под нагрузкой.
MEM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
if [ "$MEM_MB" -lt 1900 ] && ! swapon --show | grep -q /swapfile; then
  say "Памяти ${MEM_MB} МБ — создаю swap 2 ГБ"
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  grep -q /swapfile /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi
MAX_RUNS=$([ "$MEM_MB" -lt 1900 ] && echo 2 || echo 4)

say "Настраиваю Docker"
# Docker Hub из России работает нестабильно — берём официальные образы через зеркало Google.
if [ ! -f /etc/docker/daemon.json ]; then
  printf '{\n  "registry-mirrors": ["https://mirror.gcr.io"]\n}\n' > /etc/docker/daemon.json
fi
systemctl enable --now docker
systemctl restart docker

say "Пользователь и код"
id codequest >/dev/null 2>&1 || useradd --system --create-home --home-dir /home/codequest --shell /usr/sbin/nologin codequest
usermod -aG docker codequest
if [ -d "$APP/.git" ]; then
  sudo -u codequest git -C "$APP" pull --ff-only
else
  install -d -o codequest -g codequest "$APP"
  sudo -u codequest git clone "$REPO" "$APP"
fi
sudo -u codequest python3 -m venv "$APP/.venv"
sudo -u codequest "$APP/.venv/bin/pip" install -q --upgrade pip
sudo -u codequest "$APP/.venv/bin/pip" install -q -r "$APP/requirements.txt"
install -d -o codequest -g codequest "$APP/data"

say "Проверяю песочницу для кода учеников"
sudo -u codequest -H bash -c "cd $APP && .venv/bin/python -m app.cli sandbox-check"

say "Автозапуск (systemd)"
sed "s/__MAX_RUNS__/$MAX_RUNS/" "$APP/deploy/codequest.service" > /etc/systemd/system/codequest.service
systemctl daemon-reload
systemctl enable codequest
systemctl restart codequest

say "HTTPS (Caddy) для $DOMAIN"
sed "s/__DOMAIN__/$DOMAIN/g" "$APP/deploy/Caddyfile" > /etc/caddy/Caddyfile
systemctl enable caddy
systemctl reload caddy || systemctl restart caddy

say "Файрвол: открыты только SSH, HTTP и HTTPS"
ufw allow OpenSSH >/dev/null
ufw allow 80/tcp >/dev/null
ufw allow 443 >/dev/null
ufw --force enable >/dev/null

say "Ежедневный бэкап базы (/var/backups/codequest, хранится 14 дней)"
install -m 755 "$APP/deploy/backup.sh" /etc/cron.daily/codequest-backup

say "Готово"
sleep 2
systemctl --no-pager --lines=0 status codequest | head -3
cat <<MSG

  Сайт: https://$DOMAIN  (сертификат выпускается в первые минуты — если не открылось, подожди)
  Первым зарегистрируйся сам — первый аккаунт становится администратором.

  Логи:        journalctl -u codequest -f
  Обновление:  bash $APP/deploy/update.sh
MSG
