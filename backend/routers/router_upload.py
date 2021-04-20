"""
Router for upload
"""
import os
from typing import List
import shutil
import json

from werkzeug.utils import secure_filename

from fastapi import APIRouter, Form, File, UploadFile, Depends

from sqlalchemy.orm import Session

import pandas as pd


import models
from database import get_db
from crud import crud_video, crud_tissue, crud_tissue_tracking, crud_experiment, crud_bio_reactor
from schemas import schema_video, schema_tissue


router = APIRouter()

UPLOAD_FOLDER = models.UPLOAD_FOLDER


def save_video_file(vid_info, vid_file, database_session):
    """Saves vid file to disk and adds to db"""
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')

    experiment_info = crud_experiment.get_experiment(
        database_session, vid_info.experiment_id)

    # gets save loaction uploadfolder/expermentnum/date/vid
    where_to_save = os.path.join(
        UPLOAD_FOLDER, experiment_info.experiment_idenifer, date_string, 'videoFiles')

    # cheacks to make sure the save location exists if not exists
    models.check_path_exisits(where_to_save)

    orginal_filename = vid_file.filename
    extenstion = orginal_filename.rsplit('.', 1)[1].lower()

    bio_reactor_info = crud_bio_reactor.get_bio_reactor(
        database_session, vid_info.bio_reactor_id)
    # makes new file name for the vid format date_frewnum_bionum.ext
    new_filename = f"{date_string}_Freq{str(vid_info.frequency)}_Bio\
        {str(bio_reactor_info.bio_reactor_number)}.{extenstion}"

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    vid_info.save_location = path_to_file

    # saves file
    with open(path_to_file, "wb") as buffer:
        shutil.copyfileobj(vid_file.file, buffer)

    vid = crud_video.create_video(database_session, vid_info)

    return vid.id


def save_csv_file(vid_info, file, database_session):
    """Saves csv to disk and addes to db with fake vid"""
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')
    where_to_save = os.path.join(
        UPLOAD_FOLDER, vid_info.experiment_id, date_string, 'csvfiles')
    models.check_path_exisits(where_to_save)

    new_filename = date_string + "_" + \
        "Freq" + str(vid_info.frequency) + "_T1.csv"

    # makes sure file name is correct formats
    safe_filename = secure_filename(new_filename)

    vid_info.save_location = None

    # creates path to file
    path_to_file = os.path.join(where_to_save, safe_filename)

    with open(path_to_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    vid = crud_video.create_video(database_session, vid_info)
    return (vid.id, path_to_file)


def add_tissues(tissue_li: List[schema_tissue.TissueCreate],
                bio_reactor_id: int, vid_id: int, database_session: Session):
    """Adds tissues to databse"""

    tissue_id = 0

    for tissue in tissue_li:
        tissue_obj = schema_tissue.TissueCreate.parse_obj(tissue)
        tissue_obj.vid_id = vid_id
        tissue_obj.bio_reactor_id = bio_reactor_id
        tissue_id = crud_tissue.create_tissue(database_session, tissue_obj)

    return tissue_id


@router.post("/upload", tags=["upload"])
async def upload(info: str = Form(...), file: UploadFile = File(...),
                 database_session: Session = Depends(get_db)):
    """Upload csv or vid"""
    # TODO Add schema to this form and file make it weird
    vid_json: schema_video.VideoCreate = json.loads(info)
    vid_info = schema_video.VideoCreate.parse_obj(vid_json)

    extension = file.filename.split(".")[-1]

    tup = ()

    if extension == "csv":
        tup = save_csv_file(vid_info, file, database_session)
        vid_id = tup[0]

    else:
        vid_id = save_video_file(vid_info, file, database_session)

    tissue = add_tissues(
        vid_info.tissues, vid_info.bio_reactor_id, vid_id, database_session)

    if extension == "csv":
        dataframe = pd.read_csv(tup[1])
        dataframe["tissue_id"] = tissue.id
        crud_tissue_tracking.create_tissue_tracking(
            database_session, tissue.id, dataframe)
        if os.path.exists(tup[1]):
            os.remove(tup[1])
            models.delete_empties()
        else:
            print("The file does not exist")

    return {200: "OK"}
