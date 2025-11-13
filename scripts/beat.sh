#!/bin/bash
# This script starts the Celery beat scheduler

celery -A app.tasks.celery_app.celery beat --loglevel=info
