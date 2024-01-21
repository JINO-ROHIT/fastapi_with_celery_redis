# Asynchronous Torch Serving using Celery

This project shows how to serve a pytorch model using Celery, Redis and RabbitMQ to serve users asynchronously.


## Project Overview

PyTorch: A simple resnet50 model with pretrained weights for classification.

Celery: A distributed task queue system in Python, allowing asynchronous processing of tasks, making it suitable for background jobs.

Redis: An in-memory data store often used as a caching mechanism, here employed for storing and retrieving intermediate results in the distributed system to enhance performance.

RabbitMQ: A message broker that facilitates communication between different parts of a distributed application, ensuring efficient and reliable message passing between the API and Celery workers.

## Installation

1. ### Build containers

```bash
make serve
```

2. Check application health
```bash
curl -X 'GET' \
  'http://localhost:8000/health' \
  -H 'accept: application/json'
```

Response 
```json
{
  "health": "ok"
}

```

3. Call the process api
```bash
curl -X 'POST' \
  'http://localhost:8000/api/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F '<file>'
```

Response 
```json
[
  {
    "task_id": "70471dd9-7cac-49a1-9088-dd95e4f2d2fe",
    "status": "PROCESSING",
    "url_result": "/api/result/70471dd9-7cac-49a1-9088-dd95e4f2d2fe"
  }
]

```

4. Check the status in the queue
```bash
curl -X 'GET' \
  'http://localhost:8000/api/status/<task_id>' \
  -H 'accept: application/json'
```

Response 
```json
{
  "task_id": "70471dd9-7cac-49a1-9088-dd95e4f2d2fe",
  "status": "PENDING",
}
```

5. Check the result
```bash
curl -X 'GET' \
  'http://localhost:8000/api/result/<task_id>' \
  -H 'accept: application/json'
```

Response 
```json
{
  "task_id": "70471dd9-7cac-49a1-9088-dd95e4f2d2fe",
  "status": "SUCCESS",
  "result": "suit : 35%"
}
```

6. Stop the service

```bash
make stop
```
