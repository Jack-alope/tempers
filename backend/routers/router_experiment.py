"""
Router for experiment
"""
import json
from typing import List, Set
import shutil
import os
import logging
from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from database import get_db
from crud import (
    crud_experiment,
    crud_bio_reactor,
    crud_tissue_tracking,
    crud_calibration_set,
)
from schemas import schema_experiment, schema_bio_reactor, schema_calibration_set
import models


router = APIRouter()


def _check_experiment_has_vids(experiment):
    """
    Accepts a models.Experiment and returns
    experiment schema with attrbure has vids
    """
    has_vids = bool(experiment.vids)
    experiment = schema_experiment.Experiment(**experiment.__dict__)
    if has_vids:
        setattr(experiment, "has_vids", True)
    else:
        setattr(experiment, "has_vids", False)

    return experiment


@router.get(
    "/experiments",
    response_model=List[schema_experiment.Experiment],
    tags=["Experiment"],
)
def read_experiments(database_session: Session = Depends(get_db)):
    """returns all experiment"""
    experiments = crud_experiment.get_experiments(database_session)
    if not experiments:
        raise HTTPException(status_code=404, detail="Experiments not found")

    experiments = [_check_experiment_has_vids(experiment) for experiment in experiments]

    return experiments


@router.delete("/experiment/{exp_id}", tags=["Experiment"])
def delete_experiment(exp_id: str, database_session: Session = Depends(get_db)):
    """Delete expirment by id"""
    return crud_experiment.delete_experiment(database_session, exp_id)


@router.post(
    "/addExperiment",
    response_model=schema_experiment.ExperimentWithVids,
    status_code=status.HTTP_201_CREATED,
    tags=["Experiment"],
)
def add_experiment(
    experiment: schema_experiment.ExperimentBase,
    database_session: Session = Depends(get_db),
):
    """Add experiment"""
    if crud_experiment.check_experiment_id_exsits(database_session, experiment.id):
        raise HTTPException(status.HTTP_409_CONFLICT)
    elif experiment.id == "":
        # REVIEW: Better error message
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE)

    new_experiment = crud_experiment.create_experiment(database_session, experiment)
    return new_experiment


@router.post("/experiment_exist", tags=["Experiment", "upload"])
def check_experiment_exists(
    experiment_identifier: str = Query(...), database_session: Session = Depends(get_db)
):
    """Router to check if the experiment identiyer is used retunes true if it exsits"""
    return crud_experiment.check_experiment_id_exsits(
        database_session, experiment_identifier
    )


def _tissue_tracking_to_csv(database_session: Session, tissues, file_path: str):
    """
    Accepts list of tissues objests opens and saves a CVS file with the
    tracking data from that file
    """
    for tissue in tissues:
        with open(
            f"{file_path}{tissue.tissue_number}_{tissue.tissue_type}_{tissue.id}.csv",
            "w",
        ) as outfile:
            dataframe = crud_tissue_tracking.get_tracking_by_id(
                database_session, tissue.id
            )
            if not dataframe.empty:
                dataframe.to_csv(outfile)


@router.get("/experimentsJSON/{experiment_id}", tags=["Experiment"])
def json_experiment(
    background_tasks: BackgroundTasks,
    experiment_id: str,
    database_session: Session = Depends(get_db),
):
    """
    Genrates a JSON of experiment data and csv for tissue tracking database
    zips that with the vid files and sends the zip as a file response
    REVIEW: it isnt very quick, its the ziping that is slow, file response also slow
    REVIEW: Use steam file instead of saving then deleting
    """

    experiment_info = crud_experiment.get_experiment(database_session, experiment_id)
    # Path to the base of the experiment folder
    file_path = f"{models.UPLOAD_FOLDER}/{experiment_info.id}/"
    csv_path = f"{file_path}csvs/"
    experiment_info_file_path = (
        f"{file_path}{experiment_info.id}_{experiment_info.start_date}"
    )
    zip_file_path = f"{models.UPLOAD_FOLDER}/zips/{experiment_info.id}"

    models.check_path_exisits(file_path)
    models.check_path_exisits(csv_path)
    models.check_path_exisits(f"{models.UPLOAD_FOLDER}/zips/")

    bio_reactor_ids: Set[int] = set()
    calibration_set_identifers: Set[str] = set()
    tissues = []

    # List comp goes creats list of tup (bio_ids, tissues) used in expetiment
    # REVIEW: Would like to cut out the nested for loops
    for x in [
        (vid.bio_reactor_id, vid.calibration_set_identifier, vid.tissues)
        for vid in experiment_info.vids
    ]:
        # Adds bio id to set
        bio_reactor_ids.add(x[0])
        # Adds calibration ids to set
        calibration_set_identifers.add(x[1])
        for j in x[2]:
            # iterrates over tissues in vid
            # Appends tissue to list of tissue
            tissues.append(j)

    bio_reactors = crud_bio_reactor.get_bio_reactors_as_schema(
        database_session, bio_reactor_ids
    )

    calibration_sets = [
        schema_calibration_set.CalibrationSet(**asdict(i))
        for i in crud_calibration_set.get_calibration_sets_by_li_identifier(
            database_session, calibration_set_identifers
        )
    ]

    with open(f"{experiment_info_file_path}.json", "w") as outfile:
        # Saves json file with the experiemtn data by using the experiment download schema

        json.dump(
            jsonable_encoder(
                schema_experiment.ExperimentDownload(
                    experiment=schema_experiment.ExperimentWithVids(
                        **asdict(experiment_info)
                    ),
                    bio_reactors=bio_reactors,
                    calibration_sets=calibration_sets,
                )
            ),
            outfile,
            indent=1,
        )

    # Pass in list of tissues and path to csv folder
    # saves csv of tracking data for each tissue
    _tissue_tracking_to_csv(database_session, tissues, csv_path)

    # Zips the experimet folder
    # Including experiment info json, vidfolder and csv folder
    shutil.make_archive(zip_file_path, "zip", file_path)

    # removes the csv files and folder
    shutil.rmtree(csv_path)
    # deletes experiment info file
    os.remove(f"{experiment_info_file_path}.json")

    # Adds backgroud task to delete zip archive after the file is returned
    background_tasks.add_task(models.delete_file, f"{zip_file_path}.zip")

    return FileResponse(f"{zip_file_path}.zip")
