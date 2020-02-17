# sorcer
Service Oriented Computing Scheduler Environment

## Using
Redis - message broker

## Workflow

Our goal is to develop a Flask application that works in conjunction with Redis Queue to handle long-running processes outside the normal request/response cycle.

* The end user kicks off a new task via a POST request to the server-side
* Within the view, a task is added to the queue and the task id is sent back to the client-side
* Using AJAX, the client continues to poll the server to check the status of the task while the task itself is running in the background

## Installing Redis

```sh
# Redis help
https://redis.io/topics/quickstart

# Redis.exe for Windows Download (skip if Linux)
https://github.com/microsoftarchive/redis/releases

# Installation (Skip if Windows)
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

# Run redis (Window Terminal 1)
redis-server

# Check if Redis is working (Window Terminal 2)
redis-cli ping

# Enable monitoring
redis.cli monitor (Window Terminal 3)
```

## Quick Start

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Open your browser to http://localhost:5004 to view the app or to http://localhost:9181 to view the RQ dashboard.

## Want to learn how to build this?

https://testdriven.io/asynchronous-tasks-with-flask-and-redis-queue