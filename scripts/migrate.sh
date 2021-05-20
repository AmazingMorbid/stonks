#!/bin/bash

alembic upgrade head || echo "Migrations failed" | exit 1
