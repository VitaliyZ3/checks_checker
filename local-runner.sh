#!/bin/sh
set -x

gunicorn src.main:app --bind "0.0.0.0:8000" -w 1 --threads 2 --workers 2 --worker-class uvicorn.workers.UvicornWorker --timeout=600