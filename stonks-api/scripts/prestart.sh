#!/bin/bash
echo "Waiting 10 sec for database to turn on"
sleep 10
echo "Running migrations"
alembic upgrade head || echo "Migrations failed" | exit 1
