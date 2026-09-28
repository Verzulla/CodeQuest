#!/usr/bin/env bash
# Обновить CodeQuest до последней версии из GitHub. Запускать от root:  bash /opt/codequest/deploy/update.sh
set -euo pipefail
APP=/opt/codequest
/etc/cron.daily/codequest-backup                         # на всякий случай — свежий бэкап
sudo -u codequest git -C "$APP" pull --ff-only
sudo -u codequest "$APP/.venv/bin/pip" install -q -r "$APP/requirements.txt"
sudo -u codequest -H bash -c "cd $APP && .venv/bin/python -m app.cli sandbox-check"   # образ песочницы (пересоберётся, если изменился)
sudo -u codequest -H bash -c "cd $APP && .venv/bin/python -m app.cli sync"   # новый контент из content/
systemctl restart codequest
echo "Обновлено: $(sudo -u codequest git -C "$APP" log -1 --format='%h %s')"
