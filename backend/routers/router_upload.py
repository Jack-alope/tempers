"""
Router for upload
"""
import os
from typing import List
import shutil
import json
from dataclasses import asdict

from werkzeug.utils import secure_filename

from fastapi import APIRouter, Form, File, UploadFile, Depends

from sqlalchemy.orm import Session

import pandas as pd


import models
from database import get_db
from crud import crud_video, crud_tissue, crud_tissue_tracking, \
    crud_experiment, crud_bio_reactor, crud_post, crud_tissue_caculations
from schemas import schema_video, schema_tissue, schema_experiment


router = APIRouter()

UPLOAD_FOLDER = models.UPLOAD_FOLDER


def _save_file(file, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file, buffer)


def save_video_file(vid_info, vid_file, database_session):
    """Saves vid file to disk and adds to db"""
    date_string = vid_info.date_recorded.strftime('%m_%d_%Y')

    experiment_info = crud_experiment.get_experiment(
        database_session, vid_info.experiment_id)

    # gets save loaction uploadfolder/expermentnum/date/vid
    where_to_save = os.path.join(
        UPLOAD_FOLDER, experiment_info.experiment_idenifer, 'videos')

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
    _save_file(vid_file.file, path_to_file)

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

    _save_file(file.file, path_to_file)

    vid = crud_video.create_video(database_session, vid_info)
    return (vid.id, path_to_file)


def add_tissues(tissue_li: List[schema_tissue.TissueCreate],
                vid_id: int, database_session: Session):
    """Adds tissues to databse"""

    tissue_id = 0

    for tissue in tissue_li:
        tissue_obj = schema_tissue.TissueCreate.parse_obj(tissue)
        tissue_obj.vid_id = vid_id
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
        vid_info.tissues, vid_id, database_session)

    if extension == "csv":
        dataframe = pd.read_csv(tup[1])
        dataframe["tissue_id"] = tissue.id
        crud_tissue_tracking.create_tissue_tracking(
            database_session, tissue.id, dataframe)
        models.delete_file(tup[1])

    return {200: "OK"}


def _unzip_and_delete(archive_path, where_to_save):
    shutil.unpack_archive(archive_path, where_to_save)
    os.remove(archive_path)


def _add_experiment_to_db(database_session, experiment_info, bio_ids, post_ids):

    # REVIEW: Proablly dont want to just delete
    crud_experiment.delete_experiment(database_session, experiment_info.id)
    crud_experiment.delete_experiment_by_identifer(
        database_session, experiment_info.experiment_idenifer)

    delattr(experiment_info, "id")
    delattr(experiment_info, "vids")

    experiment = crud_experiment.create_experiment(
        database_session, experiment_info)

    return (experiment.id, experiment.experiment_idenifer)


def _add_bio_reactos_to_db(database_session, bio_reactors_info):
    bio_ids = {}
    post_ids = {}
    for bio in bio_reactors_info:
        print("hiii")
        print(bio.id)
        old_id = bio.id
        # REVIEW: Probally dont want to just delete
        crud_bio_reactor.delete_bio_reactor(database_session, old_id)
        posts = bio.posts
        delattr(bio, "id")
        delattr(bio, "posts")
        new_bio = crud_bio_reactor.create_bio_reactor(database_session, bio)
        bio_ids[old_id] = new_bio.id
        for post in posts:
            old_post_id = post.id
            delattr(post, "id")
            new_post = crud_post.create_post(
                database_session, post, new_bio.id)
            post_ids[old_post_id] = new_post.id

    return (bio_ids, post_ids)


def _add_vids_to_db(database_session: Session, vids,
                    experiment_id: int, bio_ids: dict, post_ids: dict):
    for vid in vids:
        #old_id = vid.id
        # REVIEW: Probally dont want to just delete
        #crud_video.delete_video(database_session, old_id)
        tissues = vid.tissues
        # delattr(vid, "id")
        # delattr(vid, "tissues")
        bio_id = bio_ids[vid.bio_reactor_id]
        print(bio_id)
        delattr(vid, "bio_reactor_id")
        vid = schema_video.VideoCreate(
            **dict(vid), experiment_id=experiment_id,
            bio_reactor_id=bio_id,)
        # setattr(vid, "experiment_id", experiment_id)
        # setattr(vid, "bio_reactor_id", bio_ids[vid.bio_reactor_id])
        new_vid_id = crud_video.create_video(database_session, vid).id

        for tissue in tissues:
            post_id = post_ids[tissue.post_id]
            delattr(tissue, "post_id")
            tissue_caculated = dict(tissue.tissue_caculated_data)
            delattr(tissue, "tissue_caculated_data")

            tissue = schema_tissue.Tissue(
                **dict(tissue), vid_id=new_vid_id, post_id=post_id)
            new_tissue_id = crud_tissue.create_tissue(
                database_session, tissue).id

            crud_tissue_caculations.create(
                database_session, tissue_caculated, new_tissue_id)


def _expirment_file_unpack(database_session,  dir_path):
    print("here")
    print(dir_path)

    json_file, = [os.path.join(dir_path, f) for f in os.listdir(
        dir_path) if f.endswith('.json')]

    with open(json_file) as f:
        data: schema_experiment.ExperimentDownload = schema_experiment.ExperimentDownload(
            **json.load(f))

    vids = data.experiment.vids

    bio_ids, post_ids = _add_bio_reactos_to_db(
        database_session, data.bio_reactors)
    experiment_id, experiment_idenifer = _add_experiment_to_db(
        database_session, data.experiment, bio_ids, post_ids)

    _add_vids_to_db(database_session, vids,
                    experiment_id, bio_ids, post_ids)

    return experiment_idenifer


@router.post("/upload/experiment_archive", tags=["upload", "experiment"])
async def upload_experiment(file: UploadFile = File(...),
                            database_session: Session = Depends(get_db)):

    # TODO: add Tracking data

    where_to_save = os.path.join(UPLOAD_FOLDER, "temp")
    models.check_path_exisits(where_to_save)

    safe_filename = secure_filename(file.filename)

    archive_path = os.path.join(where_to_save, safe_filename)

    _save_file(file.file, archive_path)

    _unzip_and_delete(archive_path, where_to_save)

    experiment_idenifer = _expirment_file_unpack(
        database_session, where_to_save)

    shutil.move(os.path.join(where_to_save, "videos"), os.path.join(
        UPLOAD_FOLDER, experiment_idenifer, "videos"))

    shutil.rmtree(where_to_save)

    return {200: "OK"}
