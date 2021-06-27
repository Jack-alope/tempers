"""
Fastapi Main
"""
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import router_upload, router_tracking, router_analysis, \
    router_experiment, router_bio_reactor, router_video, router_calibration_set

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG, filename='main.log')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_upload.router)
app.include_router(router_tracking.router)
app.include_router(router_analysis.router)
app.include_router(router_experiment.router)
app.include_router(router_bio_reactor.router)
app.include_router(router_video.router)
app.include_router(router_calibration_set.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
logging.info("New Run Started")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
