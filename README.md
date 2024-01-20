# Asynchronous Torch Serving using Celery

This project shows how to serve a pytorch model using Celery, Redis and RabbitMQ to serve users asynchronously.

## Installation

1. Build containers

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