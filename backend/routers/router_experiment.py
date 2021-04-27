"""
Router for experiment
"""
import json
from typing import List
from dataclasses import asdict
import shutil


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
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


@router.get("/experimentsJSON/{experiment_id}", tags=["Experiment"])
def json_experiment(experiment_id: int, database_session=Depends(get_db)):

    experiment_info = crud_experiment.get_experiment(
        database_session, experiment_id)

    def vid_json(vid):
        save_location = vid.save_location
        vid.save_location = "videos/" + vid.save_location.split("/")[-1]
        tissues = [x for x in vid.tissues]
        return (vid.bio_reactor_id, save_location, tissues)

    def tissue_tracking_to_csv(database_session: Session, tissue: int, file_path: str):
        with open(f"{file_path}{tissue.tissue_number}_{tissue.tissue_type}_{tissue.id}.csv", "w") as outfile:
            dataframe = crud_tissue_tracking.get_tracking_by_id(
                database_session, tissue.id)
            if not dataframe.empty:
                dataframe.to_csv(outfile)

    vid_info = [vid_json(x) for x in experiment_info.vids]

    bio_reactor_ids = set()
    save_locations = []
    tissues = []

    for x in vid_info:
        bio_reactor_ids.add(x[0])
        save_locations.append(x[1])
        for j in x[2]:
            tissues.append(j)

    experiment = schema_experiment.Experiment(**asdict(experiment_info))

    bio_reactors = crud_bio_reactor.get_bio_reactors_by_li_id(
        database_session, bio_reactor_ids)

    bio_reactors = [schema_bio_reactor.BioReactorFull(
        **asdict(i)) for i in bio_reactors]

    save_info = schema_experiment.ExperimentDownload(
        experiment=experiment, bio_reactors=bio_reactors)

    file_path = f"static/archive/{experiment_info.experiment_idenifer}/"
    csv_path = f"{file_path}csvs/"
    video_path = f"{file_path}videos/"
    zips = "static/archive/zips/"
    models.check_path_exisits(file_path)
    models.check_path_exisits(csv_path)
    models.check_path_exisits(video_path)
    models.check_path_exisits(zips)

    with open(f"{file_path}{experiment_info.experiment_idenifer}_\
        {experiment_info.start_date}.json", "w") as outfile:
        json.dump(jsonable_encoder(save_info), outfile, indent=1)

    for tissue in tissues:
        tissue_tracking_to_csv(database_session, tissue, csv_path)

    for vid_path in save_locations:
        src = vid_path
        dst = f"{video_path}{vid_path.split('/')[-1]}"
        shutil.copyfile(src, dst)

    shutil.make_archive(
        f"{zips}{experiment_info.experiment_idenifer}_{experiment_info.start_date}", 'zip', file_path)

    shutil.rmtree(file_path)

    return {f"{zips}{experiment_info.experiment_idenifer}_{experiment_info.start_date}.zip"}
