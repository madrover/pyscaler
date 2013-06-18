#!/bin/sh

cd /opt/django/pyscaler

ps -ef | grep manage.py | grep celery | awk '{print $2}' | xargs kill -9
python manage.py celery flower &


while getopts ":d" opt; do
  case $opt in
    d)
      python manage.py celery worker --concurrency=10 -E -B --loglevel=debug
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
python manage.py celery worker --concurrency=10 -E -B --loglevel=info
