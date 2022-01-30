"""
Fastapi Main
"""
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from log_config import init_loggers
from database import init_db
from routers import (
    router_upload,
    router_tracking,
    router_analysis,
    router_experiment,
    router_bio_reactor,
    router_video,
    router_calibration_set,
    router_tissue,
)

init_loggers()
log = logging.getLogger("main_logger")

init_db()

app = FastAPI()
app.include_router(router_upload.router)
app.include_router(router_tracking.router)
app.include_router(router_analysis.router)
app.include_router(router_experiment.router)
app.include_router(router_bio_reactor.router)
app.include_router(router_video.router)
app.include_router(router_calibration_set.router)
app.include_router(router_tissue.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
log.info("New Run Started")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
