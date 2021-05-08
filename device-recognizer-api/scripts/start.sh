#!/bin/bash
echo "Starting production server on port 80"
uvicorn main:app --host 0.0.0.0 --port=80 --log-level=info
