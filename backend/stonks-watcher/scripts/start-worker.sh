#!/bin/bash

# --uid is set to the celery user defined in Dockerfile
# that way it will run without root privileges
celery -A celeryapp worker -l info --uid $(id -u celery)
