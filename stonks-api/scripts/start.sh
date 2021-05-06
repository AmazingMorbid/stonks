#!/bin/bash

"$(dirname "$0")/prestart.sh" || exit

echo "Starting production server on port 8000"
uvicorn main:app --host 0.0.0.0 --port=8000 --log-level=info
