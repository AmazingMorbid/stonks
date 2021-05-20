#!/bin/bash

cd stonks-watcher || (echo "Could not cd into stonks-watcher" && exit 1)


watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A celeryapp beat -l info
