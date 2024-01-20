import os
import uuid
import logging
from typing import Any, Dict, List

import requests
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from celery_tasks.tasks import predict_image
from celery.result import AsyncResult 

from .schema import Task, Prediction

router = APIRouter()

UPLOAD_FOLDER = 'uploads'


@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.post('/api/process')
async def process(files: List[UploadFile] = File(...)):
    tasks = []
    try:
        for file in files:
            d = {}
            try:
                name = str(uuid.uuid4()).split('-')[0]
                ext = file.filename.split('.')[-1]
                file_name = f'{UPLOAD_FOLDER}/{name}.{ext}'
                with open(file_name, 'wb+') as f:
                    f.write(file.file.read())
                f.close()

                #print(os.path.join('backend', file_name))
                task_id = predict_image.delay(os.path.join('backend', file_name))
                d['task_id'] = str(task_id)
                d['status'] = 'PROCESSING'
                d['url_result'] = f'/api/result/{task_id}'
            except Exception as ex:
                logging.info(ex)
                d['task_id'] = str(task_id)
                d['status'] = 'ERROR'
                d['url_result'] = ''
            tasks.append(d)
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        logging.info(ex)
        return JSONResponse(status_code=400, content=[])


@router.get('/api/result/{task_id}', response_model=Prediction)
async def result(task_id: str):
    task = AsyncResult(task_id)

    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': task.status, 'result': ''})

    task_result = task.get()
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task_result.get('status'), 'result': task_result.get('result')})


@router.get('/api/status/{task_id}', response_model = Prediction)
async def status(task_id: str):
    task = AsyncResult(task_id)
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': ''})