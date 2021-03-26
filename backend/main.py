import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine, get_db
from routers import router_upload, router_tracking, router_analysis, router_experiment, router_bio_reactor



logging.basicConfig(filename='main.log',
                    format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logging.warning("New Run Starts Here")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router_upload.router)
app.include_router(router_tracking.router)
app.include_router(router_analysis.router)
app.include_router(router_experiment.router)
app.include_router(router_bio_reactor.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
