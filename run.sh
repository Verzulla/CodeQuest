#!/usr/bin/env bash
# Запуск CodeQuest: создаёт окружение при первом запуске и открывает http://127.0.0.1:8765
set -e
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi
echo "🦉 CodeQuest: http://127.0.0.1:${PORT:-8765}"
# Локальный запуск для себя: код выполняется без контейнера. На сервере в интернете
# запускай с CODEQUEST_SANDBOX=docker (это значение по умолчанию вне run.sh).
export CODEQUEST_SANDBOX="${CODEQUEST_SANDBOX:-local}"
exec .venv/bin/python -m app
