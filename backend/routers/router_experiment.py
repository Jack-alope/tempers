"""
Router for experiment
"""
import json
from typing import List
from dataclasses import asdict
import shutil
import os

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from crud import crud_experiment, crud_bio_reactor, crud_tissue_tracking
from schemas import schema_experiment, schema_bio_reactor
import models


router = APIRouter()


@router.get("/experiments", response_model=List[schema_experiment.ExperimentShow],
            tags=["Experiment"])
def read_experiments(database_session: Session = Depends(get_db)):
    """retunrs all experiment"""
    experiments = crud_experiment.get_experiments(database_session)
    if not experiments:
        raise HTTPException(status_code=404, detail="Experiments not found")
    return experiments


@router.delete("/experiment/{exp_id}", tags=["Experiment"])
def delete_experiment(exp_id: int, database_session: Session = Depends(get_db)):
    """Delete expirment by id"""
    return crud_experiment.delete_experiment(database_session, exp_id)


@router.post("/addExperiment", response_model=schema_experiment.Experiment,
             status_code=status.HTTP_201_CREATED, tags=["Experiment"])
def add_experiment(experiment: schema_experiment.ExperimentBase,
                   database_session: Session = Depends(get_db)):
    """Add experiment"""
    if crud_experiment.check_experiment_idetifyer_exsits(
            database_session, experiment.experiment_idenifer):
        raise HTTPException(status.HTTP_409_CONFLICT)
    new_experiment = crud_experiment.create_experiment(
        database_session, experiment)
    return new_experiment


@router.post("/experiment_exist/",
             tags=["experiment", "upload"])
def check_experiment_exists(experiment_identifier: str = Query(...),
                            database_session: Session = Depends(get_db)):
    return crud_experiment.check_experiment_idetifyer_exsits(
        database_session, experiment_identifier)


def _tissue_tracking_to_csv(database_session: Session, tissues, file_path: str):
    for tissue in tissues:
        with open(f"{file_path}{tissue.tissue_number}_{tissue.tissue_type}_{tissue.id}.csv",
                  "w") as outfile:
            dataframe = crud_tissue_tracking.get_tracking_by_id(
                database_session, tissue.id)
            if not dataframe.empty:
                dataframe.to_csv(outfile)


@router.get("/experimentsJSON/{experiment_id}", tags=["Experiment"])
def json_experiment(background_tasks: BackgroundTasks, experiment_id: int,
                    database_session=Depends(get_db)):
    """
    Genrates a JSON of experiment data and csv for tissue tracking database
    zips that with the vid files and sends the zip as a file response
    REVIEW: it isnt very quick, its the ziping that is slow, file response also slow
    REVIEW: Use steam file instead of saving then deleting
    """

    experiment_info = crud_experiment.get_experiment(
        database_session, experiment_id)

    file_path = f"{models.UPLOAD_FOLDER}/{experiment_info.experiment_idenifer}/"
    csv_path = f"{file_path}csvs/"
    experiment_info_file_path = \
        f"{file_path}{experiment_info.experiment_idenifer}_{experiment_info.start_date}"

    models.check_path_exisits(file_path)
    models.check_path_exisits(csv_path)

    bio_reactor_ids: {int} = set()
    tissues = []

    for x in [(vid.bio_reactor_id, vid.tissues)
              for vid in experiment_info.vids]:
        bio_reactor_ids.add(x[0])
        for j in x[1]:
            tissues.append(j)

    bio_reactors = [schema_bio_reactor.BioReactorFull(
        **asdict(i)) for i in crud_bio_reactor.get_bio_reactors_by_li_id(
        database_session, bio_reactor_ids)]

    with open(f"{experiment_info_file_path}.json", "w") as outfile:
        json.dump(jsonable_encoder(
            schema_experiment.ExperimentDownload(
                experiment=schema_experiment.Experiment(
                    **asdict(experiment_info)),
                bio_reactors=bio_reactors)), outfile, indent=1)

    _tissue_tracking_to_csv(database_session, tissues, csv_path)

    shutil.make_archive(experiment_info_file_path,
                        "zip", file_path)

    shutil.rmtree(csv_path)
    os.remove(f"{experiment_info_file_path}.json")

    background_tasks.add_task(
        models.delete_file, f"{experiment_info_file_path}.zip")

    return FileResponse(f"{experiment_info_file_path}.zip")
