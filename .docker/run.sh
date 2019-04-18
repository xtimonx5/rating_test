#!/usr/bin/env bash

python /opt/django/wait_for_psql.py
gosu root /usr/sbin/cron start;

if [ $DEBUG = "true" ]; then
    gosu root /usr/sbin/sshd -D
else
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000
fi
