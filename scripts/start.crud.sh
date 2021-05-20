#!/bin/bash

cd stonks-worker || (echo "Could not cd into stonks-worker" && exit 1)

celery -A celeryapp beat -l info
