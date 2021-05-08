#!/bin/bash

echo "Applying environment"
printenv >> /etc/environment

echo "Starting cron"
cron -f
