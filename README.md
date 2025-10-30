# Flask Car Report


## Overview
- Flask REST API to manage/search car reports.
- JWT-based authentication.
- Periodic background sync from Back4App (2012-2022) using Celery + Redis.

## Code structure

├── app
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── models.cpython-312.pyc
│   │   ├── routes.cpython-312.pyc
│   │   ├── schemas.cpython-312.pyc
│   │   └── tasks.cpython-312.pyc
│   ├── routes
│   │   ├── auth_routes.py
│   │   ├── car_routes.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── auth_routes.cpython-312.pyc
│   │       ├── car_routes.cpython-312.pyc
│   │       └── __init__.cpython-312.pyc
│   ├── schemas.py
│   └── tasks.py
├── app.db
├── config.py
├── flask car commands .txt
├── __pycache__
│   ├── config.cpython-312.pyc
│   └── worker.cpython-312.pyc
├── README.md
├── requirements.txt
├── run.py
└── worker.py

6 directories, 24 files
(.venv) asma@asma-HP-ZBook-Fury-15-G7-Mobile-Workstation:~/Documents/projects/car_report$ 

## How to run
1. Copy .env.example -> .env and update as needed.
2. Start Redis.
3. Activate venv, install requirements.
4. Run Flask: `python run.py`
5. Start Celery worker : `celery -A worker.celery worker --beat --loglevel=info`
