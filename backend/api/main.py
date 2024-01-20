import os
from logging import getLogger

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.routers import router

logger = getLogger(__name__)

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static/results'

isdir = os.path.isdir(UPLOAD_FOLDER)
if not isdir:
    os.makedirs(UPLOAD_FOLDER)

isdir = os.path.isdir(STATIC_FOLDER)
if not isdir:
    os.makedirs(STATIC_FOLDER)

app = FastAPI(
    title = "Torch serving",
    description = "Serve torch models using fastapi and celery",
    version = "0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
app.include_router(router, prefix="", tags=[""])