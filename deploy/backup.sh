#!/usr/bin/env bash
# Ежедневный бэкап базы CodeQuest (ставится в /etc/cron.daily). Копия консистентна и при работающем сервере.
set -euo pipefail
DIR=/var/backups/codequest
mkdir -p "$DIR"
sqlite3 /opt/codequest/data/codequest.db ".backup '$DIR/codequest-$(date +%F).db'"
gzip -f "$DIR/codequest-$(date +%F).db"
find "$DIR" -name 'codequest-*.db.gz' -mtime +14 -delete
