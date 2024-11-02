#!/bin/bash
#
# Runs an upgrade on the database using migrations and starts the gunicorn server.

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 seconds...
    sleep 5
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - tools:app
