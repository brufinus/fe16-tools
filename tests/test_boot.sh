#!/bin/bash
#
# Runs the database migration, starts the Gunicorn server in the background, then tests server startup.

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 seconds...
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - tools:app &
GUNICORN_PID=$!

sleep 2

for i in {1..5}; do
  if curl --silent --fail "http://localhost:5000" > /dev/null; then
    echo "Gunicorn server is running!"
    kill $GUNICORN_PID
    exit 0
  else
    echo "Gunicorn server is not running..."
  fi
  sleep 5
done

echo "Failed server startup check."
kill $GUNICORN_PID
exit 1
