# Flask Car Report

## Overview

* Flask REST API to manage/search car reports.
* JWT-based authentication.
* Periodic background sync from Back4App (2012–2022) using Celery + Redis.

## Code Structure

```
.
├── alembic.ini
├── app
│   ├── auth
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   ├── password.py
│   │   └── __pycache__
│   ├── db.py
│   ├── __init__.py
│   ├── llm
│   │   ├── agent.py
│   │   ├── agent_tools.py
│   │   ├── anthropic_client.py
│   │   └── __pycache__
│   ├── mcp
│   │   ├── client.py
│   │   └── server.py
│   ├── models
│   │   ├── car.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── neo4j_connection.py
│   ├── neo4j_repo.py
│   ├── tasks
│   │   ├── celery_app.py
│   │   └── fetch_and_store_cars_task.py
│   └── web
│       ├── cars
│       ├── __init__.py
│       └── users
├── config.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── scripts
│   ├── beat.sh
│   └── worker.sh
└── README.md
```


### Docker Commands

1. Build and start containers:

```bash
docker compose up --build
```

2. Check running containers:

```bash
docker ps
```

3. Stop and remove containers:

```bash
docker compose down
```

## Demonstrate Celery Calling MCP

1. Trigger the task manually:

```bash
sudo docker compose exec celery_worker celery -A app.tasks.celery_app.celery call sync_from_back4app
```

2. Expected log output on worker container:

```
worker  | Task sync_from_back4app[<task-id>] received
worker  | fetch_and_store_cars: inserted=0
worker  | Task sync_from_back4app[<task-id>] succeeded in <time>s: {'inserted': 0}
```

3. Explanation:

   * `sync_from_back4app` Celery task internally calls MCP service.
   * MCP handles the collection and storage of car data.
   * The `inserted` value indicates how many new records were added.
