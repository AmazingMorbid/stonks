#!/bin/bash

# run this inside backend directory

cd stonks-api || (echo "Could not cd into stonks-api" && exit 1)

/app/scripts/migrate.sh

./scripts/start.sh
