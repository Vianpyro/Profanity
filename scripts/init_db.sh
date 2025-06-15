#!/bin/sh
mkdir -p database
if ls database/*.sql 1> /dev/null 2>&1; then
  cat database/*.sql | sqlite3 database/profanities.db
fi
exec gunicorn --chdir api app:app --bind 0.0.0.0
