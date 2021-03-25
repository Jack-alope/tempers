import json

from database import get_db
from crud import crud_experiment, crud_bio_reactor, crud_post
from schemas import schema_experiment, schema_bio_reactor

from fastapi import APIRouter, Request, Form,  Depends, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/addExperiment", response_model=schema_experiment.Experiment, tags=["addStuff"])
def add_Experiment(experiment: schema_experiment.ExperimentBase, db: Session = Depends(get_db)):
    new_experiment = crud_experiment.create_experiment(db, experiment)
    return new_experiment


@router.post("/addBioReactor", response_model=schema_bio_reactor.BioReactorBase, tags=["addStuff"])
def add_BioReactor(bio_reactor: schema_bio_reactor.BioReactorCreate, db: Session = Depends(get_db)):
    new_bio_reactor = crud_bio_reactor.create_bio_reactor(db, bio_reactor)

    [crud_post.create_post(db, post, new_bio_reactor.id)
     for post in bio_reactor.posts]

    return bio_reactor
