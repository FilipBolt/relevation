#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn relevation.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1
