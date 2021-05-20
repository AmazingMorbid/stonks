#!/bin/bash

cd stonks-watcher || (echo "Could not cd into stonks-watcher" && exit 1)

celery -A celeryapp beat -l info
