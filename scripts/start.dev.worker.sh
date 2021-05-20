#!/bin/bash

cd stonks-watcher || (echo "Could not cd into stonks-watcher" && exit 1)

# --uid is set to the celery user defined in Dockerfile
# that way it will run without root privileges
watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A celeryapp worker -l info --uid $(id -u celery)
