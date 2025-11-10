# Flask Car Report


## Overview
- Flask REST API to manage/search car reports.
- JWT-based authentication.
- Periodic background sync from Back4App (2012-2022) using Celery + Redis.

## Code structure
asma@asma-HP-ZBook-Fury-15-G7-Mobile-Workstation:~/Documents/projects$ tree -L 4
.
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── car.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── car.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── models.cpython-312.pyc
│   │   │   └── user.cpython-312.pyc
│   │   └── user.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── models.cpython-312.pyc
│   │   ├── routes.cpython-312.pyc
│   │   ├── schemas.cpython-312.pyc
│   │   └── tasks.cpython-312.pyc
│   ├── tasks
│   │   ├── celery_app.py
│   │   ├── fetch_and_store_cars_task.py
│   │   └── __pycache__
│   │       ├── celery_app.cpython-312.pyc
│   │       ├── fetch_and_store_cars.cpython-312.pyc
│   │       ├── fetch_and_store_cars_task.cpython-312.pyc
│   │       ├── tasks.cpython-312.pyc
│   │       └── worker.cpython-312.pyc
│   └── web
│       ├── cars
│       │   ├── api.py
│       │   ├── __pycache__
│       │   └── schemas.py
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── auth_routes.cpython-312.pyc
│       │   ├── car_routes.cpython-312.pyc
│       │   └── __init__.cpython-312.pyc
│       └── users
│           ├── api.py
│           ├── __pycache__
│           └── schemas.py
├── app.db
├── app.py
├── config.py
├── flask car commands .txt
├── instance
├── __pycache__
│   ├── config.cpython-312.pyc
│   └── worker.cpython-312.pyc
├── README.md
└── requirements.txt

15 directories, 36 files

## How to run
1. Copy .env.example -> .env and update as needed.
2. Start Redis.
3. Activate venv, install requirements.
4. Run Flask: `python run.py`
5. **Start Celery worker**  
   ```bash
   celery -A worker.celery worker --beat --loglevel=info

## Docker Setup for Car Report Project
1. Install docker desktop 
2. Create dockerfile using python 3.12 slim as base image , copy requirements and install dependencies 
3. For creating multi-container application , use docker compose and defien services, images and containers 
4. Services=3
    1. API – Flask application running on port 5000, uses image car-report-app
    2. Celery – Background worker for asynchronous tasks., uses same image
    3. Redis – In-memory data store used by Celery as a broker and result backend, uses official builtin redis image
### Docker Commands

1. **Build and start containers**  
   ```bash
   docker compose up --build

2. **Check if containers are running**  
   ```bash
   docker ps
3. **Stop and remove containers**  
   ```bash
   docker compose down


