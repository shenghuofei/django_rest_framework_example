#!/usr/bin/env bash

set -e

# cd /your/project/path

export DJANGO_SETTINGS_MODULE=restpro.settings

if [ ! -d './logs' ] ; then
    mkdir logs
fi

celery worker -A restpro -Q default,custom -n worker01@%h --concurrency 4 \
    --max-tasks-per-child 10000 \
    --loglevel=DEBUG \
    --workdir=./ \
    --pidfile=./logs/celery.%n.pid \
    --logfile=./logs/%n%I.log \
    >> ./logs/celery01.log 2>&1 &

# for celery default scheduler
# Beat needs to store the last run times of the tasks in a local database file (named celerybeat-schedule by default), so it needs access to write in the current directory, or alternatively you can specify a custom location for this file
# celery -A restpro beat -l info \
#    -s ./logs/celerybeat-schedule \
#    --pidfile=./logs/celerybeat.pid \
#    >> ./logs/celery01-beat.log 2>&1 &

# for redbeat scheduler
celery -A restpro beat -l DEBUG -S redbeat.RedBeatScheduler --pidfile=./logs/celerybeat.pid \
    >> ./logs/celery01-beat.log 2>&1 &

