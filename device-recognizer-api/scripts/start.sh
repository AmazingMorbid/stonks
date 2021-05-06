#!/bin/bash
echo "Starting production server on port 8010"
uvicorn main:app --host 0.0.0.0 --port=8010 --log-level=info
