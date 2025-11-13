#!/bin/bash
# This script starts the Celery worker

celery -A app.tasks.celery_app.celery worker --loglevel=info
