#!/usr/bin/env bash 
find . -name "*.py" -not -path "./alembic/*" | xargs wc -l | sort -n
